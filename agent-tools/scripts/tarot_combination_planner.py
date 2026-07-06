#!/usr/bin/env python3
"""Plan multi-card Tarot combination reading prompts from a recorded draw."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from itertools import combinations
from typing import Any

import tarot_card_lookup
import tarot_draw_recorder


SUIT_THEMES = {
    "权杖": "行动、意志、创造力",
    "圣杯": "情绪、关系、感受",
    "宝剑": "思想、沟通、判断",
    "星币": "资源、身体、金钱、现实建设",
}

RISK_KEYWORDS = {
    "medical": ["生病", "疾病", "怀孕", "癌", "诊断", "医生", "药", "手术"],
    "professional_finance": ["股票", "投资", "贷款", "梭哈", "暴富", "破产", "比特币", "虚拟币", "合约交易"],
    "legal": ["官司", "起诉", "判刑", "违法", "合同纠纷", "离婚诉讼"],
    "coercion": ["控制他", "控制她", "让他爱我", "让她爱我", "操控", "复合咒"],
    "crisis": ["自杀", "轻生", "伤害自己", "伤害别人", "活不下去"],
}

SPREAD_LINKS = {
    ("现状", "阻碍"): ("current_obstacle_tension", "把第一张读作当前主调，第二张只作为卡点或需要验证的限制。"),
    ("阻碍", "建议"): ("obstacle_to_advice", "说明阻碍如何转成低风险下一步，不把建议写成命令。"),
    ("过去影响", "当前状态"): ("past_to_present", "只描述过去模式如何仍在影响当下。"),
    ("当前状态", "趋势提醒"): ("present_to_tendency", "用可能性语言描述可观察趋势和需留意信号。"),
    ("A 方案状态", "A 方案提醒"): ("path_a_state_to_caution", "把 A 路径拆成当前条件与验证点。"),
    ("B 方案状态", "B 方案提醒"): ("path_b_state_to_caution", "把 B 路径拆成当前条件与验证点。"),
    ("互动模式", "边界建议"): ("relationship_boundary", "把互动循环收束到用户可执行的边界和节奏。"),
    ("真正关切", "可用资源"): ("concern_to_resource", "把担忧和已有支持放在同一条现实线索里。"),
    ("主要风险", "下一步"): ("risk_to_next_step", "先列验证问题，再给一个低成本、可逆动作。"),
}


def risk_flags(question_text: str) -> list[str]:
    text = question_text.lower()
    flags = []
    for flag, keywords in RISK_KEYWORDS.items():
        if any(keyword.lower() in text for keyword in keywords):
            flags.append(flag)
    return flags


def normalize_draw(payload: dict[str, Any]) -> dict[str, Any]:
    recorded = tarot_draw_recorder.record(payload)
    if not recorded["is_valid"]:
        return {
            "recorded": recorded,
            "lookups": [],
            "errors": list(recorded["errors"]),
        }
    lookups = [
        tarot_card_lookup.lookup_card(str(item["card"]), str(item["orientation"]), str(item["position"]))
        for item in recorded["draw"]
    ]
    return {"recorded": recorded, "lookups": lookups, "errors": []}


def normalized_cards(draw: list[dict[str, Any]], lookups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cards = []
    for item, lookup in zip(draw, lookups):
        cards.append(
            {
                "index": item["index"],
                "position": item["position"],
                "card": lookup["card"],
                "english_name": lookup["english_name"],
                "orientation": lookup["orientation"],
                "arcana": lookup["arcana"],
                "suit": lookup.get("suit", ""),
                "element": lookup.get("element", ""),
                "active_keywords": lookup.get("active_keywords", [])[:4],
            }
        )
    return cards


def evidence_from(cards: list[dict[str, Any]], field: str, value: str | None = None) -> list[str]:
    matched = []
    for card in cards:
        if value is None:
            if card.get(field):
                matched.append(f"{card['position']}={card['card']}")
        elif card.get(field) == value:
            matched.append(f"{card['position']}={card['card']}")
    return matched


def make_pattern(
    pattern_id: str,
    label: str,
    evidence: list[str],
    interpretation_prompt: str,
    safe_language: str,
    avoid_language: str,
) -> dict[str, Any]:
    return {
        "pattern_id": pattern_id,
        "label": label,
        "evidence": evidence,
        "interpretation_prompt": interpretation_prompt,
        "safe_language": safe_language,
        "avoid_language": avoid_language,
    }


def combination_patterns(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    patterns: list[dict[str, Any]] = []
    total = len(cards)
    orientation_counts = Counter(card["orientation"] for card in cards)
    arcana_counts = Counter(card["arcana"] for card in cards)
    suit_counts = Counter(card["suit"] for card in cards if card.get("suit"))
    court_cards = [card for card in cards if card["card"].endswith(("侍从", "骑士", "皇后", "国王"))]

    if total >= 3 and orientation_counts["reversed"] >= max(2, (total + 1) // 2):
        patterns.append(
            make_pattern(
                "reversal_cluster",
                "逆位聚集",
                evidence_from(cards, "orientation", "reversed"),
                "把多张逆位作为阻滞、内化、过度补偿或节奏未准备好的线索来读。",
                "逆位较多，适合先看哪里卡住、哪里需要降速和修正。",
                "这些逆位说明事情一定会失败或有坏结果。",
            )
        )

    if total >= 2 and arcana_counts["major"] >= max(2, (total + 1) // 2):
        patterns.append(
            make_pattern(
                "major_arcana_weight",
                "大牌权重偏高",
                evidence_from(cards, "arcana", "major"),
                "把大牌读作阶段主题、价值选择或结构性课题，再落回具体行动。",
                "这组牌的大牌较多，可以谈阶段性主题，但仍要回到现实证据。",
                "大牌出现代表命运已经决定。",
            )
        )

    if suit_counts:
        dominant_suit, dominant_count = suit_counts.most_common(1)[0]
        if dominant_count >= 2:
            patterns.append(
                make_pattern(
                    "dominant_suit",
                    f"{dominant_suit}元素重复",
                    evidence_from(cards, "suit", dominant_suit),
                    f"把重复的{dominant_suit}读作「{SUIT_THEMES[dominant_suit]}」主题需要被优先处理。",
                    f"{dominant_suit}重复出现，说明这个维度在问题中更醒目。",
                    "某个花色多就代表单一原因或唯一答案。",
                )
            )
        missing_suits = [suit for suit in SUIT_THEMES if suit not in suit_counts]
        if len(missing_suits) >= 2 and total >= 3:
            patterns.append(
                make_pattern(
                    "missing_suit_lenses",
                    "缺席元素提醒",
                    missing_suits,
                    "把缺席花色作为尚未充分询问的现实镜头，而不是缺陷判断。",
                    "这些元素没有出现，可以作为补充提问方向。",
                    "没出现的花色代表用户没有这种能力或注定缺失。",
                )
            )

    if len(court_cards) >= 2:
        patterns.append(
            make_pattern(
                "court_card_cluster",
                "宫廷牌聚集",
                [f"{card['position']}={card['card']}" for card in court_cards],
                "把宫廷牌读作角色、姿态、成熟度或互动方式，不直接指定现实中的某个人。",
                "宫廷牌较多，适合谈角色姿态和责任边界。",
                "这张宫廷牌就是某个具体的人，且他一定会这样做。",
            )
        )

    keyword_hits: Counter[str] = Counter()
    for card in cards:
        for keyword in card.get("active_keywords", []):
            keyword_hits[str(keyword)] += 1
    repeated_keywords = [keyword for keyword, count in keyword_hits.items() if count >= 2]
    if repeated_keywords:
        patterns.append(
            make_pattern(
                "repeated_keyword_bridge",
                "重复关键词桥接",
                repeated_keywords[:5],
                "把重复关键词作为跨牌桥梁，说明不同牌位可能在谈同一个核心主题。",
                "重复关键词可以帮助收束主线，但需要结合牌位确认。",
                "关键词重复就等于现实必然发生同一件事。",
            )
        )

    if not patterns:
        patterns.append(
            make_pattern(
                "distributed_reading",
                "分散牌面",
                [f"{card['position']}={card['card']}" for card in cards],
                "未出现强聚集模式时，按牌位顺序逐层解释，并在结尾给出一个现实验证问题。",
                "牌面没有单一强模式，适合稳稳按牌位推进。",
                "为了显得完整而硬凑隐藏含义。",
            )
        )

    return patterns


def link_relationship(left: dict[str, Any], right: dict[str, Any]) -> tuple[str, str]:
    mapped = SPREAD_LINKS.get((str(left["position"]), str(right["position"])))
    if mapped:
        return mapped
    if left["orientation"] != right["orientation"]:
        return "orientation_shift", "比较两张牌从顺畅到阻滞或从阻滞到可见行动的变化。"
    if left.get("suit") and right.get("suit") and left["suit"] != right["suit"]:
        return "element_shift", "比较两个花色主题如何互相补充或拉扯。"
    if left["arcana"] != right["arcana"]:
        return "arcana_shift", "比较阶段性主题和日常现实层面的衔接。"
    return "sequential_reading", "按牌位顺序读成一条温和、非决定论的叙事线。"


def position_links(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    links = []
    for left, right in zip(cards, cards[1:]):
        relationship, prompt = link_relationship(left, right)
        links.append(
            {
                "from_position": left["position"],
                "from_card": left["card"],
                "to_position": right["position"],
                "to_card": right["card"],
                "relationship": relationship,
                "bridge_prompt": prompt,
            }
        )
    if len(cards) >= 4:
        for left, right in combinations(cards, 2):
            if left["position"] == "A 方案状态" and right["position"] == "B 方案状态":
                links.append(
                    {
                        "from_position": left["position"],
                        "from_card": left["card"],
                        "to_position": right["position"],
                        "to_card": right["card"],
                        "relationship": "path_comparison",
                        "bridge_prompt": "比较两条路径的当前条件，不替用户直接下决定。",
                    }
                )
    return links


def synthesis_prompt(patterns: list[dict[str, Any]], links: list[dict[str, Any]]) -> dict[str, Any]:
    primary = patterns[0]["pattern_id"] if patterns else "distributed_reading"
    return {
        "primary_pattern": primary,
        "reading_order": [
            "先说明本次组合只提供象征性反思，不替代现实判断。",
            "用 1-2 句交代最强组合模式。",
            "沿牌位链接说明张力如何流动。",
            "收束为 1-3 个可验证、低风险的小行动。",
        ],
        "opening_line_prompt": f"用可能性语言概括「{primary}」如何影响本次牌阵。",
        "closing_question": "读完这组牌后，用户最应该回到现实中验证哪一件小事？",
        "link_count": len(links),
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_draw(payload)
    recorded = normalized["recorded"]
    question_text = str(recorded.get("question_text", payload.get("question_text", ""))).strip()
    flags = risk_flags(question_text)
    cards = normalized_cards(recorded.get("draw", []), normalized["lookups"])
    can_continue = bool(recorded["is_valid"]) and not any(flag in {"coercion", "crisis"} for flag in flags)

    if not recorded["is_valid"]:
        return {
            "tool": "tarot_combination_planner",
            "question_text": question_text,
            "spread": recorded["spread"],
            "card_count": len(recorded.get("draw", [])),
            "can_continue_combination": False,
            "risk_flags": flags,
            "errors": normalized["errors"],
            "warnings": recorded["warnings"],
            "normalized_cards": cards,
            "combination_patterns": [],
            "position_links": [],
            "synthesis_prompt": {},
            "limits": [
                "Do not synthesize invalid or mismatched Tarot draws.",
                "Resolve card names, orientations, and spread positions before combination reading.",
            ],
            "next_steps": ["fix_draw_record", "rerun_tarot_combination_planner"],
        }

    patterns = combination_patterns(cards)
    links = position_links(cards)
    warnings = list(recorded["warnings"])
    if any(flag in {"medical", "professional_finance", "legal"} for flag in flags):
        warnings.append("high-stakes domain detected; keep the reading reflective and point back to qualified support.")
    if not can_continue:
        warnings.append("blocked risk detected; do not continue combination interpretation.")

    return {
        "tool": "tarot_combination_planner",
        "question_text": question_text,
        "spread": recorded["spread"],
        "card_count": len(cards),
        "can_continue_combination": can_continue,
        "risk_flags": flags,
        "errors": [],
        "warnings": warnings,
        "normalized_cards": cards,
        "combination_patterns": patterns if can_continue else [],
        "position_links": links if can_continue else [],
        "synthesis_prompt": synthesis_prompt(patterns, links) if can_continue else {},
        "limits": [
            "Use combination patterns as symbolic prompts, not predictions.",
            "Do not claim reversed cards, major arcana, or repeated suits guarantee outcomes.",
            "For medical, legal, financial, crisis, or coercive requests, redirect to safety and qualified support.",
            "In relationship readings, do not identify a court card as a certain real person.",
        ],
        "next_steps": [
            "merge_with_tarot_interpretation_planner",
            "draft_combination_reading_with_possibility_language",
            "run_mystic_output_lint",
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
