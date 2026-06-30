#!/usr/bin/env python3
"""Build conservative paper cards and a corpus-scoped literature matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNKNOWN = "unknown"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def list_value(value: object) -> list:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    return [value]


def explicit(record: dict, key: str, default: object = UNKNOWN) -> object:
    extra = record.get("extra_fields", {})
    if isinstance(extra, dict) and key in extra:
        return extra[key]
    return record.get(key, default)


def source_text(record: dict) -> tuple[str | None, str | None]:
    if record.get("relevant_excerpts"):
        return "relevant_excerpts", "; ".join(map(str, record["relevant_excerpts"]))
    if record.get("abstract"):
        return "abstract", str(record["abstract"])
    if record.get("user_notes"):
        return "user_notes", str(record["user_notes"])
    return None, None


def make_claim(record: dict, claim_no: int, evidence_no: int) -> dict | None:
    field, excerpt = source_text(record)
    if not field or not excerpt:
        return None
    claim_id = f"CL{claim_no:03d}"
    evidence_id = f"EV{evidence_no:03d}"
    synthetic = bool(record.get("is_synthetic"))
    return {
        "claim_id": claim_id,
        "claim_text": f"User-provided {field} describes this record's declared wind-farm optimization scope.",
        "claim_type": "domain_fact",
        "claim_scope": "corpus_scoped",
        "evidence_status": "user_provided",
        "grounding_status": "corpus_scoped_only" if synthetic else "partially_grounded",
        "support_strength": "contextual",
        "supporting_evidence_ids": [evidence_id],
        "contradicting_evidence_ids": [],
        "linked_paper_ids": [record["paper_id"]],
        "confidence": 0.5 if synthetic else 0.65,
        "limitations": "Synthetic examples and user notes are not verified field evidence.",
        "safer_wording": "within the provided corpus",
        "source_field": field,
        "source_excerpt": excerpt,
        "paraphrase": excerpt,
    }


def card_from_record(record: dict, claim_no: int, evidence_no: int) -> tuple[dict, list[dict]]:
    claim = make_claim(record, claim_no, evidence_no)
    claims = [claim] if claim else []
    title_only = not claims
    card = {
        "paper_id": record["paper_id"],
        "bibliographic_metadata": {
            "title": record.get("title"),
            "authors": record.get("authors", []),
            "year": record.get("year"),
            "venue": record.get("venue"),
            "doi": record.get("doi"),
            "url": record.get("url"),
        },
        "source_type": record.get("source_type", "user_provided_record"),
        "is_synthetic": bool(record.get("is_synthetic")),
        "relevance_to_project": explicit(record, "relevance_to_project", UNKNOWN if title_only else "user_provided_context"),
        "research_stream": explicit(record, "research_stream", UNKNOWN),
        "research_problem": explicit(record, "research_problem", UNKNOWN),
        "method_family": explicit(record, "method_family", UNKNOWN),
        "optimization_type": explicit(record, "optimization_type", UNKNOWN),
        "decision_variables": list_value(explicit(record, "decision_variables", [])),
        "objectives": list_value(explicit(record, "objectives", [])),
        "constraints": list_value(explicit(record, "constraints", [])),
        "coupling_handled": explicit(record, "coupling_handled", UNKNOWN),
        "wake_model_handled": explicit(record, "wake_model_handled", UNKNOWN),
        "cable_routing_handled": explicit(record, "cable_routing_handled", UNKNOWN),
        "electrical_losses_handled": explicit(record, "electrical_losses_handled", UNKNOWN),
        "network_topology_handled": explicit(record, "network_topology_handled", UNKNOWN),
        "uncertainty_handled": explicit(record, "uncertainty_handled", UNKNOWN),
        "baseline_methods": list_value(explicit(record, "baseline_methods", [])),
        "evaluation_metrics": list_value(explicit(record, "evaluation_metrics", [])),
        "datasets_or_case_studies": list_value(explicit(record, "datasets_or_case_studies", [])),
        "reported_findings": list_value(explicit(record, "reported_findings", [])),
        "stated_limitations": list_value(explicit(record, "stated_limitations", [])),
        "extracted_claims": claims,
        "extraction_uncertainty": "title-only record; no detailed claim extracted" if title_only else "claims are limited to user-provided text",
        "evidence_status": record.get("evidence_status", "user_provided"),
    }
    return card, claims


def coverage_level(count: int) -> str:
    if count == 0:
        return "empty_in_current_corpus"
    if count == 1:
        return "weakly_covered"
    if count == 2:
        return "moderately_covered"
    return "strongly_covered"


def make_cell(index: int, label: str, cards: list[dict]) -> dict:
    matching = [card for card in cards if label in {
        str(card.get("research_stream")),
        str(card.get("method_family")),
        str(card.get("coupling_handled")),
    }]
    evidence_ids = [
        evidence_id
        for card in matching
        for claim in card.get("extracted_claims", [])
        for evidence_id in claim.get("supporting_evidence_ids", [])
    ]
    return {
        "cell_id": f"MC{index:03d}",
        "dimension_values": [label],
        "paper_ids": [card["paper_id"] for card in matching],
        "evidence_ids": evidence_ids,
        "coverage_level": coverage_level(len(matching)),
        "grounding_status": "corpus_scoped_only" if matching else "needs_literature_verification",
        "limitations": "Coverage is limited to explicit paper-card fields in the provided corpus.",
    }


def write_markdown(path: Path, title: str, data: dict) -> None:
    lines = [f"# {title}", "", f"- corpus_id: `{data.get('corpus_id')}`", f"- corpus_scope: {data.get('corpus_scope')}"]
    path.write_text("\n".join(lines) + "\n")


def inject_evidence_context(workspace: Path, context: dict) -> None:
    module_dir = workspace / "00_project_intake"
    output_path = module_dir / "output.json"
    next_path = module_dir / "next_input.json"
    if not output_path.exists() or not next_path.exists():
        return
    output = load_json(output_path)
    output.setdefault("next_input", {})["evidence_context"] = context
    write_json(output_path, output)
    write_json(next_path, output["next_input"])


def compact_claim(claim: dict) -> dict:
    return {
        "claim_id": claim.get("claim_id"),
        "claim_type": claim.get("claim_type"),
        "claim_scope": claim.get("claim_scope"),
        "grounding_status": claim.get("grounding_status"),
        "support_strength": claim.get("support_strength"),
        "linked_paper_ids": claim.get("linked_paper_ids", []),
        "linked_evidence_ids": claim.get("supporting_evidence_ids", []),
        "safer_wording": claim.get("safer_wording"),
        "limitations": claim.get("limitations"),
    }


def compact_gap(gap: dict) -> dict:
    return {
        "gap_id": gap.get("gap_id"),
        "corpus_scope": gap.get("corpus_scope"),
        "grounding_status": gap.get("grounding_status"),
        "supporting_evidence_ids": gap.get("supporting_evidence_ids", []),
        "contradicting_evidence_ids": gap.get("contradicting_evidence_ids", []),
        "novelty_risk": gap.get("novelty_risk"),
        "safer_gap_wording": gap.get("safer_gap_wording"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace if args.workspace.is_absolute() else ROOT / args.workspace
    evidence_dir = workspace / "literature_evidence"
    records_path = evidence_dir / "bibliographic_records.json"
    if not records_path.exists():
        raise SystemExit(f"missing bibliographic_records.json: {records_path}")
    target_files = [
        evidence_dir / "paper_cards.json",
        evidence_dir / "literature_matrix.json",
        evidence_dir / "evidence_claim_map.json",
        evidence_dir / "literature_gap_audit.json",
    ]
    if not args.overwrite and any(path.exists() for path in target_files):
        raise SystemExit("literature matrix artifacts already exist; pass --overwrite")
    records_payload = load_json(records_path)
    records = records_payload.get("bibliographic_records", [])
    corpus_id = records_payload.get("corpus_id", "provided_literature_corpus")
    corpus_scope = records_payload.get("corpus_scope", "user-provided corpus only")

    cards: list[dict] = []
    claims: list[dict] = []
    for i, record in enumerate(records, start=1):
        card, card_claims = card_from_record(record, i, i)
        cards.append(card)
        claims.extend(card_claims)

    dimensions = [
        "layout_only_optimization",
        "cabling_only_optimization",
        "joint_layout_cabling_optimization",
        "sequential_layout_then_cabling",
        "multi_objective_wind_farm_optimization",
        "constrained_wind_farm_optimization",
    ]
    coverage = [make_cell(i, label, cards) for i, label in enumerate(dimensions, start=1)]
    evidence_objects = [
        {
            "evidence_id": claim["supporting_evidence_ids"][0],
            "paper_id": claim["linked_paper_ids"][0],
            "claim_id": claim["claim_id"],
            "claim_text": claim["claim_text"],
            "claim_type": claim["claim_type"],
            "source_field": claim["source_field"],
            "source_excerpt": claim["source_excerpt"],
            "paraphrase": claim["paraphrase"],
            "evidence_status": claim["evidence_status"],
            "grounding_status": claim["grounding_status"],
            "support_strength": claim["support_strength"],
            "confidence": claim["confidence"],
            "limitations": claim["limitations"],
            "extraction_uncertainty": "limited to user-provided text",
        }
        for claim in claims
    ]
    paper_cards = {"corpus_id": corpus_id, "corpus_scope": corpus_scope, "paper_cards": cards}
    matrix = {
        "corpus_id": corpus_id,
        "corpus_scope": corpus_scope,
        "paper_count": len(cards),
        "research_streams": dimensions,
        "method_families": ["evolutionary_algorithm", "graph_algorithm", "heuristic", "unknown"],
        "problem_dimensions": ["continuous_layout_variables", "graph_topology_variables", "mixed_discrete_continuous_decisions", "spatial_network_coupling"],
        "objective_dimensions": ["annual_energy_production", "wake_loss", "cable_cost", "electrical_loss", "levelized_cost_of_energy"],
        "constraint_dimensions": ["turbine_spacing", "site_boundary", "cable_capacity", "radial_topology", "cable_crossing"],
        "coupling_dimensions": ["wake_layout_coupling", "layout_cable_cost_coupling", "sequential_vs_joint_design"],
        "evidence_density": {"claim_count": len(claims), "evidence_object_count": len(evidence_objects)},
        "coverage_map": coverage,
        "underrepresented_cells": [cell for cell in coverage if cell["coverage_level"] in {"empty_in_current_corpus", "weakly_covered"}],
        "saturated_cells": [cell for cell in coverage if cell["coverage_level"] == "strongly_covered"],
        "contradictory_cells": [],
        "matrix_limitations": ["This matrix is corpus-scoped and cannot prove a field-wide gap."],
    }
    claim_map = {
        "corpus_id": corpus_id,
        "corpus_scope": corpus_scope,
        "claims": claims,
        "evidence_objects": evidence_objects,
        "support_links": [{"claim_id": claim["claim_id"], "evidence_id": claim["supporting_evidence_ids"][0]} for claim in claims],
        "contradiction_links": [],
        "ungrounded_claims": [],
        "claims_requiring_verification": [],
        "claim_grounding_summary": {
            "grounded_count": 0,
            "corpus_scoped_only_count": len(claims),
            "verified_field_claim_count": 0,
        },
    }
    joint_cells = [cell for cell in coverage if "joint_layout_cabling_optimization" in cell["dimension_values"]]
    joint_evidence = joint_cells[0]["evidence_ids"] if joint_cells else []
    gap = {
        "gap_id": "G001",
        "gap_statement": "within this synthetic demonstration corpus, evidence is insufficient for a field-wide joint layout-cabling novelty claim",
        "source_claim_ids": [claim["claim_id"] for claim in claims],
        "source_matrix_cells": [cell["cell_id"] for cell in coverage],
        "supporting_evidence_ids": [ev["evidence_id"] for ev in evidence_objects[:2]],
        "contradicting_evidence_ids": joint_evidence,
        "corpus_scope": corpus_scope,
        "gap_type": "validation_gap",
        "grounding_status": "partially_grounded" if joint_evidence else "corpus_scoped_only",
        "confidence": 0.4,
        "novelty_risk": "high unless broader literature verification is performed",
        "overclaim_risk": "field-wide no-one-studied wording is unsafe",
        "safer_gap_wording": "within the provided corpus, the coupling evidence remains limited and requires broader verification",
        "required_additional_literature": ["systematic search strategy", "real paper abstracts/full texts", "baseline coverage review"],
        "downstream_problem_potential": "Use only as a corpus-scoped candidate problem.",
    }
    accepted_gaps = [gap] if gap["supporting_evidence_ids"] else []
    gap_audit = {
        "corpus_id": corpus_id,
        "corpus_scope": corpus_scope,
        "gap_candidates": [gap],
        "accepted_gap_candidates": accepted_gaps,
        "rejected_gap_candidates": [],
        "counterevidence_summary": [{"gap_id": "G001", "contradicting_evidence_ids": joint_evidence}] if joint_evidence else [],
        "novelty_risk_summary": "No first or field-wide novelty claim is supported by this corpus.",
        "required_additional_literature": gap["required_additional_literature"],
        "audit_decision": "sufficient_for_corpus_scoped_problem_identification" if accepted_gaps else "insufficient_evidence",
    }
    report = {
        "corpus_id": corpus_id,
        "corpus_scope": corpus_scope,
        "input_summary": records_payload.get("input_files", []),
        "paper_card_summary": {"paper_count": len(cards)},
        "literature_matrix_summary": matrix["evidence_density"],
        "claim_grounding_summary": claim_map["claim_grounding_summary"],
        "gap_audit_summary": {"audit_decision": gap_audit["audit_decision"]},
        "unsupported_claims": [],
        "counterevidence": gap_audit["counterevidence_summary"],
        "claims_requiring_verification": [],
        "downstream_evidence_context": {
            "corpus_id": corpus_id,
            "corpus_scope": corpus_scope,
            "paper_count": len(cards),
            "key_grounded_claims": [compact_claim(claim) for claim in claims[:5]],
            "candidate_gap_claims": [compact_gap(gap)],
            "counterevidence_summary": gap_audit["counterevidence_summary"],
            "claims_requiring_verification": [],
            "evidence_policy": records_payload.get("evidence_policy", {}),
            "trace_context": {"evidence_ids": [ev["evidence_id"] for ev in evidence_objects]},
        },
    }

    write_json(evidence_dir / "paper_cards.json", paper_cards)
    write_json(evidence_dir / "literature_matrix.json", matrix)
    write_json(evidence_dir / "evidence_claim_map.json", claim_map)
    write_json(evidence_dir / "literature_gap_audit.json", gap_audit)
    write_json(evidence_dir / "literature_grounding_report.json", report)
    write_markdown(evidence_dir / "paper_cards.md", "Paper Cards", paper_cards)
    write_markdown(evidence_dir / "literature_matrix.md", "Literature Matrix", matrix)
    write_markdown(evidence_dir / "evidence_claim_map.md", "Evidence Claim Map", claim_map)
    write_markdown(evidence_dir / "literature_gap_audit.md", "Literature Gap Audit", gap_audit)
    inject_evidence_context(workspace, report["downstream_evidence_context"])
    print(f"PASS built literature matrix for {len(cards)} paper cards")


if __name__ == "__main__":
    main()
