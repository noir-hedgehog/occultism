#!/usr/bin/env python3
"""Record a low-risk pendulum divination session."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import pendulum_request_guard


YES_NO_MARKERS = ("是不是", "要不要", "能不能", "会不会", "是否", "吗", "yes", "no")
MOTION_ALIASES = {
    "顺时针": "clockwise",
    "逆时针": "counterclockwise",
    "前后": "back_and_forth",
    "左右": "side_to_side",
    "不动": "still",
    "乱晃": "unclear",
}


def detect_question_type(text: str) -> str:
    lowered = text.lower()
    if any(marker.lower() in lowered for marker in YES_NO_MARKERS):
        return "yes_no"
    if "校准" in text or "设置" in text:
        return "calibration"
    return "open_reflection"


def detect_motion(text: str) -> str:
    if text in MOTION_ALIASES.values():
        return text
    for keyword, motion in MOTION_ALIASES.items():
        if keyword in text:
            return motion
    return "not_recorded"


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("question_text, request_text, or text is required")
    guard = pendulum_request_guard.guard({"request_text": text})
    question_type = str(payload.get("question_type", "")).strip() or detect_question_type(text)
    answer_motion_raw = str(payload.get("answer_motion", "")).strip()
    answer_motion = detect_motion(answer_motion_raw) if answer_motion_raw else detect_motion(text)
    consent_confirmed = bool(payload.get("consent_confirmed", payload.get("user_consent", False)))
    calibration_notes = str(payload.get("calibration_notes", "")).strip()
    risk_flags = list(guard["risk_flags"])
    missing_fields = []
    if question_type == "yes_no":
        missing_fields.append("reframed_open_question")
    if answer_motion == "not_recorded":
        missing_fields.append("answer_motion_or_unclear")
    if not calibration_notes:
        missing_fields.append("calibration_notes")
    can_continue = bool(guard["can_continue_pendulum"])
    return {
        "tool": "pendulum_session_recorder",
        "system": "pendulum_divination",
        "is_valid": can_continue,
        "can_continue_pendulum": can_continue,
        "question_text": text,
        "question_type": question_type,
        "answer_motion": answer_motion,
        "consent_confirmed": consent_confirmed,
        "calibration_notes": calibration_notes,
        "risk_flags": risk_flags,
        "missing_fields": missing_fields,
        "safe_question_template": "把 yes/no 改成：我现在更需要收集哪些证据、澄清哪些偏好、或采取哪一个低风险下一步？",
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_pendulum_motion_symbol",
            "compare_real_world_options",
            "build_pendulum_interpretation_plan",
        ] if can_continue else ["pause_pendulum_reading", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Pendulum session question or notes.")
    parser.add_argument("--answer-motion", help="Observed motion or answer label.")
    parser.add_argument("--calibration-notes", help="How yes/no/unclear were calibrated.")
    parser.add_argument("--consent-confirmed", action="store_true", help="User consents to symbolic reflection.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = record(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
