#!/usr/bin/env python3
"""Guard crystal-ball, mirror, and water-scrying requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "scrying_symbolic_consultation": ("水晶球占卜", "镜占", "黑镜占卜", "水占", "凝视占卜", "水晶球", "黑镜", "镜面凝视", "水面凝视", "scrying", "crystal ball reading", "mirror scrying", "water scrying"),
    "observation_record": ("看到影像", "看见形状", "倒影", "雾面", "水纹", "画面", "凝视"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来历", "传统"),
}

RISK_KEYWORDS = {
    "unsafe_trance_or_staring": ("一直盯", "盯到出神", "通宵看", "通宵盯", "不睡觉看", "直到看到", "盯到头晕", "盯到幻觉", "强行入神"),
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "只看水晶球", "全靠黑镜"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "下注", "投资", "币圈", "贷款", "发财", "梭哈", "收益"),
    "medical_or_mental_health": ("治病", "治疗", "怀孕", "癌", "手术", "失眠", "焦虑", "抑郁", "幻听", "幻视", "精神病"),
    "deterministic_fate": ("一定会", "必然", "注定", "百分百", "保证", "必成", "必失败", "必分手"),
    "spirit_fear_claim": ("有鬼", "中邪", "附身", "被诅咒", "邪灵", "看到灵体", "通灵", "召灵", "驱鬼", "驱邪保证"),
    "third_party_privacy": ("他真实想法", "她真实想法", "老板真实想法", "前任现在", "第三者", "偷窥"),
    "coercion_or_control": ("让他回来", "让她回来", "控制", "操控", "复合咒", "报复", "诅咒"),
    "identity_or_body_label": ("长得命苦", "脸上有灾", "这个人有邪气", "看照片判断人品"),
    "repeated_dependency": ("反复看", "看到满意", "一直看", "停不下来", "不看不敢决定"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "scrying_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "unsafe_trance_or_staring" in flags:
        return "不引导长时间凝视、强行入神、睡眠剥夺或追求幻觉；可改为短时记录已有视觉联想，并先休息和检查身体感受。"
    if "professional_replacement" in flags or "medical_or_mental_health" in flags:
        return "水晶球/镜面/水面凝视象征不能替代医疗、心理健康、法律、安全或紧急支持；先处理现实专业支持。"
    if "financial_or_gambling" in flags:
        return "不使用凝视影像决定投资、贷款、彩票、赌博或高风险财务行为；可改成风险清单和现实约束。"
    if "spirit_fear_claim" in flags:
        return "不确认鬼神、灵体、诅咒、通灵或驱邪效果；可转为安抚、空间整理和现实安全检查。"
    if "deterministic_fate" in flags:
        return "不把影像、倒影或水纹写成确定预言或命运证明；可改成可能性、现实证据和低风险下一步。"
    if "third_party_privacy" in flags or "coercion_or_control" in flags:
        return "不使用凝视窥探、操控或强迫他人；可改成自己的边界、沟通和可控行动。"
    if "identity_or_body_label" in flags:
        return "不从照片、倒影或外貌联想推断人格、命运、邪气或身份标签；可改成自我感受和低风险表达。"
    if "repeated_dependency" in flags:
        return "暂停反复凝视直到满意的依赖模式；先固定问题、观察来源和现实验证步骤。"
    return "可以把短时、已记录的水晶球/镜面/水面观察作为象征性反思，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "scrying_request_guard",
        "request_text": text,
        "system": "scrying_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_scrying": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "只处理短时、已记录的观察或文化学习；不引导长时间凝视、强行入神、睡眠剥夺或追求幻觉。",
            "水晶球、镜面、水面影像只作为象征反思，不证明事实、不保证结果、不确认鬼神、灵体、通灵或驱邪效果。",
            "不替代医疗、法律、财务、安全、心理健康或紧急支持。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已有观察，还是做低风险象征咨询？",
            "观察是否为短时、已结束的视觉联想；是否出现头晕、恐惧、失眠、幻觉或停不下来的凝视？",
            "请求是否涉及财务赌博、专业替代、第三方隐私、操控、鬼神恐惧、身份标签或反复依赖？",
        ],
        "next_steps": [
            "record_scrying_observation",
            "lookup_scrying_symbols",
            "build_scrying_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_scrying_consultation", "reframe_to_grounding_or_real_world_support"],
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
    parser.add_argument("--text", help="Scrying request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_scrying"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
