#!/usr/bin/env python3
"""Validate the agent tool runtime registry before registration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import agent_tool_registry_builder


EXPECTED_BOOTSTRAP_PREFIX = ["mystic_intake_triage", "agent_workflow_router", "mystic_output_lint"]
REQUIRED_SKILL_TOOLS = ["mystic_intake_triage", "mystic_output_lint"]


def entry_by_name(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {entry["name"]: entry for entry in entries}


def validate_registry(registry: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    entries = registry["entries"]
    by_name = entry_by_name(entries)
    order = registry["registration_order"]
    if len(order) != len(entries):
        errors.append("registration_order_count_mismatch")
    if set(order) != set(by_name):
        errors.append("registration_order_tool_mismatch")
    if order[: len(EXPECTED_BOOTSTRAP_PREFIX)] != EXPECTED_BOOTSTRAP_PREFIX:
        errors.append("bootstrap_prefix_mismatch")
    if registry["safety_bootstrap"][: len(EXPECTED_BOOTSTRAP_PREFIX)] != EXPECTED_BOOTSTRAP_PREFIX:
        errors.append("safety_bootstrap_prefix_mismatch")
    for bootstrap in registry["safety_bootstrap"]:
        if bootstrap not in by_name:
            errors.append(f"missing_bootstrap_{bootstrap}")
    for name in order:
        entry = by_name.get(name)
        if not entry:
            continue
        if not entry["command"] or entry["command"][0] != "python3":
            errors.append(f"invalid_command_{name}")
        if "professional_boundary_required" not in entry["safety_tags"]:
            errors.append(f"missing_boundary_tag_{name}")
    for domain, names in registry["by_domain"].items():
        for name in names:
            if name not in by_name:
                errors.append(f"domain_index_missing_tool_{domain}_{name}")
            elif domain not in by_name[name]["domains"]:
                errors.append(f"domain_index_mismatch_{domain}_{name}")
    skill_results: list[dict[str, Any]] = []
    for skill, names in registry["by_skill"].items():
        if skill == "unassigned":
            continue
        missing = [tool for tool in REQUIRED_SKILL_TOOLS if tool not in names]
        invalid = [name for name in names if name not in by_name]
        skill_results.append({"skill": skill, "is_valid": not missing and not invalid, "missing_required_tools": missing, "invalid_tools": invalid})
        for tool in missing:
            errors.append(f"skill_missing_{skill}_{tool}")
        for tool in invalid:
            errors.append(f"skill_invalid_tool_{skill}_{tool}")
    return errors, skill_results


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    registry = agent_tool_registry_builder.build(root_path)
    errors, skill_results = validate_registry(registry)
    failed_skills = [item for item in skill_results if not item["is_valid"]]
    return {
        "tool": "agent_tool_registry_validator",
        "root": str(root_path),
        "is_valid": bool(registry["is_valid"]) and not errors,
        "registry_status": registry["registry_status"],
        "tool_count": registry["tool_count"],
        "domain_count": registry["domain_count"],
        "skill_count": registry["skill_count"],
        "error_count": len(errors),
        "errors": errors,
        "bootstrap_prefix": registry["registration_order"][: len(EXPECTED_BOOTSTRAP_PREFIX)],
        "safety_bootstrap": registry["safety_bootstrap"],
        "skill_results": skill_results,
        "failed_skill_count": len(failed_skills),
        "limits": [
            "此验证只检查注册表结构，不注册或执行工具。",
            "通过验证不代表 runtime 命令执行器已完成权限隔离。",
            "Skill 仍需通过回放和真实匿名 transcript 流程继续验证。",
        ],
        "next_steps": [
            "fix_registry_errors_if_any",
            "bind_runtime_registration_to_validated_order",
            "run_agent_runtime_dry_run_runner_after_registration_binding",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Agent Tool Registry Validation",
        "",
        "本页验证 runtime 工具注册表是否适合注册：注册顺序、索引、bootstrap 和 Skill 必备工具必须一致。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| Valid | {result['is_valid']} |",
        f"| Tool | {result['tool_count']} |",
        f"| Domain group | {result['domain_count']} |",
        f"| Skill group | {result['skill_count']} |",
        f"| Error | {result['error_count']} |",
        "",
        "## Bootstrap Prefix",
        "",
    ]
    for tool in result["bootstrap_prefix"]:
        lines.append(f"- `{tool}`")
    lines.extend(["", "## Skill Checks", "", "| Skill | Valid | Missing Required Tools | Invalid Tools |", "| --- | --- | --- | --- |"])
    for item in result["skill_results"]:
        missing = ", ".join(f"`{tool}`" for tool in item["missing_required_tools"]) or "-"
        invalid = ", ".join(f"`{tool}`" for tool in item["invalid_tools"]) or "-"
        lines.append(f"| `{item['skill']}` | {item['is_valid']} | {missing} | {invalid} |")
    if result["errors"]:
        lines.extend(["", "## Errors", ""])
        for error in result["errors"]:
            lines.append(f"- `{error}`")
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/Agent工具注册表验证.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "Agent工具注册表验证.md"
        target.write_text(render_markdown(result), encoding="utf-8")
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
