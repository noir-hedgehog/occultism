#!/usr/bin/env python3
"""Lookup safe symbolic prompts for tea-leaf and coffee-ground patterns."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "bird": ("鸟", "animal", "消息、视角、轻盈、移动", "不承诺消息到来或关系回应。"),
    "road": ("路", "path", "选择、阶段、移动、路径", "不替代搬家、出行或职业重大决定。"),
    "mountain": ("山", "landscape", "阻力、耐心、界限、长期目标", "不写成必然困难或无法完成。"),
    "tree": ("树", "plant", "成长、根基、恢复、长期投入", "不写成健康诊断或必然好转。"),
    "heart": ("心形", "shape", "感受、关系、价值、照顾", "不窥探第三方真实想法或承诺复合。"),
    "ring": ("环", "shape", "承诺、循环、边界、重复模式", "不承诺婚姻、合同或绑定结果。"),
    "star": ("星", "shape", "希望、方向、灵感、可见度", "不写成注定成功。"),
    "fish": ("鱼", "animal", "资源、流动、机会、适应", "不承诺发财或投资收益。"),
    "key": ("钥匙", "object", "入口、解法、许可、关键问题", "不写成唯一答案或秘密揭示。"),
    "circle": ("圆形", "shape", "循环、完整、边界、重复", "不强化反复占问依赖。"),
}

ALIASES = {
    "鸟": "bird",
    "bird": "bird",
    "飞鸟": "bird",
    "路": "road",
    "道路": "road",
    "road": "road",
    "path": "road",
    "山": "mountain",
    "山峰": "mountain",
    "mountain": "mountain",
    "树": "tree",
    "树木": "tree",
    "tree": "tree",
    "心": "heart",
    "心形": "heart",
    "heart": "heart",
    "环": "ring",
    "圆环": "ring",
    "戒指": "ring",
    "ring": "ring",
    "星": "star",
    "星星": "star",
    "star": "star",
    "鱼": "fish",
    "fish": "fish",
    "钥匙": "key",
    "key": "key",
    "圆": "circle",
    "圆形": "circle",
    "circle": "circle",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("shape", ""))))
    if not code:
        raise ValueError("query, symbol, or shape is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown tasseography symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "tasseography_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("shape", code)))).strip(),
        "canonical_name": canonical,
        "system": "tasseography_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "common_tasseography_motifs",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为茶叶/咖啡渣图案象征，围绕{focus}整理个人联想、现实证据、边界和低风险下一步。",
        "reflection_questions": [
            "这个图案是用户实际观察、照片描述、模拟，还是外部应用给出的？",
            "它更像提醒行动、关系、资源、阻力、边界，还是重复模式？",
            "哪些结论必须回到现实证据、专业支持、当事人沟通或安全约束？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把杯底图案写成确定预言、事实证明、诊断、财富结果、赌博建议或专业意见。",
            "不使用图案窥探第三方真实想法、控制他人或决定重大风险事项。",
            "不反复观察、冲泡或重占直到满意。",
        ],
        "next_steps": ["combine_with_pattern_record", "prefer_reality_check_and_low_risk_action", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Cup pattern symbol, e.g. 鸟, 路, 山, tree.")
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
