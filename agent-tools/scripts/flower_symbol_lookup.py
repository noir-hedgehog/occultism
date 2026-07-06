#!/usr/bin/env python3
"""Lookup safe symbolic prompts for flowers and plant motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "rose": ("玫瑰", "flower", "情感、表达、边界、珍视", "不承诺复合、桃花或第三方感情结果。"),
    "lily": ("百合", "flower", "清洁、祝福、过渡、庄重", "不作医疗、丧葬或宗教权威判断。"),
    "sunflower": ("向日葵", "flower", "可见、热情、方向、支持", "不承诺成功或好运必来。"),
    "lavender": ("薰衣草", "flower", "安定、休息、柔和、整理", "不替代失眠、焦虑、抑郁等专业支持。"),
    "lotus": ("莲花", "flower", "清明、出离、沉淀、复原", "不把痛苦写成必须忍受的命运。"),
    "plum": ("梅花", "flower", "寒中生发、韧性、等待、品格", "不把艰难写成应该硬扛。"),
    "orchid": ("兰花", "flower", "细致、气质、耐心、关系礼节", "不评价身份高低或人格优劣。"),
    "chrysanthemum": ("菊花", "flower", "收束、纪念、清醒、边界", "注意地区文化差异，不强行用于所有送礼场景。"),
    "peony": ("牡丹", "flower", "丰盛、体面、展示、资源", "不承诺富贵、招财或身份跃升。"),
    "jasmine": ("茉莉", "flower", "清香、亲近、日常照料、温和表达", "不替代过敏、香味敏感或宠物安全判断。"),
    "bamboo": ("竹", "plant", "节制、弹性、空心、秩序", "不把隐忍写成压抑需求。"),
    "willow": ("柳", "plant", "柔韧、离别、牵挂、过渡", "不承诺关系回头或分离必然。"),
    "white": ("白色", "color", "清洁、简明、告别、留白", "注意地区和仪式语境，不作单一吉凶断言。"),
    "red": ("红色", "color", "热情、显眼、庆祝、行动", "不承诺桃花、财富或好运。"),
    "yellow": ("黄色", "color", "明亮、支持、友谊、信号", "不承诺成功或回报。"),
    "purple": ("紫色", "color", "沉静、想象、尊重、边界", "不把颜色写成灵性等级。"),
}

ALIASES = {
    "玫瑰": "rose",
    "红玫瑰": "rose",
    "rose": "rose",
    "百合": "lily",
    "lily": "lily",
    "向日葵": "sunflower",
    "太阳花": "sunflower",
    "sunflower": "sunflower",
    "薰衣草": "lavender",
    "lavender": "lavender",
    "莲": "lotus",
    "莲花": "lotus",
    "lotus": "lotus",
    "梅": "plum",
    "梅花": "plum",
    "兰": "orchid",
    "兰花": "orchid",
    "菊": "chrysanthemum",
    "菊花": "chrysanthemum",
    "牡丹": "peony",
    "茉莉": "jasmine",
    "竹": "bamboo",
    "竹子": "bamboo",
    "柳": "willow",
    "柳枝": "willow",
    "白": "white",
    "白色": "white",
    "红": "red",
    "红色": "red",
    "黄": "yellow",
    "黄色": "yellow",
    "紫": "purple",
    "紫色": "purple",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("flower", ""))))
    if not code:
        raise ValueError("query, symbol, or flower is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown flower symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "flower_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("flower", code)))).strip(),
        "canonical_name": canonical,
        "system": "flower_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为花语/植物象征，围绕{focus}整理表达意图、关系边界、审美偏好和低风险行动。",
        "reflection_questions": [
            "这个花材在当前场景里用于表达、提醒、纪念、安定还是空间氛围？",
            "是否有过敏、宠物、儿童、香味、预算或场合限制需要现实优先？",
            "哪些内容必须回到当事人沟通、专业意见或安全资料？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把花语写成事实证明、专业建议、诊断、预测、财富承诺、复合保证或最终决定。",
            "不确认诅咒、附身、被害、驱邪效果或第三方真实想法。",
            "不判断过敏、毒性、宠物安全、摄入或药用安全。",
        ],
        "next_steps": ["combine_with_flower_item_record", "rank_real_world_constraints_first", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Flower, plant, or color symbol.")
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
