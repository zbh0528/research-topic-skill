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


def init_workspace(tmp_path: Path) -> Path:
    run_cmd([
        sys.executable,
        "scripts/init_workspace.py",
        "--input",
        "examples/sample_project_input.yaml",
        "--project-id",
        "negative_demo",
        "--root",
        str(tmp_path),
    ])
    return tmp_path / "negative_demo"


def validate_fails(workspace: Path, needle: str) -> None:
    result = run_cmd([
        sys.executable,
        "scripts/validate_outputs.py",
        "--workspace",
        str(workspace),
    ], check=False)
    assert result.returncode != 0
    assert needle in result.stdout


def output_path(workspace: Path, module_id: str = "00_project_intake") -> Path:
    return workspace / module_id / "output.json"


def test_missing_reviewer_risks_fails(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    output = json.loads(output_path(workspace).read_text())
    del output["reviewer_risks"]
    output_path(workspace).write_text(json.dumps(output))
    validate_fails(workspace, "reviewer_risks")


def test_missing_trace_context_fails(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    output = json.loads(output_path(workspace).read_text())
    del output["trace_context"]
    output_path(workspace).write_text(json.dumps(output))
    validate_fails(workspace, "trace_context")


def test_invalid_evidence_status_fails(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    output = json.loads(output_path(workspace).read_text())
    output["assumptions"][0]["evidence_status"] = "unsupported_status"
    output_path(workspace).write_text(json.dumps(output))
    validate_fails(workspace, "unsupported_status")


def test_empty_next_input_fails(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    (workspace / "00_project_intake" / "next_input.json").write_text("")
    validate_fails(workspace, "invalid JSON")


def test_invalid_output_json_fails(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    output_path(workspace).write_text("{not json")
    validate_fails(workspace, "invalid JSON")


def test_unsafe_contribution_claim_fails(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    path = output_path(workspace, "04_contribution_argumentation")
    output = json.loads(path.read_text())
    output["structured_output"]["central_thesis"] = "the first state-of-the-art framework"
    path.write_text(json.dumps(output))
    validate_fails(workspace, "unsafe strong claim")


def test_full_output_as_next_input_fails(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    output = json.loads(output_path(workspace).read_text())
    (workspace / "00_project_intake" / "next_input.json").write_text(json.dumps(output))
    validate_fails(workspace, "appears to contain full output fields")


def test_resume_reads_only_direct_upstream_next_input(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    path = output_path(workspace)
    output = json.loads(path.read_text())
    output["structured_output"]["researcher_profile"]["sentinel"] = "SHOULD_NOT_BE_READ_FROM_OUTPUT_JSON"
    output["next_input"]["target_output"] = "research topic package SHOULD_BE_READ_FROM_NEXT_INPUT_JSON"
    path.write_text(json.dumps(output))
    (workspace / "00_project_intake" / "next_input.json").write_text(json.dumps(output["next_input"]))

    run_cmd([
        sys.executable,
        "scripts/resume_from_module.py",
        "--workspace",
        str(workspace),
        "--module-id",
        "01_domain_scan",
        "--overwrite-current",
    ])
    text = (workspace / "01_domain_scan" / "input.json").read_text()
    assert "SHOULD_BE_READ_FROM_NEXT_INPUT_JSON" in text
    assert "SHOULD_NOT_BE_READ_FROM_OUTPUT_JSON" not in text
