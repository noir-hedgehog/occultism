#!/usr/bin/env python3
"""Build a safe low-risk aroma symbolism practice plan."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import aroma_context_recorder
import aroma_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = aroma_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_custom_aroma_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人气味联想、品牌名称或自定义混香；先询问来源和用户感受，不编造疗效或神秘保证。",
            "reflection_questions": ["气味名称、来源、使用方式、现实安全背景和用户想整理的问题是什么？"],
            "action_guidance": "不编造治疗、驱邪、开运、关系结果、专业建议或购买必要性。",
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
    record = aroma_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_aroma"]:
        return {
            "tool": "aroma_practice_planner",
            "is_valid": False,
            "can_continue_aroma": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "practice_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_aroma_consultation", "reframe_to_safety_or_professional_support"],
        }
    symbol_plans = [build_symbol_plan(item, focus) for item in record["scent_items"]]
    if record["use_mode"]:
        symbol_plans.append(build_symbol_plan(record["use_mode"], focus))
    if record["ventilation"]:
        symbol_plans.append(build_symbol_plan("ventilation", focus))
    return {
        "tool": "aroma_practice_planner",
        "is_valid": True,
        "can_continue_aroma": True,
        "question_text": record["question_text"],
        "scent_items": record["scent_items"],
        "scent_source": record["scent_source"],
        "use_mode": record["use_mode"],
        "space": record["space"],
        "duration": record["duration"],
        "ventilation": record["ventilation"],
        "focus": record["focus"],
        "safety_context": record["safety_context"],
        "reality_constraints": record["reality_constraints"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "practice_plan": {
            "core_prompt": "这组气味和使用方式能帮助用户整理哪种感受、环境切换、边界和低风险下一步？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明芳香/精油只作气味象征和环境提醒，不作治疗、驱邪、净化保证、开运或专业建议。",
                "标注气味来源、已有物件、使用方式、空间、时长、通风、安全背景、预算和缺失字段。",
                "逐一把气味或物件转成感受/记忆/空间切换提示，而不是疗效断言。",
                "给出非接触、短时、可停止、低成本、可撤回的象征动作，并保留通风和停止条件。",
                "若涉及内服、皮肤危险用法、孕婴宠物过敏、医疗替代、驱邪恐惧、高价购买或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use scent symbolism and low-risk environmental reminders only.",
            "Do not provide medical, mental-health, veterinary, pregnancy, allergy, skin-use, ingestion, or fire-safety instructions beyond pausing and seeking qualified guidance.",
            "Avoid exorcism claims, outcome guarantees, third-party coercion, expensive purchase pressure, and repeated dependency.",
        ],
        "next_steps": ["draft_aroma_answer_from_plan", "run_mystic_output_lint", "offer_stop_conditions_and_reality_checks"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "scent_items", "scent_source", "use_mode", "space", "duration", "ventilation", "focus"):
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
    parser.add_argument("--text", help="Aroma request or context notes.")
    parser.add_argument("--scent-items", help="Comma-separated scents, oils, or aromatic items.")
    parser.add_argument("--scent-source", help="Existing item, gift, shop sample, recipe, etc.")
    parser.add_argument("--use-mode", help="Diffuser, smelling strip, sachet, non-contact reminder, etc.")
    parser.add_argument("--space", help="Space or location.")
    parser.add_argument("--duration", help="Short time box or stop condition.")
    parser.add_argument("--ventilation", help="Ventilation note.")
    parser.add_argument("--focus", help="Reflection focus.")
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
