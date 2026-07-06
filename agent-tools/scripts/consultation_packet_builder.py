#!/usr/bin/env python3
"""Build a human/agent consultation packet from a mystic request."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import agent_workflow_router
import knowledge_coverage_audit
import paradigm_selector


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def first_heading(root: Path, rel_path: str) -> str:
    path = root / rel_path
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return path.stem


def context_doc(root: Path, rel_path: str, role: str) -> dict[str, str]:
    return {
        "role": role,
        "path": rel_path,
        "title": first_heading(root, rel_path) if rel_path else "",
    }


def shell_command(parts: list[str]) -> str:
    def quote(value: str) -> str:
        if not value:
            return "''"
        safe = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./:-=")
        if all(char in safe for char in value):
            return value
        return "'" + value.replace("'", "'\"'\"'") + "'"

    return " ".join(quote(part) for part in parts)


def command_for(tool: str, request_text: str) -> dict[str, Any]:
    script = f"agent-tools/scripts/{tool}.py"
    runnable_with_request = {
        "mystic_intake_triage",
        "agent_workflow_router",
        "paradigm_selector",
        "consultation_packet_builder",
    }
    if tool in runnable_with_request:
        command = shell_command(["python3", script, "--text", request_text])
        status = "runnable_now"
    elif tool == "mystic_output_lint":
        command = shell_command(["python3", script, "--text", "<draft output>"])
        status = "requires_draft_output"
    else:
        command = shell_command(["python3", script, "--help"])
        status = "requires_structured_input"
    return {
        "tool": tool,
        "command": command,
        "execution_status": status,
    }


def workflow_steps(route: dict[str, Any], paradigm: dict[str, Any]) -> list[dict[str, str]]:
    steps = [
        {"id": "intake", "status": "done", "label": "记录原始请求并识别流派、意图和风险。"},
        {"id": "paradigm", "status": "done", "label": "选择主干、问题类型、处理范式和证据轨道。"},
    ]
    if not route["can_continue_mystic_workflow"]:
        steps.extend(
            [
                {"id": "pause", "status": "next", "label": "暂停玄学流程，说明安全或专业边界。"},
                {"id": "safe_alternative", "status": "next", "label": "提供低风险替代支持、现实资源或澄清问题。"},
            ]
        )
        return steps
    steps.extend(
        [
            {"id": "context", "status": "next", "label": "读取 Skill、SOP、知识卡和范式说明。"},
            {"id": "tools", "status": "next", "label": "按工作单工具链执行可直接运行或需结构化输入的工具。"},
            {"id": "synthesis", "status": "agent", "label": "Agent 按范式综合象征层、现实约束和低风险行动。"},
            {"id": "lint", "status": "required", "label": "输出前运行或人工等价执行 mystic_output_lint。"},
        ]
    )
    if paradigm["execution_boundary"]["human_review_recommended"]:
        steps.append({"id": "review", "status": "recommended", "label": "交给内容/来源审校者复核。"})
    return steps


def review_checklist(route: dict[str, Any], paradigm: dict[str, Any]) -> list[str]:
    checklist = [
        "是否保留原始问题、风险信号和必要澄清点？",
        "是否明确该范式只提供象征反思或低风险行动，不给确定预言？",
        "是否把可程序化步骤和需要 Agent 综合的步骤分开？",
        "是否在输出前执行或等价执行 mystic_output_lint？",
    ]
    evidence = paradigm["evidence_track"]
    if evidence["scientific_or_practical_validation"]:
        checklist.append("是否加入现实观察、低成本可逆行动和复盘时间点？")
    if evidence["provenance_audit"]:
        checklist.append("是否标注来源、派别差异和无法确认的说法？")
    if evidence["mystical_boundary_priority"]:
        checklist.append("是否避免确认灵体、诅咒、附身、操控他人或结果保证？")
    if not route["can_continue_mystic_workflow"]:
        checklist.append("是否暂停占卜/仪式/排盘，并给出专业边界或安全替代？")
    return checklist


def build(payload: dict[str, Any], root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    text = str(payload.get("request_text", "")).strip()
    if not text:
        raise ValueError("request_text is required")
    route_payload: dict[str, Any] = {"request_text": text}
    if payload.get("requested_domain"):
        route_payload["requested_domain"] = str(payload["requested_domain"])

    route = agent_workflow_router.route(route_payload, root=root_path)
    paradigm = paradigm_selector.select(route_payload, root=root_path)
    names = {item["domain"]: item["display_name"] for item in knowledge_coverage_audit.audit(root_path)["domains"]}

    context_docs = []
    if route.get("skill_path"):
        context_docs.append(context_doc(root_path, route["skill_path"], "skill"))
    context_docs.extend(context_doc(root_path, path, "sop") for path in route.get("sop", []))
    context_docs.extend(context_doc(root_path, path, "knowledge") for path in route.get("knowledge", []))
    context_docs.extend(
        [
            context_doc(root_path, "知识库/03-主干生成发展史.md", "trunk_reference"),
            context_doc(root_path, "知识库/07-问题到范式映射.md", "paradigm_reference"),
        ]
    )

    tool_chain = ["consultation_packet_builder", "paradigm_selector"] + route.get("initial_tools", [])
    if route["can_continue_mystic_workflow"] and "mystic_output_lint" not in tool_chain:
        tool_chain.append("mystic_output_lint")

    packet = {
        "tool": "consultation_packet_builder",
        "root": str(root_path),
        "is_valid": bool(route["is_valid"]) and bool(paradigm["is_valid"]),
        "request_text": text,
        "session": {
            "domain": route["domain"],
            "domain_display_name": names.get(route["domain"], route["domain"]),
            "intent": route["intent"],
            "risk_level": route["risk_level"],
            "route_status": route["route_status"],
            "can_continue_mystic_workflow": route["can_continue_mystic_workflow"],
            "risk_signals": route["risk_signals"],
            "required_clarifications": route["required_clarifications"],
            "allowed_next_steps": route["allowed_next_steps"],
        },
        "paradigm": {
            "trunk": paradigm["trunk"],
            "question_type": paradigm["question_type"],
            "recommended_paradigm": paradigm["recommended_paradigm"],
            "execution_boundary": paradigm["execution_boundary"],
            "evidence_track": paradigm["evidence_track"],
        },
        "context_docs": context_docs,
        "workflow_steps": workflow_steps(route, paradigm),
        "tool_chain": [command_for(tool, text) for tool in unique(tool_chain)],
        "agent_brief": {
            "instructions": route["agent_instructions"],
            "review_checklist": review_checklist(route, paradigm),
            "handoff_summary": (
                f"{names.get(route['domain'], route['domain'])} / "
                f"{paradigm['recommended_paradigm']['title']} / {route['route_status']}"
            ),
        },
        "limits": [
            "咨询工作单只组织流程和证据，不直接生成玄学结论。",
            "orange/red 风险必须暂停玄学流程，不能用工作单绕过安全边界。",
            "requires_structured_input 的工具需要 UI、Agent 或用户补齐字段后再运行。",
        ],
        "next_steps": [
            "read_context_docs",
            "run_runnable_tool_chain",
            "collect_structured_inputs_for_domain_tools",
            "draft_agent_response",
            "run_or_equivalent_output_lint",
        ],
    }
    return packet


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
        result = build(load_payload(args), root=args.root)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
