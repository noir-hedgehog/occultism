#!/usr/bin/env python3
"""Guard palmistry and physiognomy requests before symbolic consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "palm_symbol_reflection": ("手相", "掌纹", "生命线", "智慧线", "感情线", "事业线", "太阳线", "掌丘"),
    "face_symbol_reflection": ("面相", "相术", "五官", "额头", "眉", "眼", "鼻", "嘴", "下巴", "痣相"),
    "appearance_judgment": ("好不好看", "漂亮", "丑", "颜值", "旺夫", "克夫", "克妻", "贵贱"),
    "health_or_lifespan": ("健康", "有病", "病", "短命", "寿命", "死", "活多久", "长寿"),
    "cultural_learning": ("讲讲", "科普", "文化", "什么意思", "怎么理解", "来源"),
}

RISK_KEYWORDS = {
    "health_diagnosis": ("健康", "有病", "病", "癌", "诊断", "治疗", "用药", "医生"),
    "lifespan_claim": ("短命", "寿命", "活多久", "会死", "死亡", "长寿"),
    "appearance_discrimination": ("丑", "漂亮不漂亮", "颜值", "贵贱", "旺夫", "克夫", "克妻", "扫把星"),
    "third_party_nonconsent": ("他", "她", "别人", "同事", "老板", "前任", "对象", "伴侣", "偷拍"),
    "deterministic_fate": ("注定", "一定", "必然", "必发财", "必离婚", "命不好", "富贵命", "劳碌命"),
    "coercive_profiling": ("筛人", "招聘", "录用", "淘汰", "判断人品", "看是不是坏人"),
    "minor_subject": ("孩子", "小孩", "宝宝", "未成年", "学生"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword.lower() in text.lower() for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "symbolic_reflection"


def consent_state(payload: dict[str, Any]) -> str:
    if payload.get("subject_is_self") is True:
        return "self"
    if payload.get("consent_obtained") is True:
        return "consented_subject"
    if payload.get("cultural_learning_only") is True:
        return "anonymous_cultural_learning"
    return "missing_or_unknown"


def risk_flags_for(text: str, payload: dict[str, Any]) -> list[str]:
    flags = [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]
    consent = consent_state(payload)
    if consent == "missing_or_unknown" and "third_party_nonconsent" in flags:
        return flags
    if consent in {"self", "consented_subject", "anonymous_cultural_learning"} and "third_party_nonconsent" in flags:
        flags.remove("third_party_nonconsent")
    return flags


def can_continue(flags: list[str], consent: str) -> bool:
    blocking = {
        "health_diagnosis",
        "lifespan_claim",
        "appearance_discrimination",
        "third_party_nonconsent",
        "coercive_profiling",
    }
    if blocking.intersection(flags):
        return False
    if consent == "missing_or_unknown":
        return False
    return True


def reframe(flags: list[str], consent: str) -> str:
    if "health_diagnosis" in flags:
        return "不从掌纹、五官或痣相判断健康；可改为：这个象征传统在文化上如何被解释，我现实上该如何照顾身体并咨询医生？"
    if "lifespan_claim" in flags:
        return "不判断寿命、短命或死亡时间；可改为：生命线在传统手相里通常承载哪些活力与节奏象征？"
    if "appearance_discrimination" in flags:
        return "不做颜值、贵贱、旺克或歧视性标签；可改为：某个五官意象在相术文化里如何被象征化？"
    if "third_party_nonconsent" in flags or consent == "missing_or_unknown":
        return "缺少本人同意时，不解读第三方手相、面相或性格命运；可改为匿名文化学习或自己的反思问题。"
    if "coercive_profiling" in flags:
        return "不把相术用于筛人、淘汰、招聘或判断人品；可改为讨论沟通事实、岗位标准和现实证据。"
    if "deterministic_fate" in flags:
        return "把注定、必然和富贵贫贱改写为象征偏向、个人叙事和低风险行动。"
    return "可以在本人同意、非诊断、非寿命、非歧视的前提下做象征反思。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    consent = consent_state(payload)
    flags = risk_flags_for(text, payload)
    allowed = can_continue(flags, consent)
    return {
        "tool": "physiognomy_request_guard",
        "request_text": text,
        "system": "palmistry_and_physiognomy_symbolism",
        "reading_intent": detect_intent(text),
        "consent_state": consent,
        "risk_flags": flags,
        "can_continue_physiognomy": allowed,
        "reframed_question": reframe(flags, consent),
        "required_boundaries": [
            "只处理用户自述或明确授权的观察，不从照片推断健康、身份、寿命、性格或价值。",
            "手相/面相只能作为文化象征和自我反思语言，不证明命运、财富、婚恋或人品。",
            "不得做健康诊断、寿命判断、颜值歧视、旺克标签、第三方隐私分析或招聘筛选。",
        ],
        "clarifying_questions": [
            "是否为本人，或是否已经获得当事人同意？",
            "用户想讨论手相、面相、痣相中的哪些已知观察？",
            "目标是文化学习、象征反思、写作素材，还是现实决策整理？",
        ],
        "next_steps": [
            "record_user_provided_observations",
            "lookup_safe_symbols",
            "build_symbolic_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_physiognomy_reading", "reframe_to_consent_cultural_learning_or_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["request_text"] = args.text
    if args.subject_is_self:
        payload["subject_is_self"] = True
    if args.consent_obtained:
        payload["consent_obtained"] = True
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Palmistry or physiognomy request text.")
    parser.add_argument("--subject-is-self", action="store_true", help="Subject is the user.")
    parser.add_argument("--consent-obtained", action="store_true", help="Subject consent is confirmed.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_physiognomy"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
