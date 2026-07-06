#!/usr/bin/env python3
"""Route a user mystic request to the right Skill, SOP, tools, or safety stop."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import knowledge_coverage_audit
import mystic_intake_triage
import tool_manifest_builder


DOMAIN_ALIASES = {
    "feng_shui": "fengshui",
    "ritual_safety": "ritual",
}

ROUTE_STATUS_BY_RISK = {
    "red": "blocked_safety",
    "orange": "paused_for_professional_boundary",
}


def normalize_domain(domain: str) -> str:
    return DOMAIN_ALIASES.get(domain, domain)


def domain_requirements(domain: str) -> dict[str, Any] | None:
    return knowledge_coverage_audit.DOMAIN_REQUIREMENTS.get(normalize_domain(domain))


def tools_for_skill(manifest: dict[str, Any], skill_name: str) -> list[str]:
    for skill in manifest.get("skills", []):
        if skill["skill"] == skill_name:
            return list(skill["tools"])
    return []


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def route(payload: dict[str, Any], root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    intake = mystic_intake_triage.triage(payload)
    domain = normalize_domain(str(intake["domain"]))
    requirements = domain_requirements(domain)
    manifest = tool_manifest_builder.build(root_path)
    risk_level = str(intake["risk_level"])

    if risk_level in ROUTE_STATUS_BY_RISK:
        route_status = ROUTE_STATUS_BY_RISK[risk_level]
        can_continue = False
    elif not requirements:
        route_status = "needs_domain_selection"
        can_continue = False
    else:
        route_status = "ready_to_run_skill"
        can_continue = True

    skill_path = requirements["skill"][0] if requirements else ""
    skill_name = Path(skill_path).parent.name if skill_path else ""
    skill_tools = tools_for_skill(manifest, skill_name) if skill_name else []
    domain_tools = requirements["tools"] if requirements else []
    initial_tools = ["mystic_intake_triage"]
    if can_continue:
        initial_tools.extend(skill_tools or domain_tools)
        if "mystic_output_lint" not in initial_tools:
            initial_tools.append("mystic_output_lint")
    initial_tools = unique(initial_tools)

    route_plan = {
        "tool": "agent_workflow_router",
        "root": str(root_path),
        "is_valid": bool(manifest.get("is_valid")) and (bool(requirements) or route_status != "ready_to_run_skill"),
        "request_text": intake["request_text"],
        "domain": domain,
        "original_domain": intake["domain"],
        "intent": intake["intent"],
        "risk_level": risk_level,
        "risk_signals": intake["risk_signals"],
        "route_status": route_status,
        "can_continue_mystic_workflow": can_continue,
        "skill": skill_name,
        "skill_path": skill_path,
        "sop": requirements["sop"] if requirements else [],
        "knowledge": requirements["knowledge"] if requirements else [],
        "initial_tools": initial_tools,
        "domain_tools": domain_tools,
        "required_clarifications": intake["required_clarifications"],
        "allowed_next_steps": intake["allowed_next_steps"],
        "agent_instructions": instructions_for(route_status, skill_name, requirements),
        "limits": [
            "路由计划只选择流程，不直接生成玄学结论。",
            "orange/red 风险必须暂停占卜、排盘或仪式流程。",
            "工具和 Skill 可用性来自当前仓库证据，真实运行环境仍需安装或 wrapper 接入。",
        ],
        "next_steps": next_steps_for(route_status),
    }
    return route_plan


def instructions_for(route_status: str, skill_name: str, requirements: dict[str, Any] | None) -> list[str]:
    if route_status == "blocked_safety":
        return ["停止玄学流程。优先给出安全支持、紧急资源或可信任联系人建议。"]
    if route_status == "paused_for_professional_boundary":
        return ["暂停占卜/仪式/排盘。说明不替代医疗、法律、财务或精神健康专业支持。"]
    if route_status == "needs_domain_selection":
        return ["先询问用户想使用哪个流派，或提供塔罗、风水、易经、命理等可选路径。"]
    return [
        f"加载 Skill `{skill_name}`。",
        "读取对应 SOP 和知识卡。",
        "按 initial_tools 顺序执行可用工具；缺工具时按 SOP 做人工等价检查。",
        "输出前运行或等价执行 `mystic_output_lint`。",
    ]


def next_steps_for(route_status: str) -> list[str]:
    if route_status == "ready_to_run_skill":
        return ["load_skill", "run_initial_tools", "draft_with_output_lint"]
    if route_status == "needs_domain_selection":
        return ["ask_domain_clarification"]
    return ["pause_workflow", "offer_safe_alternative_support"]


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.text:
        payload: dict[str, Any] = {"request_text": args.text}
        if args.domain:
            payload["requested_domain"] = args.domain
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--text", help="User request text.")
    parser.add_argument("--domain", help="Optional requested domain.")
    parser.add_argument("--json", help="JSON object input.")
    args = parser.parse_args()
    try:
        result = route(load_payload(args), root=args.root)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
