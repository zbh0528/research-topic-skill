# 01 Project Intake

## Module ID

Document ID: `01_project_intake`  
Workspace ID: `00_project_intake`

## Module Name

Project Intake

## Purpose

Convert the user's natural-language research intent into structured `project_context`.

## What This Module Does

- Extract researcher profile.
- Extract research domain.
- Define inclusion boundary.
- Define exclusion boundary.
- Identify target paper type.
- Identify available resources.
- Identify constraints.
- Identify preferred methods.
- Identify avoided directions.
- Generate `project_context`.
- Generate compact `next_input` for `domain_scan`.

## What This Module Does Not Do

- It does not judge novelty.
- It does not select a final topic.
- It does not claim a literature gap.
- It does not design an algorithm.

## Required Input

Natural-language user description of background, target field, method preferences, existing foundation, constraints, and target paper level.

## Required Output Files

- `workspaces/<project_id>/00_project_intake/input.json`
- `workspaces/<project_id>/00_project_intake/output.json`
- `workspaces/<project_id>/00_project_intake/output.md`
- `workspaces/<project_id>/00_project_intake/next_input.json`
- `workspaces/<project_id>/00_project_intake/validation_report.md`

## Required `structured_output` Fields

- `researcher_profile`
- `research_scope`
- `target_output`
- `known_constraints`
- `preferred_methods`
- `avoided_directions`
- `expected_contribution_types`
- `available_resources`
- `uncertainty_log`

## Required `next_input` Fields

- `project_id`
- `research_scope`
- `domain_keywords`
- `inclusion_boundary`
- `exclusion_boundary`
- `preferred_methods`
- `target_output`
- `evidence_policy`
- `trace_context`

## Procedure

1. Extract researcher profile.
2. Extract research domain.
3. Define inclusion boundary.
4. Define exclusion boundary.
5. Identify target paper type.
6. Identify available resources.
7. Identify constraints.
8. Identify preferred methods.
9. Identify avoided directions.
10. Generate `project_context`.
11. Generate `next_input` for `domain_scan`.

## Quality Gates

- Research scope is explicit.
- Excluded directions are recorded.
- Missing inputs are in `uncertainty_log`.
- `next_input` contains only what domain scan needs.
- No literature gap is asserted.

## Common Failure Modes

- Treating a method preference as a research problem.
- Omitting avoided directions.
- Copying all raw user text into `next_input`.
- Hiding missing project constraints.

## Evidence Status Requirements

Use `user_provided` for explicit user facts and preferences. Use `speculative` for guessed target directions. Do not use `verified` unless source evidence is inspectable.

## Reviewer-Risk Requirements

Record risks such as vague scope, algorithm-first framing, unrealistic target venue, or missing literature base.

## Revision Hooks

- Edit `research_scope` to change the field boundary.
- Edit `preferred_methods` to change method direction.
- Edit `avoided_directions` to block unsuitable areas.
- Changing scope affects `02_domain_scan` and downstream modules.

## Downstream Contract

`next_input.json` must be sufficient for `02_domain_scan` to scan the domain without reading full `output.json`.
