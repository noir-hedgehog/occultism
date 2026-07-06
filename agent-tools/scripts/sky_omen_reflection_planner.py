#!/usr/bin/env python3
"""Build a safe symbolic plan for sky-omen reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import sky_omen_observation_recorder
import sky_omen_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = sky_omen_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_sky_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人联想、云形描述或地点天气线索；先询问用户自己的联想，不编造灾祸、天气或神灵事实。",
            "reflection_questions": ["这个天空现象如何被观察到？", "它触发了什么情绪或现实主题？", "是否像灾祸预言、天气安全替代或专业替代？"],
            "action_guidance": "不编造天气预报、灾祸、神明显灵、第三方讯息或确定结论。",
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
    record = sky_omen_observation_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_sky_omen"]:
        return {
            "tool": "sky_omen_reflection_planner",
            "is_valid": False,
            "can_continue_sky_omen": False,
            "observation_text": record["observation_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_sky_omen_consultation", "reframe_to_weather_safety_or_real_world_support"],
        }
    queries = []
    for group in (record["phenomena"], record["shapes"], record["colors"], record["emotions"]):
        for item in group:
            if item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "sky_omen_reflection_planner",
        "is_valid": True,
        "can_continue_sky_omen": True,
        "observation_text": record["observation_text"],
        "phenomena": record["phenomena"],
        "shapes": record["shapes"],
        "colors": record["colors"],
        "location_time": record["location_time"],
        "weather_context": record["weather_context"],
        "emotions": record["emotions"],
        "reality_anchor": record["reality_anchor"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这次天空观察能怎样作为象征素材，帮助用户整理情绪、现实提醒和可验证行动？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先记录观察对象、地点时间、天气安全背景、形状颜色和用户第一联想。",
                "把天象解释限制为文化象征和自我反思，不写成天气预报、灾祸预言、天罚或灵体事实。",
                "把解释落回当下：一个情绪线索、一个现实提醒、一个低风险行动或一个官方天气检查。",
                "涉及雷雨台风洪水等现实风险时，以官方天气预警、避险和应急指引为准。",
                "不读取第三方、不替代专业支持、不鼓励危险天气暴露或反复看天象寻求确定感。",
            ],
        },
        "limits": [
            "Use symbolic sky-observation language only.",
            "Do not present sky omens as disaster prediction, weather forecast, divine command, death omen, spirit proof, third-party mind reading, or professional advice.",
            "Do not replace official weather alerts, emergency evacuation, lightning safety, medical/legal/financial advice, or mental-health support.",
        ],
        "next_steps": ["draft_sky_omen_answer_from_plan", "run_mystic_output_lint", "offer_weather_safety_or_grounded_action_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "phenomena", "shapes", "colors", "location_time", "weather_context", "emotions", "reality_anchor", "focus"):
        value = getattr(args, key)
        if value:
            payload["observation_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"observation_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Sky observation notes.")
    parser.add_argument("--phenomena", help="Sky phenomena.")
    parser.add_argument("--shapes", help="Cloud or sky shapes.")
    parser.add_argument("--colors", help="Colors or light qualities.")
    parser.add_argument("--location-time", help="Location and time.")
    parser.add_argument("--weather-context", help="Weather safety context.")
    parser.add_argument("--emotions", help="Emotions or tone.")
    parser.add_argument("--reality-anchor", help="Current practical anchor.")
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
