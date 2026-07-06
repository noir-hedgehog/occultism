#!/usr/bin/env python3
"""Lookup safe symbolic prompts for psychometry object motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "ring": ("戒指", "object", "承诺、循环、关系边界、重复模式", "不确认婚恋事实、背叛、归属或第三方想法。"),
    "necklace": ("项链/吊坠", "object", "靠近心口、珍视、保护感、身份表达", "不确认护身功效、附身、诅咒或疗愈效果。"),
    "watch": ("手表/钟表", "object", "时间、节奏、等待、阶段感", "不预测寿命、事故或确定未来。"),
    "key": ("钥匙", "object", "进入、许可、边界、选择", "不定位失物、住址、他人秘密或犯罪线索。"),
    "photo": ("照片", "object", "记忆、视角、关系投射、定格时刻", "不做人脸身份、第三方隐私或真实想法判断。"),
    "book": ("旧书/笔记", "object", "知识、传承、未完成想法、旧主题", "不确认作者意图或物品历史事实。"),
    "fabric": ("衣物/织物", "object", "贴身经验、舒适、角色、日常习惯", "不读取物主隐私、健康状况或身体事实。"),
    "stone": ("石头/小物", "object", "重量、稳定、纪念、携带感", "不证明能量、磁场、挡灾或净化功效。"),
    "heirloom": ("遗物/传家物", "source", "纪念、哀悼、传承、关系未竟", "不确认亡灵讯息、遗愿、遗产或家族秘密。"),
    "secondhand": ("二手物/古董", "source", "前任使用痕迹、再选择、清理边界", "不确认前主人身份、经历、诅咒或危险事实。"),
}

ALIASES = {
    "戒指": "ring",
    "ring": "ring",
    "项链": "necklace",
    "吊坠": "necklace",
    "necklace": "necklace",
    "手表": "watch",
    "钟表": "watch",
    "watch": "watch",
    "钥匙": "key",
    "key": "key",
    "照片": "photo",
    "photo": "photo",
    "旧书": "book",
    "笔记": "book",
    "book": "book",
    "衣物": "fabric",
    "织物": "fabric",
    "fabric": "fabric",
    "石头": "stone",
    "小物": "stone",
    "stone": "stone",
    "遗物": "heirloom",
    "传家物": "heirloom",
    "二手物": "secondhand",
    "古董": "secondhand",
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
        raise ValueError(f"unknown psychometry symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "memory_boundary_reflection"
    return {
        "tool": "psychometry_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "psychometry_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为物件象征素材，围绕{focus}整理记忆、边界、情绪联想和可验证行动。",
        "reflection_questions": [
            "这个物件是否属于用户本人或已获授权？",
            "可见特征和用户第一联想分别是什么，哪些只是象征而不是事实？",
            "是否涉及失踪犯罪、第三方隐私、灵体事实、专业替代、真伪归属或付费净化？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把物品感应写成物品历史、身份、归属、真伪、灵体、诅咒或第三方事实。",
            "不用于失踪、刑案、定位、医疗、安全检测、法律、财务或鉴定判断。",
            "不诱导付费净化、开光、反复感应或未经同意读取他人物件。",
        ],
        "next_steps": ["combine_with_object_record", "separate_symbolic_from_fact_or_identification", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Psychometry object motif.")
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
