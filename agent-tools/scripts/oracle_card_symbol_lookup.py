#!/usr/bin/env python3
"""Lookup safe symbolic prompts for common oracle-card motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


MOTIFS = {
    "door": ("门/入口", "开始、选择、进入、阈限", "不承诺机会必然打开。"),
    "bridge": ("桥", "连接、过渡、沟通、跨越", "不替代关系或合同判断。"),
    "seed": ("种子", "潜力、培育、耐心、开始", "不承诺一定成长或成功。"),
    "river": ("河流", "流动、顺势、情绪、路径", "不把顺势写成放弃现实判断。"),
    "mountain": ("山", "挑战、稳定、距离、坚持", "不写成不可改变的命运。"),
    "mirror": ("镜子", "自省、投射、诚实、看见", "不读取第三方真实想法。"),
    "compass": ("指南针", "方向、价值排序、定位、选择", "不替用户做最终决定。"),
    "moon": ("月亮", "情绪、周期、潜意识、想象", "不把情绪当事实或诊断。"),
    "sun": ("太阳", "清晰、活力、显现、鼓励", "不承诺成功。"),
    "star": ("星星", "希望、愿景、远方目标、灵感", "不承诺愿望必然实现。"),
    "feather": ("羽毛", "轻盈、信息、释放、温柔", "不写成天使命令或灵体证明。"),
    "key": ("钥匙", "重点、开启、可行入口、答案感", "不写成唯一答案。"),
}

ALIASES = {
    "门": "door",
    "入口": "door",
    "桥": "bridge",
    "种子": "seed",
    "河": "river",
    "河流": "river",
    "山": "mountain",
    "镜子": "mirror",
    "指南针": "compass",
    "月亮": "moon",
    "太阳": "sun",
    "星星": "star",
    "羽毛": "feather",
    "钥匙": "key",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_")
    if lowered in MOTIFS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("motif", payload.get("card", ""))))
    if not code:
        raise ValueError("query, motif, or card is required")
    if code not in MOTIFS:
        raise ValueError(f"unknown oracle-card motif: {code}")
    canonical, keywords_raw, action = MOTIFS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "oracle_card_symbol_lookup",
        "query": str(payload.get("query", payload.get("motif", payload.get("card", code)))).strip(),
        "canonical_name": canonical,
        "system": "oracle_card_symbolic_reflection",
        "symbol_code": code,
        "symbol_set": "common_oracle_card_motifs",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为神谕卡图像/关键词母题，围绕{focus}整理个人联想、现实证据、边界和低风险下一步。",
        "reflection_questions": [
            "这个母题在用户本轮牌面或关键词里具体出现在哪里？",
            "它更像支持、阻力、提醒、资源，还是下一步动作？",
            "哪些结论必须回到现实证据、当事人沟通、专业意见或安全措施？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把神谕卡写成事实证明、专业建议、诊断、预测或最终决定。",
            "不读取第三方真实想法，不确认灵体命令、诅咒、附身或被害。",
            "不编造某个商业牌组的固定权威牌义。",
        ],
        "next_steps": ["combine_with_draw_record", "ask_for_deck_specific_text_if_needed", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Oracle-card motif, e.g. door, bridge, seed, 门.")
    parser.add_argument("--focus", help="Optional focus.")
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
