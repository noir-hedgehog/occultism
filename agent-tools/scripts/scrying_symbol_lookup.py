#!/usr/bin/env python3
"""Lookup safe symbolic prompts for scrying visual observations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "cloudy_surface": ("雾面/模糊表面", "surface", "模糊、未定、需要澄清、信息不足", "不写成遮蔽、诅咒或灵体干扰。"),
    "clear_surface": ("清晰表面", "surface", "清楚、聚焦、可见、现实线索", "不写成真相显现或必然正确。"),
    "wave": ("波纹", "visual", "流动、情绪、变化、调整节奏", "不写成外界必然动荡或灾祸。"),
    "door": ("门", "visual", "入口、选择、边界、新阶段", "不承诺机会必然打开。"),
    "path": ("道路", "visual", "路径、推进、步骤、方向感", "不替代重大决定。"),
    "bird": ("鸟", "visual", "消息、视角、轻盈、距离", "不确认第三方消息或真实想法。"),
    "mountain": ("山", "visual", "阻力、稳定、长期目标、耐心", "不写成必然困难或命运阻碍。"),
    "circle": ("圆/环", "visual", "循环、边界、完整、重复模式", "不承诺关系、合同或结果绑定。"),
    "shadow": ("影子", "visual", "未说出的担心、模糊部分、需要命名", "不写成鬼影、邪气或人格判断。"),
}

ALIASES = {
    "雾面": "cloudy_surface",
    "模糊": "cloudy_surface",
    "cloudy": "cloudy_surface",
    "清晰": "clear_surface",
    "clear": "clear_surface",
    "波纹": "wave",
    "水纹": "wave",
    "wave": "wave",
    "门": "door",
    "入口": "door",
    "door": "door",
    "道路": "path",
    "路": "path",
    "path": "path",
    "鸟": "bird",
    "bird": "bird",
    "山": "mountain",
    "mountain": "mountain",
    "圆": "circle",
    "环": "circle",
    "circle": "circle",
    "影子": "shadow",
    "阴影": "shadow",
    "shadow": "shadow",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("observation", ""))))
    if not code:
        raise ValueError("query, symbol, or observation is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown scrying symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "scrying_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("observation", code)))).strip(),
        "canonical_name": canonical,
        "system": "scrying_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "common_scrying_visual_observations",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为水晶球/镜面/水面凝视象征，围绕{focus}整理个人联想、现实证据、身心安全边界和低风险下一步。",
        "reflection_questions": [
            "观察是否为短时、已结束的视觉联想？",
            "这个符号更像澄清、流动、入口、路径、阻力、循环，还是阴影提醒？",
            "哪些结论必须回到现实证据、身心安全、专业支持或当事人沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把影像、倒影或水纹写成确定预言、事实证明、诊断、财富结果、驱邪证明、灵体讯息或专业意见。",
            "不引导长时间凝视、强行入神、睡眠剥夺或追求幻觉。",
            "不使用观察结果窥探第三方真实想法、控制他人或决定重大风险事项。",
        ],
        "next_steps": ["combine_with_scrying_observation_record", "prefer_grounding_and_low_risk_action", "run_mystic_output_lint"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.query:
        return {"query": args.query, "focus": args.focus}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Scrying observation, e.g. 雾面, 波纹, 门.")
    parser.add_argument("--focus", help="Optional consultation focus.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
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
