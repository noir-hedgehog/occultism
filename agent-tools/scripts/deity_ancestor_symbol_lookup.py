#!/usr/bin/env python3
"""Lookup safe symbolic prompts for deity, ancestor, altar, and offering motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "altar": ("供桌/神台", "space", "秩序、尊重、家庭边界、日常提醒", "保持为整洁和纪念空间，不写成神明入住或惩罚证明。"),
    "incense": ("香/香火", "object", "敬意、暂停、专注、连接传统", "只讨论已安全结束或无火替代，不提供燃烧步骤或神明回应判断。"),
    "water": ("清水", "offering", "清明、照料、日常更换、朴素感恩", "只作象征供品，不承诺净化、治病或改运。"),
    "fruit": ("水果/食物供品", "offering", "丰盛、分享、季节、感恩", "注意食品、宠物和儿童安全；不把供品当药物或强制摄入。"),
    "ancestor_tablet": ("祖先牌位/照片", "memorial_object", "家族记忆、传承、怀念、价值观", "不确认亡灵命令或替代真实家庭沟通。"),
    "vow_return": ("还愿/酬谢", "practice", "兑现承诺、感恩、复盘、完成感", "只保留低风险、可撤回、不过度消费的感谢动作。"),
    "prayer": ("祈祷/祝祷", "practice", "表达愿望、安定、价值排序、行动提醒", "不保证神明回应或结果必成，落到现实行动。"),
    "cleaning": ("清洁整理", "practice", "秩序、照料、重新开始、家庭协作", "不写成驱邪证明；优先安全清洁和家庭同意。"),
}

ALIASES = {
    "供桌": "altar",
    "神台": "altar",
    "佛龛": "altar",
    "altar": "altar",
    "香": "incense",
    "香火": "incense",
    "incense": "incense",
    "清水": "water",
    "水": "water",
    "water": "water",
    "水果": "fruit",
    "供品": "fruit",
    "食物供品": "fruit",
    "fruit": "fruit",
    "祖先牌位": "ancestor_tablet",
    "牌位": "ancestor_tablet",
    "祖先照片": "ancestor_tablet",
    "照片": "ancestor_tablet",
    "ancestor": "ancestor_tablet",
    "还愿": "vow_return",
    "酬神": "vow_return",
    "谢神": "vow_return",
    "vow": "vow_return",
    "祈祷": "prayer",
    "祝祷": "prayer",
    "拜拜": "prayer",
    "prayer": "prayer",
    "清洁": "cleaning",
    "整理": "cleaning",
    "cleaning": "cleaning",
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
        raise ValueError(f"unknown deity ancestor symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "cultural_memorial_reflection"
    return {
        "tool": "deity_ancestor_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "deity_ancestor_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的低风险象征素材，围绕来源尊重、纪念/感恩、家庭边界、安全和现实行动整理。",
        "reflection_questions": [
            "这是文化学习、纪念表达和生活提醒，还是在寻求神明/祖先命令或灾祸确认？",
            "来源传统、家庭同意、消防食品安全、儿童宠物安全和预算边界是什么？",
            "是否涉及危险仪式、专业替代、操控报复、第三方指认、高价法事或反复依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不确认神明命令、祖先命令、托梦事实、神罚、灾祸预告、灵体事实或第三方隐私。",
            "不提供危险仪式、摄入香灰符水、专业替代、操控报复或强迫他人供奉。",
            "不制造天价法事、开光套餐、供奉消费或反复确认依赖。",
        ],
        "next_steps": ["combine_with_deity_ancestor_context", "separate_symbolic_memorial_from_commands_or_fear", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Deity or ancestor motif.")
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
