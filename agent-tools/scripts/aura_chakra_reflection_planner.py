#!/usr/bin/env python3
"""Build a safe symbolic plan for aura/chakra reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import aura_chakra_sensation_recorder
import aura_chakra_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = aura_chakra_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_energy_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人感受、课程术语或地方说法；先询问身体状态、触发场景和用户自己的联想，不编造固定能量意义。",
            "reflection_questions": ["感受在何时出现？", "是否持续、强烈或影响功能？", "用户自己的第一联想是什么？"],
            "action_guidance": "不编造诊断、疗愈、灵体、业障、身份等级或第三方结论。",
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
    record = aura_chakra_sensation_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_aura_chakra"]:
        return {
            "tool": "aura_chakra_reflection_planner",
            "is_valid": False,
            "can_continue_aura_chakra": False,
            "sensation_text": record["sensation_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_aura_chakra_consultation", "reframe_to_real_world_support"],
        }
    queries = []
    for group in (record["centers"], record["colors"], record["sensations"]):
        for item in group:
            if item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "aura_chakra_reflection_planner",
        "is_valid": True,
        "can_continue_aura_chakra": True,
        "sensation_text": record["sensation_text"],
        "centers": record["centers"],
        "colors": record["colors"],
        "sensations": record["sensations"],
        "context": record["context"],
        "duration": record["duration"],
        "intensity": record["intensity"],
        "grounding_notes": record["grounding_notes"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这些气场/脉轮符号能怎样帮助用户记录身体感受、情绪线索、边界需求和低风险行动？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先记录感受事实：位置、颜色、温度/强度、持续时间、触发场景和身体状态。",
                "把脉轮或气场解释写成象征语言，例如表达、边界、稳定、照料或行动提醒。",
                "胸痛、呼吸困难、持续失眠、惊恐、幻听幻视、强烈痛感或影响功能时，暂停象征流程并寻求专业支持。",
                "不读取第三方气场或真实想法，不承诺清理、疗愈、复合、发财或灵性等级。",
                "优先低成本 grounding：喝水、休息、记录、伸展、联系可信任的人或现实支持。",
            ],
        },
        "limits": [
            "Use symbolic reflection and body-awareness language only.",
            "Do not present aura/chakra sensations as diagnosis, healing, spirit proof, identity rank, fate proof, wealth signal, relationship proof, or professional advice.",
            "Do not create paid-healing pressure, third-party mind reading, coercion, or repeated dependency.",
        ],
        "next_steps": ["draft_aura_chakra_answer_from_plan", "run_mystic_output_lint", "offer_grounding_and_real_world_support_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "centers", "colors", "sensations", "context", "duration", "intensity", "grounding_notes", "focus"):
        value = getattr(args, key)
        if value:
            payload["sensation_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"sensation_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Aura/chakra sensation notes.")
    parser.add_argument("--centers", help="Chakra or body centers.")
    parser.add_argument("--colors", help="Aura or chakra colors.")
    parser.add_argument("--sensations", help="Sensation words.")
    parser.add_argument("--context", help="meditation, journaling, relationship_boundary, workspace, etc.")
    parser.add_argument("--duration", help="Duration note.")
    parser.add_argument("--intensity", help="Intensity note.")
    parser.add_argument("--grounding-notes", help="Grounding or body-state notes.")
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
