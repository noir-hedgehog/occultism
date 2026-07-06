#!/usr/bin/env python3
"""Plan or install validated Codex Skill blueprints into a Codex home."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

import codex_skill_blueprint_validator


def skill_source_paths(root: Path, selected: list[str] | None = None) -> list[Path]:
    paths = sorted((root / "codex-skills").glob("*/SKILL.md"))
    skill_dirs = [path.parent for path in paths]
    if not selected:
        return skill_dirs
    requested = set(selected)
    found = {path.name for path in skill_dirs}
    missing = sorted(requested - found)
    if missing:
        raise ValueError(f"unknown skill blueprint(s): {', '.join(missing)}")
    return [path for path in skill_dirs if path.name in requested]


def same_tree(source: Path, target: Path) -> bool:
    if not target.exists() or not target.is_dir():
        return False
    source_files = sorted(path.relative_to(source) for path in source.rglob("*") if path.is_file())
    target_files = sorted(path.relative_to(target) for path in target.rglob("*") if path.is_file())
    if source_files != target_files:
        return False
    return all((source / rel).read_bytes() == (target / rel).read_bytes() for rel in source_files)


def action_for(source: Path, target: Path, overwrite: bool) -> dict[str, Any]:
    if not target.exists():
        return {"action": "create", "conflict": False, "reason": "target skill is not installed"}
    if same_tree(source, target):
        return {"action": "already_current", "conflict": False, "reason": "target skill matches blueprint"}
    if overwrite:
        return {"action": "overwrite", "conflict": False, "reason": "target skill differs and overwrite is enabled"}
    return {"action": "conflict_existing", "conflict": True, "reason": "target skill differs; rerun with --overwrite after review"}


def copy_skill(source: Path, target: Path, action: str) -> bool:
    if action == "already_current":
        return False
    if action == "overwrite" and target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    return True


def install_plan(
    root: str | Path = ".",
    codex_home: str | Path | None = None,
    skills: list[str] | None = None,
    dry_run: bool = True,
    overwrite: bool = False,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    codex_home_path = Path(codex_home or os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()
    target_root = codex_home_path / "skills"
    validation = codex_skill_blueprint_validator.validate(root_path)
    valid_skills = {item["skill"] for item in validation["skills"] if item["is_valid"]}
    source_dirs = skill_source_paths(root_path, skills)

    actions: list[dict[str, Any]] = []
    for source in source_dirs:
        target = target_root / source.name
        base = action_for(source, target, overwrite)
        is_valid_source = source.name in valid_skills
        copied = False
        errors: list[str] = []
        if not is_valid_source:
            base = {"action": "invalid_blueprint", "conflict": True, "reason": "blueprint validator reported errors"}
        if not dry_run and is_valid_source and not base["conflict"]:
            try:
                copied = copy_skill(source, target, base["action"])
            except Exception as exc:  # pragma: no cover - defensive filesystem path
                base["conflict"] = True
                errors.append(str(exc))
        actions.append(
            {
                "skill": source.name,
                "source": str(source),
                "target": str(target),
                "action": base["action"],
                "reason": base["reason"],
                "conflict": base["conflict"],
                "copied": copied,
                "errors": errors,
            }
        )

    conflicts = [item for item in actions if item["conflict"] or item["errors"]]
    copied_count = sum(1 for item in actions if item["copied"])
    return {
        "tool": "codex_skill_installer",
        "root": str(root_path),
        "codex_home": str(codex_home_path),
        "target_root": str(target_root),
        "dry_run": dry_run,
        "overwrite": overwrite,
        "skill_count": len(actions),
        "copied_count": copied_count,
        "conflict_count": len(conflicts),
        "is_valid": validation["is_valid"] and not conflicts,
        "actions": actions,
        "validation_summary": {
            "skill_count": validation["skill_count"],
            "valid_skill_count": validation["valid_skill_count"],
            "invalid_skill_count": validation["invalid_skill_count"],
            "is_valid": validation["is_valid"],
        },
        "limits": [
            "Default mode is dry-run and does not write to the Codex skills directory.",
            "Existing target skills are only overwritten when --install and --overwrite are both supplied.",
            "Installed skills still depend on this repository path for referenced knowledge and tool commands unless those assets are migrated too.",
        ],
        "next_steps": [
            "review_actions",
            "run_with_install_when_ready",
            "restart_or_refresh_codex_skill_discovery_if_needed",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root containing codex-skills/.")
    parser.add_argument("--codex-home", help="Target Codex home. Defaults to CODEX_HOME or ~/.codex.")
    parser.add_argument("--skill", action="append", help="Install only this skill folder. Can be repeated.")
    parser.add_argument("--install", action="store_true", help="Write skills to the target Codex home. Default is dry-run.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite differing target skill folders when installing.")
    args = parser.parse_args()
    try:
        result = install_plan(
            root=args.root,
            codex_home=args.codex_home,
            skills=args.skill,
            dry_run=not args.install,
            overwrite=args.overwrite,
        )
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
