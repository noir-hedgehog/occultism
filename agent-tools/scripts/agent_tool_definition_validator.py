#!/usr/bin/env python3
"""Validate exported agent tool definitions before runtime registration."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import agent_tool_definition_exporter


TOOL_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,63}$")
REQUIRED_METADATA = ["script_path", "schema_path", "spec_path", "domains", "skills", "safety_tags"]


def validate_definition(definition: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    name = str(definition.get("name", ""))
    metadata = definition.get("metadata", {})
    schema = definition.get("input_schema", {})
    command = definition.get("command", [])
    if not TOOL_NAME_RE.match(name):
        errors.append("invalid_name")
    if not str(definition.get("description", "")).strip():
        errors.append("missing_description")
    if not isinstance(schema, dict) or schema.get("type") != "object":
        errors.append("input_schema_not_object")
    if not isinstance(command, list) or len(command) < 2 or command[0] != "python3":
        errors.append("invalid_command")
    for key in REQUIRED_METADATA:
        if key not in metadata:
            errors.append(f"missing_metadata_{key}")
    for key in ["script_path", "schema_path", "spec_path"]:
        path = metadata.get(key)
        if not path or not (root / str(path)).exists():
            errors.append(f"missing_file_{key}")
    if metadata.get("script_path") and len(command) >= 2 and command[1] != metadata["script_path"]:
        errors.append("command_script_mismatch")
    if not metadata.get("domains"):
        errors.append("missing_domains")
    if not metadata.get("safety_tags"):
        errors.append("missing_safety_tags")
    if "professional_boundary_required" not in metadata.get("safety_tags", []):
        errors.append("missing_professional_boundary_tag")
    return errors


def validate_openai_tool(tool: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if tool.get("type") != "function":
        errors.append("invalid_type")
    function = tool.get("function", {})
    if not TOOL_NAME_RE.match(str(function.get("name", ""))):
        errors.append("invalid_function_name")
    if not str(function.get("description", "")).strip():
        errors.append("missing_function_description")
    parameters = function.get("parameters", {})
    if not isinstance(parameters, dict) or parameters.get("type") != "object":
        errors.append("function_parameters_not_object")
    return errors


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    export = agent_tool_definition_exporter.build(root_path)
    definitions = export["definitions"]
    openai_tools = export["openai_tools"]
    names = [definition["name"] for definition in definitions]
    duplicate_names = sorted({name for name in names if names.count(name) > 1})
    definition_results: list[dict[str, Any]] = []
    for definition in definitions:
        errors = validate_definition(definition, root_path)
        if definition["name"] in duplicate_names:
            errors.append("duplicate_name")
        definition_results.append(
            {
                "name": definition["name"],
                "is_valid": not errors,
                "errors": errors,
                "schema_title": definition["input_schema"].get("title", ""),
                "domains": definition["metadata"].get("domains", []),
                "safety_tags": definition["metadata"].get("safety_tags", []),
            }
        )
    openai_results = []
    for tool in openai_tools:
        errors = validate_openai_tool(tool)
        openai_results.append({"name": tool.get("function", {}).get("name", ""), "is_valid": not errors, "errors": errors})
    failed_definitions = [item for item in definition_results if not item["is_valid"]]
    failed_openai = [item for item in openai_results if not item["is_valid"]]
    return {
        "tool": "agent_tool_definition_validator",
        "root": str(root_path),
        "is_valid": bool(export["is_valid"]) and not failed_definitions and not failed_openai,
        "definition_count": len(definition_results),
        "valid_definition_count": len(definition_results) - len(failed_definitions),
        "failed_definition_count": len(failed_definitions),
        "openai_tool_count": len(openai_results),
        "valid_openai_tool_count": len(openai_results) - len(failed_openai),
        "failed_openai_tool_count": len(failed_openai),
        "duplicate_names": duplicate_names,
        "definition_results": definition_results,
        "openai_results": openai_results,
        "limits": [
            "此验证只检查注册形状和本地文件引用，不执行工具。",
            "schema 为 object 不代表业务语义充分，仍需工具内部验证和 runtime dry-run。",
            "OpenAI-style 形状有效不表示已绑定真实命令执行器。",
        ],
        "next_steps": [
            "fix_failed_definition_results",
            "bind_validated_definitions_to_runtime_executor",
            "run_agent_runtime_dry_run_runner_after_binding",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Agent Tool Definition Validation",
        "",
        "本页验证导出的 agent tool definitions 是否适合进入 runtime 注册层。它只检查注册形状和本地引用，不执行工具。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| Definition | {result['valid_definition_count']}/{result['definition_count']} |",
        f"| OpenAI-style tool | {result['valid_openai_tool_count']}/{result['openai_tool_count']} |",
        f"| 失败 definition | {result['failed_definition_count']} |",
        f"| 失败 OpenAI tool | {result['failed_openai_tool_count']} |",
        "",
        "## Definition 检查",
        "",
        "| Tool | Valid | Domains | Safety Tags | Errors |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in result["definition_results"]:
        domains = ", ".join(f"`{domain}`" for domain in item["domains"])
        safety = ", ".join(f"`{tag}`" for tag in item["safety_tags"])
        errors = ", ".join(f"`{error}`" for error in item["errors"]) or "-"
        lines.append(f"| `{item['name']}` | {item['is_valid']} | {domains} | {safety} | {errors} |")
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/Agent工具定义验证.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "Agent工具定义验证.md"
        target.write_text(render_markdown(result), encoding="utf-8")
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
