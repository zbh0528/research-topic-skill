# LG06 Grounded Pipeline Integration

## Module ID
`LG06_grounded_pipeline_integration`

## Module Name
Grounded Pipeline Integration

## Purpose
Inject literature grounding into modules 01-07 without breaking loose coupling.

## What this module does
- Injects `evidence_claim_map.json` into domain scan through compact `evidence_context`.
- Injects `literature_gap_audit.json` into problem identification.
- Requires theoretical positioning, contribution argumentation, audit, and final package to preserve evidence links.

## What this module does not do
- It does not pass full paper text through `next_input.json`.

## Required input
`literature_grounding_report.json` and direct upstream `next_input.json`.

## Required output files
Existing module output files plus `claim_grounding_audit.json` and `.md`.

## Required structured_output fields
`evidence_context`, `grounded_claims`, `claim_grounding_risks`, `counterevidence`, `corpus_scope`.

## Required next_input fields
`evidence_context` in compact form.

## Procedure
1. Add `evidence_context` to project intake `next_input`.
2. Require domain tensions to link claim and evidence IDs.
3. Require selected problems to link accepted gap IDs.
4. Require contributions to link evidence, problem, and theory IDs.
5. Audit evidence gaps.
6. Output final Evidence Traceability Table.

## Quality gates
- No full paper text in `next_input`.
- No grounded claim without evidence ID.
- No final claim hiding counterevidence.

## Common failure modes
- Over-expanded `next_input`.
- Evidence links dropped between modules.

## Evidence requirements
Use:

```json
{
  "corpus_id": "...",
  "corpus_scope": "...",
  "paper_count": 0,
  "key_grounded_claims": [],
  "candidate_gap_claims": [],
  "counterevidence_summary": [],
  "claims_requiring_verification": [],
  "evidence_policy": {},
  "trace_context": {}
}
```

## Reviewer-risk requirements
Flag unsupported verified claims, hidden counterevidence, title-only inference, synthetic misuse, and field-general claims without evidence.

## Revision hooks
Rerun `audit_claim_grounding.py --strict` after any evidence-linked module edit.

## Downstream contract
Existing modules still read only direct upstream `next_input.json`.
