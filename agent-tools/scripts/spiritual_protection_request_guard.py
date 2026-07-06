#!/usr/bin/env python3
"""Guard evil-eye, energy-protection, and cord-cutting requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "spiritual_protection_symbolic_consultation": ("恶眼", "evil eye", "能量防护", "灵性防护", "防护罩", "保护罩", "防小人", "负能量", "energy protection", "spiritual protection"),
    "cord_cutting_boundary": ("能量断联", "切断能量", "断开连接", "cord cutting", "energy cord", "cut cord"),
    "boundary_reflection": ("边界", "提醒物", "低风险", "不诅咒", "不报复", "grounding"),
}

RISK_KEYWORDS = {
    "paranoia_or_persecution_claim": ("确定他害我", "确定她害我", "被监视", "被下咒", "有人害我", "被投毒", "被控制", "所有人针对我"),
    "retaliation_or_curse": ("诅咒", "报复", "反噬他", "让他倒霉", "惩罚他", "让她生病", "攻击对方"),
    "dangerous_ritual": ("血祭", "放血", "割手", "烧照片", "烧头发", "烧衣服", "半夜去他家", "埋东西", "喝符水"),
    "professional_or_safety_replacement": ("不用医生", "不用报警", "不用律师", "不去医院", "跟踪他", "偷看手机", "监控他", "拆摄像头", "治疗", "诊断", "用药"),
    "third_party_privacy_or_blame": ("是谁害我", "谁下的", "查出小人", "同事给我下", "前任给我下", "邻居害我"),
    "coercive_relationship_control": ("让前任回来", "切断他和她", "拆散他们", "让他离不开我", "控制他"),
    "expensive_purchase_pressure": ("天价防护", "大师套餐", "防护阵", "必须买", "越贵越灵", "付费开盾"),
    "repeated_dependency": ("每天做断联", "反复清理", "停不下来", "不做就害怕", "影响睡眠", "不敢出门"),
}

SAFE_NEGATED_PHRASES = (
    "不诅咒",
    "不报复",
    "不攻击",
    "不确认谁害我",
    "不找小人",
    "不买贵物",
    "不做危险仪式",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "spiritual_protection_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "paranoia_or_persecution_claim" in flags:
        return "不确认被害、被监视、被下咒或他人迫害事实；若有现实安全风险或强烈恐惧，优先联系可信任的人、当地紧急服务或专业支持。"
    if "retaliation_or_curse" in flags:
        return "不提供诅咒、反噬、报复或攻击他人的做法；可改成边界整理、情绪安放和现实安全计划。"
    if "dangerous_ritual" in flags:
        return "不提供放血、焚烧、埋物、符水或夜间靠近他人住所等危险步骤。"
    if "professional_or_safety_replacement" in flags:
        return "能量防护不能替代医疗、法律、报警、安全规划或心理健康支持。"
    if "third_party_privacy_or_blame" in flags:
        return "不通过恶眼或能量感受指认谁害你、谁下咒、谁是小人或读取第三方隐私。"
    if "coercive_relationship_control" in flags:
        return "能量断联只用于自我边界整理，不用于操控、拆散或控制他人关系。"
    if "expensive_purchase_pressure" in flags:
        return "不制造高价防护、付费开盾或大师套餐压力；优先低成本、可逆的提醒物和现实边界。"
    if "repeated_dependency" in flags:
        return "如果反复清理或断联已经带来恐惧、失眠或不敢出门，先暂停仪式化确认，做 grounding 并考虑支持资源。"
    return "可以把恶眼/能量防护/断联作为低风险边界整理、提醒物使用、情绪安放和现实安全检查。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "spiritual_protection_request_guard",
        "request_text": text,
        "system": "spiritual_protection_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_spiritual_protection": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "恶眼/能量防护/能量断联只作象征性边界整理、提醒物使用、情绪安放和现实安全检查。",
            "不确认谁害你、谁下咒、灵体事实、被监视事实或第三方隐私。",
            "不提供诅咒报复、危险仪式、跟踪监控、专业替代或关系操控。",
            "不制造高价购买压力，不强化反复清理和恐惧依赖。",
        ],
        "clarifying_questions": [
            "用户是想学习恶眼/防护文化、整理个人边界，还是做低风险断联反思？",
            "触发场景、身体/情绪感受、现实安全背景、可控边界动作、提醒物、复盘时间和停止条件是什么？",
            "是否涉及指认加害者、诅咒报复、危险仪式、专业替代、关系操控、高价购买或反复依赖？",
        ],
        "next_steps": [
            "record_spiritual_protection_context",
            "lookup_spiritual_protection_symbols",
            "build_spiritual_protection_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_spiritual_protection_consultation", "reframe_to_boundary_safety_or_professional_support"],
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
    parser.add_argument("--text", help="Spiritual protection request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_spiritual_protection"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
