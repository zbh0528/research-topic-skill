from __future__ import annotations

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_EXAMPLES = {
    "project_context.schema.json": "sample_project_context_output.json",
    "domain_scan.schema.json": "sample_domain_scan_output.json",
    "problem_cards.schema.json": "sample_problem_cards_output.json",
    "theoretical_positioning.schema.json": "sample_theoretical_positioning_output.json",
    "contribution_chain.schema.json": "sample_contribution_chain_output.json",
    "audit_report.schema.json": "sample_audit_report_output.json",
    "final_topic_package.schema.json": "sample_final_topic_package_output.json"
}
GLOBAL_FIELDS = {
    "status",
    "module_id",
    "module_name",
    "input_summary",
    "structured_output",
    "next_input",
    "assumptions",
    "uncertainty_log",
    "evidence_requirements",
    "reviewer_risks",
    "revision_hooks",
    "trace_context",
}
EVIDENCE_STATUSES = {
    "verified",
    "user_provided",
    "inferred",
    "needs_literature_verification",
    "speculative",
}
STATUSES = {"draft", "complete", "validated", "needs_revision"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def test_all_schemas_are_json_objects() -> None:
    for schema_path in (ROOT / "schemas").glob("*.schema.json"):
        schema = load_json(schema_path)
        assert schema["type"] == "object", schema_path
        assert GLOBAL_FIELDS.issubset(set(schema["required"])), schema_path
        assert schema["properties"]["status"]["$ref"] == "#/$defs/status"
        assert set(schema["$defs"]["status"]["enum"]) == STATUSES
        assert set(schema["$defs"]["evidence_status"]["enum"]) == EVIDENCE_STATUSES


def test_manifest_schema_paths_exist() -> None:
    manifest = load_json(ROOT / "skill_manifest.json")
    for module in manifest["modules"]:
        assert (ROOT / module["schema"]).exists()
        assert (ROOT / module["template"]).exists()
        assert (ROOT / module["module_doc"]).exists()


def test_examples_validate_against_schemas() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    for schema_name, example_name in SCHEMA_EXAMPLES.items():
        schema = load_json(ROOT / "schemas" / schema_name)
        example = load_json(ROOT / "examples" / example_name)
        jsonschema.Draft202012Validator(schema).validate(example)


def test_schema_rejects_missing_global_fields() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = load_json(ROOT / "schemas" / "project_context.schema.json")
    example = load_json(ROOT / "examples" / "sample_project_context_output.json")
    del example["structured_output"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(example)


def test_schema_rejects_invalid_status_and_evidence_status() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = load_json(ROOT / "schemas" / "project_context.schema.json")
    example = load_json(ROOT / "examples" / "sample_project_context_output.json")
    example["status"] = "ready_for_next_module"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(example)
    example = load_json(ROOT / "examples" / "sample_project_context_output.json")
    example["assumptions"][0]["evidence_status"] = "unsupported"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(example)


def test_trace_context_links_across_examples() -> None:
    domain = load_json(ROOT / "examples" / "sample_domain_scan_output.json")
    problem = load_json(ROOT / "examples" / "sample_problem_cards_output.json")
    theory = load_json(ROOT / "examples" / "sample_theoretical_positioning_output.json")
    contribution = load_json(ROOT / "examples" / "sample_contribution_chain_output.json")

    domain_tensions = {item["tension_id"] for item in domain["structured_output"]["domain_tensions"]}
    selected_problem = problem["structured_output"]["selected_problem"]
    assert selected_problem["source_domain_tension_id"] in domain_tensions

    theory_trace = theory["trace_context"]
    assert selected_problem["problem_id"] in theory_trace["problem_ids"]

    contribution_item = contribution["structured_output"]["contributions"][0]
    assert contribution_item["linked_problem_id"] == selected_problem["problem_id"]
    assert contribution_item["linked_theoretical_positioning"] in theory_trace["theory_element_ids"]
