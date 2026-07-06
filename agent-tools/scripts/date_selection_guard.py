#!/usr/bin/env python3
"""Guard auspicious-date requests against deterministic or professional claims."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


EVENT_KEYWORDS = {
    "moving": ("搬家", "入宅", "乔迁"),
    "opening": ("开业", "开张", "开工", "开市"),
    "wedding": ("结婚", "婚礼", "订婚", "领证"),
    "travel": ("出行", "旅行", "远行"),
    "contract": ("签约", "签合同", "签协议"),
    "medical": ("手术", "生产", "剖腹产", "看病", "治疗"),
    "investment": ("投资", "股票", "彩票", "币圈", "贷款"),
    "ritual": ("祭祀", "开光", "驱邪", "净化", "烧纸"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用听医生", "不用律师", "不用消防", "不用看合同", "只看黄历"),
    "deterministic_outcome": ("必发财", "一定顺利", "保证", "必旺", "必成", "一定不会出事", "必离婚", "必倒霉"),
    "medical_timing": ("手术", "剖腹产", "用药", "治疗", "生产"),
    "financial_timing": ("股票", "彩票", "赌博", "投资", "贷款", "币圈"),
    "dangerous_ritual": ("密闭烧", "放血", "刀", "血祭", "酒精点火", "烧炭"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def detect_event_type(text: str) -> str:
    for event_type, keywords in EVENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return event_type
    return "general"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    event_type = str(payload.get("event_type", "")).strip() or detect_event_type(text)
    risk_flags = risk_flags_for(text)
    if event_type in {"medical", "investment"} and event_type not in risk_flags:
        risk_flags.append(f"{event_type}_professional_timing")
    can_continue = not any(flag in risk_flags for flag in ["medical_timing", "financial_timing", "dangerous_ritual"])
    if "professional_replacement" in risk_flags:
        can_continue = False
    return {
        "tool": "date_selection_guard",
        "request_text": text,
        "event_type": event_type,
        "can_continue_date_selection": can_continue,
        "risk_flags": risk_flags,
        "required_boundaries": [
            "择日只能作为民俗象征和计划整理，不保证结果。",
            "医疗、法律、财务、消防、合同和人身安全安排必须以专业要求和现实约束优先。",
            "若用户提供外部黄历或师承说法，必须标明来源，不升级为通用事实。",
        ],
        "clarifying_questions": [
            "这次择日的事件类型、地点、参与人和不可变现实约束是什么？",
            "候选日期是用户给出的，还是需要先列出可行窗口？",
            "用户更重视现实方便、家人协调、民俗象征、纪念意义，还是避开冲突时段？",
        ],
        "next_steps": [
            "record_practical_constraints",
            "lookup_almanac_terms_if_user_mentions_them",
            "rank_candidate_dates_symbolically",
            "lint_final_output_with_mystic_output_lint",
        ] if can_continue else ["pause_date_selection", "refer_to_real_world_professional_or_safety_constraints"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["request_text"] = args.text
    if args.event_type:
        payload["event_type"] = args.event_type
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="User request text.")
    parser.add_argument("--event-type", help="Optional event type.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_date_selection"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
