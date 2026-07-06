#!/usr/bin/env python3
"""Lookup safe symbolic prompts for evil-eye, protection, and cord-cutting motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "evil_eye": ("恶眼", "protection_motif", "嫉妒感、暴露感、边界、目光压力", "把恶眼当作边界和暴露感整理提醒，不确认谁害你。"),
    "blue_eye_charm": ("蓝眼护符", "object", "提醒、注视、边界、文化象征", "只作为提醒物或文化符号，不承诺挡灾或驱邪。"),
    "protective_bubble": ("保护罩/防护罩", "visualization", "边界、空间感、暂停、呼吸", "可作为短时想象练习，不写成真实能量屏障。"),
    "cord_cutting": ("能量断联", "boundary_practice", "收回注意力、结束反复确认、界限", "只用于自我边界整理，不操控、切断或惩罚他人。"),
    "salt": ("盐", "object", "清理、界线、朴素提醒、日常秩序", "不建议摄入、撒向他人或破坏环境；只作象征提醒。"),
    "black_tourmaline": ("黑碧玺/黑色石", "object", "稳定、落地、边界、提醒物", "不承诺防小人或治疗，不制造购买压力。"),
    "mirror": ("镜子", "object", "反照、自我观察、界限、停止投射", "不用于反噬、诅咒或攻击他人。"),
    "grounding": ("grounding/落地", "practice", "呼吸、身体感、现实检查、支持系统", "用于把注意力带回现实安全和可控动作。"),
}

ALIASES = {
    "恶眼": "evil_eye",
    "evil eye": "evil_eye",
    "蓝眼": "blue_eye_charm",
    "蓝眼护符": "blue_eye_charm",
    "保护罩": "protective_bubble",
    "防护罩": "protective_bubble",
    "能量断联": "cord_cutting",
    "切断能量": "cord_cutting",
    "cord cutting": "cord_cutting",
    "energy cord": "cord_cutting",
    "盐": "salt",
    "黑碧玺": "black_tourmaline",
    "黑曜石": "black_tourmaline",
    "黑色石": "black_tourmaline",
    "镜子": "mirror",
    "grounding": "grounding",
    "落地": "grounding",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text.lower(), ALIASES.get(text, lowered))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown spiritual protection symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "boundary_reflection"
    return {
        "tool": "spiritual_protection_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "spiritual_protection_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的低风险象征素材，围绕情绪、边界、现实安全、提醒物和停止条件整理。",
        "reflection_questions": [
            "这是边界整理，还是在确认谁害你、诅咒报复或替代现实安全支持？",
            "触发场景、情绪、身体感、现实安全背景和可控边界动作是什么？",
            "是否涉及危险仪式、跟踪监控、第三方指认、高价购买或反复依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不确认加害者、小人、恶眼来源、下咒事实、灵体事实或第三方隐私。",
            "不提供诅咒报复、反噬、危险仪式、跟踪监控、专业替代或关系操控。",
            "不制造高价购买压力，不强化反复清理和恐惧依赖。",
        ],
        "next_steps": ["combine_with_spiritual_protection_context", "separate_symbolic_boundary_from_blame_or_retaliation", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Spiritual protection motif.")
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
