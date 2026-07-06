#!/usr/bin/env python3
"""Lookup safe symbolic prompts for animal, bird, and insect omen motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "bird": ("鸟", "bird", "消息、移动、视角、过境", "不把鸟类出现写成死亡、灾祸或灵体证明。"),
    "crow": ("乌鸦", "bird", "警觉、边界、声音、群体记忆", "不承诺厄运、死亡或报应。"),
    "owl": ("猫头鹰", "bird", "夜间、观察、安静、未知", "不确认鬼神、死亡预兆或诅咒。"),
    "swallow": ("燕子", "bird", "归来、筑巢、季节、家宅感", "不承诺家庭运势或必然喜事。"),
    "sparrow": ("麻雀", "bird", "日常、细碎消息、邻近环境", "不把日常出现夸大成天意。"),
    "butterfly": ("蝴蝶", "insect", "转变、轻盈、短暂停留、审美", "不承诺感情复合、转运或亡灵讯息。"),
    "moth": ("飞蛾", "insect", "趋光、执念、夜间吸引、边界", "不把趋光写成灾祸或自毁命令。"),
    "spider": ("蜘蛛", "insect", "编织、等待、连接、细节", "不鼓励徒手接触或忽视虫害。"),
    "bee": ("蜜蜂", "insect", "协作、边界、劳动、警戒", "蜂窝、过敏和叮咬风险优先现实安全处理。"),
    "snake": ("蛇", "reptile", "蜕变、边界、本能、警觉", "蛇类安全风险优先，不鼓励靠近、捕捉或自行处理。"),
    "cat": ("猫", "animal", "自主、观察、亲近与边界", "不读取第三方想法或确认灵异守护。"),
    "dog": ("狗", "animal", "守望、陪伴、警觉、习惯", "咬伤、流浪犬或狂犬风险优先现实处理。"),
    "fish": ("鱼", "animal", "流动、资源、群体、节奏", "不承诺发财、好运或投资结果。"),
    "bat": ("蝙蝠", "animal", "夜间、倒挂、隐蔽、误入", "蝙蝠接触和公共卫生风险优先，不做预兆咨询。"),
    "mouse": ("老鼠", "animal", "隐蔽、消耗、缝隙、环境提醒", "鼠患和卫生风险优先现实处理，不写成家运灾祸。"),
}

ALIASES = {
    "鸟": "bird",
    "鸟进屋": "bird",
    "bird": "bird",
    "乌鸦": "crow",
    "乌鸦叫": "crow",
    "crow": "crow",
    "猫头鹰": "owl",
    "owl": "owl",
    "燕子": "swallow",
    "swallow": "swallow",
    "麻雀": "sparrow",
    "sparrow": "sparrow",
    "蝴蝶": "butterfly",
    "butterfly": "butterfly",
    "飞蛾": "moth",
    "蛾": "moth",
    "moth": "moth",
    "蜘蛛": "spider",
    "spider": "spider",
    "蜜蜂": "bee",
    "蜂": "bee",
    "bee": "bee",
    "蛇": "snake",
    "snake": "snake",
    "猫": "cat",
    "cat": "cat",
    "狗": "dog",
    "犬": "dog",
    "dog": "dog",
    "鱼": "fish",
    "fish": "fish",
    "蝙蝠": "bat",
    "bat": "bat",
    "老鼠": "mouse",
    "鼠": "mouse",
    "mouse": "mouse",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("animal", ""))))
    if not code:
        raise ValueError("query, symbol, or animal is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown animal omen symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "animal_omen_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("animal", code)))).strip(),
        "canonical_name": canonical,
        "system": "animal_omen_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为动物征兆/民俗象征，围绕{focus}整理观察事实、文化联想、现实环境和低风险行动。",
        "reflection_questions": [
            "这是一次普通观察、季节性活动、建筑环境问题，还是用户在寻找确定性预兆？",
            "是否存在咬伤、虫害、蜂窝、鼠患、蛇/蝙蝠接触、受伤动物或公共卫生风险？",
            "哪些内容可以作为民俗象征，哪些必须回到现实安全、物业、动物救助或专业支持？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把动物出现写成死亡、灾祸、诅咒、鬼神、灵体讯息或未来事实证明。",
            "不鼓励伤害、捕捉、投喂、靠近野生动物或自行处理危险动物/虫害。",
            "不替代医疗、公共卫生、物业、动物救助、兽医、消防、法律或安全支持。",
        ],
        "next_steps": ["combine_with_observation_record", "rank_real_world_safety_first", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Animal, bird, or insect symbol.")
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
