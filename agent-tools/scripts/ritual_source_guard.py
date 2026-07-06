#!/usr/bin/env python3
"""Classify folk ritual sources and convert unsafe ritual claims into safe symbolic support."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Iterable

import ritual_safety_check


SOURCE_ALIASES = {
    "regional_folk": "regional_folk",
    "folk": "regional_folk",
    "民俗": "regional_folk",
    "地方习俗": "regional_folk",
    "religious_tradition": "religious_tradition",
    "religion": "religious_tradition",
    "宗教": "religious_tradition",
    "modern_wellness": "modern_wellness",
    "wellness": "modern_wellness",
    "现代疗愈": "modern_wellness",
    "commercial_new_age": "commercial_new_age",
    "new_age": "commercial_new_age",
    "商业课程": "commercial_new_age",
    "personal_preference": "personal_preference",
    "personal": "personal_preference",
    "个人经验": "personal_preference",
    "unknown": "unknown",
    "未知": "unknown",
}

SOURCE_LEVELS = {
    "regional_folk": "unverified_folk_claim",
    "religious_tradition": "documented_tradition_context_needed",
    "modern_wellness": "modern_symbolic_practice",
    "commercial_new_age": "commercial_or_modern_claim",
    "personal_preference": "personal_preference",
    "unknown": "unknown",
}

CERTAINTY_KEYWORDS = ("一定有鬼", "真的有鬼", "必定", "百分百", "肯定中邪", "必遭", "一定会")
SOURCE_HINTS = ("来自", "流传", "某地", "地方", "寺", "观", "老师说", "网上说", "祖传", "民间")
CONTEXT_HINTS = ("地区", "年代", "宗教", "出处", "来源", "传承", "作者", "书名", "田野", "口述")


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def normalize_source_type(raw: object, text: str) -> str:
    key = str(raw or "").strip().lower()
    if key in SOURCE_ALIASES:
        return SOURCE_ALIASES[key]
    if contains_any(text, ("佛", "道教", "寺", "道观", "神明", "法事")):
        return "religious_tradition"
    if contains_any(text, ("民间", "祖传", "地方", "某地", "村里", "老人说")):
        return "regional_folk"
    if contains_any(text, ("能量", "水晶", "新纪元", "课程", "疗愈师")):
        return "commercial_new_age"
    if contains_any(text, ("我习惯", "我自己", "个人")):
        return "personal_preference"
    return "unknown"


def missing_source_fields(text: str, source_type: str) -> list[str]:
    missing = []
    if source_type in {"regional_folk", "religious_tradition"} and not contains_any(text, CONTEXT_HINTS):
        missing.extend(["region_or_lineage", "source_context"])
    if source_type == "commercial_new_age" and not contains_any(text, ("课程", "作者", "机构", "出处")):
        missing.append("commercial_source_identity")
    if source_type == "unknown" and contains_any(text, SOURCE_HINTS):
        missing.append("source_type")
    return missing


def safe_protocol(goal: str, safety_result: dict[str, Any]) -> list[str]:
    steps = [
        "先做现实安全检查：通风、燃气、电路、霉菌、异味、尖锐物和动线。",
        "做 10-20 分钟基础清洁，只处理一个区域，避免过度消耗。",
        "用无火方式建立边界：开灯、播放轻音乐、放置一杯常温水或整理一块干净桌面。",
        "写下一句担忧和一句结束语，把纸收好或丢弃，作为象征性收尾。",
    ]
    if goal == "sleep":
        steps.append("睡前减少刺激信息，记录睡眠变化；若持续失眠或恐惧升级，优先求助现实支持。")
    if goal == "moving":
        steps.append("搬家场景优先处理入口、床铺、卫生间和厨房的清洁与照明。")
    if goal == "closure":
        steps.append("把重点放在告别、整理物品和重新安排日常节奏，不做报复或控制他人的仪式。")
    if safety_result["risk_level"] in {"orange", "red"}:
        steps.insert(0, "暂停原仪式，不执行火、烟、血、刀具、摄入、密闭燃烧或操控他人的步骤。")
    return steps


def detect_goal(text: str) -> str:
    if contains_any(text, ("睡", "失眠", "噩梦", "夜里")):
        return "sleep"
    if contains_any(text, ("搬家", "新家", "入住", "搬进")):
        return "moving"
    if contains_any(text, ("分手", "告别", "结束", "前任")):
        return "closure"
    return "space_reset"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("source_text", ""))).strip()
    if not text:
        raise ValueError("request_text or source_text is required")
    source_type = normalize_source_type(payload.get("source_type"), text)
    safety_result = ritual_safety_check.check({"request_text": text})
    risk_level = str(safety_result["risk_level"])
    certainty_flags = []
    if contains_any(text, CERTAINTY_KEYWORDS):
        certainty_flags.append("supernatural_certainty")
    if contains_any(text, ("包治", "治病", "代替医生", "发财", "稳赢", "复合成功", "保证", "开运", "转运", "必灵")):
        certainty_flags.append("outcome_or_professional_claim")

    missing = missing_source_fields(text, source_type)
    can_offer_steps = risk_level in {"green", "yellow"} and not certainty_flags
    can_use_context = source_type != "unknown" and "supernatural_certainty" not in certainty_flags
    goal = detect_goal(text)
    return {
        "request_text": text,
        "source_type": source_type,
        "source_claim_level": SOURCE_LEVELS[source_type],
        "missing_source_fields": missing,
        "certainty_flags": certainty_flags,
        "safety_result": safety_result,
        "can_use_as_cultural_context": can_use_context,
        "can_offer_steps": can_offer_steps,
        "required_framing": [
            "Frame ritual material as cultural, symbolic, historical, or personal practice, not verified supernatural fact.",
            "Separate observable safety needs from folk explanations.",
            "Name uncertainty when region, lineage, source, or context is missing.",
        ],
        "prohibited_framing": [
            "Do not confirm ghosts, curses, possession, guaranteed outcomes, or inevitable disasters.",
            "Do not provide steps involving blood, blades, ingestion, sealed smoke, coercion, or sleep deprivation.",
            "Do not present commercial or personal claims as tradition without source context.",
        ],
        "safe_symbolic_protocol": safe_protocol(goal, safety_result),
        "next_steps": [
            "run_ritual_safety_check",
            "ask_for_source_context_if_needed",
            "offer_safe_symbolic_protocol_only",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload.update(json.load(f))
    if args.text:
        payload["request_text"] = args.text
    if args.source_type:
        payload["source_type"] = args.source_type
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Ritual source or request text.")
    parser.add_argument("--source-type", help="regional_folk, religious_tradition, modern_wellness, commercial_new_age, personal_preference, unknown.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
