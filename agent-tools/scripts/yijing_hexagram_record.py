#!/usr/bin/env python3
"""Record and validate Yijing hexagram casting data."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any


TRIGRAMS = {
    "111": {"name": "乾", "image": "天", "symbol": "☰"},
    "110": {"name": "兑", "image": "泽", "symbol": "☱"},
    "101": {"name": "离", "image": "火", "symbol": "☲"},
    "100": {"name": "震", "image": "雷", "symbol": "☳"},
    "011": {"name": "巽", "image": "风", "symbol": "☴"},
    "010": {"name": "坎", "image": "水", "symbol": "☵"},
    "001": {"name": "艮", "image": "山", "symbol": "☶"},
    "000": {"name": "坤", "image": "地", "symbol": "☷"},
}

ORDER = ("乾", "兑", "离", "震", "巽", "坎", "艮", "坤")

HEXAGRAM_MATRIX = {
    "乾": {
        "乾": (1, "乾为天"),
        "兑": (43, "泽天夬"),
        "离": (14, "火天大有"),
        "震": (34, "雷天大壮"),
        "巽": (9, "风天小畜"),
        "坎": (5, "水天需"),
        "艮": (26, "山天大畜"),
        "坤": (11, "地天泰"),
    },
    "兑": {
        "乾": (10, "天泽履"),
        "兑": (58, "兑为泽"),
        "离": (38, "火泽睽"),
        "震": (54, "雷泽归妹"),
        "巽": (61, "风泽中孚"),
        "坎": (60, "水泽节"),
        "艮": (41, "山泽损"),
        "坤": (19, "地泽临"),
    },
    "离": {
        "乾": (13, "天火同人"),
        "兑": (49, "泽火革"),
        "离": (30, "离为火"),
        "震": (55, "雷火丰"),
        "巽": (37, "风火家人"),
        "坎": (63, "水火既济"),
        "艮": (22, "山火贲"),
        "坤": (36, "地火明夷"),
    },
    "震": {
        "乾": (25, "天雷无妄"),
        "兑": (17, "泽雷随"),
        "离": (21, "火雷噬嗑"),
        "震": (51, "震为雷"),
        "巽": (42, "风雷益"),
        "坎": (3, "水雷屯"),
        "艮": (27, "山雷颐"),
        "坤": (24, "地雷复"),
    },
    "巽": {
        "乾": (44, "天风姤"),
        "兑": (28, "泽风大过"),
        "离": (50, "火风鼎"),
        "震": (32, "雷风恒"),
        "巽": (57, "巽为风"),
        "坎": (48, "水风井"),
        "艮": (18, "山风蛊"),
        "坤": (46, "地风升"),
    },
    "坎": {
        "乾": (6, "天水讼"),
        "兑": (47, "泽水困"),
        "离": (64, "火水未济"),
        "震": (40, "雷水解"),
        "巽": (59, "风水涣"),
        "坎": (29, "坎为水"),
        "艮": (4, "山水蒙"),
        "坤": (7, "地水师"),
    },
    "艮": {
        "乾": (33, "天山遁"),
        "兑": (31, "泽山咸"),
        "离": (56, "火山旅"),
        "震": (62, "雷山小过"),
        "巽": (53, "风山渐"),
        "坎": (39, "水山蹇"),
        "艮": (52, "艮为山"),
        "坤": (15, "地山谦"),
    },
    "坤": {
        "乾": (12, "天地否"),
        "兑": (45, "泽地萃"),
        "离": (35, "火地晋"),
        "震": (16, "雷地豫"),
        "巽": (20, "风地观"),
        "坎": (8, "水地比"),
        "艮": (23, "山地剥"),
        "坤": (2, "坤为地"),
    },
}


def normalize_line(raw: Any, index: int) -> tuple[dict[str, Any] | None, str | None]:
    if isinstance(raw, dict):
        value = raw.get("value", raw.get("line", raw.get("type")))
        changing = raw.get("changing")
    else:
        value = raw
        changing = None

    if isinstance(value, bool):
        yin_yang = "yang" if value else "yin"
        is_changing = bool(changing) if changing is not None else False
        numeric_value = 9 if yin_yang == "yang" and is_changing else 7 if yin_yang == "yang" else 6 if is_changing else 8
    else:
        token = str(value).strip().lower()
        aliases = {
            "6": ("yin", True, 6),
            "old_yin": ("yin", True, 6),
            "老阴": ("yin", True, 6),
            "8": ("yin", False, 8),
            "young_yin": ("yin", False, 8),
            "少阴": ("yin", False, 8),
            "yin": ("yin", bool(changing) if changing is not None else False, 6 if changing else 8),
            "阴": ("yin", bool(changing) if changing is not None else False, 6 if changing else 8),
            "0": ("yin", bool(changing) if changing is not None else False, 6 if changing else 8),
            "7": ("yang", False, 7),
            "young_yang": ("yang", False, 7),
            "少阳": ("yang", False, 7),
            "9": ("yang", True, 9),
            "old_yang": ("yang", True, 9),
            "老阳": ("yang", True, 9),
            "yang": ("yang", bool(changing) if changing is not None else False, 9 if changing else 7),
            "阳": ("yang", bool(changing) if changing is not None else False, 9 if changing else 7),
            "1": ("yang", bool(changing) if changing is not None else False, 9 if changing else 7),
        }
        if token not in aliases:
            return None, f"line {index} has unknown value: {value}"
        yin_yang, is_changing, numeric_value = aliases[token]

    bit = "1" if yin_yang == "yang" else "0"
    changed_bit = "0" if bit == "1" and is_changing else "1" if bit == "0" and is_changing else bit
    return (
        {
            "index": index,
            "value": numeric_value,
            "yin_yang": yin_yang,
            "changing": is_changing,
            "bit": bit,
            "changed_bit": changed_bit,
            "label": ("老" if is_changing else "少") + ("阳" if yin_yang == "yang" else "阴"),
        },
        None,
    )


def trigram_from_bits(bits: str) -> dict[str, str]:
    trigram = TRIGRAMS[bits]
    return {"bits": bits, **trigram}


def hexagram_from_bits(bits: str) -> dict[str, Any]:
    lower = trigram_from_bits(bits[:3])
    upper = trigram_from_bits(bits[3:])
    number, name = HEXAGRAM_MATRIX[lower["name"]][upper["name"]]
    return {
        "number": number,
        "name": name,
        "bits_bottom_to_top": bits,
        "lower_trigram": lower,
        "upper_trigram": upper,
    }


def record(payload: dict[str, Any]) -> dict[str, Any]:
    raw_lines = payload.get("lines", payload.get("line_values"))
    if not isinstance(raw_lines, list):
        raise ValueError("lines or line_values must be a list of six line values")

    errors: list[str] = []
    warnings: list[str] = []
    if len(raw_lines) != 6:
        errors.append(f"expected 6 lines from bottom to top, got {len(raw_lines)}")

    normalized_lines = []
    for index, raw in enumerate(raw_lines[:6], start=1):
        line, error = normalize_line(raw, index)
        if error:
            errors.append(error)
        elif line:
            normalized_lines.append(line)

    base_hexagram = None
    changed_hexagram = None
    changing_lines: list[int] = []
    if len(normalized_lines) == 6:
        base_bits = "".join(str(line["bit"]) for line in normalized_lines)
        changed_bits = "".join(str(line["changed_bit"]) for line in normalized_lines)
        changing_lines = [int(line["index"]) for line in normalized_lines if line["changing"]]
        base_hexagram = hexagram_from_bits(base_bits)
        changed_hexagram = hexagram_from_bits(changed_bits) if changing_lines else None

        expected_number = payload.get("expected_hexagram_number")
        expected_name = str(payload.get("expected_hexagram_name", "")).strip()
        if expected_number is not None and int(expected_number) != base_hexagram["number"]:
            warnings.append(f"expected hexagram number {expected_number}, computed {base_hexagram['number']}")
        if expected_name and expected_name not in base_hexagram["name"]:
            warnings.append(f"expected hexagram name {expected_name}, computed {base_hexagram['name']}")

    return {
        "question_text": str(payload.get("question_text", "")).strip(),
        "casting_method": str(payload.get("casting_method", "manual_record")).strip() or "manual_record",
        "cast_time": str(payload.get("cast_time", datetime.now(timezone.utc).isoformat())),
        "timezone": str(payload.get("timezone", "UTC")),
        "line_order": "bottom_to_top",
        "lines": normalized_lines,
        "base_hexagram": base_hexagram,
        "changing_lines": changing_lines,
        "changed_hexagram": changed_hexagram,
        "is_valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "next_steps": [
            "interpret_base_hexagram_as_current_structure",
            "interpret_changing_lines_as_change_focus",
            "interpret_changed_hexagram_as_tendency_when_present",
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
    parser.add_argument("--json", help="JSON input with six lines from bottom to top.")
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
