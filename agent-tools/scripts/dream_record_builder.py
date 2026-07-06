#!/usr/bin/env python3
"""Build a structured record for symbolic dream interpretation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


EMOTION_KEYWORDS = {
    "fear": ("害怕", "恐惧", "惊醒", "吓醒", "紧张", "焦虑", "追", "逃"),
    "sadness": ("难过", "哭", "失落", "遗憾", "孤单"),
    "anger": ("生气", "愤怒", "吵架", "攻击", "争执"),
    "relief": ("放松", "安心", "轻松", "释然"),
    "confusion": ("迷路", "找不到", "混乱", "忘了", "看不清"),
}

SYMBOL_KEYWORDS = {
    "water": ("水", "海", "河", "湖", "雨", "洪水", "游泳"),
    "falling": ("坠落", "掉下", "摔下", "掉进"),
    "chase": ("追", "逃", "躲", "追赶"),
    "teeth": ("牙", "牙齿", "掉牙"),
    "exam": ("考试", "迟到", "作业", "学校", "老师"),
    "house": ("房子", "家", "房间", "门", "窗", "地下室"),
    "snake": ("蛇",),
    "death": ("死亡", "去世", "葬礼", "死了"),
    "flying": ("飞", "飞起来", "漂浮"),
    "lost": ("迷路", "找不到", "丢了"),
}

RISK_PATTERNS = {
    "nightmare_repetition": ("反复", "连续", "每天", "很多次", "一直梦到"),
    "sleep_impairment": ("睡不着", "不敢睡", "失眠", "整晚", "影响睡眠"),
    "diagnosis_request": ("是不是病", "诊断", "心理疾病", "抑郁", "焦虑症", "创伤"),
    "omen_certainty": ("预兆", "一定", "是不是要出事", "会不会死", "灾"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def detect_labels(text: str, table: dict[str, tuple[str, ...]]) -> list[str]:
    return [label for label, keywords in table.items() if contains_any(text, keywords)]


def sentence_excerpt(text: str, limit: int = 120) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:limit]


def build(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("dream_text", payload.get("request_text", ""))).strip()
    if not text:
        raise ValueError("dream_text or request_text is required")
    context = str(payload.get("waking_context", "")).strip()
    user_goal = str(payload.get("user_goal", "")).strip() or "symbolic_reflection"
    emotions = sorted(set(detect_labels(text + context, EMOTION_KEYWORDS) + list(payload.get("emotions", []) or [])))
    symbols = sorted(set(detect_labels(text, SYMBOL_KEYWORDS) + list(payload.get("symbols", []) or [])))
    risk_flags = detect_labels(text + context, RISK_PATTERNS)
    missing_fields = []
    if not context:
        missing_fields.append("waking_context")
    if not emotions:
        missing_fields.append("emotions")
    if not symbols:
        missing_fields.append("dream_symbols")
    can_continue = "diagnosis_request" not in risk_flags
    if "sleep_impairment" in risk_flags:
        can_continue = False
    return {
        "tool": "dream_record_builder",
        "is_valid": True,
        "can_continue_dream_reflection": can_continue,
        "dream_excerpt": sentence_excerpt(text),
        "user_goal": user_goal,
        "waking_context": context,
        "emotion_labels": emotions,
        "symbol_candidates": symbols,
        "risk_flags": risk_flags,
        "missing_fields": missing_fields,
        "clarifying_questions": [
            "醒来后最强烈的感受是什么？",
            "最近现实中有没有相似的压力、变化、关系或身体疲劳？",
            "你想把这个梦当作情绪整理、文化象征，还是创作素材？",
        ],
        "safety_notes": [
            "梦境记录不能替代心理健康、医疗或睡眠问题评估。",
            "反复噩梦、严重失眠或创伤相关困扰应优先建议现实专业支持。",
            "不要把梦写成必然预兆、诅咒证据或他人真实意图。",
        ],
        "next_steps": [
            "lookup_main_symbols",
            "build_dream_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["dream_text"] = args.text
    if args.context:
        payload["waking_context"] = args.context
    if args.goal:
        payload["user_goal"] = args.goal
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"dream_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Dream or request text.")
    parser.add_argument("--context", help="Recent waking-life context.")
    parser.add_argument("--goal", help="User goal for the dream reading.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()
    try:
        result = build(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_dream_reflection"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
