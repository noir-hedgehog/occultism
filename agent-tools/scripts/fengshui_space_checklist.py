#!/usr/bin/env python3
"""Generate a practical feng shui space-audit checklist."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ChecklistItem:
    item_id: str
    category: str
    prompt: str
    traditional_terms: tuple[str, ...]
    practical_reason: str
    low_risk_adjustments: tuple[str, ...]


COMMON_ITEMS = (
    ChecklistItem(
        "entrance_clear",
        "入口",
        "入口是否明亮、干净、能顺畅开门，鞋包杂物是否堵住动线？",
        ("气口", "明堂", "堵"),
        "入口决定进出体验；拥堵和昏暗会增加压迫感和拖延清理成本。",
        ("清理门后杂物", "补充柔和照明", "保留一条完整进出动线"),
    ),
    ChecklistItem(
        "light_air",
        "光线与通风",
        "空间是否长期阴暗、闷、潮、有异味或空气不流动？",
        ("气", "阴", "滞"),
        "光线、通风、潮湿和异味会直接影响睡眠、注意力和安全感。",
        ("每天短时通风", "检查霉菌和异味源", "增加局部照明"),
    ),
    ChecklistItem(
        "clutter_flow",
        "收纳与动线",
        "地面、桌面、床边或过道是否堆积杂物，行走是否需要绕行？",
        ("堵", "乱", "滞"),
        "杂物会增加视觉负荷，也容易造成绊倒和注意力分散。",
        ("先清一条主动线", "把高频物品固定归位", "移走破损和不用物"),
    ),
    ChecklistItem(
        "sharp_pressure",
        "冲与压",
        "是否有尖角、梁、柜角、强光、镜面或门路直冲休息/工作位置？",
        ("冲", "尖角", "压"),
        "直冲和压迫感常对应视觉干扰、身体紧张或长期不适。",
        ("调整座位/床位角度", "用软装弱化尖角", "避开梁下长期停留"),
    ),
)

SPACE_ITEMS = {
    "bedroom": (
        ChecklistItem(
            "bed_command",
            "床位",
            "床上是否能看见门但不与门直线相冲，床头是否稳定有靠？",
            ("床头有靠", "门冲", "安定"),
            "床位影响睡前警觉度、隐私感和休息稳定性。",
            ("床头靠实墙", "避开门正冲", "用床头柜或帘子增加稳定感"),
        ),
        ChecklistItem(
            "bed_reflection",
            "镜面与屏幕",
            "镜子、屏幕或反光物是否正对床，睡前是否容易被光线或通知打扰？",
            ("镜冲", "扰动"),
            "反光和通知会提高警觉，影响入睡和夜间醒来体验。",
            ("睡前遮挡镜面", "移开屏幕", "设置勿扰和低亮度"),
        ),
    ),
    "office": (
        ChecklistItem(
            "desk_support",
            "桌位",
            "坐下时背后是否有稳定支撑，是否长期背对门或被门路打断？",
            ("背后有靠", "门冲", "靠山"),
            "背后无靠和频繁被打断会增加警觉和注意力切换。",
            ("椅背靠墙或柜", "调整桌面方向", "用屏风/植物降低干扰"),
        ),
        ChecklistItem(
            "desk_focus",
            "专注区",
            "桌面是否只保留当前任务需要的物品，线缆和文件是否过载？",
            ("聚气", "散"),
            "过载桌面会增加认知负担，降低启动任务的速度。",
            ("清出一块空白工作面", "线缆收束", "文件分为待办/归档"),
        ),
    ),
    "living_room": (
        ChecklistItem(
            "seating_gathering",
            "会客区",
            "沙发座位是否有靠、能自然交流，主通道是否穿过谈话中心？",
            ("藏风聚气", "有靠", "穿堂"),
            "座位与动线影响交流舒适度和家庭成员停留意愿。",
            ("让座位有稳定背靠", "保留通道但避开谈话中心", "增加暖光局部照明"),
        ),
    ),
    "kitchen": (
        ChecklistItem(
            "stove_safety",
            "灶台",
            "灶台附近是否通风、安全，易燃物、水渍和杂物是否靠近火源？",
            ("灶", "水火", "洁净"),
            "厨房优先是现实安全问题，火源、油污和通风必须先处理。",
            ("移开易燃物", "清理油污", "检查燃气和通风"),
        ),
    ),
    "shop": (
        ChecklistItem(
            "customer_entry",
            "店铺入口",
            "顾客进门是否能快速理解动线、主商品和收银位置？",
            ("气口", "明堂", "聚气"),
            "入口清晰度影响停留、浏览和购买路径。",
            ("清出入口视线", "把主商品放在易见位置", "减少入口阻挡物"),
        ),
        ChecklistItem(
            "cashier_position",
            "收银/主位",
            "收银或主工作位是否有靠、能看见入口，是否暴露在拥挤通道中？",
            ("财位", "靠山", "守气"),
            "主位稳定和入口可见能降低打断和安全压力。",
            ("让主位背后稳定", "避免正冲通道", "保持收银区整洁"),
        ),
    ),
}

SPACE_ALIASES = {
    "bedroom": ("bedroom", "卧室", "睡房", "床"),
    "office": ("office", "办公室", "书房", "工位", "桌", "办公桌"),
    "living_room": ("living_room", "客厅", "起居室", "沙发"),
    "kitchen": ("kitchen", "厨房", "灶", "灶台"),
    "shop": ("shop", "店铺", "门店", "店", "收银"),
    "entrance": ("entrance", "玄关", "入口", "大门", "门口"),
}

CONCERN_ALIASES = {
    "sleep": ("睡眠", "失眠", "睡不好", "休息", "噩梦"),
    "focus": ("专注", "效率", "工作", "学习", "拖延"),
    "relationship": ("关系", "争吵", "家庭", "伴侣", "沟通"),
    "money": ("财运", "生意", "收入", "钱", "客流", "业绩"),
    "pressure": ("压抑", "不舒服", "焦虑", "堵", "闷"),
    "safety": ("燃气", "电路", "霉菌", "漏水", "异味", "噪音", "危险"),
}

SAFETY_KEYWORDS = {
    "gas_or_fire": ("燃气", "煤气", "明火", "烧焦", "火花", "漏气"),
    "mold_or_air": ("霉菌", "发霉", "潮湿", "异味", "头晕", "闷"),
    "electrical": ("电路", "漏电", "插座", "电线", "跳闸"),
    "security": ("跟踪", "被威胁", "入室", "门锁", "监控"),
    "health_sleep": ("连续失眠", "幻听", "幻视", "严重焦虑"),
}


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_space_type(text: str, explicit: object = None) -> str:
    if explicit:
        raw = str(explicit).strip()
        for space_type, aliases in SPACE_ALIASES.items():
            if raw == space_type or contains_any(raw, aliases):
                return space_type
    for space_type, aliases in SPACE_ALIASES.items():
        if contains_any(text, aliases):
            return space_type
    return "general"


def detect_concerns(text: str, explicit: object = None) -> list[str]:
    combined = text
    if isinstance(explicit, list):
        combined += " " + " ".join(str(item) for item in explicit)
    elif explicit:
        combined += " " + str(explicit)
    concerns = [concern for concern, aliases in CONCERN_ALIASES.items() if contains_any(combined, aliases)]
    return concerns or ["general"]


def detect_safety_flags(text: str) -> list[str]:
    return [flag for flag, aliases in SAFETY_KEYWORDS.items() if contains_any(text, aliases)]


def item_to_dict(item: ChecklistItem, priority: str) -> dict[str, object]:
    return {
        "item_id": item.item_id,
        "category": item.category,
        "priority": priority,
        "prompt": item.prompt,
        "traditional_terms": list(item.traditional_terms),
        "practical_reason": item.practical_reason,
        "low_risk_adjustments": list(item.low_risk_adjustments),
    }


def priority_for(item: ChecklistItem, concerns: list[str], safety_flags: list[str]) -> str:
    text = " ".join((item.item_id, item.category, item.prompt, item.practical_reason))
    if safety_flags and contains_any(text, ("燃气", "电路", "霉菌", "异味", "安全", "火源")):
        return "high"
    if "sleep" in concerns and contains_any(text, ("床", "睡", "镜", "光线", "噪音")):
        return "high"
    if "focus" in concerns and contains_any(text, ("桌", "专注", "工作", "动线")):
        return "high"
    if "money" in concerns and contains_any(text, ("入口", "店", "收银", "主商品")):
        return "high"
    if "pressure" in concerns and contains_any(text, ("堵", "压", "冲", "暗", "通风")):
        return "high"
    return "medium"


def build_checklist(payload: dict[str, object]) -> dict[str, object]:
    request_text = str(payload.get("request_text", "")).strip()
    description = str(payload.get("space_description", "")).strip()
    combined_text = " ".join(part for part in (request_text, description) if part)
    if not combined_text:
        raise ValueError("request_text or space_description is required")

    space_type = detect_space_type(combined_text, payload.get("space_type"))
    concerns = detect_concerns(combined_text, payload.get("concerns"))
    safety_flags = detect_safety_flags(combined_text)

    items = list(COMMON_ITEMS)
    if space_type in SPACE_ITEMS:
        items.extend(SPACE_ITEMS[space_type])
    elif space_type == "entrance":
        items = [item for item in items if item.category in {"入口", "光线与通风", "收纳与动线"}]

    checklist = [item_to_dict(item, priority_for(item, concerns, safety_flags)) for item in items]
    checklist.sort(key=lambda item: 0 if item["priority"] == "high" else 1)

    safety_notes = [
        "风水审视不能替代房屋安全、医疗、法律或安保判断。",
        "所有建议优先选择低成本、可逆、非危险的调整。",
    ]
    if safety_flags:
        safety_notes.insert(0, "先处理现实安全信号：燃气、电路、霉菌、异味、门锁、人身安全或严重睡眠/精神状态。")

    return {
        "space_type": space_type,
        "concerns": concerns,
        "safety_flags": safety_flags,
        "can_continue_fengshui": not safety_flags,
        "checklist": checklist,
        "safety_notes": safety_notes,
        "output_sections": [
            "空间类型",
            "主要困扰",
            "现实安全检查",
            "形法观察",
            "传统术语解释",
            "低风险调整",
            "限制与提醒",
        ],
        "next_steps": [
            "run_mystic_intake_triage_first",
            "ask_for_missing_layout_details_or_images",
            "answer_with_practical_observation_before_traditional_terms",
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
        return {"space_description": raw}
    if args.text:
        return {"request_text": args.text, "space_type": args.space_type}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"space_description": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Space request or description.")
    parser.add_argument("--space-type", help="Optional explicit space type.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to text or JSON input.")
    args = parser.parse_args()
    try:
        result = build_checklist(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

