#!/usr/bin/env python3
"""Record authorized object context for psychometry-style symbolic reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import psychometry_request_guard


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
    object_text = str(payload.get("object_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not object_text:
        raise ValueError("object_text, request_text, or text is required")
    guard = psychometry_request_guard.guard({"request_text": object_text})
    object_types = normalize_list(payload.get("object_types", payload.get("objects", "")))
    source_notes = str(payload.get("source_notes", payload.get("source", ""))).strip()
    ownership_status = str(payload.get("ownership_status", payload.get("consent_status", ""))).strip()
    visible_features = normalize_list(payload.get("visible_features", payload.get("features", "")))
    impressions = normalize_list(payload.get("impressions", ""))
    emotions = normalize_list(payload.get("emotions", ""))
    reality_anchor = str(payload.get("reality_anchor", "")).strip()
    focus = str(payload.get("focus", "memory_boundary_reflection")).strip() or "memory_boundary_reflection"
    missing_fields = []
    if not object_types:
        missing_fields.append("object_types")
    if not ownership_status:
        missing_fields.append("ownership_or_consent_status")
    if not visible_features and not impressions and not emotions:
        missing_fields.append("features_impressions_or_emotions")
    return {
        "tool": "psychometry_object_recorder",
        "system": "psychometry_symbolic_consultation",
        "is_valid": bool(guard["can_continue_psychometry"]),
        "can_continue_psychometry": bool(guard["can_continue_psychometry"]),
        "object_text": object_text,
        "object_types": object_types,
        "source_notes": source_notes,
        "ownership_status": ownership_status,
        "visible_features": visible_features,
        "impressions": impressions,
        "emotions": emotions,
        "reality_anchor": reality_anchor,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_psychometry_symbols",
            "build_psychometry_reflection_plan",
            "separate_object_impressions_from_fact_or_identification",
        ] if guard["can_continue_psychometry"] else ["pause_psychometry_consultation", "reframe_to_real_world_support_or_consent"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "object_types", "source_notes", "ownership_status", "visible_features", "impressions", "emotions", "reality_anchor", "focus"):
        value = getattr(args, key)
        if value:
            payload["object_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"object_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Object-reading notes.")
    parser.add_argument("--object-types", help="Object types.")
    parser.add_argument("--source-notes", help="Object source notes.")
    parser.add_argument("--ownership-status", help="Ownership or consent status.")
    parser.add_argument("--visible-features", help="Visible features.")
    parser.add_argument("--impressions", help="Symbolic impressions.")
    parser.add_argument("--emotions", help="Emotions or tones.")
    parser.add_argument("--reality-anchor", help="Current-life practical anchor.")
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
