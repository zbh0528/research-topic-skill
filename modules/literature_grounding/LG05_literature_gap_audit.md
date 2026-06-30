# LG05 Literature Gap Audit

## Module ID
`LG05_literature_gap_audit`

## Module Name
Literature Gap Audit

## Purpose
Audit whether a candidate gap is supported by the current corpus.

## What this module does
- Checks absence-of-evidence fallacy, counterevidence, corpus scope, specificity, problem potential, and overclaim risk.

## What this module does not do
- It does not certify field-wide novelty.

## Required input
`literature_matrix.json` and `evidence_claim_map.json`.

## Required output files
- `literature_evidence/literature_gap_audit.json`
- `literature_evidence/literature_gap_audit.md`

## Required structured_output fields
`gap_id`, `gap_statement`, `claim_type=gap_claim`, `support_strength`, `source_claim_ids`, `source_matrix_cells`, `supporting_evidence_ids`, `contradicting_evidence_ids`, `corpus_scope`, `gap_type`, `grounding_status`, `confidence`, `novelty_risk`, `overclaim_risk`, `safer_gap_wording`, `required_additional_literature`, `downstream_problem_potential`.

## Required next_input fields
`accepted_gap_candidates`, `counterevidence_summary`, `required_additional_literature`.

## Procedure
1. Review candidate gap evidence.
2. Check counterevidence.
3. Assign `grounding_status`.
4. Write safer corpus-scoped wording.
5. List additional literature required.

## Quality gates
- No supporting evidence means not `grounded`.
- Contradicting evidence means `partially_grounded` or `contradicted`.
- Every gap has safer wording.

## Common failure modes
- "No paper in corpus" becomes "nobody studied".
- Counterevidence hidden.

## Evidence requirements
Gap claims require source claim IDs, matrix cells, evidence IDs, corpus scope, and novelty risk.

## Reviewer-risk requirements
Flag overclaiming, weak evidence, and missing baselines.

## Revision hooks
Downgrade gaps if counterevidence appears.

## Downstream contract
LG06 injects accepted corpus-scoped gaps into existing modules.
