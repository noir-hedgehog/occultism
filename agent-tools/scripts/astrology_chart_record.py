#!/usr/bin/env python3
"""Record and validate externally provided astrology chart fields without computing a chart."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


CHART_SOURCES = {
    "external_calculator",
    "manual_user_provided",
    "user_memory",
    "cultural_explanation_only",
}

FOCUS_VALUES = {
    "self_understanding",
    "career",
    "relationship",
    "daily_prompt",
    "creative_reflection",
    "general",
}

PLACEMENT_TYPES = {
    "planet",
    "sign",
    "house",
    "point",
    "aspect",
    "emphasis",
}

SIGNS = {
    "白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
    "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座",
}

SIGN_ALIASES = {
    "白羊": "白羊座",
    "金牛": "金牛座",
    "双子": "双子座",
    "巨蟹": "巨蟹座",
    "狮子": "狮子座",
    "处女": "处女座",
    "天秤": "天秤座",
    "天平": "天秤座",
    "天蝎": "天蝎座",
    "射手": "射手座",
    "摩羯": "摩羯座",
    "魔羯": "摩羯座",
    "水瓶": "水瓶座",
    "双鱼": "双鱼座",
}

PLANETS = {"太阳", "月亮", "水星", "金星", "火星", "木星", "土星", "天王星", "海王星", "冥王星"}
POINTS = {"上升", "下降", "天顶", "天底"}
ASPECTS = {"合相", "对冲", "拱相", "刑相", "六合"}
HOUSE_PATTERN = re.compile(r"^(?:[一二三四五六七八九十]|十一|十二|[1-9]|1[0-2])宫$")
SENSITIVE_MARKERS = ("身份证", "手机号", "住址", "真实姓名", "姓名全名")


def normalize_source(value: object) -> str:
    raw = str(value or "").strip().lower()
    aliases = {
        "external": "external_calculator",
        "calculator": "external_calculator",
        "manual": "manual_user_provided",
        "user": "manual_user_provided",
        "memory": "user_memory",
        "cultural": "cultural_explanation_only",
    }
    if raw in CHART_SOURCES:
        return raw
    return aliases.get(raw, "manual_user_provided")


def normalize_focus(value: object) -> str:
    raw = str(value or "general").strip().lower()
    return raw if raw in FOCUS_VALUES else "general"


def normalize_type(value: object) -> str:
    raw = str(value or "").strip().lower()
    aliases = {
        "星体": "planet",
        "行星": "planet",
        "星座": "sign",
        "宫位": "house",
        "四轴": "point",
        "轴点": "point",
        "相位": "aspect",
        "重点": "emphasis",
        "强调": "emphasis",
    }
    if raw in PLACEMENT_TYPES:
        return raw
    return aliases.get(str(value or "").strip(), "")


def normalize_sign(value: object) -> str:
    text = str(value or "").strip()
    return SIGN_ALIASES.get(text, text)


def normalize_house(value: object) -> str:
    text = str(value or "").strip()
    aliases = {
        "1宫": "一宫",
        "第1宫": "一宫",
        "2宫": "二宫",
        "第2宫": "二宫",
        "3宫": "三宫",
        "第3宫": "三宫",
        "4宫": "四宫",
        "第4宫": "四宫",
        "5宫": "五宫",
        "第5宫": "五宫",
        "6宫": "六宫",
        "第6宫": "六宫",
        "7宫": "七宫",
        "第7宫": "七宫",
        "8宫": "八宫",
        "第8宫": "八宫",
        "9宫": "九宫",
        "第9宫": "九宫",
        "10宫": "十宫",
        "第10宫": "十宫",
        "11宫": "十一宫",
        "第11宫": "十一宫",
        "12宫": "十二宫",
        "第12宫": "十二宫",
    }
    return aliases.get(text, text)


def contains_exact_birth_data(payload: dict[str, Any]) -> bool:
    if payload.get("birth_date") or payload.get("birth_time") or payload.get("birth_datetime"):
        return True
    text = " ".join(str(value) for value in payload.values() if isinstance(value, str))
    return bool(re.search(r"(?:19|20)\d{2}[-年/.]\d{1,2}[-月/.]\d{1,2}", text) and re.search(r"\d{1,2}:\d{2}", text))


def privacy_flags(payload: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    if contains_exact_birth_data(payload):
        flags.append("exact_birth_data")
    if payload.get("subject_is_self") is False:
        flags.append("third_party_subject")
    if payload.get("subject_is_minor") is True:
        flags.append("minor_subject")
    text = " ".join(str(value) for value in payload.values() if isinstance(value, str))
    if any(marker in text for marker in SENSITIVE_MARKERS):
        flags.append("sensitive_identity")
    return flags


def normalize_placement(raw: dict[str, Any], errors: list[str], warnings: list[str]) -> dict[str, Any]:
    item_type = normalize_type(raw.get("type", raw.get("placement_type")))
    if not item_type:
        errors.append("placement type is required")
        item_type = "unknown"

    name = str(raw.get("name", raw.get("body", raw.get("point", "")))).strip()
    sign = normalize_sign(raw.get("sign", ""))
    house = normalize_house(raw.get("house", ""))
    aspect_to = str(raw.get("aspect_to", "")).strip()
    aspect = str(raw.get("aspect", raw.get("name", ""))).strip()
    notes = str(raw.get("notes", "")).strip()

    if item_type == "planet" and name not in PLANETS:
        errors.append(f"unknown planet placement: {name}")
    if item_type == "point" and name not in POINTS:
        errors.append(f"unknown chart point: {name}")
    if sign and sign not in SIGNS:
        errors.append(f"unknown sign: {sign}")
    if house and not HOUSE_PATTERN.match(house):
        errors.append(f"unknown house: {house}")
    if item_type == "aspect" and aspect not in ASPECTS:
        errors.append(f"unknown aspect: {aspect}")
    if item_type == "aspect" and not aspect_to:
        warnings.append("aspect placement missing aspect_to; interpretation will be limited")

    return {
        "type": item_type,
        "name": name,
        "sign": sign,
        "house": house,
        "aspect": aspect if item_type == "aspect" else "",
        "aspect_to": aspect_to,
        "notes": notes,
    }


def validate(payload: dict[str, Any], chart_source: str, placements: list[dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required_before_interpretation: list[str] = []
    flags = privacy_flags(payload)

    if chart_source == "cultural_explanation_only" and placements:
        warnings.append("chart_source is cultural_explanation_only; placements should be treated as examples, not a personal chart")
    if not placements and chart_source != "cultural_explanation_only":
        errors.append("at least one externally provided placement is required")
    if "third_party_subject" in flags and payload.get("subject_consent") is not True:
        errors.append("subject_consent is required for third-party chart fields")
    if "sensitive_identity" in flags:
        errors.append("do not record direct identity fields such as ID number, phone, address, or full legal name")
    if "exact_birth_data" in flags:
        warnings.append("exact birth data should be minimized after chart fields are recorded")
        required_before_interpretation.append("minimize exact birth data in logs and final answer")
    if "minor_subject" in flags:
        warnings.append("minor subject: use non-labeling and supportive language only")
        required_before_interpretation.append("confirm non-labeling minor-safe framing")
    return errors, warnings, required_before_interpretation


def record(payload: dict[str, Any]) -> dict[str, Any]:
    chart_source = normalize_source(payload.get("chart_source"))
    focus = normalize_focus(payload.get("analysis_focus", payload.get("focus")))
    placement_errors: list[str] = []
    warnings: list[str] = []
    raw_placements = payload.get("placements", [])
    if raw_placements is None:
        raw_placements = []
    if not isinstance(raw_placements, list):
        raise ValueError("placements must be a list")
    placements = []
    for raw in raw_placements:
        if not isinstance(raw, dict):
            placement_errors.append("each placement must be an object")
            continue
        placements.append(normalize_placement(raw, placement_errors, warnings))

    errors, validation_warnings, required = validate(payload, chart_source, placements)
    errors = placement_errors + errors
    warnings.extend(validation_warnings)
    flags = privacy_flags(payload)

    return {
        "system": "western_astrology",
        "chart_source": chart_source,
        "analysis_focus": focus,
        "subject": {
            "subject_is_self": payload.get("subject_is_self"),
            "subject_consent": bool(payload.get("subject_consent")),
            "subject_is_minor": bool(payload.get("subject_is_minor")),
        },
        "placements": placements,
        "privacy_flags": flags,
        "is_valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "required_before_interpretation": required + errors,
        "limits": [
            "This record stores externally provided astrology fields only; it does not calculate a chart.",
            "Do not keep or repeat exact birth data when chart placements are already available.",
            "Any interpretation must remain symbolic, non-deterministic, and scoped to low-risk reflection.",
        ],
        "next_steps": [
            "run_mystic_intake_triage_first",
            "confirm_chart_source_subject_consent_and_birth_data_minimization",
            "lookup_relevant_symbols_with_astrology_symbol_lookup",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --json, --file, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON astrology chart-field input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = record(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
