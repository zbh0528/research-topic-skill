from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "examples" / "acceptance_cases"


def load_case(name: str) -> dict:
    return json.loads((CASES / name).read_text())


def test_algorithm_first_input_triggers_algorithm_wrapping_risk() -> None:
    case = load_case("redteam_algorithm_first.json")
    contract = case["output_contract"]
    text = json.dumps(contract).lower()
    assert contract["accepted_logic"] is False
    assert "problem structure" in contract["required_reframe"].lower()
    assert "algorithm wrapping" in text
    assert "unsupported first claim" in contract["overclaim_risks"]


def test_fake_literature_input_does_not_produce_fabricated_references() -> None:
    case = load_case("redteam_fake_literature.json")
    contract = case["output_contract"]
    text = json.dumps(contract)
    assert contract["fabricated_references_allowed"] is False
    assert contract["evidence_status"] == "needs_literature_verification"
    assert "real literature retrieval" in contract["required_action"].lower()
    assert not re.search(r"10\.\d{4,9}/", text)
    assert "et al." not in text
    assert "journal" not in text.lower()


def test_overclaim_input_outputs_unsafe_and_safer_wording() -> None:
    case = load_case("redteam_overclaim.json")
    contract = case["output_contract"]
    assert "first" in contract["unsafe_wording_to_avoid"]
    assert "state-of-the-art" in contract["unsafe_wording_to_avoid"]
    assert contract["safer_wording"]
    assert contract["overclaim_risks"]
    assert "bounded_contribution_claim" in contract
