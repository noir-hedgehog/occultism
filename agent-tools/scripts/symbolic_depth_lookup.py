#!/usr/bin/env python3
"""Look up cross-domain symbolic interpretation depth patterns."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


DEPTH_ENTRIES: list[dict[str, Any]] = [
    {
        "entry_id": "tarot-single-card-to-spread",
        "domain": "tarot",
        "title": "单牌进入牌阵",
        "symbols": ["牌位", "正逆位", "大阿尔卡那", "小阿尔卡那"],
        "use_when": ["用户已有抽牌", "需要把单牌关键词落到牌位和现实行动"],
        "interpretation_steps": [
            "先读取牌阵位置，而不是直接套单牌关键词。",
            "再看正逆位，把顺畅、阻滞、过度或内化写成状态。",
            "最后给一个可观察、可撤回的小行动。",
        ],
        "boundary": "不把牌义写成必然事件，不替代医疗、法律、财务或人身安全判断。",
        "example": "建议位出现倒吊人，可写为先暂停并换视角，而不是断言事情无法推进。",
        "sop_links": ["知识库/SOP/01-塔罗解读.md", "知识库/流派/塔罗牌阵案例与逆位策略.md"],
        "toolchain": ["tarot_card_lookup", "tarot_interpretation_planner", "mystic_output_lint"],
    },
    {
        "entry_id": "tarot-reversal-cluster",
        "domain": "tarot",
        "title": "多张逆位的系统性读法",
        "symbols": ["逆位", "阻滞", "节奏", "减压"],
        "use_when": ["牌阵里多张逆位", "用户期待直接好坏判断"],
        "interpretation_steps": [
            "把多张逆位视为系统节奏不稳或信息未整合。",
            "按牌位区分内在卡点、外部阻碍和建议修正。",
            "优先建议澄清、休整、补资源，而不是扩大成灾祸。",
        ],
        "boundary": "逆位不是坏事标签，不能恐吓用户或替用户判断他人恶意。",
        "example": "关系牌阵多张逆位时，可提示沟通节奏和边界需要重整，不写成对方一定背叛。",
        "sop_links": ["知识库/流派/塔罗牌阵案例与逆位策略.md"],
        "toolchain": ["tarot_interpretation_planner", "tarot_combination_planner", "mystic_output_lint"],
    },
    {
        "entry_id": "yijing-hexagram-line-layering",
        "domain": "yijing",
        "title": "卦象与动爻分层",
        "symbols": ["本卦", "动爻", "变卦", "上下卦"],
        "use_when": ["用户已有卦号或起卦记录", "需要从卦义进入具体行动"],
        "interpretation_steps": [
            "先说明本卦描述的总体结构。",
            "再用动爻定位变化压力或关键位置。",
            "最后把变卦作为趋势提醒，而不是确定结局。",
        ],
        "boundary": "不把卦象写成绝对预言；高风险问题必须回到专业资源和现实证据。",
        "example": "既济三爻可写为完成后的转换压力，需要复盘和维护，而不是保证成功后必定出事。",
        "sop_links": ["知识库/SOP/04-易经占问.md", "知识库/流派/易经64卦速查.md", "知识库/流派/易经384爻索引.md", "知识库/流派/易经原典注疏来源规范.md"],
        "toolchain": ["yijing_hexagram_lookup", "yijing_line_lookup", "yijing_source_reference_guard", "mystic_output_lint"],
    },
    {
        "entry_id": "yijing-question-reframe",
        "domain": "yijing",
        "title": "复合问题改写为一事一问",
        "symbols": ["一事一问", "重复占问", "复合问题", "问题边界"],
        "use_when": ["用户把感情、财务、健康混在一个问题里", "用户反复占同一件事"],
        "interpretation_steps": [
            "先暂停起卦，标出问题混杂或重复占问点。",
            "请用户选一个低风险、可行动的焦点。",
            "把问题改写为现阶段可观察的选择或准备。",
        ],
        "boundary": "不为贷款、医疗、诉讼、人身安全等高风险决策直接起卦下结论。",
        "example": "把“我该不该辞职贷款创业并预测结果”改写为“现阶段我需要核对哪些资源和风险”。",
        "sop_links": ["知识库/SOP/04-易经占问.md"],
        "toolchain": ["yijing_question_guard", "yijing_casting_method_advisor", "yijing_casting_simulator", "mystic_output_lint"],
    },
    {
        "entry_id": "qimen-focus-palace-layering",
        "domain": "qimen",
        "title": "用神宫位分层读盘",
        "symbols": ["用神", "九宫", "门", "星", "神", "天盘干", "地盘干"],
        "use_when": ["外部盘式完整", "用户问项目、关系、时机或寻找"],
        "interpretation_steps": [
            "先记录派别、起局来源和盘式完整性。",
            "优先读用户或外部盘已标注用神，再读候选用神。",
            "按宫内门、星、神、干组合转成现实观察和下一步。",
        ],
        "boundary": "派别不明或盘式不完整时只能说明方法限制，不混派硬断。",
        "example": "项目问题可优先看时干、值使门和开门线索，但只能写推进条件和阻滞点。",
        "sop_links": ["知识库/SOP/05-奇门遁甲局势分析.md", "知识库/流派/奇门用神与盘式解读骨架.md"],
        "toolchain": ["qimen_method_guard", "qimen_chart_record", "qimen_focus_selector", "mystic_output_lint"],
    },
    {
        "entry_id": "qimen-method-limit",
        "domain": "qimen",
        "title": "奇门方法前提守门",
        "symbols": ["转盘", "飞盘", "置闰", "拆补", "真太阳时", "节气"],
        "use_when": ["用户要求直接排盘", "用户未说明派别和时间策略"],
        "interpretation_steps": [
            "先确认排盘方法、时区、真太阳时和节气来源。",
            "缺方法时不要生成盘式，只能请用户补充或提供外部盘。",
            "收到外部盘后记录来源和限制。",
        ],
        "boundary": "不能在方法前提缺失时假装已排盘，也不能把不同派别规则混成一个确定结论。",
        "example": "用户只说“现在起奇门盘”时，先询问转盘/飞盘和时间策略，或请其贴外部盘。",
        "sop_links": ["知识库/流派/奇门遁甲.md", "知识库/流派/奇门用神与盘式解读骨架.md"],
        "toolchain": ["qimen_method_guard", "qimen_chart_record"],
    },
    {
        "entry_id": "fengshui-visible-facts-to-bagua",
        "domain": "fengshui",
        "title": "可见事实到八卦方位",
        "symbols": ["方位", "八卦", "空间事实", "动线", "采光", "杂物"],
        "use_when": ["用户描述房间或上传空间观察", "需要把方位象征落到低风险调整"],
        "interpretation_steps": [
            "先记录可见事实，不先贴术语标签。",
            "确认空间类型、方位和用户关切。",
            "把八卦象征转成整理、照明、动线和可逆摆放建议。",
        ],
        "boundary": "不承诺发财、转运或治病；燃气、电路、结构安全先转专业处理。",
        "example": "东南方文件堆积可写为资源区象征拥堵，建议整理文件与账单，而不是保证财运提升。",
        "sop_links": ["知识库/SOP/02-风水空间审视.md", "知识库/流派/风水阳宅案例库.md", "知识库/流派/风水八卦方位映射.md"],
        "toolchain": ["fengshui_observation_recorder", "fengshui_yangzhai_case_library", "fengshui_bagua_mapper", "fengshui_recommendation_ranker", "mystic_output_lint"],
    },
    {
        "entry_id": "fengshui-recommendation-risk-ranking",
        "domain": "fengshui",
        "title": "风水建议风险排序",
        "symbols": ["成本", "可逆性", "安全", "租房限制", "低风险调整"],
        "use_when": ["用户想立刻改造空间", "建议包含搬动家具或物品"],
        "interpretation_steps": [
            "先排除安全隐患和不可逆改造。",
            "按低成本、低风险、可撤回优先排序。",
            "把建议写成试验周期和观察指标。",
        ],
        "boundary": "不建议破坏承重结构、私改电路燃气或制造消防风险。",
        "example": "先试一周清理床边杂物和改善照明，再观察睡眠感受，不直接要求大拆大改。",
        "sop_links": ["知识库/SOP/07-风水观察记录规范.md"],
        "toolchain": ["fengshui_space_checklist", "fengshui_yangzhai_case_library", "fengshui_recommendation_ranker"],
    },
    {
        "entry_id": "mingli-symbol-to-focus",
        "domain": "mingli",
        "title": "命理术语到分析焦点",
        "symbols": ["天干", "地支", "十神", "宫位", "主星"],
        "use_when": ["用户问单个八字或紫微术语", "用户想把术语用于自我理解"],
        "interpretation_steps": [
            "先确认术语类别，避免同名歧义。",
            "把术语解释成象征语言和反思问题。",
            "结合用户焦点给非标签化行动提示。",
        ],
        "boundary": "不做终身定性、寿命、婚育、灾祸或职业成败的确定判断。",
        "example": "七杀可解释为压力、边界和执行力议题，不写成此人一生凶险。",
        "sop_links": ["知识库/SOP/06-命理咨询边界.md", "知识库/流派/命理象征索引.md"],
        "toolchain": ["bazi_ziwei_intake_guard", "mingli_symbol_lookup", "mystic_output_lint"],
    },
    {
        "entry_id": "mingli-privacy-aware-chart",
        "domain": "mingli",
        "title": "出生资料与隐私边界",
        "symbols": ["出生日期", "出生时间", "出生地点", "第三方同意", "未成年人"],
        "use_when": ["用户提供精确出生资料", "用户想看第三方或未成年人命盘"],
        "interpretation_steps": [
            "先判断是否本人、是否第三方同意、是否未成年人。",
            "只记录排盘必要字段，不保留身份证、联系方式等敏感信息。",
            "输出使用倾向和反思语言，避免标签化。",
        ],
        "boundary": "第三方无同意时不做具体命盘；未成年人只做温和、非定型的支持性语言。",
        "example": "前任精确生日无同意时，改为解释术语或关系边界，不分析对方命盘。",
        "sop_links": ["知识库/SOP/08-命理排盘参数记录.md"],
        "toolchain": ["bazi_ziwei_intake_guard", "bazi_ziwei_chart_record", "mystic_output_lint"],
    },
    {
        "entry_id": "ritual-fear-to-low-risk-protocol",
        "domain": "ritual",
        "title": "恐惧请求转低风险象征流程",
        "symbols": ["驱邪", "净化", "搬家", "睡眠", "告别", "空间压迫"],
        "use_when": ["用户害怕脏东西或要求驱邪", "请求可转为低风险整理与安定流程"],
        "interpretation_steps": [
            "先检查是否有火、烟、刀具、放血、封闭空间或跟踪伤害风险。",
            "危险请求必须拒绝具体步骤并解释安全原因。",
            "改给通风、整理、照明、写下担忧、联系现实支持等低风险协议。",
        ],
        "boundary": "不提供危险仪式、恐吓性断言或替代心理/医疗/安全求助的承诺。",
        "example": "把封闭空间烧纸驱邪改为白天通风、清理入口、写下搬家祝愿和联系可信朋友。",
        "sop_links": ["知识库/SOP/03-空间净化与驱邪安全咨询.md", "知识库/流派/仪式低风险真实案例集.md"],
        "toolchain": ["ritual_safety_check", "ritual_source_guard", "ritual_low_risk_protocol", "mystic_output_lint"],
    },
    {
        "entry_id": "ritual-source-claim-guard",
        "domain": "ritual",
        "title": "民俗来源声明守门",
        "symbols": ["地区来源", "宗教来源", "商业来源", "个人经验", "禁忌声明"],
        "use_when": ["用户要求某地某教派的仪式", "资料来源不清或含商业化断言"],
        "interpretation_steps": [
            "先标注来源类型：地区、宗教、现代商业、个人经验或未知。",
            "只保留低风险象征性内容，并说明不是权威宗教指令。",
            "危险步骤一律移除，改写为安全替代。",
        ],
        "boundary": "不冒充宗教权威，不编造地方习俗，不输出危险材料和禁忌恐吓。",
        "example": "未知来源的“午夜焚烧符纸”只能改写成白天整理空间和表达愿望。",
        "sop_links": ["知识库/流派/民俗仪式资料来源规范.md", "知识库/流派/地区宗教来源样例.md"],
        "toolchain": ["ritual_source_example_lookup", "ritual_source_guard", "mystic_output_lint"],
    },
]

VALID_DOMAINS = sorted({entry["domain"] for entry in DEPTH_ENTRIES})
DOMAIN_ALIASES = {
    "feng_shui": "fengshui",
    "feng-shui": "fengshui",
    "bazi": "mingli",
    "ziwei": "mingli",
    "ritual_safety": "ritual",
    "ritual-safety": "ritual",
}


def normalize(value: str) -> str:
    return value.strip().lower().replace(" ", "").replace("　", "")


def score_entry(entry: dict[str, Any], query: str) -> int:
    if not query:
        return 1
    haystack = " ".join(
        [
            entry["entry_id"],
            entry["title"],
            entry["domain"],
            " ".join(entry["symbols"]),
            " ".join(entry["use_when"]),
            entry["example"],
        ]
    )
    compact = normalize(haystack)
    score = 0
    for token in [part for part in re_split_query(query) if part]:
        if token in compact:
            score += 1
    return score


def re_split_query(query: str) -> list[str]:
    compact = normalize(query)
    for sep in [",", "，", ";", "；", "/", "|"]:
        compact = compact.replace(sep, " ")
    return compact.split()


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    domain = normalize(str(payload.get("domain", "")))
    domain = DOMAIN_ALIASES.get(domain, domain)
    query = str(payload.get("query", payload.get("symbol", "")))
    limit = int(payload.get("limit", 5) or 5)
    if limit < 1 or limit > 12:
        raise ValueError("limit must be between 1 and 12")
    if domain and domain not in VALID_DOMAINS:
        raise ValueError(f"unknown domain: {domain}")

    candidates = [entry for entry in DEPTH_ENTRIES if not domain or entry["domain"] == domain]
    scored = [(score_entry(entry, query), entry) for entry in candidates]
    matches = [entry for score, entry in sorted(scored, key=lambda item: (-item[0], item[1]["entry_id"])) if score > 0]
    matches = matches[:limit]

    return {
        "query": query,
        "domain": domain or "all",
        "match_count": len(matches),
        "entries": matches,
        "limits": [
            "深度矩阵提供解释层级、边界和案例，不生成占断结论。",
            "命中条目仍需结合对应 SOP、原始记录工具和 mystic_output_lint。",
            "涉及医疗、法律、财务、人身安全、第三方隐私或危险仪式时，安全边界优先。",
        ],
        "next_steps": [
            "load_relevant_sop",
            "run_domain_specific_record_or_lookup_tool",
            "draft_with_boundary_and_example_language",
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
    raise ValueError("Provide --domain, --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", help=f"Optional domain: {', '.join(VALID_DOMAINS)}")
    parser.add_argument("--query", help="Symbol, scenario, or interpretation layer to search.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum entries to return, 1-12.")
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
