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

Relative to `v1.0.0`, this tag additionally includes:

- Conservative guard-aware determinism (M0–M3) implementation and unit tests
- Criterion freeze file, lexicon, and SHA-256 hashes
- Per-group guard-aware diagnostics for all 106 conflict groups (`results/guard_aware_groups.json`)
- Aggregate metric summaries and campaign manifests

Large per-pair CSV files and raw/cleaned model outputs remain with the frozen local campaign and are size-excluded from the Git tree; group-level diagnostics support audit of every EXCLUSIVE / OVERLAP / UNKNOWN verdict.

---

## Identifiers

| Item | Value |
|------|-------|
| Git tag | `v1.1.0` |
| Zenodo published version DOI | [10.5281/zenodo.20517969](https://doi.org/10.5281/zenodo.20517969) (= GitHub `v1.0.0` freeze) |
| Zenodo concept DOI | [10.5281/zenodo.20516295](https://doi.org/10.5281/zenodo.20516295) |
| GitHub Release | https://github.com/cesar-andress/llm-fsm-local-benchmark/releases/tag/v1.1.0 |

The Zenodo published record `10.5281/zenodo.20517969` archives GitHub release **`v1.0.0`**.
Readers should use GitHub tag **`v1.1.0`** for the IST revision contents (guard-aware instrument and deposited diagnostics).

---

# Release Notes — v1.0.0

**FSM-Bench-20 publication release**  
**Date:** 2026-06-02  
**Git tag:** `v1.0.0`  
**Author:** César Andrés (ORCID [0009-0001-8968-3404](https://orcid.org/0009-0001-8968-3404))

---

## Release scope

This is the **first publication-quality release** of the FSM-Bench-20 local LLM benchmark repository, aligned with the completed 140-run evaluation campaign and the *Information and Software Technology* journal submission.

The tag freezes:

- Benchmark dataset v1.0 (20 software systems)
- Prompt specification and evaluation protocol documentation
- FSM JSON schema and validation library
- Experiment and evaluation scripts
- Reproducibility and citation metadata

---

## Included artefacts (version control)

| Artefact | Path |
|----------|------|
| Dataset index and systems | `dataset/` |
| Gold FSM placeholders | `benchmark/` |
| Prompt specification | `docs/experimental_prompts.md` |
| Evaluation protocol | `docs/evaluation_protocol.md` |
| FSM schema and validators | `scripts/fsm_benchmark/` |
| Experiment driver | `scripts/run_experiment.py` |
| Metrics pipeline | `scripts/evaluate.py` |
| End-to-end runner | `run_all.sh` |
| Reproducibility guide | `REPRODUCIBILITY.md` |
| Citation metadata | `CITATION.cff` |
| License | `LICENSE` (MIT) |

---

## Final benchmark statistics (140-run freeze)

Campaign manifest: **`20260602T195520Z`**  
Finalized: **`2026-06-02T21:02:56 UTC`**  
Runs completed: **140/140** (seven Ollama models × 20 systems)

| Metric | Result |
|--------|--------|
| G1 — Valid JSON | **98.6%** (138/140) |
| G2 — Schema-valid FSM | **78.6%** (110/140) |
| G3 — Nested deterministic FSM | **31.4%** (44/140) |
| Mean requirement coverage | **69.2%** |

These values are descriptive aggregates from the frozen campaign. They are reported in the manuscript and must not be altered without rerunning the full protocol under a new manifest.

---

## Reproducibility

1. Check out tag `v1.0.0` for the pre-guard-aware baseline, or `v1.1.0` for the IST revision package.
2. Follow `REPRODUCIBILITY.md` to install Ollama models and Python dependencies.
3. Materialise prompt files from `docs/experimental_prompts.md`.
4. Execute `./run_all.sh` or the documented manual steps.
5. Compare regenerated gate rates against the statistics above.

**Note:** Full per-pair CSV records, raw/cleaned model outputs, and intermediate figures are size-excluded from the public Git tree. Compact summaries and guard-aware group diagnostics are tracked under tag `v1.1.0`.

---

## Known limitations

- All requirement specifications are **English-only**; multilingual behaviour was not evaluated.
- Every reported run used **structured JSON output**; no unstructured ablation is included in this release.
- **Gold reference FSMs** for behavioural equivalence are placeholders only (Phase 2).
- **G3 determinism** is strict pair uniqueness; guard-aware semantics are not evaluated dynamically.
- Results characterise **FSM-Bench-20** under the documented Ollama model tags and RTX 4090-class hardware; other runtimes may differ.
- Residual stochasticity may remain despite temperature 0.0 and pinned model tags.

---

## Citation

Please cite:

- **Revision package:** GitHub tag [`v1.1.0`](https://github.com/cesar-andress/llm-fsm-local-benchmark/releases/tag/v1.1.0)
- **Zenodo (`v1.0.0` freeze):** [10.5281/zenodo.20517969](https://doi.org/10.5281/zenodo.20517969)
- **Repository:** `https://github.com/cesar-andress/llm-fsm-local-benchmark`

Metadata is available in `CITATION.cff`.

```bibtex
@software{fsm_bench_20_2026,
  author    = {Andr{\'e}s, C{\'e}sar},
  title     = {{FSM-Bench-20}: Local {LLM} Benchmark for Deterministic {FSM} Generation},
  version   = {1.1.0},
  year      = {2026},
  url       = {https://github.com/cesar-andress/llm-fsm-local-benchmark/releases/tag/v1.1.0},
  note      = {Public replication package for the IST revision. Zenodo DOI 10.5281/zenodo.20517969 archives GitHub v1.0.0.}
}
```

---

## Prior releases

| Tag | Summary |
|-----|---------|
| v0.3.0 | Validation safeguards and repository hygiene |
| v0.2.0 | Documentation expansion |
| v0.1.0-dataset-and-framework | Initial dataset and framework |
| v0.1.0 | First public release |
