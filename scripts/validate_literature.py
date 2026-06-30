#!/usr/bin/env python3
"""Validate literature grounding artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "paper_cards.json": "schemas/literature_grounding/paper_card.schema.json",
    "literature_matrix.json": "schemas/literature_grounding/literature_matrix.schema.json",
    "evidence_claim_map.json": "schemas/literature_grounding/evidence_claim_map.schema.json",
    "literature_gap_audit.json": "schemas/literature_grounding/literature_gap_audit.schema.json",
    "literature_grounding_report.json": "schemas/literature_grounding/literature_grounding_report.schema.json",
}
UNSAFE = re.compile(r"(?<!algorithm-)\bfirst\b|\bnovel\b|state-of-the-art|\bunprecedented\b", re.I)


def load_json(path: Path) -> object:
    return json.loads(path.read_text())


def iter_dicts(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_dicts(child)


def has_evidence_id(item: dict) -> bool:
    ids = item.get("supporting_evidence_ids") or item.get("linked_evidence_ids") or item.get("evidence_ids") or item.get("evidence_id")
    return bool(ids)


def has_source(item: dict) -> bool:
    return bool(item.get("source_field") or item.get("source_excerpt") or item.get("supporting_evidence_ids") or item.get("linked_evidence_ids"))


def check_schema(path: Path, schema_path: Path, failures: list[str], passes: list[str], warnings: list[str]) -> None:
    try:
        from jsonschema import Draft202012Validator  # type: ignore
    except ImportError:
        warnings.append("WARNING jsonschema not installed; skipped schema validation")
        return
    schema = load_json(schema_path)
    data = load_json(path)
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda err: list(err.path))
    if errors:
        failures.append(f"FAIL schema validation failed for {path.name}: {errors[0].message}")
    else:
        passes.append(f"PASS schema validation: {path.name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace if args.workspace.is_absolute() else ROOT / args.workspace
    evidence_dir = workspace / "literature_evidence"
    failures: list[str] = []
    warnings: list[str] = []
    passes: list[str] = []

    if not evidence_dir.exists():
        raise SystemExit(f"FAIL missing literature_evidence directory: {evidence_dir}")
    records_path = evidence_dir / "bibliographic_records.json"
    if not records_path.exists():
        raise SystemExit(f"FAIL missing bibliographic_records.json: {records_path}")
    records_payload = load_json(records_path)
    if not isinstance(records_payload, dict):
        raise SystemExit("FAIL bibliographic_records.json must be an object")
    records = records_payload.get("bibliographic_records", [])
    if not isinstance(records, list):
        raise SystemExit("FAIL bibliographic_records must be a list")
    passes.append("PASS bibliographic_records.json is valid JSON")

    paper_ids = [record.get("paper_id") for record in records if isinstance(record, dict)]
    if len(paper_ids) != len(set(paper_ids)):
        failures.append("FAIL duplicate paper_id")
    else:
        passes.append("PASS paper_id values are unique")
    synthetic_papers = {record.get("paper_id") for record in records if isinstance(record, dict) and record.get("is_synthetic")}
    if synthetic_papers:
        passes.append("PASS synthetic records are explicitly tracked")
    for record in records:
        if isinstance(record, dict) and record.get("is_synthetic") and record.get("evidence_status") == "verified":
            failures.append(f"FAIL synthetic record marked verified: {record.get('paper_id')}")

    artifacts: dict[str, object] = {}
    for filename, schema_rel in SCHEMAS.items():
        path = evidence_dir / filename
        if path.exists():
            artifacts[filename] = load_json(path)
            check_schema(path, ROOT / schema_rel, failures, passes, warnings)
        else:
            warnings.append(f"WARNING optional artifact missing: {filename}")

    for data in artifacts.values():
        for item in iter_dicts(data):
            if item.get("evidence_status") == "verified" and not has_source(item):
                failures.append(f"FAIL verified claim lacks source evidence: {item.get('claim_id') or item.get('evidence_id')}")
            if item.get("grounding_status") == "grounded" and not has_evidence_id(item):
                failures.append(f"FAIL grounded claim lacks evidence_id: {item.get('claim_id')}")
            if item.get("claim_type") == "gap_claim" and not item.get("corpus_scope"):
                failures.append(f"FAIL gap claim lacks corpus_scope: {item.get('claim_id')}")
            if item.get("claim_scope") == "field_general" and item.get("support_strength") not in {"direct"}:
                failures.append(f"FAIL field_general claim lacks direct evidence: {item.get('claim_id')}")
            if item.get("evidence_status") == "verified":
                linked_papers = set(item.get("linked_paper_ids", []) or [item.get("paper_id")])
                if linked_papers & synthetic_papers:
                    failures.append(f"FAIL synthetic evidence used as verified evidence: {item.get('claim_id') or item.get('evidence_id')}")
            text = json.dumps(item, ensure_ascii=False)
            lower_text = text.lower()
            if UNSAFE.search(text) and "no first" not in lower_text and "unsafe" not in lower_text and item.get("novelty_safety_level") not in {"verified_by_user_provided_systematic_review"}:
                warnings.append(f"WARNING unsafe novelty wording needs review: {item.get('claim_id') or item.get('gap_id') or item.get('paper_id')}")

    claim_map = artifacts.get("evidence_claim_map.json")
    if isinstance(claim_map, dict):
        claim_ids = [item.get("claim_id") for item in claim_map.get("claims", []) if isinstance(item, dict)]
        evidence_ids = [item.get("evidence_id") for item in claim_map.get("evidence_objects", []) if isinstance(item, dict)]
        if len(claim_ids) != len(set(claim_ids)):
            failures.append("FAIL duplicate claim_id in evidence_claim_map claims")
        if len(evidence_ids) != len(set(evidence_ids)):
            failures.append("FAIL duplicate evidence_id in evidence_claim_map evidence_objects")

    gap_audit = artifacts.get("literature_gap_audit.json")
    if isinstance(gap_audit, dict):
        counter_summary = gap_audit.get("counterevidence_summary", [])
        for gap in gap_audit.get("gap_candidates", []):
            if gap.get("contradicting_evidence_ids") and not counter_summary:
                failures.append(f"FAIL contradictory evidence is not surfaced for gap: {gap.get('gap_id')}")
            if not gap.get("corpus_scope"):
                failures.append(f"FAIL gap candidate lacks corpus_scope: {gap.get('gap_id')}")

    report = [
        "# Literature Validation Report",
        "",
        f"- pass_count: {len(passes)}",
        f"- warning_count: {len(warnings)}",
        f"- fail_count: {len(failures)}",
        "",
        "## PASS",
        *[f"- {line}" for line in passes],
        "",
        "## WARNING",
        *[f"- {line}" for line in warnings],
        "",
        "## FAIL",
        *[f"- {line}" for line in failures],
    ]
    (evidence_dir / "literature_validation_report.md").write_text("\n".join(report) + "\n")
    print("\n".join(report))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
