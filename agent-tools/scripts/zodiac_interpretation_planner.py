#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for zodiac and Tai Sui consultations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import zodiac_profile_recorder
import zodiac_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = zodiac_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_source_specific",
            "keywords": [],
            "interpretation_prompt": "这可能是特定黄历、家族、地区、网络或商家语境中的生肖说法；先要求来源和上下文，不编造流年吉凶。",
            "reflection_questions": ["来源和使用语境是什么？", "用户要文化学习、关系沟通、现实计划，还是安抚恐惧？"],
            "action_guidance": "不编造生肖运势、太岁灾祸或化解功效。",
        }
    return {
        "symbol": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def candidate_symbols(record: dict[str, Any]) -> list[str]:
    symbols: list[str] = []
    if record.get("zodiac"):
        symbols.append(str(record["zodiac"]))
    question = str(record.get("question_text", ""))
    for marker in ("本命年", "太岁", "犯太岁", "冲太岁", "六合", "三合", "六冲", "相冲"):
        if marker in question and marker not in symbols:
            symbols.append(marker)
    return symbols or ["生肖"]


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = zodiac_profile_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_zodiac"]:
        return {
            "tool": "zodiac_interpretation_planner",
            "is_valid": False,
            "can_continue_zodiac": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_zodiac_consultation", "reframe_to_real_world_support"],
        }
    symbol_plans = [build_symbol_plan(symbol, focus) for symbol in candidate_symbols(record)]
    return {
        "tool": "zodiac_interpretation_planner",
        "is_valid": True,
        "can_continue_zodiac": True,
        "question_text": record["question_text"],
        "birth_year": record["birth_year"],
        "zodiac": record["zodiac"],
        "focus": record["focus"],
        "subject_scope": record["subject_scope"],
        "source_note": record["source_note"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这个生肖/太岁说法能帮助用户整理哪种文化语境、节奏提醒、现实风险预案或沟通问题？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明生肖/太岁只作民俗文化和象征反思，不作命运证明。",
                "标注来源限制、本人/第三方范围和缺失资料。",
                "把生肖或太岁词汇转成时间节奏、沟通差异、低风险行动或预算提醒。",
                "列出 1-3 个现实中可验证、可撤回、不花大钱的小动作。",
                "若恐惧、专业问题、关系歧视、购买压力或依赖加重，暂停生肖流程。",
            ],
        },
        "limits": [
            "Use cultural and symbolic reflection language only.",
            "Do not present zodiac or Tai Sui as fate proof, disaster proof, personality proof, compatibility proof, diagnosis, wealth promise, or professional advice.",
            "Do not create purchase pressure for Tai Sui cures, charms, ceremonies, or paid services.",
        ],
        "next_steps": ["draft_zodiac_answer_from_plan", "run_mystic_output_lint", "offer_source_and_reality_checklist"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["question_text"] = args.text
    if args.birth_year:
        payload["birth_year"] = args.birth_year
    if args.zodiac:
        payload["zodiac"] = args.zodiac
    if args.focus:
        payload["focus"] = args.focus
    if args.subject_scope:
        payload["subject_scope"] = args.subject_scope
    if args.source_note:
        payload["source_note"] = args.source_note
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"question_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Zodiac question or request notes.")
    parser.add_argument("--birth-year", help="Birth year if relevant.")
    parser.add_argument("--zodiac", help="生肖/属相, e.g. 龙, rabbit, dog.")
    parser.add_argument("--focus", help="benmingnian_reflection, taisui_culture, relationship_reflection, etc.")
    parser.add_argument("--subject-scope", help="self, third_party_with_consent, generalized.")
    parser.add_argument("--source-note", help="Source, context, or practical note.")
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
