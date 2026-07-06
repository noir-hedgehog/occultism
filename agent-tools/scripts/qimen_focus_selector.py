#!/usr/bin/env python3
"""Select Qimen focus targets and interpretation order from a recorded chart."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Iterable

import qimen_chart_record


DOMAIN_RULES = {
    "project_career": ("项目", "工作", "事业", "推进", "合作", "客户", "面试", "offer", "团队"),
    "relationship": ("关系", "感情", "复合", "伴侣", "对方", "他", "她", "沟通"),
    "money_business": ("生意", "业绩", "订单", "销售", "收入", "客流", "钱", "商业"),
    "travel_move": ("出行", "旅行", "搬家", "迁移", "路线", "去不去", "动身"),
    "timing": ("什么时候", "何时", "时机", "节奏", "择时", "多久"),
    "lost_item": ("丢", "找不到", "遗失", "失物"),
}

RISK_RULES = {
    "professional_finance": ("股票", "贷款", "借贷", "赌博", "彩票", "梭哈", "币圈", "投资"),
    "professional_health": ("医生", "用药", "手术", "怀孕", "诊断", "癌", "病"),
    "professional_legal": ("律师", "起诉", "合同", "官司", "刑事", "移民"),
    "crisis": ("自杀", "自残", "活不下去", "伤害", "家暴", "跟踪", "被威胁"),
    "coercion": ("控制他", "控制她", "让他爱我", "让她爱我", "诅咒", "报复"),
}

DOMAIN_GUIDANCE = {
    "project_career": {
        "primary_labels": ("existing_focus", "hour_stem", "duty_door", "open_door"),
        "lens": "看任务推进、外部机会、阻滞点和下一步可验证行动。",
    },
    "relationship": {
        "primary_labels": ("existing_focus", "day_stem", "hour_stem"),
        "lens": "看双方互动结构和边界，不替对方下确定结论。",
    },
    "money_business": {
        "primary_labels": ("existing_focus", "life_door", "open_door", "hour_stem"),
        "lens": "只看商业资源、客流和执行条件，不替代投资或借贷判断。",
    },
    "travel_move": {
        "primary_labels": ("existing_focus", "open_door", "rest_door", "hour_stem"),
        "lens": "看行动路径、通行条件、延迟和现实准备。",
    },
    "timing": {
        "primary_labels": ("existing_focus", "hour_stem", "duty_door"),
        "lens": "看节奏、可观察信号和需要等待/推进的条件。",
    },
    "lost_item": {
        "primary_labels": ("existing_focus", "hour_stem", "rest_door"),
        "lens": "只做寻找思路和排查路径，不保证找回。",
    },
    "general": {
        "primary_labels": ("existing_focus", "hour_stem", "day_stem", "duty_door"),
        "lens": "先确认问题对象，再从值符/值使、日干/时干和相关宫位建立读盘顺序。",
    },
}


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_domain(text: str) -> str:
    for domain, keywords in DOMAIN_RULES.items():
        if contains_any(text, keywords):
            return domain
    return "general"


def detect_risks(text: str) -> list[str]:
    return [risk for risk, keywords in RISK_RULES.items() if contains_any(text, keywords)]


def normalize_chart(payload: dict[str, Any]) -> dict[str, Any]:
    chart = payload.get("chart_record")
    if isinstance(chart, dict):
        return chart
    if isinstance(payload.get("palaces"), list):
        return qimen_chart_record.record(payload)
    raise ValueError("chart_record or palaces is required")


def palace_lookup(chart: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {
        int(item["palace"]): item
        for item in chart.get("palaces", [])
        if isinstance(item, dict) and int(item.get("palace", 0) or 0) in range(1, 10)
    }


def summarize_palace(palace: dict[str, Any] | None) -> dict[str, str]:
    if not palace:
        return {}
    return {
        "trigram": str(palace.get("trigram", "")),
        "door": str(palace.get("door", "")),
        "star": str(palace.get("star", "")),
        "deity": str(palace.get("deity", "")),
        "earth_stem": str(palace.get("earth_stem", "")),
        "heaven_stem": str(palace.get("heaven_stem", "")),
    }


def find_by_field(chart: dict[str, Any], field: str, value: str) -> int:
    if not value:
        return 0
    for palace in chart.get("palaces", []):
        if str(palace.get(field, "")) == value:
            return int(palace.get("palace", 0) or 0)
    return 0


def add_candidate(
    candidates: list[dict[str, Any]],
    seen: set[tuple[str, int, str]],
    label: str,
    palace_id: int,
    selector: str,
    confidence: str,
    reason: str,
    lens: str,
    palaces: dict[int, dict[str, Any]],
) -> None:
    key = (label, palace_id, selector)
    if palace_id < 0 or palace_id > 9 or key in seen:
        return
    seen.add(key)
    candidates.append(
        {
            "label": label,
            "palace": palace_id,
            "selector": selector,
            "confidence": confidence,
            "reason": reason,
            "palace_summary": summarize_palace(palaces.get(palace_id)),
            "interpretation_lens": lens,
        }
    )


def build_candidates(chart: dict[str, Any], domain: str) -> list[dict[str, Any]]:
    palaces = palace_lookup(chart)
    candidates: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()
    domain_lens = DOMAIN_GUIDANCE[domain]["lens"]

    for target in chart.get("focus_targets", []):
        if not isinstance(target, dict):
            continue
        palace_id = int(target.get("palace", 0) or 0)
        add_candidate(
            candidates,
            seen,
            str(target.get("label") or "existing_focus"),
            palace_id,
            "provided_focus_target",
            "high" if palace_id else "medium",
            str(target.get("reason") or "用户或外部盘已标注用神/关注宫位。"),
            domain_lens,
            palaces,
        )

    day_stem = str(chart.get("day_stem", "")).strip()
    hour_stem = str(chart.get("hour_stem", "")).strip()
    duty_door = str(chart.get("duty_door", "")).strip()
    duty_star = str(chart.get("duty_star", "")).strip()

    for label, field, value, reason in (
        ("day_stem", "heaven_stem", day_stem, "日干常作为求测者或自身状态的候选观察点。"),
        ("hour_stem", "heaven_stem", hour_stem, "时干常作为事情、当下触发点或行动对象的候选观察点。"),
        ("duty_door", "door", duty_door, "值使门可作为行动路径和事件门类的候选观察点。"),
        ("duty_star", "star", duty_star, "值符星可作为局面主调或关键资源的候选观察点。"),
    ):
        if not value:
            continue
        palace_id = find_by_field(chart, field, value)
        if not palace_id:
            continue
        add_candidate(candidates, seen, label, palace_id, f"{field}={value}", "medium", reason, domain_lens, palaces)

    for label, door, reason in (
        ("life_door", "生门", "生门可作为资源、经营、生计和增长条件的候选观察点。"),
        ("open_door", "开门", "开门可作为机会、打开局面、沟通和外部入口的候选观察点。"),
        ("rest_door", "休门", "休门可作为休整、路径、停留和寻找线索的候选观察点。"),
    ):
        palace_id = find_by_field(chart, "door", door)
        if not palace_id:
            continue
        add_candidate(candidates, seen, label, palace_id, f"door={door}", "low", reason, domain_lens, palaces)

    preferred = DOMAIN_GUIDANCE[domain]["primary_labels"]
    candidates.sort(
        key=lambda item: (
            0 if item["selector"] == "provided_focus_target" else 1,
            preferred.index(item["label"]) if item["label"] in preferred else len(preferred),
            {"high": 0, "medium": 1, "low": 2}.get(str(item["confidence"]), 3),
            int(item["palace"] or 99),
        )
    )
    return candidates


def missing_fields(chart: dict[str, Any]) -> list[str]:
    missing = []
    if not chart.get("focus_targets"):
        missing.append("focus_targets")
    if not chart.get("day_stem"):
        missing.append("day_stem")
    if not chart.get("hour_stem"):
        missing.append("hour_stem")
    if not chart.get("duty_door"):
        missing.append("duty_door")
    if not chart.get("duty_star"):
        missing.append("duty_star")
    if len(chart.get("palaces", [])) < 9:
        missing.append("complete_nine_palaces")
    return missing


def select(payload: dict[str, Any]) -> dict[str, Any]:
    request_text = str(payload.get("question_text", payload.get("request_text", ""))).strip()
    chart = normalize_chart(payload)
    chart_errors = list(chart.get("errors", []))
    chart_warnings = list(chart.get("warnings", []))
    is_chart_valid = bool(chart.get("is_valid", not chart_errors))
    domain = detect_domain(request_text or str(chart.get("question_text", "")))
    risks = detect_risks(request_text)
    missing = missing_fields(chart)
    candidates = build_candidates(chart, domain) if is_chart_valid else []
    blocking_risks = {"crisis", "coercion", "professional_health", "professional_legal", "professional_finance"}
    can_continue = is_chart_valid and any(int(item["palace"]) > 0 for item in candidates) and not (set(risks) & blocking_risks)

    warnings = list(chart_warnings)
    if risks:
        warnings.append("请求含高风险或专业替代信号；奇门只能作为象征性局势整理，不能替代现实专业判断。")
    if "focus_targets" in missing:
        warnings.append("未提供人工用神；当前结果为工具按字段生成的候选用神。")
    if not candidates and is_chart_valid:
        warnings.append("盘式字段不足，无法稳定选择候选用神。")

    return {
        "question_text": request_text or str(chart.get("question_text", "")),
        "question_domain": domain,
        "risk_flags": risks,
        "can_continue_qimen_focus": can_continue,
        "chart_is_valid": is_chart_valid,
        "chart_errors": chart_errors,
        "missing_fields": missing,
        "focus_candidates": candidates,
        "interpretation_order": [
            "confirm_method_and_chart_integrity",
            "read_existing_focus_targets_first",
            "compare_day_stem_and_hour_stem_palaces",
            "read_duty_door_and_duty_star_as_situation_frame",
            "use_domain_specific_door_candidates_as_secondary_clues",
            "map_symbols_to_grounded_actions",
        ],
        "warnings": warnings,
        "limits": [
            "This tool selects focus candidates from recorded fields; it does not compute a Qimen chart.",
            "Different Qimen schools may choose Yongshen differently; keep school and method limits visible.",
            "Do not use Qimen output as medical, legal, financial, emergency, or coercive decision authority.",
        ],
        "next_steps": [
            "resolve_chart_errors_or_missing_fields",
            "confirm_focus_targets_with_user_or_source",
            "record_confirmed_focus_targets_with_qimen_chart_record",
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
    parser.add_argument("--json", help="JSON input with chart_record or qimen_chart_record fields.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = select(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["chart_is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
