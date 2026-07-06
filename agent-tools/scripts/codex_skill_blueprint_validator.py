#!/usr/bin/env python3
"""Validate local Codex Skill blueprints for migration readiness."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FRONTMATTER_ALLOWED_KEYS = {"name", "description"}
SCRIPT_PATTERN = re.compile(r"agent-tools/scripts/([a-zA-Z0-9_]+)\.py")
REFERENCE_PATTERN = re.compile(r"`(知识库/[^`]+\.md)`")
INDEX_ROW_PATTERN = re.compile(r"^\| `([^`]+)` \| ([^|]+) \| ([^|]+) \|$")


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["missing opening frontmatter marker"]
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, ["missing closing frontmatter marker"]
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    extra = sorted(set(fields) - FRONTMATTER_ALLOWED_KEYS)
    missing = sorted(FRONTMATTER_ALLOWED_KEYS - set(fields))
    if extra:
        errors.append(f"frontmatter has unsupported keys: {', '.join(extra)}")
    if missing:
        errors.append(f"frontmatter missing keys: {', '.join(missing)}")
    return fields, errors


def parse_index(root: Path) -> dict[str, list[str]]:
    index_path = root / "codex-skills/index.md"
    if not index_path.exists():
        return {}
    entries: dict[str, list[str]] = {}
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = INDEX_ROW_PATTERN.match(line.strip())
        if not match:
            continue
        skill_name = match.group(1)
        tools = re.findall(r"`([^`]+)`", match.group(3))
        entries[skill_name] = tools
    return entries


def validate_skill(root: Path, skill_path: Path, index_tools: dict[str, list[str]]) -> dict[str, Any]:
    text = skill_path.read_text(encoding="utf-8")
    fields, frontmatter_errors = parse_frontmatter(text)
    skill_name = fields.get("name", skill_path.parent.name)
    errors = list(frontmatter_errors)
    warnings: list[str] = []

    if fields.get("name") and fields["name"] != skill_path.parent.name:
        errors.append("frontmatter name must match skill folder name")
    if len(fields.get("description", "")) < 40:
        warnings.append("description may be too short to trigger reliably")
    if "Use when" not in fields.get("description", ""):
        warnings.append("description should include trigger wording such as 'Use when'")

    referenced_tools = sorted(set(SCRIPT_PATTERN.findall(text)))
    missing_tool_scripts = [
        f"agent-tools/scripts/{tool}.py"
        for tool in referenced_tools
        if not (root / "agent-tools/scripts" / f"{tool}.py").exists()
    ]
    if missing_tool_scripts:
        errors.extend(f"missing referenced tool script: {path}" for path in missing_tool_scripts)

    references = sorted(set(REFERENCE_PATTERN.findall(text)))
    missing_references = [path for path in references if not (root / path).exists()]
    if missing_references:
        errors.extend(f"missing referenced knowledge file: {path}" for path in missing_references)

    index_declared_tools = index_tools.get(skill_name, [])
    missing_from_index = sorted(set(referenced_tools) - set(index_declared_tools))
    index_only = sorted(set(index_declared_tools) - set(referenced_tools))
    if skill_name not in index_tools:
        errors.append("skill missing from codex-skills/index.md")
    if missing_from_index:
        errors.append(f"tools referenced in SKILL.md but missing from index: {', '.join(missing_from_index)}")
    if index_only:
        warnings.append(f"tools listed in index but not explicitly hooked in SKILL.md: {', '.join(index_only)}")

    required_sections = ["## Workflow", "## Tool Hooks", "## Output Shape", "## References"]
    missing_sections = [section for section in required_sections if section not in text]
    if missing_sections:
        errors.append(f"missing required sections: {', '.join(missing_sections)}")

    return {
        "skill": skill_name,
        "path": str(skill_path),
        "is_valid": not errors,
        "frontmatter_keys": sorted(fields),
        "description_length": len(fields.get("description", "")),
        "referenced_tools": referenced_tools,
        "index_declared_tools": index_declared_tools,
        "references": references,
        "missing_references": missing_references,
        "missing_tool_scripts": missing_tool_scripts,
        "errors": errors,
        "warnings": warnings,
    }


def validate(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    index_tools = parse_index(root_path)
    skill_paths = sorted((root_path / "codex-skills").glob("*/SKILL.md"))
    skills = [validate_skill(root_path, path, index_tools) for path in skill_paths]
    invalid = [skill["skill"] for skill in skills if not skill["is_valid"]]
    return {
        "tool": "codex_skill_blueprint_validator",
        "root": str(root_path),
        "skill_count": len(skills),
        "valid_skill_count": len(skills) - len(invalid),
        "invalid_skill_count": len(invalid),
        "is_valid": not invalid,
        "skills": skills,
        "limits": [
            "此工具做静态迁移准备检查，不证明 Skill 在真实对话中表现充分。",
            "工具钩子检查只确认脚本路径存在，不运行每个工具。",
            "Skill 仍需通过 skill_replay_runner、skill_transcript_runner 和人工前向测试。",
        ],
        "next_steps": [
            "fix_invalid_skill_blueprints",
            "run_skill_replay_runner",
            "run_skill_transcript_runner",
            "forward_test_before_installing_live_skills",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to validate.")
    args = parser.parse_args()
    print(json.dumps(validate(args.root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
