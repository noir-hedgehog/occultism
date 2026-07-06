#!/usr/bin/env python3
"""Build a safe interpretation plan for oracle-lot and temple-lot readings."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import oracle_lot_record_builder
import oracle_lot_symbol_lookup


def symbol_plan(query: str, focus: str) -> dict[str, Any]:
    symbol = oracle_lot_symbol_lookup.lookup({"query": query, "focus": focus})
    return {
        "symbol": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "symbol_layer": symbol["symbol_layer"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = oracle_lot_record_builder.record(payload)
    focus = str(payload.get("focus", record["question_text"] or "symbolic_reflection")).strip()
    if not record["can_continue_oracle_lot"]:
        return {
            "tool": "oracle_lot_interpretation_planner",
            "is_valid": False,
            "can_continue_oracle_lot": False,
            "question_text": record["question_text"],
            "lot_text": record["lot_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_layers": [],
            "synthesis": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_oracle_lot_reading", "reframe_to_safe_symbolic_or_reality_support"],
        }
    queries = ["签文"]
    if record["lot_grade"] != "unspecified":
        queries.append(record["lot_grade"])
    if record["source_type"] == "temple":
        queries.append("寺庙")
    symbol_plans = []
    for query in queries:
        try:
            symbol_plans.append(symbol_plan(query, focus))
        except ValueError:
            continue
    return {
        "tool": "oracle_lot_interpretation_planner",
        "is_valid": True,
        "can_continue_oracle_lot": True,
        "question_text": record["question_text"],
        "lot_text": record["lot_text"],
        "source_type": record["source_type"],
        "lot_number": record["lot_number"],
        "lot_grade": record["lot_grade"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_layers": [
            "先记录签文来源、签号、签等和用户问题，不补造签本来源。",
            "把签文拆成字面关键词、象征提醒、现实约束和可控行动。",
            "好签不保证成功，差签不恐吓灾祸；都转成风险管理和下一步。",
            "涉及专业问题、操控他人或反复抽签依赖时暂停解签。",
        ],
        "synthesis": {
            "core_prompt": "这支签更适合提醒用户关注哪些现实条件、风险和下一步行动？",
            "source_anchor": record["source_label"] or record["source_type"],
            "grounded_actions": [
                "列出签文中 1-3 个关键词，并让用户对应现实事实。",
                "把象征提醒转成一个可执行且低风险的行动。",
                "若信息不足，先补问签文全文、来源和用户的一事一问。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not promise outcomes or claim the lot is authoritative proof.",
            "Do not replace medical, legal, financial, safety, or mental-health support.",
        ],
        "next_steps": ["draft_oracle_lot_answer_from_plan", "run_mystic_output_lint", "offer_reality_anchor_questions"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.question:
        payload["question_text"] = args.question
    if args.lot_text:
        payload["lot_text"] = args.lot_text
    if args.source_type:
        payload["source_type"] = args.source_type
    if args.focus:
        payload["focus"] = args.focus
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"lot_text": raw}
    raise ValueError("Provide --question/--lot-text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", help="User question.")
    parser.add_argument("--lot-text", help="Oracle lot text.")
    parser.add_argument("--source-type", help="temple, book, app, user_drawn, simulation, or unknown.")
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
