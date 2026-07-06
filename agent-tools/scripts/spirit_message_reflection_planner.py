#!/usr/bin/env python3
"""Build a safe symbolic plan for spirit-message reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import spirit_message_record_builder
import spirit_message_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = spirit_message_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_message_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人句子、梦境素材、课程术语或写作意象；先询问用户自己的联想，不编造灵体事实。",
            "reflection_questions": ["这句话来自哪里？", "它触发了什么情绪或现实主题？", "是否像命令、事实证明或专业替代？"],
            "action_guidance": "不编造灵体身份、外部事实、命令、预言或第三方结论。",
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
    record = spirit_message_record_builder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_spirit_message"]:
        return {
            "tool": "spirit_message_reflection_planner",
            "is_valid": False,
            "can_continue_spirit_message": False,
            "message_text": record["message_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_spirit_message_consultation", "reframe_to_safety_or_real_world_support"],
        }
    queries = []
    for group in (record["sources"], record["phrases"], record["symbols"], record["emotions"]):
        for item in group:
            if item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "spirit_message_reflection_planner",
        "is_valid": True,
        "can_continue_spirit_message": True,
        "message_text": record["message_text"],
        "sources": record["sources"],
        "phrases": record["phrases"],
        "symbols": record["symbols"],
        "emotions": record["emotions"],
        "reality_anchor": record["reality_anchor"],
        "consent_notes": record["consent_notes"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这条灵性讯息能怎样作为象征写作素材，帮助用户整理情绪、边界和可验证行动？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先标注来源：梦、冥想、自由写作、卡牌、课程或文化学习；不写成外部事实。",
                "把讯息拆成原句、符号、情绪、用户自己的第一联想和现实触发。",
                "把解释落回当下：边界、照料、沟通、休息、记录或一个可验证行动。",
                "命令式声音、幻听幻视、危机、强烈恐惧或功能受损时，暂停并建议即时/专业支持。",
                "不读取第三方、不确认灵体、不承诺疗愈/复合/发财、不诱导付费通灵或反复问灵。",
            ],
        },
        "limits": [
            "Use symbolic writing and inner-dialogue language only.",
            "Do not present spirit messages as facts, commands, diagnosis, healing proof, spirit proof, third-party mind reading, fate, or professional advice.",
            "Do not create paid-channeling pressure, coercion, curse work, or repeated dependency.",
        ],
        "next_steps": ["draft_spirit_message_answer_from_plan", "run_mystic_output_lint", "offer_grounding_and_real_world_support_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "sources", "phrases", "symbols", "emotions", "reality_anchor", "consent_notes", "focus"):
        value = getattr(args, key)
        if value:
            payload["message_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"message_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Spirit-message notes.")
    parser.add_argument("--sources", help="Sources.")
    parser.add_argument("--phrases", help="Message phrases.")
    parser.add_argument("--symbols", help="Message symbols.")
    parser.add_argument("--emotions", help="Emotions or tones.")
    parser.add_argument("--reality-anchor", help="Current-life practical anchor.")
    parser.add_argument("--consent-notes", help="Consent/privacy notes.")
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
