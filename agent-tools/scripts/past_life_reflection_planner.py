#!/usr/bin/env python3
"""Build a safe symbolic plan for past-life/Akashic reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import past_life_narrative_recorder
import past_life_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = past_life_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_past_life_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人梦境、冥想画面、课程术语或创作意象；先询问用户自己的联想，不编造前世事实。",
            "reflection_questions": ["这个画面来自梦、冥想、故事还是课程？", "它和当下哪种边界、选择或情绪相连？", "是否在寻找事实证明或创伤确认？"],
            "action_guidance": "不编造前世身份、创伤事实、灵魂契约、命运判决或第三方结论。",
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
    record = past_life_narrative_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_past_life"]:
        return {
            "tool": "past_life_reflection_planner",
            "is_valid": False,
            "can_continue_past_life": False,
            "narrative_text": record["narrative_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_past_life_consultation", "reframe_to_symbolic_or_real_world_support"],
        }
    queries = []
    for group in (record["scenes"], record["roles"], record["symbols"], record["emotions"]):
        for item in group:
            if item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "past_life_reflection_planner",
        "is_valid": True,
        "can_continue_past_life": True,
        "narrative_text": record["narrative_text"],
        "scenes": record["scenes"],
        "roles": record["roles"],
        "symbols": record["symbols"],
        "emotions": record["emotions"],
        "source_context": record["source_context"],
        "focus": record["focus"],
        "reality_anchor": record["reality_anchor"],
        "consent_notes": record["consent_notes"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这些前世/阿卡西意象能怎样帮助用户理解当下主题、边界、情绪和可验证的小行动？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先标注来源：梦、冥想、想象、课程、故事或文化学习，不写成事实证据。",
                "把画面拆成象征层：角色、场景、物件、情绪、重复主题和用户自己的第一联想。",
                "把解释落回当下：关系边界、选择压力、照料需求、沟通计划或可停止的记录练习。",
                "涉及创伤、虐待、幻听幻视、连续失眠、强烈恐惧或功能受损时，暂停象征流程并建议专业支持。",
                "不读取第三方前世或灵魂契约，不承诺复合、还债、疗愈、发财或必须付费解读。",
            ],
        },
        "limits": [
            "Use symbolic narrative and present-life reflection language only.",
            "Do not present past-life or Akashic content as fact, recovered memory, trauma proof, soul rank, guilt, fate, relationship proof, or professional advice.",
            "Do not create paid-session pressure, third-party privacy invasion, coercion, or repeated dependency.",
        ],
        "next_steps": ["draft_past_life_answer_from_plan", "run_mystic_output_lint", "offer_grounding_and_real_world_support_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "scenes", "roles", "symbols", "emotions", "source_context", "focus", "reality_anchor", "consent_notes"):
        value = getattr(args, key)
        if value:
            payload["narrative_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"narrative_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Past-life/Akashic narrative notes.")
    parser.add_argument("--scenes", help="Scenes, places, or time-feel.")
    parser.add_argument("--roles", help="Symbolic roles.")
    parser.add_argument("--symbols", help="Objects or motifs.")
    parser.add_argument("--emotions", help="Emotions or themes.")
    parser.add_argument("--source-context", help="dream, meditation, journaling, cultural_learning, etc.")
    parser.add_argument("--focus", help="Optional focus.")
    parser.add_argument("--reality-anchor", help="Current-life practical anchor.")
    parser.add_argument("--consent-notes", help="Consent/privacy notes when others appear.")
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
