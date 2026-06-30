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
    workspace = tmp_path / "redteam_v03"
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", "redteam_v03", "--root", str(tmp_path), "--overwrite"])
    run_cmd([sys.executable, "scripts/build_validation_plan.py", "--workspace", str(workspace), "--overwrite", "--demo-if-missing"])
    return workspace


def read_plan(workspace: Path, filename: str) -> dict:
    return json.loads((workspace / "experiment_validation" / filename).read_text())


def write_plan(workspace: Path, filename: str, data: dict) -> None:
    (workspace / "experiment_validation" / filename).write_text(json.dumps(data))


def validate(workspace: Path) -> subprocess.CompletedProcess[str]:
    return run_cmd([sys.executable, "scripts/validate_experiment_plan.py", "--workspace", str(workspace), "--strict"], check=False)


def audit(workspace: Path) -> subprocess.CompletedProcess[str]:
    return run_cmd([sys.executable, "scripts/audit_validation_adequacy.py", "--workspace", str(workspace), "--strict"], check=False)


def test_fabricated_results_redteam_fails_validation_and_audit(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    design = read_plan(workspace, "experiment_design.json")
    design["experiment_designs"][0]["expected_result_pattern"] = "our method improves hypervolume by 20% and significantly outperforms all baselines"
    write_plan(workspace, "experiment_design.json", design)
    for result in [validate(workspace), audit(workspace)]:
        assert result.returncode != 0
        assert "fabricated result wording" in result.stdout or "unsupported empirical claim" in result.stdout


def test_weak_baseline_redteam_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    baseline = read_plan(workspace, "baseline_plan.json")
    baseline["baselines"] = [item for item in baseline["baselines"] if item["baseline_type"] == "random_or_greedy_baseline"]
    write_plan(workspace, "baseline_plan.json", baseline)
    result = audit(workspace)
    assert result.returncode != 0
    assert "weak baseline risk" in result.stdout or "missing sequential baseline" in result.stdout


def test_missing_ablation_redteam_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    ablation = read_plan(workspace, "ablation_plan.json")
    ablation["ablations"] = []
    write_plan(workspace, "ablation_plan.json", ablation)
    result = audit(workspace)
    assert result.returncode != 0
    assert "missing ablation for algorithmic contribution C2" in result.stdout
    assert "no-coevolution" in result.stdout


def test_metric_mismatch_redteam_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    metrics = read_plan(workspace, "metric_plan.json")
    metrics["metrics"] = [metric for metric in metrics["metrics"] if metric["metric_type"] == "runtime_metric"]
    write_plan(workspace, "metric_plan.json", metrics)
    result = audit(workspace)
    assert result.returncode != 0
    assert "missing Pareto quality metric" in result.stdout


def test_missing_feasibility_redteam_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    metrics = read_plan(workspace, "metric_plan.json")
    metrics["metrics"] = [metric for metric in metrics["metrics"] if metric["metric_type"] not in {"feasibility_metric", "constraint_violation_metric"}]
    write_plan(workspace, "metric_plan.json", metrics)
    result = audit(workspace)
    assert result.returncode != 0
    assert "missing feasibility metric" in result.stdout
    assert "constraint-specific violation" in result.stdout


def test_missing_statistical_test_redteam_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    stat = read_plan(workspace, "statistical_analysis_plan.json")
    stat["statistical_analyses"] = []
    write_plan(workspace, "statistical_analysis_plan.json", stat)
    result = validate(workspace)
    assert result.returncode != 0
    assert "missing statistical test" in result.stdout


def test_fake_significance_redteam_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    stat = read_plan(workspace, "statistical_analysis_plan.json")
    stat["statistical_analyses"][0]["interpretation_rule"] = "The method is statistically significant with p < 0.05."
    write_plan(workspace, "statistical_analysis_plan.json", stat)
    result = validate(workspace)
    assert result.returncode != 0
    assert "fabricated result wording" in result.stdout


def test_missing_reproducibility_redteam_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    repro = read_plan(workspace, "reproducibility_plan.json")
    repro["random_seed_policy"] = ""
    repro["parameter_requirements"] = []
    repro["computational_budget_policy"] = ""
    repro["environment_requirements"] = []
    write_plan(workspace, "reproducibility_plan.json", repro)
    result = validate(workspace)
    assert result.returncode != 0
    assert "missing reproducibility requirement" in result.stdout


def test_hidden_validation_risk_redteam_fails(tmp_path: Path) -> None:
    workspace = workspace_with_plan(tmp_path)
    report = read_plan(workspace, "experiment_grounding_report.json")
    report["reviewer_validation_risks"] = []
    report["experiment_context"]["experiment_risks"] = []
    write_plan(workspace, "experiment_grounding_report.json", report)
    result = audit(workspace)
    assert result.returncode != 0
    assert "hidden validation risk" in result.stdout
