#!/usr/bin/env python3
"""Guard bibliomancy and random-book divination requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "bibliomancy_symbolic_consultation": ("书占", "书籍占卜", "随机翻书", "翻书占卜", "书页占卜", "抽一句书", "bibliomancy", "book divination", "random book oracle"),
    "passage_record": ("页码", "段落", "句子", "摘录", "诗句", "关键词", "章节", "quote", "passage"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用咨询", "不用吃药", "只听书", "书替我决定"),
    "medical_or_mental_health": ("治病", "治疗", "诊断", "焦虑", "抑郁", "失眠", "惊恐", "创伤", "药", "医生"),
    "financial_or_legal": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "官司", "起诉", "合同"),
    "deterministic_fate": ("一定会", "必然", "注定", "天意", "神谕命令", "必须照做", "不可违背", "百分百"),
    "third_party_privacy_or_coercion": ("他心里", "她心里", "真实想法", "让他回来", "让她回来", "控制", "操控", "报复"),
    "religious_or_scriptural_authority": ("神说必须", "经文命令", "神谕命令", "不得质疑", "违背会受罚", "天罚"),
    "copyright_or_piracy": ("整本书", "全文", "全章", "发给我原文", "盗版", "扫描版", "pdf全本", "复制整章"),
    "repeated_dependency": ("一直翻", "翻到满意", "反复确认", "停不下来", "每件事都翻书", "不敢做决定"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "bibliomancy_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_or_mental_health" in flags:
        return "书占不能替代医疗、心理健康、法律、安全或紧急支持；可改成读书摘句后的低风险反思。"
    if "financial_or_legal" in flags:
        return "不把书页或随机句子用于投资、彩票、贷款、官司或合同判断。"
    if "deterministic_fate" in flags or "religious_or_scriptural_authority" in flags:
        return "不把书页、经典、经文或随机句子写成不可违背的命令、天意或惩罚。"
    if "third_party_privacy_or_coercion" in flags:
        return "不通过书占读取第三方真实想法，也不帮助操控、报复或强迫关系结果。"
    if "copyright_or_piracy" in flags:
        return "不提供整本书、全章或长段受版权保护文本；可处理用户自提供的短句、关键词或简短摘要。"
    if "repeated_dependency" in flags:
        return "暂停反复翻书以寻求确定感；限制次数，把结果转成一个可验证的小行动。"
    return "可以把书占作为阅读触发的象征反思，不作为事实证明、命令、专业建议或版权文本获取。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "bibliomancy_request_guard",
        "request_text": text,
        "system": "bibliomancy_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_bibliomancy": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "书占、随机翻书和 bibliomancy 只作阅读触发的象征反思，不证明事实、不输出命令、不替代专业支持。",
            "只处理用户提供的短句、关键词、页码和来源说明；不补写整本书、全章或长段受版权保护文本。",
            "不读取第三方真实想法，不把经文/经典/书页写成不可违背的天意、惩罚或决定论。",
        ],
        "clarifying_questions": [
            "用户是想学习书占文化、记录一次翻书结果，还是做低风险象征反思？",
            "书名/来源、页码或抽取方式、用户自提供的短句/关键词、情绪和现实问题是什么？",
            "是否涉及医疗心理健康、法律财务、第三方隐私、经典权威命令、长段版权文本或反复依赖？",
        ],
        "next_steps": [
            "record_bibliomancy_source",
            "lookup_bibliomancy_symbols",
            "build_bibliomancy_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_bibliomancy_consultation", "reframe_to_real_world_support_or_short_user_excerpt"],
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
    parser.add_argument("--text", help="Bibliomancy request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_bibliomancy"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
