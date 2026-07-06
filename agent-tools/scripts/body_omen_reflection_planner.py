#!/usr/bin/env python3
"""Build a safe low-risk body omen symbolism reflection plan."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import body_omen_context_recorder
import body_omen_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = body_omen_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_custom_body_omen_symbol",
            "symbol_layer": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人身体记录、地方民俗说法或自定义征兆；先询问身体背景、持续时间、医疗红旗和现实照料，不编造灾祸、疾病或财运结论。",
            "reflection_questions": ["征兆、身体位置、时间、持续频率、普通诱因、身体照料和停止条件是什么？"],
            "action_guidance": "不编造疾病、灾祸、灵体、财运、他人想法、彩票投资或第三方结论。",
        }
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
    record = body_omen_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_body_omen"]:
        return {
            "tool": "body_omen_reflection_planner",
            "is_valid": False,
            "can_continue_body_omen": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_body_omen_consultation", "reframe_to_medical_or_safety_support"],
        }
    symbol_inputs = [record["omen_type"], record["body_location"], *record["sensation_notes"]]
    if record["timing"]:
        symbol_inputs.append("时辰")
    symbol_plans = [build_symbol_plan(item, focus) for item in symbol_inputs if item]
    return {
        "tool": "body_omen_reflection_planner",
        "is_valid": True,
        "can_continue_body_omen": True,
        "question_text": record["question_text"],
        "omen_type": record["omen_type"],
        "body_location": record["body_location"],
        "timing": record["timing"],
        "duration": record["duration"],
        "sensation_notes": record["sensation_notes"],
        "health_context": record["health_context"],
        "mundane_context": record["mundane_context"],
        "focus": record["focus"],
        "reality_constraints": record["reality_constraints"],
        "stop_condition": record["stop_condition"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这个身体征兆记录如何帮助用户整理民俗象征、身体照料、现实背景和低风险下一步？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明身体征兆只作民俗象征和身体照料提醒，不作诊断、灾祸、财运、他人想法或灵体证据。",
                "标注征兆类型、身体位置、时间、持续频率、感受、普通诱因、健康背景、现实约束和停止条件。",
                "逐一把征兆转成休息、节奏、刺激、情绪、预算或社交感提示，而不是事实预言。",
                "给出用眼休息、降低刺激、记录一次、观察是否持续、必要时求医的现实清单。",
                "若涉及医疗红旗、停药、灾祸恐吓、彩票赌博、第三方标签、驱邪恐惧、危险试验或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use body omen folklore as symbolic reflection and body-care journaling only.",
            "Do not provide diagnosis, treatment, medication, emergency triage replacement, disaster prediction, gambling or investment timing, third-party labeling, spirit claims, unsafe body tests, or repeated reassurance loops.",
            "Persistent, sudden, severe, one-sided, painful, vision/hearing/breathing/neurological, fever, pregnancy, medication, or functional-impact symptoms require real-world professional support.",
        ],
        "next_steps": ["draft_body_omen_answer_from_plan", "run_mystic_output_lint", "offer_body_care_reality_check_and_stop_conditions"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "omen_type", "body_location", "timing", "duration", "sensation_notes", "health_context", "mundane_context", "focus", "stop_condition"):
        value = getattr(args, attr)
        if value:
            payload["question_text" if attr == "text" else attr] = value
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
    parser.add_argument("--text", help="Body omen request or context notes.")
    parser.add_argument("--omen-type", help="Signal type, e.g. eye twitch, sneeze, ear heat.")
    parser.add_argument("--body-location", help="Body location, e.g. left eye, right ear.")
    parser.add_argument("--timing", help="Time, date, or event context.")
    parser.add_argument("--duration", help="Duration or frequency.")
    parser.add_argument("--sensation-notes", help="Comma-separated sensation notes.")
    parser.add_argument("--health-context", help="Health and medical boundary notes.")
    parser.add_argument("--mundane-context", help="Sleep, screen, caffeine, stress, weather, or other ordinary context.")
    parser.add_argument("--focus", help="Reflection focus.")
    parser.add_argument("--stop-condition", help="Stop condition.")
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
