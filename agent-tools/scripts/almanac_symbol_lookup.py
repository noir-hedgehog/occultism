#!/usr/bin/env python3
"""Lookup safe explanations for almanac and auspicious-date terms."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


TERMS = {
    "宜": ("recommended_activity_marker", ["适合", "传统标注", "活动类别"], "只能说明某来源把某类活动标为适宜，不代表现实结果保证。"),
    "忌": ("avoid_activity_marker", ["回避", "传统标注", "活动类别"], "只能作为民俗避让提示，不能覆盖安全、法律、医疗或合同要求。"),
    "冲": ("zodiac_conflict_marker", ["生肖", "冲突", "象征避让"], "若涉及生肖冲合，只能作为民俗偏好，不应给参与人贴负面标签。"),
    "煞": ("directional_inauspicious_marker", ["方位", "避让", "象征风险"], "不把方位煞写成真实灾祸；若涉及施工、交通或消防，现实安全优先。"),
    "黄道吉日": ("auspicious_day_label", ["吉日", "黄道", "民俗标签"], "必须说明来源和体系差异，不保证成功、发财、婚姻或健康结果。"),
    "黑道日": ("inauspicious_day_label", ["黑道", "避日", "民俗标签"], "只能作为传统分类，不可恐吓用户或要求取消现实必要安排。"),
    "建除十二神": ("jianchu_twelve_officers", ["建除", "十二值", "传统择日层"], "适合解释为择日体系中的一层，不能和所有派别混成唯一结论。"),
    "值神": ("day_deity_marker", ["值神", "黄黑道", "传统层"], "只做来源内术语解释；不同黄历、派别和地区可能不一致。"),
}

ALIASES = {
    "宜事项": "宜",
    "忌事项": "忌",
    "冲生肖": "冲",
    "岁煞": "煞",
    "黄道": "黄道吉日",
    "黑道": "黑道日",
    "十二建除": "建除十二神",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    return ALIASES.get(text, text)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    query = normalize(payload.get("query", payload.get("term", "")))
    if not query:
        raise ValueError("query or term is required")
    if query not in TERMS:
        raise ValueError(f"unknown almanac term: {query}")
    layer, keywords, guidance = TERMS[query]
    source_type = str(payload.get("source_type", "unknown")).strip() or "unknown"
    return {
        "tool": "almanac_symbol_lookup",
        "query": query,
        "canonical_name": query,
        "system": "almanac_symbolic_date_selection",
        "symbol_layer": layer,
        "keywords": keywords,
        "source_type": source_type,
        "interpretation_prompt": f"把「{query}」解释为择日/黄历来源中的 {layer}，先说明来源限制，再转成可讨论的偏好或避让条件。",
        "action_guidance": guidance,
        "prohibited_uses": [
            "不保证某个日期一定带来成功、发财、婚姻稳定、健康或安全结果。",
            "不把黄历术语写成必然发财、必然顺利、必然灾祸或必须服从。",
            "不替代医疗、法律、财务、合同、消防、交通或人身安全安排。",
            "不声称不同黄历、派别和地区一定会给出同一结论。",
        ],
        "next_steps": [
            "record_source_and_constraints",
            "compare_candidate_dates_against_practical_requirements",
            "rank_options_with_non_deterministic_language",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.query:
        payload["query"] = args.query
    if args.source_type:
        payload["source_type"] = args.source_type
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Almanac term.")
    parser.add_argument("--source-type", default="unknown", help="Source type label.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()
    try:
        result = lookup(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
