#!/usr/bin/env python3
"""Lookup safe symbolic prompts for talisman and charm motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "peace_charm": ("平安符", "安心、提醒、出行前检查、祝愿", "不承诺挡灾或避免事故。"),
    "protective_knot": ("护身结/结绳", "连接、记念、边界、提醒", "不写成超自然防护证明。"),
    "bag_charm": ("香囊/符袋", "收纳、随身提醒、气味记忆、节令", "不鼓励摄入或危险香料。"),
    "door_charm": ("门符/门贴", "边界、入口秩序、家庭沟通、节令", "不确认驱邪或挡煞事实。"),
    "written_fulu": ("符箓/符纸", "传统书写、秩序、愿望承载、来源记录", "不提供画符作法、烧符或符水步骤。"),
    "name_tag": ("姓名/愿望牌", "意图记录、纪念、承诺、提醒", "不承诺愿望必然实现。"),
    "red_string": ("红绳", "连接、祝愿、记念、关系边界", "不承诺姻缘或复合。"),
    "seal_symbol": ("印/印章符号", "确认、秩序、边界、仪式感", "不写成权威认证或灵验保证。"),
}

ALIASES = {
    "平安符": "peace_charm",
    "护身符": "peace_charm",
    "护身结": "protective_knot",
    "结绳": "protective_knot",
    "香囊": "bag_charm",
    "符袋": "bag_charm",
    "门符": "door_charm",
    "门贴": "door_charm",
    "符箓": "written_fulu",
    "符纸": "written_fulu",
    "灵符": "written_fulu",
    "愿望牌": "name_tag",
    "姓名牌": "name_tag",
    "红绳": "red_string",
    "印章": "seal_symbol",
    "印": "seal_symbol",
    "amulet": "peace_charm",
    "talisman": "written_fulu",
    "charm": "peace_charm",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("item", ""))))
    if not code:
        raise ValueError("query, symbol, or item is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown talisman symbol: {code}")
    canonical, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "talisman_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("item", code)))).strip(),
        "canonical_name": canonical,
        "system": "talisman_symbolic_reflection",
        "symbol_code": code,
        "symbol_set": "common_talisman_and_charm_motifs",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为护符/符箓象征，围绕{focus}整理来源、文化语境、个人联想、现实证据和低风险下一步。",
        "reflection_questions": [
            "这个物件来自寺庙、道观、家人口述、商家、朋友，还是用户自制？",
            "它更像祝愿、提醒、纪念、边界，还是空间秩序？",
            "哪些结论必须回到现实安全、预算、专业支持或当事人沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把护符写成驱邪证明、挡灾证明、治病、招财保证或专业建议。",
            "不提供画符作法、烧符、喝符水、吞符、放血、诅咒或操控他人的步骤。",
            "不制造高价购买、开光压力或反复依赖。",
        ],
        "next_steps": ["combine_with_talisman_record", "prefer_low_risk_storage_or_reminder_use", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Talisman motif, e.g. 平安符, 红绳, 符箓.")
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
