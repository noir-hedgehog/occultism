#!/usr/bin/env python3
"""Guard pet communication and animal-spirit message requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "pet_communication_symbolic_consultation": ("宠物沟通", "动物沟通", "宠物灵性", "动物灵性", "亡宠", "宠物讯息", "pet communication", "animal communication", "animal communicator"),
    "care_observation": ("猫", "狗", "宠物", "躲起来", "叫", "不吃", "陪伴", "照护", "观察"),
    "grief_reflection": ("想念", "离世", "去世", "怀念", "告别", "纪念"),
}

RISK_KEYWORDS = {
    "veterinary_emergency_or_replacement": ("不用兽医", "不用医院", "不去医院", "不看兽医", "呕吐", "抽搐", "呼吸困难", "流血", "中毒", "吃了药", "吃了巧克力", "治疗", "诊断", "用药"),
    "missing_pet_location_claim": ("走失", "丢了", "找回位置", "定位", "在哪个小区", "具体位置", "被谁抱走"),
    "guaranteed_message_or_truth": ("保证它说", "保证它没病", "一定是它说", "百分百", "真实想法", "准确读心", "它恨我", "它怪我"),
    "spirit_fact_claim": ("亡宠附身", "灵魂回来", "托梦证明", "灵体", "附体", "通灵证明"),
    "third_party_privacy_or_blame": ("判断是谁害它", "谁偷了它", "报复", "诅咒", "让它惩罚"),
    "expensive_purchase_pressure": ("必须付费", "天价沟通", "大师套餐", "买能量课", "越贵越准"),
    "repeated_dependency": ("每天问它", "反复确认", "停不下来", "每个行为都问", "不问就害怕"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "pet_communication_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "veterinary_emergency_or_replacement" in flags:
        return "宠物沟通不能替代兽医诊断、急症处理或用药建议；出现呕吐、抽搐、呼吸困难、中毒、流血等情况先联系兽医或急诊。"
    if "missing_pet_location_claim" in flags:
        return "不通过宠物沟通承诺定位走失宠物；应优先使用张贴寻宠、芯片/项圈信息、监控、邻里和救助站等现实搜索。"
    if "guaranteed_message_or_truth" in flags or "spirit_fact_claim" in flags:
        return "不确认宠物真实想法、亡宠灵魂、托梦证明或附身事实；可改成怀念、照护记录和情绪安放。"
    if "third_party_privacy_or_blame" in flags:
        return "不通过宠物沟通指认伤害者、偷窃者、报复对象或第三方隐私。"
    if "expensive_purchase_pressure" in flags:
        return "不制造付费沟通或高价课程压力；优先使用零成本观察记录和现实照护。"
    if "repeated_dependency" in flags:
        return "暂停反复读取宠物讯息以寻求确定感；把观察转成一次记录、一个照护动作和复盘时间。"
    return "可以把宠物沟通作为象征写作、行为观察、照护计划和哀伤安放，不替代兽医、不承诺真实讯息、不定位走失宠物。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "pet_communication_request_guard",
        "request_text": text,
        "system": "pet_communication_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_pet_communication": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "宠物沟通只作象征写作、观察记录、照护计划和哀伤安放，不确认宠物真实想法或灵体事实。",
            "不替代兽医诊断、急症处理、用药、走失宠物搜索或现实安全措施。",
            "不指认第三方、不制造高价付费压力、不强化反复读取依赖。",
        ],
        "clarifying_questions": [
            "用户是想记录宠物行为、做低风险象征反思，还是处理亡宠怀念？",
            "宠物种类、观察行为、时间背景、照护现状、兽医/现实安全背景、用户情绪和现实锚点是什么？",
            "是否涉及兽医替代、急症、走失定位、亡宠事实确认、第三方指认、付费压力或反复依赖？",
        ],
        "next_steps": [
            "record_pet_communication_context",
            "lookup_pet_communication_symbols",
            "build_pet_communication_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_pet_communication_consultation", "reframe_to_veterinary_or_real_world_support"],
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
    parser.add_argument("--text", help="Pet communication request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_pet_communication"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
