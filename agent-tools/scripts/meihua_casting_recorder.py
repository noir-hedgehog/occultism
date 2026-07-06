#!/usr/bin/env python3
"""Record and validate Meihua Yishu casting inputs without inventing a chart."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Iterable


TRIGRAM_ELEMENTS = {
    "乾": "metal",
    "兑": "metal",
    "离": "fire",
    "震": "wood",
    "巽": "wood",
    "坎": "water",
    "艮": "earth",
    "坤": "earth",
}

ELEMENT_LABELS = {
    "wood": "木",
    "fire": "火",
    "earth": "土",
    "metal": "金",
    "water": "水",
}

GENERATES = {
    "wood": "fire",
    "fire": "earth",
    "earth": "metal",
    "metal": "water",
    "water": "wood",
}

CONTROLS = {
    "wood": "earth",
    "earth": "water",
    "water": "fire",
    "fire": "metal",
    "metal": "wood",
}

METHOD_ALIASES = {
    "number_casting": "number_casting",
    "number": "number_casting",
    "报数": "number_casting",
    "报数起卦": "number_casting",
    "time_casting": "time_casting",
    "time": "time_casting",
    "时间": "time_casting",
    "时间起卦": "time_casting",
    "external_omen": "external_omen",
    "omen": "external_omen",
    "外应": "external_omen",
    "direction_symbol": "direction_symbol",
    "direction": "direction_symbol",
    "方位": "direction_symbol",
    "external_chart": "external_chart",
    "chart": "external_chart",
    "外部卦盘": "external_chart",
    "manual_record": "manual_record",
    "manual": "manual_record",
    "手动记录": "manual_record",
}

RELATION_ALIASES = {
    "生体": "生体",
    "克体": "克体",
    "体生用": "体生用",
    "体克用": "体克用",
    "比和": "比和",
    "same_element": "比和",
    "support_body": "生体",
    "pressure_body": "克体",
    "body_supports_use": "体生用",
    "body_controls_use": "体克用",
}

RISK_PATTERNS = {
    "professional_finance": ("贷款", "股票", "投资", "梭哈", "币圈", "期货", "发财", "破财"),
    "medical_or_crisis": ("停药", "用药", "怀孕", "病", "自杀", "自伤", "伤害他人", "幻听", "幻视"),
    "legal_or_emergency": ("起诉", "报警", "火灾", "燃气", "触电", "家暴", "跟踪"),
    "coercion_or_privacy": ("控制他", "让他爱我", "查前任", "偷看", "窥探"),
    "deterministic_claim": ("必成", "必败", "一定", "百分百", "必分", "必发财", "必有灾"),
    "supernatural_fear": ("中邪", "有鬼", "天意", "报应", "诅咒", "冲撞"),
}


def text_contains_any(text: str, values: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def normalize_str(value: Any) -> str:
    return str(value or "").strip()


def normalize_method(value: Any) -> str:
    raw = normalize_str(value)
    return METHOD_ALIASES.get(raw, METHOD_ALIASES.get(raw.lower(), "manual_record"))


def normalize_numbers(value: Any) -> list[int]:
    if value in (None, ""):
        return []
    raw_items = value if isinstance(value, list) else str(value).replace("，", ",").split(",")
    numbers: list[int] = []
    for item in raw_items:
        text = normalize_str(item)
        if not text:
            continue
        try:
            numbers.append(int(text))
        except ValueError:
            continue
    return numbers


def normalize_line(value: Any, errors: list[str]) -> int | None:
    if value in (None, ""):
        return None
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
        line = int(text)
    except ValueError:
        errors.append(f"moving_line must be 1-6: {text}")
        return None
    if line < 1 or line > 6:
        errors.append(f"moving_line must be 1-6: {line}")
        return None
    return line


def normalize_trigram(value: Any, field: str, errors: list[str]) -> str:
    trigram = normalize_str(value)
    aliases = {"天": "乾", "泽": "兑", "火": "离", "雷": "震", "风": "巽", "水": "坎", "山": "艮", "地": "坤"}
    trigram = aliases.get(trigram, trigram)
    if trigram and trigram not in TRIGRAM_ELEMENTS:
        errors.append(f"{field} has invalid trigram: {trigram}")
    return trigram


def normalize_relation(value: Any) -> str:
    raw = normalize_str(value)
    return RELATION_ALIASES.get(raw, raw)


def compute_relation(body_trigram: str, use_trigram: str) -> str:
    if not body_trigram or not use_trigram:
        return ""
    body = TRIGRAM_ELEMENTS[body_trigram]
    use = TRIGRAM_ELEMENTS[use_trigram]
    if body == use:
        return "比和"
    if GENERATES[use] == body:
        return "生体"
    if CONTROLS[use] == body:
        return "克体"
    if GENERATES[body] == use:
        return "体生用"
    if CONTROLS[body] == use:
        return "体克用"
    return ""


def missing_trigger_fields(payload: dict[str, Any], method: str, numbers: list[int]) -> list[str]:
    missing = []
    if method == "number_casting" and not numbers:
        missing.append("numbers")
    if method == "time_casting":
        if not normalize_str(payload.get("cast_time")):
            missing.append("cast_time")
        if not normalize_str(payload.get("timezone")):
            missing.append("timezone")
    if method == "external_omen" and not normalize_str(payload.get("external_omen", payload.get("omen_text"))):
        missing.append("external_omen")
    if method == "direction_symbol" and not normalize_str(payload.get("direction")):
        missing.append("direction")
    if method == "external_chart" and not normalize_str(payload.get("chart_source", payload.get("external_chart_source"))):
        missing.append("chart_source")
    if method == "manual_record" and not any(
        [
            numbers,
            normalize_str(payload.get("cast_time")),
            normalize_str(payload.get("external_omen", payload.get("omen_text"))),
            normalize_str(payload.get("direction")),
            normalize_str(payload.get("chart_source", payload.get("external_chart_source"))),
        ]
    ):
        missing.append("trigger_source")
    return missing


def detect_risk_flags(payload: dict[str, Any]) -> list[str]:
    text = " ".join(
        normalize_str(payload.get(field))
        for field in ("question_text", "external_omen", "omen_text", "notes", "interpretation_request")
    )
    return [flag for flag, patterns in RISK_PATTERNS.items() if text_contains_any(text, patterns)]


def record(payload: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    method = normalize_method(payload.get("casting_method", payload.get("method", "")))
    numbers = normalize_numbers(payload.get("numbers", payload.get("reported_numbers")))
    missing_fields = missing_trigger_fields(payload, method, numbers)
    risk_flags = detect_risk_flags(payload)

    body_trigram = normalize_trigram(payload.get("body_trigram", payload.get("body")), "body_trigram", errors)
    use_trigram = normalize_trigram(payload.get("use_trigram", payload.get("use")), "use_trigram", errors)
    mutual_hexagram = normalize_str(payload.get("mutual_hexagram"))
    changed_hexagram = normalize_str(payload.get("changed_hexagram"))
    base_hexagram = normalize_str(payload.get("base_hexagram"))
    moving_line = normalize_line(payload.get("moving_line"), errors)

    if not body_trigram:
        missing_fields.append("body_trigram")
    if not use_trigram:
        missing_fields.append("use_trigram")
    if moving_line is None:
        missing_fields.append("moving_line")

    computed_relation = compute_relation(body_trigram, use_trigram)
    provided_relation = normalize_relation(payload.get("body_use_relation", payload.get("relation")))
    if provided_relation and computed_relation and provided_relation != computed_relation:
        warnings.append(f"provided body_use_relation {provided_relation} differs from computed {computed_relation}")
    if not provided_relation and not computed_relation:
        missing_fields.append("body_use_relation")
    relation = provided_relation or computed_relation

    is_valid = not errors and not missing_fields
    can_interpret = is_valid and not any(flag in risk_flags for flag in ("professional_finance", "medical_or_crisis", "legal_or_emergency", "coercion_or_privacy"))
    if "deterministic_claim" in risk_flags or "supernatural_fear" in risk_flags:
        warnings.append("deterministic or supernatural-fear wording must be reframed before interpretation")
    if missing_fields:
        warnings.append("missing casting fields prevent a complete Meihua record; ask before interpreting")

    cast_time = normalize_str(payload.get("cast_time")) or datetime.now(timezone.utc).isoformat()
    chart_source = normalize_str(payload.get("chart_source", payload.get("external_chart_source")))
    return {
        "tool": "meihua_casting_recorder",
        "system": "meihua_yishu",
        "question_text": normalize_str(payload.get("question_text")),
        "casting_method": method,
        "trigger_source": {
            "numbers": numbers,
            "cast_time": cast_time,
            "timezone": normalize_str(payload.get("timezone")) or "UTC",
            "external_omen": normalize_str(payload.get("external_omen", payload.get("omen_text"))),
            "direction": normalize_str(payload.get("direction")),
            "chart_source": chart_source,
            "notes": normalize_str(payload.get("notes")),
        },
        "body_trigram": body_trigram,
        "use_trigram": use_trigram,
        "moving_line": moving_line,
        "base_hexagram": base_hexagram,
        "mutual_hexagram": mutual_hexagram,
        "changed_hexagram": changed_hexagram,
        "body_use_relation": relation,
        "computed_body_use_relation": computed_relation,
        "trigram_elements": {
            "body": ELEMENT_LABELS[TRIGRAM_ELEMENTS[body_trigram]] if body_trigram else "",
            "use": ELEMENT_LABELS[TRIGRAM_ELEMENTS[use_trigram]] if use_trigram else "",
        },
        "risk_flags": risk_flags,
        "missing_fields": sorted(set(missing_fields)),
        "is_valid": is_valid,
        "can_interpret_meihua": can_interpret,
        "warnings": warnings,
        "next_steps": [
            "run_yijing_question_guard_for_one_matter_boundary",
            "ask_for_missing_casting_fields_before_interpretation",
            "lookup_body_use_relation_and_trigram_symbols_with_meihua_symbol_lookup",
            "map_symbols_to_observable_signals_and_low_risk_actions",
            "lint_final_output_with_mystic_output_lint",
        ],
        "limits": [
            "此工具只记录用户提供或外部工具给出的梅花字段，不自动排卦、不补数字、不编造外应。",
            "体用、生克、外应和动爻只能作为象征反思，不作为成败、疾病、财富、关系或灾祸的确定断言。",
            "涉及医疗、法律、财务、危机、人身安全或操控他人时，先暂停占问并转现实支持。",
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
    parser.add_argument("--json", help="JSON input with Meihua casting fields.")
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
