#!/usr/bin/env python3
"""Guard animal-omen and bird/insect sign requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "animal_omen_symbolic_consultation": ("动物征兆", "动物预兆", "鸟兽征兆", "鸟飞进", "飞进阳台", "鸟进屋", "鸟撞窗", "猫头鹰叫", "乌鸦叫", "蛇进屋", "蜘蛛", "蝴蝶", "飞蛾", "虫子", "animal omen", "bird omen", "insect omen"),
    "observation_record": ("看到", "出现", "进屋", "撞窗", "叫", "停在", "飞进", "爬进", "反复出现"),
    "cultural_learning": ("来源", "文化", "民俗", "讲讲", "是什么意思", "象征", "寓意"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用报警", "不用物业", "不用疾控", "不用兽医", "只靠预兆"),
    "animal_harm": ("打死", "毒死", "烧死", "杀掉", "虐待", "活埋", "放血", "祭祀动物", "抓来做法"),
    "public_health_or_pest": ("咬伤", "抓伤", "蝙蝠", "老鼠", "鼠患", "虫害", "跳蚤", "蜱虫", "蟑螂", "蜂窝", "马蜂窝", "狂犬", "传染病", "寄生虫"),
    "dangerous_handling": ("徒手抓", "自己抓蛇", "抓蝙蝠", "抓马蜂", "靠近野生动物", "喂野生动物", "带回家养"),
    "deterministic_disaster": ("一定有灾", "必有大祸", "必死", "家人会出事", "血光之灾", "死亡预兆", "厄运注定"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "下注", "投资", "币圈", "发财", "暴富"),
    "third_party_privacy_or_coercion": ("他会不会回来", "她会不会回来", "控制", "操控", "报复", "第三者", "真实想法"),
    "spirit_fear_claim": ("鬼", "邪灵", "附身", "诅咒", "中邪", "被害", "驱邪", "挡灾"),
    "repeated_dependency": ("每天等征兆", "反复看预兆", "看到满意", "停不下来", "不敢出门", "一直查征兆"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "animal_omen_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "animal_harm" in flags:
        return "不把动物征兆解释成伤害动物、捕捉动物或祭祀动物的理由；先选择不伤害、可求助的现实处理方式。"
    if "public_health_or_pest" in flags or "dangerous_handling" in flags:
        return "涉及咬伤、虫害、蝙蝠、蛇、蜂窝、鼠患或野生动物时，先按现实安全和公共卫生流程处理，不继续做预兆判断。"
    if "professional_replacement" in flags:
        return "动物征兆不能替代医疗、安全、物业、疾控、兽医或紧急支持；先处理现实风险。"
    if "deterministic_disaster" in flags or "spirit_fear_claim" in flags:
        return "不确认灾祸、诅咒、邪灵或死亡预兆；可改成民俗象征、环境观察和安定行动。"
    if "financial_or_gambling" in flags:
        return "不把动物出现当作投资、赌博、彩票或发财信号；财务决策必须回到现实信息和风险控制。"
    if "third_party_privacy_or_coercion" in flags:
        return "不使用征兆读取第三方真实想法或操控关系；可改成自己的边界、沟通和选择。"
    if "repeated_dependency" in flags:
        return "暂停反复寻找征兆以获得确定感；先限制查询次数，并加入现实验证和情绪安定步骤。"
    return "可以把动物征兆作为民俗文化、观察记录和低风险象征反思，不作为事实证明、灾祸预言或行动命令。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "animal_omen_request_guard",
        "request_text": text,
        "system": "animal_omen_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_animal_omen": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "动物征兆、鸟兽虫鱼预兆和民俗象征只作文化学习、观察整理和低风险反思，不证明灾祸、鬼神、死亡或未来事实。",
            "不替代医疗、公共卫生、物业、消防、动物救助、兽医、法律、安全或紧急支持。",
            "不鼓励伤害、捕捉、投喂或危险接触动物，不提供驱邪、祭祀动物、赌博投资、第三方读心或操控建议。",
        ],
        "clarifying_questions": [
            "用户是想学习民俗象征、记录一次动物观察，还是做低风险反思？",
            "看到的动物、时间、地点、行为、出现次数和现实环境是什么？",
            "是否涉及咬伤、虫害、蜂窝、蝙蝠/蛇/鼠患、动物受伤、危险接触、灾祸恐惧、投资赌博或反复依赖？",
        ],
        "next_steps": [
            "record_animal_omen_observation",
            "lookup_animal_omen_symbol",
            "build_animal_omen_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_animal_omen_consultation", "reframe_to_real_world_safety"],
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
    parser.add_argument("--text", help="Animal-omen request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_animal_omen"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
