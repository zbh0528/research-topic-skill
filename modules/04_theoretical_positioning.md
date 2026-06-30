# 04 Theoretical Positioning

## Module ID

Document ID: `04_theoretical_positioning`  
Workspace ID: `03_theoretical_positioning`

## Module Name

Theoretical Positioning

## Purpose

Convert the selected problem into a clear theoretical position and formal optimization-problem description.

## What This Module Does

- Identify optimization problem class.
- Define decision variables.
- Define objective functions.
- Define constraints.
- Identify complexity sources.
- Identify coupling mechanisms.
- Translate problem properties into algorithm requirements.
- Distinguish theoretical, modeling, and algorithmic contribution opportunities.
- Generate `next_input` for contribution argumentation.

## What This Module Does Not Do

- It does not claim a theory contribution without evidence.
- It does not choose implementation details before deriving requirements.
- It does not fabricate mathematical proof or experiment results.

## Required Input

Direct upstream `02_problem_identification/next_input.json`.

## Required Output Files

- `workspaces/<project_id>/03_theoretical_positioning/input.json`
- `workspaces/<project_id>/03_theoretical_positioning/output.json`
- `workspaces/<project_id>/03_theoretical_positioning/output.md`
- `workspaces/<project_id>/03_theoretical_positioning/next_input.json`
- `workspaces/<project_id>/03_theoretical_positioning/validation_report.md`

## Required `structured_output` Fields

- `problem_class`
- `formal_problem_elements`
- `decision_variables`
- `objective_functions`
- `constraints`
- `complexity_sources`
- `coupling_mechanisms`
- `method_implications`
- `theory_to_contribution_bridge`
- `evidence_requirements`
- `uncertainty_log`

`formal_problem_elements` must include `decision_space`, `objective_space`, `constraint_space`, `coupling_structure`, `evaluation_cost`, and `search_difficulty`.

Each `method_implication` must follow:

```text
problem_property -> algorithm_requirement -> possible_mechanism -> evidence_needed
```

## Required `next_input` Fields

- `selected_problem`
- `problem_class`
- `problem_properties`
- `method_implications`
- `theory_to_contribution_bridge`
- `contribution_design_targets`
- `evidence_policy`
- `trace_context`

## Procedure

1. Identify optimization problem class.
2. Define decision variables.
3. Define objective functions.
4. Define constraints.
5. Identify complexity sources.
6. Identify coupling mechanisms.
7. Translate problem properties into algorithm requirements.
8. Distinguish theoretical, modeling, and algorithmic contribution.
9. Generate `next_input` for `contribution_argumentation`.

## Required Topic Coverage

Consider multi-objective optimization, constrained optimization, mixed discrete-continuous optimization, spatial-network coupled optimization, combinatorial optimization, evolutionary computation, Pareto optimization, decomposition, co-evolution, hybrid encoding, repair mechanisms, surrogate-assisted optimization if appropriate, constraint handling, and graph or network topology optimization.

## Quality Gates

- Algorithm requirements are derived from problem properties.
- Coupling mechanisms are explicit.
- Formal elements are not decorative.
- Theory contribution is not claimed without evidence.

## Common Failure Modes

- Starting from a preferred algorithm rather than the selected problem.
- Listing optimization terms without explaining their role.
- Treating modeling choices as verified theory.
- Omitting evidence needed for each method implication.

## Evidence Status Requirements

Use `inferred` for theory positioning derived from selected problem properties. Use `needs_literature_verification` for claims about established theory gaps.

## Reviewer-Risk Requirements

Record risks that theory positioning is too shallow, method implications are generic, or the claimed coupling is not experimentally isolated.

## Revision Hooks

- Edit `problem_class` to change the theoretical frame.
- Edit `method_implications` to change algorithm requirements.
- Changing method implications affects `05_contribution_argumentation`.

## Downstream Contract

`next_input.json` must provide method implications and contribution design targets without exposing full upstream outputs.

## Literature-Grounded Mode Requirements

- Link each `problem_property` to evidence-backed problem records or matrix dimensions.
- Each `method_implication` must state whether it comes from problem property, literature matrix, or theoretical reasoning.
- Mark inferred theory as `inferred` or `needs_literature_verification`.
- Do not write unsupported complexity sources as verified.
- Preserve `corpus_scope` and counterevidence from selected problem.
