#!/usr/bin/env python3
"""Guard dowsing rod and divining rod symbolism requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "dowsing_symbolic_consultation": ("占杖", "寻水杖", "探测棒", "探测杆", "探矿杖", "dowsing", "dowsing rod", "dowsing rods", "divining rod", "l-rods", "radiesthesia"),
    "map_or_space_record": ("地图探测", "地图寻物", "空间探测", "场地探测", "map dowsing", "remote dowsing"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来源", "象征"),
}

RISK_KEYWORDS = {
    "utility_or_digging_safety": ("地下管线", "电缆", "燃气管", "水管", "挖开", "开挖", "钻孔", "施工", "打井", "挖井", "地下空洞"),
    "water_or_resource_guarantee": ("保证找到水", "找水源", "地下水", "矿脉", "油气", "宝藏", "埋藏物", "准确定位"),
    "medical_or_geopathic_claim": ("治病", "治疗", "地气病", "地磁病", "癌", "失眠", "焦虑", "辐射病", "诊断", "能量污染"),
    "professional_replacement": ("不用专业探测", "不用勘测", "不用医生", "不用报警", "不用律师", "不用物业", "不用工程师", "只信占杖"),
    "property_or_legal_decision": ("买房决定", "卖房决定", "签合同", "定地块", "迁坟", "风水官司", "邻里纠纷", "产权"),
    "trespass_or_privacy": ("偷偷进", "翻墙", "闯入", "别人家", "邻居家", "未经同意", "跟踪", "定位某人", "查他在哪"),
    "spirit_fear_or_exorcism": ("驱邪", "除灵", "鬼", "附身", "诅咒", "中邪", "邪气", "灵体"),
    "financial_or_purchase_pressure": ("稳赚", "投资", "彩票", "赌博", "贷款买", "高价占杖", "天价课程", "会员工具", "越贵越准"),
    "repeated_dependency": ("每天探到准", "反复探测", "停不下来", "一直找", "问到安心", "不探就害怕"),
}

SAFE_NEGATED_RISK_PHRASES = (
    "不挖",
    "不开挖",
    "不钻孔",
    "不施工",
    "不打井",
    "不保证找到水",
    "不找水源",
    "不找地下水",
    "不治疗",
    "不诊断",
    "不替代医生",
    "不替代专业探测",
    "不替代勘测",
    "不替代工程师",
    "不替代物业",
    "不替代报警",
    "不替代律师",
    "不买房决定",
    "不签合同",
    "不闯入",
    "不进别人家",
    "不定位某人",
    "不驱邪",
    "不除灵",
    "不投资",
    "不赌博",
    "不买彩票",
    "不高价购买",
    "不买课程",
    "不反复探",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def remove_safe_negations(text: str) -> str:
    cleaned = text
    for phrase in SAFE_NEGATED_RISK_PHRASES:
        cleaned = cleaned.replace(phrase, "")
    return cleaned


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "dowsing_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = remove_safe_negations(text)
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "utility_or_digging_safety" in flags or "professional_replacement" in flags:
        return "占杖不能替代地下管线探测、工程勘测、施工安全、医疗、法律或紧急支持；可改成室内路线观察和低风险空间反思。"
    if "water_or_resource_guarantee" in flags:
        return "不承诺找到水源、矿脉、宝藏或准确定位资源；可改成地图联想、现实核查清单和观察记录。"
    if "medical_or_geopathic_claim" in flags:
        return "不把占杖写成诊断、治疗、地气病或辐射病判断；身体和睡眠问题优先找专业支持。"
    if "property_or_legal_decision" in flags:
        return "不让占杖决定买卖房、合同、地块、迁坟或纠纷；可改成列出现实证据和需咨询的专业问题。"
    if "trespass_or_privacy" in flags:
        return "不协助闯入、跟踪、定位他人或未经同意探测私人空间；可改成本人授权空间内的低风险观察。"
    if "spirit_fear_or_exorcism" in flags:
        return "不把占杖写成驱邪、除灵或确认灵体；可改成空间安定感、边界和现实安全检查。"
    if "financial_or_purchase_pressure" in flags:
        return "不提供投资赌博、收益保证或高价工具课程压力；优先已有物件、低成本记录和不购买。"
    if "repeated_dependency" in flags:
        return "暂停反复探测直到安心的依赖模式；设定一次性观察、停止条件和现实复盘。"
    return "可以把占杖、寻水杖或探测棒作为文化象征、路线感和空间观察提示，不作为定位、勘测、医疗或决策工具。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "dowsing_request_guard",
        "request_text": text,
        "system": "dowsing_rod_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_dowsing": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "占杖、寻水杖、探测棒和 dowsing rods 只作为文化象征、路线感、空间观察和低风险反思，不证明地下资源、管线、疾病、灵体或事实位置。",
            "不替代地下管线探测、工程勘测、施工安全、医疗、法律、物业、报警、寻人或紧急支持。",
            "不协助开挖、打井、钻孔、闯入、跟踪、定位他人、投资赌博、房产合同决定、驱邪恐惧、高价购买或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录一次占杖观察，还是在本人授权空间内做低风险路线/空间反思？",
            "是否涉及地下管线、开挖打井、水源矿脉、医疗地气、房产合同、第三方隐私、驱邪恐惧、购买压力或反复依赖？",
            "观察对象、地点、授权范围、现实核查方式、停止条件和可低成本替代是什么？",
        ],
        "next_steps": [
            "record_dowsing_context",
            "lookup_dowsing_symbols",
            "build_dowsing_practice_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_dowsing_consultation", "reframe_to_safety_or_professional_support"],
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
    parser.add_argument("--text", help="Dowsing request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_dowsing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
