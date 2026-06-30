# Manuscript Grounding Workflow

v0.4.0 adds manuscript-structure and reviewer-response planning on top of v0.1-v0.3. It converts a topic package, literature grounding, and experiment validation plan into a manuscript blueprint, section argument map, paragraph claim plan, citation requirements, result placeholders, limitation plan, reviewer-objection map, and adequacy audit.

This workflow does not generate a final paper. Draft/demo workspaces must keep `is_demo_manuscript_plan: true`, `requires_real_final_topic_package: true`, and `requires_real_results: true`.

Core commands:

```bash
python3 scripts/build_manuscript_blueprint.py --workspace workspaces/<project_id> --overwrite --demo-if-missing
python3 scripts/validate_manuscript_plan.py --workspace workspaces/<project_id> --strict
python3 scripts/audit_manuscript_claims.py --workspace workspaces/<project_id> --strict
python3 scripts/generate_reviewer_response_plan.py --workspace workspaces/<project_id> --overwrite
python3 scripts/generate_manuscript_checklist.py --workspace workspaces/<project_id>
python3 scripts/validate_outputs.py --workspace workspaces/<project_id> --manuscript-grounded --strict-manuscript
```

Complete-chain acceptance requires a real final topic package, complete manuscript traceability, verified citation links, and real result evidence. Draft/demo workspaces should fail `--require-complete-manuscript-chain` with explicit reasons.
