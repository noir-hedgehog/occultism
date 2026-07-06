#!/usr/bin/env python3
"""Build a safe symbolic plan for psychometry object reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import psychometry_object_recorder
import psychometry_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = psychometry_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_object_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人记忆、可见特征或物件来源；先询问用户自己的联想，不编造物品历史或身份事实。",
            "reflection_questions": ["这个特征如何被看见或记录？", "它触发了什么记忆或边界主题？", "是否像事实确认、隐私读取或专业替代？"],
            "action_guidance": "不编造物主身份、物品历史、真伪、灵体、犯罪线索或第三方结论。",
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
    record = psychometry_object_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_psychometry"]:
        return {
            "tool": "psychometry_reflection_planner",
            "is_valid": False,
            "can_continue_psychometry": False,
            "object_text": record["object_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_psychometry_consultation", "reframe_to_real_world_support_or_consent"],
        }
    queries = []
    for group in (record["object_types"], record["visible_features"], record["impressions"], record["emotions"]):
        for item in group:
            if item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "psychometry_reflection_planner",
        "is_valid": True,
        "can_continue_psychometry": True,
        "object_text": record["object_text"],
        "object_types": record["object_types"],
        "source_notes": record["source_notes"],
        "ownership_status": record["ownership_status"],
        "visible_features": record["visible_features"],
        "impressions": record["impressions"],
        "emotions": record["emotions"],
        "reality_anchor": record["reality_anchor"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这个物件能怎样作为象征素材，帮助用户整理记忆、边界、情绪联想和现实行动？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先确认物件属于用户本人或已获授权；未经同意、第三方隐私和失踪/刑案线索直接暂停。",
                "把内容拆成可见特征、来源备注、用户第一联想、情绪和现实问题；事实和象征分开写。",
                "把解释落回当下：整理、留存、归还、沟通、纪念、告别、预算或一个可验证行动。",
                "不确认物品历史、真伪、归属、灵体、诅咒、身份、犯罪线索或第三方想法。",
                "不替代医疗、安全检测、鉴定、法律、财务、报警或紧急支持，也不诱导付费净化。",
            ],
        },
        "limits": [
            "Use symbolic object-reflection language only.",
            "Do not present impressions as object history, identity, ownership, authenticity, spirit proof, crime clues, diagnosis, legal/financial advice, or third-party mind reading.",
            "Do not process unauthorized objects, missing-person/crime requests, paid-cleansing pressure, or repeated dependency.",
        ],
        "next_steps": ["draft_psychometry_answer_from_plan", "run_mystic_output_lint", "offer_real_world_evidence_or_consent_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "object_types", "source_notes", "ownership_status", "visible_features", "impressions", "emotions", "reality_anchor", "focus"):
        value = getattr(args, key)
        if value:
            payload["object_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"object_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Object-reading notes.")
    parser.add_argument("--object-types", help="Object types.")
    parser.add_argument("--source-notes", help="Source notes.")
    parser.add_argument("--ownership-status", help="Ownership or consent status.")
    parser.add_argument("--visible-features", help="Visible features.")
    parser.add_argument("--impressions", help="Impressions.")
    parser.add_argument("--emotions", help="Emotions or tones.")
    parser.add_argument("--reality-anchor", help="Current-life practical anchor.")
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
