#!/usr/bin/env python3
"""Build a safe low-risk sigil symbolism practice plan."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import sigil_context_recorder
import sigil_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = sigil_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_custom_sigil_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人符号、历史图形、品牌图案、课程术语或自定义 sigil；先询问来源和用户感受，不编造灵验或召唤效果。",
            "reflection_questions": ["符号来源、构图元素、媒介、展示位置、安全边界和用户想整理的问题是什么？"],
            "action_guidance": "不编造召唤、驱邪、诅咒、显化保证、专业建议、纹身必要性或购买必要性。",
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
    record = sigil_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_sigil"]:
        return {
            "tool": "sigil_practice_planner",
            "is_valid": False,
            "can_continue_sigil": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "practice_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_sigil_consultation", "reframe_to_safety_or_professional_support"],
        }
    symbol_plans = [build_symbol_plan(item, focus) for item in record["symbol_elements"]]
    if record["activation_mode"]:
        symbol_plans.append(build_symbol_plan(record["activation_mode"], focus))
    return {
        "tool": "sigil_practice_planner",
        "is_valid": True,
        "can_continue_sigil": True,
        "question_text": record["question_text"],
        "intention_text": record["intention_text"],
        "symbol_elements": record["symbol_elements"],
        "source_context": record["source_context"],
        "medium": record["medium"],
        "activation_mode": record["activation_mode"],
        "display_location": record["display_location"],
        "duration": record["duration"],
        "focus": record["focus"],
        "safety_context": record["safety_context"],
        "reality_constraints": record["reality_constraints"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "practice_plan": {
            "core_prompt": "这个 sigil 如何把意图短句、图形元素和现实行动整理成可擦除、无火、非身体伤害、非操控的提醒物？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明 sigil/符号印记只作文化象征、意图整理和低风险提醒，不作召唤、驱邪、诅咒、显化保证或专业建议。",
                "标注意图短句、符号元素、来源、媒介、展示位置、时长、安全背景、现实约束和缺失字段。",
                "逐一把形状、字母或图像母题转成边界、方向、聚焦、选择、复盘和下一步，而不是灵验断言。",
                "给出纸面或数字草稿、可擦除、无火、不接触身体、不永久化、低成本、可停止的象征动作。",
                "若涉及滴血、割伤、刻皮肤、纹身、焚烧、召唤、驱邪、诅咒、操控、结果保证、违法财务或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use sigil symbolism and low-risk removable reminder objects only.",
            "Do not provide blood, cutting, body marking, tattoo, burning, summoning, exorcism, curse, coercion, legal/financial evasion, or professional-replacement instructions.",
            "Avoid outcome guarantees, expensive template/course pressure, and repeated dependency.",
        ],
        "next_steps": ["draft_sigil_answer_from_plan", "run_mystic_output_lint", "offer_stop_conditions_and_reality_checks"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "intention_text", "symbol_elements", "source_context", "medium", "activation_mode", "display_location", "duration", "focus"):
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
    parser.add_argument("--text", help="Sigil request or context notes.")
    parser.add_argument("--intention-text", help="Intention statement.")
    parser.add_argument("--symbol-elements", help="Comma-separated symbol parts.")
    parser.add_argument("--source-context", help="User-created, historical motif, book, existing image, etc.")
    parser.add_argument("--medium", help="Paper, digital draft, card, notebook, removable sticker, etc.")
    parser.add_argument("--activation-mode", help="Quiet review, journaling, visibility prompt, archive, etc.")
    parser.add_argument("--display-location", help="Where the symbol is seen or stored.")
    parser.add_argument("--duration", help="Short time box or stop condition.")
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
