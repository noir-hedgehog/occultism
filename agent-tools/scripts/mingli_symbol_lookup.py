#!/usr/bin/env python3
"""Lookup safe symbolic prompts for Bazi and Ziwei terms."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


STEMS = {
    "甲": ("yang_wood", "生发、开创、直立、原则", "把主动性落到清晰边界和长期计划。"),
    "乙": ("yin_wood", "柔韧、协调、生长、修复", "用渐进方式调整环境和关系。"),
    "丙": ("yang_fire", "照亮、表达、热情、外显", "把热情转成稳定输出，避免过度燃烧。"),
    "丁": ("yin_fire", "专注、细腻、洞察、温度", "保护专注力，选择少量高质量行动。"),
    "戊": ("yang_earth", "承载、稳定、结构、责任", "检查负担是否过重，并建立支持结构。"),
    "己": ("yin_earth", "滋养、细节、承接、整合", "用小步骤整理资源和习惯。"),
    "庚": ("yang_metal", "决断、切割、规则、压力", "把决断用于取舍，不用于苛责自己或他人。"),
    "辛": ("yin_metal", "精炼、审美、标准、修饰", "校准标准，避免完美主义拖慢行动。"),
    "壬": ("yang_water", "流动、视野、变化、连接", "把复杂信息分流，先确定下一步方向。"),
    "癸": ("yin_water", "感受、潜伏、积累、细流", "尊重恢复周期，先补信息和体力。"),
}

BRANCHES = {
    "子": ("water", "蓄势、流动、夜间、起点", "先观察暗线和节奏。"),
    "丑": ("earth", "储藏、耐心、湿土、等待", "先做基础整理，不急着定论。"),
    "寅": ("wood", "启动、扩张、冲劲、探索", "把启动拆成可执行步骤。"),
    "卯": ("wood", "生长、关系、协调、柔性推进", "用沟通和节奏减少阻力。"),
    "辰": ("earth", "转折、整合、湿土、承载", "处理未收束事项。"),
    "巳": ("fire", "显化、热度、复杂性、转换", "降低急躁，确认信息来源。"),
    "午": ("fire", "高峰、表达、曝光、推动", "注意过热和消耗。"),
    "未": ("earth", "收束、滋养、调整、余波", "把成果落到习惯和维护。"),
    "申": ("metal", "变动、规则、切换、工具", "用流程和工具降低混乱。"),
    "酉": ("metal", "整理、标准、收成、边界", "明确取舍和验收标准。"),
    "戌": ("earth", "守成、边界、燥土、防线", "检查防御是否过强。"),
    "亥": ("water", "潜伏、想象、流动、收纳", "给变化留空间，但保留现实锚点。"),
}

TEN_GODS = {
    "比肩": ("peer_self", "自我、同伴、坚持、竞争", "看自主性与协作边界。"),
    "劫财": ("peer_drive", "争夺、冲动、同辈压力、资源分配", "先谈资源边界，避免冲动投入。"),
    "食神": ("output_ease", "表达、创造、享受、缓冲", "把输出变成可持续练习。"),
    "伤官": ("output_edge", "突破、表达锋芒、挑战规则", "让创新有边界，避免只剩对抗。"),
    "正财": ("direct_resource", "稳定资源、责任、现实经营", "回到预算、时间和可交付成果。"),
    "偏财": ("variable_resource", "机会资源、流动收益、人脉", "区分机会与风险，不做投资结论。"),
    "正官": ("proper_authority", "规则、职责、秩序、名分", "把压力转为清晰标准和承诺。"),
    "七杀": ("acute_pressure", "压力、竞争、风险、行动魄力", "先识别压力源，再设计安全出口。"),
    "正印": ("support_learning", "支持、学习、保护、资质", "寻找可依靠资源和学习路径。"),
    "偏印": ("indirect_support", "非常规学习、敏感、转换、孤独感", "把敏感转成研究和复盘，不放大恐惧。"),
}

ZIWEI_PALACES = {
    "命宫": ("self_pattern", "自我呈现、惯性模式、基本反应", "只谈倾向，不贴终身标签。"),
    "兄弟宫": ("siblings_peers", "手足、同辈、协作资源", "关注协作与边界。"),
    "夫妻宫": ("partnership", "亲密关系、合作模式、投射", "不替伴侣下确定结论。"),
    "子女宫": ("children_creation", "子女、作品、创造延伸", "涉及未成年人时只做支持性语言。"),
    "财帛宫": ("resources", "资源、收入方式、金钱习惯", "不替代投资、借贷或理财建议。"),
    "疾厄宫": ("body_stress", "身体感受、压力模式、照护习惯", "不做诊断或用药建议。"),
    "迁移宫": ("movement", "外部环境、出行、外地机会", "结合现实交通、安全和资源。"),
    "交友宫": ("network", "朋友、合作圈、团队互动", "不把他人动机写死。"),
    "仆役宫": ("network", "朋友、合作圈、团队互动", "不把他人动机写死。"),
    "官禄宫": ("career", "事业路径、职责、长期角色", "不替用户决定辞职或职业重大选择。"),
    "田宅宫": ("home_assets", "居住、家庭资产、空间稳定", "不替代法律、房产或安全判断。"),
    "福德宫": ("inner_life", "精神状态、休息、价值感", "避免把情绪困扰命定化。"),
    "父母宫": ("elders_support", "长辈、制度、文书、上级资源", "关注支持结构与沟通方式。"),
}

ZIWEI_STARS = {
    "紫微": ("central_order", "主导、整合、责任、秩序", "把主导力转成服务和承担，避免控制。"),
    "天机": ("adaptive_mind", "机动、思考、变化、策划", "把想法落到验证步骤。"),
    "太阳": ("visibility", "外显、照拂、行动、公开", "注意消耗和过度承担。"),
    "武曲": ("execution_resource", "执行、资源、纪律、财务意识", "谈管理，不做投资断言。"),
    "天同": ("comfort", "缓和、享受、关系温度、适应", "避免只求舒服而回避行动。"),
    "廉贞": ("boundary_desire", "边界、欲望、规则、复杂关系", "先厘清规则和责任。"),
    "天府": ("storage_support", "储备、承载、稳定、管理", "检查资源是否真正可用。"),
    "太阴": ("inner_resource", "内在、照顾、积累、细腻", "重视恢复和长期积累。"),
    "贪狼": ("desire_growth", "欲望、社交、才艺、变化", "区分探索、沉迷和现实成本。"),
    "巨门": ("speech_doubt", "语言、质疑、解释、误会", "把猜测、证据和结论分开。"),
    "天相": ("support_role", "协调、辅佐、制度感、形象", "检查是否过度迎合。"),
    "天梁": ("protection_principle", "保护、原则、长辈、修复", "把原则转成具体支持。"),
    "七杀": ("decisive_change", "决断、压力、突破、风险", "先做风险隔离再行动。"),
    "破军": ("break_rebuild", "破旧、重组、冒险、更新", "重大改变要先做可逆试验。"),
}

CATEGORY_DATA = {
    "stem": ("bazi", "heavenly_stem", STEMS),
    "branch": ("bazi", "earthly_branch", BRANCHES),
    "ten_god": ("bazi", "ten_god", TEN_GODS),
    "ziwei_palace": ("ziwei", "palace", ZIWEI_PALACES),
    "ziwei_star": ("ziwei", "main_star", ZIWEI_STARS),
}

ALIASES = {
    "天干": "stem",
    "地支": "branch",
    "十神": "ten_god",
    "宫位": "ziwei_palace",
    "星曜": "ziwei_star",
    "主星": "ziwei_star",
    "官禄": "官禄宫",
    "夫妻": "夫妻宫",
    "财帛": "财帛宫",
    "疾厄": "疾厄宫",
    "交友": "交友宫",
    "仆役": "仆役宫",
}


def normalize_category(raw: object) -> str:
    text = str(raw or "").strip()
    if text in CATEGORY_DATA:
        return text
    return ALIASES.get(text, "")


def normalize_query(raw: object) -> str:
    text = str(raw or "").strip()
    return ALIASES.get(text, text)


def find_symbol(query: str, category: str = "") -> tuple[str, str, tuple[str, str, str]]:
    if category:
        data = CATEGORY_DATA.get(category)
        if not data:
            raise ValueError(f"unknown category: {category}")
        if query in data[2]:
            return category, query, data[2][query]
        raise ValueError(f"unknown {category} symbol: {query}")

    matches = []
    for cat, data in CATEGORY_DATA.items():
        if query in data[2]:
            matches.append((cat, query, data[2][query]))
    if not matches:
        raise ValueError(f"unknown mingli symbol: {query}")
    if len(matches) > 1:
        categories = ", ".join(item[0] for item in matches)
        raise ValueError(f"ambiguous symbol {query}; provide category, one of: {categories}")
    return matches[0]


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    query = normalize_query(payload.get("query", payload.get("symbol", "")))
    if not query:
        raise ValueError("query or symbol is required")
    category = normalize_category(payload.get("category", payload.get("symbol_type", "")))
    category, canonical, item = find_symbol(query, category)
    system, layer, table = CATEGORY_DATA[category]
    code, keywords_raw, action = item
    keywords = [part.strip() for part in keywords_raw.split("、") if part.strip()]
    focus = str(payload.get("focus", "")).strip() or "general"
    return {
        "query": query,
        "category": category,
        "canonical_name": canonical,
        "system": system,
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": keywords,
        "interpretation_prompt": f"把「{canonical}」作为{layer}层的象征语言，围绕{focus}整理资源、压力和可行动选择。",
        "reflection_questions": [
            "这个象征更像在描述哪种惯性、资源或压力？",
            "哪些现实证据支持这个观察，哪些只是猜测？",
            "用户下一步能做的低风险验证动作是什么？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把单一符号写成终身定性、疾病诊断、财富保证或婚恋必然结果。",
            "不替代医疗、法律、财务、心理健康或紧急安全建议。",
            "第三方或未成年人资料必须最小化，并优先使用非标签化语言。",
        ],
        "next_steps": [
            "combine_with_recorded_chart_context_if_available",
            "state_method_and_data_limits",
            "map_symbol_to_observable_patterns",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.query:
        payload["query"] = args.query
    if args.category:
        payload["category"] = args.category
    if args.focus:
        payload["focus"] = args.focus
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Mingli symbol, e.g. 甲, 七杀, 官禄宫, 紫微.")
    parser.add_argument("--category", help="stem, branch, ten_god, ziwei_palace, or ziwei_star.")
    parser.add_argument("--focus", help="Optional analysis focus.")
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
