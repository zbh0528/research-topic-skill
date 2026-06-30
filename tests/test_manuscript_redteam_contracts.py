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
    workspace = tmp_path / "manuscript_redteam"
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", "manuscript_redteam", "--root", str(tmp_path), "--overwrite"])
    run_cmd([sys.executable, "scripts/build_manuscript_blueprint.py", "--workspace", str(workspace), "--overwrite", "--demo-if-missing"])
    return workspace


def load(workspace: Path, filename: str) -> dict:
    return json.loads((workspace / "manuscript_grounding" / filename).read_text())


def dump(workspace: Path, filename: str, data: dict) -> None:
    (workspace / "manuscript_grounding" / filename).write_text(json.dumps(data))


def audit(workspace: Path) -> subprocess.CompletedProcess[str]:
    return run_cmd([sys.executable, "scripts/audit_manuscript_claims.py", "--workspace", str(workspace), "--strict"], check=False)


def test_weak_introduction_jump_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    data = load(workspace, "section_argument_map.json")
    data["section_arguments"][0]["argument_chain"] = ["background", "contribution preview"]
    dump(workspace, "section_argument_map.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "weak introduction link: missing gap" in result.stdout


def test_related_work_dumping_without_stream_organization_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    data = load(workspace, "section_argument_map.json")
    for item in data["section_arguments"]:
        if item["section_name"] == "Related Work":
            item["argument_chain"] = ["paper list", "paper list", "paper list"]
    dump(workspace, "section_argument_map.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "weak related work link" in result.stdout


def test_method_algorithm_wrapping_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    data = load(workspace, "method_section_alignment.json")
    data["method_component_alignments"][0]["linked_problem_property"] = ""
    dump(workspace, "method_section_alignment.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "method component without problem property link" in result.stdout


def test_experiment_section_mismatch_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    data = load(workspace, "experiment_section_alignment.json")
    data["experiment_section_items"][0]["metric_ids"] = []
    dump(workspace, "experiment_section_alignment.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "experiment section mismatch" in result.stdout


def test_hidden_limitation_and_counterevidence_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    data = load(workspace, "discussion_limitations_plan.json")
    data["counterevidence"] = []
    dump(workspace, "discussion_limitations_plan.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "hidden limitation risk" in result.stdout
