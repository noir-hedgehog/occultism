#!/usr/bin/env python3
"""Guard synchronicity, angel-number, and repeating-sign requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "synchronicity_symbolic_consultation": ("同步性", "天使数字", "重复数字", "重复征兆", "宇宙信号", "宇宙讯号", "反复看到", "反复出现", "1111", "11:11", "synchronicity", "angel number", "angel numbers", "repeating sign"),
    "sign_tracking": ("记录", "频率", "同一首歌", "同一个名字", "镜像时间", "重复看到", "stop condition"),
    "routine_reflection": ("作息", "项目", "节奏", "行动", "复盘", "现实锚点"),
}

RISK_KEYWORDS = {
    "dangerous_attention_or_checking": ("开车也要盯", "开车看", "边开车边看", "过马路也看", "盯着车牌", "危险也要看"),
    "financial_or_professional_decision": ("贷款", "股票", "彩票", "赌博", "投资", "币圈", "辞职", "离婚官司", "用药", "手术"),
    "deterministic_command_or_fate": ("宇宙命令", "必须照做", "命中注定", "一定会发生", "不能拒绝", "天意命令"),
    "third_party_mind_reading": ("他真实想法", "她真实想法", "他心里", "她心里", "证明他爱我", "证明她爱我"),
    "mental_health_or_compulsion_signal": ("不看到就害怕", "没看到数字我就很害怕", "停不下来", "每天反复确认", "影响睡眠", "幻听", "幻视", "被监视"),
    "spirit_fact_claim": ("天使命令", "神明命令", "灵体", "亡灵", "外星讯息"),
    "expensive_purchase_pressure": ("付费解码", "天价课程", "大师套餐", "越贵越准"),
}

SAFE_NEGATED_PHRASES = (
    "不当成宇宙命令",
    "不当作宇宙命令",
    "不是宇宙命令",
    "不写成宇宙命令",
    "不当成天使命令",
    "不是天使命令",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "synchronicity_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "dangerous_attention_or_checking" in flags:
        return "不要在开车、过马路或危险环境中寻找数字和征兆；先把注意力放回现实安全。"
    if "financial_or_professional_decision" in flags:
        return "同步性和天使数字不能作为贷款、投资、辞职、医疗、法律或其他专业决策依据。"
    if "deterministic_command_or_fate" in flags or "spirit_fact_claim" in flags:
        return "不把重复数字或征兆写成宇宙、天使、神明或灵体的命令；只能作为个人反思素材。"
    if "third_party_mind_reading" in flags:
        return "不通过同步性证明他人真实想法、爱意、意图或隐私。"
    if "mental_health_or_compulsion_signal" in flags:
        return "如果反复确认数字已经带来恐惧、失眠或停不下来的检查，先暂停解读，做 grounding，并考虑可信任的人或专业支持。"
    if "expensive_purchase_pressure" in flags:
        return "不制造付费解码、天价课程或越贵越准的购买压力；优先用零成本记录和现实行动。"
    return "可以把同步性作为低风险记录、情绪整理和可控行动反思，不写成命令、预言或专业建议。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "synchronicity_request_guard",
        "request_text": text,
        "system": "synchronicity_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_synchronicity": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "同步性/天使数字只作个人象征记录、情绪整理和低风险行动反思。",
            "不把重复数字、歌曲、名字或征兆写成宇宙命令、未来保证、天使/灵体事实或第三方读心。",
            "不替代财务、职业、医疗、法律、心理健康或现实安全判断；不在开车、过马路等危险场景寻找征兆。",
            "不制造高价付费压力，不强化反复确认和依赖。",
        ],
        "clarifying_questions": [
            "用户是想做文化学习、重复征兆记录，还是低风险行动反思？",
            "重复符号、出现频率、场景、情绪、现实锚点、可控行动和停止条件是什么？",
            "是否涉及危险寻找、宇宙命令、专业替代、第三方读心、灵体事实、高价付费或反复依赖？",
        ],
        "next_steps": [
            "record_synchronicity_event",
            "lookup_synchronicity_symbols",
            "build_synchronicity_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_synchronicity_consultation", "reframe_to_grounded_safety_or_professional_support"],
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
    parser.add_argument("--text", help="Synchronicity request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_synchronicity"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
