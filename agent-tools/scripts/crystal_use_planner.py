#!/usr/bin/env python3
"""Build a safe symbolic-use plan for crystals and energy stones."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import crystal_item_recorder
import crystal_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = crystal_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "item": query,
            "symbol_code": "unknown_or_trade_name",
            "keywords": [],
            "interpretation_prompt": "这可能是商业名、复合石、染色石或用户自定义名称；先要求来源、颜色、材质说明，不编造权威功效。",
            "reflection_questions": ["这个名称来自商家、家人口述、朋友推荐，还是用户自述？", "用户看重颜色、触感、纪念意义、预算，还是使用场景？"],
            "action_guidance": "不编造固定功效，不制造购买压力。",
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
    record = crystal_item_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["use_context"]
    if not record["can_continue_crystal"]:
        return {
            "tool": "crystal_use_planner",
            "is_valid": False,
            "can_continue_crystal": False,
            "intention_text": record["intention_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "use_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_crystal_consultation", "reframe_to_real_world_support"],
        }
    symbol_plans = [build_symbol_plan(item, focus) for item in record["items"]]
    return {
        "tool": "crystal_use_planner",
        "is_valid": True,
        "can_continue_crystal": True,
        "intention_text": record["intention_text"],
        "items": record["items"],
        "use_context": record["use_context"],
        "source": record["source"],
        "budget_note": record["budget_note"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "use_plan": {
            "core_prompt": "这个水晶/能量石安排能帮助用户建立哪种低风险提醒、审美秩序、边界感或自我照顾动作？",
            "item_count": len(symbol_plans),
            "practical_steps": [
                "优先使用已有物件或低成本替代，不制造购买压力。",
                "把使用方式限制在外部佩戴、摆放、记录或短时反思，不摄入、不贴伤口、不侵入身体。",
                "为每个物件绑定一个现实动作，例如整理桌面、写下边界、睡前放下手机或列出预算。",
                "设置停止条件：若焦虑、恐惧、购物冲动或专业问题加重，暂停水晶流程并寻求现实支持。",
            ],
        },
        "limits": [
            "Use symbolic and aesthetic reflection language only.",
            "Do not present crystals as diagnosis, treatment, spirit proof, protection guarantee, wealth guarantee, or professional advice.",
            "Do not recommend ingestion, body insertion, wound contact, unsafe charging methods, or expensive pressure purchases.",
        ],
        "next_steps": ["draft_crystal_answer_from_plan", "run_mystic_output_lint", "offer_low_cost_reality_checklist"],
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
    parser.add_argument("--text", help="Crystal intention or request notes.")
    parser.add_argument("--items", help="Crystal names, colors, or candidate items.")
    parser.add_argument("--use-context", help="wearing, workspace, bedside, gift, etc.")
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
