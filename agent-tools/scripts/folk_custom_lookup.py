#!/usr/bin/env python3
"""Lookup safe cultural prompts for folk customs, festivals, taboos, and symbols."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


FESTIVALS = {
    "春节": ("spring_festival", "团圆、更新、门庭、祝福、秩序重启", "适合解释为岁首更新和家庭连接，不写成开运保证。"),
    "清明": ("qingming", "追思、扫墓、家族记忆、春季转换", "强调追思和安全出行，不给亡灵因果或恐吓判断。"),
    "端午": ("duanwu", "避疫意象、艾草、香囊、龙舟、夏季防护", "可转为季节卫生、纪念和祝愿，不声称物品能驱除真实邪祟。"),
    "中元": ("ghost_festival", "祭祖、普度、禁忌叙事、夜间谨慎", "只能作为文化叙事，遇到恐惧升级时先做安定和现实支持。"),
    "中秋": ("mid_autumn", "团圆、月亮、馈赠、思念、丰收", "适合解释关系和节令象征，不做姻缘或财富预测。"),
    "冬至": ("winter_solstice", "阴阳转换、家宴、补养、周期转折", "可转为作息和家人连接提醒，不替代健康建议。"),
}

TABOOS = {
    "筷子插饭": ("chopsticks_in_rice", "祭祀联想、餐桌礼仪、死亡象征、冒犯感", "解释为礼仪和文化联想，不写成会招灾。"),
    "夜里吹口哨": ("night_whistling", "夜间安静、惊扰他人、鬼神叙事、儿童规训", "转成邻里安静和情绪安定，不确认灵异因果。"),
    "正月剪发": ("first_month_haircut", "谐音禁忌、亲属称谓、岁首避忌、地方差异", "标注为民俗谐音和地区差异，不作灾祸判断。"),
    "孕妇禁忌": ("pregnancy_taboo", "保护性规训、身体照顾、家庭焦虑、医疗边界", "涉及孕期必须优先现实照护和医生建议。"),
    "搬家择日": ("move_in_auspicious_date", "新旧转换、家庭秩序、时间仪式、心理安定", "择日只能作为偏好和安排，不替代合同、天气、搬运安全。"),
    "丧葬避讳": ("funeral_avoidance", "哀悼边界、社群礼仪、尊重逝者、情绪保护", "不做亡灵恐吓，优先尊重当地礼仪和现实安全。"),
}

SYMBOLS = {
    "红色": ("red", "喜庆、辟邪叙事、可见度、节庆气氛", "可作为祝福和视觉传统，不声称必然开运。"),
    "门神": ("door_gods", "门户保护、年画、家庭边界、传统图像", "解释为门庭守护意象，不冒充宗教或历史权威。"),
    "艾草": ("mugwort", "端午、香气、季节防护、避疫意象", "只谈文化和气味体验；过敏、孕期和宠物环境要谨慎。"),
    "香囊": ("sachet", "气味、祝愿、随身护持、手作礼物", "适合作为礼物和安定象征，不承诺驱邪或治病。"),
    "桃木": ("peach_wood", "辟邪叙事、木质物、门饰、民间传说", "只作为民间象征，不建议购买昂贵法物或恐惧消费。"),
    "灯": ("lamp_light", "照明、明堂、迎接、安定、可见", "可转为低风险空间照明和夜间安全。"),
}

LIFE_EVENTS = {
    "搬家": ("moving_home", "空间转换、清扫、入宅、安定、邻里连接", "优先燃气、电路、通风和门锁，再谈象征流程。"),
    "开工": ("work_start", "启动、团队秩序、目标确认、祝福", "转成启动仪式和任务对齐，不承诺业绩。"),
    "婚礼": ("wedding", "亲族见证、礼序、祝福、边界协商", "尊重双方意愿和现实安排，不用禁忌压迫新人。"),
    "新生儿": ("newborn", "保护、命名、探访边界、照护节奏", "涉及婴儿健康时优先儿科和照护者判断。"),
    "考试": ("exam", "祝愿、专注、文昌叙事、准备状态", "把祝福转成复习、睡眠和考试物品检查。"),
    "出行": ("travel", "平安祝福、路线、天气、交通、家人牵挂", "先做现实交通和天气检查，不以禁忌替代安全规划。"),
}

CATEGORY_DATA = {
    "festival": ("seasonal_festival", FESTIVALS),
    "taboo": ("folk_taboo", TABOOS),
    "symbol": ("folk_symbol", SYMBOLS),
    "life_event": ("life_event_custom", LIFE_EVENTS),
}

ALIASES = {
    "节日": "festival",
    "节令": "festival",
    "传统节日": "festival",
    "禁忌": "taboo",
    "避讳": "taboo",
    "民俗禁忌": "taboo",
    "符号": "symbol",
    "物件": "symbol",
    "象征": "symbol",
    "人生礼俗": "life_event",
    "人生事件": "life_event",
    "场景": "life_event",
    "过年": "春节",
    "春节习俗": "春节",
    "扫墓": "清明",
    "清明节": "清明",
    "端午节": "端午",
    "鬼节": "中元",
    "中元节": "中元",
    "七月半": "中元",
    "月饼节": "中秋",
    "中秋节": "中秋",
    "筷子插米饭": "筷子插饭",
    "插筷子": "筷子插饭",
    "吹口哨": "夜里吹口哨",
    "剪头发": "正月剪发",
    "正月理发": "正月剪发",
    "怀孕禁忌": "孕妇禁忌",
    "孕期禁忌": "孕妇禁忌",
    "乔迁": "搬家",
    "入宅": "搬家",
    "开业": "开工",
    "婴儿": "新生儿",
    "宝宝": "新生儿",
    "高考": "考试",
    "旅行": "出行",
    "出门": "出行",
}


def normalize_category(raw: object) -> str:
    text = str(raw or "").strip()
    if text in CATEGORY_DATA:
        return text
    return ALIASES.get(text, "")


def normalize_query(raw: object) -> str:
    text = str(raw or "").strip()
    return ALIASES.get(text, text)


def find_custom(query: str, category: str = "") -> tuple[str, str, tuple[str, str, str]]:
    if category:
        data = CATEGORY_DATA.get(category)
        if not data:
            raise ValueError(f"unknown category: {category}")
        if query in data[1]:
            return category, query, data[1][query]
        raise ValueError(f"unknown {category} folk custom: {query}")

    matches = []
    for cat, data in CATEGORY_DATA.items():
        if query in data[1]:
            matches.append((cat, query, data[1][query]))
    if not matches:
        raise ValueError(f"unknown folk custom: {query}")
    if len(matches) > 1:
        categories = ", ".join(item[0] for item in matches)
        raise ValueError(f"ambiguous folk custom {query}; provide category, one of: {categories}")
    return matches[0]


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    query = normalize_query(payload.get("query", payload.get("custom", "")))
    if not query:
        raise ValueError("query or custom is required")
    category = normalize_category(payload.get("category", payload.get("custom_type", "")))
    category, canonical, item = find_custom(query, category)
    layer = CATEGORY_DATA[category][0]
    code, keywords_raw, action = item
    keywords = [part.strip() for part in keywords_raw.split("、") if part.strip()]
    focus = str(payload.get("focus", "")).strip() or "general"
    return {
        "query": query,
        "category": category,
        "canonical_name": canonical,
        "system": "chinese_folk_custom",
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": keywords,
        "interpretation_prompt": f"把「{canonical}」作为民俗{layer}层的文化材料，围绕{focus}区分节令象征、地方差异、现实安全和可低风险复用部分。",
        "reflection_questions": [
            "这个民俗说法来自节令、家庭习惯、地方传统、宗教语境还是网络传闻？",
            "哪些部分是文化象征或礼仪，哪些涉及现实安全、医疗、消防或法律风险？",
            "如何把禁忌或祝福转成尊重传统但不恐吓用户的低风险表达？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把民俗禁忌写成必然灾祸、鬼神确认、疾病判断、财富承诺或关系结局。",
            "不提供危险仪式、明火密闭燃烧、摄入不明物、伤害自己或控制他人的步骤。",
            "不冒充宗教、地方或家族权威；来源不明时必须标注为未验证说法。",
        ],
        "next_steps": [
            "run_mystic_intake_triage_with_folk_custom_domain",
            "ask_for_source_region_and_context",
            "route_dangerous_ritual_parts_to_ritual_safety_tools",
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
    parser.add_argument("--query", help="Folk custom, e.g. 端午, 筷子插饭, 艾草, 搬家.")
    parser.add_argument("--category", help="festival, taboo, symbol, or life_event.")
    parser.add_argument("--focus", help="Optional consultation focus.")
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
