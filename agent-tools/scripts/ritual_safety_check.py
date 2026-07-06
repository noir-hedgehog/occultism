#!/usr/bin/env python3
"""Check ritual/exorcism/cleansing requests for safety risks."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Hazard:
    label: str
    keywords: tuple[str, ...]
    message: str


RED_HAZARDS = (
    Hazard("blood_or_self_harm", ("放血", "割腕", "自残", "血祭", "用血"), "涉及血液或自伤，必须阻断。"),
    Hazard("weapon_or_violence", ("刀", "针扎", "伤害", "打他", "报复"), "涉及武器、暴力或报复，必须阻断。"),
    Hazard("sealed_fire_or_poison", ("密闭燃烧", "密闭房间点", "密闭房间烧", "烧炭", "酒精点火", "煤气", "有毒"), "涉及窒息、燃烧或中毒风险，必须阻断。"),
    Hazard("coercive_curse", ("诅咒", "下咒", "控制他", "控制她", "让他爱我", "让她爱我"), "涉及诅咒、控制或操纵他人，必须拒绝。"),
)

ORANGE_HAZARDS = (
    Hazard("ingestion_or_unknown_substance", ("喝下", "吃下", "服用", "草药", "粉末", "符水"), "涉及摄入或未知物质，不提供步骤。"),
    Hazard("open_flame_or_smoke", ("点火", "烧纸", "蜡烛", "香炉", "烟熏", "艾草"), "涉及明火或烟雾，只能提供无火替代。"),
    Hazard("mental_health_signal", ("幻听", "幻视", "附身", "失控", "连续失眠", "被鬼控制"), "可能涉及精神健康或睡眠危机，应先寻求现实支持。"),
)

YELLOW_HAZARDS = (
    Hazard("fearful_frame", ("有鬼", "中邪", "被下咒", "被诅咒", "不干净"), "请求带有恐惧叙事，回答需降温和非确定化。"),
    Hazard("vulnerable_context", ("小孩", "孕妇", "老人参与", "老人居住", "老人房", "家里老人", "宠物", "密闭房间"), "场景较脆弱，建议只做低风险空间整理。"),
)


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def find_hazards(text: str, hazards: Iterable[Hazard]) -> list[Hazard]:
    return [hazard for hazard in hazards if contains_any(text, hazard.keywords)]


def safe_alternatives(risk_level: str) -> list[str]:
    base = [
        "开窗通风，确认燃气、电路、霉菌和异味源等现实安全问题。",
        "做基础清洁和收纳，优先处理床边、入口、桌面和垃圾。",
        "使用无火香氛、常温饮水、柔和灯光或轻音乐替代燃烧类仪式。",
        "把担忧写下来，折叠收好，并用一句结束语完成象征性收尾。",
    ]
    if risk_level in {"orange", "red"}:
        base.insert(0, "先暂停仪式，不执行任何涉及火、血液、刀具、摄入或密闭烟雾的步骤。")
    return base


def referral_message(risk_level: str, hazard_labels: list[str]) -> str:
    if risk_level == "red":
        return "这个请求包含即时伤害、危险仪式或操控他人的风险。请先确保人身安全，并联系当地紧急服务、可信任的人或专业支持。"
    if "mental_health_signal" in hazard_labels:
        return "如果你正在经历幻听、幻视、持续失眠、失控感或强烈恐惧，请先联系心理/医疗专业人士或可信任的人陪伴。"
    if risk_level == "orange":
        return "这个请求包含现实安全风险。我不能提供执行步骤，但可以帮助你改成低风险的空间整理和安定流程。"
    return "可以继续做低风险的象征性净化，但不要把它当作医疗、法律或安全问题的替代方案。"


def check(payload: dict[str, object]) -> dict[str, object]:
    text = str(payload.get("request_text", "")).strip()
    if not text:
        raise ValueError("request_text is required")

    red = find_hazards(text, RED_HAZARDS)
    orange = find_hazards(text, ORANGE_HAZARDS)
    yellow = find_hazards(text, YELLOW_HAZARDS)

    if red:
        risk_level = "red"
        hazards = red + orange + yellow
    elif orange:
        risk_level = "orange"
        hazards = orange + yellow
    elif yellow:
        risk_level = "yellow"
        hazards = yellow
    else:
        risk_level = "green"
        hazards = []

    labels = [hazard.label for hazard in hazards]
    return {
        "request_text": text,
        "risk_level": risk_level,
        "blocked_steps": [hazard.message for hazard in hazards if risk_level in {"orange", "red"}],
        "safe_alternatives": safe_alternatives(risk_level),
        "referral_message": referral_message(risk_level, labels),
        "can_continue_symbolic_support": risk_level in {"green", "yellow"},
        "hazard_labels": labels,
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
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
    parser.add_argument("--text", help="User ritual request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()
    try:
        result = check(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
