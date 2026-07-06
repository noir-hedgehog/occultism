#!/usr/bin/env python3
"""Record a low-risk bone, shell, stone, or charm-casting layout."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import casting_lots_request_guard


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
    guard = casting_lots_request_guard.guard({"request_text": question})
    casting_system = str(payload.get("casting_system", "charm_casting")).strip() or "charm_casting"
    casting_surface = str(payload.get("casting_surface", "")).strip()
    layout_source = str(payload.get("layout_source", "user_provided")).strip() or "user_provided"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    objects = normalize_list(payload.get("objects", payload.get("items", "")))
    zones = normalize_list(payload.get("zones", ""))
    relationships = str(payload.get("relationships", payload.get("layout_notes", ""))).strip()
    if not objects and relationships:
        objects = normalize_list(relationships)
    missing_fields = []
    if not objects:
        missing_fields.append("objects_or_layout_notes")
    if not casting_surface:
        missing_fields.append("casting_surface")
    if not zones and not relationships:
        missing_fields.append("zones_or_relationships")
    return {
        "tool": "casting_lots_layout_recorder",
        "system": "casting_lots_symbolic_reflection",
        "is_valid": bool(guard["can_continue_casting_lots"]),
        "can_continue_casting_lots": bool(guard["can_continue_casting_lots"]),
        "question_text": question,
        "casting_system": casting_system,
        "casting_surface": casting_surface,
        "layout_source": layout_source,
        "focus": focus,
        "objects": objects,
        "zones": zones,
        "relationships": relationships,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_casting_lots_symbols",
            "build_casting_lots_interpretation_plan",
            "keep_objects_zones_and_uncertainty_visible",
        ] if guard["can_continue_casting_lots"] else ["pause_casting_lots_consultation", "reframe_to_real_world_support"],
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
    if args.casting_system:
        payload["casting_system"] = args.casting_system
    if args.casting_surface:
        payload["casting_surface"] = args.casting_surface
    if args.layout_source:
        payload["layout_source"] = args.layout_source
    if args.objects:
        payload["objects"] = args.objects
    if args.zones:
        payload["zones"] = args.zones
    if args.relationships:
        payload["relationships"] = args.relationships
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
    parser.add_argument("--text", help="Casting lots question or request notes.")
    parser.add_argument("--casting-system", help="bone_casting, shell_casting, stone_casting, charm_casting, custom.")
    parser.add_argument("--casting-surface", help="mat, cloth, bowl, floor, table, drawn_zones, unknown.")
    parser.add_argument("--layout-source", help="user_provided, simulated_with_consent, external_app.")
    parser.add_argument("--objects", help="Cast objects, e.g. shell key stone feather.")
    parser.add_argument("--zones", help="Layout zones, e.g. center left future.")
    parser.add_argument("--relationships", help="Free-text relation notes.")
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
