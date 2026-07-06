#!/usr/bin/env python3
"""Build a safe symbolic-use plan for talismans, charms, and fu-lu."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import talisman_record_builder
import talisman_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = talisman_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "item": query,
            "symbol_code": "unknown_or_source_specific",
            "keywords": [],
            "interpretation_prompt": "这可能是特定寺庙、道观、商家或家庭语境中的名称；先要求来源、可见文字/图案和用途说明，不编造功效。",
            "reflection_questions": ["来源和使用语境是什么？", "用户看重祝愿、纪念、安心、家庭沟通，还是空间秩序？"],
            "action_guidance": "不编造灵验、功效或仪式步骤。",
        }
    return {
        "item": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = talisman_record_builder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["use_context"]
    if not record["can_continue_talisman"]:
        return {
            "tool": "talisman_use_planner",
            "is_valid": False,
            "can_continue_talisman": False,
            "intention_text": record["intention_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "use_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_talisman_consultation", "reframe_to_real_world_support"],
        }
    symbol_plans = [build_symbol_plan(item, focus) for item in record["items"]]
    return {
        "tool": "talisman_use_planner",
        "is_valid": True,
        "can_continue_talisman": True,
        "intention_text": record["intention_text"],
        "items": record["items"],
        "source_type": record["source_type"],
        "source_label": record["source_label"],
        "use_context": record["use_context"],
        "budget_note": record["budget_note"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "use_plan": {
            "core_prompt": "这个护符/符箓安排能帮助用户建立哪种低风险提醒、来源辨析、边界感或现实行动？",
            "item_count": len(symbol_plans),
            "practical_steps": [
                "先记录来源和可见文字/图案，不补造功效或师承。",
                "使用方式限于外部佩戴、收纳、摆放、纪念或短时反思。",
                "不烧、不喝、不吞、不放血、不密闭燃烧、不用于诅咒或操控。",
                "为物件绑定现实动作，例如出门检查、联系可信任的人、整理入口、记录预算或写下边界。",
                "若恐惧、购物压力、专业问题或依赖感加重，暂停护符流程并寻求现实支持。",
            ],
        },
        "limits": [
            "Use cultural and symbolic reflection language only.",
            "Do not present talismans as treatment, spirit proof, curse proof, protection guarantee, wealth guarantee, or professional advice.",
            "Do not provide instructions for drawing spells, burning talismans, drinking talisman water, swallowing paper, blood rituals, curses, coercion, or expensive purchase pressure.",
        ],
        "next_steps": ["draft_talisman_answer_from_plan", "run_mystic_output_lint", "offer_source_and_safety_checklist"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["intention_text"] = args.text
    if args.items:
        payload["items"] = args.items
    if args.source_type:
        payload["source_type"] = args.source_type
    if args.source_label:
        payload["source_label"] = args.source_label
    if args.use_context:
        payload["use_context"] = args.use_context
    if args.budget_note:
        payload["budget_note"] = args.budget_note
    if args.focus:
        payload["focus"] = args.focus
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"intention_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Talisman intention or request notes.")
    parser.add_argument("--items", help="Talisman names or visible symbols.")
    parser.add_argument("--source-type", help="temple, daoist_temple, family_gift, store, unknown.")
    parser.add_argument("--source-label", help="Short source label.")
    parser.add_argument("--use-context", help="wearing, carrying, workspace, entrance, etc.")
    parser.add_argument("--budget-note", help="Existing item or budget note.")
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
