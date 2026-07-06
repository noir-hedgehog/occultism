#!/usr/bin/env python3
"""Record a low-risk Western geomancy shield chart."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import western_geomancy_request_guard


FIGURE_ALIASES = {
    "populus": "populus",
    "人群": "populus",
    "大众": "populus",
    "via": "via",
    "道路": "via",
    "路": "via",
    "fortuna_major": "fortuna_major",
    "fortuna major": "fortuna_major",
    "大吉": "fortuna_major",
    "fortuna_minor": "fortuna_minor",
    "fortuna minor": "fortuna_minor",
    "小吉": "fortuna_minor",
    "conjunctio": "conjunctio",
    "结合": "conjunctio",
    "连接": "conjunctio",
    "carcer": "carcer",
    "牢笼": "carcer",
    "拘束": "carcer",
    "puella": "puella",
    "少女": "puella",
    "puer": "puer",
    "少年": "puer",
    "rubeus": "rubeus",
    "红色": "rubeus",
    "albus": "albus",
    "白色": "albus",
    "acquisitio": "acquisitio",
    "获得": "acquisitio",
    "amissio": "amissio",
    "失去": "amissio",
    "laetitia": "laetitia",
    "喜悦": "laetitia",
    "tristitia": "tristitia",
    "忧伤": "tristitia",
    "caput_draconis": "caput_draconis",
    "caput draconis": "caput_draconis",
    "龙头": "caput_draconis",
    "cauda_draconis": "cauda_draconis",
    "cauda draconis": "cauda_draconis",
    "龙尾": "cauda_draconis",
}


def normalize_list(raw: object) -> list[str]:
    if isinstance(raw, list):
        parts = [str(item).strip() for item in raw if str(item).strip()]
    else:
        text = str(raw or "").strip()
        if not text:
            return []
        replacements = {
            "Fortuna Major": "fortuna_major",
            "fortuna major": "fortuna_major",
            "Fortuna Minor": "fortuna_minor",
            "fortuna minor": "fortuna_minor",
            "Caput Draconis": "caput_draconis",
            "caput draconis": "caput_draconis",
            "Cauda Draconis": "cauda_draconis",
            "cauda draconis": "cauda_draconis",
        }
        for source, target in replacements.items():
            text = text.replace(source, target)
        for sep in ("、", ",", "，", "/", "|", "；", ";", "+", "和"):
            text = text.replace(sep, " ")
        parts = [part.strip() for part in text.split() if part.strip()]
    return [FIGURE_ALIASES.get(part.lower(), FIGURE_ALIASES.get(part, part)) for part in parts]


def record(payload: dict[str, Any]) -> dict[str, Any]:
    question = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not question:
        raise ValueError("question_text, request_text, or text is required")
    guard = western_geomancy_request_guard.guard({"request_text": question})
    chart_source = str(payload.get("chart_source", "user_provided")).strip() or "user_provided"
    generation_method = str(payload.get("generation_method", "four_line_points")).strip() or "four_line_points"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    mothers = normalize_list(payload.get("mothers", payload.get("mother_figures", "")))
    daughters = normalize_list(payload.get("daughters", payload.get("daughter_figures", "")))
    nieces = normalize_list(payload.get("nieces", payload.get("niece_figures", "")))
    witnesses = normalize_list(payload.get("witnesses", ""))
    judge = normalize_list(payload.get("judge", ""))
    notes = str(payload.get("chart_notes", payload.get("notes", ""))).strip()
    all_figures = mothers + daughters + nieces + witnesses + judge
    missing_fields = []
    if len(mothers) < 4:
        missing_fields.append("four_mother_figures")
    if len(witnesses) < 2:
        missing_fields.append("two_witnesses")
    if not judge:
        missing_fields.append("judge")
    if not all_figures and notes:
        all_figures = normalize_list(notes)
    return {
        "tool": "western_geomancy_chart_recorder",
        "system": "western_geomancy_symbolic_reflection",
        "is_valid": bool(guard["can_continue_western_geomancy"]),
        "can_continue_western_geomancy": bool(guard["can_continue_western_geomancy"]),
        "question_text": question,
        "chart_source": chart_source,
        "generation_method": generation_method,
        "focus": focus,
        "mothers": mothers,
        "daughters": daughters,
        "nieces": nieces,
        "witnesses": witnesses,
        "judge": judge[:1],
        "all_figures": all_figures,
        "chart_notes": notes,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_western_geomancy_figures",
            "build_western_geomancy_interpretation_plan",
            "keep_chart_source_and_missing_fields_visible",
        ] if guard["can_continue_western_geomancy"] else ["pause_western_geomancy_consultation", "reframe_to_real_world_support"],
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
    if args.chart_source:
        payload["chart_source"] = args.chart_source
    if args.generation_method:
        payload["generation_method"] = args.generation_method
    if args.mothers:
        payload["mothers"] = args.mothers
    if args.daughters:
        payload["daughters"] = args.daughters
    if args.nieces:
        payload["nieces"] = args.nieces
    if args.witnesses:
        payload["witnesses"] = args.witnesses
    if args.judge:
        payload["judge"] = args.judge
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
    parser.add_argument("--text", help="Western geomancy question or request notes.")
    parser.add_argument("--chart-source", help="user_provided, simulated_with_consent, external_app.")
    parser.add_argument("--generation-method", help="four_line_points, app_generated, historical_example, custom.")
    parser.add_argument("--mothers", help="Four mother figures.")
    parser.add_argument("--daughters", help="Daughter figures.")
    parser.add_argument("--nieces", help="Niece figures.")
    parser.add_argument("--witnesses", help="Two witness figures.")
    parser.add_argument("--judge", help="Judge figure.")
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
