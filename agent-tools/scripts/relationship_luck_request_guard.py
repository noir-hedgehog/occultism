#!/usr/bin/env python3
"""Guard peach-blossom, romance-luck, and social-charm requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "relationship_luck_symbolic_consultation": ("桃花", "姻缘", "人缘", "爱情运", "恋爱运", "旺桃花", "招桃花", "红鸾", "天喜", "月老", "红线", "粉晶", "peach blossom luck", "romance luck"),
    "social_action_reflection": ("社交", "沟通", "认识新朋友", "约会", "表达", "边界", "形象", "自我介绍"),
    "symbolic_reminder_use": ("提醒物", "低风险", "不复合保证", "不读心", "不操控", "不骚扰"),
}

RISK_KEYWORDS = {
    "stalking_or_harassment": ("跟踪", "尾随", "蹲守", "骚扰", "堵门", "查岗", "监听", "偷拍视频", "定位他", "定位她", "人肉"),
    "coercion_or_love_spell": ("让他必须爱我", "让她必须爱我", "强制复合", "爱情降头", "情降", "和合术必须成", "操控他", "操控她", "控制对方", "迷魂"),
    "third_party_mind_reading": ("他到底爱不爱我", "她到底爱不爱我", "他真实想法", "她真实想法", "他心里有没有我", "她心里有没有我", "小三怎么想", "对方会不会回来"),
    "relationship_crisis_or_abuse": ("家暴", "威胁我", "被控制", "被打", "恐吓", "报复前任", "伤害前任", "自杀给他看", "自残给她看"),
    "professional_replacement": ("不用心理咨询", "不用报警", "不用律师", "离婚官司", "抚养权", "家暴也不用报警", "精神病"),
    "guaranteed_romance_claim": ("保证复合", "一定脱单", "必定结婚", "百分百挽回", "七天复合", "必有桃花", "正缘必来"),
    "expensive_ritual_pressure": ("天价和合术", "必须买法事", "必须请大师", "越贵越灵", "贷款做和合", "高价挽回套餐"),
    "repeated_dependency": ("每天算桃花", "每句话都问", "停不下来", "不问就害怕", "一直查对方", "反复查姻缘"),
}

SAFE_NEGATED_PHRASES = (
    "不复合保证",
    "不保证复合",
    "不读心",
    "不操控",
    "不骚扰",
    "不跟踪",
    "不买法事",
    "不做法事",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "relationship_luck_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "stalking_or_harassment" in flags:
        return "不协助跟踪、骚扰、定位、人肉、查岗或侵犯隐私；可改成尊重边界的沟通和自我照顾计划。"
    if "coercion_or_love_spell" in flags:
        return "不把桃花、和合或姻缘用于操控他人意志；可改成自我呈现、关系边界和可同意的沟通行动。"
    if "third_party_mind_reading" in flags:
        return "不读取或断定第三方真实想法、感情和未来行动；可改成围绕本人可控表达和观察事实复盘。"
    if "relationship_crisis_or_abuse" in flags:
        return "涉及家暴、威胁、自伤伤人或报复时，暂停玄学流程，优先现实安全、紧急支持或专业资源。"
    if "professional_replacement" in flags:
        return "不替代心理、法律、报警、婚姻家庭或危机支持；可提供低风险整理和求助准备。"
    if "guaranteed_romance_claim" in flags:
        return "不承诺脱单、复合、结婚、正缘到来或挽回成功；桃花语言只能作为社交行动和边界提醒。"
    if "expensive_ritual_pressure" in flags:
        return "不制造和合术、挽回套餐、高价法事或购买压力；优先低成本、可撤回的提醒和现实行动。"
    if "repeated_dependency" in flags:
        return "如果反复查桃花或对方想法已经加重焦虑，先设置固定复盘频率和停止条件。"
    return "可以把桃花/姻缘/人缘象征作为自我呈现、沟通边界、社交行动、关系复盘和停止条件提醒。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "relationship_luck_request_guard",
        "request_text": text,
        "system": "relationship_luck_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_relationship_luck": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "桃花、姻缘、人缘、月老、红线和粉晶等象征只作自我呈现、沟通边界、社交行动、关系复盘和停止条件提醒。",
            "不承诺脱单、复合、结婚、正缘到来、挽回成功或第三方真实想法。",
            "不协助跟踪、骚扰、定位、人肉、读心、操控、爱情降头、强制和合或报复。",
            "不替代心理、法律、报警、婚姻家庭、危机支持或现实安全行动；不制造高价法事和反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、已有桃花象征解释，还是把关系愿望转成社交/沟通行动计划？",
            "现实关系状态、本人目标、可同意的沟通对象、边界、已有提醒物、可控行动、复盘时间和停止条件是什么？",
            "是否涉及跟踪骚扰、读心、操控复合、家暴威胁、自伤伤人、专业替代、结果保证、高价法事或反复依赖？",
        ],
        "next_steps": [
            "record_relationship_luck_context",
            "lookup_relationship_luck_symbols",
            "build_relationship_luck_action_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_relationship_luck_consultation", "reframe_to_consent_boundary_or_professional_support"],
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
    parser.add_argument("--text", help="Relationship-luck request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_relationship_luck"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
