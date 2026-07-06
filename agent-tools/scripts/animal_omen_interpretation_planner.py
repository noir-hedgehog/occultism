#!/usr/bin/env python3
"""Build a safe symbolic plan for animal-omen consultations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import animal_omen_observation_recorder
import animal_omen_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = animal_omen_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "animal": query,
            "symbol_code": "unknown_or_local_animal",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是地方叫法、具体物种或私人联想；先询问观察事实、环境原因和用户自己的第一联想，不编造固定预兆。",
            "reflection_questions": ["看到的具体动物和行为是什么？", "它是否可能由季节、食物、灯光、建筑缝隙或环境变化解释？", "是否存在现实安全或公共卫生风险？"],
            "action_guidance": "不编造灾祸、灵异、死亡、财运、关系或驱邪结论。",
        }
    return {
        "animal": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "category": symbol["category"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = animal_omen_observation_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_animal_omen"]:
        return {
            "tool": "animal_omen_interpretation_planner",
            "is_valid": False,
            "can_continue_animal_omen": False,
            "observation_text": record["observation_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "omen_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_animal_omen_consultation", "reframe_to_real_world_safety"],
        }
    symbol_plans = [build_symbol_plan(query, focus) for query in record["animals"]]
    return {
        "tool": "animal_omen_interpretation_planner",
        "is_valid": True,
        "can_continue_animal_omen": True,
        "observation_text": record["observation_text"],
        "animals": record["animals"],
        "behavior": record["behavior"],
        "location": record["location"],
        "timing": record["timing"],
        "frequency": record["frequency"],
        "source": record["source"],
        "safety_context": record["safety_context"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "omen_plan": {
            "core_prompt": "这个观察能怎样帮助用户区分现实环境、民俗联想、情绪反应和低风险行动？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先记录可见事实：动物、行为、时间、地点、频率和环境诱因。",
                "把民俗解释写成文化联想或提醒，不写成灾祸、死亡、鬼神或命运证明。",
                "咬伤、蜂窝、蛇/蝙蝠、鼠患、虫害、受伤动物和公共卫生风险优先现实处理。",
                "不伤害、不捕捉、不投喂、不靠近野生动物；必要时联系物业、动物救助、消防、疾控或专业灭害。",
                "若用户反复寻找征兆或恐惧升级，暂停解读，转向 grounding、现实支持和求助。",
            ],
        },
        "limits": [
            "Use cultural and symbolic reflection language only.",
            "Do not present animal appearances as fate proof, disaster warning, spirit message, death omen, wealth signal, relationship proof, or professional advice.",
            "Do not encourage animal harm, dangerous handling, wildlife contact, pest neglect, third-party mind reading, coercion, or dependency.",
        ],
        "next_steps": ["draft_animal_omen_answer_from_plan", "run_mystic_output_lint", "offer_real_world_safety_actions"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "animals", "behavior", "location", "timing", "frequency", "source", "safety_context", "focus"):
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
    parser.add_argument("--text", help="Animal observation or omen request notes.")
    parser.add_argument("--animals", help="Animal names.")
    parser.add_argument("--behavior", help="Observed behavior.")
    parser.add_argument("--location", help="Observed location.")
    parser.add_argument("--timing", help="Observed timing.")
    parser.add_argument("--frequency", help="single_observation, repeated, seasonal, unknown, etc.")
    parser.add_argument("--source", help="user_observed, photo_notes, family_story, cultural_learning, etc.")
    parser.add_argument("--safety-context", help="Bite, pest, injured animal, wildlife, building, pet, or other safety notes.")
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
