#!/usr/bin/env python3
"""Validate citation coverage in a technical-talk Markdown blueprint."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ALLOWED_HOSTS = {
    "martinfowler.com",
    "akitaonrails.com",
    "substack.com",
    "news.ycombinator.com",
    "techcrunch.com",
    "huggingface.co",
    "arxiv.org",
    "anthropic.com",
    "openai.com",
    "x.com",
    "aihero.dev",
    "testingcatalog.com",
    "langchain.com",
    "serverlessland.com",
    "blogs.oracle.com",
    "developer.ibm.com",
    "research.ibm.com",
}
ALLOWED_X_HANDLES = {"garrytan", "mattpocockuk", "levelsio", "itsolelehmann"}
SLIDE_HEADING = re.compile(r"^##\s+Slide\b.*$", re.IGNORECASE | re.MULTILINE)
FINAL_HEADING = re.compile(
    r"^##\s+Slide final\s+[—-]\s+Referências bibliográficas\s*$",
    re.IGNORECASE | re.MULTILINE,
)
CITATION_GROUP = re.compile(r"\[((?:S\d{2,})(?:\s*,\s*S\d{2,})*)\]")
REFERENCE = re.compile(r"^\s*-\s*\[(S\d{2,})\]\s+.+$", re.MULTILINE)
URL = re.compile(r"https?://[^\s)>]+")
NO_TECHNICAL_CLAIM = "[sem-afirmacao-tecnica]"
GAMMA_TEMPLATE_ID = "nkhgcucv1lw00wc"


def normalize_host(url: str) -> str:
    return urlparse(url.rstrip(".,;")).netloc.lower().removeprefix("www.")


def validate_x_url(url: str) -> bool:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    return bool(parts and parts[0].lower() in ALLOWED_X_HANDLES)


def section_bounds(matches: list[re.Match[str]], index: int, text_length: int) -> tuple[int, int]:
    start = matches[index].end()
    end = matches[index + 1].start() if index + 1 < len(matches) else text_length
    return start, end


def citations_in(text: str) -> set[str]:
    citations: set[str] = set()
    for match in CITATION_GROUP.finditer(text):
        citations.update(re.findall(r"S\d{2,}", match.group(1)))
    return citations


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    final_match = FINAL_HEADING.search(text)
    headings = list(SLIDE_HEADING.finditer(text))

    if not headings:
        return ["Nenhum slide encontrado. Use títulos no formato '## Slide NN — Título'."]
    if not re.search(
        rf"^\s*-\s*Template Gamma:\s*{re.escape(GAMMA_TEMPLATE_ID)}\s*$",
        text,
        re.IGNORECASE | re.MULTILINE,
    ):
        errors.append(
            "O blueprint deve declarar o template Gamma obrigatório: "
            f"'- Template Gamma: {GAMMA_TEMPLATE_ID}'."
        )
    if not final_match:
        return [
            "Falta o último slide '## Slide final — Referências bibliográficas'. "
            "Use exatamente este título."
        ]

    final_index = next(
        (index for index, heading in enumerate(headings) if heading.start() == final_match.start()),
        None,
    )
    if final_index is None:
        errors.append("O cabeçalho de referências deve seguir o formato de slide.")
        return errors

    # Allow bibliography entries only; reject a later slide through the heading list as well.
    if final_index != len(headings) - 1:
        errors.append("O slide de Referências bibliográficas precisa ser o último slide.")

    cited_ids: set[str] = set()
    for index, heading in enumerate(headings[:final_index]):
        start, end = section_bounds(headings, index, len(text))
        body = text[start:end]
        ids = citations_in(body)
        if not ids and NO_TECHNICAL_CLAIM not in body.lower():
            errors.append(
                f"{heading.group(0)} não tem citação [SNN] nem a marca "
                f"{NO_TECHNICAL_CLAIM}."
            )
        cited_ids.update(ids)

    bibliography = text[final_match.end() :]
    reference_ids = set(REFERENCE.findall(bibliography))
    if not reference_ids:
        errors.append("O slide final não contém entradas bibliográficas no formato '- [S01] ...'.")

    for source_id in sorted(cited_ids - reference_ids):
        errors.append(f"A citação [{source_id}] não aparece no slide final de referências.")
    for source_id in sorted(reference_ids - cited_ids):
        errors.append(f"A referência [{source_id}] não é citada em nenhum slide técnico.")

    for entry in REFERENCE.finditer(bibliography):
        source_id = entry.group(1)
        line = entry.group(0)
        urls = URL.findall(line)
        if not urls:
            errors.append(f"A referência [{source_id}] não possui URL.")
            continue
        for url in urls:
            host = normalize_host(url)
            if host not in ALLOWED_HOSTS:
                errors.append(f"A referência [{source_id}] usa fonte fora do catálogo: {host}.")
            elif host == "x.com" and not validate_x_url(url):
                errors.append(
                    f"A referência [{source_id}] usa um perfil X não aprovado no catálogo."
                )

    if not re.search(r"Acesso em \d{4}-\d{2}-\d{2}", bibliography):
        errors.append("Inclua a data de acesso (Acesso em AAAA-MM-DD) nas referências.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida citações e slide final de referências de uma palestra Markdown."
    )
    parser.add_argument("blueprint", type=Path, help="Arquivo Markdown da palestra")
    args = parser.parse_args()

    if not args.blueprint.is_file():
        print(f"Arquivo não encontrado: {args.blueprint}", file=sys.stderr)
        return 2

    errors = validate(args.blueprint)
    if errors:
        print("Falha na validação de referências:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Referências validadas: {args.blueprint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
