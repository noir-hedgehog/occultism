#!/usr/bin/env python3
"""Lookup safe symbolic prompts for body omen folklore signals."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "left_eye_twitch": ("左眼跳", "signal", "注意、接收、疲劳、休息提醒", "不写成发财、灾祸或疾病判断。"),
    "right_eye_twitch": ("右眼跳", "signal", "行动、输出、紧张、节奏提醒", "不写成灾祸、损失或必然事件。"),
    "ear_ringing": ("耳鸣/耳响", "signal", "暂停、安静、信息过载、身体照料", "持续或单侧耳鸣优先医疗支持，不作预兆解读。"),
    "ear_heat": ("耳热", "signal", "被想起、社交感、注意外界评价", "不写成他人真实想法或读心。"),
    "sneeze": ("喷嚏", "signal", "打断、释放、环境刺激、节奏切换", "不写成有人必然想你或疾病诊断。"),
    "face_heat": ("脸热", "signal", "情绪、曝光感、社交压力、休息", "不写成羞辱、灾祸或他人评价事实。"),
    "palm_itch": ("手心痒", "signal", "交换、欲望、预算、触碰提醒", "不写成财运保证、中奖或投资时机。"),
    "muscle_twitch": ("肉跳", "signal", "紧绷、疲劳、身体提醒、放松", "不写成灾祸或灵异证据。"),
    "time_slot": ("时辰/时间段", "context", "民俗对照、记录、当时情境、复盘", "不把时间表写成绝对吉凶。"),
    "body_care_note": ("身体照料备注", "method", "休息、饮水、用眼间隔、降低刺激", "不替代医疗诊断、检查或治疗。"),
}

ALIASES = {
    "左眼": "left_eye_twitch",
    "左眼跳": "left_eye_twitch",
    "left eye": "left_eye_twitch",
    "右眼": "right_eye_twitch",
    "右眼跳": "right_eye_twitch",
    "right eye": "right_eye_twitch",
    "耳鸣": "ear_ringing",
    "耳响": "ear_ringing",
    "ear ringing": "ear_ringing",
    "耳热": "ear_heat",
    "耳朵热": "ear_heat",
    "喷嚏": "sneeze",
    "打喷嚏": "sneeze",
    "sneeze": "sneeze",
    "脸热": "face_heat",
    "脸红": "face_heat",
    "手心痒": "palm_itch",
    "手痒": "palm_itch",
    "肉跳": "muscle_twitch",
    "肌肉跳": "muscle_twitch",
    "时辰": "time_slot",
    "时间": "time_slot",
    "照料": "body_care_note",
    "身体照料": "body_care_note",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered.replace(" ", "_")))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("omen", ""))))
    if not code:
        raise ValueError("query, symbol, or omen is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown body omen symbol: {code}")
    canonical, layer, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "body_omen_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("omen", code)))).strip(),
        "canonical_name": canonical,
        "system": "body_omen_symbolic_reflection",
        "symbol_code": code,
        "symbol_layer": layer,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为身体征兆/{layer}民俗象征，围绕{focus}整理身体照料、现实背景、情绪提示和停止条件。",
        "reflection_questions": [
            "这是本人自愿记录的低风险征兆、民俗时间对照，还是需要医疗支持的身体症状？",
            "它更像疲劳、刺激、社交感、节奏切换、预算提醒还是休息提醒？",
            "哪些判断必须回到身体照料、现实证据、医疗红旗和不反复查询的边界？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把身体征兆写成疾病、灾祸、灵体、财运、他人想法或事实结果证明。",
            "不替代医疗诊断、检查、用药、急症处理、心理健康支持或专业建议。",
            "不鼓励彩票赌博、投资择时、第三方身体标签、危险身体试验或反复依赖。",
        ],
        "next_steps": ["combine_with_body_omen_context", "prioritize_body_care_and_reality_check", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Body omen signal or context symbol.")
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
