#!/usr/bin/env python3
"""Lookup safe symbolic prompts for consecration and object-cleansing motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "consecration": ("开光/加持", "practice", "命名、祝福、用途确认、提醒物边界", "只作文化象征和用途确认，不承诺灵验、挡灾或转运。"),
    "object_cleansing": ("净物/净化物件", "practice", "清洁、整理、来源记录、心理归位", "改写成清洁和整理流程，不确认物件有邪或能量污染。"),
    "clean_cloth": ("干净布/收纳袋", "object", "保护、收纳、边界、日常照料", "用作物理收纳和提醒，不写成封印或法力容器。"),
    "water_wipe": ("清水擦拭", "action", "清洁、降温、重新开始、可撤回", "只用于适合接触水的物件；不喝水、不作治疗或灵验保证。"),
    "sunlight": ("日光/通风", "environment", "明亮、通风、晾晒、时间限制", "注意材质褪色和安全，不做暴晒开光或驱邪断言。"),
    "incense_distance": ("远离明火的香气/通风", "environment", "气味、仪式感、通风、火源边界", "不提供燃烧步骤；如已有香气，也必须远离物件并确认通风和熄灭。"),
    "intention_note": ("意图卡/标签", "object", "用途、提醒、边界、复盘", "把意图写成可控用途，不写成神明命令或结果保证。"),
    "storage_place": ("固定收纳位置", "practice", "秩序、取放、停止反复、日常照料", "作为日常管理，不把位置写成镇压、封印或招财保证。"),
}

ALIASES = {
    "开光": "consecration",
    "加持": "consecration",
    "祝福": "consecration",
    "consecration": "consecration",
    "blessing": "consecration",
    "净物": "object_cleansing",
    "净化物件": "object_cleansing",
    "净化水晶": "object_cleansing",
    "净化手串": "object_cleansing",
    "干净布": "clean_cloth",
    "收纳袋": "clean_cloth",
    "清水": "water_wipe",
    "擦拭": "water_wipe",
    "日光": "sunlight",
    "通风": "sunlight",
    "香气": "incense_distance",
    "香": "incense_distance",
    "意图卡": "intention_note",
    "标签": "intention_note",
    "收纳位置": "storage_place",
    "固定位置": "storage_place",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    if text.lower() in ALIASES or text in ALIASES:
        return ALIASES.get(text.lower(), ALIASES.get(text, lowered))
    for alias, code in ALIASES.items():
        if any("\u4e00" <= char <= "\u9fff" for char in alias) and alias.lower() in text.lower():
            return code
    return lowered


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown consecration symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "object_care_reflection"
    return {
        "tool": "consecration_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "consecration_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的低风险象征素材，围绕来源记录、清洁整理、用途确认、无火安全、复盘和停止条件整理。",
        "reflection_questions": [
            "这是文化象征和物件照料，还是在寻求灵验保证、危险仪式、高价法事或专业替代？",
            "物件来源、材质、当前用途、安全边界、可控动作和复盘时间是什么？",
            "是否涉及摄入/伤身、明火危险、神明恐吓、欺骗操控或反复依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不承诺灵验、挡灾、发财、转运、平安保证或神明命令。",
            "不提供放血、摄入、刀具、危险燃烧、密闭明火或伤身做法。",
            "不替代医疗、法律、报警、心理或财务专业支持。",
            "不制造开光套餐、高价法事、高价购买或反复依赖。",
        ],
        "next_steps": ["combine_with_consecration_context", "separate_symbolic_object_care_from_supernatural_guarantees", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Consecration motif.")
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
