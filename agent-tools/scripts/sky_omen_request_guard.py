#!/usr/bin/env python3
"""Guard sky-omen, cloud, rainbow, halo, and weather-sign requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "sky_omen_symbolic_consultation": ("天象征兆", "云占", "看云", "云形", "彩虹", "彩虹征兆", "日晕", "月晕", "雷电征兆", "风雨预兆", "sky omen", "cloud omen", "nephomancy", "weather omen"),
    "observation_record": ("云", "彩虹", "日晕", "月晕", "霞光", "闪电", "雷", "风", "雨", "雾", "天空", "cloud", "rainbow", "halo", "lightning", "thunder"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "disaster_prediction_or_panic": ("地震", "灾难", "灾祸", "末日", "大灾", "天谴", "天罚", "死亡预兆", "不祥"),
    "weather_safety_replacement": ("不用天气预报", "不用天气预警", "不用预警", "不用撤离", "不用避雷", "不用报警", "只看天象"),
    "medical_or_professional": ("治病", "治疗", "诊断", "焦虑", "抑郁", "失眠", "医生", "药", "律师"),
    "financial_or_legal": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "官司", "起诉"),
    "third_party_privacy_or_coercion": ("他心里", "她心里", "真实想法", "让他回来", "让她回来", "控制", "操控", "报复"),
    "spirit_fact_claim": ("神明显灵", "天神命令", "亡灵", "鬼", "邪灵", "诅咒", "被下咒"),
    "dangerous_exposure": ("暴雨里站", "雷雨里站", "去楼顶", "追闪电", "台风里出门", "洪水边", "山洪", "海边等台风"),
    "repeated_dependency": ("每天看云", "反复确认", "看到云就害怕", "停不下来", "每件事都看天象"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "sky_omen_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "weather_safety_replacement" in flags or "dangerous_exposure" in flags:
        return "天象/云形征兆不能替代天气预报、预警、撤离、避雷或现实安全措施；先以官方天气和安全指引为准。"
    if "disaster_prediction_or_panic" in flags:
        return "不把云、彩虹、日月晕或雷电写成灾难、死亡、天罚或末日预言；可改成情绪安抚和现实准备。"
    if "medical_or_professional" in flags:
        return "天象象征不能替代医疗、心理健康、法律或其他专业支持。"
    if "financial_or_legal" in flags:
        return "不把天象征兆用于投资、彩票、贷款、官司或法律判断。"
    if "third_party_privacy_or_coercion" in flags:
        return "不通过天象读取第三方真实想法，也不帮助操控、报复或强迫关系结果。"
    if "spirit_fact_claim" in flags:
        return "不确认神明、亡灵、邪灵、诅咒或天命事实；可改成文化象征和现实反思。"
    if "repeated_dependency" in flags:
        return "暂停反复看天象以寻求确定感；把观察转成一次记录、一个现实锚点和停止条件。"
    return "可以把天象、云形、彩虹、日月晕和风雨雷电作为文化象征与低风险观察反思，不作为天气安全、灾祸预言或专业建议。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "sky_omen_request_guard",
        "request_text": text,
        "system": "sky_omen_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_sky_omen": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "天象/云形征兆只作文化学习、观察记录和低风险象征反思，不预测灾祸、不替代天气预报或安全预警。",
            "不替代医疗、法律、财务、安全、心理健康、应急撤离或现实专业支持。",
            "不读取第三方真实想法，不确认神明/灵体/诅咒事实，不鼓励危险天气暴露或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想学习天象民俗、记录一次天空观察，还是做低风险象征反思？",
            "观察对象、地点、时间、天气安全背景、用户第一联想和现实锚点是什么？",
            "是否涉及灾祸恐吓、天气安全替代、危险暴露、专业替代、第三方隐私、灵体事实或反复依赖？",
        ],
        "next_steps": [
            "record_sky_omen_observation",
            "lookup_sky_omen_symbols",
            "build_sky_omen_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_sky_omen_consultation", "reframe_to_weather_safety_or_real_world_support"],
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
    parser.add_argument("--text", help="Sky omen request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_sky_omen"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
