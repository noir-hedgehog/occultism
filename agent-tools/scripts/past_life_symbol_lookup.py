#!/usr/bin/env python3
"""Lookup safe symbolic prompts for past-life/Akashic narrative motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "library": ("图书馆/档案馆", "akashic_setting", "记忆整理、学习、索引、未完成的问题", "不声称进入真实阿卡西记录或获得外部事实。"),
    "door": ("门/门槛", "threshold", "选择、过渡、边界、许可", "不把门槛解释为注定事件或必须跨越的命令。"),
    "water": ("水", "element", "情绪、流动、清理、适应", "不承诺净化、疗愈或创伤清除。"),
    "battlefield": ("战场", "scene", "冲突、保护、警觉、耗竭", "不确认用户曾经历战争、暴力或死亡创伤。"),
    "monastery": ("寺院/修道院", "scene", "秩序、独处、修习、承诺", "不把宗教身份或誓言写成现实义务。"),
    "contract": ("契约/卷轴", "motif", "承诺、边界、交换、可重写的规则", "不确认灵魂契约事实，不要求用户服从某段关系。"),
    "companion": ("同行者/熟人感", "relationship_motif", "投射、熟悉感、关系模式、边界", "不确认灵魂伴侣、复合保证或第三方真实身份。"),
    "exile": ("流放/离乡", "theme", "归属、断裂、迁移、重新安顿", "不把孤独感归咎于前世罪责。"),
    "healer": ("疗愈者/医者", "role", "照料、责任、界限、过度承担", "不鼓励替代医疗或无资质治疗他人。"),
    "artist": ("工匠/艺术家", "role", "创造、技艺、耐心、表达", "不把天赋或失败写成前世决定。"),
    "child": ("孩子", "role", "脆弱、好奇、需要保护的部分", "不用于确认儿童创伤或现实虐待事实。"),
}

ALIASES = {
    "图书馆": "library",
    "档案馆": "library",
    "阿卡西图书馆": "library",
    "门": "door",
    "门槛": "door",
    "水": "water",
    "河": "water",
    "海": "water",
    "战场": "battlefield",
    "战争": "battlefield",
    "寺院": "monastery",
    "修道院": "monastery",
    "卷轴": "contract",
    "契约": "contract",
    "灵魂契约": "contract",
    "同行者": "companion",
    "熟人感": "companion",
    "灵魂伴侣": "companion",
    "流放": "exile",
    "离乡": "exile",
    "医者": "healer",
    "疗愈者": "healer",
    "工匠": "artist",
    "艺术家": "artist",
    "孩子": "child",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("motif", ""))))
    if not code:
        raise ValueError("query, symbol, or motif is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown past-life/Akashic symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "past_life_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("motif", code)))).strip(),
        "canonical_name": canonical,
        "system": "past_life_akashic_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为前世/阿卡西象征，围绕{focus}整理主题、情绪、边界和当下可验证的小行动。",
        "reflection_questions": [
            "这是文化学习、梦境/冥想画面记录，还是在寻找事实证明或创伤确认？",
            "这个符号让用户想到哪些当下关系、边界、选择或照料需求？",
            "哪些内容只能作为象征叙事，哪些必须回到现实证据、专业支持或现实沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把前世/阿卡西画面写成事实、恢复记忆、创伤证明、身份等级、罪责或命运判决。",
            "不替代医疗、心理健康、创伤治疗、法律、财务、安全或关系沟通。",
            "不读取第三方前世、灵魂契约或真实想法，不制造付费疗愈和反复查询依赖。",
        ],
        "next_steps": ["combine_with_narrative_record", "separate_symbolic_from_factual_claims", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Past-life/Akashic symbol, scene, role, or motif.")
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
