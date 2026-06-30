#!/usr/bin/env python3
"""Shared helpers for v0.4 manuscript-grounded writing plans."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR_NAME = "manuscript_grounding"

CLAIM_STATUSES = [
    "planned",
    "evidence_supported",
    "citation_required",
    "experiment_result_required",
    "partially_supported",
    "unsupported",
    "unsafe_until_verified",
    "not_applicable",
]
SAFETY_LEVELS = [
    "safe",
    "needs_citation",
    "needs_experiment_result",
    "corpus_scoped_only",
    "overclaim_risk",
    "unsafe_until_verified",
]
SECTION_ROLES = [
    "background_motivation",
    "literature_positioning",
    "gap_establishment",
    "problem_statement",
    "theory_framing",
    "contribution_summary",
    "method_rationale",
    "algorithm_description",
    "model_formulation",
    "experimental_validation",
    "result_interpretation",
    "limitation_discussion",
    "reviewer_risk_defense",
    "conclusion_synthesis",
]
PARAGRAPH_ROLES = [
    "context_setting",
    "known_stream_summary",
    "contrast_between_streams",
    "gap_claim",
    "problem_formulation",
    "theoretical_positioning",
    "contribution_claim",
    "design_rationale",
    "validation_setup",
    "evidence_interpretation",
    "limitation_statement",
    "transition",
    "reviewer_preemption",
]
CITATION_TYPES = [
    "background_citation",
    "domain_importance_citation",
    "method_stream_citation",
    "limitation_support_citation",
    "gap_support_citation",
    "baseline_support_citation",
    "metric_support_citation",
    "theory_support_citation",
    "validation_protocol_citation",
    "counterevidence_citation",
]
RESULT_TYPES = [
    "baseline_comparison_result",
    "pareto_quality_result",
    "feasibility_result",
    "runtime_result",
    "ablation_result",
    "sensitivity_result",
    "statistical_test_result",
    "case_study_result",
    "reproducibility_artifact_result",
    "qualitative_interpretation_result",
]
OBJECTION_TYPES = [
    "novelty_question",
    "significance_question",
    "problem_importance_question",
    "method_necessity_question",
    "algorithm_wrapping_question",
    "baseline_sufficiency_question",
    "metric_sufficiency_question",
    "ablation_sufficiency_question",
    "statistical_validity_question",
    "reproducibility_question",
    "limitation_question",
    "generalization_question",
    "writing_clarity_question",
    "overclaim_question",
    "citation_gap_question",
    "counterevidence_question",
]

RESULT_WORDING = [
    re.compile(r"\boutperforms?\b", re.I),
    re.compile(r"\bimproves?\s+by\s+\d", re.I),
    re.compile(r"\bachieves?\s+\d", re.I),
    re.compile(r"\bp\s*[<=>]\s*0?\.\d+\b", re.I),
    re.compile(r"\bstatistically\s+significant\b", re.I),
    re.compile(r"\bsignificantly\s+(better|outperforms?|improves?)\b", re.I),
]
CITATION_WORDING = [
    re.compile(r"\b[A-Z][A-Za-z-]+\s+et\s+al\.\s*\((19|20)\d{2}\)"),
    re.compile(r"\bdoi\s*[:=]\s*10\.\d{4,9}/", re.I),
    re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+"),
]
FAKE_REVIEWER = re.compile(r"\breviewer\s*\d+\s+(said|asked|commented|stated)\b", re.I)
OVERCLAIM = re.compile(r"(?<!algorithm-)\b(first|novel|SOTA|state-of-the-art|unprecedented)\b", re.I)

SAFE_PATH_PARTS = {
    "unsafe_wording_to_avoid",
    "unsafe_result_wording_to_avoid",
    "safer_wording",
    "safer_wording_without_citation",
    "allowed_placeholder_wording",
    "what_not_to_claim",
    "fabricated_citation_risks",
    "fabricated_result_risks",
    "overclaim_risks",
    "limitations",
    "missing_citation_risk",
    "residual_risk",
    "revision_hooks",
    "repair_actions",
}


def resolve_workspace(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def manuscript_dir(workspace: Path, manuscript_dir_arg: Path | None = None) -> Path:
    if manuscript_dir_arg is None:
        return workspace / MANUSCRIPT_DIR_NAME
    return manuscript_dir_arg if manuscript_dir_arg.is_absolute() else workspace / manuscript_dir_arg


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def write_markdown(path: Path, title: str, data: Any) -> None:
    path.write_text(f"# {title}\n\n```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```\n")


def iter_strings(value: Any, path: tuple[Any, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from iter_strings(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_strings(child, (*path, index))
    elif isinstance(value, str):
        yield path, value


def safe_path(path: tuple[Any, ...]) -> bool:
    return any(str(part) in SAFE_PATH_PARTS for part in path)


def find_patterns(value: Any, patterns: list[re.Pattern[str]], label: str) -> list[str]:
    out: list[str] = []
    for path, text in iter_strings(value):
        if safe_path(path):
            continue
        if any(pattern.search(text) for pattern in patterns):
            out.append(f"{label}: {'.'.join(map(str, path))}: {text}")
    return out


def id_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def plan_file_map() -> dict[str, str]:
    return {
        "manuscript_blueprint": "manuscript_blueprint.json",
        "section_argument_map": "section_argument_map.json",
        "paragraph_claim_plan": "paragraph_claim_plan.json",
        "citation_requirement_map": "citation_requirement_map.json",
        "result_placeholder_map": "result_placeholder_map.json",
        "method_section_alignment": "method_section_alignment.json",
        "experiment_section_alignment": "experiment_section_alignment.json",
        "discussion_limitations_plan": "discussion_limitations_plan.json",
        "reviewer_objection_map": "reviewer_objection_map.json",
        "reviewer_response_strategy": "reviewer_response_strategy.json",
        "manuscript_grounding_report": "manuscript_grounding_report.json",
    }


def load_plan(ms_dir: Path, failures: list[str] | None = None) -> dict[str, Any]:
    plan: dict[str, Any] = {}
    for key, filename in plan_file_map().items():
        path = ms_dir / filename
        if not path.exists():
            if failures is not None:
                failures.append(f"FAIL missing manuscript plan file: {filename}")
            continue
        try:
            plan[key] = read_json(path)
        except json.JSONDecodeError as exc:
            if failures is not None:
                failures.append(f"FAIL invalid JSON: {filename}: {exc}")
    return plan


def write_plan(ms_dir: Path, plan: dict[str, Any], overwrite: bool) -> None:
    ms_dir.mkdir(parents=True, exist_ok=True)
    for key, filename in plan_file_map().items():
        path = ms_dir / filename
        if path.exists() and not overwrite:
            raise SystemExit(f"FAIL output exists; use --overwrite: {path}")
        write_json(path, plan[key])
        write_markdown(path.with_suffix(".md"), filename.removesuffix(".json").replace("_", " ").title(), plan[key])


def final_topic_is_real(workspace: Path) -> bool:
    path = workspace / "06_final_topic_package" / "output.json"
    if not path.exists():
        return False
    data = read_json(path)
    return isinstance(data, dict) and data.get("status") != "draft" and "PENDING_MODULE_OUTPUT" not in json.dumps(data)


def build_sample_plan(project_id: str, is_demo: bool = True) -> dict[str, Any]:
    section_plan = [
        section("S001", "Introduction", "background_motivation", ["C1", "C2", "C3"], ["P001"], [], ["EX001", "EX002", "EX003"], ["MC001", "MC002", "MC003"], ["CR001", "CR002"], ["RP001"], ["RO001"], "needs_revision"),
        section("S002", "Related Work", "literature_positioning", ["C1", "C2", "C3"], ["P001"], [], [], ["MC004"], ["CR003", "CR004"], [], ["RO002"], "needs_revision"),
        section("S003", "Problem Formulation", "problem_statement", ["C1"], ["P001"], [], [], ["MC005"], ["CR005"], [], ["RO003"], "needs_revision"),
        section("S004", "Method", "method_rationale", ["C1", "C2"], ["P001"], [], ["EX002"], ["MC006"], [], ["RP002"], ["RO004"], "needs_revision"),
        section("S005", "Experiments", "experimental_validation", ["C1", "C2", "C3"], ["P001"], [], ["EX001", "EX002", "EX003"], ["MC007"], ["CR006"], ["RP001", "RP002", "RP003"], ["RO005"], "needs_revision"),
        section("S006", "Results and Analysis", "result_interpretation", ["C1", "C2", "C3"], ["P001"], [], ["EX001", "EX002", "EX003"], ["MC008"], [], ["RP001", "RP002", "RP003"], ["RO006"], "needs_revision"),
        section("S007", "Discussion", "limitation_discussion", ["C1", "C2", "C3"], ["P001"], [], ["EX001"], ["MC009"], ["CR007"], ["RP004"], ["RO007"], "needs_revision"),
        section("S008", "Conclusion", "conclusion_synthesis", ["C1", "C2", "C3"], ["P001"], [], [], ["MC010"], [], [], ["RO008"], "needs_revision"),
    ]
    claims = [
        claim("MC001", "The manuscript should motivate wind farm layout-cabling coupling as a planned research problem, within provided evidence limits.", "gap_claim", "S001", "P001", "C1", [], [], [], "citation_required", "needs_citation", ["CR001"], [], []),
        claim("MC002", "The manuscript should present the joint model contribution as requiring formulation and validation support.", "contribution_claim", "S001", "P002", "C1", [], ["EX001"], ["RP001"], "experiment_result_required", "needs_experiment_result", ["CR002"], ["RP001"], []),
        claim("MC003", "The manuscript should preview validation plans without reporting outcomes.", "validation_claim", "S001", "P003", "C2", [], ["EX002"], ["RP002"], "experiment_result_required", "needs_experiment_result", [], ["RP002"], []),
        claim("MC004", "Related Work should be organized by layout-only, cabling-only, sequential, joint, evolutionary, constrained, and baseline streams.", "literature_positioning_claim", "S002", "P004", "C1", [], [], [], "citation_required", "needs_citation", ["CR003", "CR004"], [], []),
        claim("MC005", "Problem Formulation should define the coupled decision structure without claiming empirical benefit.", "problem_claim", "S003", "P005", "C1", [], [], [], "planned", "corpus_scoped_only", ["CR005"], [], []),
        claim("MC006", "Method should map each mechanism to a problem property and ablation requirement.", "method_claim", "S004", "P006", "C2", [], ["EX002"], ["RP002"], "experiment_result_required", "needs_experiment_result", [], ["RP002"], []),
        claim("MC007", "Experiments should compare validation targets, baselines, metrics, ablations, statistics, and artifacts before making performance claims.", "experiment_plan_claim", "S005", "P007", "C2", [], ["EX001", "EX002"], ["RP001", "RP002"], "experiment_result_required", "needs_experiment_result", ["CR006"], ["RP001", "RP002"], []),
        claim("MC008", "Results and Analysis should use placeholders until real results are provided.", "result_placeholder_claim", "S006", "P008", "C3", [], ["EX003"], ["RP003"], "experiment_result_required", "needs_experiment_result", [], ["RP003"], []),
        claim("MC009", "Discussion must state corpus-scope, synthetic-demo, missing-real-result, and generalization limits.", "limitation_claim", "S007", "P009", "C3", [], ["EX001"], ["RP004"], "planned", "safe", ["CR007"], ["RP004"], ["synthetic demo limitation"]),
        claim("MC010", "Conclusion should summarize only supported or planned claims and introduce no new claim.", "conclusion_claim", "S008", "P010", "C3", [], [], [], "planned", "safe", [], [], []),
    ]
    paragraphs = [
        paragraph("P001", "S001", "context_setting", "MC001", [], "needs_citation", "citation_required", ["CR001"], [], "Open with domain context and evidence boundary."),
        paragraph("P002", "S001", "gap_claim", "MC002", ["MC001"], "needs_experiment_result", "experiment_result_required", ["CR002"], ["RP001"], "Establish the specific gap while avoiding unsafe novelty wording."),
        paragraph("P003", "S001", "contribution_claim", "MC003", ["MC002"], "needs_experiment_result", "experiment_result_required", [], ["RP002"], "Preview contributions and validation plan only."),
        paragraph("P004", "S002", "known_stream_summary", "MC004", [], "needs_citation", "citation_required", ["CR003", "CR004"], [], "Organize streams and relation to selected problem."),
        paragraph("P005", "S003", "problem_formulation", "MC005", [], "corpus_scoped_only", "planned", ["CR005"], [], "Define coupled problem properties."),
        paragraph("P006", "S004", "design_rationale", "MC006", [], "needs_experiment_result", "experiment_result_required", [], ["RP002"], "Map mechanism to problem property and ablation."),
        paragraph("P007", "S005", "validation_setup", "MC007", [], "needs_experiment_result", "experiment_result_required", ["CR006"], ["RP001", "RP002"], "Describe validation setup, not results."),
        paragraph("P008", "S006", "evidence_interpretation", "MC008", [], "needs_experiment_result", "experiment_result_required", [], ["RP003"], "Reserve result interpretation until evidence exists."),
        paragraph("P009", "S007", "limitation_statement", "MC009", [], "safe", "planned", ["CR007"], ["RP004"], "State limitations and threats."),
        paragraph("P010", "S008", "transition", "MC010", [], "safe", "planned", [], [], "Conclude without new claims."),
    ]
    citations = [
        citation("CR001", "S001", "P001", "MC001", "domain_importance_citation", "Support wind farm optimization background.", "domain evidence"),
        citation("CR002", "S001", "P002", "MC002", "gap_support_citation", "Support the specific joint layout-cabling gap.", "gap evidence"),
        citation("CR003", "S002", "P004", "MC004", "method_stream_citation", "Support layout-only and cabling-only streams.", "stream evidence"),
        citation("CR004", "S002", "P004", "MC004", "baseline_support_citation", "Support baseline relevance.", "baseline evidence"),
        citation("CR005", "S003", "P005", "MC005", "theory_support_citation", "Support problem formulation assumptions.", "theory evidence"),
        citation("CR006", "S005", "P007", "MC007", "validation_protocol_citation", "Support metric and baseline protocols.", "validation protocol evidence"),
        citation("CR007", "S007", "P009", "MC009", "counterevidence_citation", "Support limitations and counterevidence boundaries.", "counterevidence"),
    ]
    results = [
        result("RP001", "S005", "P007", "MC007", "EX001", ["M001", "M002", "M003"], ["B001", "B004"], [], "baseline_comparison_result"),
        result("RP002", "S004", "P006", "MC006", "EX002", ["M001", "M004"], ["B006"], ["A001"], "ablation_result"),
        result("RP003", "S006", "P008", "MC008", "EX003", ["M005", "M006", "M007", "M008"], ["B001", "B004"], [], "pareto_quality_result"),
        result("RP004", "S007", "P009", "MC009", "EX001", ["M002", "M003"], ["B001"], [], "qualitative_interpretation_result"),
    ]
    method_alignments = [
        {
            "method_component_id": "MCMP001",
            "component_name": "Joint layout-cabling representation",
            "linked_problem_property": "spatial-network coupling",
            "linked_theory_element_id": "TE001",
            "linked_contribution_id": "C1",
            "linked_mechanism_id": "MECH001",
            "design_rationale": "Represent coupled decisions before claiming benefit.",
            "expected_ablation_id": "A001",
            "required_explanation": "Explain why decoupled layout then cabling is insufficient.",
            "unsupported_design_risk": "algorithm wrapping risk if problem property is omitted",
            "reviewer_question": "Why is this mechanism necessary for this problem structure?",
            "revision_action": "Map component to problem property and validation target.",
        }
    ]
    experiment_items = [
        {
            "experiment_section_item_id": "ESI001",
            "linked_validation_target_id": "VT001",
            "linked_experiment_id": "EX001",
            "linked_contribution_id": "C1",
            "baseline_ids": ["B001", "B004"],
            "metric_ids": ["M001", "M002", "M003", "M005", "M007", "M008"],
            "ablation_ids": [],
            "statistical_test_ids": ["ST001"],
            "artifact_ids": ["AR001", "AR002"],
            "section_claim": "Experiment section should describe planned validation links only.",
            "result_placeholder_ids": ["RP001"],
            "missing_validation_risk": "No real results are available in the demo plan.",
            "reviewer_question": "Are baselines and metrics aligned with C1?",
            "revision_action": "Insert real result evidence only after execution.",
        }
    ]
    objections = [
        objection("RO001", "citation_gap_question", "How is the gap supported?", "missing citation", "S001", "MC001", "C1", "EX001", "high"),
        objection("RO002", "baseline_sufficiency_question", "Are the baselines sufficient?", "baseline adequacy", "S002", "MC004", "C1", "EX001", "high"),
        objection("RO003", "method_necessity_question", "Why is the joint model necessary?", "method necessity", "S003", "MC005", "C1", "EX001", "medium"),
        objection("RO004", "algorithm_wrapping_question", "Is this just wrapping an algorithm?", "method alignment", "S004", "MC006", "C2", "EX002", "high"),
        objection("RO005", "statistical_validity_question", "How are stochastic effects handled?", "statistical validity", "S005", "MC007", "C2", "EX002", "high"),
        objection("RO006", "overclaim_question", "Are results claimed before evidence exists?", "result placeholder", "S006", "MC008", "C3", "EX003", "high"),
        objection("RO007", "limitation_question", "Are synthetic/demo limitations visible?", "hidden limitation", "S007", "MC009", "C3", "EX001", "critical"),
        objection("RO008", "generalization_question", "Does the conclusion overgeneralize?", "generalization boundary", "S008", "MC010", "C3", "", "medium"),
    ]
    strategies = [strategy(i + 1, obj) for i, obj in enumerate(objections)]
    discussion = {
        "supported_claims": ["Only planning and traceability claims are supported in the demo."],
        "claims_requiring_more_evidence": ["Effectiveness, Pareto quality, feasibility, runtime, and ablation claims require real results."],
        "literature_limitations": ["Synthetic corpus is not real field evidence."],
        "experiment_limitations": ["Demo validation plan is not executed."],
        "model_limitations": ["Model assumptions require real manuscript decisions."],
        "algorithm_limitations": ["Mechanism benefit is not established without ablation results."],
        "case_study_limitations": ["Synthetic demo cases cannot support field generalization."],
        "external_validity_risks": ["Generalization beyond planned instances is not supported."],
        "construct_validity_risks": ["Metric choices require final protocol confirmation."],
        "internal_validity_risks": ["Baseline implementation and budget fairness require verification."],
        "conclusion_validity_risks": ["Do not conclude performance benefit without result evidence."],
        "counterevidence": ["Counterevidence must be surfaced from literature_gap_audit when available."],
        "generalization_boundary": "Claims are manuscript-planning claims until real evidence exists.",
        "future_work": ["Run experiments", "Replace synthetic examples with real or justified benchmark evidence"],
        "safer_discussion_wording": ["requires empirical confirmation", "within the provided corpus", "the planned experiments should assess"],
        "is_demo_manuscript_plan": is_demo,
        "requires_real_final_topic_package": is_demo,
        "requires_real_results": True,
    }
    trace_rows = [
        trace("C1", "joint layout-cabling optimization model", "MC002", "S001", "P002", ["CR002"], ["RP001"], [], ["EX001"], ["RO001"], ["RS001"], "needs_experiment_result", "experiment_result_required"),
        trace("C2", "problem-structure-aware evolutionary mechanism", "MC006", "S004", "P006", [], ["RP002"], [], ["EX002"], ["RO004"], ["RS004"], "needs_experiment_result", "experiment_result_required"),
        trace("C3", "aerodynamic-electrical-economic trade-off analysis", "MC008", "S006", "P008", [], ["RP003"], [], ["EX003"], ["RO006"], ["RS006"], "needs_experiment_result", "experiment_result_required"),
    ]
    context = {
        "manuscript_grounding_mode": "manuscript_grounded",
        "manuscript_blueprint_summary": {"section_count": len(section_plan), "readiness": "needs_revision"},
        "section_argument_summary": [{"section_id": s["section_id"], "section_role": s["section_role"]} for s in section_plan],
        "paragraph_claim_summary": [{"paragraph_id": p["paragraph_id"], "main_claim_id": p["main_claim_id"]} for p in paragraphs],
        "citation_requirement_summary": [{"citation_requirement_id": c["citation_requirement_id"], "linked_claim_id": c["linked_claim_id"]} for c in citations],
        "result_placeholder_summary": [{"result_placeholder_id": r["result_placeholder_id"], "linked_claim_id": r["linked_claim_id"]} for r in results],
        "reviewer_objection_summary": [{"reviewer_objection_id": o["reviewer_objection_id"], "severity": o["severity"]} for o in objections],
        "response_strategy_summary": [{"response_strategy_id": s["response_strategy_id"], "linked_reviewer_objection_id": s["linked_reviewer_objection_id"]} for s in strategies],
        "manuscript_adequacy_summary": {"manuscript_chain_status": "pass_with_minor_risks"},
        "claims_not_ready_for_manuscript": ["MC002", "MC003", "MC006", "MC007", "MC008"],
        "trace_context": {"contribution_ids": ["C1", "C2", "C3"], "manuscript_claim_ids": [c["manuscript_claim_id"] for c in claims]},
    }
    report = {
        "project_id": project_id,
        "manuscript_blueprint_summary": context["manuscript_blueprint_summary"],
        "section_argument_summary": context["section_argument_summary"],
        "paragraph_claim_summary": context["paragraph_claim_summary"],
        "citation_requirement_summary": context["citation_requirement_summary"],
        "result_placeholder_summary": context["result_placeholder_summary"],
        "method_alignment_summary": [{"method_component_id": "MCMP001", "linked_contribution_id": "C1"}],
        "experiment_section_summary": [{"experiment_section_item_id": "ESI001", "linked_experiment_id": "EX001"}],
        "discussion_limitations_summary": {"limitation_count": 4, "counterevidence_visible": True},
        "reviewer_objection_summary": context["reviewer_objection_summary"],
        "reviewer_response_summary": context["response_strategy_summary"],
        "manuscript_adequacy_summary": context["manuscript_adequacy_summary"],
        "manuscript_context": context,
        "claims_not_ready_for_manuscript": context["claims_not_ready_for_manuscript"],
        "reviewer_response_risks": ["anticipated objections only; no real reviewer comment is claimed"],
        "contribution_to_manuscript_traceability_table": trace_rows,
        "is_demo_manuscript_plan": is_demo,
        "requires_real_final_topic_package": is_demo,
        "requires_real_results": True,
    }
    return {
        "manuscript_blueprint": {
            "project_id": project_id,
            "manuscript_type": "journal_paper",
            "target_audience": "evolutionary computation and wind farm optimization reviewers",
            "target_venue_profile": "unspecified; requires user decision before submission framing",
            "manuscript_thesis": "A manuscript plan for problem-structure-aware joint layout-cabling optimization; not a final paper claim.",
            "section_plan": section_plan,
            "contribution_placement": [{"contribution_id": row["contribution_id"], "section_id": row["section_id"]} for row in trace_rows],
            "evidence_placement": [{"citation_requirement_id": c["citation_requirement_id"], "section_id": c["linked_section_id"]} for c in citations],
            "validation_placement": [{"result_placeholder_id": r["result_placeholder_id"], "section_id": r["linked_section_id"]} for r in results],
            "reviewer_risk_placement": [{"reviewer_objection_id": o["reviewer_objection_id"], "section_id": o["linked_section_id"]} for o in objections],
            "writing_risks": ["draft workspace", "synthetic evidence", "missing real results"],
            "manuscript_readiness": "not_manuscript_ready",
            "is_demo_manuscript_plan": is_demo,
            "requires_real_final_topic_package": is_demo,
            "requires_real_results": True,
        },
        "section_argument_map": {
            "section_arguments": section_arguments(section_plan),
            "section_argument_summary": context["section_argument_summary"],
            "missing_section_links": [],
            "assumptions": ["Section map is a plan, not manuscript prose."],
            "limitations": ["Requires human writing and real evidence before submission."],
            "is_demo_manuscript_plan": is_demo,
            "requires_real_final_topic_package": is_demo,
            "requires_real_results": True,
        },
        "paragraph_claim_plan": {
            "paragraph_plans": paragraphs,
            "manuscript_claims": claims,
            "paragraph_claim_summary": context["paragraph_claim_summary"],
            "unsupported_claims": ["MC002", "MC003", "MC006", "MC007", "MC008"],
            "assumptions": ["Claims are planned and safety-labeled."],
            "limitations": ["No final manuscript-ready empirical claim exists in demo mode."],
            "is_demo_manuscript_plan": is_demo,
            "requires_real_final_topic_package": is_demo,
            "requires_real_results": True,
        },
        "citation_requirement_map": {
            "citation_requirements": citations,
            "citation_requirement_summary": context["citation_requirement_summary"],
            "missing_citations": ["Real citations must be verified before submission."],
            "synthetic_citation_limitations": ["Synthetic corpus entries cannot be treated as real citations."],
            "assumptions": ["Citation requirements are not citations."],
            "limitations": ["No author-year citation is generated."],
            "is_demo_manuscript_plan": is_demo,
            "requires_real_final_topic_package": is_demo,
            "requires_real_results": True,
        },
        "result_placeholder_map": {
            "result_placeholders": results,
            "result_placeholder_summary": context["result_placeholder_summary"],
            "missing_results": ["All empirical result placeholders require real experiment outputs."],
            "assumptions": ["Placeholders mark needed evidence only."],
            "limitations": ["No numeric result exists."],
            "is_demo_manuscript_plan": is_demo,
            "requires_real_final_topic_package": is_demo,
            "requires_real_results": True,
        },
        "method_section_alignment": {
            "method_component_alignments": method_alignments,
            "method_alignment_summary": [{"method_component_id": "MCMP001", "linked_problem_property": "spatial-network coupling"}],
            "unsupported_components": [],
            "algorithm_wrapping_risks": [],
            "assumptions": ["Method alignment is planned."],
            "limitations": ["No algorithm performance is claimed."],
            "is_demo_manuscript_plan": is_demo,
            "requires_real_final_topic_package": is_demo,
            "requires_real_results": True,
        },
        "experiment_section_alignment": {
            "experiment_section_items": experiment_items,
            "experiment_section_summary": [{"experiment_section_item_id": "ESI001", "linked_validation_target_id": "VT001"}],
            "missing_validation_links": [],
            "result_wording_risks": [],
            "assumptions": ["Experiment section alignment is planned."],
            "limitations": ["No results are available."],
            "is_demo_manuscript_plan": is_demo,
            "requires_real_final_topic_package": is_demo,
            "requires_real_results": True,
        },
        "discussion_limitations_plan": discussion,
        "reviewer_objection_map": {
            "reviewer_objections": objections,
            "objection_summary": context["reviewer_objection_summary"],
            "high_severity_objections": [o["reviewer_objection_id"] for o in objections if o["severity"] in {"high", "critical"}],
            "assumptions": ["Objections are anticipated, not real reviewer comments."],
            "limitations": ["No real review is represented."],
            "is_demo_manuscript_plan": is_demo,
            "requires_real_final_topic_package": is_demo,
            "requires_real_results": True,
        },
        "reviewer_response_strategy": {
            "response_strategies": strategies,
            "response_strategy_summary": context["response_strategy_summary"],
            "unresolved_objections": [{"reviewer_objection_id": o["reviewer_objection_id"], "residual_risk": o["residual_risk"]} for o in objections],
            "assumptions": ["Response strategies are plans only."],
            "limitations": ["No real rebuttal is drafted."],
            "is_demo_manuscript_plan": is_demo,
            "requires_real_final_topic_package": is_demo,
            "requires_real_results": True,
        },
        "manuscript_grounding_report": report,
    }


def section(sid: str, name: str, role: str, cids: list[str], pids: list[str], eids: list[str], exids: list[str], claims: list[str], cites: list[str], results: list[str], risks: list[str], readiness: str) -> dict[str, Any]:
    return {
        "section_id": sid,
        "section_name": name,
        "section_role": role,
        "argument_goal": f"Plan the {name} section without unsupported manuscript claims.",
        "linked_contribution_ids": cids,
        "linked_problem_ids": pids,
        "linked_evidence_ids": eids,
        "linked_experiment_ids": exids,
        "required_claims": claims,
        "required_citations": cites,
        "required_results": results,
        "reviewer_risks": risks,
        "readiness_status": readiness,
    }


def claim(mid: str, text: str, claim_type: str, sid: str, pid: str, cid: str, eids: list[str], exids: list[str], rps: list[str], status: str, safety: str, citations: list[str], results: list[str], counter: list[str]) -> dict[str, Any]:
    return {
        "manuscript_claim_id": mid,
        "claim_text": text,
        "claim_type": claim_type,
        "section_id": sid,
        "paragraph_id": pid,
        "linked_problem_id": "P001",
        "linked_contribution_id": cid,
        "linked_evidence_ids": eids,
        "linked_experiment_ids": exids,
        "linked_result_placeholders": rps,
        "manuscript_claim_status": status,
        "claim_safety_level": safety,
        "required_citations": citations,
        "required_results": results,
        "counterevidence": counter,
        "safer_wording": "Use planned, corpus-scoped, or requires-confirmation wording until evidence exists.",
        "reviewer_risk": "Claim may be challenged if evidence, results, or traceability are missing.",
    }


def paragraph(pid: str, sid: str, role: str, main: str, supporting: list[str], safety: str, status: str, citations: list[str], results: list[str], purpose: str) -> dict[str, Any]:
    return {
        "paragraph_id": pid,
        "section_id": sid,
        "paragraph_role": role,
        "topic_sentence_purpose": purpose,
        "main_claim_id": main,
        "supporting_claim_ids": supporting,
        "linked_problem_id": "P001",
        "linked_contribution_id": "C1" if pid in {"P001", "P002", "P005"} else "C2" if pid in {"P003", "P006", "P007"} else "C3",
        "linked_evidence_ids": [],
        "linked_experiment_ids": ["EX001"] if results else [],
        "required_citation_ids": citations,
        "required_result_placeholder_ids": results,
        "claim_safety_level": safety,
        "manuscript_claim_status": status,
        "unsafe_wording_to_avoid": ["first", "novel", "outperforms", "statistically significant"],
        "safer_wording": "Use planned validation and requirement wording.",
        "reviewer_risk": "Reviewer may ask for evidence or clearer boundaries.",
        "revision_hooks": ["Add verified citation or real result evidence before strengthening this paragraph."],
    }


def citation(cid: str, sid: str, pid: str, claim_id: str, ctype: str, purpose: str, evidence_type: str) -> dict[str, Any]:
    return {
        "citation_requirement_id": cid,
        "linked_section_id": sid,
        "linked_paragraph_id": pid,
        "linked_claim_id": claim_id,
        "citation_requirement_type": ctype,
        "citation_purpose": purpose,
        "required_evidence_type": evidence_type,
        "candidate_paper_ids": [],
        "linked_evidence_ids": [],
        "corpus_scope": "provided corpus only; synthetic examples are not real citations",
        "missing_citation_risk": "Claim must remain cautious until real citation evidence is supplied.",
        "acceptable_if_unavailable": False,
        "required_before_submission": True,
        "safer_wording_without_citation": "requires further literature verification",
    }


def result(rid: str, sid: str, pid: str, claim_id: str, exid: str, metrics: list[str], baselines: list[str], ablations: list[str], rtype: str) -> dict[str, Any]:
    return {
        "result_placeholder_id": rid,
        "linked_section_id": sid,
        "linked_paragraph_id": pid,
        "linked_claim_id": claim_id,
        "linked_experiment_id": exid,
        "linked_metric_ids": metrics,
        "linked_baseline_ids": baselines,
        "linked_ablation_ids": ablations,
        "result_placeholder_type": rtype,
        "expected_result_needed": "Insert real, traceable results here only after experiments are run.",
        "success_condition": "Claim can be strengthened only if real evidence meets the validation threshold.",
        "failure_condition": "Claim must be downgraded or removed if evidence does not support it.",
        "interpretation_plan": "Interpret against baseline, metric, ablation, statistical, and artifact links.",
        "required_table_or_figure": "To be selected after real results exist.",
        "statistical_requirement": "Use planned statistical test outputs only after execution.",
        "current_status": "result_not_available",
        "unsafe_result_wording_to_avoid": ["outperforms", "improves by", "p < 0.05"],
        "allowed_placeholder_wording": "insert traceable result evidence from the linked experiment here after execution",
    }


def objection(oid: str, otype: str, question: str, risk: str, sid: str, claim: str, cid: str, exid: str, severity: str) -> dict[str, Any]:
    return {
        "reviewer_objection_id": oid,
        "objection_type": otype,
        "likely_question": question,
        "source_risk": risk,
        "linked_section_id": sid,
        "linked_claim_id": claim,
        "linked_contribution_id": cid,
        "linked_experiment_id": exid,
        "severity": severity,
        "required_evidence": ["verified citation or real result evidence, as applicable"],
        "manuscript_repair_action": "Revise section wording and add missing evidence requirement.",
        "residual_risk": "Residual risk remains until real evidence is supplied.",
    }


def strategy(index: int, objection_item: dict[str, Any]) -> dict[str, Any]:
    sid = f"RS{index:03d}"
    return {
        "response_strategy_id": sid,
        "linked_reviewer_objection_id": objection_item["reviewer_objection_id"],
        "linked_claim_id": objection_item["linked_claim_id"],
        "linked_section_id": objection_item["linked_section_id"],
        "direct_answer_plan": "Answer as an anticipated risk, not as a real reviewer exchange.",
        "evidence_to_cite": ["Use verified evidence IDs only when available."],
        "experiment_to_reference": [objection_item["linked_experiment_id"]] if objection_item["linked_experiment_id"] else [],
        "manuscript_revision": "Add or revise the relevant manuscript section before submission.",
        "safer_claim_revision": "Downgrade unsupported wording to planned or requires-confirmation wording.",
        "additional_analysis_needed": "Run or verify the required experiment/literature support before making a strong claim.",
        "what_not_to_claim": ["Do not claim reviewer approval.", "Do not claim completed experiments.", "Do not invent citations."],
        "residual_risk": objection_item["residual_risk"],
    }


def trace(cid: str, contribution: str, mid: str, sid: str, pid: str, crids: list[str], rpids: list[str], eids: list[str], exids: list[str], roids: list[str], rsids: list[str], safety: str, status: str) -> dict[str, Any]:
    return {
        "contribution_id": cid,
        "contribution_claim": contribution,
        "manuscript_claim_id": mid,
        "section_id": sid,
        "paragraph_id": pid,
        "citation_requirement_ids": crids,
        "result_placeholder_ids": rpids,
        "evidence_ids": eids,
        "experiment_ids": exids,
        "reviewer_objection_ids": roids,
        "response_strategy_ids": rsids,
        "claim_safety_level": safety,
        "manuscript_claim_status": status,
    }


def section_arguments(section_plan: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chains = {
        "Introduction": ["background", "existing streams", "unresolved tension", "specific gap", "problem statement", "theoretical positioning", "contribution preview", "validation preview"],
        "Related Work": ["research stream", "representative evidence", "limitation or boundary", "relation to selected problem", "baseline relevance", "remaining gap"],
        "Method": ["problem property", "method component", "design rationale", "contribution link", "validation or ablation link"],
        "Experiments": ["validation target", "experiment design", "baseline", "metric", "ablation", "statistical test", "artifact"],
        "Discussion": ["supported insight", "limitation", "counterevidence", "generalization boundary", "future repair"],
    }
    out = []
    for section_item in section_plan:
        name = section_item["section_name"]
        out.append({
            "section_id": section_item["section_id"],
            "section_name": name,
            "section_role": section_item["section_role"],
            "argument_chain": chains.get(name, ["planned claim", "support boundary", "transition"]),
            "opening_purpose": section_item["argument_goal"],
            "key_claims": section_item["required_claims"],
            "evidence_requirements": section_item["linked_evidence_ids"],
            "citation_requirements": section_item["required_citations"],
            "result_placeholders": section_item["required_results"],
            "transition_in": "Use a controlled transition from the previous section.",
            "transition_out": "Prepare the next section without adding unsupported claims.",
            "reviewer_risks": section_item["reviewer_risks"],
            "missing_support": [] if section_item["required_citations"] or section_item["required_results"] else ["No external support required or currently planned."],
            "revision_hooks": ["Add evidence, citation requirement, or result placeholder before strengthening claims."],
        })
    return out


def collect(plan: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        "sections": plan.get("manuscript_blueprint", {}).get("section_plan", []),
        "section_arguments": plan.get("section_argument_map", {}).get("section_arguments", []),
        "paragraphs": plan.get("paragraph_claim_plan", {}).get("paragraph_plans", []),
        "claims": plan.get("paragraph_claim_plan", {}).get("manuscript_claims", []),
        "citations": plan.get("citation_requirement_map", {}).get("citation_requirements", []),
        "results": plan.get("result_placeholder_map", {}).get("result_placeholders", []),
        "methods": plan.get("method_section_alignment", {}).get("method_component_alignments", []),
        "experiments": plan.get("experiment_section_alignment", {}).get("experiment_section_items", []),
        "objections": plan.get("reviewer_objection_map", {}).get("reviewer_objections", []),
        "strategies": plan.get("reviewer_response_strategy", {}).get("response_strategies", []),
    }


def evaluate_plan(plan: dict[str, Any], strict: bool, require_complete: bool = False, workspace: Path | None = None) -> tuple[list[str], list[str], list[str]]:
    passes: list[str] = []
    warnings: list[str] = []
    failures: list[str] = []
    objects = collect(plan)
    failures.extend(find_patterns(plan, CITATION_WORDING, "FAIL fabricated citation risk"))
    failures.extend(find_patterns(plan, RESULT_WORDING, "FAIL fabricated result wording or unsupported empirical claim"))
    failures.extend(find_patterns(plan, [FAKE_REVIEWER], "FAIL fake reviewer comment risk"))
    overclaims = find_patterns(plan, [OVERCLAIM], "FAIL overclaim risk")
    failures.extend(overclaims if strict else [])
    warnings.extend([] if strict else overclaims)

    id_specs = [
        ("sections", "section_id"),
        ("paragraphs", "paragraph_id"),
        ("claims", "manuscript_claim_id"),
        ("citations", "citation_requirement_id"),
        ("results", "result_placeholder_id"),
        ("objections", "reviewer_objection_id"),
        ("strategies", "response_strategy_id"),
    ]
    for collection, field in id_specs:
        ids = [item.get(field) for item in objects[collection] if item.get(field)]
        dupes = sorted({item for item in ids if ids.count(item) > 1})
        if dupes:
            failures.append(f"FAIL duplicate {field}: {', '.join(dupes)}")
        else:
            passes.append(f"PASS unique {field}")

    section_ids = {item.get("section_id") for item in objects["sections"]}
    paragraph_ids = {item.get("paragraph_id") for item in objects["paragraphs"]}
    claim_ids = {item.get("manuscript_claim_id") for item in objects["claims"]}
    objection_ids = {item.get("reviewer_objection_id") for item in objects["objections"]}

    for paragraph_item in objects["paragraphs"]:
        if paragraph_item.get("section_id") not in section_ids:
            failures.append(f"FAIL paragraph linked section missing: {paragraph_item.get('paragraph_id')}")
    for citation_item in objects["citations"]:
        if citation_item.get("linked_paragraph_id") not in paragraph_ids:
            failures.append(f"FAIL citation linked paragraph missing: {citation_item.get('citation_requirement_id')}")
    for result_item in objects["results"]:
        if result_item.get("linked_paragraph_id") not in paragraph_ids:
            failures.append(f"FAIL result placeholder linked paragraph missing: {result_item.get('result_placeholder_id')}")
    for objection_item in objects["objections"]:
        if objection_item.get("linked_claim_id") not in claim_ids:
            failures.append(f"FAIL reviewer objection linked claim missing: {objection_item.get('reviewer_objection_id')}")
    for strategy_item in objects["strategies"]:
        if strategy_item.get("linked_reviewer_objection_id") not in objection_ids:
            failures.append(f"FAIL response_strategy linked objection missing: {strategy_item.get('response_strategy_id')}")
        if not strategy_item.get("what_not_to_claim"):
            failures.append(f"FAIL response strategy missing what_not_to_claim: {strategy_item.get('response_strategy_id')}")
    if not any("linked" in failure for failure in failures):
        passes.append("PASS manuscript reference integrity")

    intro = next((item for item in objects["section_arguments"] if item.get("section_name") == "Introduction"), {})
    intro_chain = [str(item).lower() for item in intro.get("argument_chain", [])]
    for token in ["background", "gap", "problem", "contribution", "validation"]:
        if not any(token in item for item in intro_chain):
            failures.append(f"FAIL weak introduction link: missing {token}")
    related = next((item for item in objects["section_arguments"] if item.get("section_name") == "Related Work"), {})
    if not any("research stream" in str(item).lower() for item in related.get("argument_chain", [])):
        failures.append("FAIL weak related work link: missing stream-based organization")
    method_risks = plan.get("method_section_alignment", {}).get("algorithm_wrapping_risks", [])
    if method_risks:
        failures.append("FAIL algorithm wrapping risk: method component lacks problem-property alignment")
    for method_item in objects["methods"]:
        if not method_item.get("linked_problem_property"):
            failures.append(f"FAIL method component without problem property link: {method_item.get('method_component_id')}")
    if not objects["experiments"]:
        failures.append("FAIL experiment section without validation link")
    for exp_item in objects["experiments"]:
        if not exp_item.get("linked_validation_target_id") or not exp_item.get("metric_ids"):
            failures.append(f"FAIL experiment section mismatch: {exp_item.get('experiment_section_item_id')}")
    discussion = plan.get("discussion_limitations_plan", {})
    if not discussion.get("experiment_limitations") or not discussion.get("counterevidence"):
        failures.append("FAIL hidden limitation risk: discussion lacks limitations or counterevidence")
    for claim_item in objects["claims"]:
        cid = claim_item.get("manuscript_claim_id")
        has_trace = bool(claim_item.get("linked_contribution_id") or claim_item.get("linked_evidence_ids") or claim_item.get("linked_experiment_ids") or claim_item.get("linked_result_placeholders"))
        if not has_trace:
            failures.append(f"FAIL manuscript claim without traceability: {cid}")
        if claim_item.get("claim_type") == "gap_claim" and not claim_item.get("required_citations") and not claim_item.get("linked_evidence_ids"):
            failures.append(f"FAIL gap claim without citation requirement: {cid}")
        if "effect" in str(claim_item.get("claim_type", "")).lower() and not claim_item.get("linked_result_placeholders"):
            failures.append(f"FAIL effectiveness claim without result placeholder: {cid}")
        if claim_item.get("claim_safety_level") == "safe" and claim_item.get("manuscript_claim_status") in {"unsupported", "experiment_result_required", "citation_required"}:
            failures.append(f"FAIL unsupported safe claim: {cid}")
    high = [item for item in objects["objections"] if item.get("severity") in {"high", "critical"}]
    strategy_by_objection = {item.get("linked_reviewer_objection_id"): item for item in objects["strategies"]}
    for objection_item in high:
        strategy_item = strategy_by_objection.get(objection_item.get("reviewer_objection_id"))
        if not strategy_item:
            failures.append(f"FAIL high-risk reviewer objection without response strategy: {objection_item.get('reviewer_objection_id')}")
        elif not (strategy_item.get("manuscript_revision") or strategy_item.get("additional_analysis_needed")):
            failures.append(f"FAIL high severity objection lacks repair strategy: {objection_item.get('reviewer_objection_id')}")
    report = plan.get("manuscript_grounding_report", {})
    if not report.get("contribution_to_manuscript_traceability_table"):
        failures.append("FAIL missing manuscript traceability table")

    if require_complete:
        if any(isinstance(section, dict) and (section.get("is_demo_manuscript_plan") or section.get("requires_real_final_topic_package") or section.get("requires_real_results")) for section in plan.values()):
            failures.append("FAIL demo manuscript plan requires real final topic package and real results")
        if workspace:
            final_path = workspace / "06_final_topic_package" / "output.json"
            if not final_path.exists():
                failures.append("FAIL incomplete final topic package: missing final_topic_package output")
            else:
                final = read_json(final_path)
                if final.get("status") == "draft":
                    failures.append("FAIL incomplete final topic package: final_topic_package output is draft")
                structured = final.get("structured_output", {})
                if not isinstance(structured, dict) or not (structured.get("manuscript_traceability_table") or structured.get("Contribution-to-Manuscript Traceability")):
                    failures.append("FAIL manuscript traceability table incomplete in final topic package")

    if not failures:
        passes.append("PASS manuscript adequacy checks")
    return passes, warnings, failures


def report_lines(title: str, passes: list[str], warnings: list[str], failures: list[str], key: str = "validation_decision") -> list[str]:
    decision = "fail_requires_revision" if failures else ("pass_with_warnings" if warnings else "pass")
    return [
        f"# {title}",
        "",
        f"- pass_count: {len(passes)}",
        f"- warning_count: {len(warnings)}",
        f"- fail_count: {len(failures)}",
        f"- {key}: {decision}",
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
