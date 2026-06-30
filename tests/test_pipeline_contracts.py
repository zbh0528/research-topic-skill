from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_ORDER = [
    "00_project_intake",
    "01_domain_scan",
    "02_problem_identification",
    "03_theoretical_positioning",
    "04_contribution_argumentation",
    "05_chain_consistency_audit",
    "06_final_topic_package",
]
REQUIRED_FILES = ["input.json", "output.json", "output.md", "next_input.json", "validation_report.md"]


def run_cmd(args: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(f"command failed: {' '.join(args)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result


def test_skill_markdown_contains_key_constraints() -> None:
    text = (ROOT / "SKILL.md").read_text()
    for needle in [
        "next_input.json",
        "evidence_status",
        "reviewer_risks",
        "Do not use for fabricating",
        "resume",
        "traceability",
    ]:
        assert needle in text


def test_init_workspace_creates_persistent_contract(tmp_path: Path) -> None:
    result = run_cmd([
        sys.executable,
        "scripts/init_workspace.py",
        "--input",
        "examples/sample_project_input.yaml",
        "--project-id",
        "demo_project",
        "--root",
        str(tmp_path),
    ])
    assert "PASS initialized workspace" in result.stdout
    workspace = tmp_path / "demo_project"
    assert (workspace / "project_state.json").exists()
    state = json.loads((workspace / "project_state.json").read_text())
    assert state["module_order"] == MODULE_ORDER
    for module_id in MODULE_ORDER:
        module_dir = workspace / module_id
        assert module_dir.exists()
        for filename in REQUIRED_FILES:
            path = module_dir / filename
            assert path.exists()
            if filename.endswith(".json"):
                assert path.read_text().strip()
                json.loads(path.read_text())

    second = run_cmd([
        sys.executable,
        "scripts/init_workspace.py",
        "--input",
        "examples/sample_project_input.yaml",
        "--project-id",
        "demo_project",
        "--root",
        str(tmp_path),
    ], check=False)
    assert second.returncode != 0
    assert "already exists" in second.stderr


def test_resume_uses_direct_upstream_next_input(tmp_path: Path) -> None:
    run_cmd([
        sys.executable,
        "scripts/init_workspace.py",
        "--input",
        "examples/sample_project_input.yaml",
        "--project-id",
        "demo_project",
        "--root",
        str(tmp_path),
    ])
    workspace = tmp_path / "demo_project"
    result = run_cmd([
        sys.executable,
        "scripts/resume_from_module.py",
        "--workspace",
        str(workspace),
        "--module-id",
        "03_theoretical_positioning",
        "--overwrite-current",
    ])
    assert "PASS resumed 03_theoretical_positioning from direct upstream 02_problem_identification" in result.stdout
    loaded = json.loads((workspace / "03_theoretical_positioning" / "input.json").read_text())
    assert loaded["source_module_id"] == "02_problem_identification"
    assert loaded["source_next_input_path"].endswith("02_problem_identification/next_input.json")
    assert "source_output_path" not in loaded


def test_resume_maps_document_number_to_workspace_number(tmp_path: Path) -> None:
    run_cmd([
        sys.executable,
        "scripts/init_workspace.py",
        "--input",
        "examples/sample_project_input.yaml",
        "--project-id",
        "demo_project",
        "--root",
        str(tmp_path),
    ])
    workspace = tmp_path / "demo_project"
    result = run_cmd([
        sys.executable,
        "scripts/resume_from_module.py",
        "--workspace",
        str(workspace),
        "--module-id",
        "04_theoretical_positioning",
        "--overwrite-current",
    ])
    assert "mapped 04_theoretical_positioning -> 03_theoretical_positioning" in result.stdout


def test_validate_outputs_generates_summary(tmp_path: Path) -> None:
    run_cmd([
        sys.executable,
        "scripts/init_workspace.py",
        "--input",
        "examples/sample_project_input.yaml",
        "--project-id",
        "demo_project",
        "--root",
        str(tmp_path),
    ])
    workspace = tmp_path / "demo_project"
    result = run_cmd([
        sys.executable,
        "scripts/validate_outputs.py",
        "--workspace",
        str(workspace),
    ])
    assert "fail_count: 0" in result.stdout
    assert (workspace / "validation_summary.md").exists()
    for module_id in MODULE_ORDER:
        assert (workspace / module_id / "validation_report.md").read_text().startswith("# Validation Report")


def test_validate_outputs_fails_on_non_direct_upstream(tmp_path: Path) -> None:
    run_cmd([
        sys.executable,
        "scripts/init_workspace.py",
        "--input",
        "examples/sample_project_input.yaml",
        "--project-id",
        "demo_project",
        "--root",
        str(tmp_path),
    ])
    workspace = tmp_path / "demo_project"
    bad_input = json.loads((workspace / "03_theoretical_positioning" / "input.json").read_text())
    bad_input["source_module_id"] = "00_project_intake"
    (workspace / "03_theoretical_positioning" / "input.json").write_text(json.dumps(bad_input))
    result = run_cmd([
        sys.executable,
        "scripts/validate_outputs.py",
        "--workspace",
        str(workspace),
    ], check=False)
    assert result.returncode != 0
    assert "direct upstream 02_problem_identification" in result.stdout


def test_validate_outputs_fails_on_full_output_as_next_input(tmp_path: Path) -> None:
    run_cmd([
        sys.executable,
        "scripts/init_workspace.py",
        "--input",
        "examples/sample_project_input.yaml",
        "--project-id",
        "demo_project",
        "--root",
        str(tmp_path),
    ])
    workspace = tmp_path / "demo_project"
    output = json.loads((workspace / "00_project_intake" / "output.json").read_text())
    (workspace / "00_project_intake" / "next_input.json").write_text(json.dumps(output))
    result = run_cmd([
        sys.executable,
        "scripts/validate_outputs.py",
        "--workspace",
        str(workspace),
    ], check=False)
    assert result.returncode != 0
    assert "appears to contain full output fields" in result.stdout


def test_validate_outputs_fails_on_unsafe_claim(tmp_path: Path) -> None:
    run_cmd([
        sys.executable,
        "scripts/init_workspace.py",
        "--input",
        "examples/sample_project_input.yaml",
        "--project-id",
        "demo_project",
        "--root",
        str(tmp_path),
    ])
    workspace = tmp_path / "demo_project"
    path = workspace / "04_contribution_argumentation" / "output.json"
    output = json.loads(path.read_text())
    output["structured_output"]["central_thesis"] = "the first state-of-the-art framework"
    path.write_text(json.dumps(output))
    result = run_cmd([
        sys.executable,
        "scripts/validate_outputs.py",
        "--workspace",
        str(workspace),
    ], check=False)
    assert result.returncode != 0
    assert "unsafe strong claim" in result.stdout
