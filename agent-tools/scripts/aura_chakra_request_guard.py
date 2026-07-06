#!/usr/bin/env python3
"""Guard aura, chakra, and energy-sensation requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "aura_chakra_symbolic_consultation": ("气场", "气场颜色", "脉轮", "七轮", "海底轮", "根轮", "脐轮", "太阳轮", "太阳神经丛", "心轮", "喉轮", "眉心轮", "第三眼", "顶轮", "能量场", "能量感受", "灵气", "reiki", "aura", "chakra", "energy field"),
    "sensation_record": ("胸口", "喉咙", "眉心", "头顶", "发热", "发冷", "麻", "堵", "沉", "轻", "颜色"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用看医生", "不用心理咨询", "不用吃药", "不用报警", "只靠能量", "全靠脉轮"),
    "medical_or_mental_health": ("治病", "治疗", "诊断", "焦虑", "抑郁", "失眠", "幻听", "幻视", "惊恐", "胸痛", "心悸", "呼吸困难", "怀孕", "癌", "药", "手术"),
    "spirit_attack_claim": ("附身", "邪灵", "鬼", "诅咒", "能量攻击", "被下咒", "中邪", "被吸能量", "驱邪", "清除附体"),
    "deterministic_identity_label": ("天生低频", "灵魂有问题", "人格有问题", "命不好", "一定有业障", "必然被污染"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "发财", "暴富"),
    "third_party_privacy_or_coercion": ("看他的气场", "看她的气场", "他心里", "她心里", "真实想法", "控制", "操控", "让他回来", "让她回来"),
    "expensive_healing_pressure": ("必须付费", "必须买课", "必须买疗愈", "天价", "越贵越有效", "贷款买课", "大师远程清理"),
    "repeated_dependency": ("每天测气场", "反复清理", "清到干净", "停不下来", "不敢出门", "一直测脉轮"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "aura_chakra_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_or_mental_health" in flags:
        return "气场/脉轮象征不能替代医疗、心理健康、安全或紧急支持；先处理现实身体和心理风险。"
    if "spirit_attack_claim" in flags:
        return "不确认附身、诅咒、能量攻击或驱邪效果；可改成安全感、身体感受记录和现实支持。"
    if "deterministic_identity_label" in flags:
        return "不把气场或脉轮写成身份、人格、灵魂等级或命运标签；可改成当下状态和可调整的提醒。"
    if "financial_or_gambling" in flags:
        return "不把能量感受用于投资、赌博、彩票或发财判断；财务决策必须回到现实信息。"
    if "third_party_privacy_or_coercion" in flags:
        return "不读取第三方气场、真实想法或帮助操控关系；可改成自己的边界、沟通和选择。"
    if "expensive_healing_pressure" in flags:
        return "不制造付费疗愈、买课或远程清理压力；优先低成本、可停止、可验证的自我照料。"
    if "repeated_dependency" in flags:
        return "暂停反复检测或清理以寻求确定感；先固定次数、记录现实触发因素，并加入 grounding。"
    return "可以把气场/脉轮作为象征语言、身体感受记录和低风险反思，不作为诊断、证明或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "aura_chakra_request_guard",
        "request_text": text,
        "system": "aura_chakra_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_aura_chakra": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "气场、脉轮、灵气和能量感受只作象征语言、文化学习、身体感受记录和低风险反思，不证明事实、不诊断、不保证疗愈。",
            "不替代医疗、心理健康、法律、安全、紧急支持或药物/治疗建议。",
            "不确认附身、诅咒、能量攻击、驱邪效果、第三方真实想法、身份等级、财富信号或付费疗愈必要性。",
        ],
        "clarifying_questions": [
            "用户是想学习气场/脉轮文化、记录当下感受，还是做低风险象征反思？",
            "感受出现的位置、颜色/温度/强度、持续时间、触发场景和现实身体状态是什么？",
            "是否涉及医疗/心理健康症状、灵异恐惧、第三方窥探、付费疗愈压力、财务决策或反复依赖？",
        ],
        "next_steps": [
            "record_aura_chakra_sensation",
            "lookup_aura_chakra_symbols",
            "build_aura_chakra_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_aura_chakra_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Aura, chakra, or energy-sensation request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_aura_chakra"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
