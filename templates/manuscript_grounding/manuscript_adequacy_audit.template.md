# Manuscript Adequacy Audit Template

Purpose: plan or audit manuscript structure without generating manuscript prose.

Required boundary:
- Do not invent citations, DOI values, experiment results, or received reviewer comments.
- Mark demo outputs with `is_demo_manuscript_plan`, `requires_real_final_topic_package`, and `requires_real_results` when applicable.

JSON skeleton:
```json
{
  "manuscript_chain_status": "<fill or keep empty with explicit reason>",
  "pass_or_revise_decision": "<fill or keep empty with explicit reason>",
  "pass_count": "<fill or keep empty with explicit reason>",
  "warning_count": "<fill or keep empty with explicit reason>",
  "fail_count": "<fill or keep empty with explicit reason>",
  "passes": "<fill or keep empty with explicit reason>",
  "warnings": "<fill or keep empty with explicit reason>",
  "failures": "<fill or keep empty with explicit reason>"
}
```
