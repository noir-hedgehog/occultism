#!/usr/bin/env python3
"""Lookup safe symbolic prompts for pet communication motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "cat": ("猫", "pet", "边界、独处、敏感、节奏", "不把躲藏或亲近写成疾病诊断或真实怨恨。"),
    "dog": ("狗", "pet", "陪伴、回应、活动、习惯", "不把行为变化写成确定讯息或医疗判断。"),
    "hiding": ("躲起来", "behavior", "安全感、环境变化、休息、压力线索", "不替代兽医或行为专业判断；先观察现实触发。"),
    "purring": ("呼噜/放松声", "behavior", "安抚、亲近、身体状态线索", "不把呼噜解释成一定健康或一定开心。"),
    "meow": ("叫声", "behavior", "表达、需求、注意力、节奏变化", "不翻译成确定语言或真实指控。"),
    "tail": ("尾巴", "body_signal", "边界、警觉、互动距离、情绪线索", "不把单一动作当成确定结论。"),
    "appetite": ("食欲", "care_signal", "身体状态、日常节律、照护提醒", "食欲变化应优先记录并必要时咨询兽医。"),
    "doorway": ("门口/门边", "place", "进出、等待、边界、环境连接", "不写成走失定位或灵体通道事实。"),
    "deceased_pet_memory": ("亡宠怀念", "grief", "纪念、告别、爱、未说完的话", "不确认亡宠灵魂事实或附身。"),
    "photo": ("照片", "object", "记忆、观察、陪伴、纪念", "不通过照片确认疾病、位置或真实讯息。"),
}

ALIASES = {
    "猫": "cat",
    "狗": "dog",
    "躲": "hiding",
    "躲起来": "hiding",
    "呼噜": "purring",
    "叫": "meow",
    "叫声": "meow",
    "尾巴": "tail",
    "食欲": "appetite",
    "不吃": "appetite",
    "门口": "doorway",
    "门边": "doorway",
    "亡宠": "deceased_pet_memory",
    "离世": "deceased_pet_memory",
    "照片": "photo",
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
        raise ValueError(f"unknown pet communication symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "pet_care_reflection"
    return {
        "tool": "pet_communication_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "pet_communication_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为宠物观察和象征写作素材，围绕{focus}整理情绪、照护动作和兽医边界。",
        "reflection_questions": [
            "这是行为观察、怀念写作，还是在寻求真实讯息、兽医替代或走失定位？",
            "有哪些可见行为、环境变化、健康线索和现实照护动作？",
            "是否涉及急症、走失定位、亡宠事实确认、第三方指认、付费压力或反复依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不确认宠物真实想法、亡宠灵魂、托梦证明、附身、疾病诊断、走失位置或第三方责任。",
            "不替代兽医诊断、急症处理、用药、行为专业支持或现实寻宠流程。",
            "不制造高价付费压力，不强化反复读取依赖。",
        ],
        "next_steps": ["combine_with_pet_context_record", "separate_symbolic_from_veterinary_or_factual_claims", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Pet communication motif.")
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
