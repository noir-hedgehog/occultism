#!/usr/bin/env python3
"""Build a safe symbolic reflection plan for bibliomancy."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import bibliomancy_source_recorder
import bibliomancy_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = bibliomancy_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_bibliomancy_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是用户提供的短句、关键词、书名或私人联想；先询问用户自己的理解，不编造原文或作者意图。",
            "reflection_questions": ["这段内容来自哪里？", "它触发了什么情绪或现实主题？", "是否像命令、事实证明、专业替代或长段版权文本请求？"],
            "action_guidance": "不编造原文、作者意图、版权文本、天意命令、预言或第三方结论。",
        }
    return {
        "symbol": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "category": symbol["category"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = bibliomancy_source_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_bibliomancy"]:
        return {
            "tool": "bibliomancy_reflection_planner",
            "is_valid": False,
            "can_continue_bibliomancy": False,
            "query_text": record["query_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_bibliomancy_consultation", "reframe_to_real_world_support_or_short_user_excerpt"],
        }
    queries = []
    for item in (record["source_type"], record["selection_method"], record["page_or_location"]):
        if item and item not in queries:
            queries.append(item)
    for group in (record["keywords"], record["emotions"]):
        for item in group:
            if item not in queries:
                queries.append(item)
    if record["excerpt"] and "句子" not in queries:
        queries.append("句子")
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "bibliomancy_reflection_planner",
        "is_valid": True,
        "can_continue_bibliomancy": True,
        "query_text": record["query_text"],
        "source_title": record["source_title"],
        "source_type": record["source_type"],
        "selection_method": record["selection_method"],
        "page_or_location": record["page_or_location"],
        "excerpt": record["excerpt"],
        "keywords": record["keywords"],
        "emotions": record["emotions"],
        "reality_anchor": record["reality_anchor"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这次翻书结果能怎样作为阅读触发，帮助用户整理主题、情绪、选择和可验证行动？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先记录来源、抽取方式、页码/位置和用户自提供的短句或关键词；不补写长段原文。",
                "把书页内容作为象征提示，而不是天意、命令、事实证明或专业建议。",
                "把解释落回当下：一个主题、一个情绪线索、一个现实约束和一个可验证行动。",
                "涉及医疗心理健康、法律财务、第三方隐私、经文权威命令或反复依赖时暂停。",
                "需要引用时只保留用户已提供的短摘录，并优先用摘要和关键词复述。",
            ],
        },
        "limits": [
            "Use symbolic reading-reflection language only.",
            "Do not present a passage as fate, divine command, punishment, diagnosis, legal/financial advice, third-party mind reading, or professional replacement.",
            "Do not provide full books, chapters, long copyrighted excerpts, or invented source text.",
        ],
        "next_steps": ["draft_bibliomancy_answer_from_plan", "run_mystic_output_lint", "offer_grounded_reading_or_action_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "source_title", "source_type", "selection_method", "page_or_location", "excerpt", "keywords", "emotions", "reality_anchor", "focus"):
        value = getattr(args, key)
        if value:
            payload["query_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Bibliomancy notes.")
    parser.add_argument("--source-title", help="Book/source title.")
    parser.add_argument("--source-type", help="Book, poem, scripture, article, user notebook, etc.")
    parser.add_argument("--selection-method", help="How the passage was selected.")
    parser.add_argument("--page-or-location", help="Page, chapter, or location.")
    parser.add_argument("--excerpt", help="Short user-provided excerpt.")
    parser.add_argument("--keywords", help="Keywords from the passage.")
    parser.add_argument("--emotions", help="Emotions or tones.")
    parser.add_argument("--reality-anchor", help="Current practical anchor.")
    parser.add_argument("--focus", help="Optional focus.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = plan(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
