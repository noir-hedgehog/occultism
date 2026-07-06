#!/usr/bin/env python3
"""Map feng shui directions to safe Bagua observation prompts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable


BAGUA = {
    "north": {
        "names": ("北", "正北", "north"),
        "trigram": "坎",
        "element": "水",
        "themes": ("流动", "路径", "休息", "信息"),
        "practical_prompts": ("通风和湿气是否稳定", "是否有噪音、漏水或低温不适", "动线是否清楚"),
        "low_risk_adjustments": ("保持干燥通风", "整理通道和线缆", "用稳定照明降低阴暗感"),
    },
    "northeast": {
        "names": ("东北", "艮", "northeast"),
        "trigram": "艮",
        "element": "土",
        "themes": ("停止", "学习", "边界", "稳定"),
        "practical_prompts": ("是否堆积杂物", "是否适合安静学习或收纳", "角落是否潮湿或昏暗"),
        "low_risk_adjustments": ("清出一个稳定角落", "减少过量收纳", "补充柔和局部照明"),
    },
    "east": {
        "names": ("东", "正东", "震", "east"),
        "trigram": "震",
        "element": "木",
        "themes": ("启动", "生长", "家庭", "行动"),
        "practical_prompts": ("早晨光线是否舒适", "是否有启动一天的清晰动线", "是否被杂物阻挡"),
        "low_risk_adjustments": ("保持入口或窗边清爽", "放置常用物的固定位置", "减少起床/开工阻力"),
    },
    "southeast": {
        "names": ("东南", "巽", "southeast"),
        "trigram": "巽",
        "element": "木",
        "themes": ("资源", "流通", "渗透", "关系网络"),
        "practical_prompts": ("物品和空气是否流通", "是否堆放票据、杂物或过期物", "是否影响工作和资源管理"),
        "low_risk_adjustments": ("整理账单和文件", "保持窗边通风", "建立可持续收纳规则"),
    },
    "south": {
        "names": ("南", "正南", "离", "south"),
        "trigram": "离",
        "element": "火",
        "themes": ("可见度", "表达", "照明", "热度"),
        "practical_prompts": ("光线是否刺眼或过暗", "电子屏幕和热源是否过多", "展示区是否清晰"),
        "low_risk_adjustments": ("调整眩光和屏幕亮度", "移开易燃物", "用整洁展示替代堆叠"),
    },
    "southwest": {
        "names": ("西南", "坤", "southwest"),
        "trigram": "坤",
        "element": "土",
        "themes": ("照顾", "承载", "关系", "日常支持"),
        "practical_prompts": ("是否适合休息和交流", "是否承担过多杂物", "是否影响照护和家务动线"),
        "low_risk_adjustments": ("减少沉重堆放", "保留可坐可谈的区域", "把家务用品归位"),
    },
    "west": {
        "names": ("西", "正西", "兑", "west"),
        "trigram": "兑",
        "element": "金",
        "themes": ("表达", "收获", "愉悦", "完成"),
        "practical_prompts": ("是否适合放松或完成收尾", "是否有噪音或反光干扰", "物品是否易取易放"),
        "low_risk_adjustments": ("整理完成区", "降低反光和噪音", "给休闲物品固定位置"),
    },
    "northwest": {
        "names": ("西北", "乾", "northwest"),
        "trigram": "乾",
        "element": "金",
        "themes": ("规则", "支持", "长辈", "决策"),
        "practical_prompts": ("重要文件是否有序", "是否适合做计划和决策", "是否有压迫或尖角"),
        "low_risk_adjustments": ("整理证件和文件", "建立家庭/工作规则区", "弱化尖角和压迫感"),
    },
    "center": {
        "names": ("中心", "中宫", "中央", "center"),
        "trigram": "中",
        "element": "土",
        "themes": ("稳定", "整合", "动线核心", "承载"),
        "practical_prompts": ("中心动线是否被占用", "是否影响各区域连接", "是否积灰或堆放重物"),
        "low_risk_adjustments": ("清出中心通道", "减少大型杂物", "保持地面干净稳定"),
    },
}

CONCERN_HINTS = {
    "sleep": ("睡眠", "失眠", "睡不好", "休息", "噩梦"),
    "focus": ("专注", "工作", "学习", "效率", "拖延"),
    "relationship": ("关系", "伴侣", "家庭", "沟通", "争吵"),
    "resources": ("财运", "财务", "收入", "资源", "钱", "业绩", "客流"),
    "pressure": ("压抑", "堵", "不舒服", "焦虑", "闷"),
}

SAFETY_HINTS = {
    "gas_or_fire": ("燃气", "煤气", "明火", "火花", "烧焦", "易燃"),
    "electrical": ("插座", "电线", "漏电", "跳闸", "电路"),
    "mold_or_air": ("霉菌", "发霉", "潮湿", "异味", "头晕"),
    "security": ("被威胁", "跟踪", "门锁", "入室", "监控"),
}


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_direction(text: str, explicit: object = None) -> str:
    ordered = sorted(BAGUA.items(), key=lambda item: max(len(name) for name in item[1]["names"]), reverse=True)
    raw = str(explicit or "").strip()
    if raw:
        for direction, data in ordered:
            if raw == direction or contains_any(raw, data["names"]):
                return direction
    for direction, data in ordered:
        if contains_any(text, data["names"]):
            return direction
    return ""


def detect_concerns(text: str, explicit: object = None) -> list[str]:
    combined = text
    if isinstance(explicit, list):
        combined += " " + " ".join(str(item) for item in explicit)
    elif explicit:
        combined += " " + str(explicit)
    concerns = [concern for concern, keywords in CONCERN_HINTS.items() if contains_any(combined, keywords)]
    return concerns or ["general"]


def detect_safety(text: str) -> list[str]:
    return [flag for flag, keywords in SAFETY_HINTS.items() if contains_any(text, keywords)]


def concern_guidance(concerns: list[str]) -> list[str]:
    guidance = []
    if "sleep" in concerns:
        guidance.append("睡眠问题先看光线、噪音、温度、床边动线和睡前刺激。")
    if "focus" in concerns:
        guidance.append("专注问题先看桌面负荷、背后支撑、照明和打断来源。")
    if "relationship" in concerns:
        guidance.append("关系问题只映射为空间里的沟通舒适度和边界，不断言感情结果。")
    if "resources" in concerns:
        guidance.append("资源/财务感受只映射为文件、预算、入口和工作流整理，不预测财富。")
    if "pressure" in concerns:
        guidance.append("压迫感先看堵、暗、尖角、梁压、通风和杂物。")
    return guidance or ["先把方位象征落到可见事实：光线、通风、动线、收纳、噪音和安全。"]


def map_bagua(payload: dict[str, object]) -> dict[str, object]:
    request_text = str(payload.get("request_text", payload.get("space_description", ""))).strip()
    direction = detect_direction(request_text, payload.get("direction"))
    concerns = detect_concerns(request_text, payload.get("concerns"))
    safety_flags = detect_safety(request_text)
    missing_fields = []
    if not direction:
        missing_fields.append("direction")
    if not request_text and not payload.get("direction"):
        missing_fields.append("request_text_or_direction")

    data = BAGUA.get(direction)
    can_continue = bool(data) and not safety_flags
    result = {
        "request_text": request_text,
        "method": "compass_bagua_reference",
        "direction": direction,
        "direction_label": "unknown",
        "trigram": "",
        "element": "",
        "symbolic_themes": [],
        "concerns": concerns,
        "safety_flags": safety_flags,
        "can_continue_bagua_mapping": can_continue,
        "practical_observation_prompts": [],
        "low_risk_adjustments": [],
        "concern_guidance": concern_guidance(concerns),
        "missing_fields": missing_fields,
        "warnings": [],
        "limits": [
            "八卦方位映射只能作为传统象征和空间观察提示，不作为财富、疾病、婚姻或灾祸判断。",
            "不知道准确方位时，可以继续做形法审视，不要编造罗盘结果。",
            "任何燃气、电路、霉菌、安防或严重睡眠/精神状态问题必须先按现实安全处理。",
        ],
        "next_steps": [
            "run_fengshui_observation_recorder_for_visible_facts",
            "run_fengshui_space_checklist_for_shape_form_review",
            "rank_low_risk_adjustments_with_fengshui_recommendation_ranker",
            "lint_final_output_with_mystic_output_lint",
        ],
    }
    if not data:
        result["warnings"].append("未识别明确方位；请补充罗盘方位，或只做形法空间审视。")
        return result

    result.update(
        {
            "direction_label": data["names"][0],
            "trigram": data["trigram"],
            "element": data["element"],
            "symbolic_themes": list(data["themes"]),
            "practical_observation_prompts": list(data["practical_prompts"]),
            "low_risk_adjustments": list(data["low_risk_adjustments"]),
        }
    )
    if safety_flags:
        result["warnings"].append("检测到现实安全信号；先处理安全问题，再做八卦方位解释。")
    if "resources" in concerns:
        result["warnings"].append("资源/财务主题不得写成发财、破财或投资判断，只能转为收纳、预算和工作流建议。")
    return result


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, object] = {}
    if args.text:
        payload["request_text"] = args.text
    if args.direction:
        payload["direction"] = args.direction
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --direction, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Space description or feng shui direction request.")
    parser.add_argument("--direction", help="north, northeast, east, southeast, south, southwest, west, northwest, center.")
    parser.add_argument("--json", help="JSON input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = map_bagua(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
