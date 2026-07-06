#!/usr/bin/env python3
"""Rank feng shui recommendations by safety, cost, reversibility, and impact."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    label: str
    keywords: tuple[str, ...]


SAFETY_RULES = (
    Rule("gas_or_fire", ("燃气", "煤气", "明火", "火花", "烧焦", "易燃", "火源")),
    Rule("electrical", ("电路", "漏电", "插座", "电线", "跳闸")),
    Rule("mold_or_air", ("霉菌", "发霉", "潮湿", "异味", "头晕")),
    Rule("security", ("门锁", "监控", "入室", "被威胁", "跟踪")),
)

HIGH_COST_RULES = (
    Rule("renovation", ("拆墙", "改门", "改窗", "重装", "装修", "砸", "水电改造", "换地板")),
    Rule("large_purchase", ("换床", "换沙发", "买大型", "定制柜", "全屋")),
)

LOW_COST_RULES = (
    Rule("cleaning", ("清理", "收纳", "移走", "整理", "归位", "通风", "遮挡", "调整角度")),
    Rule("lighting", ("补充照明", "柔和照明", "暖光", "台灯")),
)

REVERSIBLE_RULES = (
    Rule("move_or_cover", ("移动", "移开", "调整", "遮挡", "屏风", "帘", "软装", "植物")),
    Rule("clean_or_label", ("清理", "收纳", "归位", "标记", "分区")),
)

IMPACT_RULES = (
    Rule("sleep", ("睡眠", "床", "镜", "卧室", "休息")),
    Rule("focus", ("专注", "桌", "办公室", "工作", "学习")),
    Rule("flow", ("入口", "动线", "门", "通道", "堵")),
    Rule("safety", ("燃气", "电路", "霉菌", "门锁", "火源")),
)


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def matched_labels(text: str, rules: Iterable[Rule]) -> list[str]:
    return [rule.label for rule in rules if contains_any(text, rule.keywords)]


def normalize_recommendations(payload: dict[str, object]) -> list[dict[str, object]]:
    if isinstance(payload.get("recommendations"), list):
        raw_items = payload["recommendations"]
        return [normalize_item(item, index) for index, item in enumerate(raw_items) if isinstance(item, (dict, str))]

    if isinstance(payload.get("checklist"), list):
        items: list[dict[str, object]] = []
        for item in payload["checklist"]:
            if not isinstance(item, dict):
                continue
            adjustments = item.get("low_risk_adjustments", [])
            if not isinstance(adjustments, list):
                continue
            for adjustment in adjustments:
                items.append(
                    {
                        "source_item_id": item.get("item_id", ""),
                        "category": item.get("category", ""),
                        "recommendation": str(adjustment),
                        "source_priority": item.get("priority", "medium"),
                        "traditional_terms": item.get("traditional_terms", []),
                    }
                )
        return [normalize_item(item, index) for index, item in enumerate(items)]

    raise ValueError("Provide recommendations or checklist")


def normalize_item(item: object, index: int) -> dict[str, object]:
    if isinstance(item, str):
        return {"id": f"rec_{index + 1}", "recommendation": item}
    normalized = dict(item)
    normalized.setdefault("id", normalized.get("source_item_id") or f"rec_{index + 1}")
    normalized.setdefault("recommendation", normalized.get("text", ""))
    return normalized


def estimate_cost(text: str) -> str:
    if matched_labels(text, HIGH_COST_RULES):
        return "high"
    if matched_labels(text, LOW_COST_RULES):
        return "low"
    return "medium"


def estimate_reversibility(text: str, cost: str) -> str:
    if cost == "high":
        return "low"
    if matched_labels(text, REVERSIBLE_RULES):
        return "high"
    return "medium"


def score_item(item: dict[str, object]) -> dict[str, object]:
    text = " ".join(str(value) for value in item.values() if not isinstance(value, list))
    safety_flags = matched_labels(text, SAFETY_RULES)
    impact_flags = matched_labels(text, IMPACT_RULES)
    cost = estimate_cost(text)
    reversibility = estimate_reversibility(text, cost)
    source_priority = str(item.get("source_priority", "medium"))

    requires_professional = bool(safety_flags) or cost == "high"
    safety_score = 100 if safety_flags else (70 if source_priority == "high" else 40)
    cost_score = {"low": 30, "medium": 15, "high": -20}[cost]
    reversibility_score = {"high": 25, "medium": 10, "low": -20}[reversibility]
    impact_score = min(30, 10 * len(impact_flags)) or (15 if source_priority == "high" else 5)
    professional_penalty = -15 if requires_professional and cost == "high" else 0
    total_score = safety_score + cost_score + reversibility_score + impact_score + professional_penalty

    urgency = "immediate" if safety_flags else ("soon" if source_priority == "high" else "later")
    action_type = "professional_check" if safety_flags else ("plan_before_action" if cost == "high" else "low_risk_adjustment")

    return {
        "id": str(item.get("id", "")),
        "recommendation": str(item.get("recommendation", "")).strip(),
        "source_item_id": str(item.get("source_item_id", "")),
        "category": str(item.get("category", "")),
        "urgency": urgency,
        "action_type": action_type,
        "cost_level": cost,
        "reversibility": reversibility,
        "impact_flags": impact_flags,
        "safety_flags": safety_flags,
        "requires_professional": requires_professional,
        "score": total_score,
        "rationale": build_rationale(safety_flags, cost, reversibility, impact_flags, requires_professional),
    }


def build_rationale(
    safety_flags: list[str],
    cost: str,
    reversibility: str,
    impact_flags: list[str],
    requires_professional: bool,
) -> str:
    parts = []
    if safety_flags:
        parts.append("涉及现实安全，必须优先处理")
    if requires_professional and cost == "high":
        parts.append("成本高或不可逆，建议先咨询专业人士")
    elif cost == "low" and reversibility == "high":
        parts.append("低成本且可逆，适合先做")
    else:
        parts.append(f"成本{cost}，可逆性{reversibility}")
    if impact_flags:
        parts.append("关联：" + "、".join(impact_flags))
    return "；".join(parts) + "。"


def rank(payload: dict[str, object]) -> dict[str, object]:
    recommendations = normalize_recommendations(payload)
    ranked = [score_item(item) for item in recommendations if str(item.get("recommendation", "")).strip()]
    ranked.sort(key=lambda item: (-int(item["score"]), item["recommendation"]))
    for index, item in enumerate(ranked, start=1):
        item["rank"] = index

    return {
        "ranked_recommendations": ranked,
        "summary": {
            "total": len(ranked),
            "immediate": sum(1 for item in ranked if item["urgency"] == "immediate"),
            "professional_required": sum(1 for item in ranked if item["requires_professional"]),
            "low_risk_first": [item["recommendation"] for item in ranked if item["action_type"] == "low_risk_adjustment"][:3],
        },
        "output_guidance": [
            "先说现实安全，再说传统术语。",
            "优先推荐低成本、可逆、非危险的调整。",
            "高成本或不可逆调整只作为讨论方向，不作为立即执行命令。",
            "最终回答仍需通过 mystic_output_lint。",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --json, --file, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON input with recommendations or checklist.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = rank(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
