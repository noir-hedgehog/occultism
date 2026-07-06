#!/usr/bin/env python3
"""Guard sleep-paralysis, nightmare-spirit-fear, and night-terror requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "sleep_paralysis_symbolic_consultation": ("鬼压床", "压床", "睡眠瘫痪", "睡瘫", "sleep paralysis", "梦魇", "梦魔", "night terror", "nightmare spirit"),
    "night_fear_grounding": ("半夜惊醒", "床边有人", "睡前害怕", "夜里害怕", "不敢睡", "醒来动不了", "胸口压着"),
    "symbolic_sleep_reflection": ("梦后复位", "睡前安定", "grounding", "安定流程", "睡眠记录"),
}

RISK_KEYWORDS = {
    "medical_or_breathing_signal": ("呼吸困难", "喘不过气", "胸痛", "心悸", "晕倒", "抽搐", "癫痫", "受伤", "窒息"),
    "severe_sleep_impairment": ("连续失眠", "很多天没睡", "不敢睡", "整晚睡不着", "严重影响白天", "无法工作", "无法上学"),
    "hallucination_or_reality_confusion": ("白天也看见", "白天也听见", "幻听", "幻视", "被控制", "它命令我", "现实里跟着我"),
    "self_harm_or_violence": ("自杀", "自残", "伤害自己", "伤害别人", "杀了", "活不下去"),
    "dangerous_ritual": ("放血", "血祭", "烧炭", "密闭烧", "通宵点香", "喝符水", "喝香灰", "刀", "驱鬼到天亮", "不睡觉等它来"),
    "professional_replacement": ("不用医生", "不用医院", "不用心理咨询", "不用报警", "不看医生", "不去医院", "治疗", "诊断", "用药"),
    "spirit_fact_or_possession_claim": ("确定有鬼", "确定附身", "被鬼控制", "灵体压我", "邪灵压我", "邪灵上床", "恶魔附体", "被下咒"),
    "expensive_ritual_pressure": ("天价法事", "必须请大师", "必须买", "越贵越灵", "开光套餐", "驱鬼套餐"),
    "repeated_checking_dependency": ("每天确认", "反复测试", "停不下来", "不做仪式就害怕", "每晚都问", "一直查征兆"),
}

SAFE_NEGATED_PHRASES = (
    "不确认有鬼",
    "不做危险仪式",
    "不买贵法事",
    "不替代医生",
    "不替代心理咨询",
    "不驱鬼",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "sleep_paralysis_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "self_harm_or_violence" in flags:
        return "若有自伤、伤人或活不下去的念头，先停止玄学解释，立即联系当地紧急服务、危机热线或可信任的人。"
    if "medical_or_breathing_signal" in flags:
        return "呼吸困难、胸痛、晕倒、抽搐或受伤等信号需要优先医疗评估；不能用玄学解释替代。"
    if "severe_sleep_impairment" in flags:
        return "连续失眠、不敢睡或白天功能受损时，先做现实睡眠支持和专业求助，而不是继续解释灵异原因。"
    if "hallucination_or_reality_confusion" in flags:
        return "若白天也出现幻听幻视、被控制感或现实混淆，优先联系专业支持和可信任的人。"
    if "dangerous_ritual" in flags:
        return "不提供放血、密闭燃烧、通宵点香、摄入符水香灰或睡眠剥夺等危险做法。"
    if "professional_replacement" in flags:
        return "鬼压床/梦魇咨询不能替代医疗、心理健康、睡眠或安全支持。"
    if "spirit_fact_or_possession_claim" in flags:
        return "不确认鬼、邪灵、附身、下咒或灵体压迫事实；可改成睡眠体验记录、安定和现实安全检查。"
    if "expensive_ritual_pressure" in flags:
        return "不制造高价法事、驱鬼套餐或购买压力；优先低成本、可撤回的睡前安定和支持连接。"
    if "repeated_checking_dependency" in flags:
        return "如果反复确认灵异原因已经加重恐惧，先暂停查询和仪式循环，改做固定睡眠记录和复盘时间。"
    return "可以把鬼压床/梦魇/夜间恐惧作为睡眠体验记录、身体安定、空间现实检查和象征反思来处理。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "sleep_paralysis_request_guard",
        "request_text": text,
        "system": "sleep_paralysis_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_sleep_paralysis": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "鬼压床、梦魇和夜间灵异恐惧只作睡眠体验记录、身体安定、现实安全检查和象征反思。",
            "不确认鬼、邪灵、附身、下咒、灵体压迫、灾祸预告或第三方影响。",
            "不提供危险仪式、睡眠剥夺、摄入符水香灰、专业替代或高价法事。",
            "严重睡眠受损、呼吸/胸痛/抽搐、幻听幻视、自伤伤人或现实功能受损时优先现实支持。",
        ],
        "clarifying_questions": [
            "这是想学习鬼压床/梦魇文化，记录一次睡眠体验，还是做睡前安定和现实安全检查？",
            "发生时间、醒来状态、身体感觉、房间环境、近期压力、睡眠时长、白天影响和复盘时间是什么？",
            "是否涉及呼吸胸痛/抽搐/受伤、连续失眠、幻听幻视、自伤伤人、危险仪式、专业替代、高价法事或反复确认？",
        ],
        "next_steps": [
            "record_sleep_paralysis_context",
            "lookup_sleep_paralysis_symbols",
            "build_sleep_paralysis_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_sleep_paralysis_consultation", "reframe_to_sleep_safety_grounding_or_professional_support"],
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
    parser.add_argument("--text", help="Sleep paralysis or night fear request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_sleep_paralysis"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
