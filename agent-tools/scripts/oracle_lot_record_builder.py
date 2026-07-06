#!/usr/bin/env python3
"""Record oracle-lot source, question, lot text, and interpretation fields."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

import oracle_lot_request_guard


LOT_NUMBER_RE = re.compile(r"(?:第)?([一二三四五六七八九十百零〇\d]{1,4})(?:签|号)")
GRADE_KEYWORDS = {
    "great_auspicious": ("上上签", "大吉", "上吉"),
    "auspicious": ("上签", "中上", "吉"),
    "mixed": ("中签", "中平", "平"),
    "challenging": ("下签", "下下签", "凶", "不利"),
}
SOURCE_KEYWORDS = {
    "temple": ("寺", "庙", "宫", "观", "现场"),
    "book": ("书", "签诗集", "纸本"),
    "app": ("app", "小程序", "网页", "在线"),
    "user_drawn": ("我抽到", "已抽", "抽到"),
    "simulation": ("帮我抽", "模拟抽签", "在线抽签"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_source_type(text: str) -> str:
    for source_type, keywords in SOURCE_KEYWORDS.items():
        if contains_any(text, keywords):
            return source_type
    return "unknown"


def detect_grade(text: str) -> str:
    for grade, keywords in GRADE_KEYWORDS.items():
        if contains_any(text, keywords):
            return grade
    return "unspecified"


def extract_lot_number(text: str) -> str:
    match = LOT_NUMBER_RE.search(text)
    return match.group(1) if match else ""


def record(payload: dict[str, Any]) -> dict[str, Any]:
    request_text = str(payload.get("request_text", payload.get("question_text", ""))).strip()
    lot_text = str(payload.get("lot_text", payload.get("text", ""))).strip()
    combined = " ".join(part for part in [request_text, lot_text] if part).strip()
    if not combined:
        raise ValueError("request_text, question_text, lot_text, or text is required")
    guard = oracle_lot_request_guard.guard({"request_text": combined})
    source_type = str(payload.get("source_type", "")).strip() or detect_source_type(combined)
    lot_number = str(payload.get("lot_number", "")).strip() or extract_lot_number(combined)
    grade = str(payload.get("lot_grade", "")).strip() or detect_grade(combined)
    missing_fields = []
    if not request_text:
        missing_fields.append("question_text")
    if not lot_text and source_type != "simulation":
        missing_fields.append("lot_text")
    if source_type == "unknown":
        missing_fields.append("source_type")
    return {
        "tool": "oracle_lot_record_builder",
        "system": "oracle_lot_symbolism",
        "is_valid": bool(guard["can_continue_oracle_lot"]),
        "can_continue_oracle_lot": bool(guard["can_continue_oracle_lot"]),
        "question_text": request_text,
        "lot_text": lot_text,
        "source_type": source_type,
        "source_label": str(payload.get("source_label", "")).strip(),
        "lot_number": lot_number,
        "lot_grade": grade,
        "draw_method": str(payload.get("draw_method", "")).strip() or ("simulation" if source_type == "simulation" else "user_provided"),
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_grade_and_source_symbols",
            "build_interpretation_plan",
            "ask_for_lot_text_if_missing",
        ] if guard["can_continue_oracle_lot"] else guard["next_steps"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.question:
        payload["question_text"] = args.question
    if args.lot_text:
        payload["lot_text"] = args.lot_text
    if args.source_type:
        payload["source_type"] = args.source_type
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"lot_text": raw}
    raise ValueError("Provide --question/--lot-text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", help="User question.")
    parser.add_argument("--lot-text", help="Oracle lot text.")
    parser.add_argument("--source-type", help="temple, book, app, user_drawn, simulation, or unknown.")
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
