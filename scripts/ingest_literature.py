#!/usr/bin/env python3
"""Ingest user-provided literature records without inventing metadata."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_FIELDS = {
    "title",
    "authors",
    "year",
    "venue",
    "doi",
    "url",
    "source_type",
    "is_synthetic",
    "evidence_status",
    "abstract",
    "keywords",
    "user_notes",
    "relevant_excerpts",
}
METADATA_FIELDS = ["authors", "year", "venue", "doi", "url"]


def load_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("papers"), list):
        return data["papers"]
    raise SystemExit("JSON input must be a list or an object with a papers list")


def load_yaml(path: Path) -> list[dict]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit("YAML input requires PyYAML in this environment; JSON and BibTeX still work") from exc
    data = yaml.safe_load(path.read_text())
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("papers"), list):
        return data["papers"]
    raise SystemExit("YAML input must be a list or an object with a papers list")


def split_bib_fields(body: str) -> list[str]:
    fields: list[str] = []
    start = 0
    depth = 0
    in_quote = False
    for i, char in enumerate(body):
        if char == '"' and (i == 0 or body[i - 1] != "\\"):
            in_quote = not in_quote
        elif not in_quote and char == "{":
            depth += 1
        elif not in_quote and char == "}":
            depth = max(0, depth - 1)
        elif char == "," and depth == 0 and not in_quote:
            fields.append(body[start:i].strip())
            start = i + 1
    tail = body[start:].strip()
    if tail:
        fields.append(tail)
    return fields


def clean_bib_value(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    if (value.startswith("{") and value.endswith("}")) or (value.startswith('"') and value.endswith('"')):
        value = value[1:-1]
    return value.strip()


def load_bibtex(path: Path) -> list[dict]:
    text = path.read_text()
    records: list[dict] = []
    for match in re.finditer(r"@(?P<type>\w+)\s*\{\s*(?P<key>[^,]+),(?P<body>.*?)\n\}", text, re.S):
        record: dict[str, object] = {"source_type": "bibtex", "bibtex_key": match.group("key").strip()}
        for field in split_bib_fields(match.group("body")):
            if "=" not in field:
                continue
            key, value = field.split("=", 1)
            key = key.strip().lower()
            if key == "journal" or key == "booktitle":
                key = "venue"
            if key == "note":
                key = "user_notes"
            record[key] = clean_bib_value(value)
        records.append(record)
    if not records:
        raise SystemExit(f"No BibTeX entries parsed from {path}")
    return records


def load_csv(path: Path) -> list[dict]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    records: list[dict] = []
    for row in rows:
        record = {k.strip().lower(): v for k, v in row.items() if k}
        if "notes" in record and "user_notes" not in record:
            record["user_notes"] = record.pop("notes")
        records.append(record)
    return records


def as_list(value: object) -> list:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str) and ";" in value:
        return [part.strip() for part in value.split(";") if part.strip()]
    return [value]


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def normalize_record(raw: dict, index: int, source_name: str) -> dict:
    if not isinstance(raw, dict):
        raise SystemExit(f"Record {index} is not an object")
    title = raw.get("title")
    if not title:
        raise SystemExit(f"Record {index} missing required title")
    missing = [field for field in METADATA_FIELDS if raw.get(field) in (None, "", [])]
    canonical = {
        "paper_id": f"P{index:03d}",
        "title": str(title),
        "authors": as_list(raw.get("authors")),
        "year": raw.get("year") if raw.get("year") not in ("", None) else None,
        "venue": raw.get("venue") if raw.get("venue") not in ("", None) else None,
        "doi": raw.get("doi") if raw.get("doi") not in ("", None) else None,
        "url": raw.get("url") if raw.get("url") not in ("", None) else None,
        "source_type": raw.get("source_type") or "user_provided_record",
        "is_synthetic": parse_bool(raw.get("is_synthetic", False)),
        "ingestion_source": source_name,
        "evidence_status": raw.get("evidence_status") or "user_provided",
        "abstract": raw.get("abstract") if raw.get("abstract") not in ("", None) else None,
        "keywords": as_list(raw.get("keywords")),
        "user_notes": raw.get("user_notes") if raw.get("user_notes") not in ("", None) else None,
        "relevant_excerpts": as_list(raw.get("relevant_excerpts")),
        "missing_metadata": missing,
        "extra_fields": {k: v for k, v in raw.items() if k not in CANONICAL_FIELDS},
    }
    return canonical


def load_records(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_json(path)
    if suffix in {".yaml", ".yml"}:
        return load_yaml(path)
    if suffix == ".bib":
        return load_bibtex(path)
    if suffix == ".csv":
        return load_csv(path)
    raise SystemExit(f"Unsupported literature input format: {path.suffix}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--corpus-id", default="provided_literature_corpus")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace if args.workspace.is_absolute() else ROOT / args.workspace
    input_path = args.input if args.input.is_absolute() else ROOT / args.input
    if not workspace.exists():
        raise SystemExit(f"workspace not found: {workspace}")
    if not input_path.exists():
        raise SystemExit(f"input not found: {input_path}")

    evidence_dir = workspace / "literature_evidence"
    if evidence_dir.exists() and not args.overwrite:
        records_path = evidence_dir / "bibliographic_records.json"
        if records_path.exists():
            raise SystemExit(f"literature evidence already exists: {records_path}; pass --overwrite")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = evidence_dir / "raw"
    raw_dir.mkdir(exist_ok=True)
    shutil.copy2(input_path, raw_dir / input_path.name)

    records = [normalize_record(record, i, input_path.name) for i, record in enumerate(load_records(input_path), start=1)]
    payload = {
        "corpus_id": args.corpus_id,
        "corpus_scope": "user-provided corpus only; not a field-wide systematic review",
        "input_files": [str(input_path)],
        "bibliographic_records": records,
        "synthetic_records": [r["paper_id"] for r in records if r["is_synthetic"]],
        "missing_metadata": [{"paper_id": r["paper_id"], "missing": r["missing_metadata"]} for r in records if r["missing_metadata"]],
        "ingestion_warnings": [
            "No missing bibliographic metadata was inferred or completed.",
            "Bibliographic records alone do not verify research claims.",
        ],
        "evidence_policy": {
            "no_fabricated_literature": True,
            "title_only_inference_allowed": False,
            "synthetic_records_are_real_evidence": False,
        },
    }
    (evidence_dir / "bibliographic_records.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    report = [
        "# Literature Intake Report",
        "",
        f"- corpus_id: `{args.corpus_id}`",
        f"- record_count: {len(records)}",
        f"- synthetic_count: {len(payload['synthetic_records'])}",
        "- metadata_completion: none",
        "- field_scope: user-provided corpus only",
    ]
    (evidence_dir / "intake_report.md").write_text("\n".join(report) + "\n")
    print(f"PASS ingested {len(records)} records into {evidence_dir}")


if __name__ == "__main__":
    main()
