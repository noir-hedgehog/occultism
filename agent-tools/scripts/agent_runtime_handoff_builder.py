#!/usr/bin/env python3
"""Build a runtime handoff packet for integrating mystic tools and Skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import agent_route_smoke_runner
import agent_runtime_dry_run_runner
import agent_tool_definition_exporter
import agent_tool_definition_validator
import agent_tool_registry_builder
import agent_tool_registry_validator
import agent_tool_wrapper_manifest_builder
import external_evidence_intake_builder
import pilot_readiness_report
import skill_install_readiness_report
import tool_manifest_builder


ENTRYPOINTS = [
    {
        "entrypoint": "request_routing",
        "tool": "agent_workflow_router",
        "contract": "输入用户原始请求，输出流派、Skill、SOP、知识卡、初始工具链和风险状态。",
    },
    {
        "entrypoint": "domain_skill_execution",
        "tool": "codex-skills/*/SKILL.md",
        "contract": "按路由结果加载对应 Skill；Skill 再调用领域工具和 SOP。",
    },
    {
        "entrypoint": "output_safety_lint",
        "tool": "mystic_output_lint",
        "contract": "所有玄学输出交付前必须做安全措辞、专业边界和危险仪式检查。",
    },
]


SAFETY_INVARIANTS = [
    "red/orange 风险不得继续占卜、排盘或仪式步骤。",
    "不替代医疗、法律、财务、人身安全或精神健康专业支持。",
    "不确认鬼神实体伤害、诅咒成立、必然灾祸、必然发财或命运定论。",
    "驱邪/净化只能提供低风险、无明火、无危险材料、可撤回的象征性替代。",
    "出生资料、第三方信息和真实 transcript 必须按最小化、同意和脱敏规则处理。",
]


def build(root: str | Path = ".", codex_home: str | Path | None = None) -> dict[str, Any]:
    root_path = Path(root).resolve()
    manifest = tool_manifest_builder.build(root_path)
    wrapper_manifest = agent_tool_wrapper_manifest_builder.build(root_path)
    tool_definitions = agent_tool_definition_exporter.build(root_path)
    definition_validation = agent_tool_definition_validator.build(root_path)
    tool_registry = agent_tool_registry_builder.build(root_path)
    registry_validation = agent_tool_registry_validator.build(root_path)
    route_smoke = agent_route_smoke_runner.run(root=root_path)
    runtime_dry_run = agent_runtime_dry_run_runner.run(root=root_path)
    install = skill_install_readiness_report.build(root=root_path, codex_home=codex_home)
    pilot = pilot_readiness_report.build(root=root_path, codex_home=codex_home)
    external = external_evidence_intake_builder.build(root=root_path, codex_home=codex_home)
    skills = [
        {
            "skill": skill["skill"],
            "role": skill["role"],
            "tools": skill["tools"],
            "index_path": skill["index_path"],
        }
        for skill in manifest.get("skills", [])
    ]
    readiness_checks = [
        {
            "check": "tool_manifest",
            "passed": bool(manifest["is_valid"]),
            "summary": f"{manifest['tool_count']} tools, {manifest['skill_count']} skills",
        },
        {
            "check": "tool_wrapper_manifest",
            "passed": bool(wrapper_manifest["is_valid"]),
            "summary": f"{wrapper_manifest['wrappable_count']}/{wrapper_manifest['wrapper_count']} wrappers ready",
        },
        {
            "check": "tool_definition_export",
            "passed": bool(tool_definitions["is_valid"]),
            "summary": f"{tool_definitions['definition_count']} tool definitions exported",
        },
        {
            "check": "tool_definition_validation",
            "passed": bool(definition_validation["is_valid"]),
            "summary": f"{definition_validation['valid_definition_count']}/{definition_validation['definition_count']} definitions valid",
        },
        {
            "check": "tool_registry",
            "passed": bool(tool_registry["is_valid"]),
            "summary": f"{tool_registry['tool_count']} tools ready for runtime registration",
        },
        {
            "check": "tool_registry_validation",
            "passed": bool(registry_validation["is_valid"]),
            "summary": f"{registry_validation['tool_count']} tools, {registry_validation['failed_skill_count']} failed skill checks",
        },
        {
            "check": "route_smoke",
            "passed": bool(route_smoke["is_valid"]),
            "summary": f"{route_smoke['passed_count']}/{route_smoke['case_count']} route cases passed",
        },
        {
            "check": "runtime_dry_run",
            "passed": bool(runtime_dry_run["is_valid"]),
            "summary": f"{runtime_dry_run['passed_count']}/{runtime_dry_run['case_count']} runtime dry-run cases passed",
        },
        {
            "check": "skill_install_readiness",
            "passed": bool(install["is_valid"]),
            "summary": install["status"],
        },
        {
            "check": "pilot_readiness",
            "passed": bool(pilot["is_valid"]),
            "summary": pilot["pilot_status"],
        },
        {
            "check": "external_evidence_intake",
            "passed": bool(external["is_valid"]),
            "summary": f"{external['open_intake_count']} open external intake items",
        },
    ]
    runtime_ready = all(check["passed"] for check in readiness_checks)
    return {
        "tool": "agent_runtime_handoff_builder",
        "root": str(root_path),
        "is_valid": runtime_ready,
        "handoff_status": "ready_for_runtime_dry_run" if runtime_ready else "blocked_by_readiness_checks",
        "runtime_scope": "mystic_agent_tools_and_codex_skill_blueprints",
        "entrypoints": ENTRYPOINTS,
        "skill_count": len(skills),
        "tool_count": manifest["tool_count"],
        "skills": skills,
        "readiness_checks": readiness_checks,
        "safety_invariants": SAFETY_INVARIANTS,
        "required_runtime_assets": [
            "agent-tools/scripts/*.py",
            "agent-tools/schemas/*.json",
            "agent-tools/specs/*.md",
            "知识库/Agent工具WrapperManifest.md",
            "codex-skills/*/SKILL.md",
            "知识库/SOP/*.md",
            "知识库/流派/*.md",
            "知识库/01-安全边界.md",
        ],
        "integration_contract": {
            "router_command": "python3 agent-tools/scripts/agent_workflow_router.py --text '<user request>'",
            "manifest_command": "python3 agent-tools/scripts/tool_manifest_builder.py",
            "wrapper_manifest_command": "python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py",
            "tool_definition_export_command": "python3 agent-tools/scripts/agent_tool_definition_exporter.py --format openai",
            "tool_definition_validation_command": "python3 agent-tools/scripts/agent_tool_definition_validator.py",
            "tool_registry_command": "python3 agent-tools/scripts/agent_tool_registry_builder.py",
            "tool_registry_validation_command": "python3 agent-tools/scripts/agent_tool_registry_validator.py",
            "install_readiness_command": f"python3 agent-tools/scripts/skill_install_readiness_report.py --codex-home {install['codex_home']} --format markdown",
            "external_intake_command": f"python3 agent-tools/scripts/external_evidence_intake_builder.py --codex-home {install['codex_home']} --format markdown",
            "pilot_readiness_command": f"python3 agent-tools/scripts/pilot_readiness_report.py --codex-home {install['codex_home']} --format markdown",
        },
        "verification_commands": [
            "python3 agent-tools/scripts/agent_route_smoke_runner.py",
            "python3 agent-tools/scripts/agent_runtime_dry_run_runner.py",
            "python3 agent-tools/scripts/tool_manifest_builder.py",
            "python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py",
            "python3 agent-tools/scripts/agent_tool_definition_exporter.py",
            "python3 agent-tools/scripts/agent_tool_definition_validator.py",
            "python3 agent-tools/scripts/agent_tool_registry_builder.py",
            "python3 agent-tools/scripts/agent_tool_registry_validator.py",
            "python3 agent-tools/scripts/skill_replay_runner.py",
            "python3 agent-tools/scripts/skill_transcript_runner.py",
            "python3 agent-tools/scripts/release_gate_runner.py",
        ],
        "open_external_items": [item["blocker"] for item in pilot["external_blockers"]],
        "limits": [
            "ready_for_runtime_dry_run 表示仓库证据足以接入测试 runtime，不表示已经安装到真实 Codex home。",
            "runtime wrapper 必须保留 agent_workflow_router 的风险暂停语义。",
            "外部证据入口仍显示 open 时，不应宣称完整公开发布完成。",
        ],
        "next_steps": [
            "wire_router_to_agent_runtime",
            "map_manifest_tools_to_mcp_or_api_wrappers",
            "run_runtime_dry_run_against_route_smoke_cases",
            "collect_open_external_evidence_before_public_release",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Agent 运行时交接包",
        "",
        "本页把玄学 agent 接入运行时所需的入口、Skill、工具、验证命令和安全不变量整理到一个交接面板。它证明可以做 runtime dry-run，不证明已经完成真实安装或公开发布。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 状态 | `{result['handoff_status']}` |",
        f"| Skill | {result['skill_count']} |",
        f"| Tool | {result['tool_count']} |",
        f"| 外部开放项 | {len(result['open_external_items'])} |",
        "",
        "## 运行时入口",
        "",
        "| Entrypoint | Tool | Contract |",
        "| --- | --- | --- |",
    ]
    for item in result["entrypoints"]:
        lines.append(f"| `{item['entrypoint']}` | `{item['tool']}` | {item['contract']} |")
    lines.extend(["", "## 准备度检查", "", "| Check | Passed | Summary |", "| --- | --- | --- |"])
    for check in result["readiness_checks"]:
        lines.append(f"| `{check['check']}` | {check['passed']} | {check['summary']} |")
    lines.extend(["", "## Skill 与工具链", "", "| Skill | Role | Tools |", "| --- | --- | --- |"])
    for skill in result["skills"]:
        tools = ", ".join(f"`{tool}`" for tool in skill["tools"])
        lines.append(f"| `{skill['skill']}` | {skill['role']} | {tools} |")
    lines.extend(["", "## 安全不变量", ""])
    for invariant in result["safety_invariants"]:
        lines.append(f"- {invariant}")
    lines.extend(["", "## 集成命令", "", "```bash"])
    for command in result["integration_contract"].values():
        lines.append(command)
    lines.extend(["```", "", "## 验证命令", "", "```bash"])
    lines.extend(result["verification_commands"])
    lines.extend(["```", "", "## 外部开放项", ""])
    for item in result["open_external_items"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--codex-home", help="Target Codex home for install-readiness commands.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/Agent运行时交接包.md.")
    args = parser.parse_args()
    result = build(root=args.root, codex_home=args.codex_home)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "Agent运行时交接包.md"
        target.write_text(render_markdown(result), encoding="utf-8")
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
