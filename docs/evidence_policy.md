# Evidence Policy

## Evidence Object

An evidence object must include:

- `evidence_id`
- `paper_id`
- `claim_id`
- `claim_text`
- `claim_type`
- `source_field`
- `source_excerpt`
- `paraphrase`
- `evidence_status`
- `grounding_status`
- `support_strength`
- `confidence`
- `limitations`
- `extraction_uncertainty`

## Status Difference

`evidence_status` answers where the information came from: `verified`, `user_provided`, `inferred`, `needs_literature_verification`, or `speculative`.

`grounding_status` answers whether the claim is supported: `grounded`, `partially_grounded`, `ungrounded`, `contradicted`, `needs_literature_verification`, or `corpus_scoped_only`.

## Claim Types

Allowed `claim_type` values:

- `bibliographic_fact`
- `domain_fact`
- `method_classification`
- `objective_classification`
- `constraint_classification`
- `limitation_claim`
- `gap_claim`
- `problem_importance_claim`
- `theory_positioning_claim`
- `contribution_claim`
- `validation_requirement`
- `baseline_requirement`
- `reviewer_risk_claim`

## Support Strength

Allowed `support_strength` values: `direct`, `indirect`, `weak`, `contradictory`, `contextual`, `not_applicable`.

## Verified Minimum

`verified` requires user-provided real material, `paper_id`, `claim_id`, and a traceable source. Bibliographic facts may use metadata fields. Non-bibliographic claims require `source_excerpt` or a locatable user note/excerpt; metadata alone is not enough.

## Gap Claim Minimum

A gap claim requires literature matrix coverage, supporting evidence claims, counterevidence check, `corpus_scope`, novelty risk, and safer wording. It cannot rely only on "not found".

## Contribution Claim Minimum

A contribution claim requires `linked_problem_id`, `linked_domain_tension_id`, `linked_evidence_ids`, `linked_theory_elements`, `required_validation`, `boundary_of_claim`, `unsafe_wording_to_avoid`, and `safer_wording`.

## Counterevidence Policy

Contradictory evidence must produce `counterevidence`, `contradiction_type`, `impact_on_gap`, and `safer_reformulation`.

## Novelty Policy

Default forbid `first`, `novel`, `state-of-the-art`, and `unprecedented`. Corpus-scoped novelty is allowed only with explicit scope limits.

## Synthetic Policy

Synthetic examples test structure only. They cannot support real `verified` field claims.

## Audit Modes

`audit_claim_grounding.py --strict` validates structured claims that already exist in module outputs and skips untouched `PENDING_MODULE_OUTPUT` draft placeholders. This mode is for incremental module checks.

`audit_claim_grounding.py --strict --require-complete-chain` is for release-grade chain acceptance. It must fail when the final topic package is incomplete, the Evidence Traceability Table is missing, the selected problem lacks evidence links, or contribution claims lack evidence links.
