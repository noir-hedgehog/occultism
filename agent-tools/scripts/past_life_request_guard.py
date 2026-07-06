#!/usr/bin/env python3
"""Guard past-life, Akashic-record, and soul-theme requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "past_life_akashic_symbolic_consultation": ("前世", "前生", "累世", "宿世", "阿卡西", "阿卡莎", "akashic", "past life", "soul contract", "灵魂契约", "灵魂课题", "灵魂伴侣", "业力关系", "业力", "因果课题"),
    "narrative_record": ("画面", "场景", "身份", "年代", "地点", "梦到", "冥想看到", "片段", "主题"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "memory_recovery_or_hypnosis": ("催眠", "前世回溯", "找回记忆", "恢复记忆", "被封印的记忆", "忘掉的创伤", "一定发生过", "证明我前世"),
    "trauma_or_abuse_confirmation": ("是不是被虐待", "是不是被侵犯", "是不是被杀", "凶手是谁", "谁害了我", "童年创伤", "创伤根源"),
    "medical_or_mental_health": ("治病", "治疗", "诊断", "焦虑", "抑郁", "失眠", "幻听", "幻视", "惊恐", "创伤后", "ptsd", "药", "医生", "心理咨询"),
    "fatalism_or_identity_label": ("注定", "逃不掉", "必须还债", "业障深重", "灵魂低级", "天生有罪", "永远不会好", "前世欠债"),
    "relationship_coercion": ("他是我的灵魂伴侣所以必须回来", "她是我的灵魂伴侣所以必须回来", "控制他", "控制她", "让他回来", "让她回来", "斩断他和别人", "第三者"),
    "third_party_privacy": ("看他的前世", "看她的前世", "他前世是谁", "她前世是谁", "他的灵魂契约", "她的灵魂契约", "真实想法"),
    "financial_or_legal": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "官司", "起诉", "离婚官司"),
    "expensive_session_pressure": ("必须付费", "必须买课", "必须做疗愈", "天价", "越贵越准", "贷款买课", "大师解读", "远程清理"),
    "repeated_dependency": ("每天查阿卡西", "反复看前世", "不敢做决定", "查到确定为止", "停不下来", "必须知道前世才"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "past_life_akashic_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "memory_recovery_or_hypnosis" in flags or "trauma_or_abuse_confirmation" in flags:
        return "不确认前世记忆、被封印记忆或创伤事实；可改成象征叙事、梦境/冥想画面记录和现实支持。"
    if "medical_or_mental_health" in flags:
        return "前世/阿卡西叙事不能替代医疗、心理健康、药物、危机或创伤支持。"
    if "fatalism_or_identity_label" in flags:
        return "不把前世、业力或灵魂课题写成注定、罪责、等级或无法改变的身份标签。"
    if "relationship_coercion" in flags or "third_party_privacy" in flags:
        return "不读取第三方前世、灵魂契约或真实想法，也不帮助操控关系；可改成自己的边界和选择。"
    if "financial_or_legal" in flags:
        return "不把前世或阿卡西叙事用于投资、赌博、贷款、官司或法律判断。"
    if "expensive_session_pressure" in flags:
        return "不制造付费解读、疗愈课程或远程清理压力；优先低成本、可停止的反思。"
    if "repeated_dependency" in flags:
        return "暂停反复查询以寻求确定感；先把问题转成当下可验证的小行动。"
    return "可以把前世/阿卡西作为象征叙事和主题反思，不作为事实证明、记忆恢复、创伤确认或命运判决。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "past_life_request_guard",
        "request_text": text,
        "system": "past_life_akashic_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_past_life": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "前世、阿卡西、灵魂契约和业力只作象征叙事、文化学习和低风险反思，不证明事实、不恢复记忆、不确认创伤。",
            "不替代医疗、心理健康、创伤治疗、法律、财务、安全、紧急支持或现实沟通。",
            "不输出宿命论、罪责标签、灵魂等级、第三方隐私、关系操控、付费疗愈必要性或反复依赖诱导。",
        ],
        "clarifying_questions": [
            "用户是想学习概念、记录梦境/冥想画面，还是做低风险象征反思？",
            "画面里的角色、地点、时代感、情绪、重复主题和用户自己的第一联想是什么？",
            "是否涉及创伤事实确认、医疗/心理健康、第三方隐私、关系操控、付费压力或反复依赖？",
        ],
        "next_steps": [
            "record_past_life_narrative",
            "lookup_past_life_symbols",
            "build_past_life_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_past_life_consultation", "reframe_to_symbolic_or_real_world_support"],
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
    parser.add_argument("--text", help="Past-life, Akashic, or soul-theme request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_past_life"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
