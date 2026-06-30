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
    workspace = tmp_path / "audit_demo"
    run_cmd([sys.executable, "scripts/init_workspace.py", "--input", "examples/sample_project_input.yaml", "--project-id", "audit_demo", "--root", str(tmp_path), "--overwrite"])
    run_cmd([sys.executable, "scripts/build_validation_plan.py", "--workspace", str(workspace), "--overwrite", "--demo-if-missing"])
    return workspace


def load(workspace: Path, filename: str) -> dict:
    path = workspace / "experiment_validation" / filename
    return json.loads(path.read_text())


def dump(workspace: Path, filename: str, data: dict) -> None:
    path = workspace / "experiment_validation" / filename
    path.write_text(json.dumps(data))


def audit(workspace: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return run_cmd([sys.executable, "scripts/audit_validation_adequacy.py", "--workspace", str(workspace), "--strict", *extra], check=False)


def test_contribution_without_validation_target_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "validation_targets.json")
    data["validation_targets"] = data["validation_targets"][1:]
    dump(workspace, "validation_targets.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "contribution without validation target" in result.stdout


def test_validation_target_without_experiment_design_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "experiment_design.json")
    data["experiment_designs"] = []
    dump(workspace, "experiment_design.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "validation target without experiment design" in result.stdout


def test_experiment_design_without_baseline_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "baseline_plan.json")
    data["baselines"] = []
    dump(workspace, "baseline_plan.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "experiment design without baseline" in result.stdout


def test_experiment_design_without_metric_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "metric_plan.json")
    data["metrics"] = []
    dump(workspace, "metric_plan.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "experiment design without metric" in result.stdout


def test_algorithmic_contribution_without_ablation_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "ablation_plan.json")
    data["ablations"] = []
    dump(workspace, "ablation_plan.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "missing ablation for algorithmic contribution C2" in result.stdout


def test_multi_objective_claim_without_pareto_metric_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "metric_plan.json")
    data["metrics"] = [metric for metric in data["metrics"] if metric["metric_type"] != "pareto_quality_metric"]
    dump(workspace, "metric_plan.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "missing Pareto quality metric" in result.stdout


def test_constrained_claim_without_feasibility_metric_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "metric_plan.json")
    data["metrics"] = [metric for metric in data["metrics"] if metric["metric_type"] not in {"feasibility_metric", "constraint_violation_metric"}]
    dump(workspace, "metric_plan.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "missing feasibility metric" in result.stdout


def test_joint_claim_without_sequential_baseline_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "baseline_plan.json")
    data["baselines"] = [baseline for baseline in data["baselines"] if baseline["baseline_type"] not in {"sequential_optimization", "layout_only_optimization", "cabling_only_optimization"}]
    dump(workspace, "baseline_plan.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "missing sequential baseline" in result.stdout


def test_stochastic_comparison_without_statistical_plan_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "statistical_analysis_plan.json")
    data["statistical_analyses"] = []
    dump(workspace, "statistical_analysis_plan.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "missing statistical test" in result.stdout


def test_reproducibility_plan_missing_random_seeds_fails(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    data = load(workspace, "reproducibility_plan.json")
    data["random_seed_policy"] = ""
    dump(workspace, "reproducibility_plan.json", data)
    result = audit(workspace)
    assert result.returncode != 0
    assert "missing reproducibility requirement: random seeds" in result.stdout


def test_complete_validation_chain_fails_clearly_on_draft_workspace(tmp_path: Path) -> None:
    workspace = prepared_workspace(tmp_path)
    result = audit(workspace, "--require-complete-validation-chain")
    assert result.returncode != 0
    assert "demo plan requires real contribution chain" in result.stdout
    assert "incomplete final topic package" in result.stdout
    assert "missing contribution-to-experiment traceability table" in result.stdout
