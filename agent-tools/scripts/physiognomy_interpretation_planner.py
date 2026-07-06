#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for palmistry and physiognomy."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import physiognomy_observation_recorder
import physiognomy_symbol_lookup


def build_feature_plan(feature_code: str, focus: str) -> dict[str, Any]:
    symbol = physiognomy_symbol_lookup.lookup({"feature_code": feature_code, "focus": focus})
    return {
        "feature_code": symbol["symbol_code"],
        "symbol": symbol["canonical_name"],
        "symbol_layer": symbol["symbol_layer"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = physiognomy_observation_recorder.record(payload)
    focus = str(payload.get("focus", payload.get("user_goal", ""))).strip() or "self_reflection"
    if not record["can_continue_physiognomy"]:
        return {
            "tool": "physiognomy_interpretation_planner",
            "is_valid": False,
            "can_continue_physiognomy": False,
            "observation_text": record["observation_text"],
            "modality": record["modality"],
            "risk_flags": record["risk_flags"],
            "feature_plans": [],
            "interpretation_layers": [],
            "synthesis": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_physiognomy_reading", "reframe_to_safe_symbolic_or_cultural_learning"],
        }
    feature_plans = [build_feature_plan(code, focus) for code in record["feature_codes"][:4]]
    return {
        "tool": "physiognomy_interpretation_planner",
        "is_valid": True,
        "can_continue_physiognomy": True,
        "observation_text": record["observation_text"],
        "modality": record["modality"],
        "consent_state": record["consent_state"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "feature_plans": feature_plans,
        "interpretation_layers": [
            "先说明资料来自用户自述或授权观察，不分析照片、不补写未给出的外貌细节。",
            "逐一解释掌纹/五官在传统象征里的可能含义，并保留不确定性。",
            "把象征转成用户可自查的现实问题：习惯、边界、压力、表达或规划。",
            "收束为 1-3 个低风险行动，不给健康、寿命、财富、婚恋或人品断言。",
        ],
        "synthesis": {
            "core_prompt": "这些手相/面相观察更适合支持哪类自我叙事或现实整理？",
            "symbol_count": len(feature_plans),
            "grounded_actions": [
                "请用户补充本人感受、现实背景和想讨论的具体主题。",
                "把每个符号改写成一个可验证的现实观察或沟通问题。",
                "若问题涉及健康、寿命、招聘、亲密控制或第三方隐私，暂停相术解读。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not infer health, lifespan, morality, identity, wealth, relationship outcome, or social worth from appearance.",
            "Only use self-provided or clearly consented observations; do not analyze third parties without consent.",
        ],
        "next_steps": ["draft_physiognomy_answer_from_plan", "run_mystic_output_lint", "offer_reality_anchor_questions"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["observation_text"] = args.text
    if args.focus:
        payload["focus"] = args.focus
    if args.subject_is_self:
        payload["subject_is_self"] = True
    if args.consent_obtained:
        payload["consent_obtained"] = True
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
    parser.add_argument("--text", help="User-provided observation text.")
    parser.add_argument("--focus", help="Optional consultation focus.")
    parser.add_argument("--subject-is-self", action="store_true")
    parser.add_argument("--consent-obtained", action="store_true")
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
