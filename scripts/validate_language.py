#!/usr/bin/env python3
"""Audit repository text files for Spanish user-facing content."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent

SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules"}
SKIP_FILES = {"validate_language.py"}
TEXT_EXTENSIONS = {
    ".md", ".txt", ".py", ".json", ".yml", ".yaml", ".sh", ".cff", ".csv", ".tex", ".bib", ".svg", ".mdc"
}

# Spanish diacritics and inverted punctuation (Unicode escapes — not Spanish prose)
SPANISH_DIACRITICS = re.compile(r"[\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00bf\u00a1]", re.IGNORECASE)

SPANISH_KEYWORDS = re.compile(
    r"\b("
    r"requisito|requisitos|ejecutar|documento|metrica|experimento|"
    r"reproducibilidad|configuracion|instalacion|ejecucion|graficos|"
    r"repositorio|archivo|traducir|descripcion|verificacion|validacion|"
    r"generacion|maquina|ningun|ninguna|tambien|ademas|contiene|incluye|informe"
    r")\b",
    re.IGNORECASE,
)

ALLOWLIST_SUBSTRINGS = (
    "Spanish diacritics",
    "Spanish text",
    "Spanish natural-language",
    "word \"Spanish\"",
    "translation requirement",
    "non-English",
)


def should_scan(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.name in SKIP_FILES:
        return False
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_EXTENSIONS


def is_allowed_line(line: str) -> bool:
    return any(token in line for token in ALLOWLIST_SUBSTRINGS)


def scan_roots(roots: list[Path]) -> tuple[list[str], list[tuple[str, int, str, str]]]:
    scanned: set[str] = set()
    findings: list[tuple[str, int, str, str]] = []

    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not should_scan(path):
                continue
            path_str = str(path.resolve())
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            scanned.add(path_str)
            for lineno, line in enumerate(text.splitlines(), start=1):
                if is_allowed_line(line):
                    continue
                if SPANISH_DIACRITICS.search(line):
                    findings.append((path_str, lineno, "diacritic", line.strip()[:160]))
                elif SPANISH_KEYWORDS.search(line):
                    findings.append((path_str, lineno, "keyword", line.strip()[:160]))
    return sorted(scanned), findings


def main() -> int:
    roots = [REPO_ROOT, WORKSPACE_ROOT]
    scanned, findings = scan_roots(roots)

    print(f"Scanned files: {len(scanned)}")
    print(f"Spanish findings: {len(findings)}")
    for path, lineno, kind, snippet in findings:
        print(f"{path}:{lineno} [{kind}] {snippet}")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
