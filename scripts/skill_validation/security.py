"""Bounded, deterministic static security checks for untrusted skill text.

This module never executes candidate content, decodes payloads, or makes network
requests. Findings intentionally describe categories rather than source excerpts.
"""

from __future__ import annotations

import re
import shlex
from typing import Any

from .models import Finding, SourceFile, finding
from .policy import validate_policy


_PEM_MARKER = re.compile(
    r"-----(BEGIN|END) ((?:(?:RSA|EC|OPENSSH|DSA|ENCRYPTED) )?PRIVATE KEY)-----", re.I
)
_GH_TOKEN = re.compile(r"(?<![A-Za-z0-9_])ghp_[A-Za-z0-9]{36}(?![A-Za-z0-9_])")
_GH_PAT = re.compile(r"(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9_]{82}(?![A-Za-z0-9_])")
_AWS_ID = re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")
_AWS_SECRET = re.compile(
    r"(?i)(?:aws[_ -]?)?(?:secret[_ -]?(?:access[_ -]?)?key)\s*[=:]\s*['\"]?([A-Za-z0-9/+=]{40})"
)
_SENSITIVE = re.compile(
    r"(?i)(?:\.ssh(?:/|\b)|\.aws/credentials\b|\.env(?:\b|/)|"
    r"(?:chrome|chromium|firefox|safari|edge)[^\n]{0,60}(?:cookie|login|credential|profile)|"
    r"(?:cookie|login|credential)[^\n]{0,60}(?:chrome|chromium|firefox|safari|edge)|"
    r"(?:os\.)?environ\b|process\.env\b|printenv\b|env\s*\(|getenv\s*\()"
)
_CURL = re.compile(r"\bcurl\b", re.I)
_EXTERNAL = re.compile(r"https?://[^\s'\"<>]+", re.I)
_DOWNLOAD = re.compile(r"\b(?:curl|wget)\b", re.I)
_EXEC = re.compile(r"\b(?:sh|bash|python(?:3)?|perl|ruby|node)\b", re.I)
_BASE64 = re.compile(r"\bbase64\b", re.I)
_DECODE = re.compile(r"(?:-d\b|--decode\b|--decode\s+)", re.I)
_DYNAMIC_EXEC = re.compile(r"\b(?:eval|exec)\b|\b(?:sh|bash)\s+-c\b|\|\s*(?:ba)?sh\b", re.I)
_PERSISTENCE = re.compile(
    r"(?i)(?:\.bashrc|\.zshrc|\.profile|\.config/autostart|launchagents|launchdaemons|"
    r"crontab|cron\.d|systemd/(?:user/)?(?:[^\s]+\.service)|\.github/workflows|"
    r"(?:agent|assistant)[^\n]{0,40}(?:config|settings)|(?:config|settings)[^\n]{0,40}(?:agent|assistant))"
)
_SENSITIVE_FILE = re.compile(
    r"(?i)(?:^|[/\\])\.ssh(?:[/\\]|$)|\.aws[/\\]credentials(?:[/\\]|$)|"
    r"(?:^|[/\\])\.env(?:[A-Za-z0-9_.-]*)(?:[/\\]|$)|"
    r"(?:chrome|chromium|firefox|safari|edge|brave)[^/\\]*(?:[/\\].*)?"
    r"(?:cookies?|login data|logins\.json|key[34]?\.db|places\.sqlite)"
)
_MUTATION = re.compile(
    r"(?i)\b(?:write|append|modify|edit|overwrite|install|add|copy|move|create|touch|sed\s+-i|"
    r"escreva|escrever|acrescente|acrescentar|modifique|modificar|altere|alterar|edite|editar|"
    r"sobrescreva|sobrescrever|instale|instalar|adicione|adicionar|copie|copiar|mova|mover|"
    r"crie|criar|toque|tocar)\b"
)
_IGNORE_SAFETY = re.compile(
    r"(?i)(?:\bignore\b[^\n]{0,55}\b(?:safety|approval|permission|policy|guardrail|security)\b|"
    r"\b(?:bypass|skip|disable|override)\b[^\n]{0,55}\b(?:approval|safety|security|policy|review)\b|"
    r"\b(?:ignore|desconsidere|ignora|ignore as|ignore todas)\b[^\n]{0,55}\b(?:instru[cç][oõ]es|regras|aprova[cç][aã]o|seguran[cç]a|pol[ií]tica)\b)"
)
_HIDE = re.compile(
    r"(?i)(?:\b(?:hide|conceal|cover up|keep secret)\b[^\n]{0,55}\b(?:action|change|command|activity|from (?:the )?user|reviewer)\b|"
    r"\b(?:hide|oculte|esconda|ocultar|esconder)\b[^\n]{0,55}\b(?:a[cç][aã]o|atividade|altera[cç][aã]o|do usu[aá]rio)\b)"
)
_SUPPRESS_AUDIT = re.compile(
    r"(?i)(?:\b(?:disable|delete|clear|suppress|remove)\b[^\n]{0,55}\b(?:audit|logs?|history|trail)\b|"
    r"\b(?:desative|apague|limpe|remova|suprima)\b[^\n]{0,55}\b(?:logs?|hist[oó]rico|auditoria|rastros?)\b)"
)

_SCRIPT_SUFFIXES = (".sh", ".bash", ".zsh", ".py", ".js", ".mjs", ".cjs", ".rb", ".pl", ".ps1")
_WINDOW = 20


def _is_markdown(path: str) -> bool:
    return path.lower().endswith((".md", ".markdown"))


def _is_executable(source: SourceFile) -> bool:
    return source.mode == "100755" or source.path.lower().endswith(_SCRIPT_SUFFIXES)


def _shell_continues(line: str) -> bool:
    """Recognize a trailing shell continuation only outside comments/single quotes."""
    quote: str | None = None
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if quote == "'":
            if char == "'":
                quote = None
            continue
        if char == "\\":
            escaped = True
            continue
        if quote == '"':
            if char == '"':
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char == "#" and (index == 0 or line[index - 1].isspace()):
            return False
    return escaped


def _shell_statements(text: str, *, markdown: bool = False) -> list[tuple[int, list[str] | None]]:
    """Tokenize shell-like statements with quote-aware comments and separators."""
    statements: list[tuple[int, list[str] | None]] = []
    buffer = ""
    start = 1
    for number, line in enumerate(text.splitlines(), 1):
        if not buffer:
            start = number
        piece = line.rstrip()
        continued = _shell_continues(piece)
        buffer += (piece[:-1] if continued else piece) + " "
        if continued:
            continue
        shell_text = buffer.replace("`", " ") if markdown else buffer
        try:
            lexer = shlex.shlex(shell_text, posix=True, punctuation_chars=";&|>")
            lexer.whitespace_split = True
            lexer.commenters = "#"
            tokens = list(lexer)
        except ValueError:
            statements.append((start, None))
            buffer = ""
            continue
        statement_tokens: list[str] = []
        for token in tokens:
            if token in {";", "&&", "||"}:
                if statement_tokens:
                    statements.append((start, statement_tokens))
                    statement_tokens = []
            else:
                statement_tokens.append(token)
        if statement_tokens:
            statements.append((start, statement_tokens))
        buffer = ""
    if buffer.strip():
        shell_text = buffer.replace("`", " ") if markdown else buffer
        try:
            lexer = shlex.shlex(shell_text, posix=True, punctuation_chars=";&|>")
            lexer.whitespace_split = True
            lexer.commenters = "#"
            tail = list(lexer)
        except ValueError:
            statements.append((start, None))
        else:
            if tail:
                statements.append((start, tail))
    return statements


def _curl_uploads(tokens: list[str], markdown: bool) -> tuple[bool, bool, bool]:
    """Return (external URL, confirmed sensitive file, uncertain file operand)."""
    normalized = [token.strip("`") if markdown else token for token in tokens]
    curl_index = next((i for i, token in enumerate(normalized) if token.lower() == "curl"), None)
    if curl_index is None:
        return False, False, False
    args = normalized[curl_index + 1:]
    has_external = any(_EXTERNAL.search(token.strip(".,;!?)]}")) for token in args)
    payloads: list[tuple[str, str]] = []
    i = 0
    while i < len(args):
        token = args[i]
        lower = token.lower()
        if token == "-T" or lower == "--upload-file":
            if i + 1 < len(args):
                payloads.append((args[i + 1], "upload"))
                i += 2
                continue
        elif lower in {"--data-binary", "--data", "--data-ascii", "--data-urlencode"} or token == "-d":
            if i + 1 < len(args):
                payloads.append((args[i + 1], "urlencode" if lower == "--data-urlencode" else "data"))
                i += 2
                continue
        elif lower == "--data-raw":
            # --data-raw treats @ as literal content rather than reading a file.
            i += 2 if i + 1 < len(args) else 1
            continue
        elif token == "-F" or lower == "--form":
            if i + 1 < len(args):
                payloads.append((args[i + 1], "form"))
                i += 2
                continue
        elif lower.startswith("--upload-file=") or token.startswith("-T="):
            payloads.append((token.split("=", 1)[1], "upload"))
        elif lower.startswith(("--data-binary=", "--data=", "--data-ascii=", "--data-urlencode=")) or token.startswith("-d="):
            kind = "urlencode" if lower.startswith("--data-urlencode=") else "data"
            payloads.append((token.split("=", 1)[1], kind))
        elif lower.startswith("--data-raw="):
            i += 1
            continue
        elif lower.startswith("--form=") or token.startswith("-F="):
            payloads.append((token.split("=", 1)[1], "form"))
        elif token.startswith("-T") and len(token) > 2:
            payloads.append((token[2:].lstrip("="), "upload"))
        elif token.startswith("-F") and len(token) > 2:
            payloads.append((token[2:].lstrip("="), "form"))
        elif token.startswith("-d") and len(token) > 2:
            payloads.append((token[2:].lstrip("="), "data"))
        i += 1

    sensitive = False
    uncertain = False
    for payload, kind in payloads:
        operand = payload.split(";", 1)[0]
        if kind == "upload":
            path = operand
        elif kind == "form":
            # Multipart form values use name=@file; plain name=value is data.
            value = operand.split("=", 1)[1] if "=" in operand else operand
            if not value.startswith("@"):
                continue
            path = value[1:]
        elif kind == "urlencode" and not operand.startswith("@") and "=" not in operand and "@" in operand:
            # --data-urlencode accepts name@filename in addition to @filename.
            path = operand.split("@", 1)[1]
        elif operand.startswith("@"):
            path = operand[1:]
        else:
            continue
        if _SENSITIVE_FILE.search(path):
            sensitive = True
        elif re.search(r"\$\{?[A-Za-z_][A-Za-z0-9_]*", path):
            # Variable indirection may resolve to a sensitive store; retain it
            # for human review without claiming a confirmed secret upload.
            uncertain = True
    return has_external, sensitive, uncertain


def _persistence_write(tokens: list[str]) -> bool:
    joined = " ".join(tokens)
    if not _PERSISTENCE.search(joined):
        return False
    lowered = [token.lower() for token in tokens]
    if lowered and lowered[0] == "crontab" and "-e" in lowered[1:]:
        return True
    if any(token in {">", ">>", "1>", "1>>", "2>", "2>>", "&>", "&>>"}
           for token in tokens) and any(_PERSISTENCE.search(token) for token in tokens):
        return True
    if lowered and lowered[0] in {"tee", "cp", "mv", "install", "touch", "sed"}:
        if any(_PERSISTENCE.search(token) for token in tokens[1:]):
            return True
    return bool(_MUTATION.search(joined))


def _windows(lines: list[str], size: int = _WINDOW):
    for start in range(len(lines)):
        yield start + 1, "\n".join(lines[start:start + size])


def scan_security(files: tuple[SourceFile, ...], policy: dict[str, Any]) -> tuple[Finding, ...]:
    """Scan supported text files using fixed, versioned rules and bounded windows."""
    policy = validate_policy(policy)
    max_window = min(_WINDOW, policy.get("limits", {}).get("max_window_lines", _WINDOW))
    findings: list[Finding] = []
    for source in files:
        try:
            text = source.data.decode("utf-8", errors="strict")
            if "\x00" in text:
                raise UnicodeError("binary data")
        except (UnicodeError, AttributeError):
            findings.append(finding("SEC008", "error", source.path, None,
                                    "Unsupported binary data or text encoding in scan input.",
                                    source.data if isinstance(source.data, bytes) else b""))
            continue
        lines = text.splitlines()

        # Credentials remain blocking in Markdown and fenced examples. Emit only
        # a category and line number, never a matched token or key material.
        for regex in (_GH_TOKEN, _GH_PAT):
            match = regex.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                findings.append(finding("SEC001", "error", source.path, line,
                                        "Embedded private-key or recognized credential material detected.", source.data))
                break
        if not any(item.rule_id == "SEC001" and item.path == source.path for item in findings):
            # PEM keys commonly exceed 20 lines. Pair markers in one linear
            # pass under the file-size cap, rather than applying prose windows.
            starts: dict[str, int] = {}
            pem_found = False
            for index, line in enumerate(lines):
                for marker in _PEM_MARKER.finditer(line):
                    kind, label = marker.group(1).upper(), marker.group(2).upper()
                    if kind == 'BEGIN':
                        starts.setdefault(label, index + 1)
                    elif label in starts:
                        findings.append(finding("SEC001", "error", source.path, index + 1,
                                                "Embedded private-key or recognized credential material detected.", source.data))
                        pem_found = True
                        break
                if pem_found:
                    break
        if not any(item.rule_id == "SEC001" and item.path == source.path for item in findings):
            for index, line in enumerate(lines):
                if _AWS_ID.search(line):
                    nearby = "\n".join(lines[max(0, index - 2):index + 3])
                    if _AWS_SECRET.search(nearby):
                        line_no = index + 1
                        findings.append(finding("SEC001", "error", source.path, line_no,
                                                "AWS access key ID and secret assignment detected.", source.data))
                        break

        for line_no, window in _windows(lines, max_window):
            if _SENSITIVE.search(window):
                findings.append(finding("SEC002", "review", source.path, line_no,
                                        "Sensitive credential storage or process environment access requires review.", source.data))
                break

        is_script = _is_executable(source)
        is_markdown = _is_markdown(source.path)
        shell_statements = _shell_statements(text, markdown=is_markdown)
        # Detect exfiltration within a single shell logical statement; Markdown
        # examples stay review findings because their execution context is unknown.
        for line_no, tokens in shell_statements:
            if tokens is None:
                raw_line = lines[line_no - 1] if line_no <= len(lines) else ""
                if _CURL.search(raw_line) and re.search(r"(?:--data-binary|--data|-d|-F)\b", raw_line) and _EXTERNAL.search(raw_line):
                    findings.append(finding("SEC003", "review", source.path, line_no,
                                            "Upload command could not be parsed safely and requires review.", source.data))
                    break
                continue
            has_external, sensitive_file, uncertain_file = _curl_uploads(tokens, is_markdown)
            if has_external and (sensitive_file or uncertain_file):
                severity = "error" if is_script and sensitive_file and not uncertain_file else "review"
                findings.append(finding("SEC003", severity, source.path, line_no,
                                        "Command sends a sensitive file to an external URL.", source.data))
                break

        for line_no, tokens in shell_statements:
            if tokens is None:
                continue
            normalized_tokens = [token.strip("`") if is_markdown else token for token in tokens]
            pipes = [index for index, token in enumerate(normalized_tokens) if token == "|"]
            if any(
                any(token.lower() in {"curl", "wget"} for token in normalized_tokens[:pipe])
                and any(token.lower() in {"sh", "bash"} for token in normalized_tokens[pipe + 1:])
                for pipe in pipes
            ):
                findings.append(finding("SEC004", "review", source.path, line_no,
                                        "Remote content is piped directly to a shell.", source.data))
                break
        if not any(item.rule_id == "SEC004" and item.path == source.path for item in findings):
            for line_no, window in _windows(lines, max_window):
                if _DOWNLOAD.search(window) and _EXEC.search(window):
                    findings.append(finding("SEC004", "review", source.path, line_no,
                                            "Download and subsequent execution occur in a bounded text window.", source.data))
                    break

        for line_no, window in _windows(lines, max_window):
            if _BASE64.search(window) and _DECODE.search(window) and _DYNAMIC_EXEC.search(window):
                findings.append(finding("SEC005", "review", source.path, line_no,
                                        "Base64 decoding is combined with dynamic execution.", source.data))
                break

        for line_no, line in enumerate(lines, 1):
            if _IGNORE_SAFETY.search(line) or _HIDE.search(line) or _SUPPRESS_AUDIT.search(line):
                findings.append(finding("SEC006", "review", source.path, line_no,
                                        "Instruction to bypass safeguards, conceal activity, or suppress audit records requires review.", source.data))
                break

        for line_no, window in _windows(lines, max_window):
            if _PERSISTENCE.search(window) and _MUTATION.search(window):
                findings.append(finding("SEC007", "review", source.path, line_no,
                                        "Possible modification of startup, scheduled-task, or agent configuration requires review.", source.data))
                break
        if not any(item.rule_id == "SEC007" and item.path == source.path for item in findings):
            for line_no, tokens in shell_statements:
                if tokens is not None and _persistence_write(tokens):
                    findings.append(finding("SEC007", "review", source.path, line_no,
                                            "Possible modification of startup, scheduled-task, or agent configuration requires review.", source.data))
                    break

    # Stable, deterministic order and no duplicate rule/path emissions.
    unique: dict[tuple[str, str], Finding] = {}
    for item in findings:
        unique.setdefault((item.rule_id, item.path), item)
    return tuple(sorted(unique.values(), key=lambda f: (f.path, f.line or 0, f.rule_id)))
