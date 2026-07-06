#!/usr/bin/env python3
"""Build a safe interpretation plan for Lenormand card readings."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import lenormand_card_lookup
import lenormand_draw_recorder


def build_card_plan(query: str, focus: str, position: str) -> dict[str, Any]:
    card = lenormand_card_lookup.lookup({"query": query, "focus": focus})
    return {
        "position": position,
        "card": card["canonical_name"],
        "card_code": card["card_code"],
        "keywords": card["keywords"],
        "interpretation_prompt": card["interpretation_prompt"],
        "reflection_questions": card["reflection_questions"],
        "action_guidance": card["action_guidance"],
    }


def adjacent_pairs(card_plans: list[dict[str, Any]]) -> list[dict[str, str]]:
    pairs: list[dict[str, str]] = []
    for left, right in zip(card_plans, card_plans[1:]):
        pairs.append(
            {
                "left": str(left["card"]),
                "right": str(right["card"]),
                "prompt": f"把「{left['card']} + {right['card']}」读成相邻线索：动作/对象/条件如何互相限定？",
            }
        )
    return pairs


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = lenormand_draw_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["spread_type"]
    if not record["can_continue_lenormand"]:
        return {
            "tool": "lenormand_interpretation_planner",
            "is_valid": False,
            "can_continue_lenormand": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "card_plans": [],
            "pair_plans": [],
            "interpretation_layers": [],
            "synthesis": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_lenormand_reading", "reframe_to_real_world_support"],
        }
    positions = record["positions"]
    card_plans = []
    for index, card in enumerate(record["cards"]):
        position = positions[index] if index < len(positions) else f"card_{index + 1}"
        try:
            card_plans.append(build_card_plan(card, focus, position))
        except ValueError:
            card_plans.append(
                {
                    "position": position,
                    "card": card,
                    "card_code": "unknown",
                    "keywords": [],
                    "interpretation_prompt": "用户提供的牌名不在当前 36 张雷诺曼索引中；先要求确认牌名或来源。",
                    "reflection_questions": ["是否为标准 36 张雷诺曼牌？", "是否需要用户补充牌面转写？"],
                    "action_guidance": "不强行解释未知牌。",
                }
            )
    return {
        "tool": "lenormand_interpretation_planner",
        "is_valid": True,
        "can_continue_lenormand": True,
        "question_text": record["question_text"],
        "spread_type": record["spread_type"],
        "positions": positions,
        "cards": record["cards"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "card_plans": card_plans,
        "pair_plans": adjacent_pairs(card_plans),
        "interpretation_layers": [
            "先说明雷诺曼只作象征反思和问题整理，不证明事实或替用户决定。",
            "确认牌阵位置和抽牌来源，未知牌先要求确认。",
            "逐张解释牌义，并用相邻牌形成事件线索或条件限定。",
            "把现实证据、专业边界、当事人沟通和用户价值排序放在象征之前。",
            "若出现依赖、恐惧、专业替代、财务投机或第三方操控，暂停雷诺曼流程。",
        ],
        "synthesis": {
            "core_prompt": "这组雷诺曼牌能帮助用户澄清哪条事件线索、现实条件、边界或低风险下一步？",
            "card_count": len(card_plans),
            "pair_count": max(0, len(card_plans) - 1),
            "grounded_actions": [
                "把牌义拆成现实事实、个人偏好和下一步行动三列。",
                "对每组相邻牌给出一个可核查或可撤回的现实动作。",
                "为同一问题设置停止追问条件，避免反复依赖。",
            ],
        },
        "limits": [
            "Use symbolic reflection language only.",
            "Do not present Lenormand cards as fact, diagnosis, prediction, curse confirmation, or instruction.",
            "Do not decide medical, legal, financial, safety, or third-party matters.",
        ],
        "next_steps": ["draft_lenormand_answer_from_plan", "run_mystic_output_lint", "offer_reality_evidence_checklist"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["question_text"] = args.text
    if args.cards:
        payload["cards"] = args.cards
    if args.spread_type:
        payload["spread_type"] = args.spread_type
    if args.focus:
        payload["focus"] = args.focus
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"question_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Lenormand question or session notes.")
    parser.add_argument("--cards", help="Drawn cards separated by space, comma, or Chinese comma.")
    parser.add_argument("--spread-type", help="three_card_line, five_card_line, or nine_card_box.")
    parser.add_argument("--focus", help="Optional focus.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = plan(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
