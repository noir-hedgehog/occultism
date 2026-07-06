#!/usr/bin/env python3
"""Select low-risk symbolic cleansing protocols for common ritual-support scenarios."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Iterable

import ritual_safety_check
import ritual_source_guard


SCENARIOS = {
    "moving_home": {
        "name": "搬家/入住安定",
        "keywords": ("搬家", "新家", "入住", "租房", "搬进", "换房"),
        "goal": "把陌生空间整理成可休息、可观察、可掌控的日常环境。",
        "steps": [
            "先检查燃气、电路、水渍、霉味、门窗和基本照明。",
            "清理入口、床铺、卫生间和厨房四个基础区域。",
            "开窗通风 10-20 分钟；若空气或治安条件不允许，改为空气净化和开灯。",
            "在干净桌面放一杯常温水或一件日常物品，作为入住开始的象征。",
            "写下三件需要后续确认的现实事项，例如维修、邻里、通勤或睡眠。",
        ],
        "monitoring": "入住后记录 3 天睡眠、气味、噪音、光线和安全感变化。",
    },
    "sleep_grounding": {
        "name": "睡前安定/噩梦后复位",
        "keywords": ("睡", "失眠", "噩梦", "夜里", "半夜", "害怕"),
        "goal": "降低睡前刺激和恐惧循环，建立可重复的安定动作。",
        "steps": [
            "睡前 30 分钟减少恐怖内容、争执信息和高刺激屏幕输入。",
            "检查门窗、燃气、电器和床边动线，只检查一遍并记录已经完成。",
            "用柔和灯光、轻音乐或白噪音替代焚香、蜡烛和烟雾。",
            "写下担忧，再写一句结束语，例如“今晚先休息，明天再处理”。",
            "若连续失眠、幻听幻视或失控感加重，优先联系专业支持或可信任的人。",
        ],
        "monitoring": "记录睡眠时长、惊醒次数、白天精神状态和是否需要现实支持。",
    },
    "relationship_closure": {
        "name": "分手/告别收束",
        "keywords": ("分手", "前任", "告别", "结束", "断联", "复合失败"),
        "goal": "把情绪收束和边界建立分开处理，不使用控制或报复型仪式。",
        "steps": [
            "整理一个小区域或一个物件盒，只处理用户自己的物品。",
            "写下想结束的循环和一个后续边界，例如暂不联系、整理聊天记录或寻求陪伴。",
            "做一个无火收尾动作：折叠纸张、放入盒子、丢弃副本或关闭通知。",
            "安排一个现实支持动作，例如约朋友散步、咨询、运动或规律进食。",
            "不做诅咒、复合保证、操控对方或跟踪查看的步骤。",
        ],
        "monitoring": "观察 7 天内冲动联系、睡眠、进食和工作/学习受影响程度。",
    },
    "space_pressure": {
        "name": "空间压迫/不安感整理",
        "keywords": ("压抑", "不舒服", "不干净", "阴森", "有鬼", "中邪", "害怕"),
        "goal": "先处理可见空间因素和身体感受，不确认超自然原因。",
        "steps": [
            "检查异味、潮湿、霉菌、噪音、光线、通风和杂物堆积。",
            "只选一个最影响动线或休息的点清理，避免整夜折腾。",
            "增加稳定光源，整理床边或入口，保留一条清楚通道。",
            "用音乐、通风、无火香氛或常温饮水替代烟熏和燃烧。",
            "把“不安感”记录为时间、地点、触发因素和身体反应，方便复盘。",
        ],
        "monitoring": "记录不安出现的时间、空间位置、身体状态和现实触发因素。",
    },
}

DO_NOT_DO = [
    "不使用血液、刀具、针扎、自伤或威胁行为。",
    "不在密闭空间燃烧纸、炭、香、蜡烛或酒精。",
    "不摄入符水、草药粉、未知液体或他人提供的不明物。",
    "不做诅咒、控制、报复、强迫复合或侵犯他人边界的步骤。",
    "不把仪式当作医疗、法律、财务、心理危机或人身安全支持的替代品。",
]


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_scenario(text: str, explicit: object = None) -> str:
    raw = str(explicit or "").strip()
    if raw in SCENARIOS:
        return raw
    for scenario_id, data in SCENARIOS.items():
        if contains_any(text, data["keywords"]):
            return scenario_id
    return "space_pressure"


def protocol(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", "")).strip()
    if not text:
        raise ValueError("request_text is required")
    scenario_id = detect_scenario(text, payload.get("scenario"))
    scenario = SCENARIOS[scenario_id]
    safety = ritual_safety_check.check({"request_text": text})
    source = ritual_source_guard.guard({"request_text": text, "source_type": payload.get("source_type", "unknown")})
    risk_level = str(safety["risk_level"])
    steps = list(scenario["steps"])
    if risk_level in {"orange", "red"}:
        steps.insert(0, "暂停原请求中的危险仪式动作，只保留现实安全检查和无火、无摄入、无伤害的替代。")
    return {
        "request_text": text,
        "scenario_id": scenario_id,
        "scenario_name": scenario["name"],
        "risk_level": risk_level,
        "can_continue_symbolic_support": risk_level in {"green", "yellow"},
        "goal": scenario["goal"],
        "protocol_steps": steps,
        "do_not_do": DO_NOT_DO,
        "monitoring": scenario["monitoring"],
        "safety_result": safety,
        "source_guard": {
            "source_type": source["source_type"],
            "source_claim_level": source["source_claim_level"],
            "missing_source_fields": source["missing_source_fields"],
            "certainty_flags": source["certainty_flags"],
        },
        "escalation": [
            "若有人身危险、自伤/他伤冲动、家暴、跟踪或被威胁，先联系当地紧急服务或可信任的人。",
            "若出现幻听幻视、持续失眠、失控感或强烈恐惧升级，优先联系心理/医疗专业支持。",
            "若发现燃气、电路、霉菌、结构安全或消防问题，联系物业、维修或专业人员。",
        ],
        "next_steps": [
            "apply_protocol_steps",
            "avoid_prohibited_actions",
            "monitor_changes",
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
    if args.scenario:
        payload["scenario"] = args.scenario
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
    parser.add_argument("--text", help="User cleansing/support request.")
    parser.add_argument("--scenario", help="Optional scenario id.")
    parser.add_argument("--source-type", help="Optional source type for ritual_source_guard.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()
    try:
        result = protocol(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
