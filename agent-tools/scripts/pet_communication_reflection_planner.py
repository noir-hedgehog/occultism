#!/usr/bin/env python3
"""Build a safe symbolic plan for pet communication reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import pet_communication_context_recorder
import pet_communication_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = pet_communication_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_pet_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人联想、宠物行为描述或照护线索；先询问用户自己的观察，不编造宠物真实讯息、疾病诊断、亡宠事实或走失位置。",
            "reflection_questions": ["这个行为可见吗？", "它和哪些环境/健康/照护因素有关？", "是否像兽医替代、事实确认或反复依赖？"],
            "action_guidance": "不编造宠物真实想法、兽医结论、亡宠灵体、走失位置或第三方责任。",
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
    record = pet_communication_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_pet_communication"]:
        return {
            "tool": "pet_communication_reflection_planner",
            "is_valid": False,
            "can_continue_pet_communication": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_pet_communication_consultation", "reframe_to_veterinary_or_real_world_support"],
        }
    queries = []
    for group in ([record["pet_type"], record["relationship"]], record["observations"], record["emotions"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "pet_communication_reflection_planner",
        "is_valid": True,
        "can_continue_pet_communication": True,
        "context_text": record["context_text"],
        "pet_type": record["pet_type"],
        "relationship": record["relationship"],
        "observations": record["observations"],
        "time_context": record["time_context"],
        "health_context": record["health_context"],
        "emotions": record["emotions"],
        "care_actions": record["care_actions"],
        "reality_anchor": record["reality_anchor"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这次宠物沟通请求能怎样被改写为行为观察、照护动作、情绪安放和兽医边界？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先记录可见行为、发生时间、环境变化和健康背景。",
                "把象征讯息限制为用户的温柔写作或照护提醒，不写成宠物真实话语。",
                "列出 1-3 个现实照护动作，例如观察食欲、补水、安静空间、记录频率。",
                "若有急症、持续异常、走失或安全风险，转向兽医、寻宠和现实支持。",
                "设置复盘时间，避免每天反复读取讯息寻求确定感。",
            ],
        },
        "limits": [
            "Use symbolic pet-observation and grief-support language only.",
            "Do not claim true pet messages, veterinary diagnosis, deceased pet spirit facts, missing pet location, third-party blame, or supernatural proof.",
            "Do not replace veterinary care, emergency treatment, medication, behavior support, or real-world missing-pet search.",
            "Do not encourage expensive purchases or repeated dependency.",
        ],
        "next_steps": ["draft_pet_communication_answer_from_plan", "run_mystic_output_lint", "offer_care_observation_and_vet_boundary_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "pet_type", "relationship", "observations", "time_context", "health_context", "emotions", "care_actions", "reality_anchor", "focus"):
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
    parser.add_argument("--text", help="Pet communication notes.")
    parser.add_argument("--pet-type", help="Pet type.")
    parser.add_argument("--relationship", help="Relationship to pet.")
    parser.add_argument("--observations", help="Observed behavior.")
    parser.add_argument("--time-context", help="Time and situation.")
    parser.add_argument("--health-context", help="Vet or health boundary.")
    parser.add_argument("--emotions", help="User emotions.")
    parser.add_argument("--care-actions", help="Practical care actions.")
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
