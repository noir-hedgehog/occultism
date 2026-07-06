#!/usr/bin/env python3
"""Reframe fear-escalating folk taboo claims into safe cultural explanations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


TABOO_PATTERNS = {
    "筷子插饭": ("chopsticks_in_rice", "餐桌礼仪、祭祀联想、尊重他人感受"),
    "夜里吹口哨": ("night_whistling", "夜间安静、儿童规训、邻里边界"),
    "正月剪发": ("first_month_haircut", "谐音禁忌、岁首避忌、地方差异"),
    "孕妇禁忌": ("pregnancy_taboo", "保护性规训、家庭焦虑、孕期照护边界"),
    "搬家择日": ("moving_date", "空间转换、时间仪式、家庭安定"),
    "中元禁忌": ("ghost_festival_taboo", "祭祖叙事、夜间谨慎、地方差异"),
}

TABOO_ALIASES = {
    "插筷子": "筷子插饭",
    "筷子插米饭": "筷子插饭",
    "吹口哨": "夜里吹口哨",
    "晚上吹口哨": "夜里吹口哨",
    "正月理发": "正月剪发",
    "剪头发": "正月剪发",
    "怀孕禁忌": "孕妇禁忌",
    "孕期禁忌": "孕妇禁忌",
    "乔迁择日": "搬家择日",
    "入宅择日": "搬家择日",
    "鬼节禁忌": "中元禁忌",
    "七月半禁忌": "中元禁忌",
}

FEAR_PATTERNS = {
    "deterministic_disaster_claim": ("一定倒霉", "必倒霉", "会出事", "必出事", "招灾", "报应", "害家人", "克家人"),
    "supernatural_confirmation": ("招鬼", "有鬼", "冲撞", "不干净", "邪祟", "鬼跟着", "被诅咒"),
    "coercive_family_pressure": ("必须照做", "不照做", "家里逼", "长辈逼", "不听就"),
    "professional_replacement": ("不用看医生", "不用去医院", "不用报警", "不用律师", "不用消防", "不用检查"),
    "dangerous_ritual": ("密闭烧", "烧纸", "点火", "放血", "喝符水", "刀", "割", "吞"),
}

VULNERABLE_CONTEXTS = {
    "pregnancy": ("孕妇", "怀孕", "孕期", "胎儿", "流产", "宝宝会不会"),
    "infant_or_child": ("婴儿", "新生儿", "小孩", "孩子", "宝宝"),
    "illness": ("生病", "病", "发烧", "失眠", "幻听", "幻视"),
    "travel_or_fire_safety": ("出行", "开车", "交通", "燃气", "电路", "火", "烟"),
}

SOURCE_TYPES = {
    "family": "家庭习惯",
    "regional": "地方口述",
    "religious": "宗教或庙宇语境",
    "internet": "网络传闻",
    "commercial": "商业课程或营销说法",
    "unknown": "来源未明",
}


def contains_any(text: str, values: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def normalize_source(raw: object) -> str:
    text = str(raw or "").strip()
    aliases = {
        "家人": "family",
        "家庭": "family",
        "长辈": "family",
        "地方": "regional",
        "地区": "regional",
        "本地": "regional",
        "宗教": "religious",
        "寺庙": "religious",
        "庙里": "religious",
        "网络": "internet",
        "网上": "internet",
        "短视频": "internet",
        "商业": "commercial",
        "课程": "commercial",
        "unknown": "unknown",
    }
    if text in SOURCE_TYPES:
        return text
    return aliases.get(text, "unknown")


def detect_taboo(text: str, explicit: object = "") -> tuple[str, str, str]:
    raw = str(explicit or "").strip()
    query = TABOO_ALIASES.get(raw, raw)
    if query in TABOO_PATTERNS:
        code, frame = TABOO_PATTERNS[query]
        return query, code, frame
    for name, item in TABOO_PATTERNS.items():
        if name in text:
            return name, item[0], item[1]
    for alias, name in TABOO_ALIASES.items():
        if alias in text:
            item = TABOO_PATTERNS[name]
            return name, item[0], item[1]
    return "unknown_taboo", "unknown", "来源、地区、礼仪、现实安全和家庭沟通"


def detect_flags(text: str, rules: dict[str, tuple[str, ...]]) -> list[str]:
    return [flag for flag, patterns in rules.items() if contains_any(text, patterns)]


def classify_fear_level(risk_flags: list[str], context_flags: list[str]) -> str:
    if "dangerous_ritual" in risk_flags or "professional_replacement" in risk_flags:
        return "high"
    if "supernatural_confirmation" in risk_flags or "deterministic_disaster_claim" in risk_flags:
        return "medium_high" if context_flags else "medium"
    if "coercive_family_pressure" in risk_flags:
        return "medium"
    return "low"


def reframe(payload: dict[str, Any]) -> dict[str, Any]:
    request_text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not request_text:
        raise ValueError("request_text or text is required")
    source_type = normalize_source(payload.get("source_type", payload.get("source", "")))
    region = str(payload.get("region", "")).strip()
    taboo_name, taboo_code, cultural_frame = detect_taboo(request_text, payload.get("taboo", ""))
    risk_flags = detect_flags(request_text, FEAR_PATTERNS)
    context_flags = detect_flags(request_text, VULNERABLE_CONTEXTS)
    fear_level = classify_fear_level(risk_flags, context_flags)

    can_reframe = "dangerous_ritual" not in risk_flags and "professional_replacement" not in risk_flags
    warnings = [
        "不得把民俗禁忌写成必然灾祸、鬼神确认、诅咒证明或惩罚机制。",
        "禁忌可解释为礼仪、地方习惯、家庭沟通、卫生安全或情绪安定线索。",
    ]
    if source_type in {"internet", "commercial", "unknown"}:
        warnings.append("来源不明、网络传闻或商业说法必须标注为未验证，不升级成地方传统。")
    if context_flags:
        warnings.append("涉及孕期、儿童、疾病或交通/消防时，现实照护和专业支持优先。")
    if not can_reframe:
        warnings.append("含危险仪式或专业替代表述时，先暂停民俗解释并转安全/专业支持。")

    response_layers = [
        {
            "layer": "source_boundary",
            "prompt": f"把来源标为{SOURCE_TYPES[source_type]}，地区为{region or '未提供'}；不要冒充地方或宗教权威。",
        },
        {
            "layer": "cultural_symbolism",
            "prompt": f"把「{taboo_name}」解释为{cultural_frame}，使用“某些家庭/地区会这样理解”的措辞。",
        },
        {
            "layer": "real_world_safety",
            "prompt": "检查是否涉及明火、烟雾、孕期、儿童、疾病、交通、消防或心理恐惧，并先处理现实风险。",
        },
        {
            "layer": "low_risk_translation",
            "prompt": "把禁忌转成可选择的礼貌、安定或沟通做法，而不是必须执行的规则。",
        },
    ]

    return {
        "tool": "folk_taboo_reframer",
        "system": "chinese_folk_custom",
        "request_text": request_text,
        "taboo_name": taboo_name,
        "taboo_code": taboo_code,
        "source_type": source_type,
        "region": region,
        "risk_flags": risk_flags,
        "context_flags": context_flags,
        "fear_level": fear_level,
        "can_reframe_taboo": can_reframe,
        "reframed_question": build_reframed_question(taboo_name, risk_flags),
        "response_layers": response_layers,
        "family_safe_wording": build_family_wording(taboo_name, source_type),
        "grounding_steps": build_grounding_steps(context_flags),
        "warnings": warnings,
        "next_steps": [
            "confirm_source_region_and_user_goal",
            "lookup_related_custom_with_folk_custom_lookup_if_needed",
            "route_dangerous_ritual_or_professional_replacement_before_explaining",
            "draft_non_fearful_cultural_explanation",
            "lint_final_output_with_mystic_output_lint",
        ],
        "limits": [
            "不确认鬼神、冲撞、诅咒、犯忌必灾或灵异因果。",
            "不提供危险仪式步骤，不用禁忌替代医疗、法律、消防、交通或心理健康支持。",
            "尊重家庭和地方习惯，但保留用户的现实安全、自主选择和低风险替代空间。",
        ],
    }


def build_reframed_question(taboo_name: str, risk_flags: list[str]) -> str:
    if taboo_name == "unknown_taboo":
        base = "这个禁忌说法可以如何从来源、文化含义和现实安全角度理解？"
    else:
        base = f"「{taboo_name}」这个说法可以如何从文化来源、礼仪含义和现实安全角度理解？"
    if risk_flags:
        return base + " 先不采用必然灾祸或鬼神确认的说法。"
    return base


def build_family_wording(taboo_name: str, source_type: str) -> str:
    if taboo_name == "unknown_taboo":
        subject = "这个说法"
    else:
        subject = f"「{taboo_name}」"
    source = SOURCE_TYPES[source_type]
    return f"可以说：我尊重{source}里的{subject}，我们先用不恐吓、低风险的方式保留礼貌和安定感。"


def build_grounding_steps(context_flags: list[str]) -> list[str]:
    steps = ["把“会不会出事”改成“我现在能做哪些现实检查和安定动作”。", "确认没有明火、烟雾、身体不适、交通或照护风险。"]
    if "pregnancy" in context_flags:
        steps.append("孕期相关担忧优先问医生或照护者，不用禁忌替代医疗判断。")
    if "infant_or_child" in context_flags:
        steps.append("儿童照护优先安全、睡眠、饮食和监护，不给孩子贴犯忌标签。")
    if "illness" in context_flags:
        steps.append("身体或精神健康症状优先现实求助，不把症状解释成犯忌。")
    return steps


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["request_text"] = args.text
    if args.taboo:
        payload["taboo"] = args.taboo
    if args.source_type:
        payload["source_type"] = args.source_type
    if args.region:
        payload["region"] = args.region
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
    parser.add_argument("--text", help="Fear-escalating taboo claim.")
    parser.add_argument("--taboo", help="Optional canonical taboo name.")
    parser.add_argument("--source-type", help="family, regional, religious, internet, commercial, unknown.")
    parser.add_argument("--region", help="Optional region or family context.")
    parser.add_argument("--json", help="JSON input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = reframe(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
