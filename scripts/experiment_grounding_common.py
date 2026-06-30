#!/usr/bin/env python3
"""Shared helpers for v0.3 experiment-grounded validation planning."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_DIR_NAME = "experiment_validation"

VALIDATION_STATUSES = [
    "validation_planned",
    "partially_planned",
    "insufficiently_planned",
    "unsupported_by_experiment_plan",
    "not_applicable",
    "requires_empirical_results",
]

EXPERIMENT_SUPPORT_STATUSES = [
    "directly_tested_by_plan",
    "indirectly_tested_by_plan",
    "weakly_tested_by_plan",
    "not_tested",
    "requires_new_experiment",
    "cannot_be_validated_empirically",
]

VALIDATION_CLAIM_TYPES = [
    "model_validity_claim",
    "algorithm_effectiveness_claim",
    "mechanism_necessity_claim",
    "tradeoff_insight_claim",
    "robustness_claim",
    "scalability_claim",
    "feasibility_claim",
    "runtime_claim",
    "constraint_handling_claim",
    "pareto_quality_claim",
    "engineering_value_claim",
    "benchmark_claim",
    "reproducibility_claim",
]

BASELINE_TYPES = [
    "classical_evolutionary_algorithm",
    "multi_objective_evolutionary_algorithm",
    "problem_specific_heuristic",
    "mathematical_programming",
    "graph_algorithm",
    "sequential_optimization",
    "layout_only_optimization",
    "cabling_only_optimization",
    "joint_optimization_existing_method",
    "random_or_greedy_baseline",
    "surrogate_assisted_baseline",
    "ablated_variant",
    "user_provided_baseline",
    "literature_supported_baseline",
]

METRIC_TYPES = [
    "objective_value",
    "cost_metric",
    "energy_metric",
    "wake_loss_metric",
    "cable_cost_metric",
    "electrical_loss_metric",
    "levelized_cost_metric",
    "pareto_quality_metric",
    "convergence_metric",
    "diversity_metric",
    "feasibility_metric",
    "constraint_violation_metric",
    "runtime_metric",
    "scalability_metric",
    "robustness_metric",
    "sensitivity_metric",
    "statistical_metric",
    "engineering_interpretability_metric",
]

EXPERIMENT_TYPES = [
    "baseline_comparison",
    "ablation_study",
    "sensitivity_analysis",
    "scalability_analysis",
    "constraint_handling_analysis",
    "pareto_tradeoff_analysis",
    "case_study_analysis",
    "robustness_analysis",
    "runtime_analysis",
    "feasibility_analysis",
    "engineering_interpretability_analysis",
]

CASE_STUDY_TYPES = [
    "synthetic_instance",
    "benchmark_instance",
    "real_site_case",
    "literature_case",
    "user_provided_case",
    "scalability_instance",
    "stress_test_instance",
]

TEST_TYPES = [
    "wilcoxon_signed_rank",
    "mann_whitney_u",
    "friedman_test",
    "nemenyi_posthoc",
    "paired_t_test",
    "anova",
    "bootstrap_confidence_interval",
    "effect_size_analysis",
    "descriptive_statistics_only",
    "not_applicable",
]

ARTIFACT_TYPES = [
    "source_code",
    "configuration_file",
    "input_instance",
    "processed_dataset",
    "raw_result",
    "statistical_analysis_script",
    "figure_generation_script",
    "experiment_log",
    "parameter_table",
    "environment_file",
    "readme",
    "supplementary_material",
]

FABRICATED_RESULT_PATTERNS = [
    re.compile(r"\boutperforms?\b", re.I),
    re.compile(r"\bsignificantly\s+(better|outperforms?|improves?)\b", re.I),
    re.compile(r"\bstatistically\s+significant\b", re.I),
    re.compile(r"\bp\s*[<=>]\s*0?\.\d+\b", re.I),
    re.compile(r"\bimproves?\s+by\s+\d", re.I),
    re.compile(r"\bachieves?\s+\d", re.I),
    re.compile(r"\b(best|superior)\s+(result|performance|hypervolume|igd)\b", re.I),
]

SAFE_WORDING_PATH_PARTS = {
    "unsafe_wording_to_avoid",
    "prohibited_wording",
    "prohibited_result_wording",
    "fabricated_result_risks",
    "reviewer_validation_risks",
    "reviewer_risks",
    "repair_actions",
    "recommended_repairs",
    "limitations",
    "failure_pattern",
    "risk_if_missing",
}


@dataclass
class Finding:
    level: str
    message: str


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_workspace(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def experiment_dir(workspace: Path, experiment_dir_arg: Path | None = None) -> Path:
    if experiment_dir_arg is None:
        return workspace / EXPERIMENT_DIR_NAME
    return experiment_dir_arg if experiment_dir_arg.is_absolute() else workspace / experiment_dir_arg


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def iter_strings(value: Any, path: tuple[Any, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from iter_strings(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_strings(child, (*path, index))
    elif isinstance(value, str):
        yield path, value


def iter_dicts(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_dicts(child)


def safe_wording_path(path: tuple[Any, ...]) -> bool:
    return any(str(part) in SAFE_WORDING_PATH_PARTS for part in path)


def find_fabricated_result_wording(value: Any) -> list[str]:
    findings: list[str] = []
    for path, text in iter_strings(value):
        if safe_wording_path(path):
            continue
        for pattern in FABRICATED_RESULT_PATTERNS:
            if pattern.search(text):
                findings.append(f"{'.'.join(map(str, path))}: {text}")
                break
    return findings


def text_blob(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False).lower()


def contains_any(value: Any, needles: list[str]) -> bool:
    blob = text_blob(value)
    return any(needle.lower() in blob for needle in needles)


def id_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def real_contribution_items(workspace: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for rel in ["04_contribution_argumentation/output.json", "06_final_topic_package/output.json"]:
        path = workspace / rel
        if not path.exists():
            continue
        data = read_json(path)
        if not isinstance(data, dict) or data.get("status") == "draft":
            continue
        structured = data.get("structured_output", {})
        if not isinstance(structured, dict):
            continue
        for key in ("contributions", "contribution_claims", "evidence_backed_contribution_claims"):
            value = structured.get(key)
            if isinstance(value, list):
                candidates.extend(item for item in value if isinstance(item, dict))
    real: list[dict[str, Any]] = []
    for index, item in enumerate(candidates, 1):
        blob = text_blob(item)
        if "pending_module_output" in blob:
            continue
        cid = item.get("contribution_id") or item.get("claim_id") or f"C{index}"
        claim = item.get("claim") or item.get("contribution_claim") or item.get("final_claim_text") or item.get("text") or str(item)
        real.append({"contribution_id": str(cid), "claim": str(claim), "source": item})
    return real


def classify_claim(claim: str) -> str:
    lower = claim.lower()
    if "mechanism" in lower or "algorithm" in lower or "evolutionary" in lower:
        return "algorithm_effectiveness_claim"
    if "trade" in lower or "pareto" in lower:
        return "tradeoff_insight_claim"
    if "constraint" in lower or "feasibility" in lower:
        return "constraint_handling_claim"
    if "runtime" in lower or "scalab" in lower:
        return "scalability_claim"
    return "model_validity_claim"


def demo_contributions() -> list[dict[str, str]]:
    return [
        {
            "contribution_id": "C1",
            "claim": "A joint layout-cabling optimization model for representing aerodynamic, electrical, economic, and feasibility trade-offs as a planned research contribution.",
            "validation_claim_type": "model_validity_claim",
        },
        {
            "contribution_id": "C2",
            "claim": "A problem-structure-aware evolutionary mechanism for joint layout-cabling search, requiring ablation-based validation before any performance claim.",
            "validation_claim_type": "algorithm_effectiveness_claim",
        },
        {
            "contribution_id": "C3",
            "claim": "An analysis plan for aerodynamic-electrical-economic Pareto trade-offs, requiring metrics and case studies before drawing conclusions.",
            "validation_claim_type": "tradeoff_insight_claim",
        },
    ]


def build_sample_plan(project_id: str, contributions: list[dict[str, Any]] | None = None, is_demo: bool = True) -> dict[str, Any]:
    contribs = contributions or demo_contributions()
    normalized: list[dict[str, str]] = []
    for index, item in enumerate(contribs, 1):
        cid = str(item.get("contribution_id") or f"C{index}")
        claim = str(item.get("claim") or item.get("contribution_claim") or f"Contribution {index} requires validation planning.")
        claim_type = str(item.get("validation_claim_type") or classify_claim(claim))
        normalized.append({"contribution_id": cid, "claim": claim, "validation_claim_type": claim_type})

    targets: list[dict[str, Any]] = []
    designs: list[dict[str, Any]] = []
    for index, contribution in enumerate(normalized, 1):
        cid = contribution["contribution_id"]
        vt = f"VT{index:03d}"
        ex = f"EX{index:03d}"
        claim_type = contribution["validation_claim_type"]
        required_types = ["baseline_comparison"]
        if cid == "C2" or claim_type in {"algorithm_effectiveness_claim", "mechanism_necessity_claim"}:
            required_types.append("ablation_study")
        if cid in {"C1", "C3"} or claim_type in {"tradeoff_insight_claim", "pareto_quality_claim"}:
            required_types.append("pareto_tradeoff_analysis")
        if cid == "C1" or "constraint" in contribution["claim"].lower() or "feasibility" in contribution["claim"].lower():
            required_types.append("feasibility_analysis")
        targets.append(
            {
                "validation_target_id": vt,
                "linked_contribution_id": cid,
                "contribution_claim": contribution["claim"],
                "linked_claim_id": f"CL{index:03d}",
                "linked_problem_id": "P001",
                "linked_theory_element_id": "TE001",
                "validation_claim_type": claim_type,
                "validation_question": f"What experiment plan would make contribution {cid} credible to a reviewer?",
                "hypothesis": f"If {cid} is valid, pre-registered comparisons should support the planned claim under equal computational budgets.",
                "required_evidence": [
                    "baseline comparison",
                    "claim-aligned metrics",
                    "statistical analysis plan",
                    "artifact traceability",
                ],
                "success_condition": "The contribution is supportable only if planned comparisons satisfy the evidence threshold without unsupported result language.",
                "failure_condition": "The contribution remains unsupported if the plan lacks aligned baselines, metrics, statistical analysis, or artifacts.",
                "evidence_threshold": "Evidence must include planned baseline, metric, ablation where applicable, statistical, and reproducibility links before empirical claims are written.",
                "required_experiment_types": sorted(set(required_types)),
                "validation_status": "validation_planned",
                "experiment_support_status": "directly_tested_by_plan",
                "reviewer_risk": "Reviewer may reject the contribution if validation evidence is weak, cherry-picked, or not reproducible.",
                "assumptions": ["This is a validation plan, not an experiment result."],
                "limitations": ["Real experiments, numerical results, and significance conclusions are not generated by v0.3.0."],
            }
        )
        experiment_type = "ablation_study" if "ablation_study" in required_types else "pareto_tradeoff_analysis"
        designs.append(
            {
                "experiment_id": ex,
                "experiment_name": f"Validation design for {cid}",
                "linked_validation_target_ids": [vt],
                "linked_contribution_ids": [cid],
                "experiment_type": experiment_type,
                "research_question": f"Which planned evidence would support {cid} under fair comparison conditions?",
                "hypothesis": f"If {cid} is credible, the planned evaluation should satisfy the evidence threshold across aligned metrics.",
                "independent_variables": ["algorithm variant", "baseline family", "case-study scale"],
                "dependent_variables": ["objective values", "Pareto quality indicators", "feasibility indicators", "runtime"],
                "controlled_variables": ["evaluation budget", "termination rule", "parameter reporting", "input instances"],
                "experimental_factors": ["layout-cabling coupling", "constraint handling", "wind and cost assumptions"],
                "comparison_groups": ["proposed method plan", "sequential baseline", "standard MOEA baseline", "ablated variant where applicable"],
                "required_baselines": ["B001", "B004"] + (["B006"] if cid == "C2" else []),
                "required_metrics": ["M001", "M002", "M003", "M004"],
                "required_ablations": ["A001"] if cid == "C2" else [],
                "required_case_studies": ["CS001", "CS002"],
                "statistical_requirements": ["ST001"],
                "computational_budget_policy": "Use equal function-evaluation or wall-clock reporting policies and disclose any unavoidable difference.",
                "fairness_requirements": "Use the same case instances, termination criteria, parameter reporting rules, and feasibility handling across methods.",
                "expected_result_pattern": "Conditional plan only: the claim would be supported only if aligned metrics meet the predeclared evidence threshold across fair comparisons.",
                "failure_pattern": "The claim should be revised if planned comparisons do not support the threshold or reveal unresolved feasibility, runtime, or baseline risks.",
                "reviewer_risk": "Comparison may be challenged if baselines, metrics, or budgets are misaligned.",
                "limitations": ["This design does not report empirical outcomes."],
            }
        )

    baselines = [
        baseline("B001", "Cabling-after-layout sequential baseline", "sequential_optimization", "EX001", ["VT001", "VT002"], ["C1", "C2", "C3"], "Tests whether joint optimization is necessary beyond a decoupled workflow."),
        baseline("B002", "Layout-only optimization baseline", "layout_only_optimization", "EX001", ["VT001"], ["C1"], "Separates aerodynamic layout benefit from cabling decisions."),
        baseline("B003", "Cabling-only fixed-layout baseline", "cabling_only_optimization", "EX001", ["VT001"], ["C1"], "Separates network routing decisions from layout changes."),
        baseline("B004", "Standard multi-objective evolutionary baseline", "multi_objective_evolutionary_algorithm", "EX001", ["VT001", "VT002", "VT003"], ["C1", "C2", "C3"], "Provides a non-problem-specific multi-objective comparison reference."),
        baseline("B005", "Greedy engineering sanity baseline", "random_or_greedy_baseline", "EX001", ["VT001"], ["C1"], "Detects whether planned methods are compared against a simple reproducible sanity check."),
        baseline("B006", "No-structure-aware ablated variant", "ablated_variant", "EX002", ["VT002"], ["C2"], "Tests whether the claimed structure-aware mechanism is necessary."),
    ]
    metrics = [
        metric("M001", "Hypervolume plan", "pareto_quality_metric", "EX001", ["VT001", "VT003"], ["C1", "C3"], "Pareto set quality under a disclosed reference strategy."),
        metric("M002", "Feasibility rate", "feasibility_metric", "EX001", ["VT001"], ["C1"], "Share of planned runs producing feasible layout-cabling solutions."),
        metric("M003", "Total constraint violation", "constraint_violation_metric", "EX001", ["VT001"], ["C1"], "Magnitude of infeasibility by constraint family."),
        metric("M004", "Runtime and evaluation budget", "runtime_metric", "EX001", ["VT001", "VT002"], ["C1", "C2"], "Computational cost needed to interpret fairness and scalability."),
        metric("M005", "AEP or energy output", "energy_metric", "EX003", ["VT001", "VT002", "VT003"], ["C1", "C2", "C3"], "Energy relevance of aerodynamic trade-offs."),
        metric("M006", "Wake loss", "wake_loss_metric", "EX003", ["VT001", "VT002", "VT003"], ["C1", "C2", "C3"], "Aerodynamic loss component for engineering interpretation."),
        metric("M007", "Cable investment cost", "cable_cost_metric", "EX003", ["VT001", "VT002", "VT003"], ["C1", "C2", "C3"], "Electrical-economic cost component for trade-off interpretation."),
        metric("M008", "LCOE or total cost proxy", "levelized_cost_metric", "EX003", ["VT001", "VT002", "VT003"], ["C1", "C2", "C3"], "Economic relevance when assumptions are disclosed."),
        metric("M009", "Spread or spacing indicator", "diversity_metric", "EX003", ["VT003"], ["C3"], "Diversity of planned Pareto approximations."),
    ]
    ablations = [
        {
            "ablation_id": "A001",
            "ablation_name": "Remove problem-structure-aware co-evolution",
            "linked_mechanism_id": "MECH001",
            "linked_contribution_id": "C2",
            "linked_experiment_id": "EX002",
            "component_removed_or_modified": "Replace the structure-aware co-evolution mechanism with a single-population variant.",
            "controlled_conditions": "Keep encoding, evaluation budget, case studies, and parameter reporting fixed except for the mechanism under test.",
            "comparison_variant": "non-coevolutionary variant",
            "expected_result_pattern": "Conditional plan only: C2 would be supported only if this variant clarifies the mechanism's role under the declared metrics.",
            "failure_pattern": "If the ablation cannot isolate the mechanism, C2 should be narrowed or redesigned.",
            "required_metrics": ["M001", "M002", "M003", "M004"],
            "required_baselines": ["B006"],
            "interpretation_rule": "Interpret only the planned comparison structure until real empirical data exist.",
            "reviewer_risk": "Reviewer may question C2 if the ablation changes more than the claimed mechanism.",
            "limitations": ["No empirical effect size is claimed."],
        }
    ]
    case_studies = [
        {
            "case_study_id": "CS001",
            "case_study_name": "Synthetic joint layout-cabling planning instance",
            "case_study_type": "synthetic_instance",
            "linked_experiment_ids": ["EX001", "EX002", "EX003"],
            "linked_validation_target_ids": ["VT001", "VT002", "VT003"],
            "site_or_instance_description": "Synthetic wind-farm instance for contract validation; not real field evidence.",
            "turbine_count_range": "small to medium planning instances; exact counts require experiment protocol",
            "layout_domain": "bounded offshore-style layout region placeholder",
            "wind_resource_assumptions": "wind rose and wake assumptions must be declared before execution",
            "wake_model_assumptions": "wake model choice must be reported and sensitivity-tested if claimed",
            "cable_cost_assumptions": "cable unit cost and capacity assumptions must be declared",
            "electrical_model_assumptions": "electrical loss and topology rules must be specified",
            "constraints_included": ["spacing", "boundary", "radial topology", "cable capacity"],
            "data_source": "synthetic example fixture",
            "is_synthetic": True,
            "realism_level": "contract fixture only",
            "scalability_role": "baseline smoke scenario",
            "why_needed": "Provides a reproducible placeholder for plan validation without real experiment claims.",
            "limitations": ["Synthetic example cannot support real engineering conclusions."],
            "reproducibility_requirements": ["publish instance generator", "record seeds", "report assumptions"],
        },
        {
            "case_study_id": "CS002",
            "case_study_name": "Scalability planning instance family",
            "case_study_type": "scalability_instance",
            "linked_experiment_ids": ["EX001", "EX002", "EX003"],
            "linked_validation_target_ids": ["VT001", "VT002", "VT003"],
            "site_or_instance_description": "Synthetic scale-varied family for planning scalability analysis.",
            "turbine_count_range": "multiple sizes to be fixed before execution",
            "layout_domain": "same domain family with size variation",
            "wind_resource_assumptions": "held constant or varied by declared sensitivity plan",
            "wake_model_assumptions": "same wake model across sizes unless sensitivity is planned",
            "cable_cost_assumptions": "consistent cost model across sizes",
            "electrical_model_assumptions": "consistent topology and capacity rules",
            "constraints_included": ["spacing", "boundary", "radial topology", "cable capacity"],
            "data_source": "synthetic example fixture",
            "is_synthetic": True,
            "realism_level": "planning only",
            "scalability_role": "scalability and stress-test planning",
            "why_needed": "Scalability claims require planned instance-size variation.",
            "limitations": ["No runtime or quality result is reported."],
            "reproducibility_requirements": ["document generator", "record seeds", "publish instance parameters"],
        },
    ]
    statistical = [
        {
            "statistical_test_id": "ST001",
            "linked_experiment_id": "EX001",
            "linked_metric_ids": ["M001", "M002", "M003", "M004", "M005", "M006", "M007", "M008", "M009"],
            "linked_baseline_ids": ["B001", "B002", "B003", "B004", "B005", "B006"],
            "test_name": "Wilcoxon or Friedman planning rule",
            "test_type": "wilcoxon_signed_rank",
            "why_needed": "Stochastic optimization comparisons require independent runs and a predeclared test rule.",
            "assumptions": ["Use paired nonparametric tests when paired stochastic runs are appropriate."],
            "independent_runs": 30,
            "random_seed_policy": "Declare and publish the seed list before execution.",
            "significance_level": "predeclare alpha before execution; do not claim significance in the plan",
            "multiple_comparison_policy": "Use correction or Friedman plus post-hoc tests when comparing many algorithms.",
            "effect_size_policy": "Report effect size or confidence interval when empirical data exist.",
            "confidence_interval_policy": "Use bootstrap confidence intervals where assumptions warrant.",
            "reporting_format": "Report per-instance summary, test statistic, adjusted decision, and limitations after real runs.",
            "interpretation_rule": "The plan defines how results would be interpreted; it does not report results.",
            "limitations": ["No p-value or significance conclusion exists before experiments are run."],
        }
    ]
    reproducibility = reproducibility_plan(project_id)
    report = experiment_report(project_id, targets, designs, baselines, metrics, ablations, case_studies, statistical, reproducibility, is_demo)
    return {
        "validation_targets": {
            "validation_targets": targets,
            "validation_target_summary": [{"validation_target_id": t["validation_target_id"], "linked_contribution_id": t["linked_contribution_id"], "validation_status": t["validation_status"]} for t in targets],
            "assumptions": ["Validation targets describe plans, not results."],
            "limitations": ["Requires real experiment execution before empirical claims."],
            "is_demo_plan": is_demo,
            "requires_real_contribution_chain": is_demo,
        },
        "experiment_design": {"experiment_designs": designs, "experiment_design_summary": [{"experiment_id": d["experiment_id"], "linked_contribution_ids": d["linked_contribution_ids"]} for d in designs], "assumptions": ["Experiment designs are planned only."], "limitations": ["No empirical outcomes are generated."], "is_demo_plan": is_demo, "requires_real_contribution_chain": is_demo},
        "baseline_plan": {"baselines": baselines, "baseline_adequacy_audit": {"missing_standard_baselines": [], "missing_problem_specific_baselines": [], "missing_sequential_baseline": [], "missing_joint_baseline": [], "missing_ablated_variants": [], "weak_baseline_risks": [], "unfair_comparison_risks": [], "recommended_repairs": []}, "assumptions": ["Baseline adequacy requires real literature review before execution."], "limitations": ["Baseline implementation availability is not verified."], "is_demo_plan": is_demo, "requires_real_contribution_chain": is_demo},
        "metric_plan": {"metrics": metrics, "metric_adequacy_audit": {"missing_pareto_metrics": [], "missing_feasibility_metrics": [], "missing_runtime_metrics": [], "missing_engineering_metrics": [], "metric_claim_mismatch_risks": [], "recommended_repairs": []}, "assumptions": ["Metric definitions must be finalized before execution."], "limitations": ["No numeric metric values are reported."], "is_demo_plan": is_demo, "requires_real_contribution_chain": is_demo},
        "ablation_plan": {"ablations": ablations, "ablation_adequacy_audit": {"missing_mechanism_ablations": [], "weak_ablation_risks": [], "confounded_ablation_risks": [], "recommended_repairs": []}, "assumptions": ["C2 is treated as the algorithmic contribution in the demo fixture."], "limitations": ["No ablation result is reported."], "is_demo_plan": is_demo, "requires_real_contribution_chain": is_demo},
        "case_study_plan": {"case_studies": case_studies, "case_study_adequacy_audit": {"missing_case_studies": [], "synthetic_only_risks": ["Demo cases are synthetic and cannot support real field evidence."], "recommended_repairs": ["Replace or supplement synthetic fixtures with justified real, benchmark, or user-provided instances before making empirical claims."]}, "assumptions": ["Synthetic examples are marked explicitly."], "limitations": ["Synthetic cases are corpus fixtures, not field evidence."], "is_demo_plan": is_demo, "requires_real_contribution_chain": is_demo},
        "statistical_analysis_plan": {"statistical_analyses": statistical, "statistical_adequacy_audit": {"missing_statistical_tests": [], "missing_independent_runs": [], "missing_seed_policy": [], "recommended_repairs": []}, "assumptions": ["Statistical choices must be checked against real data design."], "limitations": ["No significance claim is made."], "is_demo_plan": is_demo, "requires_real_contribution_chain": is_demo},
        "reproducibility_plan": reproducibility,
        "experiment_grounding_report": report,
    }


def baseline(bid: str, name: str, btype: str, ex: str, vts: list[str], cids: list[str], why: str) -> dict[str, Any]:
    return {
        "baseline_id": bid,
        "baseline_name": name,
        "baseline_type": btype,
        "linked_experiment_id": ex,
        "linked_validation_target_ids": vts,
        "linked_contribution_ids": cids,
        "literature_evidence_ids": [],
        "why_needed": why,
        "what_it_tests": why,
        "fairness_requirements": "Use equal termination criteria, disclosed parameters, same instances, and same feasibility handling.",
        "implementation_requirements": "Implementation source, parameters, and deviations must be documented before execution.",
        "parameter_tuning_policy": "Use a declared tuning budget or literature-supported defaults.",
        "termination_criterion": "Use equal function-evaluation budget or report any alternative explicitly.",
        "computational_budget_policy": "Same evaluation budget and hardware reporting policy where applicable.",
        "expected_role": "Provides a planned comparison role; it is not a result.",
        "risk_if_missing": "Reviewer may see the contribution as cherry-picked or insufficiently compared.",
        "limitations": ["Literature support and implementation availability require verification."],
    }


def metric(mid: str, name: str, mtype: str, ex: str, vts: list[str], cids: list[str], measures: str) -> dict[str, Any]:
    return {
        "metric_id": mid,
        "metric_name": name,
        "metric_type": mtype,
        "linked_experiment_id": ex,
        "linked_validation_target_ids": vts,
        "linked_contribution_ids": cids,
        "what_it_measures": measures,
        "why_it_is_needed": "This metric is tied to the stated validation target and reviewer-risk question.",
        "formula_or_definition": "Define formally in the experiment protocol before execution.",
        "interpretation_rule": "Interpret only after real results exist and statistical plan is applied.",
        "success_pattern": "Conditional: support requires meeting the predeclared evidence threshold across fair comparisons.",
        "failure_pattern": "If the metric does not align with the claim or cannot be computed, revise the validation plan.",
        "limitations": ["Metric limitations and reference-front assumptions must be disclosed."],
        "required_data": ["planned raw results", "case instance metadata", "constraint logs"],
        "statistical_use": "Included in the predeclared statistical analysis where applicable.",
    }


def reproducibility_plan(project_id: str) -> dict[str, Any]:
    artifacts = [
        artifact("AR001", "source_code", "EX001", "C1", "Experiment execution code and model implementation."),
        artifact("AR002", "configuration_file", "EX001", "C1", "Configuration files for baseline and metric settings."),
        artifact("AR003", "input_instance", "EX001", "C1", "Input case-study instances and generator metadata."),
        artifact("AR004", "statistical_analysis_script", "EX001", "C2", "Script implementing the predeclared statistical analysis."),
        artifact("AR005", "figure_generation_script", "EX003", "C3", "Scripts for Pareto and trade-off visualizations after real runs."),
        artifact("AR006", "environment_file", "EX001", "C1", "Software and hardware environment description."),
    ]
    return {
        "artifact_requirements": artifacts,
        "code_requirements": ["publish or archive source code for proposed and baseline implementations"],
        "data_requirements": ["publish synthetic instance generators and any real/user-provided data permissions"],
        "parameter_requirements": ["record all algorithm parameters and baseline parameters"],
        "environment_requirements": ["record hardware, operating system, language/runtime, and library versions"],
        "random_seed_policy": "Predeclare and publish all random seeds for independent runs.",
        "computational_budget_policy": "Predeclare function-evaluation budget, termination criterion, and hardware reporting.",
        "result_reporting_schema": {"project_id": project_id, "required_columns": ["experiment_id", "method_id", "case_study_id", "seed", "metric_id", "metric_value", "feasibility_status", "runtime"]},
        "figure_table_plan": ["Pareto front plots", "baseline metric table", "constraint violation table", "runtime/scalability table"],
        "experiment_log_requirements": ["command line", "commit or version", "seed", "start/end time", "hardware", "status"],
        "reproducibility_risks": ["baseline implementation unavailable", "synthetic-only case studies require clear limitation labeling"],
        "artifact_traceability_table": artifacts,
        "assumptions": ["Artifacts are required by the plan but are not claimed to already exist."],
        "limitations": ["Reproducibility remains planned until real artifacts are created and checked."],
        "is_demo_plan": True,
        "requires_real_contribution_chain": True,
    }


def artifact(aid: str, atype: str, ex: str, cid: str, desc: str) -> dict[str, Any]:
    return {
        "artifact_id": aid,
        "artifact_type": atype,
        "linked_experiment_id": ex,
        "linked_contribution_id": cid,
        "description": desc,
        "required_for_claim": True,
        "reproducibility_role": "Required to reproduce or audit the planned evidence chain.",
        "storage_location_placeholder": f"artifacts/{aid}",
        "versioning_requirement": "Record commit, checksum, or version tag before execution.",
        "risk_if_missing": "Claim cannot be audited or reproduced without this artifact.",
    }


def experiment_report(
    project_id: str,
    targets: list[dict[str, Any]],
    designs: list[dict[str, Any]],
    baselines: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
    ablations: list[dict[str, Any]],
    case_studies: list[dict[str, Any]],
    statistical: list[dict[str, Any]],
    reproducibility: dict[str, Any],
    is_demo: bool,
) -> dict[str, Any]:
    trace_rows = []
    artifacts = reproducibility["artifact_requirements"]
    for target in targets:
        cid = target["linked_contribution_id"]
        linked_designs = [d for d in designs if cid in d["linked_contribution_ids"]]
        exp_ids = [d["experiment_id"] for d in linked_designs]
        trace_rows.append(
            {
                "contribution_id": cid,
                "contribution_claim": target.get("contribution_claim", f"Planned validation target for {cid}"),
                "validation_target_id": target["validation_target_id"],
                "experiment_id": exp_ids[0] if exp_ids else "",
                "baseline_ids": [b["baseline_id"] for b in baselines if cid in b["linked_contribution_ids"]],
                "metric_ids": [m["metric_id"] for m in metrics if cid in m["linked_contribution_ids"]],
                "ablation_ids": [a["ablation_id"] for a in ablations if a["linked_contribution_id"] == cid],
                "statistical_test_ids": [s["statistical_test_id"] for s in statistical],
                "artifact_ids": [a["artifact_id"] for a in artifacts if a["linked_contribution_id"] == cid],
                "success_condition": target["success_condition"],
                "failure_condition": target["failure_condition"],
                "reviewer_risk": target["reviewer_risk"],
                "validation_status": target["validation_status"],
            }
        )
    context = {
        "experiment_grounding_mode": "experiment_grounded",
        "validation_target_summary": [{"validation_target_id": t["validation_target_id"], "linked_contribution_id": t["linked_contribution_id"]} for t in targets],
        "experiment_design_summary": [{"experiment_id": d["experiment_id"], "linked_validation_target_ids": d["linked_validation_target_ids"]} for d in designs],
        "baseline_summary": [{"baseline_id": b["baseline_id"], "baseline_type": b["baseline_type"]} for b in baselines],
        "metric_summary": [{"metric_id": m["metric_id"], "metric_type": m["metric_type"]} for m in metrics],
        "ablation_summary": [{"ablation_id": a["ablation_id"], "linked_contribution_id": a["linked_contribution_id"]} for a in ablations],
        "statistical_analysis_summary": [{"statistical_test_id": s["statistical_test_id"], "test_type": s["test_type"]} for s in statistical],
        "reproducibility_summary": {"artifact_count": len(artifacts), "random_seed_policy": reproducibility["random_seed_policy"]},
        "validation_adequacy_summary": {"validation_chain_status": "pass_with_minor_risks" if is_demo else "pass"},
        "experiment_risks": (
            [
                "demo plan requires real contribution chain",
                "baseline implementation unavailable must be verified before execution",
                "synthetic-only case-study evidence cannot support real field conclusions",
            ]
            if is_demo
            else []
        ),
        "claims_not_yet_supported_by_validation_plan": [],
        "trace_context": {"contribution_ids": [t["linked_contribution_id"] for t in targets], "validation_target_ids": [t["validation_target_id"] for t in targets]},
    }
    return {
        "project_id": project_id,
        "validation_target_summary": context["validation_target_summary"],
        "experiment_design_summary": context["experiment_design_summary"],
        "baseline_summary": context["baseline_summary"],
        "metric_summary": context["metric_summary"],
        "ablation_summary": context["ablation_summary"],
        "case_study_summary": [{"case_study_id": c["case_study_id"], "is_synthetic": c["is_synthetic"]} for c in case_studies],
        "statistical_analysis_summary": context["statistical_analysis_summary"],
        "reproducibility_summary": context["reproducibility_summary"],
        "validation_adequacy_summary": context["validation_adequacy_summary"],
        "experiment_context": context,
        "claims_not_yet_supported_by_validation_plan": [],
        "reviewer_validation_risks": context["experiment_risks"],
        "contribution_to_experiment_traceability_table": trace_rows,
        "is_demo_plan": is_demo,
        "requires_real_contribution_chain": is_demo,
    }


def write_markdown(path: Path, title: str, data: Any) -> None:
    path.write_text(f"# {title}\n\n```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```\n")


def plan_file_map() -> dict[str, str]:
    return {
        "validation_targets": "validation_targets.json",
        "experiment_design": "experiment_design.json",
        "baseline_plan": "baseline_plan.json",
        "metric_plan": "metric_plan.json",
        "ablation_plan": "ablation_plan.json",
        "case_study_plan": "case_study_plan.json",
        "statistical_analysis_plan": "statistical_analysis_plan.json",
        "reproducibility_plan": "reproducibility_plan.json",
        "experiment_grounding_report": "experiment_grounding_report.json",
    }


def write_plan(exp_dir: Path, plan: dict[str, Any], overwrite: bool) -> None:
    exp_dir.mkdir(parents=True, exist_ok=True)
    for key, filename in plan_file_map().items():
        path = exp_dir / filename
        if path.exists() and not overwrite:
            raise SystemExit(f"FAIL output exists; use --overwrite: {path}")
        write_json(path, plan[key])
        write_markdown(path.with_suffix(".md"), filename.removesuffix(".json").replace("_", " ").title(), plan[key])


def load_plan(exp_dir: Path, failures: list[str] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, filename in plan_file_map().items():
        path = exp_dir / filename
        if not path.exists():
            if failures is not None:
                failures.append(f"FAIL missing experiment plan file: {path.name}")
            continue
        try:
            result[key] = read_json(path)
        except json.JSONDecodeError as exc:
            if failures is not None:
                failures.append(f"FAIL invalid JSON: {path.name}: {exc}")
    return result


def collect_plan_objects(plan: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        "targets": plan.get("validation_targets", {}).get("validation_targets", []),
        "designs": plan.get("experiment_design", {}).get("experiment_designs", []),
        "baselines": plan.get("baseline_plan", {}).get("baselines", []),
        "metrics": plan.get("metric_plan", {}).get("metrics", []),
        "ablations": plan.get("ablation_plan", {}).get("ablations", []),
        "case_studies": plan.get("case_study_plan", {}).get("case_studies", []),
        "statistical": plan.get("statistical_analysis_plan", {}).get("statistical_analyses", []),
        "artifacts": plan.get("reproducibility_plan", {}).get("artifact_requirements", []),
    }


def contribution_ids(objects: dict[str, list[dict[str, Any]]]) -> set[str]:
    ids: set[str] = set()
    for target in objects["targets"]:
        if target.get("linked_contribution_id"):
            ids.add(str(target["linked_contribution_id"]))
    return ids


def linked_by_contribution(items: list[dict[str, Any]], cid: str) -> list[dict[str, Any]]:
    return [item for item in items if cid in id_list(item.get("linked_contribution_ids")) or item.get("linked_contribution_id") == cid]


def is_algorithmic_target(target: dict[str, Any]) -> bool:
    return target.get("validation_claim_type") in {"algorithm_effectiveness_claim", "mechanism_necessity_claim", "constraint_handling_claim", "benchmark_claim"} or contains_any(target, ["algorithm", "mechanism", "evolutionary", "co-evolution"])


def is_multiobjective_target(target: dict[str, Any]) -> bool:
    return target.get("validation_claim_type") in {"tradeoff_insight_claim", "pareto_quality_claim"} or contains_any(target, ["multi-objective", "pareto", "trade-off", "tradeoff"])


def is_constrained_target(target: dict[str, Any]) -> bool:
    return target.get("validation_claim_type") in {"feasibility_claim", "constraint_handling_claim"} or contains_any(target, ["constraint", "feasibility", "violation"])


def is_joint_target(target: dict[str, Any]) -> bool:
    return contains_any(target, ["joint layout-cabling", "layout-cabling", "layout and cable", "layout-cable"])


def has_pareto_metric(metrics: list[dict[str, Any]]) -> bool:
    return any(metric.get("metric_type") == "pareto_quality_metric" or contains_any(metric, ["hypervolume", "igd", "spread", "spacing", "pareto"]) for metric in metrics)


def has_feasibility_metric(metrics: list[dict[str, Any]]) -> bool:
    return any(metric.get("metric_type") in {"feasibility_metric", "constraint_violation_metric"} or contains_any(metric, ["feasibility", "violation"]) for metric in metrics)


def has_engineering_metrics(metrics: list[dict[str, Any]]) -> bool:
    types = {metric.get("metric_type") for metric in metrics}
    return bool(types & {"energy_metric", "wake_loss_metric", "cable_cost_metric", "electrical_loss_metric", "levelized_cost_metric", "cost_metric"})


def has_sequential_or_decoupled_baseline(baselines: list[dict[str, Any]]) -> bool:
    types = {baseline.get("baseline_type") for baseline in baselines}
    return bool(types & {"sequential_optimization", "layout_only_optimization", "cabling_only_optimization"})


def evaluate_plan(plan: dict[str, Any], strict: bool, require_complete_validation_chain: bool = False, workspace: Path | None = None) -> tuple[list[str], list[str], list[str]]:
    passes: list[str] = []
    warnings: list[str] = []
    failures: list[str] = []
    objects = collect_plan_objects(plan)

    unsafe = find_fabricated_result_wording(plan)
    if unsafe:
        target = failures if strict else warnings
        target.extend(f"FAIL fabricated result wording or unsupported empirical claim: {item}" for item in unsafe)
    else:
        passes.append("PASS no fabricated result wording detected")

    for collection, field in [
        ("targets", "validation_target_id"),
        ("designs", "experiment_id"),
        ("baselines", "baseline_id"),
        ("metrics", "metric_id"),
        ("ablations", "ablation_id"),
        ("case_studies", "case_study_id"),
        ("statistical", "statistical_test_id"),
        ("artifacts", "artifact_id"),
    ]:
        ids = [item.get(field) for item in objects[collection] if item.get(field)]
        duplicates = sorted({value for value in ids if ids.count(value) > 1})
        if duplicates:
            failures.append(f"FAIL duplicate {field}: {', '.join(duplicates)}")
        else:
            passes.append(f"PASS unique {field}")

    experiment_ids = {item.get("experiment_id") for item in objects["designs"]}
    for collection, field in [("baselines", "baseline_id"), ("metrics", "metric_id"), ("ablations", "ablation_id"), ("statistical", "statistical_test_id"), ("artifacts", "artifact_id")]:
        for item in objects[collection]:
            ex = item.get("linked_experiment_id")
            if ex and ex not in experiment_ids:
                failures.append(f"FAIL {field} links unknown experiment_id: {item.get(field)} -> {ex}")
    if not any("links unknown" in failure for failure in failures):
        passes.append("PASS experiment reference integrity")

    for baseline_item in objects["baselines"]:
        if not baseline_item.get("why_needed"):
            failures.append(f"FAIL baseline missing why_needed: {baseline_item.get('baseline_id')}")
        if not baseline_item.get("fairness_requirements"):
            failures.append(f"FAIL baseline missing fairness_requirements: {baseline_item.get('baseline_id')}")

    for metric_item in objects["metrics"]:
        if not metric_item.get("linked_contribution_ids") and not metric_item.get("linked_validation_target_ids"):
            failures.append(f"FAIL metric lacks contribution or validation target link: {metric_item.get('metric_id')}")
        if not metric_item.get("interpretation_rule"):
            failures.append(f"FAIL metric missing interpretation_rule: {metric_item.get('metric_id')}")

    targets_by_cid = {target.get("linked_contribution_id"): target for target in objects["targets"] if target.get("linked_contribution_id")}
    report_trace = plan.get("experiment_grounding_report", {}).get("contribution_to_experiment_traceability_table", [])
    target_cids = set(targets_by_cid)
    for row in report_trace if isinstance(report_trace, list) else []:
        cid = row.get("contribution_id") if isinstance(row, dict) else None
        if cid and cid not in target_cids:
            failures.append(f"FAIL contribution without validation target: {cid}")

    for cid, target in targets_by_cid.items():
        designs = linked_by_contribution(objects["designs"], str(cid))
        baselines = linked_by_contribution(objects["baselines"], str(cid))
        metrics = linked_by_contribution(objects["metrics"], str(cid))
        ablations = linked_by_contribution(objects["ablations"], str(cid))
        artifacts = linked_by_contribution(objects["artifacts"], str(cid))
        if not designs:
            failures.append(f"FAIL validation target without experiment design for {cid}")
        if not baselines:
            failures.append(f"FAIL experiment design without baseline for {cid}")
        if not metrics:
            failures.append(f"FAIL experiment design without metric for {cid}")
        if baselines and all(b.get("baseline_type") == "random_or_greedy_baseline" for b in baselines):
            failures.append(f"FAIL weak baseline risk for {cid}: only random_or_greedy_baseline is planned")
        if is_algorithmic_target(target) and not ablations:
            failures.append(f"FAIL missing ablation for algorithmic contribution {cid}")
        if is_multiobjective_target(target) and not has_pareto_metric(metrics):
            failures.append(f"FAIL missing Pareto quality metric for {cid}")
        if is_multiobjective_target(target) and baselines and not any(b.get("baseline_type") == "multi_objective_evolutionary_algorithm" for b in baselines):
            failures.append(f"FAIL missing standard MOEA baseline for multi-objective contribution {cid}")
        if is_constrained_target(target) and not has_feasibility_metric(metrics):
            failures.append(f"FAIL missing feasibility metric for {cid}")
        if is_joint_target(target) and not has_sequential_or_decoupled_baseline(baselines):
            failures.append(f"FAIL missing sequential baseline for joint layout-cabling contribution {cid}")
        if is_joint_target(target) and not has_engineering_metrics(metrics):
            failures.append(f"FAIL missing aerodynamic/electrical/economic metric coverage for {cid}")
        if not artifacts:
            failures.append(f"FAIL missing artifact requirement for {cid}")
        if not target.get("success_condition") or str(target.get("success_condition")).strip().lower() in {"tbd", "to be determined"}:
            failures.append(f"FAIL success condition too vague for {cid}")
        if not target.get("failure_condition"):
            failures.append(f"FAIL failure condition missing for {cid}")

    statistical = objects["statistical"]
    if not statistical:
        failures.append("FAIL missing statistical test for stochastic comparison")
    for item in statistical:
        if item.get("test_type") != "not_applicable" and not item.get("independent_runs"):
            failures.append(f"FAIL missing independent runs for statistical test {item.get('statistical_test_id')}")
        if item.get("test_type") != "not_applicable" and not item.get("random_seed_policy"):
            failures.append(f"FAIL missing random seed policy for statistical test {item.get('statistical_test_id')}")
        if not item.get("why_needed"):
            failures.append(f"FAIL missing test rationale for statistical test {item.get('statistical_test_id')}")

    repro = plan.get("reproducibility_plan", {})
    for key, label in [
        ("random_seed_policy", "random seeds"),
        ("computational_budget_policy", "computational budget"),
        ("parameter_requirements", "parameter settings"),
        ("environment_requirements", "environment"),
        ("artifact_traceability_table", "artifact traceability"),
    ]:
        if not repro.get(key):
            failures.append(f"FAIL missing reproducibility requirement: {label}")

    report = plan.get("experiment_grounding_report", {})
    trace = report.get("contribution_to_experiment_traceability_table", [])
    if not trace:
        failures.append("FAIL missing experiment traceability table")
    else:
        passes.append("PASS contribution-to-experiment traceability table exists")

    if contains_any(plan, ["baseline implementation unavailable", "synthetic-only", "synthetic only"]):
        risks = text_blob(report.get("reviewer_validation_risks", [])) + text_blob(report.get("experiment_context", {}).get("experiment_risks", []))
        if "baseline implementation unavailable" not in risks and "synthetic" not in risks:
            failures.append("FAIL hidden validation risk not surfaced in experiment report")

    if require_complete_validation_chain:
        if any(section.get("is_demo_plan") or section.get("requires_real_contribution_chain") for section in plan.values() if isinstance(section, dict)):
            failures.append("FAIL demo plan requires real contribution chain")
        if workspace:
            final_path = workspace / "06_final_topic_package" / "output.json"
            if not final_path.exists():
                failures.append("FAIL incomplete final topic package: final_topic_package output is missing")
            else:
                final = read_json(final_path)
                structured = final.get("structured_output", {}) if isinstance(final, dict) else {}
                table = structured.get("contribution_to_experiment_traceability_table") or structured.get("Contribution-to-Experiment Traceability Table")
                if final.get("status") == "draft":
                    failures.append("FAIL incomplete final topic package: final_topic_package output is draft")
                if not table:
                    failures.append("FAIL missing contribution-to-experiment traceability table in final topic package")

    if failures:
        pass
    else:
        passes.append("PASS validation adequacy checks")
    return passes, warnings, failures


def report_lines(title: str, passes: list[str], warnings: list[str], failures: list[str], decision_key: str = "validation_decision") -> list[str]:
    decision = "fail_requires_revision" if failures else ("pass_with_warnings" if warnings else "pass")
    return [
        f"# {title}",
        "",
        f"- pass_count: {len(passes)}",
        f"- warning_count: {len(warnings)}",
        f"- fail_count: {len(failures)}",
        f"- {decision_key}: {decision}",
        "",
        "## PASS",
        *[f"- {line}" for line in passes],
        "",
        "## WARNING",
        *[f"- {line}" for line in warnings],
        "",
        "## FAIL",
        *[f"- {line}" for line in failures],
        "",
    ]
