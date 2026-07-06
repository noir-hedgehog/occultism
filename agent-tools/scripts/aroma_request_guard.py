#!/usr/bin/env python3
"""Guard aroma, essential oil, and scent symbolism requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "aroma_symbolic_consultation": ("芳香", "香薰", "精油", "气味", "嗅觉", "香氛", "香气", "aromatherapy", "essential oil", "scent", "diffuser"),
    "scent_record": ("闻到", "扩香", "喷雾", "香水", "线香", "香包", "味道", "香调", "配方", "blend"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来源", "象征"),
}

RISK_KEYWORDS = {
    "medical_or_mental_health_claim": ("治病", "治疗", "疗愈疾病", "抗癌", "消炎", "抗病毒", "抑郁", "焦虑", "失眠", "adhd", "诊断", "用药", "停药"),
    "ingestion_or_unsafe_application": ("喝精油", "内服", "滴嘴里", "入口", "直接涂", "原液涂", "滴眼睛", "滴耳朵", "私处", "伤口"),
    "pregnancy_baby_pet_allergy": ("孕妇", "怀孕", "备孕", "婴儿", "宝宝", "儿童", "猫", "狗", "宠物", "哮喘", "过敏", "癫痫"),
    "fire_or_diffuser_safety": ("整夜点", "无人看管", "密闭房间", "靠近火", "明火", "酒精灯", "一直扩香", "不通风"),
    "professional_replacement": ("不用医生", "不用看医生", "不用心理咨询", "不用报警", "不用吃药", "全靠精油"),
    "spirit_fear_or_exorcism": ("驱邪", "除灵", "赶鬼", "附身", "诅咒", "中邪", "清除邪气", "保证净化"),
    "financial_or_outcome_guarantee": ("保证开运", "保证招财", "保证复合", "保证睡着", "一定有效", "一定转运"),
    "third_party_or_coercion": ("让他爱我", "让她回来", "控制伴侣", "操控", "报复", "读取他真实想法", "读取她真实想法"),
    "purchase_pressure": ("必须买", "高价精油", "天价套装", "会员囤货", "贷款买", "越贵越灵", "代理课程"),
    "repeated_dependency": ("每天闻到满意", "一直扩香", "停不下来", "不闻不敢睡", "反复调到满意", "每天问精油"),
}

SAFE_NEGATED_RISK_PHRASES = (
    "不治疗",
    "不诊断",
    "不替代医生",
    "不替代医疗",
    "不替代心理咨询",
    "不内服",
    "不入口",
    "不直接涂",
    "不碰宠物",
    "不碰孕妇",
    "不用明火",
    "不驱邪",
    "不保证开运",
    "不保证招财",
    "不操控",
    "不高价购买",
    "不囤货",
    "不反复闻",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def remove_safe_negations(text: str) -> str:
    cleaned = text
    for phrase in SAFE_NEGATED_RISK_PHRASES:
        cleaned = cleaned.replace(phrase, "")
    return cleaned


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "aroma_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = remove_safe_negations(text)
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "medical_or_mental_health_claim" in flags or "professional_replacement" in flags:
        return "芳香/精油不能替代医疗、心理健康、安全或紧急支持；可改成气味偏好、环境线索和低风险自我照料提醒。"
    if "ingestion_or_unsafe_application" in flags:
        return "不提供内服、入口、原液直接涂抹、眼耳伤口等危险用法；只讨论安全边界和非接触式象征提醒。"
    if "pregnancy_baby_pet_allergy" in flags:
        return "孕婴儿童、宠物、过敏、哮喘或癫痫等场景需要先遵循专业安全建议；不做具体精油适用判断。"
    if "fire_or_diffuser_safety" in flags:
        return "不建议无人看管、密闭、整夜、靠近火源或不通风的使用方式；优先停止、通风和现实安全。"
    if "spirit_fear_or_exorcism" in flags:
        return "不把气味写成驱邪、除灵或保证净化；可改成空间整理、安定感和象征性收尾。"
    if "financial_or_outcome_guarantee" in flags:
        return "不承诺开运、招财、复合、睡眠或任何结果；可改成可观察、可撤回的小行动。"
    if "third_party_or_coercion" in flags:
        return "不使用气味操控他人、读心、复合或报复；可改成自己的边界和沟通准备。"
    if "purchase_pressure" in flags:
        return "不制造高价套装、会员囤货或课程压力；优先已有物件、低成本替代和不购买选项。"
    if "repeated_dependency" in flags:
        return "暂停反复调配或一直扩香直到安心的依赖模式；先设定时长、停止条件和现实复盘。"
    return "可以把芳香、精油和气味作为文化象征、环境提醒和低风险反思工具，不作为治疗、净化保证或结果承诺。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "aroma_request_guard",
        "request_text": text,
        "system": "aroma_scent_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_aroma": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "芳香、精油、香薰、香氛和气味只作为文化象征、环境提醒和低风险反思，不证明疗效、净化、开运或关系结果。",
            "不提供内服、入口、原液直接涂抹、眼耳伤口、孕婴宠物过敏等具体安全适用判断。",
            "不替代医疗、心理健康、法律、安全、消防、宠物兽医或紧急支持。",
            "不制造高价购买、会员囤货、代理课程、反复依赖、驱邪恐惧、第三方操控或结果保证。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已有气味体验，还是做低风险象征咨询？",
            "气味/物件来源、使用方式、空间通风、时长、是否接触皮肤、是否有孕婴宠物过敏等现实安全背景是什么？",
            "关注主题、预算、已有物件、停止条件和是否涉及医疗替代、驱邪恐惧、操控、结果保证或购买压力是什么？",
        ],
        "next_steps": [
            "record_aroma_context",
            "lookup_aroma_symbols",
            "build_aroma_practice_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_aroma_consultation", "reframe_to_safety_or_professional_support"],
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
    parser.add_argument("--text", help="Aroma, essential oil, or scent request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_aroma"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
