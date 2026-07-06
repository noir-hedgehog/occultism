#!/usr/bin/env python3
"""Lookup safe symbolic prompts for Nine Star Ki stars and contexts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "one_white_water": ("一白水星", "water", "流动、倾听、信息、适应、内在整理", "不写成情绪诊断、桃花保证或暗中操控。"),
    "two_black_earth": ("二黑土星", "earth", "承载、照料、积累、身体感、日常秩序", "不写成疾病预言、女性标签或必须忍耐。"),
    "three_jade_wood": ("三碧木星", "wood", "启动、表达、雷动、学习、早期冲劲", "不鼓励冲动争执、攻击或高风险行动。"),
    "four_green_wood": ("四绿木星", "wood", "沟通、关系网络、传播、信任、成长空间", "不窥探他人真实想法或承诺关系结果。"),
    "five_yellow_earth": ("五黄土星", "earth_center", "中心、压力、结构重整、边界、暂停核对", "不制造灾祸恐吓、方位禁忌或高价化解压力。"),
    "six_white_metal": ("六白金星", "metal", "责任、规则、权威、资源、决断框架", "不把权威、职位或法律结果写成定论。"),
    "seven_red_metal": ("七赤金星", "metal", "表达、愉悦、交换、口才、社交资源", "不承诺发财、桃花或让他人服从。"),
    "eight_white_earth": ("八白土星", "earth_mountain", "停止、积累、转折、门槛、长期建设", "不写成必然停滞、分手或失败。"),
    "nine_purple_fire": ("九紫火星", "fire", "可见度、热度、审美、洞察、完成感", "不鼓励曝光隐私、炒作或结果保证。"),
    "home_star": ("本命星", "profile_layer", "长期惯性、偏好、资源调用方式", "本命星不是人格定论，也不能用于筛选或歧视。"),
    "month_star": ("月命星", "profile_layer", "日常反应、节奏、关系中的细部模式", "需保留体系差异和节气边界，不强行计算。"),
    "annual_star": ("年星/流年星", "time_layer", "年度主题、提醒、复盘问题、行动节奏", "不写成某年必有灾祸或必然发财。"),
    "direction": ("方位", "space_layer", "空间提醒、动线、边界、低成本整理", "不制造方位恐吓、不要求搬家或高价化解。"),
    "center_palace": ("中宫", "space_layer", "中心主题、压力汇聚、需要先整理的核心条件", "不把中宫写成危险中心或命令。"),
}

ALIASES = {
    "1": "one_white_water",
    "一白": "one_white_water",
    "一白水星": "one_white_water",
    "one white": "one_white_water",
    "one_white_water": "one_white_water",
    "2": "two_black_earth",
    "二黑": "two_black_earth",
    "二黑土星": "two_black_earth",
    "two black": "two_black_earth",
    "two_black_earth": "two_black_earth",
    "3": "three_jade_wood",
    "三碧": "three_jade_wood",
    "三碧木星": "three_jade_wood",
    "three jade": "three_jade_wood",
    "three_jade_wood": "three_jade_wood",
    "4": "four_green_wood",
    "四绿": "four_green_wood",
    "四绿木星": "four_green_wood",
    "four green": "four_green_wood",
    "four_green_wood": "four_green_wood",
    "5": "five_yellow_earth",
    "五黄": "five_yellow_earth",
    "五黄土星": "five_yellow_earth",
    "five yellow": "five_yellow_earth",
    "five_yellow_earth": "five_yellow_earth",
    "6": "six_white_metal",
    "六白": "six_white_metal",
    "六白金星": "six_white_metal",
    "six white": "six_white_metal",
    "six_white_metal": "six_white_metal",
    "7": "seven_red_metal",
    "七赤": "seven_red_metal",
    "七赤金星": "seven_red_metal",
    "seven red": "seven_red_metal",
    "seven_red_metal": "seven_red_metal",
    "8": "eight_white_earth",
    "八白": "eight_white_earth",
    "八白土星": "eight_white_earth",
    "eight white": "eight_white_earth",
    "eight_white_earth": "eight_white_earth",
    "9": "nine_purple_fire",
    "九紫": "nine_purple_fire",
    "九紫火星": "nine_purple_fire",
    "nine purple": "nine_purple_fire",
    "nine_purple_fire": "nine_purple_fire",
    "本命星": "home_star",
    "月命星": "month_star",
    "年星": "annual_star",
    "流年星": "annual_star",
    "方位": "direction",
    "九星方位": "direction",
    "中宫": "center_palace",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered.replace(" ", "_")))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("star", payload.get("symbol", ""))))
    if not code:
        raise ValueError("query, star, or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown nine star ki symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "nine_star_ki_symbol_lookup",
        "query": str(payload.get("query", payload.get("star", payload.get("symbol", code)))).strip(),
        "canonical_name": canonical,
        "system": "nine_star_ki_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "nine_stars_plus_profile_time_space_layers",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为九星气学象征，围绕{focus}整理现实主题、可验证线索、边界和低风险下一步。",
        "reflection_questions": [
            "这是本命星、月命星、年星、方位，还是用户已知的外部资料？",
            "它更像资源、节奏、压力、沟通、边界、可见度还是复盘提醒？",
            "哪些结论必须回到现实证据、专业支持、预算、当事人沟通或空间安全？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把九星写成确定预言、事实证明、诊断、财富结果、赌博建议、搬迁命令或专业意见。",
            "不使用九星给关系贴标签、筛人、窥探第三方真实想法或控制他人。",
            "不制造方位恐吓、高价化解压力或反复计算直到满意。",
        ],
        "next_steps": ["combine_with_nine_star_ki_profile_record", "prefer_reality_check_and_low_risk_action", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Nine Star Ki star or layer, e.g. 一白水星, 五黄, 本命星.")
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
