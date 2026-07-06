#!/usr/bin/env python3
"""Build a safe low-risk dowsing rod symbolism practice plan."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import dowsing_context_recorder
import dowsing_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = dowsing_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_custom_dowsing_symbol",
            "symbol_layer": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人动作描述、场地称呼、地图标记或自定义占杖记录；先询问来源和现实核查方式，不编造定位、医疗或资源结论。",
            "reflection_questions": ["动作/地点、授权范围、安全背景、现实核查和用户想整理的问题是什么？"],
            "action_guidance": "不编造地下管线、水源、疾病、灵体、寻人、投资、房产或施工结论。",
        }
    return {
        "symbol": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "symbol_layer": symbol["symbol_layer"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = dowsing_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_dowsing"]:
        return {
            "tool": "dowsing_practice_planner",
            "is_valid": False,
            "can_continue_dowsing": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "practice_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_dowsing_consultation", "reframe_to_safety_or_professional_support"],
        }
    symbol_plans = [build_symbol_plan(item, focus) for item in record["movement_notes"]]
    for extra in (record["observation_target"], record["space_or_map"]):
        if extra:
            symbol_plans.append(build_symbol_plan(extra, focus))
    return {
        "tool": "dowsing_practice_planner",
        "is_valid": True,
        "can_continue_dowsing": True,
        "question_text": record["question_text"],
        "tool_type": record["tool_type"],
        "observation_target": record["observation_target"],
        "space_or_map": record["space_or_map"],
        "movement_notes": record["movement_notes"],
        "authorization_context": record["authorization_context"],
        "focus": record["focus"],
        "safety_context": record["safety_context"],
        "reality_constraints": record["reality_constraints"],
        "duration": record["duration"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "practice_plan": {
            "core_prompt": "这个占杖记录如何帮助用户整理授权空间内的路线感、观察点、现实核查和低风险下一步？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明占杖只作文化象征和空间观察，不作地下管线、水源、医疗、寻人、法律、施工或房产决策工具。",
                "标注观察目标、授权范围、空间/地图、动作记录、安全背景、现实约束、时长和缺失字段。",
                "逐一把动作或空间点转成暂停、方向、边界、分区、动线和待核查假设，而不是事实定位。",
                "给出不挖掘、不闯入、不施工、不替代专业探测、低成本、可停止的现实核查清单。",
                "若涉及地下管线、开挖打井、水源矿脉、医疗地气、房产合同、第三方定位、驱邪恐惧、高价购买或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use dowsing symbolism and authorized low-risk observation only.",
            "Do not provide utility locating, excavation, well drilling, medical/geopathic, legal/property, missing-person, trespass, investment, or professional-replacement instructions.",
            "Avoid guarantees, resource-location claims, expensive tool/course pressure, and repeated dependency.",
        ],
        "next_steps": ["draft_dowsing_answer_from_plan", "run_mystic_output_lint", "offer_reality_checklist_and_stop_conditions"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "tool_type", "observation_target", "space_or_map", "movement_notes", "authorization_context", "focus", "duration"):
        value = getattr(args, attr)
        if value:
            payload["question_text" if attr == "text" else attr] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"question_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Dowsing request or context notes.")
    parser.add_argument("--tool-type", help="Tool type, e.g. L-rods, branch, map pointer.")
    parser.add_argument("--observation-target", help="Low-risk target, e.g. desk route reflection.")
    parser.add_argument("--space-or-map", help="Authorized room, desk, garden path, or map.")
    parser.add_argument("--movement-notes", help="Comma-separated movement notes.")
    parser.add_argument("--authorization-context", help="Self-authorized space or permitted context.")
    parser.add_argument("--focus", help="Reflection focus.")
    parser.add_argument("--duration", help="Time box or stop condition.")
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
