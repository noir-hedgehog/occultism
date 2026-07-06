#!/usr/bin/env python3
"""Lookup safe symbolic prompts for common crystals and energy stones."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


CRYSTALS = {
    "clear_quartz": ("白水晶", "清明、聚焦、整理、放大提醒", "不写成万能净化或疗愈工具。"),
    "amethyst": ("紫水晶", "安定、节制、睡前放松、直觉", "不替代失眠、焦虑或成瘾的专业支持。"),
    "rose_quartz": ("粉晶/玫瑰石英", "温柔、自我接纳、关系修复、善意", "不承诺复合、桃花或操控他人。"),
    "citrine": ("黄水晶", "信心、资源感、表达、目标感", "不承诺发财、收益或事业成功。"),
    "black_tourmaline": ("黑碧玺", "边界、隔离干扰、稳定、保护感", "不确认邪灵、诅咒或被害。"),
    "obsidian": ("黑曜石", "扎根、诚实面对、防御感、清理", "不写成吸走灾祸或替人挡灾。"),
    "fluorite": ("萤石", "学习、秩序、专注、信息分类", "不替代学习计划、诊断或治疗。"),
    "labradorite": ("拉长石", "转变、过渡、灵感、界限", "不把转变写成命中注定。"),
    "tiger_eye": ("虎眼石", "勇气、行动、判断、稳定推进", "不替代风险评估或财务判断。"),
    "green_aventurine": ("绿东陵/绿色砂金石", "成长、机会感、耐心、复原", "不承诺好运、中奖或投资收益。"),
    "moonstone": ("月光石", "周期、情绪照顾、变化、温柔", "不替代妇科、孕产或心理健康支持。"),
    "selenite": ("透石膏/selenite", "清理感、空间秩序、轻盈、重置", "不写成驱邪证明或强制净化。"),
}

ALIASES = {
    "白水晶": "clear_quartz",
    "clear quartz": "clear_quartz",
    "quartz": "clear_quartz",
    "紫水晶": "amethyst",
    "amethyst": "amethyst",
    "粉晶": "rose_quartz",
    "玫瑰石英": "rose_quartz",
    "rose quartz": "rose_quartz",
    "黄水晶": "citrine",
    "citrine": "citrine",
    "黑碧玺": "black_tourmaline",
    "black tourmaline": "black_tourmaline",
    "黑曜石": "obsidian",
    "obsidian": "obsidian",
    "萤石": "fluorite",
    "fluorite": "fluorite",
    "拉长石": "labradorite",
    "labradorite": "labradorite",
    "虎眼石": "tiger_eye",
    "tiger eye": "tiger_eye",
    "绿东陵": "green_aventurine",
    "绿色砂金石": "green_aventurine",
    "aventurine": "green_aventurine",
    "月光石": "moonstone",
    "moonstone": "moonstone",
    "透石膏": "selenite",
    "selenite": "selenite",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_")
    if lowered in CRYSTALS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("crystal", payload.get("item", ""))))
    if not code:
        raise ValueError("query, crystal, or item is required")
    if code not in CRYSTALS:
        raise ValueError(f"unknown crystal symbol: {code}")
    canonical, keywords_raw, action = CRYSTALS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "crystal_symbol_lookup",
        "query": str(payload.get("query", payload.get("crystal", payload.get("item", code)))).strip(),
        "canonical_name": canonical,
        "system": "crystal_symbolic_reflection",
        "symbol_code": code,
        "symbol_set": "common_crystal_symbolic_meanings",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为水晶/能量石象征，围绕{focus}整理审美偏好、个人联想、现实证据和低风险下一步。",
        "reflection_questions": [
            "用户已有这个物件，还是正在考虑购买？是否有低成本或已有物替代？",
            "这个象征更像提醒、边界、安定、审美偏好，还是行动触发器？",
            "哪些结论必须回到现实证据、预算、专业支持或当事人沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把水晶写成治病、驱邪证明、招财保证、复合保证或专业建议。",
            "不鼓励饮用水晶水、吞服、磨粉、贴伤口或身体侵入式做法。",
            "不制造高价购买压力，不暗示越贵越灵。",
        ],
        "next_steps": ["combine_with_item_record", "prefer_existing_or_low_cost_items", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Crystal name, e.g. 紫水晶, rose quartz, obsidian.")
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
