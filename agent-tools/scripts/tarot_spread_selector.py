#!/usr/bin/env python3
"""Select a safe Tarot spread and question framing for a user request."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Spread:
    spread_id: str
    name: str
    card_count: int
    positions: tuple[str, ...]
    best_for: tuple[str, ...]
    avoid_when: tuple[str, ...]
    notes: tuple[str, ...]


SPREADS = {
    "single_focus": Spread(
        "single_focus",
        "单张聚焦",
        1,
        ("当前提醒",),
        ("daily_focus", "self_reflection", "cultural_learning"),
        ("需要比较多个方案", "用户期待确定预测"),
        ("适合低风险、轻量的状态观察。",),
    ),
    "three_card_situation": Spread(
        "three_card_situation",
        "三张状态牌阵",
        3,
        ("现状", "阻碍", "建议"),
        ("career", "relationship", "self_reflection", "general"),
        ("问题要求替代专业判断",),
        ("优先用于整理局势，而不是预测结果。",),
    ),
    "past_present_tendency": Spread(
        "past_present_tendency",
        "过去-现在-趋势",
        3,
        ("过去影响", "当前状态", "趋势提醒"),
        ("timeline", "relationship", "career"),
        ("用户要求确定日期或结果",),
        ("趋势只能作为提醒，不作为确定预言。",),
    ),
    "two_paths": Spread(
        "two_paths",
        "二选一路径",
        5,
        ("A 方案状态", "A 方案提醒", "B 方案状态", "B 方案提醒", "共同建议"),
        ("choice", "career", "move", "relationship"),
        ("选择涉及医疗、法律、重大财务风险且用户要 agent 代替决定",),
        ("输出应帮助比较取舍，不替用户做最终决定。",),
    ),
    "relationship_mirror": Spread(
        "relationship_mirror",
        "关系镜像",
        4,
        ("我的状态", "对方可能状态", "互动模式", "边界建议"),
        ("relationship",),
        ("监控、操控、复仇、强迫复合",),
        ("对方状态只能表述为可能性，重点放在用户边界和行动。",),
    ),
    "decision_grounding": Spread(
        "decision_grounding",
        "决策落地",
        4,
        ("真正关切", "可用资源", "主要风险", "下一步"),
        ("decision_support", "career", "move"),
        ("投资、贷款、赌博、医疗、法律等专业决策",),
        ("适合把焦虑拆成资源、风险和下一步。",),
    ),
}

DOMAIN_KEYWORDS = {
    "relationship": ("关系", "感情", "复合", "分手", "他", "她", "暧昧", "伴侣", "出轨", "回来"),
    "career": ("工作", "事业", "offer", "跳槽", "辞职", "面试", "老板", "同事", "项目"),
    "choice": ("二选一", "选择", "选哪个", "该选", "要不要", "还是", "方案", "a offer", "b offer", "A 方案", "B 方案"),
    "move": ("搬家", "城市", "换房", "搬去", "留在"),
    "daily_focus": ("今日", "今天", "每日", "一天", "提醒"),
    "timeline": ("过去", "现在", "趋势", "未来", "发展"),
    "cultural_learning": ("塔罗是什么", "牌阵是什么", "学习", "介绍", "讲讲"),
}

RISK_KEYWORDS = {
    "professional_decision": ("医生", "用药", "手术", "律师", "起诉", "合同", "股票", "贷款", "赌博", "彩票", "梭哈"),
    "coercion": ("控制", "让他爱我", "让她爱我", "报复", "下咒", "诅咒"),
    "crisis": ("自杀", "自残", "活不下去", "伤害", "家暴", "跟踪"),
}


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_question_type(text: str) -> str:
    if contains_any(text, DOMAIN_KEYWORDS["choice"]):
        return "choice"
    for question_type, keywords in DOMAIN_KEYWORDS.items():
        if contains_any(text, keywords):
            return question_type
    return "general"


def detect_risk_flags(text: str) -> list[str]:
    flags = []
    for risk, keywords in RISK_KEYWORDS.items():
        if contains_any(text, keywords):
            flags.append(risk)
    return flags


def select_spread(question_type: str, text: str) -> Spread:
    if question_type == "choice":
        return SPREADS["two_paths"]
    if question_type == "relationship":
        if contains_any(text, ("回来", "复合", "对方", "他", "她")):
            return SPREADS["relationship_mirror"]
        return SPREADS["three_card_situation"]
    if question_type in {"career", "timeline"}:
        return SPREADS["three_card_situation"]
    if question_type == "move":
        return SPREADS["two_paths"]
    if question_type == "daily_focus":
        return SPREADS["single_focus"]
    if question_type == "cultural_learning":
        return SPREADS["single_focus"]
    return SPREADS["three_card_situation"]


def reframe_question(text: str, question_type: str, risk_flags: list[str]) -> str:
    if "crisis" in risk_flags:
        return "先暂停塔罗，把问题改为：我现在如何获得即时安全和可信任支持？"
    if "professional_decision" in risk_flags:
        return "塔罗不能替代专业判断；可改为：我对这个决定的担忧、资源和下一步准备是什么？"
    if "coercion" in risk_flags:
        return "不做操控他人的提问；可改为：我如何照顾自己的边界，并以尊重的方式处理关系？"

    if question_type == "relationship":
        return "这段关系里我能看见哪些互动模式，以及我接下来如何照顾自己的边界？"
    if question_type == "choice":
        return "两个选择分别提醒我注意什么，我可以如何比较取舍？"
    if question_type == "career":
        return "我当前的工作局势、阻碍和下一步重点是什么？"
    if question_type == "move":
        return "两个居住/行动方案分别有什么提醒，我需要优先确认哪些现实条件？"
    if question_type == "daily_focus":
        return "今天我最需要留意的状态或行动重点是什么？"
    if question_type == "timeline":
        return "这件事从过去影响、当前状态到趋势提醒，可以如何理解？"
    return "我可以从这件事里看见哪些状态、阻碍和可行动的下一步？"


def build_limits(risk_flags: list[str]) -> list[str]:
    limits = [
        "塔罗输出只能作为象征性反思，不作为确定预言。",
        "不得替代医疗、法律、财务或紧急安全建议。",
    ]
    if "coercion" in risk_flags:
        limits.append("不得用于操控、报复或强迫他人。")
    if "crisis" in risk_flags:
        limits.append("出现即时危险时应先联系当地紧急服务或可信任的人。")
    return limits


def select(payload: dict[str, object]) -> dict[str, object]:
    text = str(payload.get("question_text", payload.get("request_text", ""))).strip()
    if not text:
        raise ValueError("question_text or request_text is required")

    question_type = detect_question_type(text)
    risk_flags = detect_risk_flags(text)
    spread = select_spread(question_type, text)
    can_continue = not any(flag in risk_flags for flag in ("crisis", "coercion"))

    return {
        "question_text": text,
        "question_type": question_type,
        "risk_flags": risk_flags,
        "can_continue_tarot": can_continue,
        "recommended_spread": {
            "spread_id": spread.spread_id,
            "name": spread.name,
            "card_count": spread.card_count,
            "positions": list(spread.positions),
            "best_for": list(spread.best_for),
            "avoid_when": list(spread.avoid_when),
            "notes": list(spread.notes),
        },
        "reframed_question": reframe_question(text, question_type, risk_flags),
        "limits": build_limits(risk_flags),
        "next_steps": [
            "run_mystic_intake_triage_first",
            "confirm_or_adjust_reframed_question",
            "record_draw_with_positions",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"question_text": raw}
    if args.text:
        return {"question_text": args.text}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"question_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Tarot question text.")
    parser.add_argument("--json", help="JSON object input with question_text or request_text.")
    parser.add_argument("--file", help="Path to question text or JSON input.")
    args = parser.parse_args()
    try:
        result = select(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
