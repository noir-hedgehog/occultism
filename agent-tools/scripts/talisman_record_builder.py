#!/usr/bin/env python3
"""Record a low-risk talisman or charm consultation context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import talisman_request_guard


CONTEXT_ALIASES = {
    "佩戴": "wearing",
    "随身": "carrying",
    "钱包": "carrying",
    "书桌": "workspace",
    "办公桌": "workspace",
    "床头": "bedside",
    "门口": "entrance",
    "车里": "vehicle",
    "礼物": "gift",
    "保存": "storage",
}


def normalize_items(raw: object) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    text = str(raw or "").strip()
    if not text:
        return []
    for sep in ("、", ",", "，", "/", "|", "；", ";", "和"):
        text = text.replace(sep, " ")
    return [part.strip() for part in text.split() if part.strip()]


def detect_use_context(text: str) -> str:
    for keyword, context in CONTEXT_ALIASES.items():
        if keyword in text:
            return context
    return "symbolic_reflection"


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("intention_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("intention_text, request_text, or text is required")
    guard = talisman_request_guard.guard({"request_text": text})
    items = normalize_items(payload.get("items", payload.get("talismans", "")))
    source_type = str(payload.get("source_type", "unknown")).strip() or "unknown"
    source_label = str(payload.get("source_label", "")).strip()
    use_context = str(payload.get("use_context", "")).strip() or detect_use_context(text)
    budget_note = str(payload.get("budget_note", "")).strip()
    missing_fields = []
    if not items:
        missing_fields.append("talisman_name_or_visible_symbols")
    if source_type == "unknown" and not source_label:
        missing_fields.append("source_type_or_source_label")
    if not budget_note:
        missing_fields.append("budget_or_existing_item_note")
    return {
        "tool": "talisman_record_builder",
        "system": "talisman_symbolic_reflection",
        "is_valid": bool(guard["can_continue_talisman"]),
        "can_continue_talisman": bool(guard["can_continue_talisman"]),
        "intention_text": text,
        "items": items,
        "item_count": len(items),
        "source_type": source_type,
        "source_label": source_label,
        "use_context": use_context,
        "budget_note": budget_note,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_talisman_symbols",
            "build_talisman_use_plan",
            "keep_source_and_budget_visible",
        ] if guard["can_continue_talisman"] else ["pause_talisman_consultation", "reframe_to_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["intention_text"] = args.text
    if args.items:
        payload["items"] = args.items
    if args.source_type:
        payload["source_type"] = args.source_type
    if args.source_label:
        payload["source_label"] = args.source_label
    if args.use_context:
        payload["use_context"] = args.use_context
    if args.budget_note:
        payload["budget_note"] = args.budget_note
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"intention_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Talisman intention or request notes.")
    parser.add_argument("--items", help="Talisman names or visible symbols.")
    parser.add_argument("--source-type", help="temple, daoist_temple, family_gift, store, unknown.")
    parser.add_argument("--source-label", help="Short source label.")
    parser.add_argument("--use-context", help="wearing, carrying, workspace, entrance, etc.")
    parser.add_argument("--budget-note", help="Existing item or budget note.")
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
