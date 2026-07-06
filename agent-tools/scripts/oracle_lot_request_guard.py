#!/usr/bin/env python3
"""Guard oracle-lot and temple-lot divination requests before interpretation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "lot_interpretation": ("求签", "解签", "签文", "签诗", "签号", "观音签", "月老签", "灵签", "抽签"),
    "draw_request": ("帮我抽", "代抽", "模拟抽签", "在线抽签", "抽一签"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "怎么解"),
    "decision_support": ("要不要", "适不适合", "选择", "怎么办", "下一步"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用看合同", "只看签", "全听签"),
    "medical": ("诊断", "用药", "手术", "怀孕", "病", "癌", "医生"),
    "legal": ("起诉", "坐牢", "刑事", "律师", "离婚官司", "移民"),
    "financial": ("股票", "彩票", "赌博", "投资", "贷款", "币圈", "梭哈"),
    "deterministic_fate": ("一定", "必然", "注定", "必发财", "必复合", "必分手", "必有灾", "大祸"),
    "coercion": ("让他爱我", "让她爱我", "控制他", "控制她", "报复", "下咒"),
    "third_party_privacy": ("他是不是", "她是不是", "前任", "对方想", "爱不爱我", "真实想法"),
    "dependency_loop": ("一直抽", "反复抽", "抽到满意", "每天抽很多次"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    blocking = {"professional_replacement", "medical", "legal", "financial", "coercion"}
    return not bool(blocking.intersection(flags))


def reframe(flags: list[str]) -> str:
    if {"medical", "legal", "financial", "professional_replacement"}.intersection(flags):
        return "不把签文作为医疗、法律、财务或安全决策依据；可改为：签文给我哪些反思问题，现实上我该咨询哪些专业人士？"
    if "coercion" in flags:
        return "不把求签用于操控、报复或强迫关系；可改为：我如何尊重边界并整理自己的需要？"
    if "third_party_privacy" in flags:
        return "不通过签文断定第三方真实想法；可改为：我能观察到哪些事实，以及自己的边界是什么？"
    if "deterministic_fate" in flags:
        return "把必然结论改写为象征提醒、风险清单和可控行动。"
    if "dependency_loop" in flags:
        return "不鼓励反复抽到满意；可固定一次签文，转为记录和现实行动。"
    return "可以把签文作为文化象征和决策整理材料，不作为命令或保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("question_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("request_text, question_text, or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "oracle_lot_request_guard",
        "request_text": text,
        "system": "oracle_lot_symbolism",
        "reading_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_oracle_lot": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "签文只能作为文化象征、情绪整理和低风险决策辅助，不保证结果。",
            "医疗、法律、财务、人身安全和高压关系问题必须优先使用现实专业支持。",
            "不反复抽到满意，不用签文操控他人或断定第三方真实想法。",
        ],
        "clarifying_questions": [
            "签文来自哪里：寺庙、书籍、应用、用户已抽，还是希望模拟抽签？",
            "用户的问题是否能改写为一事一问和可行动反思？",
            "是否涉及医疗、法律、财务、安全、操控或第三方隐私？",
        ],
        "next_steps": [
            "record_lot_source_and_text",
            "lookup_lot_symbols",
            "build_oracle_lot_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_oracle_lot_reading", "reframe_to_reality_support_or_symbolic_reflection"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.text:
        return {"request_text": args.text}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Oracle-lot request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_oracle_lot"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
