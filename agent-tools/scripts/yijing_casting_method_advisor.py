#!/usr/bin/env python3
"""Advise Yijing casting method selection and repeat-question handling."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Iterable


METHOD_ALIASES = {
    "three_coins": "three_coins",
    "three_coin": "three_coins",
    "coins": "three_coins",
    "coin": "three_coins",
    "三枚铜钱": "three_coins",
    "铜钱": "three_coins",
    "硬币": "three_coins",
    "yarrow_stalk": "yarrow_stalk",
    "yarrow_stalks": "yarrow_stalk",
    "yarrow": "yarrow_stalk",
    "蓍草": "yarrow_stalk",
    "manual": "manual_user_cast",
    "manual_user_cast": "manual_user_cast",
    "手动": "manual_user_cast",
    "自己起卦": "manual_user_cast",
    "external": "external_hexagram",
    "external_hexagram": "external_hexagram",
    "外部卦": "external_hexagram",
    "已有卦": "external_hexagram",
}

METHOD_PROFILES = {
    "three_coins": {
        "display_name": "三枚铜钱模拟",
        "method_type": "agent_simulated",
        "use_when": "用户没有自行起卦，且同意 agent 使用可复现随机模拟。",
        "required_fields": ["question_text", "casting_method", "seed_or_seed_generated", "cast_time", "timezone"],
        "record_with": "yijing_casting_simulator",
        "limits": "需要保留 seed；模拟随机只是象征反思入口，不是命运证明。",
    },
    "yarrow_stalk": {
        "display_name": "蓍草概率模拟",
        "method_type": "agent_simulated",
        "use_when": "用户想采用蓍草概率分布，但不做完整分蓍过程。",
        "required_fields": ["question_text", "casting_method", "seed_or_seed_generated", "cast_time", "timezone", "probability_model"],
        "record_with": "yijing_casting_simulator",
        "limits": "当前实现是传统蓍草概率模型，不模拟完整蓍草操作步骤。",
    },
    "manual_user_cast": {
        "display_name": "用户手动起卦",
        "method_type": "user_cast",
        "use_when": "用户自己掷币、抽签、蓍草或按既定方式得到六爻。",
        "required_fields": ["question_text", "casting_method", "line_values_bottom_to_top", "cast_time", "timezone"],
        "record_with": "yijing_hexagram_record",
        "limits": "必须确认六爻自下而上记录；不能替用户补造缺失爻位。",
    },
    "external_hexagram": {
        "display_name": "外部卦盘/用户提供结果",
        "method_type": "external_record",
        "use_when": "用户已经从外部工具、书籍、老师或笔记得到本卦、动爻或六爻值。",
        "required_fields": ["question_text", "chart_source", "base_hexagram_or_line_values", "changing_lines_if_any", "cast_time_or_source_time"],
        "record_with": "yijing_hexagram_record",
        "limits": "只记录来源和字段；字段不足时不重新生成或补造卦。",
    },
}

REPEAT_MARKERS = ("再占", "再问一次", "反复问", "刚刚问过", "又问", "同一个问题", "同样的问题")
NEW_FACT_MARKERS = ("新增", "新情况", "已经行动", "行动后", "隔了", "变化", "有了结果", "新的选择", "补充事实")
HIGH_RISK_MARKERS = ("股票", "贷款", "投资", "停药", "手术", "自杀", "自残", "家暴", "控制他", "让他爱我")


def normalize_str(value: Any) -> str:
    return str(value or "").strip()


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text.strip().lower())


def similarity_key(text: str) -> str:
    cleaned = normalize_text(text)
    for token in ("我想问", "请问", "帮我", "用易经", "占一下", "看看", "是否", "会不会", "该不该"):
        cleaned = cleaned.replace(token, "")
    return cleaned[:24]


def normalize_method(value: Any) -> str | None:
    text = normalize_str(value)
    if not text:
        return None
    return METHOD_ALIASES.get(text, METHOD_ALIASES.get(text.lower()))


def detect_requested_method(payload: dict[str, Any]) -> str | None:
    for field in ("requested_method", "casting_method", "method"):
        method = normalize_method(payload.get(field))
        if method:
            return method
    text = " ".join(normalize_str(payload.get(field)) for field in ("question_text", "request_text", "notes"))
    for alias, method in sorted(METHOD_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if alias and alias.lower() in text.lower():
            return method
    if payload.get("user_has_cast") or payload.get("has_external_cast"):
        return "external_hexagram"
    return None


def detect_repeat(payload: dict[str, Any]) -> tuple[bool, bool]:
    text = normalize_str(payload.get("question_text", payload.get("request_text", "")))
    repeat = contains_any(text, REPEAT_MARKERS)
    has_new_facts = bool(payload.get("new_facts"))
    previous_questions = payload.get("previous_questions", [])
    if isinstance(previous_questions, list) and text:
        current_key = similarity_key(text)
        for previous in previous_questions:
            if current_key and current_key == similarity_key(str(previous)):
                repeat = True
                break
    previous_casts = payload.get("previous_casts", [])
    if isinstance(previous_casts, list) and previous_casts:
        previous_texts = [cast.get("question_text", "") for cast in previous_casts if isinstance(cast, dict)]
        current_key = similarity_key(text)
        if any(current_key and current_key == similarity_key(str(previous)) for previous in previous_texts):
            repeat = True
    if repeat and contains_any(text, NEW_FACT_MARKERS):
        has_new_facts = True
    return repeat, has_new_facts


def profile_for(method: str) -> dict[str, Any]:
    profile = METHOD_PROFILES[method]
    return {
        "method": method,
        "display_name": profile["display_name"],
        "method_type": profile["method_type"],
        "use_when": profile["use_when"],
        "required_fields": profile["required_fields"],
        "record_with": profile["record_with"],
        "limits": profile["limits"],
    }


def detect_risk_flags(payload: dict[str, Any]) -> list[str]:
    text = " ".join(normalize_str(payload.get(field)) for field in ("question_text", "request_text", "notes"))
    flags: list[str] = []
    if contains_any(text, ("股票", "贷款", "投资")):
        flags.append("professional_finance")
    if contains_any(text, ("停药", "手术", "病", "怀孕")):
        flags.append("professional_health")
    if contains_any(text, ("自杀", "自残", "家暴")):
        flags.append("crisis")
    if contains_any(text, ("控制他", "让他爱我", "诅咒", "报复")):
        flags.append("coercion")
    if not flags and contains_any(text, HIGH_RISK_MARKERS):
        flags.append("high_risk")
    return flags


def choose_method(payload: dict[str, Any], requested_method: str | None) -> str | None:
    if requested_method:
        return requested_method
    if payload.get("user_has_cast") or payload.get("has_external_cast"):
        return "external_hexagram"
    if payload.get("user_consent_to_simulation") is True:
        return "three_coins"
    return None


def required_record_fields(method: str | None) -> list[str]:
    if not method:
        return ["question_text", "casting_method_or_existing_cast", "user_consent_or_external_source"]
    return list(METHOD_PROFILES[method]["required_fields"])


def advise(payload: dict[str, Any]) -> dict[str, Any]:
    question_text = normalize_str(payload.get("question_text", payload.get("request_text", "")))
    if not question_text:
        raise ValueError("question_text or request_text is required")

    requested_method = detect_requested_method(payload)
    recommended_method = choose_method(payload, requested_method)
    repeat, has_new_facts = detect_repeat(payload)
    risk_flags = detect_risk_flags(payload)
    warnings: list[str] = []
    missing_fields: list[str] = []

    if repeat and not has_new_facts:
        warnings.append("同一问题不建议重复起卦；除非有新增事实、行动选择或足够时间后的新问题边界。")
    if risk_flags:
        warnings.append("问题含高风险或专业替代内容，应先回到 yijing_question_guard 暂停或改写。")
    if not recommended_method:
        missing_fields.append("casting_method_or_user_consent")
        warnings.append("未选择起卦方式；需要用户手动起卦、提供外部卦，或同意使用模拟起卦。")
    if recommended_method in {"three_coins", "yarrow_stalk"} and payload.get("user_consent_to_simulation") is not True:
        missing_fields.append("user_consent_to_simulation")
        warnings.append("agent 模拟起卦前需要用户明确同意，并保留 seed 以便审计。")
    if recommended_method == "external_hexagram" and not (payload.get("chart_source") or payload.get("source_label")):
        missing_fields.append("chart_source")
        warnings.append("外部卦需要记录来源；来源不明时只能做字段整理，不能补造卦。")

    can_continue = not risk_flags and not (repeat and not has_new_facts) and not missing_fields
    mode = "ready_to_cast" if can_continue and recommended_method in {"three_coins", "yarrow_stalk"} else "record_existing" if can_continue else "needs_clarification"

    return {
        "tool": "yijing_casting_method_advisor",
        "question_text": question_text,
        "requested_method": requested_method or "unspecified",
        "recommended_method": recommended_method or "unspecified",
        "method_profile": profile_for(recommended_method) if recommended_method else None,
        "allowed_methods": [profile_for(method) for method in ("manual_user_cast", "external_hexagram", "three_coins", "yarrow_stalk")],
        "is_repeat_question": repeat,
        "has_new_facts": has_new_facts,
        "can_continue_casting": can_continue,
        "casting_mode": mode,
        "required_record_fields": required_record_fields(recommended_method),
        "missing_fields": missing_fields,
        "risk_flags": risk_flags,
        "warnings": warnings,
        "safe_usage": [
            "先通过 yijing_question_guard 确认一事一问、非重复、非高风险。",
            "用户未自行起卦时，必须先取得模拟起卦同意并保留 seed、时间和方法。",
            "重复占问只有在新增事实、行动选择或问题边界变化后才可重新进入流程。",
        ],
        "limits": [
            "此工具只建议起卦方法和记录字段，不生成卦、不解释卦。",
            "外部卦字段不足时不补造六爻、本卦、动爻或变卦。",
            "高风险、专业替代、危机或操控请求应先暂停占问并改写。",
        ],
        "next_steps": [
            "run_or_confirm_yijing_question_guard",
            "if_agent_simulated_run_yijing_casting_simulator",
            "if_existing_cast_record_with_yijing_hexagram_record",
            "lookup_hexagrams_and_lines_before_interpretation",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload.update(json.load(f))
    if args.text:
        payload["question_text"] = args.text
    if args.method:
        payload["requested_method"] = args.method
    if args.user_consent_to_simulation:
        payload["user_consent_to_simulation"] = True
    if args.user_has_cast:
        payload["user_has_cast"] = True
    if args.chart_source:
        payload["chart_source"] = args.chart_source
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"question_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Yijing question text.")
    parser.add_argument("--method", help="Requested casting method.")
    parser.add_argument("--user-consent-to-simulation", action="store_true", help="User agreed to agent-randomized casting.")
    parser.add_argument("--user-has-cast", action="store_true", help="User has already cast or provides an external hexagram.")
    parser.add_argument("--chart-source", help="Source label for an external cast.")
    parser.add_argument("--json", help="Inline JSON payload.")
    parser.add_argument("--file", help="Path to JSON payload.")
    args = parser.parse_args()
    try:
        result = advise(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_casting"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
