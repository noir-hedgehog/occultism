#!/usr/bin/env python3
"""Build a low-risk practice plan for sound-cleansing requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import sound_cleansing_context_recorder
import sound_cleansing_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = sound_cleansing_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_sound_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人的声音、短句或空间联想；先询问语境，不编造治疗、驱邪、灵验或高价必要性。",
            "reflection_questions": ["它对应开始、结束、提醒、呼吸还是空间整理？", "音量、时长、时段和邻里边界是什么？", "是否像医疗替代、驱灵证明、扰民或反复依赖？"],
            "action_guidance": "只转成低音量、短时、可停止的空间复位或注意力提示。",
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
    record = sound_cleansing_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_sound_cleansing"]:
        return {
            "tool": "sound_cleansing_practice_planner",
            "is_valid": False,
            "can_continue_sound_cleansing": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "practice_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_sound_cleansing_consultation", "reframe_to_low_risk_space_reset_or_professional_support"],
        }
    queries = []
    for group in (record["sound_tools"], record["grounding_actions"], [record["practice_intention"]]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "sound_cleansing_practice_planner",
        "is_valid": True,
        "can_continue_sound_cleansing": True,
        "context_text": record["context_text"],
        "space_context": record["space_context"],
        "sound_tools": record["sound_tools"],
        "practice_intention": record["practice_intention"],
        "volume_duration": record["volume_duration"],
        "safety_boundaries": record["safety_boundaries"],
        "sensory_notes": record["sensory_notes"],
        "grounding_actions": record["grounding_actions"],
        "review_time": record["review_time"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "practice_plan": {
            "core_prompt": "这次声响净化请求怎样改写为短时、低音量、尊重身体和邻里边界的空间复位？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先说明声响净化只作文化象征、空间复位和注意力提示，不承诺驱邪或治疗。",
                "记录空间、时段、声音工具、音量时长、身体感受、宠物/婴儿/邻里边界。",
                "用计时器限制短时练习，保持舒适音量；任何耳痛、耳鸣、头晕或焦虑升高都停止。",
                "把铃钵、铃铛、音叉、拍手或诵念拆成开始、环视、整理、安静收尾和复盘。",
                "设置复盘时间和停止条件，避免反复净化、冲动购买或把声音当成专业支持替代。",
            ],
        },
        "limits": [
            "Use symbolic space-reset, attention, grounding, and review language only.",
            "Do not promise exorcism, cleansing certainty, healing, sleep, luck changes, or supernatural effects.",
            "Do not provide loud, ear-adjacent, overnight, pain-tolerating, infant/pet-near, or neighbor-conflict steps.",
            "Do not replace medical, mental-health, sleep, emergency, legal, or other professional support.",
            "Do not encourage expensive tools, ritual packages, manipulative sales, or repeated dependency.",
        ],
        "next_steps": ["draft_sound_cleansing_answer_from_plan", "run_mystic_output_lint", "offer_short_low_volume_practice_and_stop_condition"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "space_context", "sound_tools", "practice_intention", "volume_duration", "safety_boundaries", "sensory_notes", "grounding_actions", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Sound-cleansing notes.")
    parser.add_argument("--space-context", help="Space and timing context.")
    parser.add_argument("--sound-tools", help="Sound tools or voice practice.")
    parser.add_argument("--practice-intention", help="Practice intention.")
    parser.add_argument("--volume-duration", help="Volume and duration boundaries.")
    parser.add_argument("--safety-boundaries", help="Safety boundaries.")
    parser.add_argument("--sensory-notes", help="Sensory or body notes.")
    parser.add_argument("--grounding-actions", help="Grounding actions.")
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
