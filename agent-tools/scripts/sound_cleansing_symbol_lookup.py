#!/usr/bin/env python3
"""Lookup safe symbolic prompts for sound-cleansing motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "singing_bowl": ("铃钵/颂钵", "tool", "边界、回响、空间复位、短时练习", "只作低音量短时提示，不贴耳、不通宵、不承诺疗愈或驱邪。"),
    "bell": ("铃铛/手铃", "tool", "开始、结束、提醒、门口边界", "用于标记开始/结束和收心，不用于惊吓、驱赶或扰民。"),
    "tuning_fork": ("音叉", "tool", "校准、单点注意、微小动作", "不接触耳部或疼痛部位，不替代治疗。"),
    "clap": ("拍手/轻叩", "action", "唤醒、清点角落、节奏、可撤回", "保持轻量、短时和尊重邻里，不写成驱灵攻击。"),
    "mantra": ("诵念/短句", "voice", "意图、呼吸、稳定、重复边界", "把诵念写成自我提醒，不写成咒令或神明命令。"),
    "silence": ("安静收尾", "phase", "沉淀、聆听、复盘、停止条件", "练习后保留安静，不持续追求特殊感应。"),
    "window": ("开窗/通风", "environment", "空气、转换、现实安全", "只作通风和整理，不承诺把负能量排走。"),
    "timer": ("计时器", "safety", "时长、停止、反复依赖边界", "用于限制练习时长，避免反复敲击或焦虑循环。"),
}

ALIASES = {
    "铃钵": "singing_bowl",
    "颂钵": "singing_bowl",
    "singing bowl": "singing_bowl",
    "铃铛": "bell",
    "手铃": "bell",
    "bell": "bell",
    "音叉": "tuning_fork",
    "tuning fork": "tuning_fork",
    "拍手": "clap",
    "轻叩": "clap",
    "诵念": "mantra",
    "念咒": "mantra",
    "mantra": "mantra",
    "chanting": "mantra",
    "安静": "silence",
    "收尾": "silence",
    "开窗": "window",
    "通风": "window",
    "计时器": "timer",
    "短时": "timer",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    if text.lower() in ALIASES or text in ALIASES:
        return ALIASES.get(text.lower(), ALIASES.get(text, lowered))
    for alias, code in ALIASES.items():
        if any("\u4e00" <= char <= "\u9fff" for char in alias) and alias.lower() in text.lower():
            return code
    return lowered.replace(" ", "_")


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown sound-cleansing symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "space_reset_reflection"
    return {
        "tool": "sound_cleansing_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "sound_cleansing_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的低风险象征素材，围绕空间复位、音量时长、身体感受、邻里边界、收尾和停止条件整理。",
        "reflection_questions": [
            "这是文化象征和空间复位，还是在寻求治疗、驱灵证明、效果保证或高价器具？",
            "声音工具、音量、时长、时段、身体感受、宠物/婴儿/邻里边界是什么？",
            "练习何时结束，结束后用什么安静收尾或现实整理动作？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不承诺驱邪、清除负能量、治疗、入睡、转运或灵验结果。",
            "不提供贴耳、超大音量、通宵、耳痛仍继续、靠近婴儿/宠物或扰民做法。",
            "不替代医疗、心理、睡眠、法律、报警或其他专业支持。",
            "不制造高价铃钵、课程、套餐或反复依赖。",
        ],
        "next_steps": ["combine_with_sound_cleansing_context", "separate_symbolic_space_reset_from_exorcism_or_medical_claims", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Sound-cleansing motif.")
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
