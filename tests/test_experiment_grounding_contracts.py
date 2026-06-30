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


def init_workspace(tmp_path: Path, project_id: str = "exp_demo") -> Path:
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", project_id, "--root", str(tmp_path), "--overwrite"])
    return tmp_path / project_id


def build_plan(workspace: Path) -> None:
    run_cmd([sys.executable, "scripts/build_validation_plan.py", "--workspace", str(workspace), "--overwrite", "--demo-if-missing"])


def test_experiment_schemas_are_valid_json_objects() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    for path in (ROOT / "schemas" / "experiment_grounding").glob("*.schema.json"):
        schema = json.loads(path.read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        assert schema["type"] == "object", path
        assert "required" in schema, path
        assert schema.get("additionalProperties") is False, path


def test_experiment_examples_validate_against_schemas() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    pairs = {
        "validation_target.schema.json": "sample_validation_targets_output.json",
        "experiment_design.schema.json": "sample_experiment_design_output.json",
        "baseline_plan.schema.json": "sample_baseline_plan_output.json",
        "metric_plan.schema.json": "sample_metric_plan_output.json",
        "ablation_plan.schema.json": "sample_ablation_plan_output.json",
        "case_study_plan.schema.json": "sample_case_study_plan_output.json",
        "statistical_analysis_plan.schema.json": "sample_statistical_analysis_plan_output.json",
        "reproducibility_plan.schema.json": "sample_reproducibility_plan_output.json",
        "validation_adequacy_audit.schema.json": "sample_validation_adequacy_audit_output.json",
        "experiment_grounding_report.schema.json": "sample_experiment_grounding_report_output.json",
    }
    for schema_name, sample_name in pairs.items():
        schema = json.loads((ROOT / "schemas" / "experiment_grounding" / schema_name).read_text())
        sample = json.loads((ROOT / "examples" / "experiment" / sample_name).read_text())
        jsonschema.Draft202012Validator(schema).validate(sample)


def test_build_validate_audit_and_checklist_flow(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    build_plan(workspace)
    run_cmd([sys.executable, "scripts/validate_experiment_plan.py", "--workspace", str(workspace), "--strict"])
    run_cmd([sys.executable, "scripts/audit_validation_adequacy.py", "--workspace", str(workspace), "--strict"])
    result = run_cmd([sys.executable, "scripts/generate_reproducibility_checklist.py", "--workspace", str(workspace)])
    assert "PASS generated reproducibility checklist" in result.stdout
    result = run_cmd([sys.executable, "scripts/validate_outputs.py", "--workspace", str(workspace), "--experiment-grounded", "--strict-validation"])
    assert "fail_count: 0" in result.stdout


def test_id_uniqueness_check_is_effective(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    build_plan(workspace)
    path = workspace / "experiment_validation" / "metric_plan.json"
    data = json.loads(path.read_text())
    data["metrics"][1]["metric_id"] = data["metrics"][0]["metric_id"]
    path.write_text(json.dumps(data))
    result = run_cmd([sys.executable, "scripts/validate_experiment_plan.py", "--workspace", str(workspace), "--strict"], check=False)
    assert result.returncode != 0
    assert "duplicate metric_id" in result.stdout


def test_reference_integrity_check_is_effective(tmp_path: Path) -> None:
    workspace = init_workspace(tmp_path)
    build_plan(workspace)
    path = workspace / "experiment_validation" / "baseline_plan.json"
    data = json.loads(path.read_text())
    data["baselines"][0]["linked_experiment_id"] = "EX999"
    path.write_text(json.dumps(data))
    result = run_cmd([sys.executable, "scripts/validate_experiment_plan.py", "--workspace", str(workspace), "--strict"], check=False)
    assert result.returncode != 0
    assert "links unknown experiment_id" in result.stdout


def test_expected_result_patterns_are_conditional_in_samples() -> None:
    for path in (ROOT / "examples" / "experiment").glob("*.json"):
        text = path.read_text().lower()
        assert "outperforms" not in text
        assert "p <" not in text
        assert "statistically significant" not in text
        if "expected_result_pattern" in text:
            assert "conditional" in text


def test_final_topic_package_sample_has_experiment_traceability_table() -> None:
    data = json.loads((ROOT / "examples" / "experiment" / "sample_grounded_final_topic_package_with_validation_output.json").read_text())
    structured = data["structured_output"]
    rows = structured["contribution_to_experiment_traceability_table"]
    assert rows
    for key in ["contribution_id", "validation_target_id", "experiment_id", "baseline_ids", "metric_ids", "artifact_ids", "validation_status"]:
        assert key in rows[0]


def test_manifest_and_skill_advertise_v03() -> None:
    manifest = json.loads((ROOT / "skill_manifest.json").read_text())
    assert manifest["version"] == "0.3.0"
    assert "experiment_grounded_mode" in manifest["modes"]
    assert "experiment_grounding_modules" in manifest
    skill = (ROOT / "SKILL.md").read_text()
    assert "v0.3.0-experiment-grounded-validation-planning" in skill
    assert "does not fabricate experimental results" in skill
