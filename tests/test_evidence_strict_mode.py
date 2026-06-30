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


def prepared_workspace(tmp_path: Path, project_id: str = "strict_lit") -> Path:
    workspace = tmp_path / project_id
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", project_id, "--root", str(tmp_path), "--overwrite"])
    run_cmd([sys.executable, "scripts/ingest_literature.py", "--workspace", str(workspace), "--input", "examples/literature/sample_literature_input.json", "--overwrite"])
    run_cmd([sys.executable, "scripts/build_literature_matrix.py", "--workspace", str(workspace), "--overwrite"])
    return workspace


def test_validate_outputs_strict_finds_unsupported_verified_claim(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    path = workspace / "04_contribution_argumentation" / "output.json"
    output = json.loads(path.read_text())
    output["status"] = "complete"
    output["structured_output"]["claims"] = [{"claim_id": "CL_BAD", "evidence_status": "verified"}]
    path.write_text(json.dumps(output))
    result = run_cmd([sys.executable, "scripts/validate_outputs.py", "--workspace", str(workspace), "--literature-grounded", "--strict-evidence"], check=False)
    assert result.returncode != 0
    assert "unsupported verified claim" in result.stdout


def test_audit_strict_finds_contribution_without_evidence(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    path = workspace / "04_contribution_argumentation" / "output.json"
    output = json.loads(path.read_text())
    output["status"] = "complete"
    output["structured_output"] = {"contributions": [{"contribution_id": "C_BAD", "claim_type": "contribution_claim"}]}
    path.write_text(json.dumps(output))
    result = run_cmd([sys.executable, "scripts/audit_claim_grounding.py", "--workspace", str(workspace), "--strict"], check=False)
    assert result.returncode != 0
    assert "contribution_claim without linked evidence" in result.stdout


def test_logic_only_workspace_not_strict_checked_without_flag(tmp_path: Path) -> None:
    workspace = tmp_path / "logic_only"
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", "logic_only", "--root", str(tmp_path), "--overwrite"])
    result = run_cmd([sys.executable, "scripts/validate_outputs.py", "--workspace", str(workspace)])
    assert "fail_count: 0" in result.stdout


def test_next_input_over_expansion_still_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    output = json.loads((workspace / "00_project_intake" / "output.json").read_text())
    (workspace / "00_project_intake" / "next_input.json").write_text(json.dumps(output))
    result = run_cmd([sys.executable, "scripts/validate_outputs.py", "--workspace", str(workspace)], check=False)
    assert result.returncode != 0
    assert "appears to contain full output fields" in result.stdout


def test_evidence_context_exists_after_matrix_build(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    next_input = json.loads((workspace / "00_project_intake" / "next_input.json").read_text())
    assert "evidence_context" in next_input
    assert "key_grounded_claims" in next_input["evidence_context"]
    text = json.dumps(next_input["evidence_context"])
    assert "source_excerpt" not in text
    assert "paraphrase" not in text
    assert "abstract" not in text


def test_strict_rejects_overexpanded_evidence_context(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    path = workspace / "00_project_intake" / "next_input.json"
    next_input = json.loads(path.read_text())
    next_input["evidence_context"]["key_grounded_claims"][0]["source_excerpt"] = "too much source text"
    path.write_text(json.dumps(next_input))
    output_path = workspace / "00_project_intake" / "output.json"
    output = json.loads(output_path.read_text())
    output["next_input"] = next_input
    output_path.write_text(json.dumps(output))
    result = run_cmd([sys.executable, "scripts/validate_outputs.py", "--workspace", str(workspace), "--literature-grounded", "--strict-evidence"], check=False)
    assert result.returncode != 0
    assert "over-expanded evidence fields" in result.stdout


def test_final_topic_package_without_traceability_table_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    path = workspace / "06_final_topic_package" / "output.json"
    output = json.loads(path.read_text())
    output["status"] = "complete"
    output["structured_output"] = {"claim": "within the provided corpus"}
    path.write_text(json.dumps(output))
    result = run_cmd([sys.executable, "scripts/validate_outputs.py", "--workspace", str(workspace), "--literature-grounded", "--strict-evidence"], check=False)
    assert result.returncode != 0
    assert "Evidence Traceability Table" in result.stdout


def test_absence_of_evidence_wording_is_flagged(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    path = workspace / "04_contribution_argumentation" / "output.json"
    output = json.loads(path.read_text())
    output["status"] = "complete"
    output["structured_output"] = {"claim": "no one has studied this problem"}
    path.write_text(json.dumps(output))
    result = run_cmd([sys.executable, "scripts/audit_claim_grounding.py", "--workspace", str(workspace), "--strict"], check=False)
    assert result.returncode != 0
    assert "absence-of-evidence" in result.stdout


def test_corpus_scoped_wording_can_pass(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    path = workspace / "04_contribution_argumentation" / "output.json"
    output = json.loads(path.read_text())
    output["status"] = "complete"
    output["structured_output"] = {"claim": "within the provided corpus, no sufficient evidence was found", "evidence_traceability_table": []}
    path.write_text(json.dumps(output))
    result = run_cmd([sys.executable, "scripts/audit_claim_grounding.py", "--workspace", str(workspace), "--strict"], check=False)
    assert "absence-of-evidence" not in result.stdout
