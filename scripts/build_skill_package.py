#!/usr/bin/env python3
"""Build a self-contained generic research-topic-skill package."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INCLUDE = [
    ".gitignore",
    "SKILL.md",
    "README.md",
    "skill_manifest.json",
    "docs",
    "examples",
    "modules",
    "profiles",
    "schemas",
    "scripts",
    "templates",
]


def copy_path(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc", ".pytest_cache"))
    elif src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def rewrite_skill(path: Path, package_name: str) -> None:
    text = path.read_text()
    text = text.replace("name: windfarm-research-topic-skill", f"name: {package_name}", 1)
    text = text.replace("# Windfarm Research Topic Skill", "# Research Topic Skill", 1)
    text = text.replace("`windfarm-research-topic-skill`", f"`{package_name}`", 1)
    path.write_text(text)


def rewrite_manifest(path: Path, package_name: str) -> None:
    data = json.loads(path.read_text())
    data["name"] = package_name
    data["source_skill_name"] = "windfarm-research-topic-skill"
    data["description"] = "A generic, profile-driven research-topic reasoning skill with literature, experiment, and manuscript grounding."
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--package-name", default="research-topic-skill")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    package_dir = args.output / args.package_name
    if package_dir.exists():
        if not args.overwrite:
            raise SystemExit(f"FAIL package exists; use --overwrite: {package_dir}")
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)
    for rel in INCLUDE:
        copy_path(ROOT / rel, package_dir / rel)
    shutil.rmtree(package_dir / "workspaces", ignore_errors=True)
    rewrite_skill(package_dir / "SKILL.md", args.package_name)
    rewrite_manifest(package_dir / "skill_manifest.json", args.package_name)
    print(f"PASS built skill package: {package_dir}")


if __name__ == "__main__":
    main()
