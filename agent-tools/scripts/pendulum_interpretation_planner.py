#!/usr/bin/env python3
"""Build a safe interpretation plan for pendulum divination."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import pendulum_session_recorder
import pendulum_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    symbol = pendulum_symbol_lookup.lookup({"query": query, "focus": focus})
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
    record = pendulum_session_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["question_type"]
    if not record["can_continue_pendulum"]:
        return {
            "tool": "pendulum_interpretation_planner",
            "is_valid": False,
            "can_continue_pendulum": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_layers": [],
            "synthesis": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_pendulum_reading", "reframe_to_real_world_support"],
        }
    queries = ["calibration", record["answer_motion"], "maybe" if record["question_type"] == "yes_no" else "unclear"]
    symbol_plans = []
    for query in queries:
        try:
            symbol_plans.append(build_symbol_plan(query, focus))
        except ValueError:
            continue
    return {
        "tool": "pendulum_interpretation_planner",
        "is_valid": True,
        "can_continue_pendulum": True,
        "question_text": record["question_text"],
        "question_type": record["question_type"],
        "answer_motion": record["answer_motion"],
        "consent_confirmed": record["consent_confirmed"],
        "calibration_notes": record["calibration_notes"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_layers": [
            "先说明灵摆只作象征反思，不证明外部事实或替用户决定。",
            "确认问题已从绝对 yes/no 改写成可验证、可撤回、低风险的反思问题。",
            "解释校准和摆动记录，只用倾向、提醒、缺失证据等语言。",
            "把现实证据、专业边界、当事人沟通和用户价值排序放在象征之前。",
            "若出现依赖、恐惧、专业替代或第三方操控，暂停灵摆流程。",
        ],
        "synthesis": {
            "core_prompt": "这个灵摆记录能帮助用户澄清哪个偏好、证据缺口或低风险下一步？",
            "symbol_count": len(symbol_plans),
            "grounded_actions": [
                "把问题拆成可观察事实、个人偏好和下一步行动三列。",
                "对 yes/no 结果给出至少一个现实核查动作。",
                "为同一问题设置停止追问条件，避免反复依赖。",
            ],
        },
        "limits": [
            "Use symbolic reflection language only.",
            "Do not present pendulum motion as fact, diagnosis, prediction, or instruction.",
            "Do not decide medical, legal, financial, safety, or third-party matters.",
        ],
        "next_steps": ["draft_pendulum_answer_from_plan", "run_mystic_output_lint", "offer_reality_evidence_checklist"],
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
    if args.answer_motion:
        payload["answer_motion"] = args.answer_motion
    if args.calibration_notes:
        payload["calibration_notes"] = args.calibration_notes
    if args.focus:
        payload["focus"] = args.focus
    if args.consent_confirmed:
        payload["consent_confirmed"] = True
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
    parser.add_argument("--text", help="Pendulum question or session notes.")
    parser.add_argument("--answer-motion", help="Observed motion or answer label.")
    parser.add_argument("--calibration-notes", help="Calibration notes.")
    parser.add_argument("--focus", help="Optional focus.")
    parser.add_argument("--consent-confirmed", action="store_true", help="User consents to symbolic reflection.")
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
