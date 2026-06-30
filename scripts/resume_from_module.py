#!/usr/bin/env python3
"""Resume a workflow module from the direct upstream next_input.json."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_manifest() -> dict:
    return json.loads((ROOT / "skill_manifest.json").read_text())


def load_state(workspace: Path) -> dict:
    state_path = workspace / "project_state.json"
    if not state_path.exists():
        raise SystemExit(f"project_state.json not found: {state_path}")
    return json.loads(state_path.read_text())


def module_maps() -> tuple[list[dict], dict[str, str]]:
    modules = load_manifest()["modules"]
    aliases: dict[str, str] = {}
    for index, module in enumerate(modules):
        workspace_id = module["workspace_id"]
        doc_id = module["doc_id"]
        aliases[workspace_id] = workspace_id
        aliases[doc_id] = workspace_id
        aliases[str(index)] = workspace_id
        aliases[f"{index:02d}"] = workspace_id
        aliases[workspace_id.split("_", 1)[1]] = workspace_id
        aliases[doc_id.split("_", 1)[1]] = workspace_id
    return modules, aliases


def resolve_module(module_id: str) -> tuple[str, str | None]:
    _, aliases = module_maps()
    if module_id not in aliases:
        valid = ", ".join(sorted(aliases))
        raise SystemExit(f"unknown module id: {module_id}; valid aliases include: {valid}")
    resolved = aliases[module_id]
    return resolved, None if module_id == resolved else f"mapped {module_id} -> {resolved}"


def json_nonempty(path: Path) -> bool:
    if not path.exists() or path.stat().st_size == 0:
        return False
    try:
        return json.loads(path.read_text()) not in ({}, [])
    except json.JSONDecodeError:
        return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--module-id", required=True)
    parser.add_argument("--overwrite-current", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace if args.workspace.is_absolute() else ROOT / args.workspace
    if not workspace.exists():
        raise SystemExit(f"workspace not found: {workspace}")

    modules, _ = module_maps()
    module_order = [m["workspace_id"] for m in modules]
    target, mapping_note = resolve_module(args.module_id)
    if target not in module_order:
        raise SystemExit(f"target module not in manifest order: {target}")

    target_dir = workspace / target
    if not target_dir.exists():
        raise SystemExit(f"target module directory not found: {target_dir}")

    target_index = module_order.index(target)
    state = load_state(workspace)

    if mapping_note:
        print(f"INFO {mapping_note}")

    if target_index == 0:
        state["current_module"] = target
        state.setdefault("history", []).append({"timestamp": now(), "event": "resume_first_module", "module_id": target})
        (workspace / "project_state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
        print(f"PASS current module set to {target}; no upstream next_input required")
        return

    upstream = module_order[target_index - 1]
    upstream_next = workspace / upstream / "next_input.json"
    if not upstream_next.exists():
        raise SystemExit(f"direct upstream next_input.json not found: {upstream_next}")
    upstream_payload = json.loads(upstream_next.read_text())
    if upstream_payload == {}:
        raise SystemExit(f"direct upstream next_input.json is empty: {upstream_next}")

    target_input = target_dir / "input.json"
    target_output = target_dir / "output.json"
    if json_nonempty(target_output) and not args.overwrite_current:
        raise SystemExit(f"current module output.json is non-empty: {target_output}; pass --overwrite-current")
    if json_nonempty(target_input) and not args.overwrite_current:
        raise SystemExit(f"current module input.json is non-empty: {target_input}; pass --overwrite-current")

    input_payload = {
        "module_id": target,
        "source_module_id": upstream,
        "source_next_input_path": str(upstream_next),
        "loaded_at": now(),
        "payload": upstream_payload,
    }
    target_input.write_text(json.dumps(input_payload, indent=2, ensure_ascii=False) + "\n")

    state["current_module"] = target
    state.setdefault("history", []).append(
        {
            "timestamp": now(),
            "event": "resume_from_module",
            "module_id": target,
            "direct_upstream_module_id": upstream,
            "source_next_input_path": str(upstream_next),
            "overwrite_current": args.overwrite_current,
        }
    )
    (workspace / "project_state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"PASS resumed {target} from direct upstream {upstream}")


if __name__ == "__main__":
    main()
