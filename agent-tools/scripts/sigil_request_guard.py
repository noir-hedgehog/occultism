#!/usr/bin/env python3
"""Guard sigil, seal, and magic-circle symbolism requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "sigil_symbolic_consultation": ("sigil", "sigils", "符号印记", "印记魔法", "魔法印记", "个人印记", "意图符号", "愿望符号", "seal magic", "magical seal"),
    "circle_or_symbol_record": ("魔法阵", "阵图", "符号阵", "圆阵", "护圈", "circle", "magic circle", "symbol circle"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来源", "象征"),
}

RISK_KEYWORDS = {
    "blood_or_body_harm": ("血", "滴血", "割", "割手", "划皮肤", "刻皮肤", "刺破", "伤口", "自残", "疼痛献祭"),
    "fire_or_destruction": ("烧掉", "焚烧", "点燃", "烧纸", "烧符", "蜡烛烧", "火盆", "密闭燃烧"),
    "spirit_summoning_or_exorcism": ("召唤", "召灵", "召魔", "恶魔", "驱邪", "除灵", "赶鬼", "附身", "通灵命令", "封印灵体"),
    "curse_or_coercion": ("诅咒", "下咒", "报复", "让他爱我", "让她回来", "控制伴侣", "操控", "绑定某人", "爱情咒", "和合"),
    "outcome_guarantee": ("保证实现", "一定显化", "必成", "必然成功", "百分百有效", "马上应验", " guaranteed"),
    "professional_replacement": ("不用医生", "不用报警", "不用律师", "不用心理咨询", "不用还债", "替代治疗", "替代药物"),
    "financial_or_legal_risk": ("暴富", "稳赚", "彩票", "赌博", "投资翻倍", "躲法律", "逃债", "骗过审查"),
    "tattoo_or_permanent_mark": ("纹身", "刺青", "永久刻", "烙印", "刻在身上", "脸上画", "皮肤印记"),
    "purchase_pressure": ("必须买", "高价课程", "天价模板", "开光印章", "越贵越灵", "会员符号库", "贷款买"),
    "repeated_dependency": ("每天画到灵", "反复画到安心", "停不下来", "一直重画", "每天问符号", "不画就害怕"),
}

SAFE_NEGATED_RISK_PHRASES = (
    "不用血",
    "不滴血",
    "不割",
    "不划皮肤",
    "不刻皮肤",
    "不自残",
    "不烧",
    "不焚烧",
    "不用火",
    "不点燃",
    "不召唤",
    "不召灵",
    "不驱邪",
    "不除灵",
    "不诅咒",
    "不下咒",
    "不报复",
    "不操控",
    "不控制",
    "不绑定别人",
    "不保证实现",
    "不保证",
    "不替代医生",
    "不替代医疗",
    "不替代心理咨询",
    "不替代法律",
    "不赌博",
    "不投资",
    "不纹身",
    "不刺青",
    "不永久",
    "不高价购买",
    "不买课程",
    "不反复画",
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
    return "sigil_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = remove_safe_negations(text)
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "blood_or_body_harm" in flags:
        return "不提供滴血、割伤、刻皮肤、疼痛献祭或任何伤害身体的印记做法；可改成纸上草稿、可擦除卡片和非接触提醒。"
    if "fire_or_destruction" in flags:
        return "不提供焚烧、点燃、烧符、密闭燃烧或危险销毁步骤；可改成撕碎草稿、归档或普通回收等安全收尾。"
    if "spirit_summoning_or_exorcism" in flags:
        return "不把 sigil 写成召唤、封印、驱邪或灵体命令；可改成边界、专注、复盘和现实行动提示。"
    if "curse_or_coercion" in flags:
        return "不协助诅咒、报复、绑定或操控他人；可改成自己的边界、沟通准备和可控行动。"
    if "outcome_guarantee" in flags:
        return "不承诺显化、必成或马上应验；可把符号当作意图整理和行动复盘工具。"
    if "professional_replacement" in flags:
        return "符号印记不能替代医疗、心理、法律、安全或紧急支持；可改成辅助记录和准备问题清单。"
    if "financial_or_legal_risk" in flags:
        return "不提供赌博、投资、逃债、违法或绕过审查的符号建议；可改成预算、风险和合规提醒。"
    if "tattoo_or_permanent_mark" in flags:
        return "不建议把未审慎确认的印记永久纹身、刺青、烙印或刻在身体上；先用可擦、可撤回的纸面版本。"
    if "purchase_pressure" in flags:
        return "不制造高价课程、模板、印章或会员符号库压力；优先已有纸笔和低成本方案。"
    if "repeated_dependency" in flags:
        return "暂停反复画到安心或一直重画的依赖模式；先设定一次性时长、停止条件和现实复盘。"
    return "可以把 sigil、符号印记或魔法阵作为文化象征、意图整理和低风险提醒物，不作为灵验保证、召唤命令或操控工具。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "sigil_request_guard",
        "request_text": text,
        "system": "sigil_seal_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_sigil": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "Sigil、符号印记、魔法阵和 seal 只作为文化象征、意图整理、提醒物和低风险反思，不证明灵验、召唤、驱邪、显化或关系结果。",
            "不提供滴血、割伤、刻皮肤、纹身刺青、烙印、焚烧、密闭燃烧、危险销毁、召唤、封印灵体或驱邪步骤。",
            "不替代医疗、心理健康、法律、安全、财务、消防或紧急支持。",
            "不协助诅咒、报复、操控他人、爱情咒、违法逃避、高价课程购买、反复依赖或结果保证。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、整理个人符号，还是把已有图案转成低风险意图提醒？",
            "符号来源、绘制媒介、展示位置、是否可擦除、是否涉及身体、火、第三方或永久化是什么？",
            "关注主题、意图短句、现实行动、预算、停止条件和是否涉及召唤/诅咒/操控/保证/专业替代是什么？",
        ],
        "next_steps": [
            "record_sigil_context",
            "lookup_sigil_symbols",
            "build_sigil_practice_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_sigil_consultation", "reframe_to_safety_or_professional_support"],
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
    parser.add_argument("--text", help="Sigil, seal, or magic-circle request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_sigil"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
