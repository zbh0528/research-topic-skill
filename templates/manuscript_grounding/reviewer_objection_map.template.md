# Reviewer Objection Map Template

Purpose: plan or audit manuscript structure without generating manuscript prose.

Required boundary:
- Do not invent citations, DOI values, experiment results, or received reviewer comments.
- Mark demo outputs with `is_demo_manuscript_plan`, `requires_real_final_topic_package`, and `requires_real_results` when applicable.

JSON skeleton:
```json
{
  "reviewer_objections": "<fill or keep empty with explicit reason>",
  "objection_summary": "<fill or keep empty with explicit reason>",
  "high_severity_objections": "<fill or keep empty with explicit reason>",
  "assumptions": "<fill or keep empty with explicit reason>",
  "limitations": "<fill or keep empty with explicit reason>"
}
```
