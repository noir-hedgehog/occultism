#!/usr/bin/env python3
"""Guard pendulum divination requests before symbolic consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "pendulum_symbolic_reflection": ("灵摆", "摆锤", "摆 pendulum", "摆动", "顺时针", "逆时针"),
    "yes_no_question": ("是不是", "要不要", "能不能", "会不会", "yes", "no", "是否"),
    "calibration": ("校准", "校验", "怎么问", "如何问", "设置是和否"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "怎么玩"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用看合同", "只听灵摆", "全听灵摆"),
    "deterministic_decision": ("替我决定", "必须照做", "一定会", "必然", "注定", "唯一答案", "最后答案"),
    "financial_claim": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "发财", "收益"),
    "health_or_safety": ("怀孕", "生病", "吃药", "手术", "自杀", "自残", "危险", "报警"),
    "third_party_control": ("让他回来", "让她回来", "操控", "控制", "复合咒", "他心里", "她心里", "老板会不会"),
    "spirit_fear_claim": ("附身", "鬼", "邪灵", "诅咒", "中邪", "被害", "有东西跟着"),
    "repeated_dependency": ("一直问", "反复问", "问到它答应", "每天问几十次", "停不下来"),
    "minor_labeling": ("孩子命运", "宝宝是不是", "小孩以后一定"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "symbolic_yes_no_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    blocking = {
        "professional_replacement",
        "deterministic_decision",
        "financial_claim",
        "health_or_safety",
        "third_party_control",
        "spirit_fear_claim",
        "repeated_dependency",
    }
    return not bool(blocking.intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "health_or_safety" in flags:
        return "灵摆不能替代医疗、法律、财务、安全或紧急判断；先处理现实支持，再把问题改成低风险反思。"
    if "financial_claim" in flags:
        return "不让灵摆决定投资、贷款、彩票或赌博；可改成梳理风险承受度和下一步信息核查。"
    if "third_party_control" in flags:
        return "不使用灵摆操控第三方或判断第三方隐私；可改成自己的边界、沟通选择和可控行动。"
    if "spirit_fear_claim" in flags:
        return "不确认附身、邪灵、诅咒或超自然伤害；可转成安定感、环境安全和可信任支持。"
    if "repeated_dependency" in flags:
        return "暂停反复问同一问题；把问题改成一次性反思，并设置现实决策标准。"
    if "deterministic_decision" in flags:
        return "把唯一答案改写为选项澄清：灵摆只作象征提示，决定仍由现实证据和本人价值排序承担。"
    if "minor_labeling" in flags:
        return "不把灵摆回答贴成未成年人命运标签；可改为照护者的低风险观察和沟通。"
    return "可以把灵摆作为自我反思、偏好澄清和仪式化记录，不作为事实证明或最终决策。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "pendulum_request_guard",
        "request_text": text,
        "system": "pendulum_divination",
        "reading_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_pendulum": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "灵摆只作为象征性自我反思和偏好澄清，不证明事实、不替代专业判断、不做最终决定。",
            "医疗、法律、财务、安全、紧急情况和第三方隐私/操控请求必须暂停灵摆流程。",
            "同一问题反复追问、问到满意为止或依赖灵摆行动时，应转向现实标准和支持资源。",
        ],
        "clarifying_questions": [
            "用户是想学习灵摆流程、记录一次低风险自我反思，还是询问 yes/no？",
            "这个问题是否涉及医疗、法律、财务、安全、第三方隐私或操控？",
            "如果只是偏好澄清，用户愿意把 yes/no 改成可验证的选项标准吗？",
        ],
        "next_steps": [
            "record_pendulum_session",
            "lookup_pendulum_answer_symbols",
            "build_pendulum_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_pendulum_reading", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Pendulum request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_pendulum"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
