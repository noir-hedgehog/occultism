#!/usr/bin/env python3
"""Lookup safe symbolic prompts for five-elements colors."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "green": ("绿色/青色", "wood", "生长、更新、弹性、计划", "不承诺事业上涨或健康疗愈。"),
    "red": ("红色", "fire", "可见度、热情、行动、提醒", "不承诺招桃花、发财或避灾。"),
    "yellow": ("黄色/土色", "earth", "稳定、承载、秩序、照顾", "不写成必稳财或压制他人。"),
    "white": ("白色/金色", "metal", "清晰、边界、结构、简洁", "不写成贵人保证或身份优越。"),
    "black": ("黑色/蓝色", "water", "沉静、休息、流动、观察", "不写成神秘力量或避祸证明。"),
    "purple": ("紫色", "fire_metal_blend", "仪式感、专注、审美、过渡", "不写成灵性等级或疗愈功效。"),
    "pink": ("粉色", "soft_fire", "温和、亲和、柔软、关系提醒", "不承诺恋爱、复合或他人回应。"),
    "brown": ("棕色", "earth", "扎根、耐用、朴素、日常", "不写成保守宿命或低价值。"),
}

ALIASES = {
    "绿": "green",
    "绿色": "green",
    "青色": "green",
    "青": "green",
    "木": "green",
    "红": "red",
    "红色": "red",
    "火": "red",
    "黄": "yellow",
    "黄色": "yellow",
    "土色": "yellow",
    "土": "yellow",
    "白": "white",
    "白色": "white",
    "金色": "white",
    "金": "white",
    "黑": "black",
    "黑色": "black",
    "蓝色": "black",
    "蓝": "black",
    "水": "black",
    "紫": "purple",
    "紫色": "purple",
    "粉": "pink",
    "粉色": "pink",
    "棕": "brown",
    "棕色": "brown",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("color", payload.get("element", ""))))
    if not code:
        raise ValueError("query, color, or element is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown color symbol: {code}")
    canonical, element, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "color_symbol_lookup",
        "query": str(payload.get("query", payload.get("color", payload.get("element", code)))).strip(),
        "canonical_name": canonical,
        "system": "color_symbolic_reflection",
        "symbol_code": code,
        "element": element,
        "symbol_set": "five_elements_color_symbols",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为五行颜色象征，围绕{focus}整理文化语境、个人偏好、现实约束和低风险下一步。",
        "reflection_questions": [
            "这个颜色用于穿搭、饰品、空间、品牌，还是情绪提醒？",
            "用户已有物件、预算、舒适度、场合规范和禁忌色是什么？",
            "哪些结论必须回到现实专业支持、审美偏好、预算或安全约束？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把颜色写成发财、转运、治病、避灾、桃花或人品证明。",
            "不贬低外貌、身份、肤色、体型、年龄、性别或文化背景。",
            "不制造高价购买、必须换装或反复依赖。",
        ],
        "next_steps": ["combine_with_color_profile", "prefer_existing_items_or_low_cost_adjustments", "run_mystic_output_lint"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.query:
        return {"query": args.query, "focus": args.focus}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Color or element, e.g. 绿色, 火, black.")
    parser.add_argument("--focus", help="Optional consultation focus.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
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
