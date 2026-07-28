# Release Notes — v1.1.0

**v1.1.0 – Guard-Aware Reproducibility Release (IST Revision)**  
**Date:** 2026-07-28  
**Git tag:** `v1.1.0`  
**Author:** César Andrés (ORCID [0009-0001-8968-3404](https://orcid.org/0009-0001-8968-3404))  
**Repository:** https://github.com/cesar-andress/llm-fsm-local-benchmark

---

## Release scope

This tag is the public replication package for the *Information and Software Technology* major-revision manuscript.
It freezes the guard-aware determinism instrument and deposited diagnostics on top of the frozen 140-run campaign (`20260602T195520Z`), with standardised author identity (César Andrés).

The public replication package includes:

- Benchmark dataset, prompt specification, schema, and evaluator
- Conservative guard-aware determinism (M0-M3) implementation and unit tests
- Criterion freeze file, lexicon, and SHA-256 hashes
- Per-group guard-aware diagnostics for all 106 conflict groups (`results/guard_aware_groups.json`)
- Aggregate metric summaries and campaign manifests
- Reproducibility guide (`REPRODUCIBILITY.md`)

Large per-pair CSV files and raw/cleaned model outputs remain with the frozen local campaign and are size-excluded from the Git tree; group-level diagnostics support audit of every EXCLUSIVE / OVERLAP / UNKNOWN verdict.

---

## Identifiers

| Item | Value |
|------|-------|
| Git tag | `v1.1.0` |
| Zenodo published record DOI | [10.5281/zenodo.20517969](https://doi.org/10.5281/zenodo.20517969) |
| Zenodo concept DOI | [10.5281/zenodo.20516295](https://doi.org/10.5281/zenodo.20516295) |
| GitHub Release | https://github.com/cesar-andress/llm-fsm-local-benchmark/releases/tag/v1.1.0 |

---

## Final benchmark statistics (140-run freeze)

Campaign manifest: **`20260602T195520Z`**  
Finalized: **`2026-06-02T21:02:56 UTC`**  
Runs completed: **140/140** (seven Ollama models × 20 systems)

| Metric | Result |
|--------|--------|
| G1 — Valid JSON | **98.6%** (138/140) |
| G2 — Schema-valid FSM | **78.6%** (110/140) |
| Nested M0 (strict determinism) | **31.4%** (44/140) |
| Nested M1 (conservative guard-aware) | **33.6%** (47/140) |
| Mean requirement coverage | **69.2%** |

These values are descriptive aggregates from the frozen campaign. They are reported in the manuscript and must not be altered without rerunning the full protocol under a new manifest.

---

## Reproducibility

1. Check out tag `v1.1.0`.
2. Follow `REPRODUCIBILITY.md` to install Ollama models and Python dependencies.
3. Materialise prompt files from `docs/experimental_prompts.md`.
4. Execute `./run_all.sh` or the documented manual steps.
5. Compare regenerated gate rates against the statistics above.

**Note:** Full per-pair CSV records, raw/cleaned model outputs, and intermediate figures are size-excluded from the public Git tree.

---

## Citation

Please cite:

- **Public replication package:** GitHub tag [`v1.1.0`](https://github.com/cesar-andress/llm-fsm-local-benchmark/releases/tag/v1.1.0)
- **Zenodo:** [10.5281/zenodo.20517969](https://doi.org/10.5281/zenodo.20517969)
- **Repository:** `https://github.com/cesar-andress/llm-fsm-local-benchmark`

Metadata is available in `CITATION.cff`.

```bibtex
@software{fsm_bench_20_2026,
  author    = {Andr{\'e}s, C{\'e}sar},
  title     = {{FSM-Bench-20}: Local {LLM} Benchmark for Deterministic {FSM} Generation},
  version   = {1.1.0},
  year      = {2026},
  doi       = {10.5281/zenodo.20517969},
  url       = {https://github.com/cesar-andress/llm-fsm-local-benchmark/releases/tag/v1.1.0}
}
```
