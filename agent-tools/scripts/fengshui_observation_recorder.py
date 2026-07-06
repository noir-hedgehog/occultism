#!/usr/bin/env python3
"""Record observable feng shui space facts before interpretation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    label: str
    keywords: tuple[str, ...]


SPACE_RULES = (
    Rule("bedroom", ("卧室", "睡房", "床", "床头", "衣柜")),
    Rule("office", ("办公室", "书房", "工位", "办公桌", "电脑桌", "会议室")),
    Rule("living_room", ("客厅", "沙发", "电视", "茶几", "起居室")),
    Rule("kitchen", ("厨房", "灶", "灶台", "水槽", "冰箱")),
    Rule("entrance", ("玄关", "入口", "大门", "门口", "鞋柜")),
    Rule("shop", ("店铺", "门店", "收银", "货架", "客流")),
)

ZONE_RULES = (
    Rule("entrance", ("门", "入口", "玄关", "门口", "大门")),
    Rule("window", ("窗", "窗户", "阳台", "采光")),
    Rule("rest_position", ("床", "床头", "床尾", "枕", "卧室")),
    Rule("work_position", ("桌", "书桌", "办公桌", "工位", "椅")),
    Rule("stove_or_sink", ("灶", "灶台", "水槽", "厨房", "冰箱")),
    Rule("storage", ("柜", "衣柜", "鞋柜", "杂物", "收纳", "箱子")),
    Rule("pathway", ("过道", "通道", "走廊", "动线", "路")),
)

OBSERVATION_RULES = (
    Rule("blocked_path", ("堵", "挡", "杂物", "堆", "绕行", "打不开", "拥挤")),
    Rule("low_light", ("暗", "昏暗", "采光差", "没光", "阴暗")),
    Rule("poor_air", ("闷", "不通风", "潮", "潮湿", "异味", "霉")),
    Rule("direct_alignment", ("正对", "一条线", "直冲", "对着", "门冲")),
    Rule("overhead_pressure", ("梁", "压", "低矮", "吊柜", "压迫")),
    Rule("sharp_or_reflective", ("尖角", "柜角", "镜", "反光", "屏幕")),
    Rule("unsupported_back", ("背对门", "背后空", "背后无靠", "没有靠")),
    Rule("noise_or_disruption", ("吵", "噪音", "打扰", "通知", "路冲")),
)

SAFETY_RULES = (
    Rule("gas_or_fire", ("燃气", "煤气", "漏气", "明火", "火花", "烧焦", "易燃")),
    Rule("electrical", ("电线", "插座", "漏电", "跳闸", "电路", "火花")),
    Rule("mold_or_air", ("霉菌", "发霉", "潮湿", "异味", "头晕", "闷")),
    Rule("security", ("门锁", "被威胁", "跟踪", "入室", "监控")),
    Rule("health_sleep", ("连续失眠", "幻听", "幻视", "严重焦虑", "睡不着很多天")),
)

INFERENCE_MARKERS = (
    "财位",
    "破财",
    "招灾",
    "有鬼",
    "中邪",
    "煞气很重",
    "一定",
    "必然",
    "克",
)


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def matched_labels(text: str, rules: Iterable[Rule]) -> list[str]:
    return [rule.label for rule in rules if contains_any(text, rule.keywords)]


def split_observation_text(text: str) -> list[str]:
    chunks = re.split(r"[。！？!?；;\n]+", text)
    return [chunk.strip(" ，,、") for chunk in chunks if chunk.strip(" ，,、")]


def detect_space_type(text: str, explicit: object = None) -> str:
    if explicit:
        raw = str(explicit).strip()
        for rule in SPACE_RULES:
            if raw == rule.label or contains_any(raw, rule.keywords):
                return rule.label
    for rule in SPACE_RULES:
        if contains_any(text, rule.keywords):
            return rule.label
    return "general"


def confidence_for(text: str) -> str:
    if contains_any(text, ("照片", "图里", "看见", "显示", "可见", "标注")):
        return "observed"
    if contains_any(text, ("感觉", "好像", "可能", "应该", "似乎")):
        return "reported"
    return "reported"


def traditional_terms_for(flags: list[str], zones: list[str]) -> list[str]:
    terms: set[str] = set()
    if "blocked_path" in flags or "entrance" in zones:
        terms.update(("气口", "明堂", "堵"))
    if "direct_alignment" in flags:
        terms.add("冲")
    if "overhead_pressure" in flags:
        terms.add("压")
    if "unsupported_back" in flags:
        terms.add("靠")
    if "poor_air" in flags or "low_light" in flags:
        terms.update(("气滞", "阴"))
    if "sharp_or_reflective" in flags:
        terms.update(("尖角", "镜冲"))
    return sorted(terms)


def practical_mapping_for(flags: list[str]) -> list[str]:
    mapping: list[str] = []
    if "blocked_path" in flags:
        mapping.append("动线受阻或收纳压力较高")
    if "low_light" in flags:
        mapping.append("光线不足可能影响安全感、清洁意愿和注意力")
    if "poor_air" in flags:
        mapping.append("通风、潮湿或异味需要先做现实检查")
    if "direct_alignment" in flags:
        mapping.append("门窗、床桌或通道直线关系可能带来干扰感")
    if "overhead_pressure" in flags:
        mapping.append("上方梁柜或低矮结构可能增加压迫感")
    if "sharp_or_reflective" in flags:
        mapping.append("尖角、镜面或屏幕反光可能造成视觉干扰")
    if "unsupported_back" in flags:
        mapping.append("背后缺少支撑可能增加警觉和分心")
    if "noise_or_disruption" in flags:
        mapping.append("噪音或频繁打扰会影响休息和专注")
    return mapping or ["需要补充更多可见事实后再映射现实体验"]


def build_observations(text: str) -> list[dict[str, object]]:
    observations: list[dict[str, object]] = []
    for index, chunk in enumerate(split_observation_text(text), start=1):
        zones = matched_labels(chunk, ZONE_RULES)
        flags = matched_labels(chunk, OBSERVATION_RULES)
        if not zones and not flags:
            continue
        observations.append(
            {
                "id": f"obs_{index}",
                "source_text": chunk,
                "confidence": confidence_for(chunk),
                "zones": zones or ["general"],
                "observable_features": flags or ["general_layout"],
                "traditional_terms_candidate": traditional_terms_for(flags, zones),
                "practical_mapping": practical_mapping_for(flags),
            }
        )
    return observations


def missing_details(space_type: str, observations: list[dict[str, object]], text: str) -> list[str]:
    zones = {zone for observation in observations for zone in observation["zones"]}
    missing: list[str] = []
    if space_type == "general":
        missing.append("space_type")
    if "entrance" not in zones:
        missing.append("entrance_or_door_position")
    if space_type == "bedroom" and "rest_position" not in zones:
        missing.append("bed_position")
    if space_type == "office" and "work_position" not in zones:
        missing.append("desk_position")
    if space_type == "kitchen" and "stove_or_sink" not in zones:
        missing.append("stove_and_sink_position")
    if not contains_any(text, ("窗", "采光", "光", "通风", "阳台")):
        missing.append("light_and_air")
    if not observations:
        missing.append("observable_facts")
    return missing


def interpretation_queue(observations: list[dict[str, object]]) -> list[dict[str, object]]:
    queued: list[dict[str, object]] = []
    for observation in observations:
        terms = observation["traditional_terms_candidate"]
        if not terms:
            continue
        queued.append(
            {
                "observation_id": observation["id"],
                "traditional_terms": terms,
                "must_explain_after_fact": True,
            }
        )
    return queued


def record(payload: dict[str, object]) -> dict[str, object]:
    text = str(payload.get("observation_text", payload.get("space_description", payload.get("request_text", "")))).strip()
    if not text:
        raise ValueError("observation_text, space_description, or request_text is required")

    space_type = detect_space_type(text, payload.get("space_type"))
    observations = build_observations(text)
    safety_flags = matched_labels(text, SAFETY_RULES)
    inferred_claims = [marker for marker in INFERENCE_MARKERS if marker in text]
    missing = missing_details(space_type, observations, text)

    return {
        "space_type": space_type,
        "input_mode": str(payload.get("input_mode", "text_description")),
        "observations": observations,
        "safety_flags": safety_flags,
        "inferred_claims_to_avoid": inferred_claims,
        "missing_details": missing,
        "can_continue_fengshui": not safety_flags,
        "interpretation_queue": interpretation_queue(observations),
        "notes": [
            "先描述可见事实，再解释传统术语。",
            "不要从照片或描述直接断言灾祸、财富、婚姻、疾病或超自然原因。",
            "涉及燃气、电路、霉菌、门锁、人身安全或严重睡眠/精神状态时，先处理现实安全。",
        ],
        "next_steps": [
            "run_fengshui_space_checklist_with_recorded_observations",
            "ask_for_missing_details_if_needed",
            "rank_low_risk_adjustments_with_fengshui_recommendation_ranker",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"observation_text": raw}
    if args.text:
        return {"observation_text": args.text, "space_type": args.space_type, "input_mode": args.input_mode}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"observation_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Observable space description or image notes.")
    parser.add_argument("--space-type", help="Optional explicit space type.")
    parser.add_argument("--input-mode", default="text_description", help="text_description, image_notes, or mixed.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to text or JSON input.")
    args = parser.parse_args()
    try:
        result = record(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
