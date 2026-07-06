#!/usr/bin/env python3
"""Lookup safe symbolic prompts for Meihua Yishu divination terms."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


STRUCTURES = {
    "体卦": ("body_hexagram", "主体、本人、承受点、内在条件", "先看用户自身处境、资源和可控范围。"),
    "用卦": ("use_hexagram", "对象、外部、事件、压力来源", "只用可能性语言描述外部因素。"),
    "互卦": ("mutual_hexagram", "中间过程、隐藏结构、内在牵连", "寻找过程中的关键环节和未显性因素。"),
    "变卦": ("changed_hexagram", "变化方向、后续倾向、调整结果", "把倾向转成可观察信号，不写成必然结局。"),
    "动爻": ("moving_line", "触发点、变化位置、行动焦点", "定位变化发生在哪个层级，再找低风险动作。"),
}

METHODS = {
    "报数起卦": ("number_casting", "数字、随问随起、即时触发", "记录数字来源、时间和用户同意，不随意补数。"),
    "时间起卦": ("time_casting", "年月日时、时间触发、节律", "记录时间、时区和历法来源。"),
    "外应": ("external_omen", "环境线索、偶发信号、同步观察", "先描述可见事实，不把巧合写成天意。"),
    "方位取象": ("direction_symbol", "方向、空间、来处去处", "需要明确方位来源，不编造罗盘。"),
}

RELATIONS = {
    "生体": ("support_body", "外部支持主体、资源进入、条件助力", "确认支持是否真实可用。"),
    "克体": ("pressure_body", "外部压力主体、约束、冲突", "把压力拆成风险、边界和求助对象。"),
    "体生用": ("body_supports_use", "主体付出、资源外流、主动投入", "检查投入是否过量，是否有回收机制。"),
    "体克用": ("body_controls_use", "主体能制约事件、主动处理、可控性", "把可控性转成具体行动，不夸大掌控。"),
    "比和": ("same_element", "同类、平衡、僵持、同频", "观察是协同还是停滞。"),
}

TRIGRAMS = {
    "乾": ("qian", "天、刚健、规则、父性/权威象征", "把权威和规则转成清晰责任。"),
    "兑": ("dui", "泽、交流、悦纳、口舌", "区分沟通、承诺和真实行动。"),
    "离": ("li", "火、显现、文书、可见度", "核实信息来源和公开表达。"),
    "震": ("zhen", "雷、启动、惊动、行动", "先做小步试探，避免冲动。"),
    "巽": ("xun", "风、进入、协商、渗透", "用渐进沟通和细节调整推进。"),
    "坎": ("kan", "水、风险、流动、隐忧", "先识别不确定性和安全边界。"),
    "艮": ("gen", "山、停止、门槛、边界", "判断哪里需要暂停和稳住。"),
    "坤": ("kun", "地、承载、资源、顺势", "检查承接能力和实际支持。"),
}

CATEGORY_DATA = {
    "structure": ("chart_structure", STRUCTURES),
    "method": ("casting_method", METHODS),
    "relation": ("five_phase_relation", RELATIONS),
    "trigram": ("trigram_symbol", TRIGRAMS),
}

ALIASES = {
    "结构": "structure",
    "盘式": "structure",
    "方法": "method",
    "起卦": "method",
    "五行": "relation",
    "生克": "relation",
    "八卦": "trigram",
    "卦象": "trigram",
    "体": "体卦",
    "用": "用卦",
    "互": "互卦",
    "变": "变卦",
    "动": "动爻",
    "动爻": "动爻",
    "报数": "报数起卦",
    "数字起卦": "报数起卦",
    "时间": "时间起卦",
    "外部应象": "外应",
    "生我": "生体",
    "克我": "克体",
    "我生": "体生用",
    "我克": "体克用",
    "同气": "比和",
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
        if query in data[1]:
            return category, query, data[1][query]
        raise ValueError(f"unknown {category} symbol: {query}")

    matches = []
    for cat, data in CATEGORY_DATA.items():
        if query in data[1]:
            matches.append((cat, query, data[1][query]))
    if not matches:
        raise ValueError(f"unknown meihua symbol: {query}")
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
    layer = CATEGORY_DATA[category][0]
    code, keywords_raw, action = item
    keywords = [part.strip() for part in keywords_raw.split("、") if part.strip()]
    focus = str(payload.get("focus", "")).strip() or "general"
    return {
        "query": query,
        "category": category,
        "canonical_name": canonical,
        "system": "meihua_yishu",
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": keywords,
        "interpretation_prompt": f"把「{canonical}」作为梅花易数{layer}层的象征语言，围绕{focus}整理体用、触发、变化和现实证据。",
        "reflection_questions": [
            "这个符号在本问题里对应主体、对象、过程还是变化触发？",
            "它指向哪些可见事实、资源、阻力或时间/环境线索？",
            "用户下一步能做的低风险验证动作是什么？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把体用、生克、外应或动爻写成成败、疾病、财富、婚恋或灾祸的确定断言。",
            "不替代医疗、法律、财务、心理健康、职业或紧急安全建议。",
            "不借外应恐吓用户，不把巧合写成超自然确认。",
        ],
        "next_steps": [
            "run_yijing_question_guard_for_one_matter_boundary",
            "confirm_casting_method_number_time_or_external_chart_source",
            "state_method_school_and_symbol_limits",
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
    parser.add_argument("--query", help="Meihua symbol, e.g. 体卦, 用卦, 外应, 生体, 离.")
    parser.add_argument("--category", help="structure, method, relation, or trigram.")
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
