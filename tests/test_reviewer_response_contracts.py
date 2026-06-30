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
    workspace = tmp_path / "reviewer_contract"
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", "reviewer_contract", "--root", str(tmp_path), "--overwrite"])
    run_cmd([sys.executable, "scripts/build_manuscript_blueprint.py", "--workspace", str(workspace), "--overwrite", "--demo-if-missing"])
    return workspace


def test_reviewer_response_plan_is_nonempty_and_counts_objections(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    result = run_cmd([sys.executable, "scripts/generate_reviewer_response_plan.py", "--workspace", str(workspace), "--overwrite"])
    assert "PASS generated reviewer response plan" in result.stdout
    data = json.loads((workspace / "manuscript_grounding" / "reviewer_response_plan.json").read_text())
    assert data["is_received_reviewer_response"] is False
    assert data["objection_count"] > 0
    assert data["strategy_count"] > 0
    assert "RO001" in (workspace / "manuscript_grounding" / "reviewer_response_plan.md").read_text()


def test_fake_received_reviewer_comment_wording_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    path = workspace / "manuscript_grounding" / "reviewer_response_strategy.json"
    data = json.loads(path.read_text())
    data["response_strategies"][0]["direct_answer_plan"] = "Reviewer 2 said the method is unclear, so we claim this is resolved."
    path.write_text(json.dumps(data))
    result = run_cmd([sys.executable, "scripts/audit_manuscript_claims.py", "--workspace", str(workspace), "--strict"], check=False)
    assert result.returncode != 0
    assert "fake reviewer comment risk" in result.stdout
