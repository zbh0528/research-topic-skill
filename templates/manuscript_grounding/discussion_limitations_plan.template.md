# Discussion Limitations Plan Template

Purpose: plan or audit manuscript structure without generating manuscript prose.

Required boundary:
- Do not invent citations, DOI values, experiment results, or received reviewer comments.
- Mark demo outputs with `is_demo_manuscript_plan`, `requires_real_final_topic_package`, and `requires_real_results` when applicable.

JSON skeleton:
```json
{
  "supported_claims": "<fill or keep empty with explicit reason>",
  "claims_requiring_more_evidence": "<fill or keep empty with explicit reason>",
  "experiment_limitations": "<fill or keep empty with explicit reason>",
  "counterevidence": "<fill or keep empty with explicit reason>",
  "generalization_boundary": "<fill or keep empty with explicit reason>"
}
```
