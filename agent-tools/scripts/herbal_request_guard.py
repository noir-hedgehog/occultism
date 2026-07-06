#!/usr/bin/env python3
"""Guard herbal, green witchcraft, and plant magic symbolism requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "herbal_symbolic_consultation": ("草本", "香草", "草药", "药草", "植物魔法", "绿巫", "草药魔法", "herbal", "herb magic", "green witchcraft"),
    "plant_bundle_record": ("草本包", "香草束", "药草包", "草药包", "草药袋", "植物包", "herbal bundle", "herb bundle", "spell jar"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来源", "象征"),
}

RISK_KEYWORDS = {
    "medical_or_mental_health_claim": ("治病", "治疗", "疗愈疾病", "抗癌", "消炎", "抗病毒", "止痛", "抑郁", "焦虑", "失眠", "诊断", "用药", "停药"),
    "ingestion_or_topical_use": ("喝草药", "泡水喝", "煮水喝", "内服", "吃下去", "吞服", "药浴", "敷伤口", "涂伤口", "外敷", "滴眼睛", "私处"),
    "pregnancy_baby_pet_allergy": ("孕妇", "怀孕", "备孕", "婴儿", "宝宝", "儿童", "猫", "狗", "宠物", "哮喘", "过敏", "癫痫"),
    "foraging_or_poisoning_risk": ("野外采", "自己采", "采野草", "路边摘", "毒草", "蘑菇", "不认识的植物", "分辨毒性", "可不可以吃"),
    "fire_smoke_or_mold_safety": ("点燃", "焚烧", "烟熏", "密闭烧", "整夜烧", "无人看管", "发霉", "霉味", "潮湿草药"),
    "professional_replacement": ("不用医生", "不用看医生", "不用心理咨询", "不用报警", "不用吃药", "全靠草药"),
    "spirit_fear_or_exorcism": ("驱邪", "除灵", "赶鬼", "附身", "诅咒", "中邪", "清除邪气", "保证净化"),
    "financial_or_outcome_guarantee": ("保证开运", "保证招财", "保证复合", "保证睡着", "一定有效", "一定转运"),
    "third_party_or_coercion": ("让他爱我", "让她回来", "爱情咒", "和合咒", "控制伴侣", "操控", "报复", "下咒", "诅咒他"),
    "purchase_pressure": ("必须买", "高价草药", "天价套装", "会员囤货", "贷款买", "越贵越灵", "代理课程"),
    "repeated_dependency": ("每天做到满意", "反复做草药包", "停不下来", "不用就不安心", "每天问草药", "一直换配方"),
}

SAFE_NEGATED_RISK_PHRASES = (
    "不治疗",
    "不诊断",
    "不替代医生",
    "不替代医疗",
    "不替代心理咨询",
    "不内服",
    "不喝",
    "不泡水喝",
    "不吃",
    "不外敷",
    "不碰宠物",
    "不碰孕妇",
    "不野采",
    "不采野草",
    "不用明火",
    "不焚烧",
    "不驱邪",
    "不保证开运",
    "不保证招财",
    "不操控",
    "不下咒",
    "不高价购买",
    "不囤货",
    "不反复做",
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
    return "herbal_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = remove_safe_negations(text)
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "medical_or_mental_health_claim" in flags or "professional_replacement" in flags:
        return "草本/香草象征不能替代医疗、心理健康、安全或紧急支持；可改成植物意象、提醒物和低风险自我整理。"
    if "ingestion_or_topical_use" in flags:
        return "不提供内服、泡水喝、吞服、药浴、外敷、眼耳伤口或私密部位使用建议；只讨论非接触式象征提醒。"
    if "pregnancy_baby_pet_allergy" in flags:
        return "孕婴儿童、宠物、过敏、哮喘或癫痫等场景需要遵循专业安全建议；不做具体草本适用判断。"
    if "foraging_or_poisoning_risk" in flags:
        return "不协助野外采摘、辨毒、食用未知植物或替代中毒/食品安全判断；可改成已知、安全来源物件的象征记录。"
    if "fire_smoke_or_mold_safety" in flags:
        return "不建议密闭焚烧、整夜烟熏、无人看管火源或使用发霉潮湿草药；优先停止、通风和现实安全。"
    if "spirit_fear_or_exorcism" in flags:
        return "不把草本写成驱邪、除灵或保证净化；可改成整理空间、边界提醒和象征性收尾。"
    if "financial_or_outcome_guarantee" in flags:
        return "不承诺开运、招财、复合、睡眠或任何结果；可改成可观察、可撤回的小行动。"
    if "third_party_or_coercion" in flags:
        return "不使用草本仪式操控他人、爱情咒、读心、复合或报复；可改成自己的边界和沟通准备。"
    if "purchase_pressure" in flags:
        return "不制造高价草药套装、会员囤货或课程压力；优先已有物件、低成本替代和不购买选项。"
    if "repeated_dependency" in flags:
        return "暂停反复制作或一直换配方直到安心的依赖模式；先设定时长、停止条件和现实复盘。"
    return "可以把草本、香草和植物包作为文化象征、提醒物和低风险反思工具，不作为治疗、净化保证或结果承诺。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "herbal_request_guard",
        "request_text": text,
        "system": "herbal_plant_magic_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_herbal": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "草本、香草、草药包、植物魔法和绿巫语境只作为文化象征、提醒物和低风险反思，不证明疗效、净化、开运或关系结果。",
            "不提供内服、泡水喝、吞服、外敷、药浴、孕婴宠物过敏、野外采摘、辨毒或未知植物食用建议。",
            "不替代医疗、心理健康、法律、安全、消防、食品安全、宠物兽医或紧急支持。",
            "不制造高价购买、会员囤货、代理课程、反复依赖、驱邪恐惧、第三方操控、爱情咒、诅咒或结果保证。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已有草本物件，还是做低风险植物象征反思？",
            "草本/物件来源、使用方式、是否接触身体、是否燃烧、空间通风、是否有孕婴宠物过敏或野采风险是什么？",
            "关注主题、预算、已有物件、停止条件和是否涉及医疗替代、驱邪恐惧、操控、结果保证或购买压力是什么？",
        ],
        "next_steps": [
            "record_herbal_context",
            "lookup_herbal_symbols",
            "build_herbal_practice_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_herbal_consultation", "reframe_to_safety_or_professional_support"],
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
    parser.add_argument("--text", help="Herbal, green witchcraft, or plant magic request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_herbal"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
