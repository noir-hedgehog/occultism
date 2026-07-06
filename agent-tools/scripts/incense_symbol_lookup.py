#!/usr/bin/env python3
"""Lookup safe symbolic prompts for incense ash and smoke observations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "straight_smoke": ("直上烟", "smoke", "集中、上升、清晰、意图聚焦", "不写成神明回应或必然通达。"),
    "drifting_smoke": ("飘散烟", "smoke", "分散、环境影响、注意力转移、需要调整", "优先提醒通风和环境因素，不写成灵体信号。"),
    "curling_smoke": ("旋卷烟", "smoke", "回旋、重复模式、迟疑、需要复盘", "不写成被缠住、诅咒或鬼神干扰。"),
    "heavy_smoke": ("浓烟", "smoke", "负担、干扰、材料或通风检查", "优先提醒停止燃烧和通风，不写成灾祸预兆。"),
    "tower_ash": ("塔形香灰", "ash", "累积、支撑、阶段成果、稳定结构", "不写成神迹或必然成功。"),
    "broken_ash": ("断裂香灰", "ash", "中断、释放、节奏切换、重新安排", "不写成失败、冲撞或不祥定论。"),
    "bridge_ash": ("桥形香灰", "ash", "连接、过渡、沟通、两端协调", "不承诺关系或合作必然修复。"),
    "fan_ash": ("扇形香灰", "ash", "展开、选择、扩散、信息面增加", "不替代重大决定或专业判断。"),
    "glowing_tip": ("香头余光", "ember", "持续、余温、需要收尾、注意安全", "优先提醒确认完全熄灭，不写成神谕命令。"),
}

ALIASES = {
    "直上": "straight_smoke",
    "直上烟": "straight_smoke",
    "直烟": "straight_smoke",
    "straight": "straight_smoke",
    "飘散": "drifting_smoke",
    "散烟": "drifting_smoke",
    "drifting": "drifting_smoke",
    "旋卷": "curling_smoke",
    "卷烟": "curling_smoke",
    "curling": "curling_smoke",
    "浓烟": "heavy_smoke",
    "heavy smoke": "heavy_smoke",
    "塔形": "tower_ash",
    "塔形香灰": "tower_ash",
    "塔": "tower_ash",
    "tower": "tower_ash",
    "断裂": "broken_ash",
    "断香灰": "broken_ash",
    "broken": "broken_ash",
    "桥": "bridge_ash",
    "桥形": "bridge_ash",
    "bridge": "bridge_ash",
    "扇形": "fan_ash",
    "展开": "fan_ash",
    "fan": "fan_ash",
    "香头": "glowing_tip",
    "余光": "glowing_tip",
    "ember": "glowing_tip",
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
        raise ValueError(f"unknown incense symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "incense_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("observation", code)))).strip(),
        "canonical_name": canonical,
        "system": "incense_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "common_incense_ash_and_smoke_observations",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为香火/香灰/烟形象征，围绕{focus}整理个人联想、现实证据、通风与火源安全边界和低风险下一步。",
        "reflection_questions": [
            "观察是否已经安全结束，或是否来自照片/无烟替代？",
            "这个符号更像集中、分散、累积、中断、连接，还是展开提醒？",
            "哪些结论必须回到现实证据、消防/通风安全、专业支持或当事人沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把香火、香灰或烟形写成确定预言、事实证明、诊断、财富结果、驱邪证明、神明指令或专业意见。",
            "不提供点香、燃烧、烧纸、烧符、摄入香灰、放血或密闭燃烧步骤。",
            "不使用观察结果窥探第三方真实想法、控制他人或决定重大风险事项。",
        ],
        "next_steps": ["combine_with_incense_observation_record", "prefer_fire_smoke_safety_and_low_risk_action", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Incense observation, e.g. 直上烟, 塔形香灰, 香头.")
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
