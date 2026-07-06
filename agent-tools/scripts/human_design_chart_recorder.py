#!/usr/bin/env python3
"""Record a low-risk Human Design chart context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import human_design_request_guard


TYPE_ALIASES = {
    "显示者": "manifestor",
    "manifestor": "manifestor",
    "生产者": "generator",
    "generator": "generator",
    "显生": "manifesting_generator",
    "显示生产者": "manifesting_generator",
    "manifesting generator": "manifesting_generator",
    "manifesting_generator": "manifesting_generator",
    "投射者": "projector",
    "projector": "projector",
    "反映者": "reflector",
    "reflector": "reflector",
}


AUTHORITY_ALIASES = {
    "情绪权威": "emotional_authority",
    "emotional": "emotional_authority",
    "荐骨权威": "sacral_authority",
    "sacral": "sacral_authority",
    "脾脏权威": "splenic_authority",
    "splenic": "splenic_authority",
    "意志权威": "ego_authority",
    "ego": "ego_authority",
    "自我投射权威": "self_projected_authority",
    "self projected": "self_projected_authority",
    "环境权威": "mental_projector_authority",
    "mental projector": "mental_projector_authority",
    "月亮权威": "lunar_authority",
    "lunar": "lunar_authority",
}


def normalize_alias(raw: object, aliases: dict[str, str]) -> str:
    text = str(raw or "").strip()
    if not text:
        return ""
    lowered = text.lower().replace("-", "_")
    return aliases.get(text, aliases.get(text.lower(), aliases.get(lowered, lowered.replace(" ", "_"))))


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
    guard = human_design_request_guard.guard({"request_text": question})
    chart_source = str(payload.get("chart_source", "user_provided_or_external_chart")).strip() or "user_provided_or_external_chart"
    data_scope = str(payload.get("data_scope", "already_generated_chart_preferred")).strip() or "already_generated_chart_preferred"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    hd_type = normalize_alias(payload.get("type", payload.get("human_design_type", "")), TYPE_ALIASES)
    strategy = str(payload.get("strategy", "")).strip()
    authority = normalize_alias(payload.get("authority", payload.get("inner_authority", "")), AUTHORITY_ALIASES)
    profile = str(payload.get("profile", "")).strip()
    definition = str(payload.get("definition", "")).strip()
    centers = normalize_list(payload.get("centers", payload.get("defined_centers", "")))
    channels = normalize_list(payload.get("channels", ""))
    gates = normalize_list(payload.get("gates", ""))
    reality_constraints = normalize_list(payload.get("reality_constraints", payload.get("constraints", "")))
    notes = str(payload.get("notes", payload.get("chart_notes", ""))).strip()
    missing_fields = []
    if not hd_type:
        missing_fields.append("type")
    if not authority:
        missing_fields.append("authority")
    if not profile:
        missing_fields.append("profile")
    return {
        "tool": "human_design_chart_recorder",
        "system": "human_design_symbolic_reflection",
        "is_valid": bool(guard["can_continue_human_design"]),
        "can_continue_human_design": bool(guard["can_continue_human_design"]),
        "question_text": question,
        "chart_source": chart_source,
        "data_scope": data_scope,
        "focus": focus,
        "type": hd_type,
        "strategy": strategy,
        "authority": authority,
        "profile": profile,
        "definition": definition,
        "centers": centers,
        "channels": channels,
        "gates": gates,
        "reality_constraints": reality_constraints,
        "chart_notes": notes,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_human_design_symbols",
            "build_human_design_interpretation_plan",
            "keep_chart_source_and_missing_fields_visible",
        ] if guard["can_continue_human_design"] else ["pause_human_design_consultation", "reframe_to_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "chart_source", "data_scope", "type", "strategy", "authority", "profile", "definition", "centers", "channels", "gates", "focus"):
        value = getattr(args, attr)
        if value:
            payload["question_text" if attr == "text" else attr] = value
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
    parser.add_argument("--text", help="Human Design question or request notes.")
    parser.add_argument("--chart-source", help="user_provided, external_app, book_example.")
    parser.add_argument("--data-scope", help="already_generated_chart_preferred, birth_data_minimized.")
    parser.add_argument("--type", help="Human Design type.")
    parser.add_argument("--strategy", help="Strategy from chart.")
    parser.add_argument("--authority", help="Inner authority.")
    parser.add_argument("--profile", help="Profile, e.g. 2/4.")
    parser.add_argument("--definition", help="Definition.")
    parser.add_argument("--centers", help="Centers list.")
    parser.add_argument("--channels", help="Channels list.")
    parser.add_argument("--gates", help="Gates list.")
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
