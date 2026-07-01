from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(f"command failed: {' '.join(args)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result


def test_profiles_validate() -> None:
    result = run_cmd([sys.executable, "scripts/validate_profiles.py"])
    assert "PASS validated" in result.stdout


def test_build_generic_skill_package(tmp_path: Path) -> None:
    result = run_cmd([sys.executable, "scripts/build_skill_package.py", "--output", str(tmp_path), "--overwrite"])
    assert "PASS built skill package" in result.stdout
    package = tmp_path / "research-topic-skill"
    skill = (package / "SKILL.md").read_text()
    manifest = json.loads((package / "skill_manifest.json").read_text())
    assert "name: research-topic-skill" in skill
    assert manifest["name"] == "research-topic-skill"
    assert (package / "README.en.md").exists()
    assert (package / "profiles" / "generic-research" / "profile.json").exists()
    assert not (package / "workspaces").exists()
