#!/usr/bin/env python3
"""Look up safe cross-domain interpretation cases for mystic-agent workflows."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


CASES: list[dict[str, Any]] = [
    {
        "case_id": "tarot-three-card-career-block",
        "domain": "tarot",
        "skill": "tarot-symbolic-reading",
        "scenario": "normal",
        "prompt_pattern": "用户问工作卡住，并接受三张状态牌阵。",
        "symbol_stack": ["三张状态牌阵", "现状", "阻碍", "建议", "逆位"],
        "safe_interpretation": [
            "先按牌位拆成现状、阻碍和建议。",
            "把逆位写成节奏、沟通或资源上的卡点。",
            "最后给一个低风险行动，例如整理信息、安排沟通或降低负荷。",
        ],
        "sample_language": "这组牌更像是在提醒你先看清工作中的阻碍和资源，不是断言结果。建议先做一次任务优先级整理。",
        "avoid_language": ["你一定会被辞退", "牌面保证你会成功", "不用看现实证据"],
        "recommended_tools": ["tarot_spread_selector", "tarot_interpretation_planner", "tarot_combination_planner", "symbolic_depth_lookup", "mystic_output_lint"],
        "review_questions": ["牌位是否先于单牌关键词？", "建议是否可执行且可撤回？"],
    },
    {
        "case_id": "tarot-two-offers-choice",
        "domain": "tarot",
        "skill": "tarot-symbolic-reading",
        "scenario": "boundary_reframed",
        "prompt_pattern": "用户要求塔罗替自己选 A/B offer。",
        "symbol_stack": ["二选一路径", "决策标准", "共同建议"],
        "safe_interpretation": [
            "不替用户做决定。",
            "把 A/B 牌位读成条件、提醒和需要补充的信息。",
            "输出共同决策标准和下一步核对清单。",
        ],
        "sample_language": "我不会替你选边，但可以把两条路径各自的条件和风险整理出来，帮助你回到自己的决策标准。",
        "avoid_language": ["选 A 一定发财", "B 一定后悔", "塔罗已经替你决定"],
        "recommended_tools": ["tarot_spread_selector", "tarot_interpretation_planner", "mystic_output_lint"],
        "review_questions": ["是否保留用户自主决策？", "是否避开财务/法律专业替代？"],
    },
    {
        "case_id": "tarot-relationship-third-person",
        "domain": "tarot",
        "skill": "tarot-symbolic-reading",
        "scenario": "privacy_boundary",
        "prompt_pattern": "用户问对方心里到底怎么想。",
        "symbol_stack": ["关系镜像", "对方可能状态", "互动边界"],
        "safe_interpretation": [
            "对第三方内心只写可能状态。",
            "把重点拉回用户可观察互动、沟通和边界。",
            "不鼓励监控、试探或操控。",
        ],
        "sample_language": "对方牌只能作为互动可能性的镜头，不能替他下定论；更重要的是你能观察到什么、愿意如何沟通。",
        "avoid_language": ["他一定还爱你", "他绝对背叛", "用牌控制他回来"],
        "recommended_tools": ["mystic_intake_triage", "tarot_spread_selector", "mystic_output_lint"],
        "review_questions": ["是否避免读心断言？", "是否阻断操控或跟踪建议？"],
    },
    {
        "case_id": "yijing-compound-career-home-finance",
        "domain": "yijing",
        "skill": "yijing-symbolic-consultation",
        "scenario": "boundary_reframed",
        "prompt_pattern": "用户把跳槽、搬家、贷款投资放在同一卦里。",
        "symbol_stack": ["一事一问", "复合问题", "财务高风险"],
        "safe_interpretation": [
            "先暂停起卦。",
            "指出问题混杂和财务风险。",
            "请用户选择一个低风险、可观察的问题。",
        ],
        "sample_language": "这不是一个适合直接起卦的问题；我们先拆出一个焦点，例如当前工作变化里最需要核对的现实信号。",
        "avoid_language": ["一卦包所有事", "卦象替你决定贷款", "直接按卦辞行动"],
        "recommended_tools": ["yijing_question_guard", "yijing_casting_method_advisor", "symbolic_depth_lookup", "mystic_output_lint"],
        "review_questions": ["是否先拆问题？", "是否阻断高风险财务决策？"],
    },
    {
        "case_id": "yijing-changing-line-pressure",
        "domain": "yijing",
        "skill": "yijing-symbolic-consultation",
        "scenario": "normal",
        "prompt_pattern": "用户已有本卦和一个动爻，想知道变化重点。",
        "symbol_stack": ["本卦", "动爻", "变卦", "现实映射"],
        "safe_interpretation": [
            "本卦描述当前结构。",
            "动爻定位变化压力。",
            "变卦只作为趋势提醒，回到现实行动。",
        ],
        "sample_language": "动爻像是把注意力放在转折位置；它提示你先处理这个阶段的压力点，而不是保证某个结果。",
        "avoid_language": ["此爻必凶", "变卦保证结局", "不用现实沟通"],
        "recommended_tools": ["yijing_hexagram_lookup", "yijing_line_lookup", "yijing_source_reference_guard", "mystic_output_lint"],
        "review_questions": ["是否区分本卦、动爻、变卦？", "是否避免绝对预言？"],
    },
    {
        "case_id": "yijing-repeated-question",
        "domain": "yijing",
        "skill": "yijing-symbolic-consultation",
        "scenario": "blocked",
        "prompt_pattern": "用户反复问同一关系或结果问题。",
        "symbol_stack": ["重复占问", "焦虑循环", "暂停"],
        "safe_interpretation": [
            "不继续重复起卦。",
            "说明反复占问会放大焦虑和确认偏误。",
            "改为复盘已经得到的信息和现实下一步。",
        ],
        "sample_language": "同一个问题反复占问容易让焦虑替代判断。我们先停下来，整理你已经知道的事实和下一步可做的沟通。",
        "avoid_language": ["一直占到满意为止", "再起一卦覆盖前卦", "卦不准就重来"],
        "recommended_tools": ["yijing_question_guard", "yijing_casting_method_advisor", "mystic_output_lint"],
        "review_questions": ["是否阻断重复占问？", "是否给出替代的整理动作？"],
    },
    {
        "case_id": "qimen-project-external-chart",
        "domain": "qimen",
        "skill": "qimen-chart-consultation",
        "scenario": "normal",
        "prompt_pattern": "用户提供外部奇门盘，标注项目用神。",
        "symbol_stack": ["外部盘", "用神", "九宫", "门星神干"],
        "safe_interpretation": [
            "先记录外部盘来源和方法限制。",
            "优先读取用户标注用神宫。",
            "把门星神干象意转成项目推进条件和可验证行动。",
        ],
        "sample_language": "我按你提供的外部盘做结构观察，不重新发明排盘；项目用神宫可作为优先观察点。",
        "avoid_language": ["我已经自动排出精准盘", "项目一定成功", "不用核对现实进度"],
        "recommended_tools": ["qimen_method_guard", "qimen_chart_record", "qimen_focus_selector", "mystic_output_lint"],
        "review_questions": ["是否记录来源而非伪造排盘？", "是否把象意映射为项目行动？"],
    },
    {
        "case_id": "qimen-missing-school",
        "domain": "qimen",
        "skill": "qimen-chart-consultation",
        "scenario": "blocked",
        "prompt_pattern": "用户要求立即排奇门盘，但缺派别和时间策略。",
        "symbol_stack": ["派别", "节气来源", "真太阳时", "方法守门"],
        "safe_interpretation": [
            "不生成盘式。",
            "列出缺失方法字段。",
            "请用户补充或提供外部盘。",
        ],
        "sample_language": "派别和时间策略不明时，我不能假装已经排盘；你可以补方法，或贴外部盘让我只记录来源。",
        "avoid_language": ["缺方法也能断", "所有派别都一样", "我随便排一个"],
        "recommended_tools": ["qimen_method_guard", "symbolic_depth_lookup"],
        "review_questions": ["是否阻断混派？", "是否给出补充字段？"],
    },
    {
        "case_id": "fengshui-bedroom-mirror-bed",
        "domain": "fengshui",
        "skill": "feng-shui-space-audit",
        "scenario": "normal",
        "prompt_pattern": "用户描述卧室镜子对床、床边堆物、睡眠不稳。",
        "symbol_stack": ["卧室", "镜子", "床位", "动线", "睡眠感受"],
        "safe_interpretation": [
            "先记录可见事实和现实体验。",
            "把传统术语转成光线、反射、动线、压迫感等可观察因素。",
            "建议低成本、可逆调整和观察周期。",
        ],
        "sample_language": "镜面对床可以先从反光、夜间惊扰和心理压迫感理解；建议先遮挡或调整角度试一周。",
        "avoid_language": ["这一定招灾", "必须大拆大改", "保证睡眠立刻变好"],
        "recommended_tools": ["fengshui_observation_recorder", "fengshui_space_checklist", "fengshui_yangzhai_case_library", "fengshui_recommendation_ranker", "mystic_output_lint"],
        "review_questions": ["是否先事实后术语？", "建议是否低成本可逆？"],
    },
    {
        "case_id": "fengshui-southeast-documents",
        "domain": "fengshui",
        "skill": "feng-shui-space-audit",
        "scenario": "normal",
        "prompt_pattern": "用户说东南书桌文件账单很多，关心工作和财务感受。",
        "symbol_stack": ["东南", "巽", "资源", "文件", "账单"],
        "safe_interpretation": [
            "把东南/巽作为资源和流动的象征线索。",
            "建议整理文件、账单和工作流。",
            "不承诺发财或转运。",
        ],
        "sample_language": "东南方可以作为资源整理的提醒：先让文件、账单和待办流动起来，而不是把它写成发财保证。",
        "avoid_language": ["这样一定发财", "摆一个物件就转运", "不用处理账单"],
        "recommended_tools": ["fengshui_yangzhai_case_library", "fengshui_bagua_mapper", "fengshui_recommendation_ranker", "mystic_output_lint"],
        "review_questions": ["是否避免财富保证？", "是否转成现实整理动作？"],
    },
    {
        "case_id": "fengshui-gas-electrical-pause",
        "domain": "fengshui",
        "skill": "feng-shui-space-audit",
        "scenario": "blocked",
        "prompt_pattern": "用户描述燃气异味或插座火花，还想看风水。",
        "symbol_stack": ["燃气", "电路", "现实安全", "暂停风水"],
        "safe_interpretation": [
            "暂停风水解释。",
            "提醒通风、远离火源和联系专业维修或物业。",
            "安全问题处理后再谈空间感受。",
        ],
        "sample_language": "燃气异味和插座火花先按现实安全处理；这一步不做风水判断，请先联系专业人员。",
        "avoid_language": ["这是煞气", "点香化解", "摆件能处理燃气"],
        "recommended_tools": ["fengshui_observation_recorder", "fengshui_space_checklist", "fengshui_yangzhai_case_library", "mystic_output_lint"],
        "review_questions": ["是否安全优先？", "是否阻断明火/香烛建议？"],
    },
    {
        "case_id": "mingli-ten-god-career",
        "domain": "mingli",
        "skill": "mingli-bazi-ziwei-consultation",
        "scenario": "normal",
        "prompt_pattern": "用户问七杀或正官等十神在事业里的象征。",
        "symbol_stack": ["十神", "事业焦点", "压力", "边界", "行动"],
        "safe_interpretation": [
            "先确认术语类别。",
            "用象征语言解释压力、规则、执行或资源主题。",
            "给反思问题，不做职业成败断言。",
        ],
        "sample_language": "七杀可以作为压力、边界和执行力议题来理解；重点是你如何把压力转成清晰规则和行动。",
        "avoid_language": ["你命里注定凶", "必然适合某职业", "一生事业失败"],
        "recommended_tools": ["bazi_ziwei_intake_guard", "mingli_symbol_lookup", "symbolic_depth_lookup", "mystic_output_lint"],
        "review_questions": ["是否避免终身定性？", "是否把术语转为反思问题？"],
    },
    {
        "case_id": "mingli-third-party-birth-data",
        "domain": "mingli",
        "skill": "mingli-bazi-ziwei-consultation",
        "scenario": "blocked",
        "prompt_pattern": "用户提供前任或同事精确出生资料，要求看感情或命盘。",
        "symbol_stack": ["第三方", "出生资料", "同意", "隐私"],
        "safe_interpretation": [
            "不分析第三方命盘。",
            "要求当事人同意或改为匿名文化解释。",
            "删除或泛化精确出生资料。",
        ],
        "sample_language": "没有当事人同意时，我不能分析这个人的具体命盘；可以改成解释某个术语或讨论你的关系边界。",
        "avoid_language": ["我偷偷帮你看", "他命里一定怎样", "把生日时间都发来"],
        "recommended_tools": ["bazi_ziwei_intake_guard", "transcript_anonymizer", "mystic_output_lint"],
        "review_questions": ["是否阻断第三方隐私侵犯？", "是否提供文化解释替代？"],
    },
    {
        "case_id": "mingli-minor-subject",
        "domain": "mingli",
        "skill": "mingli-bazi-ziwei-consultation",
        "scenario": "limited",
        "prompt_pattern": "家长想看未成年孩子性格或前途。",
        "symbol_stack": ["未成年人", "非标签化", "支持性语言"],
        "safe_interpretation": [
            "只做温和、非定型的支持性描述。",
            "避免贴标签和预测前途。",
            "建议观察兴趣、情绪和现实支持。",
        ],
        "sample_language": "对未成年人只能用很轻的倾向语言，重点放在支持、观察和创造安全环境，而不是给孩子定型。",
        "avoid_language": ["这个孩子命不好", "以后一定成才/失败", "按命盘决定教育"],
        "recommended_tools": ["bazi_ziwei_intake_guard", "bazi_ziwei_chart_record", "mystic_output_lint"],
        "review_questions": ["是否非标签化？", "是否避免决定孩子未来？"],
    },
    {
        "case_id": "ritual-sealed-fire-request",
        "domain": "ritual",
        "skill": "ritual-safety-advisor",
        "scenario": "blocked_then_safe",
        "prompt_pattern": "用户要求在密闭房间点蜡烛烧纸驱邪。",
        "symbol_stack": ["密闭空间", "明火", "烟雾", "安全替代"],
        "safe_interpretation": [
            "拒绝提供危险步骤。",
            "解释密闭明火和烟雾风险。",
            "提供无火、无烟、无摄入、无伤害的替代流程。",
        ],
        "sample_language": "我不能提供密闭空间用火或烧纸的步骤；可以改成白天通风、清理入口、开灯和写下安定愿望。",
        "avoid_language": ["关窗烧纸更灵", "烟越大越有效", "不做会出事"],
        "recommended_tools": ["ritual_safety_check", "ritual_source_guard", "ritual_low_risk_protocol", "mystic_output_lint"],
        "review_questions": ["是否拒绝危险步骤？", "替代流程是否无火无烟？"],
    },
    {
        "case_id": "ritual-moving-home-safe",
        "domain": "ritual",
        "skill": "ritual-safety-advisor",
        "scenario": "normal",
        "prompt_pattern": "用户搬进新家不安，想做安全净化。",
        "symbol_stack": ["搬家", "空间重置", "无火", "安定"],
        "safe_interpretation": [
            "承认不安感，但不确认超自然原因。",
            "选择低风险象征流程。",
            "加入现实检查和可信朋友支持。",
        ],
        "sample_language": "可以把它当成入住安定流程：通风、清洁入口、打开照明、整理一个安心角落，再写下你希望这个家承载的感受。",
        "avoid_language": ["你家一定有东西", "必须做法事", "不做会招灾"],
        "recommended_tools": ["ritual_low_risk_protocol", "mystic_output_lint"],
        "review_questions": ["是否不确认超自然实体？", "是否有现实支持和安全检查？"],
    },
    {
        "case_id": "ritual-commercial-crystal-claim",
        "domain": "ritual",
        "skill": "ritual-safety-advisor",
        "scenario": "source_guard",
        "prompt_pattern": "用户引用课程或商家说水晶阵保证转运。",
        "symbol_stack": ["商业来源", "效果保证", "来源声明", "低风险改写"],
        "safe_interpretation": [
            "标注为商业或未知来源。",
            "移除保证转运和恐吓性禁忌。",
            "只保留低风险装饰、提醒或自我整理意义。",
        ],
        "sample_language": "这类说法更像商业化身心灵材料，不能写成保证转运；如果喜欢水晶，只能当作提醒物或装饰。",
        "avoid_language": ["买了必转运", "不买会倒霉", "这是权威宗教要求"],
        "recommended_tools": ["ritual_source_example_lookup", "ritual_source_guard", "mystic_output_lint"],
        "review_questions": ["是否标注来源类型？", "是否移除商业效果保证？"],
    },
]

VALID_DOMAINS = sorted({case["domain"] for case in CASES})
VALID_SCENARIOS = sorted({case["scenario"] for case in CASES})


def normalize(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")


def tokenize(value: str) -> list[str]:
    compact = value.lower()
    for sep in [",", "，", ";", "；", "/", "|", "\n"]:
        compact = compact.replace(sep, " ")
    return [part.strip() for part in compact.split() if part.strip()]


def score_case(case: dict[str, Any], query: str) -> int:
    if not query:
        return 1
    haystack = " ".join(
        [
            case["case_id"],
            case["domain"],
            case["skill"],
            case["scenario"],
            case["prompt_pattern"],
            " ".join(case["symbol_stack"]),
            case["sample_language"],
        ]
    ).lower()
    compact_query = "".join(tokenize(query))
    compact_haystack = "".join(tokenize(haystack))
    score = 3 if compact_query and compact_query in compact_haystack else 0
    score += sum(1 for token in tokenize(query) if token in haystack)
    return score


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    domain = normalize(str(payload.get("domain", "")))
    scenario = normalize(str(payload.get("scenario", "")))
    query = str(payload.get("query", payload.get("text", "")))
    limit = int(payload.get("limit", 6) or 6)
    if limit < 1 or limit > 18:
        raise ValueError("limit must be between 1 and 18")
    if domain and domain not in VALID_DOMAINS:
        raise ValueError(f"unknown domain: {domain}")
    if scenario and scenario not in VALID_SCENARIOS:
        raise ValueError(f"unknown scenario: {scenario}")

    candidates = [
        case
        for case in CASES
        if (not domain or case["domain"] == domain) and (not scenario or case["scenario"] == scenario)
    ]
    matches = [
        case
        for score, case in sorted(
            ((score_case(case, query), case) for case in candidates),
            key=lambda item: (-item[0], item[1]["case_id"]),
        )
        if score > 0
    ][:limit]
    return {
        "tool": "symbolic_case_library",
        "query": query,
        "domain": domain or "all",
        "scenario": scenario or "all",
        "case_count": len(matches),
        "cases": matches,
        "limits": [
            "案例库只提供安全写法和审查问题，不输出占断结论。",
            "案例不替代对应 SOP、记录工具、来源守门或 mystic_output_lint。",
            "新增案例必须包含 avoid_language，防止 agent 学到危险或确定性措辞。",
        ],
        "next_steps": [
            "select_relevant_case",
            "run_recommended_tools",
            "draft_with_sample_language_as_style_boundary",
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
    if args.domain:
        payload["domain"] = args.domain
    if args.scenario:
        payload["scenario"] = args.scenario
    if args.query:
        payload["query"] = args.query
    if args.limit:
        payload["limit"] = args.limit
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --domain, --scenario, --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", help=f"Optional domain: {', '.join(VALID_DOMAINS)}")
    parser.add_argument("--scenario", help=f"Optional scenario: {', '.join(VALID_SCENARIOS)}")
    parser.add_argument("--query", help="Prompt pattern or symbol stack to search.")
    parser.add_argument("--limit", type=int, default=6, help="Maximum cases to return, 1-18.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
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
