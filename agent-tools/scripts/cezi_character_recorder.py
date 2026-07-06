#!/usr/bin/env python3
"""Record a low-risk Chinese character-divination prompt."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import cezi_request_guard


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
    guard = cezi_request_guard.guard({"request_text": question})
    character = str(payload.get("character", payload.get("zi", payload.get("word", "")))).strip()
    source = str(payload.get("character_source", "user_provided")).strip() or "user_provided"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    components = normalize_list(payload.get("components", payload.get("radicals", "")))
    visible_features = normalize_list(payload.get("visible_features", payload.get("features", "")))
    user_association = str(payload.get("user_association", payload.get("association", ""))).strip()
    if not components and visible_features:
        components = visible_features
    missing_fields = []
    if not character:
        missing_fields.append("character")
    if not source:
        missing_fields.append("character_source")
    if not components and not visible_features and not user_association:
        missing_fields.append("components_or_features_or_user_association")
    return {
        "tool": "cezi_character_recorder",
        "system": "character_divination_symbolic_reflection",
        "is_valid": bool(guard["can_continue_cezi"]),
        "can_continue_cezi": bool(guard["can_continue_cezi"]),
        "question_text": question,
        "character": character,
        "character_source": source,
        "focus": focus,
        "components": components,
        "visible_features": visible_features,
        "user_association": user_association,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_cezi_symbols",
            "build_cezi_interpretation_plan",
            "keep_source_components_and_uncertainty_visible",
        ] if guard["can_continue_cezi"] else ["pause_cezi_consultation", "reframe_to_real_world_support"],
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
    if args.character:
        payload["character"] = args.character
    if args.character_source:
        payload["character_source"] = args.character_source
    if args.components:
        payload["components"] = args.components
    if args.visible_features:
        payload["visible_features"] = args.visible_features
    if args.user_association:
        payload["user_association"] = args.user_association
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
    parser.add_argument("--text", help="Cezi question or request notes.")
    parser.add_argument("--character", help="Character being interpreted.")
    parser.add_argument("--character-source", help="user_provided, random_draw, dream, name, simulated_with_consent, other.")
    parser.add_argument("--components", help="Components/radicals, e.g. 木 日 门.")
    parser.add_argument("--visible-features", help="Visible form notes, e.g. 左右结构 开口.")
    parser.add_argument("--user-association", help="User's own association with the character.")
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
