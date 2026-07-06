#!/usr/bin/env python3
"""Record low-risk aura/chakra sensation context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import aura_chakra_request_guard


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
    sensation_text = str(payload.get("sensation_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not sensation_text:
        raise ValueError("sensation_text, request_text, or text is required")
    guard = aura_chakra_request_guard.guard({"request_text": sensation_text})
    centers = normalize_list(payload.get("centers", payload.get("chakras", "")))
    colors = normalize_list(payload.get("colors", ""))
    sensations = normalize_list(payload.get("sensations", ""))
    context = str(payload.get("context", "symbolic_reflection")).strip() or "symbolic_reflection"
    duration = str(payload.get("duration", "")).strip()
    intensity = str(payload.get("intensity", "")).strip()
    grounding_notes = str(payload.get("grounding_notes", "")).strip()
    focus = str(payload.get("focus", context)).strip() or context
    missing_fields = []
    if not centers and not colors and not sensations:
        missing_fields.append("centers_colors_or_sensations")
    if not context:
        missing_fields.append("context")
    return {
        "tool": "aura_chakra_sensation_recorder",
        "system": "aura_chakra_symbolic_consultation",
        "is_valid": bool(guard["can_continue_aura_chakra"]),
        "can_continue_aura_chakra": bool(guard["can_continue_aura_chakra"]),
        "sensation_text": sensation_text,
        "centers": centers,
        "colors": colors,
        "sensations": sensations,
        "context": context,
        "duration": duration,
        "intensity": intensity,
        "grounding_notes": grounding_notes,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_aura_chakra_symbols",
            "build_aura_chakra_reflection_plan",
            "keep_body_and_grounding_context_visible",
        ] if guard["can_continue_aura_chakra"] else ["pause_aura_chakra_consultation", "reframe_to_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "centers", "colors", "sensations", "context", "duration", "intensity", "grounding_notes", "focus"):
        value = getattr(args, key)
        if value:
            payload["sensation_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"sensation_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Aura/chakra sensation notes.")
    parser.add_argument("--centers", help="Chakra or body centers.")
    parser.add_argument("--colors", help="Aura or chakra colors.")
    parser.add_argument("--sensations", help="Sensation words.")
    parser.add_argument("--context", help="meditation, journaling, relationship_boundary, workspace, etc.")
    parser.add_argument("--duration", help="Duration note.")
    parser.add_argument("--intensity", help="Intensity note.")
    parser.add_argument("--grounding-notes", help="Grounding or body-state notes.")
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
