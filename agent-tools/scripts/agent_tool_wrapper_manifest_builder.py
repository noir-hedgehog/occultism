#!/usr/bin/env python3
"""Build runtime wrapper metadata for exposing mystic scripts as agent tools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import tool_manifest_builder


SAFETY_TAGS_BY_DOMAIN = {
    "ritual": ["dangerous_materials_guarded", "low_risk_only"],
    "mingli": ["birth_data_minimization", "no_fatalism"],
    "astrology": ["birth_data_minimization", "third_party_privacy"],
    "fengshui": ["real_world_safety_first", "no_deterministic_disaster_claims"],
    "naming": ["no_fate_or_compliance_guarantee"],
}


def load_schema_title(root: Path, schema_path: str) -> str:
    path = root / schema_path
    if not path.exists():
        return ""
    try:
        return str(json.loads(path.read_text(encoding="utf-8")).get("title", ""))
    except json.JSONDecodeError:
        return ""


def safety_tags(domains: list[str]) -> list[str]:
    tags = {"symbolic_interpretation_only", "professional_boundary_required"}
    for domain in domains:
        tags.update(SAFETY_TAGS_BY_DOMAIN.get(domain, []))
    if "shared" in domains:
        tags.add("runtime_infrastructure")
    return sorted(tags)


def wrapper_for_tool(root: Path, tool: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": tool["name"],
        "description": tool["summary"] or tool["name"],
        "command": ["python3", tool["script"]],
        "script_path": tool["script"],
        "input_schema_path": tool["schema"],
        "input_schema_title": load_schema_title(root, tool["schema"]),
        "spec_path": tool["spec"],
        "domains": tool["domains"],
        "skills": tool["skills"],
        "safety_tags": safety_tags(tool["domains"]),
        "status": "wrappable" if tool["status"] == "ready" else "blocked",
        "wrapper_notes": [
            "Use the JSON schema as the external input contract.",
            "Preserve script exit codes: 0 means accepted/passed, non-zero means blocked or invalid.",
            "Do not bypass domain safety gates when wrapping this tool.",
        ],
    }


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    manifest = tool_manifest_builder.build(root_path)
    wrappers = [wrapper_for_tool(root_path, tool) for tool in manifest.get("tools", [])]
    blocked = [wrapper for wrapper in wrappers if wrapper["status"] != "wrappable"]
    return {
        "tool": "agent_tool_wrapper_manifest_builder",
        "root": str(root_path),
        "is_valid": bool(manifest["is_valid"]) and not blocked,
        "wrapper_count": len(wrappers),
        "wrappable_count": len(wrappers) - len(blocked),
        "blocked_count": len(blocked),
        "skill_count": manifest["skill_count"],
        "wrappers": wrappers,
        "runtime_contract": {
            "invocation": "python3 <script_path>",
            "input_contract": "Use input_schema_path as the wrapper input schema.",
            "output_contract": "Scripts emit JSON to stdout; wrappers should preserve the full JSON object.",
            "error_contract": "Non-zero exit means invalid, blocked, or not ready; expose stderr/error JSON to the agent.",
        },
        "limits": [
            "此 manifest 只描述 wrapper 元数据，不启动 MCP/API server。",
            "schema 能约束输入形状，但不能替代工具内部安全检查。",
            "真实 runtime wrapper 仍需前向测试和权限隔离。",
        ],
        "next_steps": [
            "generate_mcp_or_api_tool_definitions_from_wrappers",
            "run_agent_runtime_dry_run_runner_after_wrapper_changes",
            "forward_test_wrapped_tools_before_public_release",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Agent Tool Wrapper Manifest",
        "",
        "本页把 `agent-tools/scripts` 中的可运行脚本整理成 agent runtime 可消费的 wrapper 清单。它描述如何包装工具，不表示已经启动 MCP/API server。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| Wrapper | {result['wrapper_count']} |",
        f"| 可包装 | {result['wrappable_count']} |",
        f"| 阻塞 | {result['blocked_count']} |",
        f"| Skill | {result['skill_count']} |",
        "",
        "## Runtime Contract",
        "",
    ]
    for key, value in result["runtime_contract"].items():
        lines.append(f"- `{key}`：{value}")
    lines.extend(["", "## Wrapper 清单", "", "| Tool | Domains | Skills | Schema | Safety Tags |", "| --- | --- | --- | --- | --- |"])
    for wrapper in result["wrappers"]:
        domains = ", ".join(f"`{item}`" for item in wrapper["domains"])
        skills = ", ".join(f"`{item}`" for item in wrapper["skills"]) or "-"
        safety = ", ".join(f"`{item}`" for item in wrapper["safety_tags"])
        lines.append(
            f"| `{wrapper['name']}` | {domains} | {skills} | [{Path(wrapper['input_schema_path']).name}](../{wrapper['input_schema_path']}) | {safety} |"
        )
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/Agent工具WrapperManifest.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "Agent工具WrapperManifest.md"
        target.write_text(render_markdown(result), encoding="utf-8")
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
