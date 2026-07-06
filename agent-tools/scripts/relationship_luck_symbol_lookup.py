#!/usr/bin/env python3
"""Lookup safe symbolic prompts for peach-blossom and relationship-luck motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "peach_blossom": ("桃花/人缘", "theme", "可见度、亲和力、社交机会、自我呈现", "只作为社交行动和自我呈现提醒，不承诺脱单、复合或被喜欢。"),
    "marriage_affinity": ("姻缘/正缘", "theme", "价值观、关系准备、选择边界、长期相处", "改写成关系目标和选择标准，不断定正缘身份或婚姻结果。"),
    "yuelao": ("月老", "deity_motif", "祝福、牵线、善意介绍、节庆文化", "只作文化象征和善意连接提醒，不确认神明安排或强制缘分。"),
    "red_thread": ("红线/红绳", "object", "连接、边界、承诺、可同意互动", "不写成绑定他人；只作为本人沟通边界和尊重同意的提醒。"),
    "rose_quartz": ("粉晶", "object", "温和表达、自我接纳、关系柔软度", "不写成招桃花保证或必须购买；已有物件可作表达提醒。"),
    "flower": ("花/花束", "object", "表达、礼貌、场合、互惠", "不诱导越界送礼或超预算购买；先确认场景和对方接受度。"),
    "mirror": ("镜子/形象整理", "practice", "自我观察、仪容、表达一致性", "作为现实行动，不替代心理咨询或操控技巧。"),
    "message": ("消息/邀约", "practice", "清晰表达、节奏、尊重回复、不追问", "把行动限制为一次清晰、可拒绝的沟通，不进行轰炸或骚扰。"),
}

ALIASES = {
    "桃花": "peach_blossom",
    "人缘": "peach_blossom",
    "旺桃花": "peach_blossom",
    "招桃花": "peach_blossom",
    "peach blossom": "peach_blossom",
    "姻缘": "marriage_affinity",
    "正缘": "marriage_affinity",
    "爱情运": "marriage_affinity",
    "恋爱运": "marriage_affinity",
    "romance luck": "marriage_affinity",
    "月老": "yuelao",
    "红线": "red_thread",
    "红绳": "red_thread",
    "粉晶": "rose_quartz",
    "玫瑰石英": "rose_quartz",
    "花": "flower",
    "花束": "flower",
    "镜子": "mirror",
    "形象整理": "mirror",
    "消息": "message",
    "邀约": "message",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    if text.lower() in ALIASES or text in ALIASES:
        return ALIASES.get(text.lower(), ALIASES.get(text, lowered))
    for alias, code in ALIASES.items():
        if alias.lower() in text.lower():
            return code
    return lowered


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown relationship luck symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "social_action_reflection"
    return {
        "tool": "relationship_luck_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "relationship_luck_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的低风险象征素材，围绕自我呈现、沟通边界、社交行动、尊重同意、复盘和停止条件整理。",
        "reflection_questions": [
            "这是自我呈现和沟通提醒，还是在寻求复合保证、第三方读心、操控或骚扰？",
            "本人目标、可同意沟通对象、边界、已有物件、可控行动和复盘时间是什么？",
            "是否涉及家暴威胁、自伤伤人、法律/心理专业替代、高价法事或反复依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不承诺脱单、复合、结婚、正缘到来、挽回成功或第三方真实想法。",
            "不协助跟踪、骚扰、定位、人肉、读心、操控、爱情降头、强制和合或报复。",
            "不替代心理、法律、报警、婚姻家庭、危机支持或现实安全行动。",
            "不制造和合术、挽回套餐、高价法事、高价购买或反复依赖。",
        ],
        "next_steps": ["combine_with_relationship_luck_context", "separate_symbolic_romance_from_mind_reading_or_coercion", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Relationship-luck motif.")
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
