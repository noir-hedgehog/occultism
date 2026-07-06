#!/usr/bin/env python3
"""Lookup Qimen school and plate-convention differences without generating charts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Iterable


SCHOOL_ALIASES = {
    "置闰": "zhirun",
    "置闰法": "zhirun",
    "zhirun": "zhirun",
    "拆补": "chaibu",
    "拆补法": "chaibu",
    "chaibu": "chaibu",
    "茅山": "maoshan",
    "茅山法": "maoshan",
    "maoshan": "maoshan",
    "飞盘": "feipan",
    "飞盘奇门": "feipan",
    "feipan": "feipan",
    "转盘": "turning_plate",
    "转盘奇门": "turning_plate",
    "turning_plate": "turning_plate",
    "zhuanpan": "turning_plate",
    "未知": "unspecified",
    "不确定": "unspecified",
    "unspecified": "unspecified",
}

SCHOOL_PROFILES = {
    "zhirun": {
        "display_name": "置闰",
        "category": "jieqi_boundary",
        "core_difference": "以置闰方式处理节气边界和局数连续性；排盘前必须声明节气来源。",
        "affects": ["节气边界", "阴阳遁", "局数", "起局时点"],
        "required_fields": ["chart_time", "timezone", "location", "solar_term_source", "solar_time_strategy"],
        "conflicts_with": ["chaibu"],
        "safe_use": "适合在节气来源明确时记录为起局方法，不把置闰结果与拆补结果混作同一盘。",
    },
    "chaibu": {
        "display_name": "拆补",
        "category": "jieqi_boundary",
        "core_difference": "以拆补方式处理节气交接和局数补足；与置闰在边界时点可能给出不同局。",
        "affects": ["节气边界", "阴阳遁", "局数", "起局时点"],
        "required_fields": ["chart_time", "timezone", "location", "solar_term_source", "solar_time_strategy"],
        "conflicts_with": ["zhirun"],
        "safe_use": "适合在拆补口径已声明时使用；不能用置闰盘的宫位套拆补断法。",
    },
    "maoshan": {
        "display_name": "茅山",
        "category": "lineage_label",
        "core_difference": "更像传承或流派标签，具体排盘和断法细节需要来源说明，不能只凭名称补算法。",
        "affects": ["起局口径", "用神细则", "断法术语", "资料来源"],
        "required_fields": ["source_label", "chart_method", "chart_time_or_external_chart"],
        "conflicts_with": [],
        "safe_use": "作为来源标签记录；若没有老师、书籍或外部盘说明，只能做方法边界说明。",
    },
    "feipan": {
        "display_name": "飞盘",
        "category": "plate_convention",
        "core_difference": "飞盘与转盘的门、星、神、干布列/移动约定不同，会影响九宫字段和后续解释。",
        "affects": ["九宫布列", "门星神干位置", "用神落宫", "宫位关系"],
        "required_fields": ["chart_source_or_engine", "plate_convention", "palaces"],
        "conflicts_with": ["turning_plate"],
        "safe_use": "只解释已按飞盘口径生成或外部提供的盘；不要把转盘字段改名为飞盘。",
    },
    "turning_plate": {
        "display_name": "转盘",
        "category": "plate_convention",
        "core_difference": "转盘与飞盘的布盘约定不同，同一时间参数可能得到不同宫位结构。",
        "affects": ["九宫布列", "门星神干位置", "用神落宫", "宫位关系"],
        "required_fields": ["chart_source_or_engine", "plate_convention", "palaces"],
        "conflicts_with": ["feipan"],
        "safe_use": "只解释已按转盘口径生成或外部提供的盘；不要与飞盘断法混用。",
    },
    "unspecified": {
        "display_name": "未声明派别",
        "category": "missing_method",
        "core_difference": "派别或盘式约定未声明，不能生成盘式或做派别细节判断。",
        "affects": ["排盘有效性", "方法边界", "解释置信度"],
        "required_fields": ["school", "chart_method", "chart_source_or_generation_assumptions"],
        "conflicts_with": [],
        "safe_use": "先补问派别、来源或外部盘；最多做通用奇门方法说明。",
    },
}

RISK_PATTERNS = {
    "deterministic_claim": ("必成", "必败", "一定", "百分百", "绝对", "必然"),
    "professional_finance": ("股票", "贷款", "投资", "梭哈", "期货", "彩票", "赌博"),
    "medical_or_crisis": ("停药", "用药", "病", "自杀", "自伤", "伤害他人"),
    "legal_or_emergency": ("起诉", "报警", "火灾", "燃气", "触电", "家暴"),
    "coercion_or_privacy": ("控制他", "让他爱我", "查前任", "跟踪", "偷看"),
}


def normalize_str(value: Any) -> str:
    return str(value or "").strip()


def text_contains_any(text: str, values: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def normalize_school(value: Any) -> str:
    text = normalize_str(value)
    return SCHOOL_ALIASES.get(text, SCHOOL_ALIASES.get(text.lower(), "unspecified"))


def parse_schools(payload: dict[str, Any]) -> list[str]:
    raw = payload.get("schools", payload.get("school", payload.get("query", "")))
    if isinstance(raw, list):
        candidates = raw
    else:
        text = normalize_str(raw)
        found: list[str] = []
        for alias, school in sorted(SCHOOL_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
            if school != "unspecified" and alias and alias.lower() in text.lower() and school not in found:
                found.append(school)
        if found:
            return found
        for sep in ("、", "，", ",", "/", " vs ", "和", "与"):
            text = text.replace(sep, "|")
        candidates = [part for part in text.split("|") if part.strip()]
    normalized: list[str] = []
    for candidate in candidates:
        school = normalize_school(candidate)
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
    selected = set(schools)
    seen: set[tuple[str, str]] = set()
    for school in schools:
        for conflict in SCHOOL_PROFILES[school]["conflicts_with"]:
            pair = tuple(sorted((school, conflict)))
            if conflict in selected and pair not in seen:
                seen.add(pair)
                points.append(
                    {
                        "schools": f"{SCHOOL_PROFILES[school]['display_name']} vs {SCHOOL_PROFILES[conflict]['display_name']}",
                        "reason": "两者属于不同起局或盘式约定，可能改变局数、宫位或门星神干位置；必须分盘比较，不能混用字段。",
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


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    schools = parse_schools(payload)
    profiles = [profile_for(school) for school in schools]
    conflicts = conflict_points(schools)
    risk_flags = detect_risk_flags(payload)
    warnings: list[str] = []
    if "unspecified" in schools:
        warnings.append("派别或盘式约定未声明；不能生成奇门盘或做派别细节判断。")
    if conflicts:
        warnings.append("所选派别/盘式存在冲突；必须分开记录和比较，不得把字段混成一个盘。")
    if "deterministic_claim" in risk_flags:
        warnings.append("派别差异只能说明方法影响，不支持必成、必败或绝对吉凶断语。")
    if any(flag in risk_flags for flag in ("professional_finance", "medical_or_crisis", "legal_or_emergency", "coercion_or_privacy")):
        warnings.append("高风险或专业替代请求应暂停奇门解读，转向现实支持或专业意见。")

    mode = "single_school"
    if len(schools) > 1:
        mode = "comparison"
    if schools == ["unspecified"]:
        mode = "unknown"

    return {
        "tool": "qimen_school_reference",
        "system": "qimen_dunjia",
        "query": normalize_str(payload.get("query", payload.get("question_text", payload.get("request_text", "")))),
        "comparison_mode": mode,
        "schools": schools,
        "school_profiles": profiles,
        "conflict_points": conflicts,
        "required_method_fields": required_fields_for(schools),
        "risk_flags": risk_flags,
        "warnings": warnings,
        "safe_usage": [
            "先声明派别、盘式约定、节气来源、时间地点和外部盘/生成器来源。",
            "若比较置闰/拆补或飞盘/转盘，必须分盘并列，不把不同口径字段混成一个结论。",
            "派别差异只说明方法前提和解释置信度，不作为成败、疾病、财富或关系结局保证。",
        ],
        "limits": [
            "此工具只做派别和盘式约定说明，不生成奇门盘。",
            "没有明确来源时，不冒充某一派正统规则，也不补造门、星、神、干位置。",
            "涉及医疗、法律、财务、危机、人身安全、隐私或操控他人时，暂停占问并转现实支持。",
        ],
        "next_steps": [
            "run_qimen_method_guard_with_declared_school",
            "record_external_or_generated_chart_with_qimen_chart_record",
            "select_focus_targets_with_qimen_focus_selector",
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
    raise ValueError("Provide --query, --school, --schools, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="School query, e.g. 置闰和拆补, 飞盘 vs 转盘.")
    parser.add_argument("--school", help="Single school id or label.")
    parser.add_argument("--schools", nargs="+", help="One or more school ids or labels.")
    parser.add_argument("--json", help="JSON input.")
    parser.add_argument("--file", help="Path to JSON input.")
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
