#!/usr/bin/env python3
"""Record and validate Liuyao chart fields without casting or inventing lines."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Iterable


LINE_POSITIONS = {
    1: "初爻",
    2: "二爻",
    3: "三爻",
    4: "四爻",
    5: "五爻",
    6: "上爻",
}

KINSHIPS = {"父母", "兄弟", "子孙", "妻财", "官鬼", ""}
SPIRITS = {"青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武", ""}
ROLES = {"世爻", "应爻", "用神", "原神", "忌神", "仇神", ""}
YIN_YANG = {"yin", "yang", "阴", "阳", ""}
BRANCHES = {"子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", ""}
ELEMENTS = {"wood", "fire", "earth", "metal", "water", "木", "火", "土", "金", "水", ""}

METHOD_ALIASES = {
    "coin": "coin_casting",
    "coins": "coin_casting",
    "three_coins": "coin_casting",
    "铜钱": "coin_casting",
    "铜钱起卦": "coin_casting",
    "manual": "manual_record",
    "manual_record": "manual_record",
    "手动记录": "manual_record",
    "external_chart": "external_chart",
    "external": "external_chart",
    "外部卦盘": "external_chart",
    "time": "time_casting",
    "time_casting": "time_casting",
    "时间起卦": "time_casting",
    "unknown": "unknown",
    "未知": "unknown",
}

RISK_PATTERNS = {
    "professional_finance": ("贷款", "股票", "投资", "梭哈", "币圈", "期货", "发财", "破财"),
    "medical_or_crisis": ("停药", "用药", "怀孕", "病", "自杀", "自伤", "伤害他人", "幻听", "幻视"),
    "legal_or_emergency": ("起诉", "报警", "火灾", "燃气", "触电", "家暴", "跟踪"),
    "coercion_or_privacy": ("控制他", "让他爱我", "查前任", "偷看", "窥探", "跟踪对方"),
    "deterministic_claim": ("必成", "必败", "一定", "百分百", "必分", "必发财", "必有灾"),
    "supernatural_fear": ("中邪", "有鬼", "报应", "诅咒", "冲撞"),
}


def normalize_str(value: Any) -> str:
    return str(value or "").strip()


def contains_any(text: str, values: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def normalize_method(value: Any) -> str:
    raw = normalize_str(value)
    return METHOD_ALIASES.get(raw, METHOD_ALIASES.get(raw.lower(), "unknown"))


def normalize_position(value: Any, errors: list[str]) -> int:
    aliases = {
        "初爻": 1,
        "一爻": 1,
        "二爻": 2,
        "三爻": 3,
        "四爻": 4,
        "五爻": 5,
        "上爻": 6,
        "六爻": 6,
    }
    text = normalize_str(value)
    if text in aliases:
        return aliases[text]
    try:
        position = int(text)
    except ValueError:
        errors.append(f"line position must be 1-6: {text}")
        return 0
    if position < 1 or position > 6:
        errors.append(f"line position must be 1-6: {position}")
        return 0
    return position


def normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return normalize_str(value).lower() in {"1", "true", "yes", "动", "动爻", "changing"}


def validate_choice(value: str, allowed: set[str], field: str, position: int, errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"{LINE_POSITIONS.get(position, position)} has invalid {field}: {value}")


def normalize_roles(raw_roles: Any) -> list[str]:
    if raw_roles in (None, ""):
        return []
    if isinstance(raw_roles, list):
        items = raw_roles
    else:
        items = str(raw_roles).replace("，", ",").split(",")
    normalized = []
    aliases = {"世": "世爻", "应": "应爻", "用": "用神", "原": "原神", "忌": "忌神", "仇": "仇神"}
    for item in items:
        role = aliases.get(normalize_str(item), normalize_str(item))
        if role:
            normalized.append(role)
    return normalized


def normalize_line(raw: Any, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(raw, dict):
        errors.append("each line must be an object")
        return None
    position = normalize_position(raw.get("position", raw.get("line", raw.get("index"))), errors)
    if not position:
        return None
    kinship = normalize_str(raw.get("kinship"))
    spirit = normalize_str(raw.get("spirit"))
    roles = normalize_roles(raw.get("roles", raw.get("role")))
    branch = normalize_str(raw.get("branch"))
    element = normalize_str(raw.get("element"))
    yin_yang = normalize_str(raw.get("yin_yang", raw.get("value"))).lower()
    if yin_yang == "阴":
        yin_yang = "yin"
    if yin_yang == "阳":
        yin_yang = "yang"

    validate_choice(kinship, KINSHIPS, "kinship", position, errors)
    validate_choice(spirit, SPIRITS, "spirit", position, errors)
    validate_choice(branch, BRANCHES, "branch", position, errors)
    validate_choice(element, ELEMENTS, "element", position, errors)
    validate_choice(yin_yang, YIN_YANG, "yin_yang", position, errors)
    for role in roles:
        validate_choice(role, ROLES, "role", position, errors)

    return {
        "position": position,
        "position_label": LINE_POSITIONS[position],
        "yin_yang": yin_yang,
        "kinship": kinship,
        "spirit": spirit,
        "roles": roles,
        "branch": branch,
        "element": element,
        "changing": normalize_bool(raw.get("changing", raw.get("is_changing"))),
        "hidden_kinship": normalize_str(raw.get("hidden_kinship")),
        "notes": normalize_str(raw.get("notes")),
    }


def detect_risk_flags(payload: dict[str, Any]) -> list[str]:
    text = " ".join(
        normalize_str(payload.get(field))
        for field in ("question_text", "notes", "focus_logic", "interpretation_request")
    )
    return [flag for flag, patterns in RISK_PATTERNS.items() if contains_any(text, patterns)]


def missing_chart_fields(payload: dict[str, Any], method: str, lines: list[dict[str, Any]]) -> list[str]:
    missing = []
    if method == "unknown":
        missing.append("casting_method")
    if method == "external_chart" and not normalize_str(payload.get("chart_source", payload.get("external_chart_source"))):
        missing.append("chart_source")
    if method == "time_casting":
        if not normalize_str(payload.get("cast_time")):
            missing.append("cast_time")
        if not normalize_str(payload.get("timezone")):
            missing.append("timezone")
    if not normalize_str(payload.get("base_hexagram")):
        missing.append("base_hexagram")
    if not lines:
        missing.append("lines")
    if len(lines) != 6:
        missing.append("six_lines")
    if not any("世爻" in line["roles"] for line in lines):
        missing.append("self_line")
    if not any("应爻" in line["roles"] for line in lines):
        missing.append("other_line")
    if not normalize_str(payload.get("focus_spirit", payload.get("focus_kinship"))):
        missing.append("focus_spirit")
    if not normalize_str(payload.get("focus_logic")):
        missing.append("focus_logic")
    return sorted(set(missing))


def record(payload: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    raw_lines = payload.get("lines")
    if raw_lines is None:
        raw_lines = []
    if not isinstance(raw_lines, list):
        raise ValueError("lines must be a list of six line objects")

    lines = []
    seen: set[int] = set()
    for raw in raw_lines:
        line = normalize_line(raw, errors)
        if line is None:
            continue
        position = int(line["position"])
        if position in seen:
            errors.append(f"duplicate line position: {position}")
        seen.add(position)
        lines.append(line)

    lines = sorted(lines, key=lambda item: int(item["position"]))
    missing_positions = [position for position in range(1, 7) if position not in seen]
    if missing_positions:
        warnings.append("missing line positions: " + ",".join(str(item) for item in missing_positions))

    method = normalize_method(payload.get("casting_method", payload.get("method")))
    risk_flags = detect_risk_flags(payload)
    missing_fields = missing_chart_fields(payload, method, lines)
    is_valid = not errors and not missing_fields
    can_interpret = is_valid and not any(
        flag in risk_flags for flag in ("professional_finance", "medical_or_crisis", "legal_or_emergency", "coercion_or_privacy")
    )
    if "deterministic_claim" in risk_flags or "supernatural_fear" in risk_flags:
        warnings.append("deterministic or supernatural-fear wording must be reframed before interpretation")
    if missing_fields:
        warnings.append("missing chart fields prevent a complete Liuyao record; ask before interpreting")

    changing_lines = [line["position"] for line in lines if line["changing"]]
    focus_spirit = normalize_str(payload.get("focus_spirit", payload.get("focus_kinship")))
    return {
        "tool": "liuyao_chart_recorder",
        "system": "liuyao",
        "question_text": normalize_str(payload.get("question_text")),
        "casting_method": method,
        "chart_source": normalize_str(payload.get("chart_source", payload.get("external_chart_source"))),
        "cast_time": normalize_str(payload.get("cast_time")) or datetime.now(timezone.utc).isoformat(),
        "timezone": normalize_str(payload.get("timezone")) or "UTC",
        "base_hexagram": normalize_str(payload.get("base_hexagram")),
        "changed_hexagram": normalize_str(payload.get("changed_hexagram")),
        "changing_lines": changing_lines,
        "focus_spirit": focus_spirit,
        "focus_logic": normalize_str(payload.get("focus_logic")),
        "lines": lines,
        "risk_flags": risk_flags,
        "missing_fields": missing_fields,
        "is_valid": is_valid,
        "can_interpret_liuyao": can_interpret,
        "errors": errors,
        "warnings": warnings,
        "next_steps": [
            "run_yijing_question_guard_for_one_matter_boundary",
            "ask_for_missing_chart_fields_before_interpretation",
            "lookup_focus_spirit_self_other_and_changing_lines_with_liuyao_symbol_lookup",
            "map_symbols_to_observable_signals_and_low_risk_actions",
            "lint_final_output_with_mystic_output_lint",
        ],
        "limits": [
            "此工具只记录用户提供或外部工具给出的六爻盘字段，不自动起卦、不补世应、不编造用神。",
            "六亲、六神、世应、用神和动爻只能作为象征反思，不作为成败、疾病、财富、关系或灾祸的确定断言。",
            "涉及医疗、法律、财务、危机、人身安全、第三方隐私或操控他人时，先暂停占问并转现实支持。",
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
    parser.add_argument("--json", help="JSON input with Liuyao chart fields.")
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
