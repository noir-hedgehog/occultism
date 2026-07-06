#!/usr/bin/env python3
"""Build a safe reflection plan for sleep paralysis, nightmares, and night fear."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import sleep_paralysis_context_recorder
import sleep_paralysis_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = sleep_paralysis_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_sleep_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人睡眠体验、梦后情绪或房间线索；先询问语境，不编造鬼神、附身、下咒、灾祸或法事必要性。",
            "reflection_questions": ["它对应身体感、房间环境、压力背景还是醒后情绪？", "有哪些低风险安定动作？", "是否像灵体事实、危险仪式、专业替代或反复依赖？"],
            "action_guidance": "不编造灵异原因或驱邪步骤；只放回睡眠记录、身体安定、现实安全和可控行动。",
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
    record = sleep_paralysis_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_sleep_paralysis"]:
        return {
            "tool": "sleep_paralysis_reflection_planner",
            "is_valid": False,
            "can_continue_sleep_paralysis": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_sleep_paralysis_consultation", "reframe_to_sleep_safety_grounding_or_professional_support"],
        }
    queries = []
    for group in ([record["episode_pattern"], record["wake_state"], record["room_context"]], record["body_sensations"], record["perceived_images"], record["grounding_actions"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "sleep_paralysis_reflection_planner",
        "is_valid": True,
        "can_continue_sleep_paralysis": True,
        "context_text": record["context_text"],
        "episode_pattern": record["episode_pattern"],
        "wake_state": record["wake_state"],
        "body_sensations": record["body_sensations"],
        "perceived_images": record["perceived_images"],
        "room_context": record["room_context"],
        "recent_stressors": record["recent_stressors"],
        "sleep_context": record["sleep_context"],
        "grounding_actions": record["grounding_actions"],
        "daytime_impact": record["daytime_impact"],
        "review_time": record["review_time"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这次鬼压床/梦魇/夜间恐惧请求能怎样被改写为睡眠体验记录、醒后安定、房间现实安全检查和低风险象征反思？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "把鬼压床或梦魇语言限制为睡眠体验和恐惧象征，不确认灵体事实。",
                "记录发生时间、身体感、醒来状态、房间环境、近期压力、睡眠时长和白天影响。",
                "列出 1-3 个醒后复位动作，例如开床边灯、喝常温水、触摸稳定物、慢呼吸、写一句现实定位。",
                "检查现实安全：门锁、光线、噪音、温度、睡前刺激和是否需要联系可信任的人。",
                "设置复盘时间和停止条件，避免反复查灵异解释、做仪式或不敢睡。",
            ],
        },
        "limits": [
            "Use sleep-experience, grounding, reality-safety, and symbolic-reflection language only.",
            "Do not confirm ghosts, spirits, possession, curses, supernatural pressure, disasters, or third-party influence.",
            "Do not provide dangerous rituals, sleep deprivation, ingestion, professional replacement, or expensive ritual pressure.",
            "Prioritize real-world support for severe sleep impairment, breathing/chest symptoms, seizures, hallucinations, self-harm, violence, or functional impairment.",
        ],
        "next_steps": ["draft_sleep_paralysis_answer_from_plan", "run_mystic_output_lint", "offer_grounding_actions_and_stop_condition"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "episode_pattern", "wake_state", "body_sensations", "perceived_images", "room_context", "recent_stressors", "sleep_context", "grounding_actions", "daytime_impact", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Sleep paralysis or night fear notes.")
    parser.add_argument("--episode-pattern", help="Episode timing or pattern.")
    parser.add_argument("--wake-state", help="Waking state.")
    parser.add_argument("--body-sensations", help="Body sensations.")
    parser.add_argument("--perceived-images", help="Images or perceptions.")
    parser.add_argument("--room-context", help="Room and environment context.")
    parser.add_argument("--recent-stressors", help="Recent stressors.")
    parser.add_argument("--sleep-context", help="Sleep timing, fatigue, and routine context.")
    parser.add_argument("--grounding-actions", help="Grounding or safety actions.")
    parser.add_argument("--daytime-impact", help="Daytime impact.")
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
