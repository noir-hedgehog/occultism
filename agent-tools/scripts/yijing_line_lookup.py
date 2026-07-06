#!/usr/bin/env python3
"""Lookup a Yijing changing-line interpretation scaffold across 384 lines."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import yijing_hexagram_lookup


LINE_ROLES = {
    1: {
        "label": "初爻",
        "stage": "起点",
        "focus": "根基、潜动、尚未外显的开端",
        "question": "这件事最底层的动因或条件是什么？",
        "action": "先稳住基础，不急于扩大动作。",
    },
    2: {
        "label": "二爻",
        "stage": "内在承接",
        "focus": "位置较中，重在配合、承载和可持续性",
        "question": "我能否在自己的位置上稳定承接？",
        "action": "从可持续的配合和日常节奏入手。",
    },
    3: {
        "label": "三爻",
        "stage": "临界压力",
        "focus": "内外转换处，容易躁进、试探或遭遇风险",
        "question": "我正跨过哪个边界，风险是否被看见？",
        "action": "放慢推进，先评估代价和支持。",
    },
    4: {
        "label": "四爻",
        "stage": "外部连接",
        "focus": "接近外部资源、权责或更高位置，重在试探分寸",
        "question": "我该如何连接外部资源而不越位？",
        "action": "小步试探，确认边界和反馈。",
    },
    5: {
        "label": "五爻",
        "stage": "主位决策",
        "focus": "主位、责任、决策核心和整合能力",
        "question": "谁在承担主责，决策标准是什么？",
        "action": "明确责任、标准和可公开承担的选择。",
    },
    6: {
        "label": "上爻",
        "stage": "阶段尾声",
        "focus": "过度、收束、余波和转入下一阶段",
        "question": "这件事是否已经过了合适的度？",
        "action": "及时收尾，避免把旧阶段硬拖下去。",
    },
}

RELATION_NOTES = {
    ("yang", "yang_position"): "阳爻居阳位，动力和位置较一致；仍需防止过刚。",
    ("yin", "yin_position"): "阴爻居阴位，承接和位置较一致；仍需防止过柔。",
    ("yang", "yin_position"): "阳爻居阴位，行动力处在承接位置；宜柔化表达。",
    ("yin", "yang_position"): "阴爻居阳位，承接力处在主动位置；宜补足决断。",
}


def parse_hexagram(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("hexagram_number") is not None:
        return yijing_hexagram_lookup.lookup({"number": payload["hexagram_number"]})
    if payload.get("number") is not None:
        return yijing_hexagram_lookup.lookup({"number": payload["number"]})
    if payload.get("hexagram") is not None:
        return yijing_hexagram_lookup.lookup({"query": payload["hexagram"]})
    if payload.get("query") is not None:
        return yijing_hexagram_lookup.lookup({"query": payload["query"]})
    if payload.get("name") is not None:
        return yijing_hexagram_lookup.lookup({"query": payload["name"]})
    raise ValueError("provide hexagram_number, number, hexagram, query, or name")


def normalize_line(raw: object) -> int:
    line = int(raw)
    if line < 1 or line > 6:
        raise ValueError("line must be between 1 and 6")
    return line


def changed_hexagram_for(bits: str, line: int) -> dict[str, Any]:
    chars = list(bits)
    index = line - 1
    chars[index] = "0" if chars[index] == "1" else "1"
    changed_bits = "".join(chars)
    for item in yijing_hexagram_lookup.HEXAGRAMS:
        if item["bits_bottom_to_top"] == changed_bits:
            return item
    raise ValueError(f"cannot find changed hexagram for bits {changed_bits}")


def line_nature(bit: str) -> str:
    return "yang" if bit == "1" else "yin"


def position_nature(line: int) -> str:
    return "yang_position" if line % 2 == 1 else "yin_position"


def direction_for(base: dict[str, Any], changed: dict[str, Any], line: int, nature: str) -> str:
    role = LINE_ROLES[line]
    verb = "由主动转为承接" if nature == "yang" else "由承接转为主动"
    return f"{role['label']}动，{verb}；从「{base['short_name']}」的主题转向「{changed['short_name']}」的主题。"


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("line") is None:
        raise ValueError("line is required")
    line = normalize_line(payload["line"])
    base = parse_hexagram(payload)
    bits = str(base["bits_bottom_to_top"])
    nature = line_nature(bits[line - 1])
    position = position_nature(line)
    changed = changed_hexagram_for(bits, line)
    role = LINE_ROLES[line]
    return {
        "hexagram": {
            "number": base["number"],
            "name": base["name"],
            "short_name": base["short_name"],
            "keywords": base["keywords"],
            "bits_bottom_to_top": bits,
        },
        "line": line,
        "line_label": role["label"],
        "line_stage": role["stage"],
        "line_focus": role["focus"],
        "line_nature": nature,
        "position_nature": position,
        "fit_note": RELATION_NOTES[(nature, position)],
        "changing_to": {
            "number": changed["number"],
            "name": changed["name"],
            "short_name": changed["short_name"],
            "keywords": changed["keywords"],
            "bits_bottom_to_top": changed["bits_bottom_to_top"],
        },
        "interpretation_scaffold": {
            "line_question": role["question"],
            "line_action": role["action"],
            "change_direction": direction_for(base, changed, line, nature),
            "compare_prompt": f"先读本卦「{base['name']}」的处境，再把{role['label']}作为变化焦点，最后看变卦「{changed['name']}」提示的趋势。",
        },
        "source_level": "modern_line_index_not_classical_text",
        "limits": [
            "此工具覆盖 64 卦 × 6 爻的爻位索引和变化骨架，不提供原文爻辞或传统注疏。",
            "爻位解释需结合具体问题、起卦方法、本卦、变卦和现实处境。",
            "不得把动爻解释为确定预言、医疗/法律/财务建议或灾祸断言。",
        ],
        "next_steps": [
            "lookup_base_hexagram",
            "compare_changed_hexagram",
            "map_line_focus_to_grounded_action",
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
    if args.number is not None:
        payload["number"] = args.number
    if args.query:
        payload["query"] = args.query
    if args.line is not None:
        payload["line"] = args.line
    if payload:
        return payload
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --number/--query with --line, --json, --file, or JSON stdin")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--number", type=int, help="King Wen sequence number, 1-64.")
    parser.add_argument("--query", help="Hexagram name or short name.")
    parser.add_argument("--line", type=int, help="Changing line number, 1-6.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()
    try:
        result = lookup(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
