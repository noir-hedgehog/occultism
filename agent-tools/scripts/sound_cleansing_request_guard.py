#!/usr/bin/env python3
"""Guard sound-cleansing, bells, bowls, and chanting requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "sound_cleansing_symbolic_consultation": ("声响净化", "声音净化", "铃铛净化", "铃铛清理", "铃钵", "颂钵", "音叉", "诵念", "念咒", "mantra", "chanting", "singing bowl", "sound cleansing"),
    "space_reset": ("空间", "房间", "办公室", "搬家", "睡前", "复位", "收心", "安定"),
    "low_risk_practice": ("低风险", "无火", "不驱邪保证", "不替代医生", "不扰民", "短时"),
}

RISK_KEYWORDS = {
    "medical_or_mental_health_replacement": ("不用医生", "不用心理咨询", "不用吃药", "治疗失眠", "治抑郁", "治病", "替代治疗", "赶走幻听"),
    "coercive_or_exorcism_claim": ("驱走附身", "赶走附身", "确认有鬼", "把鬼赶出去", "强行净化别人", "让别人听到崩溃", "惩罚邻居"),
    "unsafe_sound_exposure": ("最大音量", "贴耳朵敲", "通宵敲", "让耳朵疼", "耳鸣也继续", "婴儿旁边敲", "宠物旁边大声敲"),
    "legal_or_neighbor_conflict": ("半夜敲", "扰民也要", "无视邻居", "物业不用管", "报警也不管"),
    "guaranteed_effect": ("一定净化干净", "保证驱邪", "保证睡着", "立刻转运", "百分百清除负能量"),
    "expensive_ritual_pressure": ("高价铃钵", "必须买高价铃钵", "越贵越灵", "大师开声", "声音净化套餐", "贷款买钵"),
    "repeated_dependency": ("每天敲很多小时", "停不下来", "不敲就害怕", "反复净化", "一焦虑就敲"),
}

SAFE_NEGATED_PHRASES = (
    "不替代医生",
    "不替代心理咨询",
    "不治疗失眠",
    "不保证驱邪",
    "不保证睡着",
    "不扰民",
    "不用大音量",
    "不买高价",
    "不反复净化",
    "不反复敲",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "sound_cleansing_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "medical_or_mental_health_replacement" in flags:
        return "不把声响净化、铃钵、音叉或诵念替代医疗、心理、睡眠或精神健康支持。"
    if "coercive_or_exorcism_claim" in flags:
        return "不确认鬼神附身或提供强制驱灵、操控他人、惩罚他人的声响做法。"
    if "unsafe_sound_exposure" in flags:
        return "不提供贴耳、超大音量、通宵、耳痛仍继续或靠近婴儿/宠物的声响步骤。"
    if "legal_or_neighbor_conflict" in flags:
        return "声响练习必须尊重安静时段、邻里、物业和公共空间规则。"
    if "guaranteed_effect" in flags:
        return "不承诺净化干净、驱邪、入睡、转运或清除负能量；只能做空间复位和注意力提示。"
    if "expensive_ritual_pressure" in flags:
        return "不制造高价铃钵、套餐、大师开声或贷款购买压力；优先已有物件和低成本替代。"
    if "repeated_dependency" in flags:
        return "如果声响练习已经加重焦虑，先设置时长、频率和停止条件。"
    return "可以把声响净化改写为短时、低音量、尊重邻里和身体感受的空间复位流程。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "sound_cleansing_request_guard",
        "request_text": text,
        "system": "sound_cleansing_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_sound_cleansing": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "声响净化、铃钵、铃铛、音叉和诵念只作文化象征、空间复位、注意力提示和低风险练习。",
            "不承诺驱邪、清除负能量、治疗、入睡、转运或灵验结果。",
            "不提供超大音量、贴耳、通宵、耳痛仍继续、靠近婴儿/宠物或扰民做法。",
            "不替代医疗、心理、睡眠、法律、报警或其他专业支持；不制造高价器具或课程压力。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、整理空间复位流程，还是记录已有铃钵/铃铛/诵念体验？",
            "空间、时段、声音工具、音量、时长、身体感受、邻里/宠物/婴儿边界、复盘时间和停止条件是什么？",
            "是否涉及医疗/心理替代、强制驱灵、超大音量、扰民、高价购买、效果保证或反复依赖？",
        ],
        "next_steps": [
            "record_sound_cleansing_context",
            "lookup_sound_cleansing_symbols",
            "build_sound_cleansing_practice_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_sound_cleansing_consultation", "reframe_to_low_risk_space_reset_or_professional_support"],
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
    parser.add_argument("--text", help="Sound-cleansing request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_sound_cleansing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
