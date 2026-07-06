#!/usr/bin/env python3
"""Lookup safe symbolic prompts for Liuyao six-line divination terms."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


KINSHIP = {
    "父母": ("parents", "文书、信息、保护、制度、房屋", "先确认资料、规则、凭证和支持结构。"),
    "兄弟": ("siblings", "同辈、竞争、消耗、协作、分担", "区分互助、竞争和资源消耗。"),
    "子孙": ("children", "产出、缓冲、放松、结果、创造", "看哪些行动能降低压力并产出反馈。"),
    "妻财": ("wealth_spouse", "资源、现实收益、关系对象、经营", "不做投资或关系必然结论，只谈资源管理。"),
    "官鬼": ("officer_ghost", "压力、规则、风险、责任、病象隐喻", "把压力转成风险清单和可求助对象。"),
}

SPIRITS = {
    "青龙": ("azure_dragon", "顺势、喜庆、资源显现、温和推进", "把顺势条件落实为现实行动。"),
    "朱雀": ("vermilion_bird", "消息、口舌、表达、文书", "先区分事实、传闻和情绪表达。"),
    "勾陈": ("hooked_serpent", "拖延、牵连、旧账、结构阻滞", "整理遗留事项和责任边界。"),
    "腾蛇": ("soaring_serpent", "疑虑、缠绕、想象、复杂感", "降低恐惧解释，回到证据和澄清。"),
    "白虎": ("white_tiger", "冲突、损耗、急迫、安全警讯", "涉及现实危险时先处理安全，不做灾祸断言。"),
    "玄武": ("black_tortoise", "隐藏、暧昧、遗漏、背后信息", "用核实问题替代猜测他人动机。"),
}

ROLES = {
    "世爻": ("self_line", "本人位置、主观处境、当前承受点", "先看用户能控制和能观察的部分。"),
    "应爻": ("other_line", "对方、环境、外部回应、合作方", "只用可能性语言描述外部因素。"),
    "用神": ("focus_spirit", "所问事项的主要观察点", "先声明取用逻辑，不同派别可不同。"),
    "原神": ("supporting_spirit", "支持用神的资源或条件", "寻找能补足主线的现实支持。"),
    "忌神": ("blocking_spirit", "阻滞用神的压力或冲突", "把阻滞转成可管理风险。"),
    "仇神": ("counter_spirit", "间接消耗或反复牵制", "避免恐吓，关注消耗路径和边界。"),
}

POSITIONS = {
    "初爻": ("line_1", "基础、起点、底层条件", "先检查最底层事实和准备。"),
    "二爻": ("line_2", "内部执行、日常位置、近身资源", "看日常动作和内部配合。"),
    "三爻": ("line_3", "过渡、压力、临界动作", "行动前先做风险隔离。"),
    "四爻": ("line_4", "外部连接、接近主位、协作", "看沟通接口和外部反馈。"),
    "五爻": ("line_5", "主位、决策、核心资源", "聚焦关键责任和主要选择。"),
    "上爻": ("line_6", "收束、远端、结果边界", "不要把结果写死，关注收束信号。"),
}

CATEGORY_DATA = {
    "kinship": ("six_kinship", KINSHIP),
    "spirit": ("six_spirit", SPIRITS),
    "role": ("line_role", ROLES),
    "position": ("line_position", POSITIONS),
}

ALIASES = {
    "六亲": "kinship",
    "亲": "kinship",
    "六神": "spirit",
    "神煞": "spirit",
    "角色": "role",
    "世应": "role",
    "爻位": "position",
    "位置": "position",
    "父母爻": "父母",
    "兄弟爻": "兄弟",
    "子孙爻": "子孙",
    "妻财爻": "妻财",
    "财爻": "妻财",
    "官鬼爻": "官鬼",
    "官鬼": "官鬼",
    "青龙": "青龙",
    "朱雀": "朱雀",
    "勾陈": "勾陈",
    "螣蛇": "腾蛇",
    "腾蛇": "腾蛇",
    "白虎": "白虎",
    "玄武": "玄武",
    "世": "世爻",
    "应": "应爻",
    "1爻": "初爻",
    "一爻": "初爻",
    "第1爻": "初爻",
    "2爻": "二爻",
    "第2爻": "二爻",
    "3爻": "三爻",
    "第3爻": "三爻",
    "4爻": "四爻",
    "第4爻": "四爻",
    "5爻": "五爻",
    "第5爻": "五爻",
    "6爻": "上爻",
    "六爻位": "上爻",
    "第6爻": "上爻",
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
        raise ValueError(f"unknown liuyao symbol: {query}")
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
        "system": "liuyao",
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": keywords,
        "interpretation_prompt": f"把「{canonical}」作为六爻{layer}层的象征语言，围绕{focus}整理用神、世应、风险和可观察证据。",
        "reflection_questions": [
            "这个符号在本问题里被取作什么观察点，取用逻辑是否已声明？",
            "它指向哪些现实证据、资源、压力或沟通边界？",
            "用户下一步能做的低风险验证动作是什么？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把六亲、六神、世应或爻位写成灾祸、疾病、财富或关系结局的确定断言。",
            "不替代医疗、法律、财务、心理健康、职业或紧急安全建议。",
            "不分析未经同意的第三方隐私，不用六爻窥探或操控他人。",
        ],
        "next_steps": [
            "run_yijing_question_guard_for_one_matter_boundary",
            "confirm_casting_method_and_external_chart_source",
            "state_school_and_line_role_limits",
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
    parser.add_argument("--query", help="Liuyao symbol, e.g. 官鬼, 世爻, 青龙, 三爻.")
    parser.add_argument("--category", help="kinship, spirit, role, or position.")
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
