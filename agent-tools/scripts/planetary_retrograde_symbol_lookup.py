#!/usr/bin/env python3
"""Lookup safe symbolic prompts for planetary retrogrades and astrology weather."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "mercury_retrograde": ("水星逆行/水逆", "retrograde", "沟通、复盘、备份、延迟", "把水逆当作沟通复核、备份和节奏调整提醒，不当作必然倒霉。"),
    "venus_retrograde": ("金星逆行", "retrograde", "关系、价值、审美、消费", "把金星逆行当作关系和消费复盘提醒，不证明爱意或关系结果。"),
    "mars_retrograde": ("火星逆行", "retrograde", "行动、冲突、能量、节奏", "把火星逆行当作放慢冲突反应和调整行动节奏的提示。"),
    "jupiter_retrograde": ("木星逆行", "retrograde", "信念、扩张、学习、承诺", "把木星逆行当作检查承诺和学习方向的提示，不保证好运或坏运。"),
    "saturn_retrograde": ("土星逆行", "retrograde", "责任、边界、结构、长期计划", "把土星逆行当作整理责任和边界的提示，不写成惩罚。"),
    "shadow_period": ("逆行阴影期", "cycle_phase", "前奏、复查、遗留事项、缓冲", "把阴影期当作提前检查和缓冲安排，不制造恐慌。"),
    "station_direct": ("顺行/停滞转向", "cycle_phase", "转折、恢复、确认、整合", "把顺行转向当作复盘后确认下一步的提示，不承诺立刻顺利。"),
    "astrology_weather": ("星象天气", "context", "背景、氛围、提醒、周期", "把星象天气当作背景语言，不替代现实判断和专业支持。"),
}

ALIASES = {
    "水逆": "mercury_retrograde",
    "水星逆行": "mercury_retrograde",
    "mercury retrograde": "mercury_retrograde",
    "金星逆行": "venus_retrograde",
    "venus retrograde": "venus_retrograde",
    "火星逆行": "mars_retrograde",
    "mars retrograde": "mars_retrograde",
    "木星逆行": "jupiter_retrograde",
    "jupiter retrograde": "jupiter_retrograde",
    "土星逆行": "saturn_retrograde",
    "saturn retrograde": "saturn_retrograde",
    "阴影期": "shadow_period",
    "逆行阴影期": "shadow_period",
    "顺行": "station_direct",
    "停滞": "station_direct",
    "星象天气": "astrology_weather",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text.lower(), ALIASES.get(text, lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown planetary retrograde symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "communication_review"
    return {
        "tool": "planetary_retrograde_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "planetary_retrograde_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的象征性复盘素材，围绕现实事项、沟通检查、备份、边界和停止查询条件整理。",
        "reflection_questions": [
            "用户是在做低风险复盘，还是把星象当作必然灾祸或专业决策依据？",
            "现实事项、已知限制、可控行动、复盘时间和停止查询条件是什么？",
            "是否涉及宿命归因、第三方读心/操控、危险仪式、高价转运或焦虑依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把水逆或逆行写成必然灾祸、命中注定、行星惩罚或灵体事实。",
            "不证明第三方真实想法，不替代医疗、法律、财务、职业或心理健康判断。",
            "不制造高价转运、危险仪式、反复查询或恐慌依赖。",
        ],
        "next_steps": ["combine_with_planetary_retrograde_context", "separate_symbolic_weather_from_decision_or_blame", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Planetary retrograde motif.")
    parser.add_argument("--focus", help="Optional focus.")
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
