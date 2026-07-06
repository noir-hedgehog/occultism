#!/usr/bin/env python3
"""Guard synastry and compatibility-style astrology requests before interpretation."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    label: str
    keywords: tuple[str, ...]


INTENT_RULES = {
    "relationship_reflection": ("关系", "相处", "互动", "沟通", "边界", "伴侣", "合作"),
    "compatibility_claim": ("合不合", "配不配", "绝配", "命中注定", "正缘", "灵魂伴侣", "分手", "复合"),
    "third_party_inference": ("他是不是", "她是不是", "对方想", "前任", "暗恋", "爱不爱", "真实想法"),
    "chart_comparison": ("合盘", "比较盘", "组合盘", "synastry", "composite", "金星", "火星", "七宫"),
    "cultural_learning": ("讲讲", "科普", "文化", "概念", "什么意思", "怎么理解"),
}

RISK_RULES = (
    Rule("deterministic_compatibility", ("绝配", "命中注定", "正缘", "孽缘", "一定会", "注定", "必分", "必复合")),
    Rule("third_party_privacy", ("前任", "他是不是", "她是不是", "对方想", "爱不爱我", "暗恋对象")),
    Rule("coercion", ("让他爱我", "让她爱我", "控制他", "控制她", "挽回术", "操控")),
    Rule("professional_or_crisis", ("停药", "怀孕", "自杀", "自残", "家暴", "跟踪", "律师", "贷款", "股票")),
)


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_RULES.items():
        if contains_any(text, keywords):
            return intent
    return "relationship_reflection"


def detect_risks(text: str) -> list[str]:
    return [rule.label for rule in RISK_RULES if contains_any(text, rule.keywords)]


def consent_state(payload: dict[str, object]) -> str:
    if payload.get("all_subjects_self_or_consented") is True:
        return "all_consented"
    if payload.get("other_subject_consent") is True:
        return "other_consented"
    if payload.get("relationship_is_self_reflection_only") is True:
        return "self_reflection_only"
    return "missing_or_unknown"


def can_continue(intent: str, risks: list[str], consent: str) -> bool:
    if "professional_or_crisis" in risks or "coercion" in risks:
        return False
    if "deterministic_compatibility" in risks:
        return False
    if "third_party_privacy" in risks and consent not in {"all_consented", "other_consented", "self_reflection_only"}:
        return False
    if intent in {"third_party_inference", "compatibility_claim"} and consent == "missing_or_unknown":
        return False
    return True


def reframe(intent: str, risks: list[str], consent: str) -> str:
    if "professional_or_crisis" in risks:
        return "先暂停占星合盘，把问题改为：我需要哪些现实安全、专业支持或可信任帮助？"
    if "coercion" in risks:
        return "不做操控或强迫复合；可改为：我如何守住边界，并以尊重方式表达需要？"
    if "deterministic_compatibility" in risks:
        return "不判断绝配、正缘或注定结局；可改为：这段关系有哪些互动模式、需求差异和可沟通边界？"
    if intent == "third_party_inference" and consent == "missing_or_unknown":
        return "缺少对方同意时，不分析对方真实想法或命盘；可改为：我在这段互动里能观察到什么事实和自己的需要？"
    if intent == "compatibility_claim":
        return "把合不合改写为：双方互动里有哪些资源、张力、边界和低风险沟通动作？"
    if intent == "chart_comparison":
        return "把合盘字段作为象征比较，只讨论互动模式，不证明关系命运。"
    if intent == "cultural_learning":
        return "可以做匿名文化解释：合盘/比较盘通常如何被用作关系象征语言？"
    return "把关系占星限定为自我反思、互动模式和低风险沟通建议。"


def next_steps(allowed: bool, consent: str) -> list[str]:
    if not allowed:
        steps = ["pause_compatibility_interpretation", "reframe_to_self_reflection_or_consent_request"]
        if consent == "missing_or_unknown":
            steps.append("ask_for_subject_consent_or_remove_third_party_chart_data")
        return steps
    return [
        "record_chart_source_and_subject_consent",
        "use_astrology_chart_record_for_provided_fields",
        "lookup_relevant_symbols_with_astrology_symbol_lookup",
        "lint_final_output_with_mystic_output_lint",
    ]


def guard(payload: dict[str, object]) -> dict[str, object]:
    text = str(payload.get("request_text", payload.get("question_text", ""))).strip()
    if not text:
        raise ValueError("request_text or question_text is required")

    intent = detect_intent(text)
    risks = detect_risks(text)
    consent = consent_state(payload)
    allowed = can_continue(intent, risks, consent)
    warnings: list[str] = []
    if "deterministic_compatibility" in risks:
        warnings.append("合盘不能用于绝配、正缘、注定分合或关系结局保证。")
    if "third_party_privacy" in risks and consent == "missing_or_unknown":
        warnings.append("缺少对方同意时，不分析第三方命盘、真实想法或隐私。")
    if "coercion" in risks:
        warnings.append("不得使用占星建议操控、强迫复合或侵犯他人边界。")
    if "professional_or_crisis" in risks:
        warnings.append("危机或专业问题必须先转向现实安全和合格专业支持。")

    return {
        "system": "western_astrology",
        "request_text": text,
        "relationship_intent": intent,
        "consent_state": consent,
        "risk_flags": risks,
        "can_continue_compatibility": allowed,
        "reframed_question": reframe(intent, risks, consent),
        "warnings": warnings,
        "limits": [
            "合盘/比较盘只能作为关系互动的象征反思，不证明绝配、正缘、分手或复合结局。",
            "缺少当事人同意时，不分析第三方星盘、真实想法、性格标签或隐私。",
            "不得把占星用于控制、跟踪、报复、强迫复合或替代专业建议。",
        ],
        "next_steps": next_steps(allowed, consent),
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"request_text": raw}
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
    parser.add_argument("--text", help="Compatibility or synastry request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to text or JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
