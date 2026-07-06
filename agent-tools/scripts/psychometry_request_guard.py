#!/usr/bin/env python3
"""Guard psychometry and object-reading requests before symbolic reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "psychometry_symbolic_consultation": ("物品感应", "触物占卜", "物件能量", "旧物能量", "首饰能量", "遗物能量", "读物品", "psychometry", "object reading", "read this object"),
    "object_record": ("戒指", "项链", "手表", "钥匙", "照片", "旧书", "衣物", "首饰", "遗物", "二手物", "古董"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "missing_person_or_crime": ("失踪", "凶手", "谋杀", "杀人", "犯罪", "案子", "尸体", "遗体", "定位", "找到人", "找孩子"),
    "third_party_privacy": ("他心里", "她心里", "前任想法", "真实想法", "偷看", "隐私", "秘密", "出轨没有", "背叛没有"),
    "no_owner_consent": ("偷偷拿", "不是我的", "没同意", "未经同意", "别告诉他", "别告诉她"),
    "spirit_fact_claim": ("有鬼", "灵体", "亡灵", "附身", "被附体", "诅咒", "邪灵", "驱邪", "阴气"),
    "professional_replacement": ("不用医生", "不用报警", "不用律师", "不用鉴定", "不用检测", "只靠感应"),
    "medical_or_safety": ("治病", "治疗", "诊断", "中毒", "感染", "过敏", "危险品", "药", "医生"),
    "financial_or_legal": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "官司", "起诉", "遗产"),
    "identity_or_authenticity_claim": ("鉴定真假", "证明真伪", "一定是真的", "一定是假的", "谁的", "属于谁"),
    "expensive_cleansing_pressure": ("必须付费", "必须买", "天价", "大师净化", "开光", "越贵越灵", "贷款"),
    "repeated_dependency": ("每个东西都感应", "反复确认", "停不下来", "不敢碰", "不敢丢", "每天问"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "psychometry_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "missing_person_or_crime" in flags:
        return "不把物品感应用于失踪、犯罪、定位或刑案判断；这类内容应转向现实安全、警方或专业机构。"
    if "third_party_privacy" in flags or "no_owner_consent" in flags:
        return "不读取第三方隐私或未经同意的物品；可改成用户本人拥有或获授权物件的象征联想。"
    if "spirit_fact_claim" in flags:
        return "不确认灵体、亡灵、附身、诅咒、阴气或驱邪事实；可改成情绪、记忆和边界整理。"
    if "professional_replacement" in flags or "medical_or_safety" in flags:
        return "物品感应不能替代医疗、安全检测、报警、法律或专业鉴定。"
    if "financial_or_legal" in flags:
        return "不把物品感应用于投资、彩票、贷款、官司、遗产或法律判断。"
    if "identity_or_authenticity_claim" in flags:
        return "不通过感应确认物品真伪、归属、身份或历史事实；需要现实证据或专业鉴定。"
    if "expensive_cleansing_pressure" in flags:
        return "不制造付费净化、开光、买课或大师处理压力；优先低成本、可停止的整理。"
    if "repeated_dependency" in flags:
        return "暂停反复感应以寻求确定感；把问题转成现实信息、边界和一个可验证行动。"
    return "可以把物品感应作为象征联想、记忆整理和低风险反思，不作为事实证明、鉴定、隐私读取或专业建议。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "psychometry_request_guard",
        "request_text": text,
        "system": "psychometry_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_psychometry": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "物品感应、触物占卜和 object reading 只作象征联想、记忆整理和低风险反思，不证明物品历史、归属、真伪、灵体或第三方事实。",
            "不替代医疗、安全检测、报警、法律、鉴定、财务或紧急支持。",
            "只处理用户本人拥有或已获授权的物件；不读取第三方隐私，不制造付费净化、开光或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想学习物品感应文化，记录一个获授权物件，还是做低风险象征反思？",
            "物件类型、来源、拥有/授权情况、可见特征、情绪联想和现实问题是什么？",
            "是否涉及失踪犯罪、第三方隐私、灵体事实、专业替代、真伪归属、付费净化或反复依赖？",
        ],
        "next_steps": [
            "record_psychometry_object",
            "lookup_psychometry_symbols",
            "build_psychometry_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_psychometry_consultation", "reframe_to_real_world_support_or_consent"],
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
    parser.add_argument("--text", help="Psychometry or object-reading request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_psychometry"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
