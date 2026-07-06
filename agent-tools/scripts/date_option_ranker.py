#!/usr/bin/env python3
"""Rank candidate dates by practical constraints and symbolic preferences."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from typing import Any

import date_constraint_recorder


def weekday_name(iso_date: str) -> str:
    names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return names[date.fromisoformat(iso_date).weekday()]


def score_date(iso_date: str, record: dict[str, Any], symbolic_preferences: list[str]) -> dict[str, Any]:
    score = 0
    reasons: list[str] = []
    cautions: list[str] = []
    weekday = weekday_name(iso_date)
    if iso_date in record["unavailable_dates"]:
        score -= 100
        cautions.append("date_marked_unavailable")
    if "prefer_weekend" in record["practical_constraints"] and weekday in {"Saturday", "Sunday"}:
        score += 3
        reasons.append("matches_weekend_preference")
    if "elder_accessibility" in record["practical_constraints"]:
        score += 1
        reasons.append("requires_accessibility_check_before_finalizing")
    if "site_permission_or_safety" in record["practical_constraints"]:
        cautions.append("confirm_site_permission_or_safety_first")
    if "纪念" in symbolic_preferences or "memorial" in symbolic_preferences:
        score += 1
        reasons.append("symbolic_memorial_preference_noted")
    if "避开冲" in symbolic_preferences:
        cautions.append("zodiac_conflict_preference_requires_user_provided_source")
    return {
        "date": iso_date,
        "weekday": weekday,
        "score": score,
        "reasons": reasons or ["usable_candidate_if_practical_constraints_pass"],
        "cautions": cautions,
    }


def rank(payload: dict[str, Any]) -> dict[str, Any]:
    record = date_constraint_recorder.record(payload)
    symbolic_preferences = list(payload.get("symbolic_preferences", []) or [])
    if not record["can_continue_date_selection"]:
        return {
            "tool": "date_option_ranker",
            "is_valid": False,
            "can_rank_dates": False,
            "event_type": record["event_type"],
            "ranked_dates": [],
            "risk_flags": record["risk_flags"],
            "limits": [
                "Do not rank dates when the request asks to replace professional or safety judgment.",
                "Resolve medical, legal, financial, safety or dangerous ritual issues first.",
            ],
            "next_steps": record["next_steps"],
        }
    ranked = [score_date(item, record, symbolic_preferences) for item in record["candidate_dates"]]
    ranked.sort(key=lambda item: (item["score"], item["date"]), reverse=True)
    return {
        "tool": "date_option_ranker",
        "is_valid": bool(record["candidate_dates"]),
        "can_rank_dates": bool(record["candidate_dates"]),
        "event_type": record["event_type"],
        "candidate_count": len(record["candidate_dates"]),
        "ranked_dates": ranked,
        "risk_flags": record["risk_flags"],
        "selection_guidance": [
            "先排除现实不可用或安全/手续未确认的日期。",
            "再按家庭协调、场地、交通、纪念意义和用户提供的黄历偏好排序。",
            "输出时使用偏好和建议语言，不使用必吉、必凶或保证结果语言。",
        ],
        "limits": [
            "This tool does not calculate authoritative almanac data.",
            "User-provided almanac notes must be cited as source-limited context.",
            "Practical constraints outrank symbolic preferences.",
        ],
        "next_steps": ["draft_date_selection_answer", "cite_source_limits", "run_mystic_output_lint"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["request_text"] = args.text
    if args.event_type:
        payload["event_type"] = args.event_type
    if args.candidate_date:
        payload["candidate_dates"] = args.candidate_date
    if payload:
        return payload
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --text, --json, --file, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="User request or constraint text.")
    parser.add_argument("--event-type", help="Optional event type.")
    parser.add_argument("--candidate-date", action="append", help="Candidate date in YYYY-MM-DD. Can be repeated.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()
    try:
        result = rank(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
