#!/usr/bin/env python3
"""Build a runtime registry from validated agent tool definitions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import agent_tool_definition_exporter
import agent_tool_definition_validator


PRIORITY_PREFIXES = [
    "mystic_intake_triage",
    "agent_workflow_router",
    "mystic_output_lint",
    "ritual_safety_check",
    "bazi_ziwei_intake_guard",
    "astrology_compatibility_guard",
    "fengshui_school_guard",
    "yijing_question_guard",
    "qimen_method_guard",
]


def registration_priority(name: str, metadata: dict[str, Any]) -> int:
    if name in PRIORITY_PREFIXES:
        return PRIORITY_PREFIXES.index(name)
    if "runtime_infrastructure" in metadata.get("safety_tags", []):
        return 20
    if name.endswith("_guard") or name.endswith("_check"):
        return 30
    if metadata.get("skills"):
        return 50
    return 80


def registry_entry(definition: dict[str, Any]) -> dict[str, Any]:
    metadata = definition["metadata"]
    return {
        "name": definition["name"],
        "description": definition["description"],
        "command": definition["command"],
        "schema_path": metadata["schema_path"],
        "script_path": metadata["script_path"],
        "spec_path": metadata["spec_path"],
        "domains": metadata["domains"],
        "skills": metadata["skills"],
        "safety_tags": metadata["safety_tags"],
        "registration_priority": registration_priority(definition["name"], metadata),
    }


def group_by(entries: list[dict[str, Any]], key: str) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for entry in entries:
        values = entry.get(key, []) or ["unassigned"]
        for value in values:
            grouped.setdefault(value, []).append(entry["name"])
    return {name: sorted(items) for name, items in sorted(grouped.items())}


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    validation = agent_tool_definition_validator.build(root_path)
    export = agent_tool_definition_exporter.build(root_path)
    entries = [registry_entry(definition) for definition in export["definitions"]]
    ordered = sorted(entries, key=lambda item: (item["registration_priority"], item["name"]))
    return {
        "tool": "agent_tool_registry_builder",
        "root": str(root_path),
        "is_valid": bool(validation["is_valid"]) and len(entries) == validation["valid_definition_count"],
        "registry_status": "ready_for_runtime_registration" if validation["is_valid"] else "blocked_by_definition_validation",
        "tool_count": len(entries),
        "domain_count": len(group_by(entries, "domains")),
        "skill_count": len(group_by(entries, "skills")) - (1 if "unassigned" in group_by(entries, "skills") else 0),
        "registration_order": [entry["name"] for entry in ordered],
        "entries": ordered,
        "by_domain": group_by(entries, "domains"),
        "by_skill": group_by(entries, "skills"),
        "safety_bootstrap": [name for name in PRIORITY_PREFIXES if any(entry["name"] == name for entry in entries)],
        "runtime_contract": {
            "register": "Register entries in registration_order.",
            "execute": "Invoke command with schema-validated input and preserve JSON stdout.",
            "guard": "Do not call domain tools when agent_workflow_router returns paused or blocked status.",
            "lint": "Run mystic_output_lint or equivalent before user-visible mystic output.",
        },
        "limits": [
            "此 registry 不启动工具服务，只提供注册表。",
            "注册顺序不能替代 runtime 权限隔离和命令执行沙箱。",
            "外部证据未完成前，只能用于 dry-run 或内部试运行。",
        ],
        "next_steps": [
            "register_tools_in_runtime_using_registration_order",
            "bind_command_executor_to_registry_entries",
            "run_agent_runtime_dry_run_runner_after_registration",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Agent Tool Registry",
        "",
        "本页把已验证的 agent tool definitions 组织成 runtime 注册表，包括注册顺序、按流派索引、按 Skill 索引和安全启动工具。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 状态 | `{result['registry_status']}` |",
        f"| Tool | {result['tool_count']} |",
        f"| Domain group | {result['domain_count']} |",
        f"| Skill group | {result['skill_count']} |",
        "",
        "## Runtime Contract",
        "",
    ]
    for key, value in result["runtime_contract"].items():
        lines.append(f"- `{key}`：{value}")
    lines.extend(["", "## Safety Bootstrap", ""])
    for name in result["safety_bootstrap"]:
        lines.append(f"- `{name}`")
    lines.extend(["", "## Registration Order", ""])
    for index, name in enumerate(result["registration_order"], start=1):
        lines.append(f"{index}. `{name}`")
    lines.extend(["", "## Domain Index", ""])
    for domain, names in result["by_domain"].items():
        lines.append(f"### {domain}")
        for name in names:
            lines.append(f"- `{name}`")
        lines.append("")
    lines.extend(["## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/Agent工具注册表.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "Agent工具注册表.md"
        target.write_text(render_markdown(result), encoding="utf-8")
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
