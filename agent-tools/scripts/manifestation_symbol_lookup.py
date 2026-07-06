#!/usr/bin/env python3
"""Lookup safe symbolic prompts for manifestation and intention motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "intention": ("意图/愿望", "core", "方向、选择、承诺、可控行动", "不写成宇宙必须兑现或命运保证。"),
    "written_note": ("祈愿纸/愿望清单", "object", "记录、聚焦、复盘、边界", "不要求焚烧、摄入或保密恐吓。"),
    "moon": ("月亮", "cycle", "周期、复盘、开始、释放", "不保证显化结果，不替代月相天文或仪式权威。"),
    "seed": ("种子", "object", "萌芽、耐心、照料、小步行动", "不承诺必然开花结果。"),
    "key": ("钥匙", "object", "入口、选择、准备、权限", "不写成必然打开所有机会。"),
    "water": ("水杯/清水", "object", "澄清、流动、情绪、补给", "不暗示饮用可治疗或改变命运。"),
    "thread": ("红绳/线", "object", "连接、提醒、边界、持续", "不作为捆绑他人或关系操控。"),
    "candle": ("蜡烛", "object", "注意力、点亮、仪式感、结束", "不鼓励明火风险或密闭燃烧。"),
    "mirror": ("镜子", "object", "自我看见、校准、诚实复盘", "不确认灵体或第三方真相。"),
    "gratitude": ("感恩", "practice", "看见已有资源、稳定、复盘", "不要求用户压抑痛苦或否认现实困难。"),
}

ALIASES = {
    "意图": "intention",
    "愿望": "intention",
    "心愿": "intention",
    "祈愿": "intention",
    "祈愿纸": "written_note",
    "愿望清单": "written_note",
    "纸": "written_note",
    "新月": "moon",
    "月亮": "moon",
    "种子": "seed",
    "钥匙": "key",
    "水杯": "water",
    "清水": "water",
    "红绳": "thread",
    "线": "thread",
    "蜡烛": "candle",
    "镜子": "mirror",
    "感恩": "gratitude",
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
        raise ValueError(f"unknown manifestation symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "grounded_intention_planning"
    return {
        "tool": "manifestation_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "manifestation_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为意图整理的象征素材，围绕{focus}转成现实约束、可控行动和复盘点。",
        "reflection_questions": [
            "这是文化学习、意图整理，还是在寻求结果保证或控制他人？",
            "哪些部分是用户可控行动，哪些部分需要现实证据或专业支持？",
            "是否涉及危险仪式、付费压力、财务医疗替代、第三方操控或反复依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不承诺愿望必然实现、宇宙响应、神灵命令、命运保证或显化成功率。",
            "不替代医疗、法律、财务、心理健康、报警、求助或现实专业支持。",
            "不控制第三方、不诅咒报复、不鼓励危险仪式、高价购买或反复依赖。",
        ],
        "next_steps": ["combine_with_intention_record", "separate_symbolic_from_guaranteed_result", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Manifestation motif.")
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
