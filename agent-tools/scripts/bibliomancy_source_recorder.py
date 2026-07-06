#!/usr/bin/env python3
"""Record source and short excerpt context for bibliomancy reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import bibliomancy_request_guard


def normalize_list(raw: object) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    text = str(raw or "").strip()
    if not text:
        return []
    for sep in ("、", ",", "，", "/", "|", "；", ";", "+", "和"):
        text = text.replace(sep, " ")
    return [part.strip() for part in text.split() if part.strip()]


def record(payload: dict[str, Any]) -> dict[str, Any]:
    query_text = str(payload.get("query_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not query_text:
        raise ValueError("query_text, request_text, or text is required")
    guard = bibliomancy_request_guard.guard({"request_text": query_text})
    source_title = str(payload.get("source_title", "")).strip()
    source_type = str(payload.get("source_type", "book_or_user_source")).strip() or "book_or_user_source"
    selection_method = str(payload.get("selection_method", "")).strip()
    page_or_location = str(payload.get("page_or_location", "")).strip()
    excerpt = str(payload.get("excerpt", "")).strip()
    keywords = normalize_list(payload.get("keywords", ""))
    emotions = normalize_list(payload.get("emotions", ""))
    reality_anchor = str(payload.get("reality_anchor", "")).strip()
    focus = str(payload.get("focus", "reading_reflection")).strip() or "reading_reflection"
    missing_fields = []
    if not source_title:
        missing_fields.append("source_title")
    if not excerpt and not keywords:
        missing_fields.append("excerpt_or_keywords")
    if len(excerpt) > 260:
        missing_fields.append("excerpt_too_long_for_bibliomancy_record")
    return {
        "tool": "bibliomancy_source_recorder",
        "system": "bibliomancy_symbolic_consultation",
        "is_valid": bool(guard["can_continue_bibliomancy"]) and len(excerpt) <= 260,
        "can_continue_bibliomancy": bool(guard["can_continue_bibliomancy"]) and len(excerpt) <= 260,
        "query_text": query_text,
        "source_title": source_title,
        "source_type": source_type,
        "selection_method": selection_method,
        "page_or_location": page_or_location,
        "excerpt": excerpt,
        "keywords": keywords,
        "emotions": emotions,
        "reality_anchor": reality_anchor,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_bibliomancy_symbols",
            "build_bibliomancy_reflection_plan",
            "separate_short_excerpt_from_authority_or_fate",
        ] if guard["can_continue_bibliomancy"] and len(excerpt) <= 260 else ["pause_bibliomancy_consultation", "reframe_to_real_world_support_or_short_user_excerpt"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "source_title", "source_type", "selection_method", "page_or_location", "excerpt", "keywords", "emotions", "reality_anchor", "focus"):
        value = getattr(args, key)
        if value:
            payload["query_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Bibliomancy notes.")
    parser.add_argument("--source-title", help="Book/source title.")
    parser.add_argument("--source-type", help="Book, poem, scripture, article, user notebook, etc.")
    parser.add_argument("--selection-method", help="How the passage was selected.")
    parser.add_argument("--page-or-location", help="Page, chapter, or location.")
    parser.add_argument("--excerpt", help="Short user-provided excerpt.")
    parser.add_argument("--keywords", help="Keywords from the passage.")
    parser.add_argument("--emotions", help="Emotions or tones.")
    parser.add_argument("--reality-anchor", help="Current practical anchor.")
    parser.add_argument("--focus", help="Optional focus.")
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
