#!/usr/bin/env python3
"""Record a low-risk crystal-ball, mirror, or water-scrying observation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import scrying_request_guard


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
    question = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not question:
        raise ValueError("question_text, request_text, or text is required")
    guard = scrying_request_guard.guard({"request_text": question})
    observation_source = str(payload.get("observation_source", "user_described")).strip() or "user_described"
    observation_state = str(payload.get("observation_state", "short_completed")).strip() or "short_completed"
    medium = str(payload.get("medium", "unspecified")).strip() or "unspecified"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    visual_notes = normalize_list(payload.get("visual_notes", ""))
    surface_notes = normalize_list(payload.get("surface_notes", ""))
    feeling_notes = normalize_list(payload.get("feeling_notes", ""))
    description = str(payload.get("description", payload.get("observation_description", ""))).strip()
    if not visual_notes and not surface_notes and not feeling_notes and description:
        visual_notes = normalize_list(description)
    missing_fields = []
    if not visual_notes and not surface_notes and not feeling_notes and not description:
        missing_fields.append("observation_notes")
    if observation_state not in {"short_completed", "photo_notes", "memory_notes", "guided_visualization_ended", "unknown"}:
        missing_fields.append("safe_observation_state")
    if medium not in {"crystal_ball", "mirror", "black_mirror", "water_bowl", "photo_notes", "guided_visualization", "unspecified"}:
        missing_fields.append("medium")
    return {
        "tool": "scrying_observation_recorder",
        "system": "scrying_symbolic_reflection",
        "is_valid": bool(guard["can_continue_scrying"]),
        "can_continue_scrying": bool(guard["can_continue_scrying"]),
        "question_text": question,
        "observation_source": observation_source,
        "observation_state": observation_state,
        "medium": medium,
        "focus": focus,
        "visual_notes": visual_notes,
        "surface_notes": surface_notes,
        "feeling_notes": feeling_notes,
        "observation_description": description,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_scrying_symbols",
            "build_scrying_interpretation_plan",
            "keep_grounding_limits_visible",
        ] if guard["can_continue_scrying"] else ["pause_scrying_consultation", "reframe_to_grounding_or_real_world_support"],
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
    if args.observation_source:
        payload["observation_source"] = args.observation_source
    if args.observation_state:
        payload["observation_state"] = args.observation_state
    if args.medium:
        payload["medium"] = args.medium
    if args.visual_notes:
        payload["visual_notes"] = args.visual_notes
    if args.surface_notes:
        payload["surface_notes"] = args.surface_notes
    if args.feeling_notes:
        payload["feeling_notes"] = args.feeling_notes
    if args.description:
        payload["description"] = args.description
    if args.focus:
        payload["focus"] = args.focus
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
    parser.add_argument("--text", help="Scrying observation question or notes.")
    parser.add_argument("--observation-source", help="user_described, image_notes, memory_notes.")
    parser.add_argument("--observation-state", help="short_completed, photo_notes, memory_notes, guided_visualization_ended, unknown.")
    parser.add_argument("--medium", help="crystal_ball, mirror, black_mirror, water_bowl, photo_notes, guided_visualization.")
    parser.add_argument("--visual-notes", help="Observed visual symbols, e.g. door wave bird.")
    parser.add_argument("--surface-notes", help="Observed surface qualities, e.g. cloudy reflection.")
    parser.add_argument("--feeling-notes", help="User feeling notes.")
    parser.add_argument("--description", help="Free-text observation description.")
    parser.add_argument("--focus", help="Consultation focus.")
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
