#!/usr/bin/env python3
"""Build a safe search plan for lost-object symbolic requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import lost_object_context_recorder
import lost_object_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = lost_object_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_lost_object_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人物品、地点或记忆线索；先询问语境，不编造定位、嫌疑人或灵验方位。",
            "reflection_questions": ["它对应最后看见、移动路径、容器、场所还是联系渠道？", "怎样转成一个可执行的现实搜索动作？", "是否涉及寻人、隐私定位、犯罪定责、专业渠道替代或反复依赖？"],
            "action_guidance": "不编造准确位置或灵验结果；只放回路径复盘、区域排查、联系渠道和停止条件。",
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
    record = lost_object_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_lost_object"]:
        return {
            "tool": "lost_object_search_planner",
            "is_valid": False,
            "can_continue_lost_object": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "search_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_lost_object_consultation", "reframe_to_real_world_search_or_safety_support"],
        }
    queries = []
    for group in ([record["item_description"], record["last_seen"], record["route_context"]], record["possible_areas"], record["checked_areas"], record["contact_channels"], record["practical_actions"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "lost_object_search_planner",
        "is_valid": True,
        "can_continue_lost_object": True,
        "context_text": record["context_text"],
        "item_description": record["item_description"],
        "last_seen": record["last_seen"],
        "route_context": record["route_context"],
        "possible_areas": record["possible_areas"],
        "checked_areas": record["checked_areas"],
        "contact_channels": record["contact_channels"],
        "practical_actions": record["practical_actions"],
        "risk_notes": record["risk_notes"],
        "review_time": record["review_time"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "search_plan": {
            "core_prompt": "这次失物/寻物请求怎样从占卜定位改写为最后接触记录、路径复盘、区域分层和现实联系？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先声明不保证定位或找到，只提供有限搜索计划。",
                "按最后看见时间地点、离手动作和当天路线重建时间线。",
                "把可能区域分成随身容器、转场点、固定台面、交通/公共场所和已排除区域。",
                "列出可联系渠道，例如同伴、物业、前台、客服、失物招领或支付/证件挂失渠道。",
                "设置复盘时间和停止条件，避免反复占问；证件、财务或疑似盗窃优先现实处理。",
            ],
        },
        "limits": [
            "Use memory, route, container, area, contact-channel, and bounded-search language only.",
            "Do not promise accurate location, guaranteed recovery, supernatural tracking, or identify a thief.",
            "Do not handle missing people, emergency missing pets, crime evidence, stalking, or privacy location requests.",
            "Do not replace police, property management, customer service, school, hospital, transport lost-and-found, or family support.",
            "Do not encourage repeated divination loops; include review time and stop condition.",
        ],
        "next_steps": ["draft_lost_object_answer_from_plan", "run_mystic_output_lint", "offer_bounded_search_and_stop_condition"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "item_description", "last_seen", "route_context", "possible_areas", "checked_areas", "contact_channels", "practical_actions", "risk_notes", "review_time", "stop_condition", "focus"):
        value = getattr(args, key)
        if value:
            payload["context_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"context_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Lost-object notes.")
    parser.add_argument("--item-description", help="Lost item description.")
    parser.add_argument("--last-seen", help="Last seen time/place.")
    parser.add_argument("--route-context", help="Route context.")
    parser.add_argument("--possible-areas", help="Possible areas.")
    parser.add_argument("--checked-areas", help="Already checked areas.")
    parser.add_argument("--contact-channels", help="Contact channels.")
    parser.add_argument("--practical-actions", help="Practical actions.")
    parser.add_argument("--risk-notes", help="Risk notes.")
    parser.add_argument("--review-time", help="Review time.")
    parser.add_argument("--stop-condition", help="Stopping condition.")
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
