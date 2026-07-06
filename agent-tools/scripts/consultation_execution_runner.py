#!/usr/bin/env python3
"""Run the safe programmable subset of a consultation packet and mark Agent handoff work."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

import consultation_packet_builder
import mystic_intake_triage
import paradigm_selector


SAFE_RUNNERS: dict[str, Callable[[dict[str, Any], Path], dict[str, Any]]] = {
    "consultation_packet_builder": lambda payload, root: consultation_packet_builder.build(payload, root=root),
    "paradigm_selector": lambda payload, root: paradigm_selector.select(payload, root=root),
    "mystic_intake_triage": lambda payload, _root: mystic_intake_triage.triage(payload),
}


def run_safe_tool(tool: str, payload: dict[str, Any], root: Path) -> dict[str, Any]:
    runner = SAFE_RUNNERS[tool]
    result = runner(payload, root)
    return {
        "tool": tool,
        "status": "executed",
        "is_valid": bool(result.get("is_valid", True)),
        "summary": summarize_result(tool, result),
        "result": result,
    }


def summarize_result(tool: str, result: dict[str, Any]) -> dict[str, Any]:
    if tool == "consultation_packet_builder":
        return {
            "domain": result["session"]["domain"],
            "route_status": result["session"]["route_status"],
            "tool_chain_count": len(result["tool_chain"]),
            "review_checklist_count": len(result["agent_brief"]["review_checklist"]),
        }
    if tool == "paradigm_selector":
        return {
            "domain": result["domain"],
            "paradigm": result["recommended_paradigm"]["id"],
            "automation_mode": result["execution_boundary"]["automation_mode"],
        }
    if tool == "mystic_intake_triage":
        return {
            "domain": result["domain"],
            "intent": result["intent"],
            "risk_level": result["risk_level"],
        }
    return {"keys": sorted(result.keys())[:8]}


def skip_reason(item: dict[str, Any]) -> tuple[str, str]:
    status = item["execution_status"]
    if status == "requires_structured_input":
        return ("requires_structured_input", "Collect structured fields in UI or let Agent ask follow-up questions.")
    if status == "requires_draft_output":
        return ("requires_draft_output", "Run after Agent drafts a user-visible answer.")
    return ("not_in_safe_runner_whitelist", "Only deterministic no-side-effect tools run in this local API path.")


def build(payload: dict[str, Any], root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    text = str(payload.get("request_text", "")).strip()
    if not text:
        raise ValueError("request_text is required")
    run_payload: dict[str, Any] = {"request_text": text}
    if payload.get("requested_domain"):
        run_payload["requested_domain"] = str(payload["requested_domain"])

    packet = consultation_packet_builder.build(run_payload, root=root_path)
    executed: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for item in packet["tool_chain"]:
        tool = item["tool"]
        if item["execution_status"] == "runnable_now" and tool in SAFE_RUNNERS:
            try:
                executed.append(run_safe_tool(tool, run_payload, root_path))
            except Exception as exc:
                errors.append({"tool": tool, "error": str(exc)})
        else:
            reason, action = skip_reason(item)
            skipped.append(
                {
                    "tool": tool,
                    "execution_status": item["execution_status"],
                    "reason": reason,
                    "agent_or_user_action": action,
                    "command": item["command"],
                }
            )

    structured = [item for item in skipped if item["execution_status"] == "requires_structured_input"]
    draft_required = [item for item in skipped if item["execution_status"] == "requires_draft_output"]
    agent_required = structured + draft_required
    next_ui_steps = [
        step
        for step in [
            "use_tool_preview_for_structured_inputs" if structured else "",
            "draft_agent_response_then_run_handoff" if draft_required else "",
            "use_consultation_handoff_builder_for_review"
            if packet["session"]["can_continue_mystic_workflow"]
            else "pause_for_safety_or_professional_boundary",
        ]
        if step
    ]
    route_status = packet["session"]["route_status"]
    if errors:
        run_status = "execution_errors"
    elif not packet["session"]["can_continue_mystic_workflow"]:
        run_status = "paused_after_safe_tools"
    elif agent_required:
        run_status = "safe_subset_executed_agent_handoff_required"
    else:
        run_status = "safe_subset_complete"

    return {
        "tool": "consultation_execution_runner",
        "root": str(root_path),
        "is_valid": bool(packet["is_valid"]) and not errors and all(item["is_valid"] for item in executed),
        "request_text": text,
        "domain": packet["session"]["domain"],
        "route_status": route_status,
        "run_status": run_status,
        "execution_summary": {
            "tool_chain_count": len(packet["tool_chain"]),
            "executed_count": len(executed),
            "skipped_count": len(skipped),
            "structured_input_count": len(structured),
            "draft_required_count": len(draft_required),
            "agent_required_count": len(agent_required),
            "error_count": len(errors),
        },
        "executed_tools": executed,
        "skipped_tools": skipped,
        "errors": errors,
        "agent_handoff": {
            "required": bool(agent_required) or not packet["session"]["can_continue_mystic_workflow"],
            "reasons": [item["reason"] for item in skipped],
            "next_ui_steps": next_ui_steps,
        },
        "packet": packet,
        "limits": [
            "此 runner 只执行安全白名单中的确定性工具，不执行任意 shell 命令。",
            "领域工具、照片/牌面/盘式输入和最终综合解读仍需要 UI 补字段或 Agent 接管。",
            "orange/red 风险只运行安全分流工具，不继续领域咨询。",
        ],
        "next_steps": [
            "collect_structured_inputs_for_skipped_tools",
            "run_consultation_handoff_builder_after_preview_or_draft",
            "record_follow_up_with_consultation_case_recorder",
        ],
    }


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
