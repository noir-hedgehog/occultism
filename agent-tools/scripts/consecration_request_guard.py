#!/usr/bin/env python3
"""Guard consecration, blessing, and object-cleansing requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "consecration_symbolic_consultation": ("开光", "加持", "净物", "净化物件", "净化手串", "净化水晶", "过香火", "祝福物件", "consecration", "blessing", "cleanse object"),
    "object_reminder_use": ("物件", "手串", "水晶", "护符", "貔貅", "红绳", "香囊", "提醒物"),
    "low_risk_care": ("低风险", "无火", "不喝符水", "不保证灵验", "不买法事", "不替代医生"),
}

RISK_KEYWORDS = {
    "dangerous_ritual": ("放血", "割腕", "血祭", "密闭燃烧", "通宵点香", "酒精点火", "火烧", "烧头发", "烧照片", "刀割"),
    "ingestion_or_body_harm": ("喝符水", "吃香灰", "喝香灰", "吞符", "涂血", "滴血", "伤口", "刺破手指"),
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用心理咨询", "不用财务顾问", "病不用治", "合同不用看"),
    "guaranteed_effect": ("一定灵", "必灵", "保证灵验", "保证平安", "保证发财", "立刻转运", "消灾免祸", "百分百挡灾"),
    "expensive_ritual_pressure": ("天价开光", "开光套餐", "加持套餐", "必须请大师", "越贵越灵", "贷款开光", "必须买法事"),
    "deity_command_or_fear": ("神明命令", "不开光就倒霉", "不开光会招邪", "被封印", "不加持就出事", "物件有鬼"),
    "fraud_or_coercion": ("骗客户", "让客户必须买", "操控别人", "诅咒别人", "害竞争对手"),
    "repeated_dependency": ("每天开光", "反复加持", "停不下来", "不做就害怕", "每次出门都要净化"),
}

SAFE_NEGATED_PHRASES = (
    "不用明火",
    "不喝符水",
    "不吃香灰",
    "不滴血",
    "不买法事",
    "不保证灵验",
    "不保证发财",
    "不替代医生",
    "不高价",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "consecration_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "dangerous_ritual" in flags:
        return "不提供放血、燃烧、刀具、密闭燃烧或通宵明火步骤；可改成无火清洁、来源记录和提醒物整理。"
    if "ingestion_or_body_harm" in flags:
        return "不建议喝符水、吃香灰、吞符、滴血或任何伤害身体的做法。"
    if "professional_replacement" in flags:
        return "不把开光、加持或净物替代医疗、法律、报警、心理或财务专业支持。"
    if "guaranteed_effect" in flags:
        return "不承诺灵验、挡灾、转运、发财或平安保证；只能作为文化象征和提醒物使用。"
    if "expensive_ritual_pressure" in flags:
        return "不制造开光套餐、大师、高价法事或贷款购买压力；优先低成本、可撤回流程。"
    if "deity_command_or_fear" in flags:
        return "不确认神明命令、物件招邪或不开光会出事；可改成物件来源、感受和现实安全整理。"
    if "fraud_or_coercion" in flags:
        return "不协助欺骗客户、操控他人、诅咒或伤害竞争对手。"
    if "repeated_dependency" in flags:
        return "如果反复开光/净物已经加重焦虑，先设置固定频率和停止条件。"
    return "可以把开光、加持或净物改写为物件来源记录、清洁整理、无火提醒物使用和复盘。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "consecration_request_guard",
        "request_text": text,
        "system": "consecration_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_consecration": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "开光、加持、净物和净化物件只作文化象征、来源记录、清洁整理、提醒物使用和复盘。",
            "不承诺灵验、挡灾、发财、转运、平安保证或神明命令。",
            "不提供放血、摄入、刀具、危险燃烧、密闭明火、伤身做法或违法操控。",
            "不替代医疗、法律、报警、心理、财务专业支持；不制造高价法事或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、已有物件整理，还是做无火低风险提醒物流程？",
            "物件来源、当前用途、已有物件、安全边界、可控动作、复盘时间和停止条件是什么？",
            "是否涉及危险仪式、摄入/伤身、专业替代、灵验保证、高价开光、神明恐吓、欺骗操控或反复依赖？",
        ],
        "next_steps": [
            "record_consecration_context",
            "lookup_consecration_symbols",
            "build_consecration_care_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_consecration_consultation", "reframe_to_low_risk_object_care_or_professional_support"],
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
    parser.add_argument("--text", help="Consecration request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_consecration"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
