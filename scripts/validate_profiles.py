#!/usr/bin/env python3
"""Validate research-topic-skill profile files."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "profiles"


def main() -> None:
    schema_path = PROFILES / "profile.schema.json"
    if not schema_path.exists():
        raise SystemExit(f"FAIL missing profile schema: {schema_path}")
    schema = json.loads(schema_path.read_text())
    required = set(schema["required"])
    failures: list[str] = []
    profile_paths = sorted(PROFILES.glob("*/profile.json"))
    if not profile_paths:
        failures.append("FAIL no profile.json files found")
    ids: list[str] = []
    for path in profile_paths:
        data = json.loads(path.read_text())
        missing = sorted(required - data.keys())
        if missing:
            failures.append(f"FAIL {path}: missing {', '.join(missing)}")
        if data.get("profile_id") != path.parent.name:
            failures.append(f"FAIL {path}: profile_id must match directory name")
        ids.append(str(data.get("profile_id", "")))
        for key in ["domain_terms", "problem_structures", "method_families", "baseline_families", "metric_families", "reviewer_risks", "claim_boundaries"]:
            value = data.get(key)
            if not isinstance(value, list) or not value:
                failures.append(f"FAIL {path}: {key} must be a non-empty list")
            elif not all(isinstance(item, str) and item.strip() for item in value):
                failures.append(f"FAIL {path}: {key} must contain non-empty strings")
    duplicates = sorted({pid for pid in ids if ids.count(pid) > 1})
    if duplicates:
        failures.append(f"FAIL duplicate profile_id: {', '.join(duplicates)}")
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
    print(f"PASS validated {len(profile_paths)} profiles")


if __name__ == "__main__":
    main()
