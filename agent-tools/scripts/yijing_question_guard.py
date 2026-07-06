#!/usr/bin/env python3
"""Guard and reframe I Ching / Yijing divination questions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    label: str
    keywords: tuple[str, ...]


DOMAIN_RULES = {
    "relationship": ("关系", "感情", "复合", "分手", "他", "她", "伴侣", "暧昧"),
    "career": ("工作", "事业", "跳槽", "辞职", "offer", "项目", "面试"),
    "decision": ("选择", "选哪个", "要不要", "是否", "该不该", "方案", "搬家"),
    "timing": ("什么时候", "何时", "多久", "哪天", "日期"),
    "self_cultivation": ("修身", "状态", "心态", "如何调整", "下一步"),
    "health": ("病", "医生", "用药", "手术", "怀孕", "诊断"),
    "finance": ("股票", "彩票", "赌博", "投资", "贷款", "梭哈", "币"),
    "legal": ("律师", "起诉", "合同", "官司", "刑事", "移民"),
}

RISK_RULES = (
    Rule("crisis", ("自杀", "自残", "活不下去", "伤害", "家暴", "跟踪", "被威胁")),
    Rule("professional_health", ("医生", "用药", "手术", "怀孕", "诊断", "癌", "病")),
    Rule("professional_legal", ("律师", "起诉", "合同", "官司", "刑事", "移民")),
    Rule("professional_finance", ("股票", "彩票", "赌博", "投资", "贷款", "梭哈", "币圈")),
    Rule("coercion", ("控制他", "控制她", "让他爱我", "让她爱我", "诅咒", "报复")),
)

REPEAT_PATTERNS = (
    "再占",
    "再问一次",
    "反复问",
    "刚刚问过",
    "又问",
    "同一个问题",
)

COMPOUND_MARKERS = ("，", "、", " 和 ", " 以及 ", "还是", "并且", "同时", "还有")


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_domain(text: str) -> str:
    for domain, keywords in DOMAIN_RULES.items():
        if contains_any(text, keywords):
            return domain
    return "general"


def detect_risks(text: str) -> list[str]:
    return [rule.label for rule in RISK_RULES if contains_any(text, rule.keywords)]


def is_repeat_question(text: str, previous_questions: object = None) -> bool:
    if contains_any(text, REPEAT_PATTERNS):
        return True
    if isinstance(previous_questions, list):
        normalized = normalize_text(text)
        for previous in previous_questions:
            if similarity_key(str(previous)) and similarity_key(str(previous)) == similarity_key(normalized):
                return True
    return False


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text.strip().lower())


def similarity_key(text: str) -> str:
    cleaned = normalize_text(text)
    for token in ("我想问", "请问", "帮我", "用易经", "占一下", "看看", "是否", "会不会"):
        cleaned = cleaned.replace(token, "")
    return cleaned[:24]


def is_single_matter(text: str) -> bool:
    if sum(1 for marker in COMPOUND_MARKERS if marker in text) >= 2:
        return False
    question_marks = text.count("?") + text.count("？")
    if question_marks > 1:
        return False
    if "还是" in text and contains_any(text, ("工作", "关系", "搬家", "投资", "健康")):
        return False
    return True


def reframe(text: str, domain: str, risks: list[str], repeat: bool, single_matter: bool) -> str:
    if "crisis" in risks:
        return "先暂停占问，把问题改为：我现在如何获得即时安全和可信任支持？"
    if any(risk.startswith("professional_") for risk in risks):
        return "易经不能替代专业判断；可改为：面对这个现实问题，我需要优先确认哪些信息、风险和下一步？"
    if "coercion" in risks:
        return "不做操控他人的占问；可改为：我如何守住边界，并以尊重的方式处理这段关系？"
    if repeat:
        return "同一问题不建议反复占问；可改为：上一次结果之后，我现在新增了什么事实或行动选择？"
    if not single_matter:
        return "请拆成一事一问；优先选择当前最需要行动的一个问题。"

    if domain == "relationship":
        return "这段关系当前的互动结构和我下一步可调整之处是什么？"
    if domain == "career":
        return "我当前工作局势的主要变化、阻碍和下一步重点是什么？"
    if domain == "decision":
        return "面对这个选择，我应如何理解当前形势、风险和可行动的下一步？"
    if domain == "timing":
        return "这件事的发展节奏有哪些阻滞和可观察信号？"
    if domain == "self_cultivation":
        return "我当前状态需要如何调整，下一步应守住什么原则？"
    return "这件事当前的变化结构、阻碍和可行动的下一步是什么？"


def next_steps(can_continue: bool) -> list[str]:
    if not can_continue:
        return ["pause_yijing_divination", "resolve_safety_or_question_framing_first"]
    return [
        "confirm_reframed_question",
        "choose_or_record_casting_method",
        "record_hexagram_with_yijing_hexagram_record",
        "lint_final_output_with_mystic_output_lint",
    ]


def guard(payload: dict[str, object]) -> dict[str, object]:
    text = str(payload.get("question_text", payload.get("request_text", ""))).strip()
    if not text:
        raise ValueError("question_text or request_text is required")

    domain = detect_domain(text)
    risks = detect_risks(text)
    repeat = is_repeat_question(text, payload.get("previous_questions"))
    single_matter = is_single_matter(text)
    can_continue = not risks and not repeat and single_matter

    warnings: list[str] = []
    if repeat:
        warnings.append("同一问题不建议反复占问，除非事实或行动选择已经发生实质变化。")
    if not single_matter:
        warnings.append("易经占问应一事一问，避免把多个问题合并成一个卦。")
    if risks:
        warnings.append("此问题涉及危机、操控或专业判断，不能直接进入占问。")

    return {
        "question_text": text,
        "question_domain": domain,
        "risk_flags": risks,
        "is_repeat_question": repeat,
        "is_single_matter": single_matter,
        "can_continue_yijing": can_continue,
        "reframed_question": reframe(text, domain, risks, repeat, single_matter),
        "warnings": warnings,
        "limits": [
            "易经输出只能作为变化结构和行动反思，不作为确定预言。",
            "一事一问，避免反复占问同一问题。",
            "不得替代医疗、法律、财务或紧急安全建议。",
        ],
        "next_steps": next_steps(can_continue),
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
        return {"question_text": raw}
    if args.text:
        return {"question_text": args.text}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"question_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Yijing question text.")
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

