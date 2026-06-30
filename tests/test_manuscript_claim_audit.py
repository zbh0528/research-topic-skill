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


def workspace_with_plan(tmp_path: Path) -> Path:
    workspace = tmp_path / "manuscript_claim_audit"
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", "manuscript_claim_audit", "--root", str(tmp_path), "--overwrite"])
    run_cmd([sys.executable, "scripts/build_manuscript_blueprint.py", "--workspace", str(workspace), "--overwrite", "--demo-if-missing"])
    return workspace


def load(workspace: Path, filename: str) -> dict:
    return json.loads((workspace / "manuscript_grounding" / filename).read_text())


def dump(workspace: Path, filename: str, data: dict) -> None:
    (workspace / "manuscript_grounding" / filename).write_text(json.dumps(data))


def validate(workspace: Path) -> subprocess.CompletedProcess[str]:
    return run_cmd([sys.executable, "scripts/validate_manuscript_plan.py", "--workspace", str(workspace), "--strict"], check=False)


def audit(workspace: Path) -> subprocess.CompletedProcess[str]:
    return run_cmd([sys.executable, "scripts/audit_manuscript_claims.py", "--workspace", str(workspace), "--strict"], check=False)


def test_fabricated_citation_and_result_wording_redteam_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    plan = load(workspace, "paragraph_claim_plan.json")
    plan["manuscript_claims"][0]["claim_text"] = "Smith et al. (2024) prove the method significantly outperforms baselines with p < 0.05."
    dump(workspace, "paragraph_claim_plan.json", plan)
    for result in [validate(workspace), audit(workspace)]:
        assert result.returncode != 0
        assert "fabricated citation risk" in result.stdout
        assert "fabricated result wording" in result.stdout


def test_unsupported_manuscript_claim_without_traceability_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    plan = load(workspace, "paragraph_claim_plan.json")
    claim = plan["manuscript_claims"][0]
    claim["linked_contribution_id"] = ""
    claim["linked_evidence_ids"] = []
    claim["linked_experiment_ids"] = []
    claim["linked_result_placeholders"] = []
    dump(workspace, "paragraph_claim_plan.json", plan)
    result = audit(workspace)
    assert result.returncode != 0
    assert "manuscript claim without traceability" in result.stdout


def test_missing_manuscript_traceability_table_fails_workspace_validation(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    report = load(workspace, "manuscript_grounding_report.json")
    report["contribution_to_manuscript_traceability_table"] = []
    dump(workspace, "manuscript_grounding_report.json", report)
    result = run_cmd([sys.executable, "scripts/validate_outputs.py", "--workspace", str(workspace), "--manuscript-grounded", "--strict-manuscript"], check=False)
    assert result.returncode != 0
    assert "Contribution-to-Manuscript Traceability table" in result.stdout
