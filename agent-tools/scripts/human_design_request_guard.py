#!/usr/bin/env python3
"""Guard Human Design requests before symbolic consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "human_design_symbolic_consultation": ("人类图", "human design", "类型", "人生角色", "内在权威", "策略", "荐骨", "投射者", "显示者", "生产者", "反映者", "manifestor", "generator", "projector", "reflector"),
    "chart_record": ("图表", "bodygraph", "chart", "type", "authority", "profile", "center", "gates", "channels", "通道", "闸门", "中心"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "体系", "来源"),
}

RISK_KEYWORDS = {
    "birth_data_privacy": ("完整出生资料", "精确出生时间", "帮我查别人", "前任出生", "老板出生", "孩子出生时间", "身份证", "手机号"),
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "替我决定", "全靠人类图"),
    "medical_or_mental_health": ("治病", "治疗", "抑郁", "焦虑", "adhd", "自闭", "创伤", "用药", "诊断"),
    "financial_or_career_guarantee": ("股票", "投资", "贷款", "赌博", "彩票", "保证赚钱", "一定升职", "一定成功", "辞职梭哈"),
    "deterministic_identity": ("天生就是", "注定", "永远", "一定不适合", "不能改变", "命中注定", "人生剧本"),
    "relationship_label_or_discrimination": ("不适合结婚", "天生不合", "筛掉", "克", "低频人", "高频人", "不配", "控制伴侣"),
    "third_party_privacy": ("他真实想法", "她真实想法", "老板真实想法", "前任真实想法", "第三者", "偷窥"),
    "coercion_or_control": ("让他回来", "让她回来", "控制", "操控", "让对方听话", "报复"),
    "paid_pressure": ("必须报课", "高价解读", "买课程", "认证课", "付费疗愈", "必须找老师"),
    "repeated_dependency": ("反复算", "算到满意", "一直看图", "停不下来", "不看不敢决定", "每天问人类图"),
}

SAFE_NEGATED_RISK_PHRASES = (
    "不投资",
    "不赌博",
    "不贷款",
    "不预测",
    "不诊断",
    "不读心",
    "不操控",
    "不报课",
    "不高价解读",
    "不反复算",
    "不替代医生",
    "不替代医疗",
    "不替代心理咨询",
    "只整理现实下一步",
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
    return "human_design_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = remove_safe_negations(text)
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "birth_data_privacy" in flags or "third_party_privacy" in flags:
        return "人类图涉及出生资料和第三方隐私；只处理用户自愿提供的最小化资料或已生成图表，不读取他人真实想法。"
    if "professional_replacement" in flags or "medical_or_mental_health" in flags:
        return "人类图不能替代医疗、法律、安全、心理健康或紧急支持；先处理现实专业支持，再把图表当作反思语言。"
    if "financial_or_career_guarantee" in flags:
        return "不使用人类图决定投资、贷款、赌博、辞职或职业结果保证；可改成现实约束和行动复盘。"
    if "deterministic_identity" in flags or "relationship_label_or_discrimination" in flags:
        return "不把类型、权威或人生角色写成人格定论、关系筛选或命运证明；可改成偏好、沟通和自我观察问题。"
    if "coercion_or_control" in flags:
        return "不使用人类图操控或强迫他人；可改成自己的边界、沟通和可控行动。"
    if "paid_pressure" in flags:
        return "不制造必须报课、认证或高价解读的压力；可优先用免费记录、低成本复盘和现实反馈。"
    if "repeated_dependency" in flags:
        return "暂停反复看图直到满意的依赖模式；先固定问题、复盘时间和现实验证步骤。"
    return "可以把人类图作为象征性自我观察工具，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "human_design_request_guard",
        "request_text": text,
        "system": "human_design_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_human_design": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "人类图类型、策略、权威、人生角色、中心、通道和闸门只作为象征性自我观察语言，不证明人格、命运或结果。",
            "不替代医疗、法律、财务、安全、心理健康、紧急支持、职业决策或当事人沟通。",
            "不用于第三方隐私、关系筛选、身份歧视、操控、确定预言、高风险财务、付费压力或反复依赖。",
            "出生资料按最小化原则处理；优先记录用户已生成图表而非要求精确出生资料。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已有 bodygraph，还是做低风险象征咨询？",
            "资料来源、已知类型、策略、内在权威、人生角色、中心、通道/闸门、关注主题和复盘时间是什么？",
            "请求是否涉及出生资料隐私、专业替代、投资职业保证、关系标签、第三方读心、操控、付费压力或反复依赖？",
        ],
        "next_steps": [
            "record_human_design_chart_context",
            "lookup_human_design_symbols",
            "build_human_design_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_human_design_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Human Design request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_human_design"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
