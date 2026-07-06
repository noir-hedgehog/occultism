#!/usr/bin/env python3
"""Lookup safe symbolic prompts for zodiac animals and Tai Sui motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "rat": ("子鼠", "机敏、资源、开端、适应", "不写成投机、偷巧或财富保证。"),
    "ox": ("丑牛", "稳定、耐力、耕耘、秩序", "不写成吃苦宿命或关系标签。"),
    "tiger": ("寅虎", "行动、边界、勇气、风险感", "不写成冲动必败或强势标签。"),
    "rabbit": ("卯兔", "敏感、协调、审美、谨慎", "不写成胆小或婚恋定论。"),
    "dragon": ("辰龙", "愿景、变化、声望、承担", "不写成天生贵命或必发财。"),
    "snake": ("巳蛇", "洞察、节奏、保留、转化", "不写成阴险或危险人格标签。"),
    "horse": ("午马", "移动、热情、推进、自由", "不写成飘忽或关系不稳定定论。"),
    "goat": ("未羊", "照顾、审美、群体、温和", "不写成软弱或被动命运。"),
    "monkey": ("申猴", "灵活、学习、尝试、幽默", "不写成不可靠标签。"),
    "rooster": ("酉鸡", "秩序、表达、细节、提醒", "不写成挑剔或口舌灾。"),
    "dog": ("戌狗", "忠诚、边界、守护、信任", "不写成牺牲或必被辜负。"),
    "pig": ("亥猪", "丰足、休息、人情、收束", "不写成懒散或享乐标签。"),
    "benmingnian": ("本命年", "周期回看、节奏调整、风险预案、低风险提醒", "不写成必倒霉或必须穿戴购买。"),
    "taisui": ("太岁/犯太岁", "时间秩序、民俗提醒、谨慎规划、来源限制", "不写成灾祸证明、报复或高价化解。"),
    "six_harmony": ("六合/三合", "关系互补、协作想象、沟通线索", "不写成合婚保证或生肖歧视。"),
    "six_clash": ("六冲/相冲", "差异提醒、节奏冲突、沟通边界", "不写成必须分手、克害或灾祸。"),
}

ALIASES = {
    "鼠": "rat",
    "子鼠": "rat",
    "牛": "ox",
    "丑牛": "ox",
    "虎": "tiger",
    "寅虎": "tiger",
    "兔": "rabbit",
    "卯兔": "rabbit",
    "龙": "dragon",
    "辰龙": "dragon",
    "蛇": "snake",
    "巳蛇": "snake",
    "马": "horse",
    "午马": "horse",
    "羊": "goat",
    "未羊": "goat",
    "猴": "monkey",
    "申猴": "monkey",
    "鸡": "rooster",
    "酉鸡": "rooster",
    "狗": "dog",
    "戌狗": "dog",
    "猪": "pig",
    "亥猪": "pig",
    "本命年": "benmingnian",
    "太岁": "taisui",
    "犯太岁": "taisui",
    "冲太岁": "taisui",
    "三合": "six_harmony",
    "六合": "six_harmony",
    "六冲": "six_clash",
    "相冲": "six_clash",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("zodiac", ""))))
    if not code:
        raise ValueError("query, symbol, or zodiac is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown zodiac symbol: {code}")
    canonical, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "zodiac_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("zodiac", code)))).strip(),
        "canonical_name": canonical,
        "system": "zodiac_symbolic_reflection",
        "symbol_code": code,
        "symbol_set": "chinese_zodiac_and_taisui_symbols",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为生肖/太岁象征，围绕{focus}整理文化语境、个人联想、现实证据和低风险下一步。",
        "reflection_questions": [
            "这是文化学习、本人反思、关系沟通，还是现实计划整理？",
            "这个生肖/太岁说法来自黄历、家人口述、网络文章、商家，还是用户个人联想？",
            "哪些结论必须回到现实证据、预算、安全、专业支持或当事人沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把生肖写成命运、人品、婚恋、健康、财富或灾祸证明。",
            "不输出犯太岁必有灾、生肖相克必须分手、化太岁必须购买等断言。",
            "不替代医疗、法律、财务、安全或心理健康支持。",
        ],
        "next_steps": ["combine_with_zodiac_profile", "prefer_low_risk_reflection_or_planning", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Zodiac motif, e.g. 龙, 本命年, 太岁, 六合.")
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
