#!/usr/bin/env python3
"""Aggregate metrics from raw/cleaned outputs into CSV summaries."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fsm_benchmark.config import CLEANED_DIR, RAW_DIR, RESULTS_DIR
from fsm_benchmark.dataset import load_all_systems
from fsm_benchmark.metrics import compute_metrics, validate_fsm_dict


def sanitize_model_dir(model: str) -> str:
    return model.replace(":", "_").replace("/", "_")


def model_dir_to_name(model_dir: str) -> str:
    if "_latest" in model_dir:
        return model_dir.replace("_latest", ":latest")
    parts = model_dir.rsplit("_", 1)
    if len(parts) == 2:
        return f"{parts[0]}:{parts[1]}"
    return model_dir


def load_raw_record(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_all(output_csv: Path) -> list[dict]:
    systems = {system.file_stem: system for system in load_all_systems()}
    rows: list[dict] = []

    for raw_path in sorted(RAW_DIR.glob("*/*.json")):
        record = load_raw_record(raw_path)
        model = record.get("model") or model_dir_to_name(raw_path.parent.name)
        system_stem = record.get("system") or raw_path.stem
        system = systems.get(system_stem)
        if system is None:
            continue

        parsed = record.get("parsed")
        cleaned_path = CLEANED_DIR / raw_path.parent.name / raw_path.name
        if cleaned_path.exists():
            parsed = json.loads(cleaned_path.read_text(encoding="utf-8"))

        validation = validate_fsm_dict(parsed)
        metrics = compute_metrics(
            model=model,
            system_name=system.system_name,
            domain=system.domain,
            requirements=system.requirements,
            payload=parsed,
            validation=validation,
            eval_count=record.get("eval_count"),
            eval_duration_ns=record.get("eval_duration_ns"),
            total_duration_ns=record.get("total_duration_ns"),
        )

        row = metrics.__dict__.copy()
        row["system_stem"] = system_stem
        row["invalid_json"] = not metrics.valid_json
        row["missing_requirements"] = ",".join(metrics.missing_requirements)
        row["unreachable_states"] = ",".join(metrics.unreachable_states)
        row["validation_errors"] = "|".join(metrics.validation_errors)
        row["validation_warnings"] = "|".join(metrics.validation_warnings)
        rows.append(row)

        details_path = RESULTS_DIR / "details" / raw_path.parent.name / raw_path.name
        details_path.parent.mkdir(parents=True, exist_ok=True)
        details_path.write_text(json.dumps(row, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if not rows:
        return rows

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary = summarize(rows)
    summary_path = RESULTS_DIR / "summary_by_model.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return rows


def summarize(rows: list[dict]) -> dict:
    by_model: dict[str, list[dict]] = {}
    for row in rows:
        by_model.setdefault(row["model"], []).append(row)

    summary: dict[str, dict] = {}
    for model, model_rows in by_model.items():
        n = len(model_rows)
        summary[model] = {
            "runs": n,
            "invalid_json_rate": round(sum(1 for r in model_rows if r["invalid_json"]) / n, 4),
            "avg_requirement_coverage": round(sum(r["requirement_coverage"] for r in model_rows) / n, 4),
            "avg_num_states": round(sum(r["num_states"] for r in model_rows) / n, 2),
            "avg_num_events": round(sum(r["num_events"] for r in model_rows) / n, 2),
            "avg_num_transitions": round(sum(r["num_transitions"] for r in model_rows) / n, 2),
            "determinism_rate": round(sum(1 for r in model_rows if r["deterministic"]) / n, 4),
            "avg_unsupported_transitions": round(
                sum(r["unsupported_transitions"] for r in model_rows) / n, 2
            ),
            "avg_inferred_transitions": round(sum(r["inferred_transitions"] for r in model_rows) / n, 2),
            "schema_valid_rate": round(sum(1 for r in model_rows if r["schema_valid"]) / n, 4),
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate FSM benchmark outputs")
    parser.add_argument(
        "--csv",
        default=str(RESULTS_DIR / "metrics.csv"),
        help="Path to output CSV",
    )
    args = parser.parse_args()

    rows = evaluate_all(Path(args.csv))
    if not rows:
        print("No raw outputs found. Run scripts/run_experiment.py first.")
        return 1

    print(f"Wrote {len(rows)} rows to {args.csv}")
    print(f"Summary: {RESULTS_DIR / 'summary_by_model.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
