#!/usr/bin/env python3
"""Guard Feng Shui school-specific and liqi method requests before interpretation."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    label: str
    keywords: tuple[str, ...]


SCHOOL_RULES = {
    "xingfa": ("形法", "形势", "门冲", "梁压", "尖角", "明堂", "动线", "采光"),
    "symbolic_bagua": ("八卦", "方位", "东南", "西南", "正北", "正南", "东北", "西北", "东方", "西方"),
    "xuankong_feixing": ("玄空", "飞星", "玄空飞星", "九运", "运盘", "山星", "向星", "五黄", "二黑"),
    "bazhai": ("八宅", "东四命", "西四命", "宅命", "命卦", "生气位", "延年位", "伏位", "绝命位"),
    "sanhe_sanyuan": ("三合", "三元", "水法", "来龙", "砂水", "纳甲"),
    "date_selection": ("择日", "动土日", "搬家日", "入宅日", "开业日"),
}

RISK_RULES = (
    Rule("deterministic_wealth_or_illness", ("破财", "发财", "生病", "得病", "灾", "凶", "必定", "一定")),
    Rule("professional_replacement", ("投资", "贷款", "医生", "用药", "律师", "官司", "合同")),
    Rule("unsafe_structural_action", ("拆承重墙", "砸墙", "改燃气", "改电路", "封窗", "堵消防", "拆门")),
)

DIRECTION_MARKERS = ("坐北朝南", "坐南朝北", "坐东朝西", "坐西朝东", "朝北", "朝南", "朝东", "朝西", "向北", "向南", "向东", "向西")
DIRECTION_SOURCE_MARKERS = ("罗盘", "指南针", "户型图", "坐向", "朝向", "手机指南针", "实测")
TIME_MARKERS = ("建造年份", "入住年份", "入宅", "装修年份", "九运", "八运", "七运", "202", "199", "198")
OCCUPANT_MARKERS = ("出生年", "命卦", "东四命", "西四命")


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_schools(text: str) -> list[str]:
    matches = [school for school, keywords in SCHOOL_RULES.items() if contains_any(text, keywords)]
    if matches:
        return matches
    return ["xingfa"]


def requested_school(payload: dict[str, object], text: str) -> str:
    raw = str(payload.get("school", payload.get("method", ""))).strip().lower()
    aliases = {
        "form": "xingfa",
        "形法": "xingfa",
        "bagua": "symbolic_bagua",
        "八卦": "symbolic_bagua",
        "flying_star": "xuankong_feixing",
        "玄空飞星": "xuankong_feixing",
        "玄空": "xuankong_feixing",
        "八宅": "bazhai",
        "sanyuan": "sanhe_sanyuan",
        "sanhe": "sanhe_sanyuan",
        "择日": "date_selection",
    }
    if raw in SCHOOL_RULES:
        return raw
    if raw in aliases:
        return aliases[raw]
    schools = detect_schools(text)
    if len(schools) == 1:
        return schools[0]
    return "mixed_or_unclear"


def method_level(school: str) -> str:
    if school == "xingfa":
        return "visible_form"
    if school == "symbolic_bagua":
        return "symbolic_direction"
    if school == "mixed_or_unclear":
        return "mixed_or_unclear"
    return "liqi_school"


def detect_risks(text: str) -> list[str]:
    return [rule.label for rule in RISK_RULES if contains_any(text, rule.keywords)]


def has_direction(payload: dict[str, object], text: str) -> bool:
    return bool(payload.get("facing_direction") or payload.get("sitting_direction") or contains_any(text, DIRECTION_MARKERS))


def has_direction_source(payload: dict[str, object], text: str) -> bool:
    source = str(payload.get("direction_source", "")).strip()
    return bool(source and source != "unknown") or contains_any(text, DIRECTION_SOURCE_MARKERS)


def has_time_basis(payload: dict[str, object], text: str) -> bool:
    return bool(payload.get("build_year") or payload.get("move_in_year") or payload.get("period") or contains_any(text, TIME_MARKERS))


def has_occupant_basis(payload: dict[str, object], text: str) -> bool:
    return bool(payload.get("occupant_birth_year") or payload.get("occupant_mingua") or contains_any(text, OCCUPANT_MARKERS))


def required_fields(school: str) -> list[str]:
    if school == "xuankong_feixing":
        return ["school", "facing_direction", "direction_source", "time_basis_or_external_chart"]
    if school == "bazhai":
        return ["school", "facing_or_sitting_direction", "direction_source", "occupant_or_house_mingua_basis"]
    if school == "sanhe_sanyuan":
        return ["school", "direction_source", "terrain_or_water_context", "source_scope"]
    if school == "date_selection":
        return ["school", "event_type", "date_range", "professional_boundary"]
    if school == "symbolic_bagua":
        return ["direction_or_area", "direction_source_if_claiming_compass"]
    if school == "mixed_or_unclear":
        return ["single_declared_school_or_form-only_scope"]
    return ["visible_observations"]


def missing_fields(payload: dict[str, object], text: str, school: str) -> list[str]:
    missing: list[str] = []
    if school in {"xuankong_feixing", "bazhai", "sanhe_sanyuan"}:
        if not has_direction_source(payload, text):
            missing.append("direction_source")
    if school == "xuankong_feixing":
        if not has_direction(payload, text):
            missing.append("facing_direction")
        if not has_time_basis(payload, text) and payload.get("external_liqi_chart") is not True:
            missing.append("time_basis_or_external_chart")
    elif school == "bazhai":
        if not has_direction(payload, text):
            missing.append("facing_or_sitting_direction")
        if not has_occupant_basis(payload, text):
            missing.append("occupant_or_house_mingua_basis")
    elif school == "sanhe_sanyuan":
        if not payload.get("terrain_or_water_context"):
            missing.append("terrain_or_water_context")
        if not payload.get("source_scope"):
            missing.append("source_scope")
    elif school == "date_selection":
        if not payload.get("event_type"):
            missing.append("event_type")
        if not payload.get("date_range"):
            missing.append("date_range")
    elif school == "mixed_or_unclear":
        missing.append("single_declared_school")
    return missing


def reframe(school: str, risks: list[str], missing: list[str]) -> str:
    if "unsafe_structural_action" in risks:
        return "先暂停风水建议，改为现实房屋安全：承重、燃气、电路、消防必须找合格专业人员。"
    if "professional_replacement" in risks:
        return "风水不能替代医疗、法律或财务判断；可改为整理空间如何支持作息、专注和低风险行动。"
    if "deterministic_wealth_or_illness" in risks:
        return "不把理气术语写成发财、破财、生病或灾祸保证；可改为观察空间动线、卫生、收纳和压力感。"
    if school == "mixed_or_unclear":
        return "先选择一个派别或退回形法审视，不混用玄空、八宅、三合等规则硬断。"
    if missing:
        return "理气前提不足时，不排盘也不下吉凶结论；可先补字段，或改做形法/八卦象征审视。"
    if school == "xingfa":
        return "可继续做形法审视：先看可见事实，再给低成本、可逆调整。"
    if school == "symbolic_bagua":
        return "可继续做八卦方位象征映射，但必须说明方位来源和非决定论限制。"
    return "可在已声明派别和来源的前提下做方法受限的理气解释，不给财富、疾病或婚恋定论。"


def guard(payload: dict[str, object]) -> dict[str, object]:
    text = str(payload.get("request_text", payload.get("space_description", ""))).strip()
    if not text:
        raise ValueError("request_text or space_description is required")

    schools = detect_schools(text)
    school = requested_school(payload, text)
    risks = detect_risks(text)
    missing = missing_fields(payload, text, school)
    mixed = len([item for item in schools if item not in {"xingfa", "symbolic_bagua"}]) > 1 or school == "mixed_or_unclear"
    if mixed and "mixed_school_rules" not in risks:
        risks.append("mixed_school_rules")
    can_continue_liqi = not mixed and (method_level(school) != "liqi_school" or (not missing and not risks))
    can_continue_fengshui = "unsafe_structural_action" not in risks

    warnings: list[str] = []
    if mixed:
        warnings.append("检测到多个理气派别或派别不清；不要混派硬断。")
    if missing:
        warnings.append("理气解释缺少必要前提；只能补问、记录外部盘，或退回形法审视。")
    if "deterministic_wealth_or_illness" in risks:
        warnings.append("不得把五黄、飞星、宅命或方位写成破财、生病、发财或灾祸保证。")
    if "unsafe_structural_action" in risks:
        warnings.append("承重、燃气、电路、消防等必须先交给合格专业人员。")

    return {
        "system": "feng_shui",
        "request_text": text,
        "detected_schools": schools,
        "requested_school": school,
        "method_level": method_level(school),
        "required_fields": required_fields(school),
        "missing_fields": missing,
        "risk_flags": risks,
        "can_continue_liqi": can_continue_liqi,
        "can_continue_fengshui": can_continue_fengshui,
        "reframed_scope": reframe(school, risks, missing),
        "warnings": warnings,
        "limits": [
            "风水理气派别规则必须声明来源和前提，不混用玄空、八宅、三合、三元或择日规则。",
            "缺少坐向、方位来源、时间依据或外部盘时，不排盘、不补盘、不下吉凶结论。",
            "不得把风水术语写成疾病、财富、婚恋、灾祸或房屋安全的确定判断。",
        ],
        "next_steps": [
            "run_mystic_intake_triage_first",
            "if_missing_method_fields_reframe_to_form_audit_or_ask_for_source",
            "record_visible_facts_with_fengshui_observation_recorder",
            "use_fengshui_bagua_mapper_only_for_symbolic_direction_mapping",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"request_text": raw}
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
    parser.add_argument("--text", help="Feng Shui school-specific request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to text or JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
