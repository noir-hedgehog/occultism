#!/usr/bin/env python3
"""Lookup safe symbolic prompts for synchronicity and repeating-sign motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "repeating_ones": ("1111/重复 1", "angel_number", "开始、注意力、意图、归零", "把 1111 当作停一下、整理注意力和写下一个可控行动的提醒，不当成命令。"),
    "repeating_twos": ("222/重复 2", "angel_number", "关系、平衡、协作、节奏", "把 222 当作关系和节奏复盘提示，不证明任何人的真实想法。"),
    "repeating_threes": ("333/重复 3", "angel_number", "支持、结构、表达、创作", "把 333 当作整理支持系统和表达结构的提示，不写成天使命令。"),
    "repeating_fours": ("444/重复 4", "angel_number", "稳定、 routine、边界、基础", "把 444 当作检查作息、边界和基础工作的提示，不预测必然结果。"),
    "repeating_fives": ("555/重复 5", "angel_number", "变化、调整、弹性、过渡", "把 555 当作温和调整和复盘变化的提示，不替代重大决策。"),
    "mirror_time": ("镜像时间", "time_pattern", "映照、停顿、注意力、节律", "只记录看到它时的场景和心情，不主动反复检查时间。"),
    "repeated_song": ("反复出现的歌", "media_pattern", "情绪、主题、记忆、节奏", "把歌曲当作情绪和主题线索，不当作外部实体下达的讯息。"),
    "name": ("重复出现的名字", "word_pattern", "关系、投射、注意力、未完成议题", "不通过名字判断第三方真实想法或关系结果。"),
    "animal": ("重复出现的动物", "omen_overlap", "本能、习性、环境、注意力", "可转向动物征兆的低风险观察，但不做灾祸或事实保证。"),
    "feather": ("羽毛", "object_pattern", "轻盈、讯息、纪念、放下", "只作为私人纪念或整理提醒，不确认天使、亡灵或灵体事实。"),
}

ALIASES = {
    "1111": "repeating_ones",
    "11:11": "repeating_ones",
    "222": "repeating_twos",
    "333": "repeating_threes",
    "444": "repeating_fours",
    "555": "repeating_fives",
    "镜像时间": "mirror_time",
    "同一首歌": "repeated_song",
    "歌": "repeated_song",
    "歌曲": "repeated_song",
    "名字": "name",
    "动物": "animal",
    "羽毛": "feather",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown synchronicity symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "routine_reflection"
    return {
        "tool": "synchronicity_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "synchronicity_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的低风险记录素材，围绕情绪、现实锚点、可控行动和停止条件整理。",
        "reflection_questions": [
            "这个符号是在自然出现，还是用户正在主动危险寻找或反复确认？",
            "看到它时的场景、情绪、现实议题和可控行动是什么？",
            "是否涉及宇宙命令、专业替代、第三方读心、灵体事实、付费压力或焦虑依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把同步性写成宇宙、天使、神明、亡灵、灵体或外星讯息的事实命令。",
            "不预测必然结果，不证明第三方真实想法，不替代财务、职业、医疗、法律或心理健康判断。",
            "不鼓励开车、过马路或危险环境中寻找征兆，不强化反复检查和付费依赖。",
        ],
        "next_steps": ["combine_with_synchronicity_event_record", "separate_symbolic_prompt_from_command_or_decision", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Synchronicity motif.")
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
