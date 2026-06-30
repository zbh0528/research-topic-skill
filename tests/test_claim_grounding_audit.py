from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cmd(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(f"command failed: {' '.join(args)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result


def prepared_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "audit_lit"
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", "audit_lit", "--root", str(tmp_path), "--overwrite"])
    run_cmd([sys.executable, "scripts/ingest_literature.py", "--workspace", str(workspace), "--input", "examples/literature/sample_literature_input.json", "--overwrite"])
    run_cmd([sys.executable, "scripts/build_literature_matrix.py", "--workspace", str(workspace), "--overwrite"])
    return workspace


def set_module_payload(workspace: Path, rel: str, payload: dict) -> None:
    path = workspace / rel
    data = json.loads(path.read_text())
    data["status"] = "complete"
    data["structured_output"] = payload
    path.write_text(json.dumps(data))


def audit_fails(workspace: Path, expected: str) -> None:
    result = run_cmd([sys.executable, "scripts/audit_claim_grounding.py", "--workspace", str(workspace), "--strict"], check=False)
    assert result.returncode != 0
    assert expected in result.stdout


def test_grounded_claim_without_evidence_id_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    set_module_payload(workspace, "04_contribution_argumentation/output.json", {"claims": [{"claim_id": "CL_BAD", "grounding_status": "grounded"}]})
    audit_fails(workspace, "grounded claim without evidence_id")


def test_verified_claim_without_source_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    set_module_payload(workspace, "04_contribution_argumentation/output.json", {"claims": [{"claim_id": "CL_BAD", "evidence_status": "verified"}]})
    audit_fails(workspace, "unsupported verified claim")


def test_synthetic_verified_claim_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    set_module_payload(workspace, "04_contribution_argumentation/output.json", {"claims": [{"claim_id": "CL_BAD", "evidence_status": "verified", "linked_paper_ids": ["P001"], "source_field": "user_notes"}]})
    audit_fails(workspace, "synthetic evidence used as verified")


def test_unsafe_first_or_sota_claim_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    set_module_payload(workspace, "04_contribution_argumentation/output.json", {"claim": "the first state-of-the-art framework"})
    audit_fails(workspace, "unsafe novelty wording")


def test_gap_without_corpus_scope_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    set_module_payload(workspace, "02_problem_identification/output.json", {"gap": {"gap_id": "G_BAD", "supporting_evidence_ids": ["EV001"]}})
    audit_fails(workspace, "gap claim without corpus_scope")


def test_hidden_counterevidence_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    set_module_payload(workspace, "06_final_topic_package/output.json", {"final_claim": "corpus-scoped candidate package", "evidence_traceability_table": []})
    audit_fails(workspace, "hidden counterevidence")


def test_field_general_without_evidence_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    set_module_payload(workspace, "04_contribution_argumentation/output.json", {"claims": [{"claim_id": "CL_BAD", "claim_scope": "field_general"}]})
    audit_fails(workspace, "field-general claim without evidence")


def test_contribution_without_linked_evidence_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    set_module_payload(workspace, "04_contribution_argumentation/output.json", {"contributions": [{"contribution_id": "C_BAD", "claim_type": "contribution_claim"}]})
    audit_fails(workspace, "contribution_claim without linked evidence")


def test_sample_literature_outputs_validate_against_schema() -> None:
    jsonschema = __import__("jsonschema")
    pairs = [
        ("schemas/literature_grounding/evidence_claim_map.schema.json", "examples/literature/sample_evidence_claim_map_output.json"),
        ("schemas/literature_grounding/literature_gap_audit.schema.json", "examples/literature/sample_literature_gap_audit_output.json"),
    ]
    for schema_rel, example_rel in pairs:
        jsonschema.Draft202012Validator(json.loads((ROOT / schema_rel).read_text())).validate(json.loads((ROOT / example_rel).read_text()))
