#!/usr/bin/env python3
"""Lookup safe symbolic prompts for oracle-lot and temple-lot readings."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "great_auspicious": ("上上签", "lot_grade", "顺势、资源较足、仍需现实落实", "把好签写成鼓励和行动提醒，不承诺必成。"),
    "auspicious": ("上签/吉签", "lot_grade", "可推进、条件较顺、需确认现实约束", "适合整理下一步和风险清单，不跳到保证结果。"),
    "mixed": ("中签/平签", "lot_grade", "平衡、等待、审慎推进、信息不足", "适合提醒补充信息和稳住节奏。"),
    "challenging": ("下签/不利签", "lot_grade", "阻力、延迟、风险暴露、需要降速", "适合转成风险管理，不恐吓灾祸。"),
    "lot_text": ("签文/签诗", "text_layer", "隐喻、诗句、关键词、个人联想", "先解释字面和象征，再连接现实背景。"),
    "temple_source": ("寺庙/宫观来源", "source_layer", "地点、传统、版本、来源限制", "标注来源，不把单一签本升格为通用权威。"),
    "love_lot": ("月老签/姻缘签", "topic_layer", "关系期待、边界、沟通、现实互动", "不判断正缘、复合或对方真实想法。"),
    "career_lot": ("事业签", "topic_layer", "资源、阻力、时机、可控行动", "不保证录用、升职、发财或项目成败。"),
    "draw_method": ("抽签方法", "method_layer", "已抽、代抽、模拟、一次性、记录", "模拟抽签需要用户同意，不鼓励反复抽到满意。"),
}

ALIASES = {
    "上上签": "great_auspicious",
    "大吉": "great_auspicious",
    "上签": "auspicious",
    "吉签": "auspicious",
    "中签": "mixed",
    "中平": "mixed",
    "平签": "mixed",
    "下签": "challenging",
    "下下签": "challenging",
    "签文": "lot_text",
    "签诗": "lot_text",
    "签": "lot_text",
    "寺庙": "temple_source",
    "宫观": "temple_source",
    "月老签": "love_lot",
    "姻缘签": "love_lot",
    "事业签": "career_lot",
    "抽签": "draw_method",
    "代抽": "draw_method",
    "模拟抽签": "draw_method",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    if text in SYMBOLS:
        return text
    return ALIASES.get(text, text)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown oracle lot symbol: {code}")
    canonical, layer, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "oracle_lot_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "oracle_lot_symbolism",
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为{layer}层的签文象征，围绕{focus}整理提醒、现实约束和低风险行动。",
        "reflection_questions": [
            "这个签文来自哪里，版本和上下文是否清楚？",
            "签文里哪些词是鼓励、提醒、阻力或等待？",
            "现实中有哪些事实可以验证，哪些行动是低风险且可控的？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把签文写成必然应验、灾祸恐吓或结果保证。",
            "不替代医疗、法律、财务、人身安全或心理健康专业支持。",
            "不通过签文断定第三方真实想法、操控关系或鼓励反复抽签依赖。",
        ],
        "next_steps": ["combine_with_lot_record", "draft_symbolic_interpretation", "run_mystic_output_lint"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.query:
        payload["query"] = args.query
    if args.focus:
        payload["focus"] = args.focus
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Oracle-lot symbol, e.g. 上上签, 签文, 月老签.")
    parser.add_argument("--focus", help="Optional focus.")
    parser.add_argument("--json", help="JSON input.")
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
