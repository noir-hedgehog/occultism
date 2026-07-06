#!/usr/bin/env python3
"""Select Liuyao focus-spirit candidates from question type and recorded chart fields."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Iterable

import liuyao_chart_recorder


DOMAIN_RULES = {
    "project_career": ("项目", "合作", "工作", "事业", "客户", "团队", "推进", "面试", "offer", "阻力"),
    "relationship": ("关系", "感情", "复合", "伴侣", "对象", "喜欢", "分手", "沟通"),
    "money_resources": ("资源", "钱", "收入", "生意", "销售", "订单", "经营", "客户"),
    "documents_study": ("合同", "文书", "考试", "学习", "证书", "材料", "消息", "邮件", "方案"),
    "health_safety": ("身体", "健康", "病", "用药", "手术", "怀孕", "安全"),
    "legal_dispute": ("官司", "起诉", "报警", "律师", "纠纷", "投诉", "合同违约"),
    "lost_item": ("失物", "丢", "找不到", "遗失"),
    "travel_move": ("出行", "搬家", "迁移", "旅行", "路线", "去不去"),
}

RISK_RULES = {
    "professional_finance": ("股票", "贷款", "借贷", "赌博", "彩票", "梭哈", "币圈", "期货", "投资"),
    "medical_or_crisis": ("停药", "用药", "手术", "怀孕", "诊断", "癌", "自杀", "自残", "幻听", "幻视"),
    "legal_or_emergency": ("律师", "起诉", "报警", "刑事", "火灾", "燃气", "触电", "家暴", "被威胁"),
    "coercion_or_privacy": ("控制他", "控制她", "让他爱我", "让她爱我", "查前任", "窥探", "跟踪对方"),
    "deterministic_claim": ("必成", "必败", "一定", "百分百", "必分", "必发财", "必有灾"),
    "supernatural_fear": ("中邪", "有鬼", "诅咒", "冲撞", "报应"),
}

DOMAIN_GUIDANCE = {
    "project_career": {
        "kinships": ("官鬼", "父母", "兄弟", "妻财", "子孙"),
        "lens": "看项目压力、规则责任、文书凭证、团队竞争和可交付产出。",
    },
    "relationship": {
        "kinships": ("官鬼", "妻财", "父母", "兄弟", "子孙"),
        "lens": "先看世应互动和边界；关系类六亲取法需声明性别/派别/问题语境，不窥探对方真实想法。",
    },
    "money_resources": {
        "kinships": ("妻财", "兄弟", "子孙", "父母", "官鬼"),
        "lens": "只看资源、经营条件、消耗和执行反馈，不替代投资、借贷或收益判断。",
    },
    "documents_study": {
        "kinships": ("父母", "官鬼", "子孙", "兄弟", "妻财"),
        "lens": "看资料、规则、考试/审核压力、表达产出和可核验证据。",
    },
    "health_safety": {
        "kinships": ("官鬼", "子孙", "父母", "兄弟", "妻财"),
        "lens": "健康或安全主题只用于提醒现实求助和照护资源，不做诊断或治疗建议。",
    },
    "legal_dispute": {
        "kinships": ("官鬼", "父母", "兄弟", "妻财", "子孙"),
        "lens": "法律纠纷只能整理文件、责任、沟通和求助路径，不替代律师或紧急处理。",
    },
    "lost_item": {
        "kinships": ("父母", "妻财", "子孙", "兄弟", "官鬼"),
        "lens": "失物只做排查路径和线索整理，不保证找回。",
    },
    "travel_move": {
        "kinships": ("父母", "官鬼", "子孙", "妻财", "兄弟"),
        "lens": "看路线、凭证、现实阻滞、安全准备和低风险调整。",
    },
    "general": {
        "kinships": ("世爻", "应爻", "官鬼", "父母", "妻财", "兄弟", "子孙"),
        "lens": "先确认问题类型，再把世应、用神和动爻转成可观察信号。",
    },
}

KINSHIP_REASONS = {
    "父母": "父母爻常作为文书、信息、保护、规则、房屋或资料凭证的候选观察点。",
    "兄弟": "兄弟爻常作为同辈、竞争、消耗、协作或分担的候选观察点。",
    "子孙": "子孙爻常作为产出、缓冲、结果、创造和减压路径的候选观察点。",
    "妻财": "妻财爻常作为资源、现实收益、经营对象或关系对象的候选观察点，但不能作投资/关系定论。",
    "官鬼": "官鬼爻常作为压力、规则、责任、风险或阻滞的候选观察点，不能作疾病/灾祸断言。",
    "世爻": "世爻是用户自身、主观处境和可控行动的基础观察点。",
    "应爻": "应爻是对方、环境、合作方或外部回应的基础观察点。",
}

ROLE_PRIORITY = {"用神": 0, "世爻": 1, "应爻": 2, "原神": 3, "忌神": 4, "仇神": 5}
BLOCKING_RISKS = {"professional_finance", "medical_or_crisis", "legal_or_emergency", "coercion_or_privacy"}


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def normalize_text(value: Any) -> str:
    return str(value or "").strip()


def detect_domain(text: str) -> str:
    for domain, keywords in DOMAIN_RULES.items():
        if contains_any(text, keywords):
            return domain
    return "general"


def detect_risks(text: str) -> list[str]:
    return [risk for risk, keywords in RISK_RULES.items() if contains_any(text, keywords)]


def normalize_chart(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, bool]:
    chart = payload.get("chart_record")
    if isinstance(chart, dict):
        return chart, True
    if "lines" in payload:
        return liuyao_chart_recorder.record(payload), True
    return None, False


def line_positions_for(chart: dict[str, Any] | None, kinship_or_role: str) -> list[dict[str, Any]]:
    if not chart:
        return []
    matches = []
    for line in chart.get("lines", []):
        if not isinstance(line, dict):
            continue
        roles = list(line.get("roles", []))
        if line.get("kinship") != kinship_or_role and kinship_or_role not in roles:
            continue
        matches.append(
            {
                "position": int(line.get("position", 0) or 0),
                "position_label": normalize_text(line.get("position_label")),
                "kinship": normalize_text(line.get("kinship")),
                "spirit": normalize_text(line.get("spirit")),
                "roles": roles,
                "changing": bool(line.get("changing")),
            }
        )
    matches.sort(
        key=lambda item: (
            0 if "用神" in item["roles"] else 1,
            0 if item["changing"] else 1,
            min((ROLE_PRIORITY.get(role, 99) for role in item["roles"]), default=99),
            item["position"],
        )
    )
    return matches


def add_candidate(
    candidates: list[dict[str, Any]],
    seen: set[tuple[str, str]],
    label: str,
    kinship_or_role: str,
    selector: str,
    confidence: str,
    reason: str,
    lens: str,
    chart: dict[str, Any] | None,
    method_notes: list[str] | None = None,
) -> None:
    key = (kinship_or_role, selector)
    if key in seen:
        return
    seen.add(key)
    lines = line_positions_for(chart, kinship_or_role)
    candidates.append(
        {
            "label": label,
            "kinship_or_role": kinship_or_role,
            "selector": selector,
            "confidence": confidence,
            "reason": reason,
            "line_matches": lines,
            "changing_positions": [item["position"] for item in lines if item["changing"]],
            "interpretation_lens": lens,
            "method_notes": method_notes or [],
        }
    )


def build_candidates(chart: dict[str, Any] | None, domain: str, provided_focus: str) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    guidance = DOMAIN_GUIDANCE[domain]
    lens = guidance["lens"]

    if provided_focus:
        add_candidate(
            candidates,
            seen,
            "provided_focus",
            provided_focus,
            "provided_focus_spirit",
            "high",
            "用户、外部盘或上游记录已标注用神；优先保留，但仍需说明取用来源。",
            lens,
            chart,
            ["外部标注不等于唯一正统取法；不同派别可复核。"],
        )

    add_candidate(
        candidates,
        seen,
        "self_line",
        "世爻",
        "role=self_line",
        "high" if chart and line_positions_for(chart, "世爻") else "medium",
        KINSHIP_REASONS["世爻"],
        lens,
        chart,
    )
    add_candidate(
        candidates,
        seen,
        "other_line",
        "应爻",
        "role=other_line",
        "high" if chart and line_positions_for(chart, "应爻") else "medium",
        KINSHIP_REASONS["应爻"],
        lens,
        chart,
    )

    for index, kinship in enumerate(guidance["kinships"]):
        if kinship in {"世爻", "应爻"}:
            continue
        notes = []
        if domain == "relationship" and kinship in {"官鬼", "妻财"}:
            notes.append("关系类取官鬼/妻财需由用户问题、性别语境或派别规则确认；否则先以世应互动为主。")
        add_candidate(
            candidates,
            seen,
            f"domain_{domain}",
            kinship,
            f"question_domain={domain}",
            "medium" if index < 2 else "low",
            KINSHIP_REASONS[kinship],
            lens,
            chart,
            notes,
        )

    preferred = (provided_focus, "世爻", "应爻", *guidance["kinships"])
    candidates.sort(
        key=lambda item: (
            0 if item["selector"] == "provided_focus_spirit" else 1,
            preferred.index(item["kinship_or_role"]) if item["kinship_or_role"] in preferred else len(preferred),
            {"high": 0, "medium": 1, "low": 2}.get(item["confidence"], 9),
            0 if item["line_matches"] else 1,
        )
    )
    return candidates


def select(payload: dict[str, Any]) -> dict[str, Any]:
    request_text = normalize_text(payload.get("question_text", payload.get("request_text")))
    chart, chart_provided = normalize_chart(payload)
    chart_text = normalize_text(chart.get("question_text") if chart else "")
    question_text = request_text or chart_text
    domain = detect_domain(question_text)
    risks = sorted(set(detect_risks(question_text) + (list(chart.get("risk_flags", [])) if chart else [])))
    chart_errors = list(chart.get("errors", [])) if chart else []
    chart_missing = list(chart.get("missing_fields", [])) if chart else []
    chart_is_valid = bool(chart.get("is_valid", False)) if chart else False
    provided_focus = normalize_text(
        payload.get("focus_spirit", payload.get("focus_kinship", chart.get("focus_spirit") if chart else ""))
    )

    candidates = build_candidates(chart, domain, provided_focus)
    can_select_focus = bool(candidates) and not (set(risks) & BLOCKING_RISKS)
    can_continue = can_select_focus and chart_provided and chart_is_valid

    warnings = []
    if not chart_provided:
        warnings.append("未提供六爻盘；当前只生成候选用神，不能进入爻位解读。")
    if chart_provided and not chart_is_valid:
        warnings.append("六爻盘式记录不完整或有错误；先补盘式字段再解释。")
    if risks:
        warnings.append("请求含高风险、决定论或隐私信号时，六爻只能暂停或转为现实支持。")
    if not provided_focus:
        warnings.append("未提供已确认用神；候选用神需要用户或派别规则确认。")
    if domain == "general":
        warnings.append("问题类型不明确；先追问事项类别再确定用神。")

    return {
        "tool": "liuyao_focus_selector",
        "system": "liuyao",
        "question_text": question_text,
        "question_domain": domain,
        "risk_flags": risks,
        "can_select_focus": can_select_focus,
        "can_continue_liuyao_focus": can_continue,
        "chart_provided": chart_provided,
        "chart_is_valid": chart_is_valid,
        "chart_errors": chart_errors,
        "missing_fields": chart_missing,
        "focus_candidates": candidates,
        "interpretation_order": [
            "confirm_one_matter_and_safety_boundary",
            "confirm_chart_source_and_method",
            "confirm_or_choose_focus_spirit_as_candidate",
            "read_self_and_other_lines_before_external_claims",
            "prioritize_provided_focus_and_changing_lines",
            "map_symbols_to_observable_evidence_and_low_risk_actions",
        ],
        "warnings": warnings,
        "limits": [
            "此工具只给出六爻候选用神和读盘顺序，不自动起卦、不补盘、不声明唯一正统取法。",
            "不同六爻派别、性别语境和事项分类可能采用不同取用规则；输出必须保留方法限制。",
            "不得用候选用神替代医疗、法律、财务、危机、人身安全、隐私或操控相关判断。",
        ],
        "next_steps": [
            "resolve_high_risk_or_professional_replacement_first",
            "confirm_candidate_focus_with_user_or_source",
            "record_confirmed_focus_logic_with_liuyao_chart_recorder",
            "lookup_selected_kinship_role_and_position_with_liuyao_symbol_lookup",
            "draft_symbolic_interpretation_and_run_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --json, --file, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON input with question text and optional Liuyao chart fields.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = select(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_select_focus"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
