#!/usr/bin/env python3
"""Lookup safe symbolic prompts for candle flame and wax observations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "steady_flame": ("稳定火焰", "flame", "稳定、专注、持续、节奏", "不写成必然成功或神明认可。"),
    "flickering_flame": ("摇曳火焰", "flame", "波动、注意力、环境因素、调整", "优先提醒通风和安全，不写成灵体信号。"),
    "low_flame": ("低火焰", "flame", "能量保留、节奏放慢、资源不足", "不写成坏运、失败或健康诊断。"),
    "tall_flame": ("高火焰", "flame", "强烈、显眼、推动力、需要边界", "优先提醒火源安全，不写成保证达成。"),
    "smoke": ("烟", "smoke", "释放、干扰、环境检查、需要通风", "不写成有鬼、中邪或诅咒证明。"),
    "river_wax": ("河流状蜡泪", "wax", "流动、路径、过渡、释放", "不承诺事情自然变好。"),
    "mountain_wax": ("山形蜡泪", "wax", "阻力、边界、耐心、长期目标", "不写成必然困难或灾祸。"),
    "ring_wax": ("环形蜡泪", "wax", "循环、承诺、边界、重复模式", "不承诺婚姻、合同或关系绑定。"),
    "split_wax": ("分叉蜡泪", "wax", "选择、分流、比较路径、分阶段", "不替代重大决定。"),
}

ALIASES = {
    "稳定": "steady_flame",
    "稳定火焰": "steady_flame",
    "steady": "steady_flame",
    "steady_flame": "steady_flame",
    "摇曳": "flickering_flame",
    "闪烁": "flickering_flame",
    "晃动": "flickering_flame",
    "flickering": "flickering_flame",
    "低火": "low_flame",
    "低火焰": "low_flame",
    "low": "low_flame",
    "高火": "tall_flame",
    "高火焰": "tall_flame",
    "tall": "tall_flame",
    "烟": "smoke",
    "冒烟": "smoke",
    "smoke": "smoke",
    "河流": "river_wax",
    "河流状": "river_wax",
    "流动": "river_wax",
    "river": "river_wax",
    "山": "mountain_wax",
    "山形": "mountain_wax",
    "mountain": "mountain_wax",
    "环": "ring_wax",
    "圆环": "ring_wax",
    "ring": "ring_wax",
    "分叉": "split_wax",
    "岔路": "split_wax",
    "split": "split_wax",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("observation", ""))))
    if not code:
        raise ValueError("query, symbol, or observation is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown candle symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "candle_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("observation", code)))).strip(),
        "canonical_name": canonical,
        "system": "candle_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "common_candle_flame_and_wax_observations",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为蜡烛火焰/蜡泪象征，围绕{focus}整理个人联想、现实证据、安全边界和低风险下一步。",
        "reflection_questions": [
            "观察是否已经安全结束，或是否来自照片/LED 蜡烛？",
            "这个符号更像稳定、波动、路径、阻力、边界，还是分岔提醒？",
            "哪些结论必须回到现实证据、消防安全、专业支持或当事人沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把火焰或蜡泪写成确定预言、事实证明、诊断、财富结果、驱邪证明或专业意见。",
            "不提供点火、燃烧、烧纸、烧符、放血或密闭燃烧步骤。",
            "不使用观察结果窥探第三方真实想法、控制他人或决定重大风险事项。",
        ],
        "next_steps": ["combine_with_candle_observation_record", "prefer_fire_safety_and_low_risk_action", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Candle observation, e.g. 稳定火焰, 河流, 烟.")
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
