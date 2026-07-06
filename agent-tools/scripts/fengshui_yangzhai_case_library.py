#!/usr/bin/env python3
"""Look up safe Yangzhai feng shui case patterns for home and shop audits."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


CASES: list[dict[str, Any]] = [
    {
        "case_id": "yangzhai-bedroom-door-mirror-sleep",
        "title": "卧室门冲与镜面干扰",
        "space_type": "bedroom",
        "concern_tags": ["sleep", "pressure"],
        "query_terms": ["卧室", "床", "门冲", "正对门", "镜子", "镜面", "睡不好", "休息"],
        "observable_facts": [
            "床与门形成直线关系，睡前视线容易被入口打断。",
            "镜面或屏幕正对床，夜间反光或通知可能提高警觉。",
            "床边过道若堆放杂物，会增加起夜和整理压力。",
        ],
        "traditional_terms": ["门冲", "镜冲", "床头有靠", "气口"],
        "practical_mapping": [
            "入口直线关系可转译为隐私感和警觉度问题。",
            "镜面干扰可转译为光线、反射和睡前注意力问题。",
            "床边杂物先按动线和安全处理，不写成灾祸。",
        ],
        "low_risk_adjustments": [
            "调整床位或用床头柜/屏风弱化门的直线干扰。",
            "睡前遮挡镜面或移动反光物。",
            "先清出床边一条完整动线，观察一周睡眠感受。",
        ],
        "avoid_language": ["门冲一定伤身", "镜子对床必招灾", "必须大装修才能化解"],
        "recommended_tools": [
            "fengshui_observation_recorder",
            "fengshui_space_checklist",
            "fengshui_recommendation_ranker",
            "mystic_output_lint",
        ],
        "review_questions": ["是否先描述可见事实？", "建议是否低成本、可逆、可观察？"],
        "safety_boundary": "若用户描述连续严重失眠、幻听幻视或强烈恐惧，先转向医疗/心理支持。",
    },
    {
        "case_id": "yangzhai-entrance-dark-clutter",
        "title": "玄关昏暗与入口堵塞",
        "space_type": "entrance",
        "concern_tags": ["pressure", "general"],
        "query_terms": ["玄关", "入口", "大门", "门口", "鞋柜", "暗", "堵", "杂物"],
        "observable_facts": [
            "入口光线不足，进门第一眼信息负荷较重。",
            "鞋包或杂物堵住门后和主通道，影响开门与进出。",
            "入口缺少固定归位区时，杂物容易持续回流。",
        ],
        "traditional_terms": ["气口", "明堂", "堵", "气滞"],
        "practical_mapping": [
            "气口可转译为进出体验、清洁启动成本和第一视觉印象。",
            "明堂不开阔可转译为入口没有缓冲和收纳压力。",
        ],
        "low_risk_adjustments": [
            "清理门后 60-90 厘米开门区和主通道。",
            "增加柔和照明或感应灯。",
            "设置鞋、钥匙、包的固定归位点。",
        ],
        "avoid_language": ["门口堵一定挡财", "玄关暗就会家运差", "摆某个物件保证转运"],
        "recommended_tools": [
            "fengshui_observation_recorder",
            "fengshui_space_checklist",
            "fengshui_recommendation_ranker",
            "mystic_output_lint",
        ],
        "review_questions": ["有没有把财运话术降级为动线/收纳？", "有没有给出可回退的整理动作？"],
        "safety_boundary": "如果入口涉及门锁损坏、被威胁或入室风险，先处理安防而不是风水。",
    },
    {
        "case_id": "yangzhai-kitchen-gas-clutter-safety",
        "title": "厨房灶台、通风与现实安全优先",
        "space_type": "kitchen",
        "concern_tags": ["safety", "pressure"],
        "query_terms": ["厨房", "灶", "灶台", "燃气", "煤气", "插座", "火花", "通风", "油污"],
        "observable_facts": [
            "灶台附近若有易燃物、油污或水渍，优先按厨房安全处理。",
            "燃气异味、插座火花、电线发热属于现实风险。",
            "通风差和潮湿异味需要先排查设备和卫生问题。",
        ],
        "traditional_terms": ["灶", "水火", "洁净", "气"],
        "practical_mapping": [
            "灶位解释必须先让位于燃气、电路、消防和通风安全。",
            "水火不协调可转译为操作台安全、清洁和动线冲突，不作疾病/破财断言。",
        ],
        "low_risk_adjustments": [
            "燃气、电路或火花问题先联系物业、维修或专业人员。",
            "移开灶台周围易燃物并清理油污。",
            "确认排风、窗户和烟道可正常工作。",
        ],
        "avoid_language": ["灶位不好一定破财生病", "摆风水物可以替代检修", "不用找专业人员"],
        "recommended_tools": [
            "fengshui_observation_recorder",
            "fengshui_space_checklist",
            "fengshui_recommendation_ranker",
            "mystic_output_lint",
        ],
        "review_questions": ["是否在传统解释前暂停现实安全风险？", "是否避免用化煞物替代检修？"],
        "safety_boundary": "燃气、电路、明火、霉菌和严重异味必须先停止风水解释并处理现实风险。",
    },
    {
        "case_id": "yangzhai-office-back-door-focus",
        "title": "书房/工位背后无靠与专注干扰",
        "space_type": "office",
        "concern_tags": ["focus", "pressure"],
        "query_terms": ["书房", "办公室", "工位", "办公桌", "背对门", "背后无靠", "专注", "效率"],
        "observable_facts": [
            "座位背后为空或背对门，容易增加被打断感。",
            "桌面堆满文件和线缆，会增加启动任务的视觉负荷。",
            "主通道穿过工作区时，注意力会频繁切换。",
        ],
        "traditional_terms": ["靠山", "门冲", "聚气", "散"],
        "practical_mapping": [
            "靠山可转译为背后支撑、可预期性和安全感。",
            "聚气可转译为当前任务的视觉边界和启动摩擦。",
        ],
        "low_risk_adjustments": [
            "调整座位，让背后有墙、柜或稳定椅背。",
            "桌面只保留当前任务物品，文件分为待办/归档。",
            "用植物、矮柜或屏风降低通道打扰。",
        ],
        "avoid_language": ["背后无靠一定没有贵人", "换座位保证升职", "办公桌决定事业成败"],
        "recommended_tools": [
            "fengshui_observation_recorder",
            "fengshui_space_checklist",
            "fengshui_recommendation_ranker",
            "mystic_output_lint",
        ],
        "review_questions": ["是否把事业判断转成专注和工作流？", "是否保留用户现实选择空间？"],
        "safety_boundary": "若涉及职场法律、劳动争议或严重心理压力，不用风水替代专业支持。",
    },
    {
        "case_id": "yangzhai-shop-entry-cashier-flow",
        "title": "店铺入口、主商品与收银主位",
        "space_type": "shop",
        "concern_tags": ["money", "focus"],
        "query_terms": ["店铺", "门店", "客流", "业绩", "收银", "货架", "入口", "主商品"],
        "observable_facts": [
            "入口被货架或海报遮挡，顾客进门难以理解动线。",
            "主商品不在第一视线内，浏览路径不清楚。",
            "收银或主位暴露在拥挤通道中，会增加打断和安全压力。",
        ],
        "traditional_terms": ["气口", "明堂", "财位", "靠山", "聚气"],
        "practical_mapping": [
            "财位只作为主位和资源区的传统称呼，不承诺营收。",
            "入口明堂可转译为顾客第一印象、动线和展示清晰度。",
        ],
        "low_risk_adjustments": [
            "清出入口视线，让顾客进门能看到主商品和动线。",
            "把主商品或核心服务放在自然停留点。",
            "让收银/主位背后稳定，避免正冲拥挤通道。",
        ],
        "avoid_language": ["这样摆一定发财", "财位摆物保证客流", "风水可替代选品和运营"],
        "recommended_tools": [
            "fengshui_observation_recorder",
            "fengshui_space_checklist",
            "fengshui_recommendation_ranker",
            "mystic_output_lint",
        ],
        "review_questions": ["是否避免营收保证？", "是否把建议转成动线、展示和安全压力？"],
        "safety_boundary": "商业选址、消防、租约、广告合规和财务经营需另行专业判断。",
    },
]


def text_matches(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def score_case(case: dict[str, Any], query: str, space_type: str, concern: str) -> int:
    score = 0
    if query:
        score += sum(2 for term in case["query_terms"] if term.lower() in query.lower())
    if space_type and space_type == case["space_type"]:
        score += 4
    if concern and concern in case["concern_tags"]:
        score += 3
    return score


def select_cases(payload: dict[str, Any]) -> dict[str, Any]:
    query = str(payload.get("query", payload.get("request_text", ""))).strip()
    space_type = str(payload.get("space_type", "")).strip()
    concern = str(payload.get("concern", "")).strip()
    limit = int(payload.get("limit", 3))
    if limit < 1 or limit > 10:
        raise ValueError("limit must be between 1 and 10")

    ranked = []
    for case in CASES:
        score = score_case(case, query, space_type, concern)
        if score or not (query or space_type or concern):
            ranked.append((score, case))
    ranked.sort(key=lambda item: (-item[0], item[1]["case_id"]))
    selected_pairs = ranked[:limit]
    selected = [case for _, case in selected_pairs]
    safety_first = any(score > 0 and "safety" in case["concern_tags"] for score, case in selected_pairs)

    return {
        "tool": "fengshui_yangzhai_case_library",
        "query": query,
        "filters": {"space_type": space_type, "concern": concern, "limit": limit},
        "case_count": len(selected),
        "cases": selected,
        "can_continue_fengshui": not safety_first,
        "warnings": ["safety case matched; handle real-world safety before feng shui interpretation"] if safety_first else [],
        "limits": [
            "Yangzhai cases are analogy and workflow references, not proof of wealth, illness, marriage, disaster, or fate.",
            "Describe observable facts before traditional terms.",
            "Prefer low-cost, reversible, non-dangerous adjustments and run mystic_output_lint before final output.",
        ],
        "next_steps": [
            "record_observable_facts_with_fengshui_observation_recorder",
            "run_fengshui_space_checklist",
            "rank_adjustments_with_fengshui_recommendation_ranker",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload.update(json.load(f))
    elif args.query:
        payload["query"] = args.query
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            payload.update(json.loads(raw))
        else:
            payload["query"] = raw
    else:
        raise ValueError("Provide --query, --json, --file, or stdin input")
    if args.space_type:
        payload["space_type"] = args.space_type
    if args.concern:
        payload["concern"] = args.concern
    if args.limit is not None:
        payload["limit"] = args.limit
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Yangzhai scenario query or user request text.")
    parser.add_argument("--space-type", help="Optional space type filter.")
    parser.add_argument("--concern", help="Optional concern filter, e.g. sleep/focus/money/safety.")
    parser.add_argument("--limit", type=int, help="Maximum cases to return, 1-10.")
    parser.add_argument("--json", help="JSON input with query/request_text, space_type, concern, limit.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = select_cases(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
