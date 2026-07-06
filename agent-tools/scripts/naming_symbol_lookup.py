#!/usr/bin/env python3
"""Lookup safe symbolic prompts for Chinese naming and name-reflection terms."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


DIMENSIONS = {
    "字义": ("meaning", "本义、引申义、价值取向、文化联想", "先确认字义是否符合使用者想表达的品质和边界。"),
    "字音": ("sound", "声调、读音、节奏、称呼便利、误读风险", "朗读全名和常见称呼，检查是否顺口、清楚、不过度费解。"),
    "字形": ("form", "结构、笔画观感、书写成本、视觉平衡", "优先考虑可读性、签名便利和长期使用舒适度。"),
    "五行意象": ("five_phase_image", "木火土金水、象征偏向、气质隐喻", "只能作为传统象征语言，不写成命运补救或人生保证。"),
    "生肖避讳": ("zodiac_custom", "民俗偏好、生肖联想、家庭传统", "把生肖说法标为民俗参考，不把禁忌写成灾祸判断。"),
    "用字避讳": ("avoidance", "谐音、歧义、生僻字、负面联想、同名冲突", "先筛掉明显误读、冒犯、嘲笑或行政使用成本高的字。"),
    "场景匹配": ("usage_context", "乳名、学名、艺名、品牌名、笔名、跨语境使用", "根据实际使用场景选择正式度、记忆度和可扩展性。"),
}

ELEMENTS = {
    "木": ("wood", "生发、成长、柔韧、学习、连接", "适合表达成长和探索，但不要写成必然旺运。"),
    "火": ("fire", "明亮、表达、热情、可见度、行动", "适合表达活力和呈现，需留意是否过于张扬。"),
    "土": ("earth", "稳定、承载、信任、秩序、照顾", "适合表达安定和可靠，需避免过度沉重。"),
    "金": ("metal", "清晰、规则、决断、审美、边界", "适合表达清朗和原则，需避免解释成刚硬定性。"),
    "水": ("water", "流动、智慧、适应、深度、沟通", "适合表达灵动和包容，需避免写成性格注定。"),
}

NAME_TYPES = {
    "大名": ("formal_name", "证件、学校、职场、长期正式使用", "优先稳定、易读、少歧义和跨年龄适用。"),
    "小名": ("nickname", "家庭称呼、亲密关系、童年使用", "优先亲切、好叫、低压力，不承担过多命运期待。"),
    "艺名": ("stage_name", "公众展示、记忆点、风格标签", "平衡辨识度和长期职业形象，避免过度猎奇。"),
    "笔名": ("pen_name", "创作身份、文本气质、署名辨识", "让名字服务作品调性，而不是替代作品本身。"),
    "品牌名": ("brand_name", "传播、搜索、注册、品类联想", "先检查可读、可搜、可注册和品类匹配。"),
}

CULTURAL_CHECKS = {
    "谐音": ("homophone", "同音误解、玩笑空间、方言读法、负面词联想", "用普通话和主要方言场景读几遍，筛掉明显尴尬读法。"),
    "生僻字": ("rare_character", "识别成本、输入法成本、证件系统、老师同事误读", "除非有强烈理由，否则优先选择可输入、可读、可解释的字。"),
    "重名": ("duplicate_name", "同名密度、搜索结果、社交区分、身份混淆", "常用名不一定不好，但要确认是否影响识别和搜索。"),
    "性别期待": ("gender_expectation", "性别化联想、家庭期待、未来自主性", "避免把名字写成性别角色规定，保留使用者未来空间。"),
    "家族字辈": ("generation_name", "字辈、家族秩序、长辈期待、个人偏好", "尊重家族传统，同时确认使用者和照护者真实偏好。"),
}

CATEGORY_DATA = {
    "dimension": ("naming_dimension", DIMENSIONS),
    "element": ("five_phase_symbol", ELEMENTS),
    "name_type": ("name_usage_type", NAME_TYPES),
    "cultural_check": ("cultural_risk_check", CULTURAL_CHECKS),
}

ALIASES = {
    "维度": "dimension",
    "取名维度": "dimension",
    "姓名维度": "dimension",
    "五行": "element",
    "五行象征": "element",
    "类型": "name_type",
    "名字类型": "name_type",
    "用途": "name_type",
    "检查": "cultural_check",
    "避讳": "cultural_check",
    "风险": "cultural_check",
    "意义": "字义",
    "含义": "字义",
    "音": "字音",
    "读音": "字音",
    "声音": "字音",
    "形": "字形",
    "笔画": "字形",
    "结构": "字形",
    "五格": "五行意象",
    "三才五格": "五行意象",
    "生肖": "生肖避讳",
    "属相": "生肖避讳",
    "禁忌": "用字避讳",
    "忌讳": "用字避讳",
    "场景": "场景匹配",
    "正式名": "大名",
    "本名": "大名",
    "学名": "大名",
    "昵称": "小名",
    "乳名": "小名",
    "网名": "艺名",
    "品牌": "品牌名",
    "同音": "谐音",
    "谐音梗": "谐音",
    "罕见字": "生僻字",
    "冷僻字": "生僻字",
    "撞名": "重名",
    "字辈": "家族字辈",
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
        raise ValueError(f"unknown {category} naming symbol: {query}")

    matches = []
    for cat, data in CATEGORY_DATA.items():
        if query in data[1]:
            matches.append((cat, query, data[1][query]))
    if not matches:
        raise ValueError(f"unknown naming symbol: {query}")
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
        "system": "chinese_naming",
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": keywords,
        "interpretation_prompt": f"把「{canonical}」作为姓名学{layer}层的安全检查维度，围绕{focus}整理文化联想、现实使用成本和可讨论偏好。",
        "reflection_questions": [
            "这个名字或用字想表达什么价值、气质或使用场景？",
            "哪些联想来自文化偏好，哪些是现实可验证的读写和使用成本？",
            "有没有谐音、歧义、隐私、标签化或过度宿命论风险？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把姓名、笔画、五行、生肖或字义写成命运保证、疾病判断、财富承诺、婚恋结论或灾祸断言。",
            "不替代法律登记、商标注册、品牌检索、心理健康、医疗、财务或职业专业建议。",
            "涉及未成年人姓名时，避免贴性格标签或替孩子规定人生角色。",
        ],
        "next_steps": [
            "run_mystic_intake_triage_with_naming_domain",
            "confirm_name_type_and_user_goal",
            "check_sound_meaning_form_culture_and_usage_context",
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
    parser.add_argument("--query", help="Naming symbol/check, e.g. 字义, 木, 小名, 谐音.")
    parser.add_argument("--category", help="dimension, element, name_type, or cultural_check.")
    parser.add_argument("--focus", help="Optional naming focus.")
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
