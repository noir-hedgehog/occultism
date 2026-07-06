#!/usr/bin/env python3
"""Lookup safe symbolic prompts for bibliomancy motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "page": ("页码/位置", "selection", "偶然、定位、当下注意力", "不把页码写成天意、必然或唯一答案。"),
    "opening": ("翻开/随机打开", "selection", "入口、开始、被注意到的主题", "不鼓励反复翻到满意或用随机性替代决定。"),
    "line": ("句子/短句", "text_unit", "凝缩、提示、可复述的线索", "不扩写受版权保护原文，不把短句写成命令。"),
    "keyword": ("关键词", "text_unit", "主题、筛选、反复出现的焦点", "不把关键词变成诊断、判决或预言。"),
    "poem": ("诗/诗句", "source", "意象、节奏、留白、情绪", "不把诗句写成事实证明或关系保证。"),
    "classic": ("经典/经文", "source", "传统、训诫、价值、文化语境", "不写成不可质疑的神谕命令、天罚或专业替代。"),
    "novel": ("小说/故事", "source", "角色投射、叙事选择、冲突结构", "不把虚构情节当现实预言。"),
    "notebook": ("笔记/日记", "source", "个人记忆、未完成想法、复盘线索", "不读取第三方隐私或暴露敏感原文。"),
    "door": ("门/入口", "motif", "选择、许可、开始、边界", "不写成必须跨越的命令。"),
    "road": ("路/道路", "motif", "过程、方向、分岔、下一步", "不预测唯一未来或保证结果。"),
}

ALIASES = {
    "页码": "page",
    "位置": "page",
    "随机翻书": "opening",
    "随机翻开": "opening",
    "翻开": "opening",
    "句子": "line",
    "短句": "line",
    "关键词": "keyword",
    "诗": "poem",
    "诗句": "poem",
    "经典": "classic",
    "经文": "classic",
    "小说": "novel",
    "故事": "novel",
    "笔记": "notebook",
    "日记": "notebook",
    "门": "door",
    "入口": "door",
    "路": "road",
    "道路": "road",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown bibliomancy symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "reading_reflection"
    return {
        "tool": "bibliomancy_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "bibliomancy_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为阅读触发的象征素材，围绕{focus}整理主题、情绪、选择和可验证行动。",
        "reflection_questions": [
            "这是文化学习、一次翻书记录，还是在寻找决定论答案？",
            "用户提供的是短句/关键词/摘要，还是要求长段版权文本？",
            "是否涉及专业替代、第三方隐私、经文权威命令、财务法律或反复依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把书页、经文、经典、随机句子写成事实证明、命令、天意、惩罚、专业建议或命运保证。",
            "不提供整本书、全章或长段受版权保护文本。",
            "不用于第三方读心、投资法律、医疗心理健康替代或反复翻书依赖。",
        ],
        "next_steps": ["combine_with_bibliomancy_record", "separate_symbolic_prompt_from_authority_or_fate", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Bibliomancy motif.")
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
