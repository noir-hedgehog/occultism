#!/usr/bin/env python3
"""Lookup safe symbolic prompts for moon phases and lunar-cycle motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "new_moon": ("新月", "phase", "开始、播种、意图、留白", "不保证许愿显化或结果成真。"),
    "waxing_crescent": ("娥眉月/蛾眉月", "phase", "试探、积累、照料、小步行动", "不要求用户熬夜、禁食或做危险仪式。"),
    "first_quarter": ("上弦月", "phase", "选择、推进、调整阻力、行动承诺", "不替代重大决策中的现实评估。"),
    "waxing_gibbous": ("盈凸月", "phase", "修正、打磨、接近完成、反馈", "不承诺项目成功或关系结果。"),
    "full_moon": ("满月", "phase", "照亮、完成、复盘、释放", "不保证释放、疗愈、复合或发财。"),
    "waning_gibbous": ("亏凸月", "phase", "分享、整合、感谢、复盘经验", "不制造必须付费分享或课程压力。"),
    "last_quarter": ("下弦月", "phase", "整理、取舍、修正结构、放下负担", "不把放下解释成必须断联或操控他人。"),
    "waning_crescent": ("残月", "phase", "休息、收尾、恢复、安静观察", "不替代睡眠障碍、抑郁或身心症状支持。"),
    "eclipse": ("月食", "event", "暂停、揭示、变化敏感期、观察", "不输出灾祸预言或恐吓。"),
    "blue_moon": ("蓝月", "event", "稀有复盘、重复主题、第二次机会", "不承诺特殊灵力或高价仪式必要性。"),
    "supermoon": ("超级月亮", "event", "放大感受、可见度、注意力集中", "不把情绪波动写成诊断或命运信号。"),
}

ALIASES = {
    "新月": "new_moon",
    "new moon": "new_moon",
    "娥眉月": "waxing_crescent",
    "蛾眉月": "waxing_crescent",
    "眉月": "waxing_crescent",
    "上弦月": "first_quarter",
    "first quarter": "first_quarter",
    "盈凸月": "waxing_gibbous",
    "满月": "full_moon",
    "full moon": "full_moon",
    "亏凸月": "waning_gibbous",
    "下弦月": "last_quarter",
    "last quarter": "last_quarter",
    "残月": "waning_crescent",
    "月食": "eclipse",
    "eclipse": "eclipse",
    "蓝月": "blue_moon",
    "blue moon": "blue_moon",
    "超级月亮": "supermoon",
    "supermoon": "supermoon",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("phase", payload.get("symbol", ""))))
    if not code:
        raise ValueError("query, phase, or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown moon phase symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "cycle_reflection"
    return {
        "tool": "moon_phase_symbol_lookup",
        "query": str(payload.get("query", payload.get("phase", payload.get("symbol", code)))).strip(),
        "canonical_name": canonical,
        "system": "moon_phase_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为月亮周期象征，围绕{focus}整理意图、复盘、现实约束和下一步行动。",
        "reflection_questions": [
            "月相信源来自哪里，是否需要注明只是用户提供或日历来源？",
            "这个周期主题可以转成哪一个可执行、可复盘的小行动？",
            "是否在寻找显化保证、危险仪式、专业替代或第三方操控？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把月相解释成天文权威、显化保证、灾祸预言、医疗/生育建议、投资信号或关系命令。",
            "不提供明火、血液、禁食、熬夜、危险地点或诅咒操控类仪式步骤。",
            "不制造付费课程、付费仪式、反复许愿或查月相依赖。",
        ],
        "next_steps": ["combine_with_context_record", "rank_real_world_constraints_first", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Moon phase or lunar event.")
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
