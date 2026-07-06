#!/usr/bin/env python3
"""Guard body omen symbolism requests such as eye twitching and ear ringing."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "body_omen_symbolic_consultation": (
        "眼跳",
        "左眼跳",
        "右眼跳",
        "耳鸣",
        "耳热",
        "打喷嚏",
        "喷嚏",
        "脸热",
        "手心痒",
        "身体征兆",
        "身体预兆",
        "肉跳",
        "body omen",
        "eye twitch",
        "ear ringing",
    ),
    "omen_journal_record": ("记录", "日志", "今天", "时辰", "民俗表", "对照表", "omen journal"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来源", "象征", "民俗"),
}

RISK_KEYWORDS = {
    "medical_red_flag": (
        "突然失明",
        "视力下降",
        "看不清",
        "剧烈头痛",
        "胸痛",
        "呼吸困难",
        "半边麻",
        "说话不清",
        "晕厥",
        "昏倒",
        "持续耳鸣",
        "单侧耳鸣",
        "听力下降",
        "耳痛",
        "眼痛",
        "抽搐",
        "发烧",
        "怀孕",
        "孕期",
    ),
    "medical_replacement": ("不用医生", "不看医生", "不去医院", "只看预兆", "不用检查", "不体检", "不吃药", "停药"),
    "deterministic_disaster_claim": ("一定有灾", "必有灾", "要出事", "血光之灾", "死亡预兆", "大祸", "凶兆", "灾祸"),
    "financial_or_gambling_timing": ("彩票", "赌博", "股票", "投资", "梭哈", "买币", "下注", "开奖", "稳赚"),
    "third_party_body_label": ("看他眼跳", "看她眼跳", "判断他", "判断她", "替别人", "同事眼跳", "前任耳鸣", "他是不是"),
    "spirit_fear_or_exorcism": ("鬼", "中邪", "附身", "被下咒", "诅咒", "邪气", "驱邪", "除灵"),
    "body_harm_or_unsafe_test": ("按眼球", "扎针", "放血", "割", "烫", "憋气", "撞头", "自残"),
    "repeated_dependency": ("每天查", "反复查", "停不下来", "一跳就查", "不查就害怕", "问到安心"),
}

SAFE_NEGATED_RISK_PHRASES = (
    "不替代医生",
    "不替代医疗",
    "不替代检查",
    "不诊断",
    "不治疗",
    "不看成疾病",
    "不是疾病判断",
    "不决定彩票",
    "不买彩票",
    "不赌博",
    "不投资",
    "不看别人",
    "不判断别人",
    "不驱邪",
    "不除灵",
    "不按眼球",
    "不放血",
    "不自残",
    "不反复查",
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
    return "body_omen_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = remove_safe_negations(text)
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "medical_red_flag" in flags or "medical_replacement" in flags:
        return "身体症状不能按预兆处理；若持续、突发、严重或影响视听/呼吸/行动，应优先联系医疗支持，再把民俗部分作为低风险文化记录。"
    if "deterministic_disaster_claim" in flags:
        return "不把眼跳、耳鸣、喷嚏或肉跳写成灾祸定论；可改成民俗象征、身体照料和现实核查清单。"
    if "financial_or_gambling_timing" in flags:
        return "不把身体征兆用于彩票、赌博、投资或收益判断；可改成情绪提醒和预算边界。"
    if "third_party_body_label" in flags:
        return "不根据他人身体反应替其贴标签、读心或判断命运；只处理用户本人自愿提供的低风险记录。"
    if "spirit_fear_or_exorcism" in flags:
        return "不把身体征兆写成中邪、附身、诅咒或驱邪证据；可改成安定感、休息和现实支持。"
    if "body_harm_or_unsafe_test" in flags:
        return "不做按压眼球、放血、自伤或危险试验；身体不适优先停止、休息和求助。"
    if "repeated_dependency" in flags:
        return "暂停一跳就查的依赖模式；设定一次性记录、停止条件和身体照料动作。"
    return "可以把眼跳、耳鸣、喷嚏、耳热等身体征兆作为民俗象征和身体照料提醒，不作为诊断、灾祸预言或决策依据。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "body_omen_request_guard",
        "request_text": text,
        "system": "body_omen_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_body_omen": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "眼跳、耳鸣、喷嚏、耳热、肉跳等只作为民俗象征、身体照料提醒和低风险记录，不证明疾病、灾祸、灵体、财运或事实结果。",
            "不替代医疗诊断、检查、用药、急症处理、心理健康支持或专业建议；持续、突发、严重或影响功能的症状优先现实求助。",
            "不用于彩票、赌博、投资、第三方身体标签、驱邪恐惧、危险身体试验或反复依赖。",
        ],
        "clarifying_questions": [
            "这是文化学习、本人身体征兆记录，还是低风险象征反思？",
            "是否有持续、突发、严重、单侧、疼痛、视听下降、胸痛、呼吸困难、麻木、晕厥、发烧、孕期或停药等医疗红旗？",
            "用户希望整理的现实照料动作、停止条件、记录频率和不用于赌博/灾祸/第三方判断的边界是什么？",
        ],
        "next_steps": [
            "record_body_omen_context",
            "lookup_body_omen_symbols",
            "build_body_omen_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_body_omen_consultation", "reframe_to_medical_or_safety_support"],
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
    parser.add_argument("--text", help="Body omen request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_body_omen"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
