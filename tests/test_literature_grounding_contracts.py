from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def run_cmd(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(f"command failed: {' '.join(args)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result


def init_workspace(tmp_path: Path, project_id: str) -> Path:
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", project_id, "--root", str(tmp_path), "--overwrite"])
    return tmp_path / project_id


def test_literature_schemas_are_valid_json_objects() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    for path in (ROOT / "schemas" / "literature_grounding").glob("*.schema.json"):
        schema = json.loads(path.read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        assert schema["type"] == "object", path
        assert "required" in schema, path


def test_all_literature_samples_validate_against_schemas() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    pairs = {
        "paper_card.schema.json": "sample_paper_cards_output.json",
        "literature_matrix.schema.json": "sample_literature_matrix_output.json",
        "evidence_claim_map.schema.json": "sample_evidence_claim_map_output.json",
        "literature_gap_audit.schema.json": "sample_literature_gap_audit_output.json",
        "literature_grounding_report.schema.json": "sample_literature_grounding_report_output.json",
    }
    for schema_name, sample_name in pairs.items():
        schema = json.loads((ROOT / "schemas" / "literature_grounding" / schema_name).read_text())
        sample = json.loads((ROOT / "examples" / "literature" / sample_name).read_text())
        jsonschema.Draft202012Validator(schema).validate(sample)


def test_literature_schema_rejects_invalid_claim_shape() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((ROOT / "schemas" / "literature_grounding" / "evidence_claim_map.schema.json").read_text())
    sample = json.loads((ROOT / "examples" / "literature" / "sample_evidence_claim_map_output.json").read_text())
    sample["claims"] = [{}]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(sample)


def test_paper_card_schema_rejects_invalid_confidence_and_scope() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((ROOT / "schemas" / "literature_grounding" / "paper_card.schema.json").read_text())
    sample = json.loads((ROOT / "examples" / "literature" / "sample_paper_cards_output.json").read_text())
    claim = sample["paper_cards"][0]["extracted_claims"][0]
    claim["confidence"] = 99
    claim["claim_scope"] = "field_everywhere"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(sample)


def test_synthetic_fixtures_do_not_contain_real_bibliographic_claims() -> None:
    import re

    data = json.loads((ROOT / "examples" / "literature" / "sample_literature_input.json").read_text())
    text = json.dumps(data)
    assert not re.search(r"10\\.\\d{4,9}/", text)
    for record in data["papers"]:
        assert record["is_synthetic"] is True
        assert record["title"].startswith("Synthetic Example:")
        assert record["authors"] == []
        assert record["venue"] is None


def test_sample_json_can_ingest_and_preserve_synthetic_records(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path, "json_lit")
    run_cmd([sys.executable, "scripts/ingest_literature.py", "--workspace", str(workspace), "--input", "examples/literature/sample_literature_input.json", "--overwrite"])
    records = json.loads((workspace / "literature_evidence" / "bibliographic_records.json").read_text())
    assert len(records["bibliographic_records"]) == 5
    assert {record["paper_id"] for record in records["bibliographic_records"]} == {"P001", "P002", "P003", "P004", "P005"}
    assert all(record["is_synthetic"] is True for record in records["bibliographic_records"])
    assert records["missing_metadata"]


def test_sample_yaml_can_ingest_or_reports_clear_dependency(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path, "yaml_lit")
    result = run_cmd([sys.executable, "scripts/ingest_literature.py", "--workspace", str(workspace), "--input", "examples/literature/sample_literature_input.yaml", "--overwrite"], check=False)
    if result.returncode != 0:
        assert "YAML input requires PyYAML" in result.stderr
        pytest.skip("PyYAML not installed")
    records = json.loads((workspace / "literature_evidence" / "bibliographic_records.json").read_text())
    assert len(records["bibliographic_records"]) == 2


def test_sample_bibtex_can_ingest_without_metadata_fabrication(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path, "bib_lit")
    run_cmd([sys.executable, "scripts/ingest_literature.py", "--workspace", str(workspace), "--input", "examples/literature/sample_literature_input.bib", "--overwrite"])
    records = json.loads((workspace / "literature_evidence" / "bibliographic_records.json").read_text())
    first = records["bibliographic_records"][0]
    assert first["title"].startswith("Synthetic Example")
    assert first["doi"] is None
    assert "doi" in first["missing_metadata"]


def test_build_matrix_does_not_infer_detailed_content_from_title_only(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path, "title_only")
    title_only = tmp_path / "title_only.json"
    title_only.write_text(json.dumps({"papers": [{"title": "Synthetic Example: Title Only", "is_synthetic": True, "evidence_status": "user_provided", "source_type": "synthetic"}]}))
    run_cmd([sys.executable, "scripts/ingest_literature.py", "--workspace", str(workspace), "--input", str(title_only), "--overwrite"])
    run_cmd([sys.executable, "scripts/build_literature_matrix.py", "--workspace", str(workspace), "--overwrite"])
    cards = json.loads((workspace / "literature_evidence" / "paper_cards.json").read_text())
    card = cards["paper_cards"][0]
    assert card["method_family"] == "unknown"
    assert card["objectives"] == []
    assert card["extracted_claims"] == []
    assert "title-only" in card["extraction_uncertainty"]
