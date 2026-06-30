# 02 Domain Scan

## Module ID

Document ID: `02_domain_scan`  
Workspace ID: `01_domain_scan`

## Module Name

Domain Scan

## Purpose

Generate a bounded domain map and candidate research tensions from `project_context.next_input`.

## What This Module Does

- Define domain boundaries.
- Decompose the field into research streams.
- Build a method-problem matrix.
- Identify objectives and constraints.
- Identify coupling relations between wind farm layout and cable routing.
- Identify saturated, active, and underexplored areas.
- Generate domain tensions.
- Mark `evidence_status` for every important claim.
- Generate `next_input` for problem identification.

## What This Module Does Not Do

- It does not choose the final research problem.
- It does not fabricate literature findings.
- It does not claim a gap is verified without evidence.
- It does not design contribution claims.

## Required Input

Direct upstream `00_project_intake/next_input.json`.

## Required Output Files

- `workspaces/<project_id>/01_domain_scan/input.json`
- `workspaces/<project_id>/01_domain_scan/output.json`
- `workspaces/<project_id>/01_domain_scan/output.md`
- `workspaces/<project_id>/01_domain_scan/next_input.json`
- `workspaces/<project_id>/01_domain_scan/validation_report.md`

## Required `structured_output` Fields

- `domain_boundaries`
- `research_streams`
- `method_problem_matrix`
- `objective_constraint_map`
- `coupling_map`
- `domain_tensions`
- `saturated_areas`
- `active_areas`
- `underexplored_areas`
- `evidence_requirements`
- `uncertainty_log`

Each `domain_tension` must include `tension_id`, `tension_statement`, `source_streams`, `why_it_matters`, `possible_gap`, `evidence_status`, `evidence_needed`, and `downstream_problem_potential`.

## Required `next_input` Fields

- `candidate_tensions`
- `domain_boundaries`
- `method_problem_matrix_summary`
- `objective_constraint_summary`
- `coupling_summary`
- `evidence_policy`
- `trace_context`

## Procedure

1. Define domain boundaries.
2. Decompose the field into research streams.
3. Build a method-problem matrix.
4. Identify typical objectives and constraints.
5. Identify coupling relations between layout and cabling.
6. Identify saturated, active, and underexplored areas.
7. Generate domain tensions.
8. Mark `evidence_status`.
9. Generate `next_input` for `problem_identification`.

## Required Topic Coverage

Consider wind farm layout optimization, cable routing optimization, joint layout-cabling optimization, evolutionary computation, multi-objective optimization, constrained optimization, wake effect, cable cost, electrical losses, network topology, spatial-network coupling, offshore wind farm scope, radial or tree-like collection topology, cable capacity constraints, substation connection constraints, and Pareto trade-off analysis.

## Quality Gates

- Domain boundaries are explicit.
- Every tension has an evidence status.
- Literature-state claims default to `needs_literature_verification` without real literature input.
- `next_input` passes only candidate tensions and compact summaries.

## Common Failure Modes

- Fabricating prior-work conclusions.
- Treating broad field descriptions as gaps.
- Ignoring layout-cabling coupling.
- Passing full domain scan output downstream.

## Evidence Status Requirements

Use `needs_literature_verification` for claims about saturated, active, or underexplored areas unless verified sources are provided.

## Reviewer-Risk Requirements

Record risks that the gap may be too broad, already studied, weakly connected to optimization theory, or not distinct from sequential layout-then-cabling workflows.

## Revision Hooks

- Edit `domain_boundaries` to adjust scope.
- Edit `domain_tensions` to change downstream candidate problems.
- Changing `candidate_tensions` affects `03_problem_identification`.

## Downstream Contract

`next_input.json` must provide candidate tensions and compact domain summaries only.
