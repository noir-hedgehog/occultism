#!/usr/bin/env python3
"""Build an agent handoff dossier from a consultation packet and optional tool preview."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import consultation_packet_builder
import mystic_output_lint
from _ui_action_manifest import build_ui_actions


def preview_summary(preview_result: Any) -> dict[str, Any]:
    if not isinstance(preview_result, dict) or not preview_result:
        return {
            "present": False,
            "mode": "",
            "tool_name": "",
            "is_valid": False,
            "result_keys": [],
        }
    result = preview_result.get("result", {})
    return {
        "present": True,
        "mode": str(preview_result.get("mode", "")),
        "tool_name": str(preview_result.get("tool_name", "")),
        "is_valid": bool(preview_result.get("is_valid", False)),
        "result_keys": sorted(result.keys()) if isinstance(result, dict) else [],
    }


def required_inputs_status(packet: dict[str, Any], preview: dict[str, Any]) -> dict[str, Any]:
    required = [
        item["tool"]
        for item in packet.get("tool_chain", [])
        if item.get("execution_status") == "requires_structured_input"
    ]
    covered = bool(preview.get("present") and preview.get("is_valid"))
    return {
        "required_structured_tools": required,
        "has_structured_preview": covered,
        "remaining_structured_input_needed": [] if covered else required,
    }


def lint_result_for(draft_output: str) -> dict[str, Any] | None:
    draft = draft_output.strip()
    if not draft:
        return None
    return mystic_output_lint.lint({"output_text": draft})


def handoff_status(packet: dict[str, Any], inputs: dict[str, Any], lint_result: dict[str, Any] | None) -> str:
    session = packet["session"]
    if not session["can_continue_mystic_workflow"]:
        return "pause_required"
    if inputs["remaining_structured_input_needed"]:
        return "needs_structured_tool_results"
    if lint_result:
        if lint_result["risk_level"] == "red":
            return "blocked_by_lint"
        if lint_result["publishable"]:
            return "ready_for_review"
        return "rewrite_required"
    return "ready_for_agent_synthesis"


def review_checklist(packet: dict[str, Any], preview: dict[str, Any], lint_result: dict[str, Any] | None) -> list[str]:
    checklist = list(packet.get("agent_brief", {}).get("review_checklist", []))
    if preview["present"]:
        checklist.append("是否把结构化工具结果中的观察、牌位、清单或模式纳入回答，而不是只复述原始问题？")
    else:
        checklist.append("是否已说明哪些结构化工具还没有运行，哪些字段需要用户补充？")
    if lint_result:
        checklist.append("是否处理 mystic_output_lint 的 findings 和 required_actions？")
    else:
        checklist.append("最终草稿是否会在发布前运行 mystic_output_lint？")
    return checklist


def agent_resume_prompt(packet: dict[str, Any], preview: dict[str, Any], status: str) -> list[str]:
    if status == "pause_required":
        return [
            "暂停玄学流程。",
            "先说明安全或专业边界，并给出低风险现实支持路径。",
            "按 handoff.ui_actions 只使用 enabled=true 的动作，不要继续结构化预览或普通案例采集。",
        ]
    prompts = [
        "读取 handoff.packet.context_docs 中的 Skill、SOP、知识卡和范式文档。",
        "使用 handoff.preview_result 作为结构化证据，不要编造未提供的牌、盘、图像或来源。",
        "按 handoff.packet.paradigm.execution_boundary 区分自动化结果、Agent 综合和人工审校。",
        "按 handoff.ui_actions 选择下一步动作；disabled 动作只解释原因，不直接执行。",
        "回答必须保留限制语、现实约束和低风险下一步。",
    ]
    if not preview["present"]:
        prompts.insert(1, "先向用户补齐结构化输入或说明当前只能做流程建议。")
    prompts.append("发布前运行或等价执行 mystic_output_lint。")
    return prompts


def ui_actions_for_packet(packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return build_ui_actions(packet["session"]["can_continue_mystic_workflow"])


def build(payload: dict[str, Any], root: str | Path = ".") -> dict[str, Any]:
    request_text = str(payload.get("request_text", "")).strip()
    if not request_text:
        raise ValueError("request_text is required")
    packet_payload: dict[str, Any] = {"request_text": request_text}
    if payload.get("requested_domain"):
        packet_payload["requested_domain"] = str(payload["requested_domain"])
    packet = consultation_packet_builder.build(packet_payload, root=root)
    preview = preview_summary(payload.get("preview_result"))
    input_status = required_inputs_status(packet, preview)
    draft_output = str(payload.get("draft_output", ""))
    lint_result = lint_result_for(draft_output)
    status = handoff_status(packet, input_status, lint_result)
    ui_actions = ui_actions_for_packet(packet)
    return {
        "tool": "consultation_handoff_builder",
        "root": str(Path(root).resolve()),
        "is_valid": status not in {"blocked_by_lint"} and bool(packet["is_valid"]),
        "request_text": request_text,
        "handoff_status": status,
        "ui_actions": ui_actions,
        "packet": packet,
        "preview": preview,
        "preview_result": payload.get("preview_result", {}),
        "input_status": input_status,
        "draft_output": draft_output,
        "lint_result": lint_result or {},
        "agent_resume_prompt": agent_resume_prompt(packet, preview, status),
        "review_checklist": review_checklist(packet, preview, lint_result),
        "limits": [
            "交接包只组织证据和边界，不替 Agent 生成最终玄学回答。",
            "preview_result 必须来自白名单工具或可信 runtime，不能当作已审校事实。",
            "lint_result 通过不代表内容专家批准，只表示当前安全措辞规则未阻断。",
        ],
        "next_steps": [
            "agent_reads_context_docs",
            "agent_synthesizes_from_preview_or_requests_missing_inputs",
            "run_mystic_output_lint_before_release",
            "record_case_outcome_if_user_allows",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        return json.loads(Path(args.file).read_text(encoding="utf-8"))
    if args.text:
        payload: dict[str, Any] = {"request_text": args.text}
        if args.domain:
            payload["requested_domain"] = args.domain
        if args.draft:
            payload["draft_output"] = args.draft
        return payload
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --text, --json, --file, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--text", help="User request text.")
    parser.add_argument("--domain", help="Optional requested domain.")
    parser.add_argument("--draft", help="Optional draft output for linting.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
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
