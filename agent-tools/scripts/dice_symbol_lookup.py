#!/usr/bin/env python3
"""Lookup safe symbolic prompts for astrodice and divination-dice faces."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "mars": ("火星", "planet", "行动、冲突、推进、勇气", "不写成必须冲动行动或胜负保证。"),
    "venus": ("金星", "planet", "关系、价值、舒适、吸引", "不承诺恋爱、复合或他人回应。"),
    "mercury": ("水星", "planet", "沟通、信息、学习、连接", "不替代合同、法律或专业沟通。"),
    "moon": ("月亮", "planet", "感受、习惯、安全感、节律", "不写成心理诊断。"),
    "sun": ("太阳", "planet", "核心、可见度、自我表达、方向", "不写成命运保证。"),
    "saturn": ("土星", "planet", "结构、限制、责任、时间", "不写成惩罚或厄运证明。"),
    "aries": ("白羊座", "sign", "启动、直接、试探、勇气", "不写成鲁莽定论。"),
    "libra": ("天秤座", "sign", "平衡、协商、关系、审美", "不写成讨好或关系定论。"),
    "capricorn": ("摩羯座", "sign", "结构、目标、耐心、现实", "不写成冷漠或宿命。"),
    "pisces": ("双鱼座", "sign", "想象、共情、边界、流动", "不写成逃避或灵性命令。"),
    "first_house": ("第一宫", "house", "自我呈现、身体感受、开端", "不做健康诊断或外貌评价。"),
    "seventh_house": ("第七宫", "house", "合作、关系、对话、镜像", "不窥探第三方真实想法。"),
    "tenth_house": ("第十宫", "house", "目标、责任、公开角色、事业结构", "不承诺升职或成功。"),
    "twelfth_house": ("第十二宫", "house", "休息、潜意识、隐退、整理", "不写成附身、诅咒或精神诊断。"),
}

ALIASES = {
    "火星": "mars",
    "mars": "mars",
    "金星": "venus",
    "venus": "venus",
    "水星": "mercury",
    "mercury": "mercury",
    "月亮": "moon",
    "moon": "moon",
    "太阳": "sun",
    "sun": "sun",
    "土星": "saturn",
    "saturn": "saturn",
    "白羊": "aries",
    "白羊座": "aries",
    "aries": "aries",
    "天秤": "libra",
    "天秤座": "libra",
    "libra": "libra",
    "摩羯": "capricorn",
    "摩羯座": "capricorn",
    "capricorn": "capricorn",
    "双鱼": "pisces",
    "双鱼座": "pisces",
    "pisces": "pisces",
    "1宫": "first_house",
    "第一宫": "first_house",
    "first_house": "first_house",
    "7宫": "seventh_house",
    "第七宫": "seventh_house",
    "seventh_house": "seventh_house",
    "10宫": "tenth_house",
    "第十宫": "tenth_house",
    "tenth_house": "tenth_house",
    "12宫": "twelfth_house",
    "第十二宫": "twelfth_house",
    "twelfth_house": "twelfth_house",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("face", ""))))
    if not code:
        raise ValueError("query, symbol, or face is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown dice symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "dice_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("face", code)))).strip(),
        "canonical_name": canonical,
        "system": "dice_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "astrodice_common_faces",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为星骰/占卜骰象征，围绕{focus}整理个人联想、现实证据、边界和低风险下一步。",
        "reflection_questions": [
            "这个骰面来自用户已掷结果、模拟同意，还是外部应用？",
            "它更像行动、沟通、关系、限制、目标，还是休息提醒？",
            "哪些结论必须回到现实证据、专业支持、当事人沟通或安全约束？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把骰面写成确定预言、事实证明、诊断、财富结果、赌博建议或专业意见。",
            "不使用骰面窥探第三方真实想法、控制他人或决定重大风险事项。",
            "不反复掷骰直到满意。",
        ],
        "next_steps": ["combine_with_dice_roll_record", "prefer_reality_check_and_low_risk_action", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Dice face, e.g. 火星, 白羊座, 第十宫.")
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
