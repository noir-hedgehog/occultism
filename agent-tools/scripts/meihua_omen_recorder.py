#!/usr/bin/env python3
"""Record Meihua external omens as observable facts before symbolic interpretation."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Iterable


SOURCE_ALIASES = {
    "self_observed": "self_observed",
    "user_observed": "self_observed",
    "本人观察": "self_observed",
    "image_notes": "image_notes",
    "photo": "image_notes",
    "照片": "image_notes",
    "audio_notes": "audio_notes",
    "sound": "audio_notes",
    "声音": "audio_notes",
    "third_party_report": "third_party_report",
    "别人转述": "third_party_report",
    "dream": "dream",
    "梦": "dream",
    "online_claim": "online_claim",
    "网络说法": "online_claim",
    "unknown": "unknown",
    "未知": "unknown",
}

TIMING_ALIASES = {
    "before_question": "before_question",
    "问前": "before_question",
    "during_question": "during_question",
    "问时": "during_question",
    "after_question": "after_question",
    "问后": "after_question",
    "unknown": "unknown",
    "未知": "unknown",
}

CATEGORY_RULES = {
    "sound": ("响", "声音", "敲", "铃", "电话", "消息", "叫", "噪音"),
    "movement": ("动", "掉", "落", "开", "关", "经过", "飞", "走", "停"),
    "object": ("灯", "杯", "门", "窗", "书", "纸", "手机", "钥匙", "箱", "镜"),
    "light_weather": ("光", "亮", "暗", "雨", "风", "雷", "云", "晴"),
    "person_message": ("人", "同事", "朋友", "客户", "家人", "消息", "回复", "电话"),
    "direction_place": ("东", "南", "西", "北", "左", "右", "前", "后", "门口", "窗边"),
    "body_feeling": ("心慌", "头痛", "胸闷", "发冷", "发热", "不舒服", "失眠"),
}

SYMBOL_TAGS = {
    "sound": ("communication_signal", "attention_trigger"),
    "movement": ("change_trigger", "timing_signal"),
    "object": ("material_clue", "environment_context"),
    "light_weather": ("visibility_context", "mood_context"),
    "person_message": ("relationship_context", "information_flow"),
    "direction_place": ("space_context", "directional_symbol"),
    "body_feeling": ("body_state", "grounding_needed"),
    "unclear": ("unclear_observation",),
}

RISK_PATTERNS = {
    "professional_finance": ("贷款", "股票", "投资", "梭哈", "币圈", "期货", "发财", "破财"),
    "medical_or_crisis": ("停药", "用药", "怀孕", "病", "自杀", "自伤", "伤害他人", "幻听", "幻视"),
    "legal_or_emergency": ("起诉", "报警", "火灾", "燃气", "触电", "家暴", "跟踪"),
    "coercion_or_privacy": ("控制他", "让他爱我", "查前任", "偷看", "窥探", "跟踪对方"),
    "deterministic_claim": ("必成", "必败", "一定", "百分百", "必分", "必发财", "必有灾"),
    "supernatural_fear": ("中邪", "有鬼", "天意", "报应", "诅咒", "冲撞", "显灵"),
}

BLOCKING_RISKS = {"professional_finance", "medical_or_crisis", "legal_or_emergency", "coercion_or_privacy"}


def normalize_str(value: Any) -> str:
    return str(value or "").strip()


def contains_any(text: str, values: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def normalize_source(value: Any) -> str:
    raw = normalize_str(value)
    return SOURCE_ALIASES.get(raw, SOURCE_ALIASES.get(raw.lower(), "unknown"))


def normalize_timing(value: Any) -> str:
    raw = normalize_str(value)
    return TIMING_ALIASES.get(raw, TIMING_ALIASES.get(raw.lower(), "unknown"))


def split_observations(payload: dict[str, Any]) -> list[str]:
    raw = payload.get("observations")
    if isinstance(raw, list):
        items = [normalize_str(item) if not isinstance(item, dict) else normalize_str(item.get("text")) for item in raw]
    else:
        text = normalize_str(payload.get("omen_text", payload.get("external_omen", raw)))
        items = [part.strip() for part in text.replace("；", ";").replace("，", ";").split(";")]
    return [item for item in items if item]


def detect_category(text: str) -> str:
    for category, keywords in CATEGORY_RULES.items():
        if contains_any(text, keywords):
            return category
    return "unclear"


def detect_risk_flags(payload: dict[str, Any], observations: list[str]) -> list[str]:
    text = " ".join(
        [normalize_str(payload.get(field)) for field in ("question_text", "notes", "interpretation_request")]
        + observations
    )
    return [flag for flag, patterns in RISK_PATTERNS.items() if contains_any(text, patterns)]


def build_observations(payload: dict[str, Any], observations: list[str]) -> list[dict[str, Any]]:
    source_type = normalize_source(payload.get("source_type", payload.get("source")))
    timing = normalize_timing(payload.get("timing_relation", payload.get("timing")))
    direction = normalize_str(payload.get("direction"))
    location = normalize_str(payload.get("location"))
    records = []
    for index, text in enumerate(observations, start=1):
        category = detect_category(text)
        records.append(
            {
                "index": index,
                "text": text,
                "source_type": source_type,
                "timing_relation": timing,
                "category": category,
                "symbol_tags": list(SYMBOL_TAGS[category]),
                "direction": direction,
                "location": location,
                "is_direct_observation": source_type in {"self_observed", "image_notes", "audio_notes"},
                "interpretation_boundary": "先作为可见/可听事实记录，再作为象征提示；不得写成天意、灾祸或成败证明。",
            }
        )
    return records


def record(payload: dict[str, Any]) -> dict[str, Any]:
    observations_text = split_observations(payload)
    risk_flags = detect_risk_flags(payload, observations_text)
    observations = build_observations(payload, observations_text)
    missing_fields = []
    warnings = []

    if not normalize_str(payload.get("question_text")):
        missing_fields.append("question_text")
    if not observations:
        missing_fields.append("omen_text")
    if normalize_source(payload.get("source_type", payload.get("source"))) == "unknown":
        missing_fields.append("source_type")
    if normalize_timing(payload.get("timing_relation", payload.get("timing"))) == "unknown":
        warnings.append("未说明外应相对提问的时间关系；只能作为弱观察材料。")
    if any(item["category"] == "body_feeling" for item in observations):
        warnings.append("身体感受类外应先按现实身心状态处理，不作疾病或灾祸解释。")
    if "deterministic_claim" in risk_flags or "supernatural_fear" in risk_flags:
        warnings.append("外应含决定论或超自然恐惧表达，必须先降级为观察和安定支持。")
    if set(risk_flags) & BLOCKING_RISKS:
        warnings.append("请求含专业替代、危机、隐私或操控风险；暂停梅花外应解读。")
    if missing_fields:
        warnings.append("缺少外应记录字段；先补充事实来源再取象。")

    source_type = normalize_source(payload.get("source_type", payload.get("source")))
    is_valid = not missing_fields
    can_use = is_valid and not (set(risk_flags) & BLOCKING_RISKS)
    return {
        "tool": "meihua_omen_recorder",
        "system": "meihua_yishu",
        "question_text": normalize_str(payload.get("question_text")),
        "recorded_at": normalize_str(payload.get("recorded_at")) or datetime.now(timezone.utc).isoformat(),
        "source_type": source_type,
        "timing_relation": normalize_timing(payload.get("timing_relation", payload.get("timing"))),
        "observation_count": len(observations),
        "observations": observations,
        "risk_flags": risk_flags,
        "missing_fields": sorted(set(missing_fields)),
        "is_valid": is_valid,
        "can_use_as_meihua_omen": can_use,
        "warnings": warnings,
        "grounding_questions": [
            "这个外应具体发生了什么，哪些是可见事实，哪些只是联想？",
            "它和问题的时间关系是什么：问前、问时还是问后？",
            "有没有现实解释、环境因素或需要先处理的安全/健康信号？",
        ],
        "next_steps": [
            "run_yijing_question_guard_for_one_matter_boundary",
            "record_casting_fields_with_meihua_casting_recorder_if_used_for_casting",
            "lookup_external_omen_or_trigram_symbols_with_meihua_symbol_lookup",
            "map_omen_to_observable_signal_not_supernatural_confirmation",
            "lint_final_output_with_mystic_output_lint",
        ],
        "limits": [
            "外应记录只保存用户提供或可观察的事实，不证明天意、灾祸、成败或他人想法。",
            "外应只能作为象征反思和问题澄清材料，不替代医疗、法律、财务、危机或安全处理。",
            "若外应引发恐惧，先做现实核验、安定支持和低风险行动，不追加恐吓式解释。",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["omen_text"] = args.text
    if args.question:
        payload["question_text"] = args.question
    if args.source_type:
        payload["source_type"] = args.source_type
    if args.timing:
        payload["timing_relation"] = args.timing
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"omen_text": raw}
    raise ValueError("Provide --text, --json, --file, or JSON/stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Observed omen text.")
    parser.add_argument("--question", help="Question text.")
    parser.add_argument("--source-type", help="self_observed, image_notes, audio_notes, third_party_report, dream, online_claim, unknown.")
    parser.add_argument("--timing", help="before_question, during_question, after_question, or unknown.")
    parser.add_argument("--json", help="JSON input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = record(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_use_as_meihua_omen"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
