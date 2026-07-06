#!/usr/bin/env python3
"""Lookup safe symbolic prompts for sky-omen motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "cloud": ("云", "phenomenon", "变化、遮蔽、想象、过渡", "不写成灾祸、死亡或天气预报。"),
    "dragon_cloud": ("龙形云", "shape", "力量、上升、行动欲、文化意象", "不确认神明显灵、帝王命格或必然成功。"),
    "bird_cloud": ("鸟形云", "shape", "消息、移动、轻盈、离开与返回", "不确认第三方讯息或关系结果。"),
    "rainbow": ("彩虹", "phenomenon", "过渡、和解、希望、雨后整理", "不保证好运、复合、疗愈或财运。"),
    "sun_halo": ("日晕", "phenomenon", "边界、光环、注意力、天气变化提醒", "不替代天气预报或灾害预警。"),
    "moon_halo": ("月晕", "phenomenon", "夜间情绪、周期、边界、温和提醒", "不预测灾祸、疾病或关系结局。"),
    "lightning": ("闪电", "phenomenon", "突发、警醒、能量释放、边界", "不鼓励雷雨暴露或追逐闪电。"),
    "thunder": ("雷声", "phenomenon", "提醒、声量、压力释放、停顿", "不写成天罚、神怒或威胁。"),
    "red_sky": ("霞光/红天", "color", "结束、余温、显眼信号、一天复盘", "不写成灾难预兆或确定天气结论。"),
    "mist": ("雾", "phenomenon", "不确定、放慢、模糊边界、谨慎", "不替代交通安全或天气能见度判断。"),
}

ALIASES = {
    "云": "cloud",
    "云形": "cloud",
    "龙形云": "dragon_cloud",
    "龙": "dragon_cloud",
    "鸟形云": "bird_cloud",
    "鸟": "bird_cloud",
    "彩虹": "rainbow",
    "日晕": "sun_halo",
    "月晕": "moon_halo",
    "闪电": "lightning",
    "雷电": "lightning",
    "雷声": "thunder",
    "雷": "thunder",
    "霞光": "red_sky",
    "红天": "red_sky",
    "晚霞": "red_sky",
    "雾": "mist",
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
        raise ValueError(f"unknown sky-omen symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "daily_reflection"
    return {
        "tool": "sky_omen_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "sky_omen_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为天空观察的象征素材，围绕{focus}整理情绪、现实提醒和可验证行动。",
        "reflection_questions": [
            "这是民俗文化学习、一次观察记录，还是在寻找灾祸/天气/命运判断？",
            "观察时的现实天气、安全背景和用户第一联想是什么？",
            "是否涉及天气安全替代、灾祸恐吓、专业替代、第三方隐私或反复依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把天象、云形、彩虹、日月晕或雷电写成灾祸、死亡、天罚、灵体事实、天气预报或安全预警。",
            "不替代官方天气、应急撤离、避雷、交通安全、医疗法律财务或心理健康支持。",
            "不读取第三方真实想法，不鼓励危险天气暴露或反复观察依赖。",
        ],
        "next_steps": ["combine_with_sky_observation_record", "separate_symbolic_from_weather_or_disaster_prediction", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Sky omen motif.")
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
