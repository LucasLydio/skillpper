"""Bounded, read-only Git tree access for untrusted candidate content."""

from pathlib import Path
import re
import subprocess
import threading
import unicodedata

from .models import SourceFile, portable_path_prefixes


MAX_TREE_BYTES = 100 * 1024 * 1024
MAX_TEXT_FILE_BYTES = 1 * 1024 * 1024
MAX_BINARY_FILE_BYTES = 5 * 1024 * 1024
MAX_BUNDLE_BYTES = 20 * 1024 * 1024
MAX_PATH_BYTES = 1024
MAX_FILES_PER_ROOT = 500
MAX_TREE_ENTRIES = 10_000
MAX_TREE_OUTPUT_BYTES = 8 * 1024 * 1024
MAX_OBJECT_METADATA_BYTES = 2 * 1024 * 1024
_FULL_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


class InputError(ValueError):
    """A safe, candidate-independent error raised while reading Git inputs."""


def _run_command(
    command: list[str],
    *,
    input_bytes: bytes | None = None,
    timeout: float = 30,
    max_output_bytes: int = MAX_OBJECT_METADATA_BYTES,
) -> bytes:
    """Run a trusted command with bounded buffered output and a wall-clock limit."""
    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        raise InputError("Git input operation failed") from None

    output = bytearray()
    output_error: list[BaseException] = []
    exceeded_limit = threading.Event()

    def drain_stdout() -> None:
        assert process.stdout is not None
        try:
            while True:
                chunk = process.stdout.read(64 * 1024)
                if not chunk:
                    break
                remaining = max_output_bytes + 1 - len(output)
                if remaining > 0:
                    output.extend(chunk[:remaining])
                if len(output) > max_output_bytes:
                    exceeded_limit.set()
                # Continue draining without retaining more bytes so the child
                # cannot block on a full pipe while the parent waits.
        except (OSError, ValueError) as exc:
            output_error.append(exc)

    def feed_stdin() -> None:
        assert process.stdin is not None
        try:
            process.stdin.write(input_bytes or b"")
            process.stdin.flush()
        except (BrokenPipeError, OSError, ValueError):
            pass
        finally:
            try:
                process.stdin.close()
            except OSError:
                pass

    reader = threading.Thread(target=drain_stdout, name="skill-validation-stdout", daemon=True)
    writer = None
    reader.start()
    if input_bytes is not None:
        writer = threading.Thread(target=feed_stdin, name="skill-validation-stdin", daemon=True)
        writer.start()

    timed_out = False
    try:
        return_code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()
        return_code = process.returncode

    # The direct Git commands used here do not spawn children. Still bound the
    # joins so a broken pipe endpoint cannot defeat the wall-clock limit.
    reader.join(timeout=1)
    if writer is not None:
        writer.join(timeout=1)
    if process.stdout is not None:
        try:
            process.stdout.close()
        except OSError:
            pass
    if process.stdin is not None:
        try:
            process.stdin.close()
        except OSError:
            pass

    if timed_out or reader.is_alive() or (writer is not None and writer.is_alive()):
        raise InputError("Git input operation failed or timed out")
    if output_error:
        raise InputError("Git input operation failed") from None
    if exceeded_limit.is_set():
        raise InputError("Git output exceeds the configured limit")
    if return_code != 0:
        # Git diagnostics may echo candidate paths or other untrusted data.
        raise InputError("Git input operation failed")
    return bytes(output)


def _run(
    repo: Path,
    args: list[str],
    *,
    input_bytes: bytes | None = None,
    timeout: float = 30,
    max_output_bytes: int = MAX_OBJECT_METADATA_BYTES,
) -> bytes:
    return _run_command(
        ["git", "-C", str(repo), *args],
        input_bytes=input_bytes,
        timeout=timeout,
        max_output_bytes=max_output_bytes,
    )


def _safe_tree_path(raw_path: bytes) -> tuple[str, str]:
    if len(raw_path) > MAX_PATH_BYTES:
        raise InputError("Git tree contains a path over the configured limit")
    try:
        path = raw_path.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise InputError("Git tree contains a path that is not valid UTF-8") from None
    if not path or path.startswith("/") or "\\" in path or any(part in {"", ".", ".."} for part in path.split("/")):
        raise InputError("Git tree contains an unsafe path")
    if any(ord(char) < 32 or ord(char) == 127 or unicodedata.category(char) in {"Cf", "Cs"} for char in path):
        raise InputError("Git tree contains a path with control characters")
    return path, path.split("/", 1)[0]


def _per_file_limit(path: str) -> int:
    if path.endswith(".skill") and "/" not in path:
        return MAX_BUNDLE_BYTES
    if path.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        return MAX_BINARY_FILE_BYTES
    return MAX_TEXT_FILE_BYTES


def read_tree(repo: Path, revision: str, max_bytes: int) -> tuple[SourceFile, ...]:
    """Read regular blobs from a full immutable commit SHA under trusted budgets.

    This function never checks out, extracts, imports, or executes candidate data.
    ``max_bytes`` may lower the aggregate cap but cannot raise the trusted cap.
    """
    if not isinstance(revision, str) or not _FULL_SHA.fullmatch(revision):
        raise InputError("revision must be a full commit SHA")
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or max_bytes <= 0:
        raise InputError("max_bytes must be a positive integer")
    tree_budget = min(max_bytes, MAX_TREE_BYTES)
    repo = Path(repo)

    object_type = _run(repo, ["cat-file", "-t", revision]).strip()
    if object_type != b"commit":
        raise InputError("revision does not identify a commit")

    raw_tree = _run(
        repo,
        ["ls-tree", "-rz", "--full-tree", revision],
        max_output_bytes=MAX_TREE_OUTPUT_BYTES,
    )
    entries: list[tuple[str, bytes, str, str]] = []
    counts: dict[str, int] = {}
    portable_prefixes: dict[str, str] = {}
    for record in raw_tree.split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            mode_b, type_b, oid_b = metadata.split(b" ", 2)
        except ValueError:
            raise InputError("Git returned a malformed tree entry") from None
        mode = mode_b.decode("ascii", errors="ignore")
        if mode not in {"100644", "100755"}:
            raise InputError("unsupported Git entry mode")
        if type_b != b"blob" or not re.fullmatch(rb"[0-9a-f]{40}|[0-9a-f]{64}", oid_b):
            raise InputError("Git tree contains an unsupported object")
        path, root = _safe_tree_path(raw_path)
        for portable_key, spelling in portable_path_prefixes(path):
            previous_spelling = portable_prefixes.get(portable_key)
            if previous_spelling is not None and previous_spelling != spelling:
                raise InputError("Git tree contains case-colliding paths")
            portable_prefixes[portable_key] = spelling
        counts[root] = counts.get(root, 0) + 1
        if counts[root] > MAX_FILES_PER_ROOT:
            raise InputError("Git tree exceeds the per-root file limit")
        entries.append((path, oid_b, mode, root))
        if len(entries) > MAX_TREE_ENTRIES:
            raise InputError("Git tree exceeds the configured entry limit")

    if not entries:
        return ()
    oids = [entry[1] for entry in entries]
    oid_input = b"".join(oid + b"\n" for oid in oids)
    checked = _run(
        repo,
        ["cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
        input_bytes=oid_input,
        max_output_bytes=MAX_OBJECT_METADATA_BYTES,
    )
    checks = checked.splitlines()
    if len(checks) != len(entries):
        raise InputError("Git returned incomplete object metadata")
    sizes: list[int] = []
    total = 0
    for (path, oid, _mode, _root), row in zip(entries, checks):
        try:
            found_oid, kind, size_text = row.split(b" ", 2)
            size = int(size_text)
        except (ValueError, TypeError):
            raise InputError("Git returned malformed object metadata") from None
        if found_oid != oid or kind != b"blob" or size < 0:
            raise InputError("Git tree contains a missing or unsupported blob")
        if size > _per_file_limit(path):
            raise InputError("Git blob exceeds the configured per-file limit")
        total += size
        if total > tree_budget:
            raise InputError("Git tree exceeds the configured byte limit")
        sizes.append(size)

    batch_limit = tree_budget + len(entries) * 128 + 1
    batch = _run(
        repo,
        ["cat-file", "--batch"],
        input_bytes=oid_input,
        timeout=60,
        max_output_bytes=batch_limit,
    )
    offset = 0
    result: list[SourceFile] = []
    for (path, oid, mode, _root), expected_size in zip(entries, sizes):
        header_end = batch.find(b"\n", offset)
        if header_end < 0:
            raise InputError("Git returned incomplete blob data")
        header = batch[offset:header_end].split(b" ")
        if len(header) != 3 or header[0] != oid or header[1] != b"blob":
            raise InputError("Git returned unexpected blob data")
        try:
            actual_size = int(header[2])
        except ValueError:
            raise InputError("Git returned malformed blob size") from None
        data_start = header_end + 1
        data_end = data_start + actual_size
        if actual_size != expected_size or data_end >= len(batch) or batch[data_end:data_end + 1] != b"\n":
            raise InputError("Git returned incomplete or inconsistent blob data")
        data = batch[data_start:data_end]
        result.append(SourceFile(path, data, mode))
        offset = data_end + 1
    if offset != len(batch):
        raise InputError("Git returned unexpected trailing blob data")
    return tuple(sorted(result, key=lambda source: source.path))
