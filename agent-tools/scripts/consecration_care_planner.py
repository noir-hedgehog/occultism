#!/usr/bin/env python3
"""Build a safe care plan for consecration and object-cleansing requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import consecration_context_recorder
import consecration_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = consecration_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_consecration_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人物件、来源或照料联想；先询问语境，不编造灵验、神明命令、邪气事实或法事必要性。",
            "reflection_questions": ["它对应来源、用途、清洁、收纳还是提醒？", "有哪些无火、可撤回的可控动作？", "是否像危险仪式、专业替代、高价法事或反复依赖？"],
            "action_guidance": "不编造灵验或转运承诺；只放回来源记录、清洁整理、用途确认和复盘。",
        }
    return {
        "symbol": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "category": symbol["category"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = consecration_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_consecration"]:
        return {
            "tool": "consecration_care_planner",
            "is_valid": False,
            "can_continue_consecration": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "care_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_consecration_consultation", "reframe_to_low_risk_object_care_or_professional_support"],
        }
    queries = []
    for group in ([record["object_focus"]], record["existing_items"], record["symbolic_actions"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "consecration_care_planner",
        "is_valid": True,
        "can_continue_consecration": True,
        "context_text": record["context_text"],
        "object_focus": record["object_focus"],
        "source_context": record["source_context"],
        "current_use": record["current_use"],
        "existing_items": record["existing_items"],
        "safety_boundaries": record["safety_boundaries"],
        "symbolic_actions": record["symbolic_actions"],
        "risk_notes": record["risk_notes"],
        "review_time": record["review_time"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "care_plan": {
            "core_prompt": "这次开光/加持/净物请求能怎样被改写为来源记录、清洁整理、用途确认、无火安全和复盘提醒？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "把开光或净物语言限制为文化象征、来源记录和提醒物照料，不承诺灵验。",
                "记录物件来源、当前用途、材质限制、已有物件、安全边界和现实风险。",
                "列出 1-3 个无火、可撤回动作，例如清水擦拭、干净布收纳、写用途标签、固定收纳位置。",
                "不提供燃烧、摄入、放血、刀具或密闭空间步骤；明火相关内容只保留安全边界提醒。",
                "设置复盘时间和停止条件，避免反复开光、净物或冲动购买。",
            ],
        },
        "limits": [
            "Use symbolic object-care, source-recording, cleaning, reminder, and grounded-action language only.",
            "Do not promise efficacy, protection, wealth, luck changes, deity guarantees, or supernatural object effects.",
            "Do not provide ingestion, blood, blade, dangerous fire, sealed burning, self-harm, or illegal/coercive steps.",
            "Do not replace medical, legal, emergency, mental-health, or financial support.",
            "Do not encourage expensive rituals, paid consecration packages, manipulative sales, or repeated dependency.",
        ],
        "next_steps": ["draft_consecration_answer_from_plan", "run_mystic_output_lint", "offer_low_risk_object_care_and_stop_condition"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "object_focus", "source_context", "current_use", "existing_items", "safety_boundaries", "symbolic_actions", "risk_notes", "review_time", "stop_condition", "focus"):
        value = getattr(args, key)
        if value:
            payload["context_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"context_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Consecration notes.")
    parser.add_argument("--object-focus", help="Object or blessing focus.")
    parser.add_argument("--source-context", help="Object source context.")
    parser.add_argument("--current-use", help="Current use.")
    parser.add_argument("--existing-items", help="Existing items.")
    parser.add_argument("--safety-boundaries", help="Safety boundaries.")
    parser.add_argument("--symbolic-actions", help="Symbolic actions.")
    parser.add_argument("--risk-notes", help="Risk notes.")
    parser.add_argument("--review-time", help="Review time.")
    parser.add_argument("--stop-condition", help="Stopping condition.")
    parser.add_argument("--focus", help="Optional focus.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = plan(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
