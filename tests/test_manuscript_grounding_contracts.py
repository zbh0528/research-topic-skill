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


def init_workspace(tmp_path: Path, project_id: str = "manuscript_demo") -> Path:
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", project_id, "--root", str(tmp_path), "--overwrite"])
    return tmp_path / project_id


def build_plan(workspace: Path) -> None:
    run_cmd([sys.executable, "scripts/build_manuscript_blueprint.py", "--workspace", str(workspace), "--overwrite", "--demo-if-missing"])


def test_manuscript_schemas_are_valid_json_objects() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schemas = sorted((ROOT / "schemas" / "manuscript_grounding").glob("*.schema.json"))
    assert len(schemas) == 13
    for path in schemas:
        schema = json.loads(path.read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        assert schema["type"] == "object", path
        assert "required" in schema, path
        assert schema.get("additionalProperties") is False, path


def test_manuscript_examples_validate_against_schemas() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    for schema_path in (ROOT / "schemas" / "manuscript_grounding").glob("*.schema.json"):
        sample_path = ROOT / "examples" / "manuscript" / f"sample_{schema_path.stem.removesuffix('.schema')}_output.json"
        schema = json.loads(schema_path.read_text())
        sample = json.loads(sample_path.read_text())
        jsonschema.Draft202012Validator(schema).validate(sample)


def test_build_validate_audit_checklist_and_workspace_validation_flow(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    result = run_cmd([sys.executable, "scripts/build_manuscript_blueprint.py", "--workspace", str(workspace), "--overwrite", "--demo-if-missing"])
    assert "PASS built manuscript blueprint" in result.stdout
    run_cmd([sys.executable, "scripts/validate_manuscript_plan.py", "--workspace", str(workspace), "--strict"])
    run_cmd([sys.executable, "scripts/audit_manuscript_claims.py", "--workspace", str(workspace), "--strict"])
    result = run_cmd([sys.executable, "scripts/generate_manuscript_checklist.py", "--workspace", str(workspace), "--strict"])
    assert "PASS generated manuscript checklist" in result.stdout
    result = run_cmd([sys.executable, "scripts/validate_outputs.py", "--workspace", str(workspace), "--manuscript-grounded", "--strict-manuscript"])
    assert "PASS manuscript_grounding directory exists" in result.stdout
    assert "fail_count: 0" in result.stdout


def test_complete_manuscript_chain_fails_demo_workspace_with_clear_reason(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    build_plan(workspace)
    result = run_cmd([sys.executable, "scripts/audit_manuscript_claims.py", "--workspace", str(workspace), "--strict", "--require-complete-manuscript-chain"], check=False)
    assert result.returncode != 0
    assert "demo manuscript plan requires real final topic package and real results" in result.stdout
    assert "incomplete final topic package" in result.stdout
    assert "manuscript traceability table incomplete" in result.stdout


def test_manifest_and_skill_advertise_v04() -> None:
    manifest = json.loads((ROOT / "skill_manifest.json").read_text())
    assert manifest["version"] == "0.4.0"
    assert "manuscript_grounded_mode" in manifest["modes"]
    assert "manuscript_grounding_modules" in manifest
    assert "manuscript_claim_status" in manifest
    skill = (ROOT / "SKILL.md").read_text()
    assert "v0.4.0-manuscript-structure-and-reviewer-response-grounded-writing-support" in skill
    assert "does not write a final paper" in skill
