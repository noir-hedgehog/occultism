#!/usr/bin/env python3
"""Lookup safe symbolic prompts for spirit-message motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "higher_self": ("高我", "source_metaphor", "内在价值、长期视角、自我照料", "不写成外部命令或绝对权威。"),
    "spirit_guide": ("守护灵/指导灵", "source_metaphor", "支持感、提醒、陪伴、边界", "不证明灵体存在或要求服从。"),
    "angel": ("天使讯息", "source_metaphor", "安抚、慈悲、保护感、温和提醒", "不写成天使命令、医疗建议或结果保证。"),
    "ancestor": ("祖先/祖辈意象", "source_metaphor", "传承、家族记忆、价值观、祝福", "不确认亡灵讯息或替代家庭沟通。"),
    "inner_voice": ("内在声音", "process", "直觉句子、情绪线索、需要被听见的部分", "持续声音、命令或失控感优先专业支持。"),
    "automatic_writing": ("自动书写", "process", "自由写作、联想流、未整理想法", "不作为事实证明、预言或外部实体控制。"),
    "feather": ("羽毛", "symbol", "轻盈、信息、温柔、释放", "不确认天使或亡灵在场。"),
    "light": ("光", "symbol", "看见、清晰、希望、注意力", "不承诺净化、疗愈或驱邪。"),
    "door": ("门", "symbol", "选择、许可、边界、过渡", "不写成必须跨越的命令。"),
    "name": ("名字/称呼", "symbol", "身份、关系、记忆触发、称呼边界", "不确认实体身份或第三方事实。"),
}

ALIASES = {
    "高我": "higher_self",
    "higher self": "higher_self",
    "守护灵": "spirit_guide",
    "指导灵": "spirit_guide",
    "spirit guide": "spirit_guide",
    "天使": "angel",
    "天使讯息": "angel",
    "祖先": "ancestor",
    "祖辈": "ancestor",
    "内在声音": "inner_voice",
    "直觉句子": "inner_voice",
    "自动书写": "automatic_writing",
    "automatic writing": "automatic_writing",
    "羽毛": "feather",
    "光": "light",
    "门": "door",
    "名字": "name",
    "称呼": "name",
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
        raise ValueError(f"unknown spirit-message symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "inner_dialogue_reflection"
    return {
        "tool": "spirit_message_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "spirit_message_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为象征写作素材，围绕{focus}整理情绪线索、边界提醒和可验证行动。",
        "reflection_questions": [
            "这是文化学习、写作/冥想记录，还是在寻找事实证明或命令？",
            "这句话让用户想到哪些当下边界、需求、关系或行动？",
            "是否涉及危机、幻听幻视、第三方隐私、专业替代或付费压力？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把通灵/高我/守护灵讯息写成事实证明、灵体命令、医疗建议、关系保证或财务法律判断。",
            "不确认亡灵、附身、诅咒、驱邪或第三方真实想法。",
            "不制造付费通灵、开天眼、反复问灵或依赖诱导。",
        ],
        "next_steps": ["combine_with_message_record", "separate_symbolic_from_fact_or_command", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Spirit-message motif.")
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
