#!/usr/bin/env python3
"""Export wrapper metadata into agent tool definitions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import agent_tool_wrapper_manifest_builder


def load_schema(root: Path, schema_path: str) -> dict[str, Any]:
    path = root / schema_path
    if not path.exists():
        return {"type": "object", "properties": {}, "additionalProperties": True}
    return json.loads(path.read_text(encoding="utf-8"))


def compact_description(wrapper: dict[str, Any]) -> str:
    tags = ", ".join(wrapper["safety_tags"])
    domains = ", ".join(wrapper["domains"])
    return f"{wrapper['description']} Domains: {domains}. Safety tags: {tags}."


def definition_for_wrapper(root: Path, wrapper: dict[str, Any]) -> dict[str, Any]:
    schema = load_schema(root, wrapper["input_schema_path"])
    return {
        "name": wrapper["name"],
        "description": compact_description(wrapper),
        "input_schema": schema,
        "command": wrapper["command"],
        "metadata": {
            "script_path": wrapper["script_path"],
            "schema_path": wrapper["input_schema_path"],
            "spec_path": wrapper["spec_path"],
            "domains": wrapper["domains"],
            "skills": wrapper["skills"],
            "safety_tags": wrapper["safety_tags"],
        },
    }


def openai_tool_for(definition: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": definition["name"],
            "description": definition["description"],
            "parameters": definition["input_schema"],
        },
    }


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    wrapper_manifest = agent_tool_wrapper_manifest_builder.build(root_path)
    definitions = [
        definition_for_wrapper(root_path, wrapper)
        for wrapper in wrapper_manifest["wrappers"]
        if wrapper["status"] == "wrappable"
    ]
    openai_tools = [openai_tool_for(definition) for definition in definitions]
    return {
        "tool": "agent_tool_definition_exporter",
        "root": str(root_path),
        "is_valid": bool(wrapper_manifest["is_valid"]) and len(definitions) == wrapper_manifest["wrappable_count"],
        "definition_count": len(definitions),
        "openai_tool_count": len(openai_tools),
        "source_wrapper_count": wrapper_manifest["wrapper_count"],
        "definitions": definitions,
        "openai_tools": openai_tools,
        "limits": [
            "此导出器生成工具定义，不执行工具、不启动 server。",
            "OpenAI-style tools 只携带 schema；实际命令执行仍需 runtime wrapper 绑定 metadata.command。",
            "导出的 schema 不替代工具内部安全守门和输出 lint。",
        ],
        "next_steps": [
            "bind_definitions_to_runtime_command_executor",
            "run_agent_runtime_dry_run_runner_after_binding",
            "forward_test_with_representative_requests_before_public_release",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Agent Tool Definition Export",
        "",
        "本页把 wrapper manifest 导出为 agent tool definition 和 OpenAI-style function tool 形状。它不执行工具，也不表示已经启动 runtime server。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| Definition | {result['definition_count']} |",
        f"| OpenAI-style tool | {result['openai_tool_count']} |",
        f"| 来源 wrapper | {result['source_wrapper_count']} |",
        "",
        "## 定义清单",
        "",
        "| Tool | Script | Schema | Domains | Safety Tags |",
        "| --- | --- | --- | --- | --- |",
    ]
    for definition in result["definitions"]:
        metadata = definition["metadata"]
        domains = ", ".join(f"`{item}`" for item in metadata["domains"])
        safety = ", ".join(f"`{item}`" for item in metadata["safety_tags"])
        lines.append(
            f"| `{definition['name']}` | `{metadata['script_path']}` | [{Path(metadata['schema_path']).name}](../{metadata['schema_path']}) | {domains} | {safety} |"
        )
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["json", "markdown", "openai"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/Agent工具定义导出.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "Agent工具定义导出.md"
        target.write_text(render_markdown(result), encoding="utf-8")
    if args.format == "markdown":
        print(render_markdown(result))
    elif args.format == "openai":
        print(json.dumps(result["openai_tools"], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
