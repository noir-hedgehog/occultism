#!/usr/bin/env python3
"""Record and validate Tarot draws against a selected spread."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class SpreadTemplate:
    spread_id: str
    name: str
    positions: tuple[str, ...]


SPREADS = {
    "single_focus": SpreadTemplate("single_focus", "单张聚焦", ("当前提醒",)),
    "three_card_situation": SpreadTemplate("three_card_situation", "三张状态牌阵", ("现状", "阻碍", "建议")),
    "past_present_tendency": SpreadTemplate("past_present_tendency", "过去-现在-趋势", ("过去影响", "当前状态", "趋势提醒")),
    "two_paths": SpreadTemplate("two_paths", "二选一路径", ("A 方案状态", "A 方案提醒", "B 方案状态", "B 方案提醒", "共同建议")),
    "relationship_mirror": SpreadTemplate("relationship_mirror", "关系镜像", ("我的状态", "对方可能状态", "互动模式", "边界建议")),
    "decision_grounding": SpreadTemplate("decision_grounding", "决策落地", ("真正关切", "可用资源", "主要风险", "下一步")),
}

MAJOR_ARCANA = {
    "愚者": ("the fool", "fool", "0"),
    "魔术师": ("the magician", "magician", "i", "1"),
    "女祭司": ("the high priestess", "high priestess", "ii", "2"),
    "皇后": ("the empress", "empress", "iii", "3"),
    "皇帝": ("the emperor", "emperor", "iv", "4"),
    "教皇": ("the hierophant", "hierophant", "v", "5"),
    "恋人": ("the lovers", "lovers", "vi", "6"),
    "战车": ("the chariot", "chariot", "vii", "7"),
    "力量": ("strength", "viii", "8"),
    "隐士": ("the hermit", "hermit", "ix", "9"),
    "命运之轮": ("wheel of fortune", "x", "10"),
    "正义": ("justice", "xi", "11"),
    "倒吊人": ("the hanged man", "hanged man", "xii", "12"),
    "死神": ("death", "xiii", "13"),
    "节制": ("temperance", "xiv", "14"),
    "恶魔": ("the devil", "devil", "xv", "15"),
    "高塔": ("the tower", "tower", "xvi", "16"),
    "星星": ("the star", "star", "xvii", "17"),
    "月亮": ("the moon", "moon", "xviii", "18"),
    "太阳": ("the sun", "sun", "xix", "19"),
    "审判": ("judgement", "judgment", "xx", "20"),
    "世界": ("the world", "world", "xxi", "21"),
}

SUITS = {
    "权杖": ("wands", "wand", "权杖"),
    "圣杯": ("cups", "cup", "chalices", "圣杯"),
    "宝剑": ("swords", "sword", "宝剑"),
    "星币": ("pentacles", "pentacle", "coins", "coin", "星币", "金币"),
}

RANKS = {
    "王牌": ("ace", "a", "1", "一", "王牌"),
    "二": ("two", "2", "二"),
    "三": ("three", "3", "三"),
    "四": ("four", "4", "四"),
    "五": ("five", "5", "五"),
    "六": ("six", "6", "六"),
    "七": ("seven", "7", "七"),
    "八": ("eight", "8", "八"),
    "九": ("nine", "9", "九"),
    "十": ("ten", "10", "十"),
    "侍从": ("page", "princess", "侍从"),
    "骑士": ("knight", "prince", "骑士"),
    "皇后": ("queen", "皇后"),
    "国王": ("king", "国王"),
}

ORIENTATION_ALIASES = {
    "upright": "upright",
    "正位": "upright",
    "正": "upright",
    "reversed": "reversed",
    "reverse": "reversed",
    "逆位": "reversed",
    "逆": "reversed",
}


def alias_map() -> dict[str, str]:
    aliases: dict[str, str] = {}
    for canonical, names in MAJOR_ARCANA.items():
        aliases[canonical.lower()] = canonical
        for name in names:
            aliases[name.lower()] = canonical
    for suit, suit_aliases in SUITS.items():
        for rank, rank_aliases in RANKS.items():
            canonical = f"{suit}{rank}"
            aliases[canonical.lower()] = canonical
            for suit_alias in suit_aliases:
                for rank_alias in rank_aliases:
                    aliases[f"{rank_alias} of {suit_alias}".lower()] = canonical
                    aliases[f"{suit_alias} {rank_alias}".lower()] = canonical
                aliases[f"{suit}{rank}".lower()] = canonical
                aliases[f"{rank}{suit}".lower()] = canonical
    return aliases


CARD_ALIASES = alias_map()


def normalize_card(card_name: object) -> tuple[str | None, str | None]:
    raw = str(card_name or "").strip()
    if not raw:
        return None, "card name is required"
    normalized = CARD_ALIASES.get(raw.lower())
    if not normalized:
        return raw, f"unknown tarot card: {raw}"
    return normalized, None


def normalize_orientation(orientation: object) -> tuple[str | None, str | None]:
    raw = str(orientation or "").strip().lower()
    if not raw:
        return "upright", None
    normalized = ORIENTATION_ALIASES.get(raw)
    if not normalized:
        return None, f"unknown orientation: {orientation}"
    return normalized, None


def template_for(spread_id: str | None, custom_positions: Iterable[object] | None) -> tuple[str, str, list[str], list[str]]:
    warnings: list[str] = []
    if spread_id and spread_id in SPREADS:
        template = SPREADS[spread_id]
        positions = list(template.positions)
        name = template.name
    else:
        if spread_id:
            warnings.append(f"unknown spread_id: {spread_id}; using custom positions")
        positions = []
        name = str(spread_id or "custom_spread")

    if custom_positions:
        positions = [str(position).strip() for position in custom_positions if str(position).strip()]
        name = name if spread_id in SPREADS else "自定义牌阵"

    if not positions:
        warnings.append("positions are missing; generated generic position names from card count")

    return str(spread_id or "custom_spread"), name, positions, warnings


def record(payload: dict[str, object]) -> dict[str, object]:
    question = str(payload.get("question_text", payload.get("request_text", ""))).strip()
    spread_id = str(payload.get("spread_id", "")).strip() or None
    custom_positions = payload.get("positions")
    if custom_positions is not None and not isinstance(custom_positions, list):
        raise ValueError("positions must be a list when provided")

    cards = payload.get("cards")
    if not isinstance(cards, list) or not cards:
        raise ValueError("cards must be a non-empty list")

    spread_id_value, spread_name, positions, warnings = template_for(spread_id, custom_positions)
    if not positions:
        positions = [f"牌位 {index + 1}" for index in range(len(cards))]

    errors: list[str] = []
    if len(cards) != len(positions):
        errors.append(f"card count {len(cards)} does not match position count {len(positions)}")

    seen_cards: set[str] = set()
    draw: list[dict[str, object]] = []
    for index, card_item in enumerate(cards):
        if not isinstance(card_item, dict):
            errors.append(f"card at index {index} must be an object")
            continue
        canonical_card, card_error = normalize_card(card_item.get("card"))
        orientation, orientation_error = normalize_orientation(card_item.get("orientation"))
        if card_error:
            errors.append(card_error)
        if orientation_error:
            errors.append(orientation_error)
        if canonical_card and canonical_card in seen_cards:
            errors.append(f"duplicate card: {canonical_card}")
        if canonical_card:
            seen_cards.add(canonical_card)
        draw.append(
            {
                "index": index + 1,
                "position": str(card_item.get("position") or (positions[index] if index < len(positions) else f"牌位 {index + 1}")),
                "card": canonical_card or str(card_item.get("card", "")),
                "orientation": orientation or "unknown",
                "note": str(card_item.get("note", "")).strip(),
            }
        )

    return {
        "question_text": question,
        "spread": {
            "spread_id": spread_id_value,
            "name": spread_name,
            "position_count": len(positions),
            "positions": positions,
        },
        "draw": draw,
        "is_valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "next_steps": [
            "interpret_each_card_by_position",
            "compare_card_interactions",
            "map_symbols_to_grounded_actions",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
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
    parser.add_argument("--json", help="JSON input with spread_id, positions, cards, and optional question_text.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = record(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
