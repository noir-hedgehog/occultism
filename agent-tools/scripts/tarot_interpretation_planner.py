#!/usr/bin/env python3
"""Build a structured Tarot interpretation plan from a recorded draw."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from typing import Any

import tarot_card_lookup
import tarot_draw_recorder


POSITION_LENSES = {
    "当前提醒": "把这张牌读作此刻最需要留意的状态或焦点。",
    "现状": "描述当前局势的主调，不把它当成最终结果。",
    "阻碍": "描述卡住、过度、缺失或需要调整的环节。",
    "建议": "转译为一个低风险、可执行的下一步。",
    "过去影响": "只说明仍在影响当下的模式，不把过去写成宿命。",
    "当前状态": "描述当下资源、情绪或限制。",
    "趋势提醒": "写成可能的发展倾向和需观察的信号。",
    "A 方案状态": "描述 A 路径的当前能量和现实条件。",
    "A 方案提醒": "指出 A 路径需要验证或修正的点。",
    "B 方案状态": "描述 B 路径的当前能量和现实条件。",
    "B 方案提醒": "指出 B 路径需要验证或修正的点。",
    "共同建议": "抽出两个选项都适用的行动原则。",
    "我的状态": "聚焦用户自己的感受、需要和可控行动。",
    "对方可能状态": "只用可能性语言，不替对方下确定结论。",
    "互动模式": "描述双方互动循环，避免归罪单方。",
    "边界建议": "落到沟通边界、节奏和自我照顾。",
    "真正关切": "辨认问题背后的真实担忧。",
    "可用资源": "列出现有支持、时间、能力或信息。",
    "主要风险": "指出需提前验证的现实风险。",
    "下一步": "收束为一个小行动或澄清问题。",
}

SUIT_ACTIONS = {
    "权杖": "把灵感拆成一个能在 24-72 小时内启动的小动作。",
    "圣杯": "先命名感受，再决定要不要表达或调整距离。",
    "宝剑": "把事实、猜测和结论分开写清楚。",
    "星币": "检查时间、预算、身体状态和可持续习惯。",
}


def card_theme(card_lookup: dict[str, Any]) -> str:
    keywords = card_lookup.get("active_keywords", [])
    if isinstance(keywords, list) and keywords:
        return "、".join(str(item) for item in keywords[:3])
    return str(card_lookup.get("card", ""))


def reversal_strategy(draw: list[dict[str, Any]]) -> str:
    reversed_count = sum(1 for item in draw if item.get("orientation") == "reversed")
    if reversed_count == 0:
        return "本次没有逆位；先按能量较顺畅或可见的表达读取，再检查现实限制。"
    if reversed_count == len(draw):
        return "本次全部为逆位；把整体读作内化、阻滞、过度或尚未准备好，重点放在减压和澄清。"
    if reversed_count >= max(2, len(draw) // 2):
        return "逆位比例偏高；降低结论确定性，把重点放在卡点、延迟、边界和修正动作。"
    return "少量逆位可读作局部阻滞、内在化或过度补偿；必须结合牌位判断。"


def pattern_flags(card_lookups: list[dict[str, Any]]) -> dict[str, Any]:
    suits = Counter(str(item.get("suit")) for item in card_lookups if item.get("suit"))
    arcana = Counter(str(item.get("arcana")) for item in card_lookups)
    orientations = Counter(str(item.get("orientation")) for item in card_lookups)
    dominant_suit = ""
    if suits:
        candidate, count = suits.most_common(1)[0]
        if count >= 2:
            dominant_suit = candidate
    flags: list[str] = []
    if arcana.get("major", 0) >= 2:
        flags.append("major_arcana_emphasis")
    if orientations.get("reversed", 0) >= max(2, len(card_lookups) // 2):
        flags.append("reversal_emphasis")
    if dominant_suit:
        flags.append(f"{dominant_suit}_emphasis")
    return {
        "major_arcana_count": arcana.get("major", 0),
        "minor_arcana_count": arcana.get("minor", 0),
        "reversed_count": orientations.get("reversed", 0),
        "upright_count": orientations.get("upright", 0),
        "suits": dict(suits),
        "dominant_suit": dominant_suit,
        "flags": flags,
    }


def build_card_plan(draw_item: dict[str, Any], lookup: dict[str, Any]) -> dict[str, Any]:
    position = str(draw_item.get("position", ""))
    action = str(lookup.get("action_guidance", "把象征转译成一个低风险行动。"))
    if lookup.get("suit") in SUIT_ACTIONS:
        action = SUIT_ACTIONS[str(lookup["suit"])]
    return {
        "index": draw_item.get("index"),
        "position": position,
        "position_lens": POSITION_LENSES.get(position, "先说明这个牌位在本次问题中的观察角度。"),
        "card": lookup.get("card"),
        "english_name": lookup.get("english_name"),
        "orientation": lookup.get("orientation"),
        "active_keywords": lookup.get("active_keywords", []),
        "interpretation_prompt": f"在「{position}」位置，把「{lookup.get('card')}」读成：{card_theme(lookup)}。",
        "reflection_prompt": lookup.get("reflection_prompt", ""),
        "action_prompt": action,
    }


def synthesis_from(card_plans: list[dict[str, Any]], patterns: dict[str, Any]) -> dict[str, Any]:
    actions = []
    for item in card_plans:
        action = str(item.get("action_prompt", ""))
        if action and action not in actions:
            actions.append(action)
    tension_points = []
    if "reversal_emphasis" in patterns["flags"]:
        tension_points.append("逆位较多，优先解释为卡点和需要调整的节奏。")
    if patterns["dominant_suit"]:
        tension_points.append(f"{patterns['dominant_suit']}重复出现，说明该元素对应的主题需要被优先处理。")
    if patterns["major_arcana_count"] >= 2:
        tension_points.append("大牌较多，适合谈阶段性主题，但仍需落到具体行动。")
    if not tension_points:
        tension_points.append("牌面未显示单一强模式，按牌位逐层解释即可。")
    return {
        "core_theme": card_plans[0]["interpretation_prompt"] if card_plans else "",
        "tension_points": tension_points,
        "grounded_actions": actions[:3],
        "closing_prompt": "用户读完后最需要确认的一件现实小事是什么？",
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    recorded = tarot_draw_recorder.record(payload)
    if not recorded["is_valid"]:
        return {
            "question_text": recorded["question_text"],
            "spread": recorded["spread"],
            "is_valid": False,
            "errors": recorded["errors"],
            "warnings": recorded["warnings"],
            "card_plans": [],
            "patterns": {},
            "reversal_strategy": "",
            "synthesis": {},
            "limits": [
                "Do not interpret invalid or mismatched Tarot draws.",
                "Resolve card names, orientations, and spread positions before synthesis.",
            ],
            "next_steps": ["fix_draw_record", "rerun_tarot_interpretation_planner"],
        }

    lookups = [
        tarot_card_lookup.lookup_card(str(item["card"]), str(item["orientation"]), str(item["position"]))
        for item in recorded["draw"]
    ]
    card_plans = [build_card_plan(item, lookup) for item, lookup in zip(recorded["draw"], lookups)]
    patterns = pattern_flags(lookups)
    return {
        "question_text": recorded["question_text"],
        "spread": recorded["spread"],
        "is_valid": True,
        "errors": [],
        "warnings": recorded["warnings"],
        "card_plans": card_plans,
        "patterns": patterns,
        "reversal_strategy": reversal_strategy(recorded["draw"]),
        "synthesis": synthesis_from(card_plans, patterns),
        "limits": [
            "Use possibility language; do not claim certainty or inevitability.",
            "Do not replace medical, legal, financial, or emergency safety advice.",
            "In relationship readings, describe the other person only as a possibility and return agency to the user.",
        ],
        "next_steps": [
            "draft_tarot_answer_from_plan",
            "run_mystic_output_lint",
            "offer_1_to_3_grounded_next_steps",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --json, --file, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON input accepted by tarot_draw_recorder.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = plan(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
