#!/usr/bin/env python3
"""Record and validate Bazi / Ziwei chart preparation parameters."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


SYSTEM_ALIASES = {
    "bazi": ("bazi", "八字", "四柱", "生辰八字"),
    "ziwei": ("ziwei", "紫微", "紫微斗数", "斗数"),
}

CALENDAR_ALIASES = {
    "solar": ("solar", "gregorian", "公历", "阳历", "新历"),
    "lunar": ("lunar", "农历", "阴历", "旧历"),
    "unknown": ("unknown", "未知", "不确定"),
}

SOLAR_TIME_STRATEGIES = {
    "not_applied",
    "true_solar_time",
    "local_mean_time",
    "unknown",
}

CHART_SOURCES = {
    "manual_user_provided",
    "external_calculator",
    "future_tool_generated",
    "cultural_explanation_only",
}

BAZI_SCHOOLS = {
    "unspecified",
    "ziping",
    "traditional",
    "modern_synthesis",
}

ZIWEI_SCHOOLS = {
    "unspecified",
    "sanhe",
    "sihua",
    "zhongzhou",
    "modern_synthesis",
}

FOCUS_VALUES = {
    "career",
    "relationship",
    "self_understanding",
    "timing",
    "family",
    "general",
}

SENSITIVE_MARKERS = ("身份证", "手机号", "住址", "真实姓名", "姓名全名")


def normalize_choice(value: object, aliases: dict[str, tuple[str, ...]], default: str) -> str:
    raw = str(value or "").strip().lower()
    if not raw:
        return default
    for canonical, candidates in aliases.items():
        if raw == canonical or any(raw == candidate.lower() for candidate in candidates):
            return canonical
    return default


def normalize_system(value: object, text: str = "") -> str:
    raw = str(value or "").strip().lower()
    combined = f"{raw} {text}".lower()
    for system, aliases in SYSTEM_ALIASES.items():
        if raw == system or any(alias.lower() in combined for alias in aliases):
            return system
    return "mingli"


def normalize_calendar(value: object, text: str = "") -> str:
    if value:
        return normalize_choice(value, CALENDAR_ALIASES, "unknown")
    return normalize_choice(text, CALENDAR_ALIASES, "unknown")


def normalize_school(system: str, value: object) -> str:
    raw = str(value or "unspecified").strip().lower()
    allowed = BAZI_SCHOOLS if system == "bazi" else ZIWEI_SCHOOLS if system == "ziwei" else {"unspecified", "modern_synthesis"}
    return raw if raw in allowed else "unspecified"


def normalize_solar_time_strategy(value: object) -> str:
    raw = str(value or "").strip().lower()
    aliases = {
        "不校正": "not_applied",
        "不用": "not_applied",
        "真太阳时": "true_solar_time",
        "平太阳时": "local_mean_time",
        "未知": "unknown",
    }
    if raw in SOLAR_TIME_STRATEGIES:
        return raw
    return aliases.get(str(value or "").strip(), "unknown")


def normalize_chart_source(value: object) -> str:
    raw = str(value or "").strip().lower()
    aliases = {
        "manual": "manual_user_provided",
        "user": "manual_user_provided",
        "external": "external_calculator",
        "generated": "future_tool_generated",
        "cultural": "cultural_explanation_only",
    }
    if raw in CHART_SOURCES:
        return raw
    return aliases.get(raw, "manual_user_provided")


def normalize_focus(value: object) -> str:
    raw = str(value or "general").strip().lower()
    return raw if raw in FOCUS_VALUES else "general"


def looks_like_date(value: object) -> bool:
    raw = str(value or "").strip()
    return bool(re.match(r"^(?:19|20)\d{2}[-/.年]\d{1,2}(?:[-/.月]\d{1,2})?(?:日)?$", raw))


def looks_like_time(value: object) -> bool:
    raw = str(value or "").strip()
    if raw in {"子时", "丑时", "寅时", "卯时", "辰时", "巳时", "午时", "未时", "申时", "酉时", "戌时", "亥时"}:
        return True
    return bool(re.match(r"^\d{1,2}:\d{2}$", raw))


def privacy_flags(payload: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    if payload.get("birth_date") or payload.get("birth_time") or payload.get("birth_datetime"):
        flags.append("exact_birth_data")
    if payload.get("subject_is_self") is False:
        flags.append("third_party_subject")
    if payload.get("subject_is_minor") is True:
        flags.append("minor_subject")
    text = " ".join(str(value) for value in payload.values() if isinstance(value, str))
    if any(marker in text for marker in SENSITIVE_MARKERS):
        flags.append("sensitive_identity")
    return flags


def validate(payload: dict[str, Any], system: str, calendar: str, solar_time_strategy: str, chart_source: str) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    assumptions: list[str] = []

    if system == "mingli":
        errors.append("system must be bazi or ziwei for chart parameter recording")
    if not payload.get("birth_date") and not payload.get("birth_datetime"):
        errors.append("birth_date is required")
    elif payload.get("birth_date") and not looks_like_date(payload.get("birth_date")):
        warnings.append("birth_date format is not normalized; prefer YYYY-MM-DD with calendar_type")
    if not payload.get("birth_time") and not payload.get("birth_datetime"):
        errors.append("birth_time is required")
    elif payload.get("birth_time") and not looks_like_time(payload.get("birth_time")):
        warnings.append("birth_time is not HH:MM or a standard Chinese double-hour label")
    if not payload.get("birth_place"):
        errors.append("birth_place is required")
    if calendar == "unknown":
        errors.append("calendar_type must be solar or lunar before chart generation")
    if not payload.get("timezone"):
        warnings.append("timezone missing; defaulting to Asia/Shanghai for record only")
        assumptions.append("timezone=Asia/Shanghai")
    if solar_time_strategy == "unknown":
        warnings.append("solar_time_strategy is unknown; record cannot claim true-solar-time precision")
    if chart_source == "cultural_explanation_only":
        warnings.append("chart_source is cultural_explanation_only; do not interpret as a calculated chart")
    if payload.get("subject_is_self") is False and payload.get("subject_consent") is not True:
        errors.append("subject_consent is required for third-party chart parameters")

    flags = privacy_flags(payload)
    if "sensitive_identity" in flags:
        errors.append("do not record direct identity fields such as ID number, phone, address, or full legal name")
    if "minor_subject" in flags:
        warnings.append("minor subject: only non-labeling, supportive language is allowed")
    return errors, warnings, assumptions


def record(payload: dict[str, Any]) -> dict[str, Any]:
    request_text = str(payload.get("request_text", "")).strip()
    system = normalize_system(payload.get("system", payload.get("domain")), request_text)
    calendar = normalize_calendar(payload.get("calendar_type"), request_text)
    solar_time_strategy = normalize_solar_time_strategy(payload.get("solar_time_strategy"))
    chart_source = normalize_chart_source(payload.get("chart_source"))
    school = normalize_school(system, payload.get("school"))
    focus = normalize_focus(payload.get("analysis_focus"))
    timezone = str(payload.get("timezone") or "Asia/Shanghai")
    errors, warnings, assumptions = validate(payload, system, calendar, solar_time_strategy, chart_source)
    flags = privacy_flags(payload)

    birth_data = {
        "birth_date": str(payload.get("birth_date", "")).strip(),
        "birth_time": str(payload.get("birth_time", "")).strip(),
        "birth_place": str(payload.get("birth_place", "")).strip(),
        "calendar_type": calendar,
        "timezone": timezone,
        "solar_time_strategy": solar_time_strategy,
    }
    method = {
        "system": system,
        "school": school,
        "chart_source": chart_source,
        "analysis_focus": focus,
        "gender_policy": str(payload.get("gender_policy", "record_only_if_method_requires_it")),
    }

    required_before_interpretation = []
    if errors:
        required_before_interpretation.extend(errors)
    if solar_time_strategy == "unknown":
        required_before_interpretation.append("confirm solar_time_strategy")
    if "minor_subject" in flags:
        required_before_interpretation.append("confirm non-labeling minor-safe framing")

    return {
        "system": system,
        "birth_data": birth_data,
        "method": method,
        "privacy_flags": flags,
        "is_valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "assumptions": assumptions,
        "required_before_interpretation": required_before_interpretation,
        "limits": [
            "This record stores chart parameters only; it does not generate stems, branches, palaces, stars, or fate claims.",
            "Do not record direct identity fields; use the minimum birth data needed for the chosen method.",
            "Any later interpretation must remain symbolic, non-deterministic, and scoped to low-risk reflection.",
        ],
        "next_steps": [
            "run_bazi_ziwei_intake_guard_first",
            "confirm_calendar_timezone_and_solar_time_strategy",
            "generate_or_enter_chart_fields_with_declared_source",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.text:
        return {"request_text": args.text, "system": args.system}
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --json, --file, --text, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON chart parameter input.")
    parser.add_argument("--file", help="Path to JSON input.")
    parser.add_argument("--text", help="Loose request text; structured JSON is preferred.")
    parser.add_argument("--system", help="Optional system: bazi or ziwei.")
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
