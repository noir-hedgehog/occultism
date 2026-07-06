#!/usr/bin/env python3
"""Guard deity, ancestor, altar, offering, and vow-return requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "deity_ancestor_symbolic_consultation": ("神明", "祖先", "祖灵", "供奉", "供桌", "神台", "祭拜", "祭祖", "拜神", "拜拜", "上供", "供品", "altar", "offering", "ancestor", "deity"),
    "vow_or_return_thanks": ("许愿", "还愿", "愿望", "酬神", "谢神", "vow", "votive"),
    "memorial_reflection": ("纪念", "怀念", "家族", "祖辈", "清明", "中元", "忌日", "memorial"),
}

RISK_KEYWORDS = {
    "deity_command_or_threat": ("神明命令", "祖先命令", "必须照做", "不供就惩罚", "会降灾", "神罚", "托梦命令", "祖先生气"),
    "dangerous_ritual": ("放血", "血祭", "烧炭", "密闭烧", "密闭点香", "通宵点香", "烧房间", "喝香灰", "喝符水", "吃供品治病"),
    "professional_or_safety_replacement": ("不用医生", "不用报警", "不用律师", "不去医院", "治疗", "诊断", "用药", "官司", "投资", "股票", "彩票"),
    "coercion_or_relationship_control": ("让他回来", "让她回来", "拆散", "控制他", "让他离不开我", "惩罚对方", "报复"),
    "third_party_privacy_or_blame": ("谁害我", "谁冲撞", "谁冒犯神明", "查出小人", "祖先说他", "神明说她"),
    "expensive_ritual_pressure": ("天价法事", "必须请大师", "必须买", "越贵越灵", "开光套餐", "供奉套餐", "不花钱不灵"),
    "family_conflict_or_forced_worship": ("逼家人供奉", "强迫孩子拜", "家人不同意也要", "偷偷在别人家摆", "不拜就是不孝"),
    "repeated_dependency": ("每天问神明", "反复还愿", "停不下来", "不拜就害怕", "不拜就睡不着", "不供就睡不着", "每件事都问祖先"),
}

SAFE_NEGATED_PHRASES = (
    "不做危险仪式",
    "不强迫家人",
    "不买贵物",
    "不求神明命令",
    "不确认谁害我",
    "不替代医生",
    "不替代报警",
    "不操控别人",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "deity_ancestor_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "deity_command_or_threat" in flags:
        return "不确认神明、祖先、梦境或供桌现象给出命令、惩罚或灾祸预告；可改成文化象征、纪念和现实选择整理。"
    if "dangerous_ritual" in flags:
        return "不提供放血、密闭燃烧、通宵点香、摄入香灰符水或把供品当治疗的做法。"
    if "professional_or_safety_replacement" in flags:
        return "祭拜、供奉和还愿不能替代医疗、法律、报警、财务或安全支持。"
    if "coercion_or_relationship_control" in flags:
        return "不把神明/祖先供奉用于操控、惩罚、拆散或控制他人。"
    if "third_party_privacy_or_blame" in flags:
        return "不通过神明或祖先讯息指认谁害你、谁冒犯、谁是小人或读取第三方隐私。"
    if "expensive_ritual_pressure" in flags:
        return "不制造天价法事、开光套餐或供奉消费压力；优先低成本、可撤回、尊重来源的纪念动作。"
    if "family_conflict_or_forced_worship" in flags:
        return "不强迫家人、孩子或他人参与供奉；优先同意、尊重和家庭沟通边界。"
    if "repeated_dependency" in flags:
        return "如果反复祭拜、还愿或求确认已经带来恐惧和失眠，先暂停确认循环，做现实安定和支持连接。"
    return "可以把神明/祖先/供奉/还愿请求作为文化学习、纪念整理、感恩表达和低风险生活提醒。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "deity_ancestor_request_guard",
        "request_text": text,
        "system": "deity_ancestor_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_deity_ancestor": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "神明、祖先、供奉、祭拜和还愿只作文化学习、纪念整理、感恩表达和低风险生活提醒。",
            "不确认神明命令、祖先命令、托梦事实、灾祸惩罚、灵体事实或第三方隐私。",
            "不提供危险仪式、摄入供品/香灰/符水、专业替代、操控报复或强迫他人供奉。",
            "不制造高价法事、开光套餐、供奉消费或反复确认依赖。",
        ],
        "clarifying_questions": [
            "用户是想学习文化、整理供桌/纪念动作、表达感恩，还是处理许愿还愿焦虑？",
            "来源传统、对象、场景、已有物件、家庭同意边界、消防/食品/宠物儿童安全和复盘时间是什么？",
            "是否涉及神明/祖先命令、灾祸恐吓、危险仪式、专业替代、操控报复、强迫家人、高价法事或反复依赖？",
        ],
        "next_steps": [
            "record_deity_ancestor_context",
            "lookup_deity_ancestor_symbols",
            "build_deity_ancestor_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_deity_ancestor_consultation", "reframe_to_cultural_memorial_safety_or_professional_support"],
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
    parser.add_argument("--text", help="Deity or ancestor request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_deity_ancestor"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
