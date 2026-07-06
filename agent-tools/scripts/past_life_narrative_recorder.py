#!/usr/bin/env python3
"""Record low-risk past-life/Akashic symbolic narrative context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import past_life_request_guard


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
    narrative_text = str(payload.get("narrative_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not narrative_text:
        raise ValueError("narrative_text, request_text, or text is required")
    guard = past_life_request_guard.guard({"request_text": narrative_text})
    scenes = normalize_list(payload.get("scenes", ""))
    roles = normalize_list(payload.get("roles", ""))
    symbols = normalize_list(payload.get("symbols", ""))
    emotions = normalize_list(payload.get("emotions", ""))
    source_context = str(payload.get("source_context", "symbolic_reflection")).strip() or "symbolic_reflection"
    focus = str(payload.get("focus", source_context)).strip() or source_context
    reality_anchor = str(payload.get("reality_anchor", "")).strip()
    consent_notes = str(payload.get("consent_notes", "")).strip()
    missing_fields = []
    if not scenes and not roles and not symbols and not emotions:
        missing_fields.append("scenes_roles_symbols_or_emotions")
    if not source_context:
        missing_fields.append("source_context")
    return {
        "tool": "past_life_narrative_recorder",
        "system": "past_life_akashic_symbolic_consultation",
        "is_valid": bool(guard["can_continue_past_life"]),
        "can_continue_past_life": bool(guard["can_continue_past_life"]),
        "narrative_text": narrative_text,
        "scenes": scenes,
        "roles": roles,
        "symbols": symbols,
        "emotions": emotions,
        "source_context": source_context,
        "focus": focus,
        "reality_anchor": reality_anchor,
        "consent_notes": consent_notes,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_past_life_symbols",
            "build_past_life_reflection_plan",
            "keep_symbolic_and_reality_layers_separate",
        ] if guard["can_continue_past_life"] else ["pause_past_life_consultation", "reframe_to_symbolic_or_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "scenes", "roles", "symbols", "emotions", "source_context", "focus", "reality_anchor", "consent_notes"):
        value = getattr(args, key)
        if value:
            payload["narrative_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"narrative_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Past-life/Akashic narrative notes.")
    parser.add_argument("--scenes", help="Scenes, places, or time-feel.")
    parser.add_argument("--roles", help="Roles or identities treated as symbolic images.")
    parser.add_argument("--symbols", help="Objects, colors, animals, doors, water, contracts, etc.")
    parser.add_argument("--emotions", help="Emotions or themes.")
    parser.add_argument("--source-context", help="dream, meditation, journaling, cultural_learning, etc.")
    parser.add_argument("--focus", help="Optional reflection focus.")
    parser.add_argument("--reality-anchor", help="Current-life practical anchor.")
    parser.add_argument("--consent-notes", help="Consent/privacy notes when others appear.")
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
