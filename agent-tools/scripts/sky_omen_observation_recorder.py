#!/usr/bin/env python3
"""Record low-risk sky-omen observation context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import sky_omen_request_guard


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
    observation_text = str(payload.get("observation_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not observation_text:
        raise ValueError("observation_text, request_text, or text is required")
    guard = sky_omen_request_guard.guard({"request_text": observation_text})
    phenomena = normalize_list(payload.get("phenomena", ""))
    shapes = normalize_list(payload.get("shapes", ""))
    colors = normalize_list(payload.get("colors", ""))
    location_time = str(payload.get("location_time", "")).strip()
    weather_context = str(payload.get("weather_context", "")).strip()
    emotions = normalize_list(payload.get("emotions", ""))
    reality_anchor = str(payload.get("reality_anchor", "")).strip()
    focus = str(payload.get("focus", "daily_reflection")).strip() or "daily_reflection"
    missing_fields = []
    if not phenomena:
        missing_fields.append("phenomena")
    if not location_time:
        missing_fields.append("location_time")
    if not shapes and not colors and not emotions:
        missing_fields.append("shapes_colors_or_emotions")
    return {
        "tool": "sky_omen_observation_recorder",
        "system": "sky_omen_symbolic_consultation",
        "is_valid": bool(guard["can_continue_sky_omen"]),
        "can_continue_sky_omen": bool(guard["can_continue_sky_omen"]),
        "observation_text": observation_text,
        "phenomena": phenomena,
        "shapes": shapes,
        "colors": colors,
        "location_time": location_time,
        "weather_context": weather_context,
        "emotions": emotions,
        "reality_anchor": reality_anchor,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_sky_omen_symbols",
            "build_sky_omen_reflection_plan",
            "separate_symbolic_observation_from_weather_prediction",
        ] if guard["can_continue_sky_omen"] else ["pause_sky_omen_consultation", "reframe_to_weather_safety_or_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "phenomena", "shapes", "colors", "location_time", "weather_context", "emotions", "reality_anchor", "focus"):
        value = getattr(args, key)
        if value:
            payload["observation_text" if key == "text" else key] = value
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
    parser.add_argument("--text", help="Sky observation notes.")
    parser.add_argument("--phenomena", help="Sky phenomena.")
    parser.add_argument("--shapes", help="Cloud or sky shapes.")
    parser.add_argument("--colors", help="Colors or light qualities.")
    parser.add_argument("--location-time", help="Location and time.")
    parser.add_argument("--weather-context", help="Weather safety context.")
    parser.add_argument("--emotions", help="Emotions or tone.")
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
