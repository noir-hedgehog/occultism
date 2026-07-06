#!/usr/bin/env python3
"""Record and validate Qimen Dunjia chart fields without computing a chart."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any


PALACE_IDS = {1, 2, 3, 4, 5, 6, 7, 8, 9}
STEMS = {"甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", ""}
DOORS = {"休门", "生门", "伤门", "杜门", "景门", "死门", "惊门", "开门", ""}
STARS = {"天蓬", "天任", "天冲", "天辅", "天英", "天芮", "天柱", "天心", "天禽", ""}
DEITIES = {"值符", "腾蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天", ""}
TRIGRAMS = {"坎", "坤", "震", "巽", "中", "乾", "兑", "艮", "离", ""}


def normalize_str(value: Any) -> str:
    return str(value or "").strip()


def validate_enum(value: str, allowed: set[str], field: str, palace_id: int, errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"palace {palace_id} has invalid {field}: {value}")


def normalize_palace(raw: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    palace_id = int(raw.get("palace", raw.get("palace_id", 0)) or 0)
    if palace_id not in PALACE_IDS:
        errors.append(f"invalid palace id: {palace_id}")

    item = {
        "palace": palace_id,
        "trigram": normalize_str(raw.get("trigram")),
        "earth_stem": normalize_str(raw.get("earth_stem")),
        "heaven_stem": normalize_str(raw.get("heaven_stem")),
        "door": normalize_str(raw.get("door")),
        "star": normalize_str(raw.get("star")),
        "deity": normalize_str(raw.get("deity")),
        "notes": normalize_str(raw.get("notes")),
    }
    if palace_id in PALACE_IDS:
        validate_enum(item["trigram"], TRIGRAMS, "trigram", palace_id, errors)
        validate_enum(item["earth_stem"], STEMS, "earth_stem", palace_id, errors)
        validate_enum(item["heaven_stem"], STEMS, "heaven_stem", palace_id, errors)
        validate_enum(item["door"], DOORS, "door", palace_id, errors)
        validate_enum(item["star"], STARS, "star", palace_id, errors)
        validate_enum(item["deity"], DEITIES, "deity", palace_id, errors)
    return item


def validate_focus_targets(focus_targets: Any, errors: list[str]) -> list[dict[str, Any]]:
    if focus_targets is None:
        return []
    if not isinstance(focus_targets, list):
        errors.append("focus_targets must be a list when provided")
        return []
    normalized = []
    for index, target in enumerate(focus_targets, start=1):
        if not isinstance(target, dict):
            errors.append(f"focus target {index} must be an object")
            continue
        palace = int(target.get("palace", 0) or 0)
        if palace and palace not in PALACE_IDS:
            errors.append(f"focus target {index} has invalid palace: {palace}")
        normalized.append(
            {
                "label": normalize_str(target.get("label")),
                "palace": palace,
                "reason": normalize_str(target.get("reason")),
            }
        )
    return normalized


def record(payload: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    raw_palaces = payload.get("palaces")
    if not isinstance(raw_palaces, list) or not raw_palaces:
        raise ValueError("palaces must be a non-empty list")

    palaces = []
    seen: set[int] = set()
    for raw in raw_palaces:
        if not isinstance(raw, dict):
            errors.append("each palace must be an object")
            continue
        palace = normalize_palace(raw, errors)
        palace_id = int(palace["palace"])
        if palace_id in seen:
            errors.append(f"duplicate palace: {palace_id}")
        if palace_id in PALACE_IDS:
            seen.add(palace_id)
        palaces.append(palace)

    missing = sorted(PALACE_IDS - seen)
    if missing:
        warnings.append("missing palace ids: " + ",".join(str(item) for item in missing))

    dun = normalize_str(payload.get("dun"))
    if dun and dun not in {"yang", "yin", "阳遁", "阴遁"}:
        errors.append(f"invalid dun: {dun}")
    ju = payload.get("ju")
    if ju is not None:
        try:
            ju_int = int(ju)
            if ju_int < 1 or ju_int > 9:
                errors.append(f"ju must be 1-9: {ju}")
        except (TypeError, ValueError):
            errors.append(f"ju must be an integer 1-9: {ju}")
            ju_int = None
    else:
        ju_int = None

    focus_targets = validate_focus_targets(payload.get("focus_targets"), errors)

    return {
        "question_text": normalize_str(payload.get("question_text")),
        "chart_time": normalize_str(payload.get("chart_time")) or datetime.now(timezone.utc).isoformat(),
        "timezone": normalize_str(payload.get("timezone")) or "UTC",
        "location": normalize_str(payload.get("location")),
        "method": normalize_str(payload.get("method")) or "manual_record",
        "dun": dun,
        "ju": ju_int,
        "duty_star": normalize_str(payload.get("duty_star")),
        "duty_door": normalize_str(payload.get("duty_door")),
        "day_stem": normalize_str(payload.get("day_stem")),
        "hour_stem": normalize_str(payload.get("hour_stem")),
        "focus_targets": focus_targets,
        "palaces": sorted(palaces, key=lambda item: int(item["palace"])),
        "is_valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "next_steps": [
            "confirm_chart_source_and_method",
            "identify_focus_targets_and_relevant_palaces",
            "interpret_doors_stars_deities_stems_by_palace",
            "map_symbols_to_grounded_actions",
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
    parser.add_argument("--json", help="JSON input with Qimen chart fields.")
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

