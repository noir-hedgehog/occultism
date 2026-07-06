#!/usr/bin/env python3
"""Lookup safe symbolic prompts for sleep paralysis and night-fear motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "sleep_paralysis": ("鬼压床/睡眠瘫痪体验", "episode", "醒来、身体未动、恐惧、过渡状态", "不确认灵体压迫；先作为睡眠体验记录和安定流程处理。"),
    "heavy_chest": ("胸口压迫感", "body_sensation", "压力、紧绷、呼吸觉察、身体警报", "若有胸痛或呼吸困难，优先现实医疗支持；不作灵异证明。"),
    "shadow_figure": ("黑影/床边人影", "image", "未知、警觉、夜间恐惧、边界", "只作为醒后印象和恐惧象征，不确认实体或鬼神。"),
    "frozen_body": ("动不了", "body_sensation", "卡住、无力、等待恢复、求助信号", "用于记录恢复过程和 grounding，不鼓励强行对抗或睡眠剥夺。"),
    "door_or_window": ("门窗", "room_context", "安全感、边界、通风、光线", "转成现实检查：门锁、光线、噪音、温度，不写成灵体入口。"),
    "bedside_light": ("床边灯/夜灯", "object", "照明、方向感、醒后复位、安全提示", "可作为低风险安定物，不承诺驱邪。"),
    "breathing_anchor": ("呼吸锚点", "practice", "慢呼吸、身体复位、注意力回到当下", "只作安定练习；有呼吸困难时优先医疗支持。"),
    "sleep_log": ("睡眠记录", "practice", "频率、时长、触发因素、复盘", "用于观察模式和决定是否寻求现实支持，不用于反复找灵异证据。"),
}

ALIASES = {
    "鬼压床": "sleep_paralysis",
    "压床": "sleep_paralysis",
    "睡眠瘫痪": "sleep_paralysis",
    "睡瘫": "sleep_paralysis",
    "sleep paralysis": "sleep_paralysis",
    "胸口压": "heavy_chest",
    "胸口压迫": "heavy_chest",
    "胸口压迫感": "heavy_chest",
    "黑影": "shadow_figure",
    "人影": "shadow_figure",
    "床边有人": "shadow_figure",
    "动不了": "frozen_body",
    "身体动不了": "frozen_body",
    "门": "door_or_window",
    "窗": "door_or_window",
    "门窗": "door_or_window",
    "夜灯": "bedside_light",
    "床边灯": "bedside_light",
    "呼吸": "breathing_anchor",
    "呼吸锚点": "breathing_anchor",
    "grounding": "breathing_anchor",
    "睡眠记录": "sleep_log",
    "记录": "sleep_log",
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
        raise ValueError(f"unknown sleep paralysis symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "sleep_grounding_reflection"
    return {
        "tool": "sleep_paralysis_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "sleep_paralysis_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的低风险素材，围绕睡眠记录、醒后安定、房间现实安全、压力背景和复盘整理。",
        "reflection_questions": [
            "这是睡眠体验记录和安定，还是在确认鬼神、附身或下咒事实？",
            "发生频率、身体感、房间环境、近期压力、睡眠时长和白天影响是什么？",
            "是否涉及呼吸胸痛、抽搐受伤、连续失眠、幻听幻视、自伤伤人、危险仪式或专业替代？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不确认鬼、邪灵、附身、下咒、灵体压迫、灾祸预告或第三方影响。",
            "不提供危险仪式、睡眠剥夺、摄入符水香灰、专业替代或高价法事。",
            "严重睡眠受损、呼吸/胸痛/抽搐、幻听幻视、自伤伤人或现实功能受损时优先现实支持。",
        ],
        "next_steps": ["combine_with_sleep_paralysis_context", "separate_sleep_experience_from_spirit_fact_claims", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Sleep paralysis motif.")
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
