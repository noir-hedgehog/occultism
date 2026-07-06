#!/usr/bin/env python3
"""Guard Qimen Dunjia chart-generation method assumptions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


METHODS = {"time_chart", "event_chart", "manual_external_chart"}
SCHOOLS = {"zhirun", "chaibu", "maoshan", "feipan", "turning_plate", "unspecified"}
SOLAR_TIME = {"not_applied", "true_solar_time", "local_mean_time", "unknown"}
SOLAR_TERM_SOURCE = {"manual", "external_calendar", "future_tool_generated", "unknown"}


def normalize(raw: object) -> str:
    return str(raw or "").strip()


def normalize_choice(raw: object, allowed: set[str], aliases: dict[str, str], default: str) -> str:
    text = normalize(raw).lower()
    if not text:
        return default
    return aliases.get(text, text if text in allowed else default)


def normalize_method(raw: object) -> str:
    return normalize_choice(
        raw,
        METHODS,
        {
            "time": "time_chart",
            "event": "event_chart",
            "manual": "manual_external_chart",
            "external": "manual_external_chart",
            "时家奇门": "time_chart",
            "事件局": "event_chart",
            "外部盘": "manual_external_chart",
        },
        "time_chart",
    )


def normalize_school(raw: object) -> str:
    return normalize_choice(
        raw,
        SCHOOLS,
        {
            "置闰": "zhirun",
            "拆补": "chaibu",
            "茅山": "maoshan",
            "飞盘": "feipan",
            "转盘": "turning_plate",
            "未知": "unspecified",
        },
        "unspecified",
    )


def normalize_solar_time(raw: object) -> str:
    return normalize_choice(
        raw,
        SOLAR_TIME,
        {
            "真太阳时": "true_solar_time",
            "平太阳时": "local_mean_time",
            "不校正": "not_applied",
            "未知": "unknown",
        },
        "unknown",
    )


def normalize_solar_term_source(raw: object) -> str:
    return normalize_choice(
        raw,
        SOLAR_TERM_SOURCE,
        {
            "手动": "manual",
            "外部万年历": "external_calendar",
            "工具生成": "future_tool_generated",
            "未知": "unknown",
        },
        "unknown",
    )


def looks_like_datetime(value: object) -> bool:
    text = normalize(value)
    return bool(re.match(r"^(?:19|20)\d{2}-\d{1,2}-\d{1,2}(?:[ T]\d{1,2}:\d{2})?", text))


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    method = normalize_method(payload.get("chart_method", payload.get("method")))
    school = normalize_school(payload.get("school"))
    solar_time_strategy = normalize_solar_time(payload.get("solar_time_strategy"))
    solar_term_source = normalize_solar_term_source(payload.get("solar_term_source"))
    chart_time = normalize(payload.get("chart_time"))
    timezone = normalize(payload.get("timezone"))
    location = normalize(payload.get("location"))
    errors: list[str] = []
    warnings: list[str] = []
    assumptions: list[str] = []

    if method != "manual_external_chart" and not chart_time:
        errors.append("chart_time is required before generating a Qimen chart")
    elif chart_time and not looks_like_datetime(chart_time):
        warnings.append("chart_time is not normalized; prefer YYYY-MM-DD HH:MM")
    if method != "manual_external_chart" and not timezone:
        errors.append("timezone is required before generating a Qimen chart")
    if method != "manual_external_chart" and not location:
        errors.append("location is required before generating a Qimen chart")
    if school == "unspecified":
        errors.append("school must be declared, such as zhirun or chaibu, before generation")
    if school in {"zhirun", "chaibu"} and solar_term_source == "unknown":
        errors.append("solar_term_source is required for zhirun/chaibu boundary handling")
    if solar_time_strategy == "unknown":
        warnings.append("solar_time_strategy is unknown; generated chart must not claim solar-time precision")
        assumptions.append("solar_time_strategy=unknown")
    if method == "manual_external_chart":
        warnings.append("manual_external_chart records external chart assumptions only; do not regenerate palaces")
    if payload.get("dun") and normalize(payload.get("dun")) not in {"yang", "yin", "阳遁", "阴遁"}:
        errors.append("dun must be yang/yin when provided")
    if payload.get("ju") is not None:
        try:
            ju = int(payload["ju"])
            if ju < 1 or ju > 9:
                errors.append("ju must be 1-9 when provided")
                ju = None
        except (TypeError, ValueError):
            errors.append("ju must be an integer 1-9 when provided")
            ju = None
    else:
        ju = None

    can_generate = not errors and method != "manual_external_chart"
    return {
        "chart_method": method,
        "school": school,
        "chart_time": chart_time,
        "timezone": timezone,
        "location": location,
        "solar_time_strategy": solar_time_strategy,
        "solar_term_source": solar_term_source,
        "dun": normalize(payload.get("dun")),
        "ju": ju,
        "can_generate_chart": can_generate,
        "is_external_chart_only": method == "manual_external_chart",
        "errors": errors,
        "warnings": warnings,
        "assumptions": assumptions,
        "required_before_generation": errors,
        "limits": [
            "This tool records Qimen generation assumptions only; it does not compute a chart.",
            "Do not mix zhirun, chaibu, feipan, and turning-plate conventions without declaring the school.",
            "If solar time or solar-term source is unclear, mark the chart as method-limited before interpretation.",
        ],
        "next_steps": [
            "resolve_required_before_generation",
            "generate_chart_with_declared_qimen_engine_when_available",
            "record_or_validate_palaces_with_qimen_chart_record",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload.update(json.load(f))
    if args.method:
        payload["method"] = args.method
    if args.school:
        payload["school"] = args.school
    if args.chart_time:
        payload["chart_time"] = args.chart_time
    if args.timezone:
        payload["timezone"] = args.timezone
    if args.location:
        payload["location"] = args.location
    if payload:
        return payload
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --json, --file, or method parameters")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON method input.")
    parser.add_argument("--file", help="Path to JSON input.")
    parser.add_argument("--method", help="time_chart, event_chart, or manual_external_chart.")
    parser.add_argument("--school", help="zhirun, chaibu, maoshan, feipan, turning_plate.")
    parser.add_argument("--chart-time", help="Chart datetime.")
    parser.add_argument("--timezone", help="Timezone label.")
    parser.add_argument("--location", help="Location label.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
