#!/usr/bin/env python3
"""Guard lost-object divination and search-symbol requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "lost_object_symbolic_consultation": ("失物", "寻物", "找东西", "丢了", "不见了", "找不到", "遗失", "lost object", "missing item"),
    "memory_search_reflection": ("回忆", "最后一次", "路径", "搜索", "排查", "清单", "可能放哪"),
    "divination_frame": ("占卜找", "塔罗找", "灵摆找", "卦找", "方位", "在哪个方向"),
}

RISK_KEYWORDS = {
    "missing_person_or_child": ("找人", "寻人", "孩子不见", "小孩不见", "老人走失", "失踪", "人口失踪", "同学失联", "家人失联"),
    "missing_pet_emergency": ("猫丢了", "狗丢了", "宠物走失", "宠物丢了", "猫不见", "狗不见"),
    "crime_or_evidence": ("被偷", "盗窃", "偷走", "嫌疑人", "小偷", "犯罪证据", "监控不用看", "不用报警"),
    "professional_replacement": ("不用报警", "不用物业", "不用学校", "不用医院", "不用警察", "不用联系家人", "不用客服"),
    "guaranteed_location": ("一定在", "百分百在", "保证找到", "立刻找到", "准确定位", "绝对方向", "神准定位"),
    "privacy_or_stalking": ("定位别人", "查他在哪", "跟踪", "偷看", "监视", "破解定位"),
    "repeated_dependency": ("一直占", "反复占", "每天占", "停不下来", "不占就焦虑", "找不到就一直问"),
}

SAFE_NEGATED_PHRASES = (
    "不保证找到",
    "不保证定位",
    "不替代报警",
    "不替代物业",
    "不替代客服",
    "不查别人",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "lost_object_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "missing_person_or_child" in flags:
        return "寻人、儿童/老人走失或失联不能用玄学替代现实求助；应优先联系家人、场所工作人员和当地紧急/警方渠道。"
    if "missing_pet_emergency" in flags:
        return "走失宠物先走现实搜寻：联系物业/邻居/兽医/收容渠道、发布清晰信息，不用占卜替代行动。"
    if "crime_or_evidence" in flags:
        return "疑似盗窃或证据问题不能用占卜定罪；应保留证据、查看现实记录并联系合适渠道。"
    if "professional_replacement" in flags:
        return "寻物象征咨询不能替代报警、物业、客服、学校、医院或家人协助。"
    if "guaranteed_location" in flags:
        return "不保证定位或一定找到；只能把方位/元素说法改写成搜索清单和记忆线索。"
    if "privacy_or_stalking" in flags:
        return "不协助定位、监视或跟踪他人；只能处理本人有权寻找的物品。"
    if "repeated_dependency" in flags:
        return "如果反复占问加重焦虑，先限定一次搜索计划、复盘时间和停止条件。"
    return "可以把失物占卜改写为最后接触记录、路径复盘、区域分层、现实搜索清单和停止条件。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "lost_object_request_guard",
        "request_text": text,
        "system": "lost_object_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_lost_object": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "失物/寻物只处理本人有权寻找的物品，不处理寻人、跟踪、犯罪定责或隐私定位。",
            "不承诺准确方位、一定找到、灵验定位或神秘指认。",
            "疑似盗窃、紧急走失、证件财务风险或安全风险时，优先现实渠道和专业支持。",
            "输出必须转成最后接触记录、路径复盘、区域搜索、联系渠道、复盘时间和停止条件。",
        ],
        "clarifying_questions": [
            "丢失的是本人有权寻找的物品，还是人、宠物、证件、财物或疑似盗窃相关？",
            "物品类型、最后看见时间地点、当天路线、可能区域、已找过位置、可联系对象和搜索时限是什么？",
            "是否涉及报警/客服/物业/学校/医院等现实渠道、隐私定位、保证找到或反复占问依赖？",
        ],
        "next_steps": [
            "record_lost_object_context",
            "lookup_lost_object_symbols",
            "build_lost_object_search_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_lost_object_consultation", "reframe_to_real_world_search_or_safety_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.text:
        return {"request_text": args.text}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Lost-object request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_lost_object"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
