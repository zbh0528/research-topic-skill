# LG04 Evidence Claim Mapping

## Module ID
`LG04_evidence_claim_mapping`

## Module Name
Evidence Claim Mapping

## Purpose
Map evidence objects to domain facts, tensions, gap claims, problem claims, and contribution claims.

## What this module does
- Builds `claims`, `evidence_objects`, `support_links`, and `contradiction_links`.
- Records ungrounded claims and claims requiring verification.

## What this module does not do
- It does not upgrade field-general claims without direct evidence.

## Required input
`paper_cards.json` and `literature_matrix.json`.

## Required output files
- `literature_evidence/evidence_claim_map.json`
- `literature_evidence/evidence_claim_map.md`

## Required structured_output fields
`corpus_id`, `corpus_scope`, `claims`, `evidence_objects`, `support_links`, `contradiction_links`, `ungrounded_claims`, `claims_requiring_verification`, `claim_grounding_summary`.

## Required next_input fields
`key_grounded_claims`, `claims_requiring_verification`, `counterevidence_summary`.

## Procedure
1. Convert extracted claims into evidence objects.
2. Link support and contradiction.
3. Downgrade unsupported field-general claims.
4. Add safer wording.

## Quality gates
- `field_general` requires strong direct evidence.
- Contradicted claims cannot enter final package except as risk.

## Common failure modes
- Missing safer wording.
- Unsupported verified claims.

## Evidence requirements
Each claim needs `claim_type`, `claim_scope`, `grounding_status`, `support_strength`, `supporting_evidence_ids`, `contradicting_evidence_ids`, and `safer_wording`.

## Reviewer-risk requirements
Flag ungrounded claims and hidden counterevidence.

## Revision hooks
Update mappings when modules introduce new claims.

## Downstream contract
LG05 audits candidate gaps from this map.
