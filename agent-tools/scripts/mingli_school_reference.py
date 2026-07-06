#!/usr/bin/env python3
"""Lookup Bazi and Ziwei school differences without generating charts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Iterable


SCHOOL_ALIASES = {
    "子平": "bazi_ziping",
    "子平法": "bazi_ziping",
    "八字子平": "bazi_ziping",
    "ziping": "bazi_ziping",
    "bazi_ziping": "bazi_ziping",
    "传统八字": "bazi_traditional",
    "传统": "bazi_traditional",
    "古法": "bazi_traditional",
    "格局派": "bazi_traditional",
    "traditional": "bazi_traditional",
    "bazi_traditional": "bazi_traditional",
    "现代八字": "bazi_modern_synthesis",
    "现代综合": "bazi_modern_synthesis",
    "综合派": "bazi_modern_synthesis",
    "新派": "bazi_modern_synthesis",
    "modern_synthesis": "bazi_modern_synthesis",
    "bazi_modern_synthesis": "bazi_modern_synthesis",
    "三合": "ziwei_sanhe",
    "三合派": "ziwei_sanhe",
    "紫微三合": "ziwei_sanhe",
    "sanhe": "ziwei_sanhe",
    "ziwei_sanhe": "ziwei_sanhe",
    "四化": "ziwei_sihua",
    "飞星四化": "ziwei_sihua",
    "紫微四化": "ziwei_sihua",
    "sihua": "ziwei_sihua",
    "ziwei_sihua": "ziwei_sihua",
    "中州": "ziwei_zhongzhou",
    "中州派": "ziwei_zhongzhou",
    "zhongzhou": "ziwei_zhongzhou",
    "ziwei_zhongzhou": "ziwei_zhongzhou",
    "现代紫微": "ziwei_modern_synthesis",
    "紫微综合": "ziwei_modern_synthesis",
    "ziwei_modern_synthesis": "ziwei_modern_synthesis",
    "未知": "unspecified",
    "不确定": "unspecified",
    "未声明": "unspecified",
    "unspecified": "unspecified",
}

SYSTEM_DEFAULTS = {
    "bazi": "bazi_unspecified",
    "八字": "bazi_unspecified",
    "四柱": "bazi_unspecified",
    "ziwei": "ziwei_unspecified",
    "紫微": "ziwei_unspecified",
    "紫微斗数": "ziwei_unspecified",
}

SCHOOL_PROFILES = {
    "bazi_ziping": {
        "system": "bazi",
        "display_name": "八字子平",
        "category": "bazi_structure",
        "core_difference": "以日主、月令、十神、格局、旺衰等为常见分析骨架；不同师承在旺衰、调候、格局优先级上仍有差异。",
        "affects": ["日主", "月令", "十神", "格局", "旺衰", "用神"],
        "required_fields": [
            "birth_date",
            "birth_time",
            "birth_place",
            "calendar_type",
            "timezone",
            "solar_time_strategy",
            "chart_source",
            "school",
        ],
        "conflicts_with": [],
        "safe_use": "适合记录为八字分析口径；输出时说明只是象征解释框架，不把用神或格局说成确定命运。",
    },
    "bazi_traditional": {
        "system": "bazi",
        "display_name": "传统八字/古法标签",
        "category": "lineage_label",
        "core_difference": "传统、古法、格局派等标签过宽，必须补充书系、老师或资料来源；不能只凭标签推断唯一断法。",
        "affects": ["格局", "调候", "神煞取舍", "用神顺序", "资料来源"],
        "required_fields": ["source_label", "chart_source", "school", "interpretive_priority"],
        "conflicts_with": [],
        "safe_use": "作为来源标签记录，并把具体口径写清楚；来源不足时只做方法边界说明。",
    },
    "bazi_modern_synthesis": {
        "system": "bazi",
        "display_name": "现代八字综合",
        "category": "bazi_synthesis",
        "core_difference": "常混合旺衰、格局、调候、心理和职业语言；需要声明各层权重，避免冒充单一传统正统断法。",
        "affects": ["解释语言", "权重排序", "职业/心理转译", "行动建议"],
        "required_fields": ["chart_source", "school", "synthesis_rules", "analysis_focus"],
        "conflicts_with": [],
        "safe_use": "适合做低风险反思和行动提示；应标注综合框架，不给健康、财富、婚恋结局保证。",
    },
    "ziwei_sanhe": {
        "system": "ziwei",
        "display_name": "紫微三合",
        "category": "ziwei_structure",
        "core_difference": "重视三方四正、星曜组合和宫位结构；解读会优先看宫位关系与主辅星组合。",
        "affects": ["宫位", "主星", "辅星", "三方四正", "宫位关系"],
        "required_fields": ["birth_date", "birth_time", "birth_place", "calendar_type", "chart_source", "palaces", "stars", "school"],
        "conflicts_with": [],
        "safe_use": "只解释已按三合口径生成或外部提供的紫微盘；缺宫位和星曜字段时不补造。",
    },
    "ziwei_sihua": {
        "system": "ziwei",
        "display_name": "紫微四化/飞星四化",
        "category": "ziwei_sihua",
        "core_difference": "重视化禄、化权、化科、化忌及飞化路径；同一盘在互动和事件语言上会有不同侧重。",
        "affects": ["四化", "飞化路径", "宫位互动", "时间层次", "事件语言"],
        "required_fields": ["birth_date", "birth_time", "birth_place", "calendar_type", "chart_source", "sihua_fields", "school"],
        "conflicts_with": [],
        "safe_use": "适合在四化字段来源明确时做关系和阶段性象征分析；不能把飞化路径当作确定事件预言。",
    },
    "ziwei_zhongzhou": {
        "system": "ziwei",
        "display_name": "紫微中州派",
        "category": "lineage_label",
        "core_difference": "中州派是具体传承标签，常见口径更细；使用前需要说明资料来源、排盘字段和解释术语出处。",
        "affects": ["传承来源", "星曜细则", "四化解释", "术语口径"],
        "required_fields": ["source_label", "chart_source", "palaces", "stars", "school"],
        "conflicts_with": [],
        "safe_use": "作为有来源的流派标签记录；来源不足时不冒充中州派细则。",
    },
    "ziwei_modern_synthesis": {
        "system": "ziwei",
        "display_name": "现代紫微综合",
        "category": "ziwei_synthesis",
        "core_difference": "常综合三合、四化、心理转译和咨询语言；需要声明混合规则和哪些字段来自外部盘。",
        "affects": ["宫位权重", "星曜组合", "四化权重", "咨询语言", "行动建议"],
        "required_fields": ["chart_source", "school", "synthesis_rules", "palaces", "stars"],
        "conflicts_with": [],
        "safe_use": "适合做象征性复盘和低风险建议；不要把综合解读包装成唯一派别结论。",
    },
    "bazi_unspecified": {
        "system": "bazi",
        "display_name": "八字未声明派别",
        "category": "missing_method",
        "core_difference": "已知用户想用八字，但派别、排盘来源或解释优先级未声明。",
        "affects": ["排盘有效性", "用神口径", "格局/旺衰判断", "解释置信度"],
        "required_fields": ["school", "chart_source", "birth_date", "birth_time", "calendar_type", "solar_time_strategy"],
        "conflicts_with": [],
        "safe_use": "先补问八字口径或外部盘来源；最多做通用资料需求说明。",
    },
    "ziwei_unspecified": {
        "system": "ziwei",
        "display_name": "紫微未声明派别",
        "category": "missing_method",
        "core_difference": "已知用户想用紫微斗数，但三合、四化、中州或综合口径未声明。",
        "affects": ["宫位解释", "星曜权重", "四化取用", "解释置信度"],
        "required_fields": ["school", "chart_source", "birth_date", "birth_time", "calendar_type", "palaces", "stars"],
        "conflicts_with": [],
        "safe_use": "先补问紫微派别、外部盘和字段；不要自动补造宫位星曜。",
    },
    "unspecified": {
        "system": "mingli",
        "display_name": "未声明命理系统/派别",
        "category": "missing_method",
        "core_difference": "命理系统、派别或资料来源未声明，不能排盘或做派别细节判断。",
        "affects": ["系统选择", "方法边界", "资料需求", "解释置信度"],
        "required_fields": ["system", "school", "chart_source_or_generation_assumptions"],
        "conflicts_with": [],
        "safe_use": "先确认八字还是紫微，以及外部盘/排盘参数；最多做通用方法说明。",
    },
}

RISK_PATTERNS = {
    "deterministic_claim": ("必富贵", "必离婚", "命苦", "克夫", "孤寡", "一定", "百分百", "绝对", "必然"),
    "professional_finance": ("股票", "贷款", "投资", "梭哈", "期货", "彩票", "赌博", "发财"),
    "medical_or_crisis": ("停药", "用药", "病", "寿命", "死期", "怀孕", "自杀", "自伤", "伤害他人"),
    "legal_or_emergency": ("起诉", "报警", "火灾", "燃气", "触电", "家暴"),
    "coercion_or_privacy": ("控制他", "让他爱我", "查前任", "前任出生", "跟踪", "偷看"),
    "minor_labeling": ("孩子一生", "宝宝一生", "小孩命", "孩子命", "宝宝命苦"),
}


def normalize_str(value: Any) -> str:
    return str(value or "").strip()


def text_contains_any(text: str, values: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def normalize_system(value: Any) -> str:
    text = normalize_str(value)
    direct = SYSTEM_DEFAULTS.get(text, SYSTEM_DEFAULTS.get(text.lower()))
    if direct:
        return direct
    lowered = text.lower()
    for alias, school in sorted(SYSTEM_DEFAULTS.items(), key=lambda item: len(item[0]), reverse=True):
        if alias.lower() in lowered:
            return school
    return "unspecified"


def normalize_school(value: Any) -> str:
    text = normalize_str(value)
    return SCHOOL_ALIASES.get(text, SCHOOL_ALIASES.get(text.lower(), "unspecified"))


def parse_schools(payload: dict[str, Any]) -> list[str]:
    if payload.get("schools"):
        raw = payload["schools"]
        candidates = raw if isinstance(raw, list) else [raw]
    elif payload.get("school"):
        candidates = [payload["school"]]
    else:
        text = " ".join(
            normalize_str(payload.get(field))
            for field in ("query", "question_text", "request_text", "focus")
        )
        found: list[str] = []
        for alias, school in sorted(SCHOOL_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
            if school != "unspecified" and alias and alias.lower() in text.lower() and school not in found:
                found.append(school)
        if found:
            return found
        system_default = normalize_system(payload.get("system", text))
        return [system_default]

    normalized: list[str] = []
    for candidate in candidates:
        school = normalize_school(candidate)
        if school == "unspecified":
            school = normalize_system(payload.get("system", ""))
        if school not in normalized:
            normalized.append(school)
    return normalized or ["unspecified"]


def detect_risk_flags(payload: dict[str, Any]) -> list[str]:
    text = " ".join(
        normalize_str(payload.get(field))
        for field in ("query", "question_text", "request_text", "focus", "notes")
    )
    return [flag for flag, patterns in RISK_PATTERNS.items() if text_contains_any(text, patterns)]


def profile_for(school: str) -> dict[str, Any]:
    data = SCHOOL_PROFILES[school]
    return {
        "school": school,
        "system": data["system"],
        "display_name": data["display_name"],
        "category": data["category"],
        "core_difference": data["core_difference"],
        "affects": data["affects"],
        "required_fields": data["required_fields"],
        "conflicts_with": data["conflicts_with"],
        "safe_use": data["safe_use"],
    }


def conflict_points(schools: list[str]) -> list[dict[str, str]]:
    points: list[dict[str, str]] = []
    systems = {SCHOOL_PROFILES[school]["system"] for school in schools}
    if "bazi" in systems and "ziwei" in systems:
        points.append(
            {
                "schools": "八字 vs 紫微斗数",
                "reason": "两者不是同一张盘或同一套字段；可以并列比较主题倾向，但必须分开记录出生参数、排盘来源、派别和解释层级。",
            }
        )
    if {"ziwei_sanhe", "ziwei_sihua"}.issubset(set(schools)):
        points.append(
            {
                "schools": "紫微三合 vs 紫微四化",
                "reason": "三合偏宫位结构和星曜组合，四化偏化曜与飞化路径；可作为两种镜头并列，不能把权重混成未声明口径。",
            }
        )
    if {"bazi_traditional", "bazi_modern_synthesis"}.issubset(set(schools)):
        points.append(
            {
                "schools": "传统八字 vs 现代综合",
                "reason": "传统标签需要具体来源，现代综合需要说明混合规则；两者的语言和权重不同，应分层呈现。",
            }
        )
    return points


def required_fields_for(schools: list[str]) -> list[str]:
    fields: list[str] = []
    for school in schools:
        for field in SCHOOL_PROFILES[school]["required_fields"]:
            if field not in fields:
                fields.append(field)
    return fields


def comparison_mode_for(schools: list[str]) -> str:
    if schools == ["unspecified"] or all(SCHOOL_PROFILES[school]["category"] == "missing_method" for school in schools):
        return "unknown"
    systems = {SCHOOL_PROFILES[school]["system"] for school in schools if SCHOOL_PROFILES[school]["system"] != "mingli"}
    if len(systems) > 1:
        return "cross_system"
    if len(schools) > 1:
        return "comparison"
    return "single_school"


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    schools = parse_schools(payload)
    profiles = [profile_for(school) for school in schools]
    conflicts = conflict_points(schools)
    risk_flags = detect_risk_flags(payload)
    warnings: list[str] = []
    if any(SCHOOL_PROFILES[school]["category"] == "missing_method" for school in schools):
        warnings.append("命理系统、派别或排盘来源未完整声明；不能排盘或做派别细节判断。")
    if conflicts:
        warnings.append("所选系统/派别的字段和解释权重不同；必须分开记录，不得混成一个断法。")
    if "deterministic_claim" in risk_flags:
        warnings.append("派别差异只能说明方法影响，不支持富贵、婚恋、寿命或灾祸的确定断语。")
    if any(flag in risk_flags for flag in ("professional_finance", "medical_or_crisis", "legal_or_emergency", "coercion_or_privacy")):
        warnings.append("高风险、专业替代、隐私或操控他人的请求应暂停命理解读，转向现实支持或专业意见。")
    if "minor_labeling" in risk_flags:
        warnings.append("涉及未成年人时只能做非标签化、支持性的沟通建议，不给一生命运定性。")

    return {
        "tool": "mingli_school_reference",
        "system": "mingli",
        "query": normalize_str(payload.get("query", payload.get("question_text", payload.get("request_text", "")))),
        "comparison_mode": comparison_mode_for(schools),
        "schools": schools,
        "school_profiles": profiles,
        "conflict_points": conflicts,
        "required_method_fields": required_fields_for(schools),
        "risk_flags": risk_flags,
        "warnings": warnings,
        "safe_usage": [
            "先声明八字或紫微系统、派别、出生资料、时区/真太阳时策略、外部盘或排盘来源。",
            "跨系统或跨派别比较时分层并列，不把不同字段和权重混成单一命运结论。",
            "派别差异只说明方法前提、解释侧重和置信度，不作为健康、财富、婚恋、寿命或重大决策保证。",
        ],
        "limits": [
            "此工具只做八字/紫微派别差异说明，不生成命盘。",
            "没有明确来源时，不冒充某一派正统规则，也不补造干支、宫位、星曜或四化字段。",
            "涉及医疗、法律、财务、危机、人身安全、隐私、操控他人或未成年人标签化时，应暂停占断并转现实支持。",
        ],
        "next_steps": [
            "run_bazi_ziwei_intake_guard_before_birth_data_use",
            "record_chart_parameters_with_bazi_ziwei_chart_record",
            "lookup_symbols_with_mingli_symbol_lookup",
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
    if args.query:
        payload["query"] = args.query
    if args.system:
        payload["system"] = args.system
    if args.school:
        payload["school"] = args.school
    if args.schools:
        payload["schools"] = args.schools
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --query, --system, --school, --schools, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Natural-language school difference query.")
    parser.add_argument("--system", help="bazi or ziwei, used when no concrete school is named.")
    parser.add_argument("--school", help="Single Bazi/Ziwei school label.")
    parser.add_argument("--schools", nargs="+", help="Multiple Bazi/Ziwei school labels.")
    parser.add_argument("--json", help="Inline JSON payload.")
    parser.add_argument("--file", help="Path to JSON payload.")
    args = parser.parse_args()
    try:
        result = lookup(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
