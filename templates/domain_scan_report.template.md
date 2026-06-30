# Domain Scan Report

## Metadata

- project_id: `{{project_id}}`
- module_id: `{{module_id}}`
- input_source: `{{input_source}}`
- upstream_next_input_path: `{{upstream_next_input_path}}`
- validation_status: `{{validation_status}}`

## domain_boundaries

{{domain_boundaries}}

## research_streams

{{research_streams}}

## method_problem_matrix

{{method_problem_matrix}}

## objective_constraint_map

{{objective_constraint_map}}

## coupling_map

{{coupling_map}}

## domain_tensions

| tension_id | tension_statement | possible_gap | evidence_status | evidence_needed |
| --- | --- | --- | --- | --- |
| `{{domain_tension_id}}` | {{tension_statement}} | {{possible_gap}} | {{evidence_status}} | {{evidence_needed}} |

## saturated_areas

{{saturated_areas}}

## active_areas

{{active_areas}}

## underexplored_areas

{{underexplored_areas}}

## Evidence Partitions

### facts

{{facts}}

### inferences

{{inferences}}

### assumptions

{{assumptions}}

### to_verify

{{to_verify}}

## uncertainty_log

{{uncertainty_log}}

## reviewer_risks

{{reviewer_risks}}

## revision_hooks

{{revision_hooks}}

## trace_context

{{trace_context}}

## next_input Summary

{{next_input_summary}}

If no real literature search was performed, mark prior-work and gap statements as `needs_literature_verification`.
