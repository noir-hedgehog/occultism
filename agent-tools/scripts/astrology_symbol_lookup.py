#!/usr/bin/env python3
"""Lookup safe symbolic prompts for astrology signs, planets, houses, points, and aspects."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SIGNS = {
    "白羊座": ("aries", "启动、直接、勇气、探索", "把冲劲转成一个可完成的小行动。"),
    "金牛座": ("taurus", "稳定、感官、资源、耐心", "先确认资源、节奏和身体感受。"),
    "双子座": ("gemini", "信息、表达、连接、好奇", "把分散信息整理成可验证的问题。"),
    "巨蟹座": ("cancer", "照顾、安全感、记忆、边界", "区分真实需要和过度防御。"),
    "狮子座": ("leo", "创造、自尊、可见度、热情", "让表达服务于具体作品或关系。"),
    "处女座": ("virgo", "细节、修正、服务、秩序", "用清单和迭代减少焦虑。"),
    "天秤座": ("libra", "关系、平衡、审美、协商", "把和谐愿望落到清晰选择和边界。"),
    "天蝎座": ("scorpio", "深度、信任、转化、敏锐", "先确认事实，再处理强烈感受。"),
    "射手座": ("sagittarius", "意义、远方、学习、扩展", "把远景拆成近期可试验路径。"),
    "摩羯座": ("capricorn", "责任、结构、长期、现实", "把压力转成阶段目标和支持结构。"),
    "水瓶座": ("aquarius", "系统、独立、社群、革新", "让新想法接受现实反馈。"),
    "双鱼座": ("pisces", "想象、共情、流动、灵感", "给感受命名，同时保留现实锚点。"),
}

PLANETS = {
    "太阳": ("sun", "核心意志、生命力、自我表达", "观察用户如何获得能量和承担可见角色。"),
    "月亮": ("moon", "情绪需求、安全感、习惯反应", "关注照顾方式、恢复节奏和情绪触发点。"),
    "水星": ("mercury", "思考、沟通、学习、信息交换", "检查表达方式和信息过滤。"),
    "金星": ("venus", "价值感、关系吸引、审美、愉悦", "把喜欢和需要区分清楚。"),
    "火星": ("mars", "行动、欲望、冲突、边界推进", "把行动力和冲突管理分开谈。"),
    "木星": ("jupiter", "扩展、信念、机会、学习", "看扩张是否有现实承接。"),
    "土星": ("saturn", "限制、责任、时间、结构", "把限制转成边界、训练和成熟路径。"),
    "天王星": ("uranus", "突破、自由、突变、非典型路径", "先做可逆试验，不把冲动写成命运。"),
    "海王星": ("neptune", "理想、想象、迷雾、共情", "区分愿景、投射和现实证据。"),
    "冥王星": ("pluto", "深层转化、权力、执着、重建", "避免恐吓式解释，回到边界和修复。"),
}

POINTS = {
    "上升": ("ascendant", "外在呈现、进入世界的方式、第一反应", "观察别人最先感受到的风格和自我保护方式。"),
    "下降": ("descendant", "关系镜像、合作入口、他者议题", "不替对方下结论，只谈互动模式。"),
    "天顶": ("midheaven", "公众角色、职业方向、长期可见度", "把职业象征转为能力、场景和长期建设。"),
    "天底": ("imum_coeli", "根基、家庭感、私人安全", "回到稳定感、休息和支持系统。"),
}

HOUSES = {
    "一宫": ("house_1", "自我呈现、身体感、启动方式", "只谈呈现方式，不贴人格标签。"),
    "二宫": ("house_2", "资源、金钱习惯、价值感", "不替代理财或投资建议。"),
    "三宫": ("house_3", "沟通、学习、近距离连接", "关注表达、信息和日常练习。"),
    "四宫": ("house_4", "家、根基、私人安全", "结合现实居住和支持结构。"),
    "五宫": ("house_5", "创造、恋爱、游戏感、自我表达", "不把浪漫可能写成必然结果。"),
    "六宫": ("house_6", "日常、工作流、健康习惯", "只谈习惯和压力，不做诊断。"),
    "七宫": ("house_7", "伴侣、合作、一对一关系", "不判断某人必定爱或不爱。"),
    "八宫": ("house_8", "共享资源、亲密、信任、转化", "避开财富承诺和恐吓式灾祸语言。"),
    "九宫": ("house_9", "远行、高等学习、信念、视野", "把意义追求落到学习和探索计划。"),
    "十宫": ("house_10", "事业、公众角色、长期目标", "不替用户做辞职、升迁或投资决定。"),
    "十一宫": ("house_11", "社群、朋友、长期愿景", "区分社群支持和群体压力。"),
    "十二宫": ("house_12", "潜意识、退隐、收束、疗愈意象", "避免病理化，必要时建议专业心理支持。"),
}

ASPECTS = {
    "合相": ("conjunction", "聚焦、强化、合流", "先看两个象征如何共同放大同一主题。"),
    "对冲": ("opposition", "拉扯、镜像、两端平衡", "把冲突转成双方需求和边界的整理。"),
    "拱相": ("trine", "顺流、天赋、自然支持", "把顺手的资源转成实际练习。"),
    "刑相": ("square", "摩擦、压力、行动课题", "把压力转成可管理的小步调整。"),
    "六合": ("sextile", "机会、协作、可开发潜能", "需要主动使用，不能写成自动好运。"),
}

CATEGORY_DATA = {
    "sign": ("zodiac_sign", SIGNS),
    "planet": ("planetary_function", PLANETS),
    "point": ("chart_point", POINTS),
    "house": ("house_topic", HOUSES),
    "aspect": ("aspect_relationship", ASPECTS),
}

ALIASES = {
    "星座": "sign",
    "行星": "planet",
    "星体": "planet",
    "轴点": "point",
    "四轴": "point",
    "宫位": "house",
    "相位": "aspect",
    "白羊": "白羊座",
    "金牛": "金牛座",
    "双子": "双子座",
    "巨蟹": "巨蟹座",
    "狮子": "狮子座",
    "处女": "处女座",
    "天秤": "天秤座",
    "天平": "天秤座",
    "天蝎": "天蝎座",
    "射手": "射手座",
    "摩羯": "摩羯座",
    "魔羯": "摩羯座",
    "水瓶": "水瓶座",
    "双鱼": "双鱼座",
    "命宫": "一宫",
    "第1宫": "一宫",
    "第2宫": "二宫",
    "第3宫": "三宫",
    "第4宫": "四宫",
    "第5宫": "五宫",
    "第6宫": "六宫",
    "第7宫": "七宫",
    "第8宫": "八宫",
    "第9宫": "九宫",
    "第10宫": "十宫",
    "第11宫": "十一宫",
    "第12宫": "十二宫",
    "一宫": "一宫",
    "1宫": "一宫",
    "二宫": "二宫",
    "2宫": "二宫",
    "三宫": "三宫",
    "3宫": "三宫",
    "四宫": "四宫",
    "4宫": "四宫",
    "五宫": "五宫",
    "5宫": "五宫",
    "六宫": "六宫",
    "6宫": "六宫",
    "七宫": "七宫",
    "7宫": "七宫",
    "八宫": "八宫",
    "8宫": "八宫",
    "九宫": "九宫",
    "9宫": "九宫",
    "十宫": "十宫",
    "10宫": "十宫",
    "十一宫": "十一宫",
    "11宫": "十一宫",
    "十二宫": "十二宫",
    "12宫": "十二宫",
    "上升星座": "上升",
    "asc": "上升",
    "ASC": "上升",
    "下降点": "下降",
    "mc": "天顶",
    "MC": "天顶",
    "ic": "天底",
    "IC": "天底",
    "冲相": "对冲",
    "三分": "拱相",
    "四分": "刑相",
    "六分": "六合",
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
        raise ValueError(f"unknown astrology symbol: {query}")
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
        "system": "western_astrology",
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": keywords,
        "interpretation_prompt": f"把「{canonical}」作为占星{layer}层的象征语言，围绕{focus}整理倾向、资源、张力和可观察证据。",
        "reflection_questions": [
            "这个象征更像在描述哪种需求、表达方式或关系张力？",
            "哪些现实证据支持这个观察，哪些只是投射或期待？",
            "用户下一步能做的低风险验证动作是什么？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把星盘符号写成命运保证、绝配结论、疾病诊断、财富承诺或灾祸断言。",
            "不替代医疗、法律、财务、心理健康、职业或紧急安全建议。",
            "第三方星盘、精确出生资料和未成年人资料必须最小化，并优先要求同意。",
        ],
        "next_steps": [
            "confirm_birth_data_or_external_chart_source_if_needed",
            "state_non_deterministic_symbolic_limits",
            "map_symbols_to_observable_patterns",
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
    parser.add_argument("--query", help="Astrology symbol, e.g. 天秤, 月亮, 上升, 十宫, 合相.")
    parser.add_argument("--category", help="sign, planet, point, house, or aspect.")
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
