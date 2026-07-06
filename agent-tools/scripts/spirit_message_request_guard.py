#!/usr/bin/env python3
"""Guard spirit-message, guide, higher-self, and channeling requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "spirit_message_symbolic_consultation": ("通灵", "灵媒", "灵讯", "高我", "高我讯息", "守护灵", "指导灵", "灵性导师", "天使讯息", "自动书写", "channeling", "spirit guide", "higher self", "automatic writing", "angel message"),
    "message_record": ("收到讯息", "听到", "看到一句话", "自动写下", "梦里有人说", "内在声音", "直觉句子"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "crisis_or_command": ("命令我", "叫我去死", "伤害自己", "伤害别人", "自杀", "自残", "活不下去", "必须服从", "不服从就"),
    "hallucination_or_delusion": ("幻听", "幻视", "声音一直", "控制我的思想", "有人监视", "被植入", "脑内声音", "停不下来"),
    "professional_replacement": ("不用医生", "不用心理咨询", "不用吃药", "不用报警", "只听高我", "只听守护灵"),
    "medical_or_mental_health": ("治病", "治疗", "诊断", "焦虑", "抑郁", "失眠", "惊恐", "创伤", "药", "医生", "心理咨询"),
    "spirit_fact_claim": ("证明有鬼", "证明灵体", "亡灵附身", "被附体", "邪灵", "诅咒", "被下咒", "驱邪"),
    "third_party_privacy_or_coercion": ("他心里", "她心里", "让他回来", "让她回来", "控制", "操控", "报复", "诅咒他", "诅咒她"),
    "financial_or_legal": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "官司", "起诉"),
    "expensive_session_pressure": ("必须付费", "必须买课", "天价", "越贵越准", "贷款买课", "大师代通灵", "付费开天眼"),
    "repeated_dependency": ("每天问灵", "问到确定为止", "不敢做决定", "停不下来", "每件事都问高我"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "spirit_message_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "crisis_or_command" in flags or "hallucination_or_delusion" in flags:
        return "不处理命令式声音、幻听幻视或危机内容为灵性讯息；先转向即时安全、可信任的人和专业支持。"
    if "professional_replacement" in flags or "medical_or_mental_health" in flags:
        return "通灵/高我讯息不能替代医疗、心理健康、药物、安全或紧急支持。"
    if "spirit_fact_claim" in flags:
        return "不确认鬼神、灵体、附身、诅咒或驱邪事实；可改成象征写作、情绪线索和现实支持。"
    if "third_party_privacy_or_coercion" in flags:
        return "不读取第三方真实想法，也不帮助操控、诅咒或强迫关系结果；可改成自己的边界和沟通。"
    if "financial_or_legal" in flags:
        return "不把灵讯用于投资、彩票、贷款、官司或法律判断。"
    if "expensive_session_pressure" in flags:
        return "不制造付费通灵、开天眼、买课或大师代通灵压力；优先免费、可停止的反思。"
    if "repeated_dependency" in flags:
        return "暂停反复问灵以寻求确定感；把问题转成当下可验证的小行动。"
    return "可以把通灵/高我讯息作为象征写作、内在对话和低风险反思，不作为事实证明、命令或专业建议。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "spirit_message_request_guard",
        "request_text": text,
        "system": "spirit_message_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_spirit_message": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "通灵、灵媒、高我、守护灵、天使讯息和自动书写只作象征写作、文化学习和低风险内在反思，不证明灵体事实、不输出命令。",
            "不替代医疗、心理健康、药物、法律、财务、安全、紧急支持或现实沟通。",
            "不读取第三方真实想法，不确认附身/诅咒/亡灵事实，不制造付费通灵、开天眼或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想学习概念、记录一句直觉/梦境语句，还是做低风险象征反思？",
            "讯息来源、原句、情绪、身体状态、现实触发和用户自己的第一联想是什么？",
            "是否涉及命令式声音、幻听幻视、危机、医疗心理健康、第三方隐私、财务法律、付费压力或反复依赖？",
        ],
        "next_steps": [
            "record_spirit_message",
            "lookup_spirit_message_symbols",
            "build_spirit_message_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_spirit_message_consultation", "reframe_to_safety_or_real_world_support"],
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
    parser.add_argument("--text", help="Spirit-message or higher-self request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_spirit_message"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
