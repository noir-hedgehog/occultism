#!/usr/bin/env python3
"""Lookup safe symbolic prompts for Elder Futhark rune names."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "fehu": ("Fehu", "财富、资源、流动、照料", "把资源看作可管理条件，不承诺发财。"),
    "uruz": ("Uruz", "体力、韧性、原始动力、恢复", "不作医疗、体能或健康诊断。"),
    "thurisaz": ("Thurisaz", "边界、阻力、冲突、门槛", "不鼓励攻击、报复或诅咒。"),
    "ansuz": ("Ansuz", "语言、讯息、学习、倾听", "不声称收到神谕或外部事实。"),
    "raidho": ("Raidho", "旅程、节奏、路线、协调", "不保证出行或项目必顺。"),
    "kenaz": ("Kenaz", "火炬、洞察、技能、显明", "不把灵感写成事实证明。"),
    "gebo": ("Gebo", "交换、礼物、互惠、关系平衡", "不替用户判断第三方真实想法。"),
    "wunjo": ("Wunjo", "喜悦、归属、满足、协作", "不承诺幸福或关系结果。"),
    "hagalaz": ("Hagalaz", "扰动、打断、天气、重组", "不恐吓灾祸。"),
    "naudiz": ("Nauthiz", "需求、限制、耐心、必要条件", "不把困境说成命定惩罚。"),
    "isa": ("Isa", "冻结、暂停、静止、保留", "不鼓励拖延专业处理。"),
    "jera": ("Jera", "周期、收成、时机、累积", "不承诺特定回报。"),
    "eihwaz": ("Eihwaz", "耐久、转化、防护、轴心", "不确认超自然保护或攻击。"),
    "perthro": ("Perthro", "未知、概率、揭示、游戏", "不用于赌博或投机决策。"),
    "algiz": ("Algiz", "保护、警觉、界限、支持", "不替代现实安全措施。"),
    "sowilo": ("Sowilo", "太阳、清晰、方向、活力", "不作健康或成功保证。"),
    "tiwaz": ("Tiwaz", "原则、公正、承诺、勇气", "不替代法律判断。"),
    "berkano": ("Berkano", "生长、照护、孕育、恢复", "不作怀孕或医疗判断。"),
    "ehwaz": ("Ehwaz", "伙伴、移动、信任、协作", "不读取第三方隐私。"),
    "mannaz": ("Mannaz", "自我、群体、镜像、学习", "不贴人格标签。"),
    "laguz": ("Laguz", "水、情绪、直觉、流动", "不把情绪当事实证据。"),
    "ingwaz": ("Ingwaz", "潜能、封存、整合、成熟", "不承诺结果成熟。"),
    "dagaz": ("Dagaz", "破晓、转折、重新看见、转换", "不宣称命运翻盘。"),
    "othala": ("Othala", "家族、传承、边界、归属", "不做血统优劣或家族命运断言。"),
}

ALIASES = {
    "财富": "fehu",
    "资源": "fehu",
    "力量": "uruz",
    "边界": "thurisaz",
    "讯息": "ansuz",
    "旅程": "raidho",
    "火炬": "kenaz",
    "礼物": "gebo",
    "喜悦": "wunjo",
    "冰雹": "hagalaz",
    "限制": "naudiz",
    "冰": "isa",
    "收成": "jera",
    "紫杉": "eihwaz",
    "未知": "perthro",
    "保护": "algiz",
    "太阳": "sowilo",
    "公正": "tiwaz",
    "生长": "berkano",
    "伙伴": "ehwaz",
    "自我": "mannaz",
    "水": "laguz",
    "潜能": "ingwaz",
    "破晓": "dagaz",
    "家族": "othala",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower()
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown rune symbol: {code}")
    canonical, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "rune_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "rune_divination",
        "symbol_code": code,
        "symbol_family": "elder_futhark",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把 {canonical} 作为卢恩符文象征，围绕{focus}整理资源、阻力、选择边界和低风险下一步。",
        "reflection_questions": [
            "这枚符文在本轮位置里指向现实中的哪类资源、阻力或行动条件？",
            "哪些内容必须回到事实、当事人沟通、专业意见或安全措施？",
            "用户是否把符文结果当作命运断言或最终决定？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把符文写成事实证明、专业建议、诊断、预测或最终决定。",
            "不确认诅咒、黑魔法、附身、被害或第三方真实想法。",
            "不鼓励反复抽取直到满意。",
        ],
        "next_steps": ["combine_with_rune_cast_record", "rank_real_world_evidence_first", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Rune name, e.g. fehu, ansuz, algiz.")
    parser.add_argument("--focus", help="Optional focus.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = lookup(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False)
, file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
