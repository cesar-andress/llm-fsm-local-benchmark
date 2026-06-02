# Agent Instructions — LLM-FSM Local Benchmark

This repository is an academic research artifact for **FSM-Bench-20**: evaluating local open-source LLMs on deterministic FSM generation from natural-language requirements.

## Required reading

- `docs/PROJECT_RULES.md` — language, repository separation, commits, releases
- `REPRODUCIBILITY.md` — local Ollama experiment pipeline
- `docs/evaluation_protocol.md` — research design

## Hard constraints

1. **English only** in all repository files (see `docs/LANGUAGE_POLICY.md`).
2. **Conventional Commits** for every change: `<type>(<scope>): <short summary>`.
3. **No paper LaTeX** in this repository; use `~/papers/ist2026/paper/`.
4. **No raw experiment outputs** in the paper directory.
5. Run `python3.12 scripts/validate_integrity.py` before committing.
6. Do not reference internal development tools or automated assistants in commits, documentation, or release notes.

## Cursor rules

Project-specific rules live in `.cursor/rules/project-rules.mdc` (`alwaysApply: true`).

## Validation

```bash
python3.12 scripts/validate_integrity.py
python3.12 scripts/check_models.py
```

## Citation

See `CITATION.cff` and `LICENSE` (MIT).
