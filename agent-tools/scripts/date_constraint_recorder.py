#!/usr/bin/env python3
"""Record practical constraints for symbolic auspicious-date selection."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from typing import Any

import date_selection_guard


DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")


def parse_dates(items: Any, text: str = "") -> list[str]:
    dates: list[str] = []
    if isinstance(items, list):
        dates.extend(str(item) for item in items)
    elif isinstance(items, str):
        dates.extend(DATE_RE.findall(items))
    if text:
        dates.extend(DATE_RE.findall(text))
    normalized: list[str] = []
    for item in dates:
        try:
            normalized.append(date.fromisoformat(item).isoformat())
        except ValueError:
            continue
    return sorted(set(normalized))


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text and not payload.get("candidate_dates"):
        raise ValueError("request_text/text or candidate_dates is required")
    guard = date_selection_guard.guard(payload if text else {"request_text": "择日", **payload})
    candidates = parse_dates(payload.get("candidate_dates"), text)
    unavailable = parse_dates(payload.get("unavailable_dates"), str(payload.get("unavailable_text", "")))
    participants = list(payload.get("participants", []) or [])
    practical_constraints = list(payload.get("practical_constraints", []) or [])
    if "周末" in text or "weekend" in text.lower():
        practical_constraints.append("prefer_weekend")
    if "上午" in text or "早上" in text:
        practical_constraints.append("prefer_morning")
    if "老人" in text:
        practical_constraints.append("elder_accessibility")
    if "消防" in text or "物业" in text:
        practical_constraints.append("site_permission_or_safety")
    missing_fields = []
    if not candidates:
        missing_fields.append("candidate_dates")
    if not practical_constraints:
        missing_fields.append("practical_constraints")
    return {
        "tool": "date_constraint_recorder",
        "is_valid": bool(guard["can_continue_date_selection"]),
        "event_type": guard["event_type"],
        "can_continue_date_selection": guard["can_continue_date_selection"],
        "candidate_dates": candidates,
        "unavailable_dates": unavailable,
        "participant_count": len(participants),
        "participants": participants,
        "practical_constraints": sorted(set(practical_constraints)),
        "source_notes": list(payload.get("source_notes", []) or []),
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "questions_to_ask": [
            "候选日期有哪些，哪些日期现实上不可用？",
            "场地、证件、合同、交通、长辈时间和安全要求是否已确认？",
            "是否有外部黄历来源；如果有，来源名称和截图/条目是什么？",
        ],
        "next_steps": [
            "lookup_user_mentioned_almanac_terms",
            "rank_candidate_dates",
            "keep_practical_constraints_above_symbolic_preferences",
        ] if guard["can_continue_date_selection"] else guard["next_steps"],
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
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="User request or constraint text.")
    parser.add_argument("--event-type", help="Optional event type.")
    parser.add_argument("--candidate-date", action="append", help="Candidate date in YYYY-MM-DD. Can be repeated.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
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
