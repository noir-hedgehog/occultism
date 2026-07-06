#!/usr/bin/env python3
"""Look up concise Tarot card meanings for symbolic readings."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


MAJORS = {
    "愚者": {"number": 0, "en": "The Fool", "keywords": ["开始", "信任", "冒险"], "shadow": ["鲁莽", "逃避后果", "准备不足"], "prompt": "我正站在哪个新起点前？"},
    "魔术师": {"number": 1, "en": "The Magician", "keywords": ["资源", "行动", "显化"], "shadow": ["操控", "空谈", "分心"], "prompt": "我手上已有哪几种资源可以整合？"},
    "女祭司": {"number": 2, "en": "The High Priestess", "keywords": ["直觉", "沉默", "隐秘"], "shadow": ["信息不透明", "过度内耗", "逃避沟通"], "prompt": "哪些信息需要先观察而不是急着判断？"},
    "皇后": {"number": 3, "en": "The Empress", "keywords": ["滋养", "创造", "丰盛"], "shadow": ["过度照顾", "依赖舒适", "边界松散"], "prompt": "我如何滋养这件事，同时保留边界？"},
    "皇帝": {"number": 4, "en": "The Emperor", "keywords": ["结构", "责任", "秩序"], "shadow": ["僵硬", "控制欲", "压迫"], "prompt": "这里需要建立什么规则或责任边界？"},
    "教皇": {"number": 5, "en": "The Hierophant", "keywords": ["传统", "学习", "制度"], "shadow": ["教条", "从众", "权威依赖"], "prompt": "我需要遵循规则，还是重新理解规则？"},
    "恋人": {"number": 6, "en": "The Lovers", "keywords": ["选择", "联结", "价值一致"], "shadow": ["摇摆", "投射", "讨好"], "prompt": "这个选择最考验我的哪项价值？"},
    "战车": {"number": 7, "en": "The Chariot", "keywords": ["意志", "推进", "整合冲突"], "shadow": ["硬撑", "失控", "只顾胜负"], "prompt": "我需要把哪些相反力量拉到同一方向？"},
    "力量": {"number": 8, "en": "Strength", "keywords": ["温柔的控制", "耐心", "勇气"], "shadow": ["压抑情绪", "逞强", "耗竭"], "prompt": "我如何用稳定而非蛮力处理这件事？"},
    "隐士": {"number": 9, "en": "The Hermit", "keywords": ["独处", "内省", "寻找方向"], "shadow": ["孤立", "拖延", "拒绝求助"], "prompt": "我需要安静下来确认什么？"},
    "命运之轮": {"number": 10, "en": "Wheel of Fortune", "keywords": ["变化", "周期", "转折"], "shadow": ["被动等待", "失控感", "重复模式"], "prompt": "这个周期正在提醒我识别什么模式？"},
    "正义": {"number": 11, "en": "Justice", "keywords": ["因果", "公平", "判断"], "shadow": ["苛责", "逃避责任", "片面判断"], "prompt": "哪些事实和责任需要被摆到台面上？"},
    "倒吊人": {"number": 12, "en": "The Hanged Man", "keywords": ["暂停", "换视角", "交付"], "shadow": ["停滞", "牺牲成瘾", "无力感"], "prompt": "如果先暂停，我会看见什么新角度？"},
    "死神": {"number": 13, "en": "Death", "keywords": ["结束", "转化", "清理"], "shadow": ["抗拒结束", "恐惧变化", "拖泥带水"], "prompt": "什么已经完成使命，需要体面结束？"},
    "节制": {"number": 14, "en": "Temperance", "keywords": ["调和", "节奏", "整合"], "shadow": ["失衡", "过度妥协", "节奏混乱"], "prompt": "我需要如何调配资源和节奏？"},
    "恶魔": {"number": 15, "en": "The Devil", "keywords": ["束缚", "欲望", "依赖"], "shadow": ["成瘾", "恐惧驱动", "权力不平等"], "prompt": "我以为离不开的东西，真的不能松动吗？"},
    "高塔": {"number": 16, "en": "The Tower", "keywords": ["崩塌", "真相", "重建"], "shadow": ["冲击", "失序", "拒绝面对"], "prompt": "哪个不稳固的结构正在暴露问题？"},
    "星星": {"number": 17, "en": "The Star", "keywords": ["希望", "疗愈", "愿景"], "shadow": ["空想", "迟迟不落地", "过度理想化"], "prompt": "我仍然愿意相信和修复什么？"},
    "月亮": {"number": 18, "en": "The Moon", "keywords": ["不确定", "潜意识", "迷雾"], "shadow": ["误判", "焦虑投射", "隐瞒"], "prompt": "哪些恐惧可能来自不完整的信息？"},
    "太阳": {"number": 19, "en": "The Sun", "keywords": ["清晰", "生命力", "公开"], "shadow": ["过度乐观", "忽略阴影", "自我中心"], "prompt": "什么事情已经可以更坦然地被看见？"},
    "审判": {"number": 20, "en": "Judgement", "keywords": ["召唤", "复盘", "更新"], "shadow": ["自责", "逃避召唤", "旧账反复"], "prompt": "我被什么更真实的方向召回？"},
    "世界": {"number": 21, "en": "The World", "keywords": ["完成", "整合", "阶段闭环"], "shadow": ["不肯收尾", "完美主义", "害怕下一阶段"], "prompt": "这个阶段如何完整收束，并进入下一轮？"},
}

SUITS = {
    "权杖": {"en": "Wands", "element": "火", "theme": "行动、意志、创造力", "action": "把灵感拆成可执行的第一步"},
    "圣杯": {"en": "Cups", "element": "水", "theme": "情绪、关系、感受", "action": "辨认真实感受并温和表达"},
    "宝剑": {"en": "Swords", "element": "风", "theme": "思想、沟通、判断", "action": "澄清事实、语言和决策标准"},
    "星币": {"en": "Pentacles", "element": "土", "theme": "资源、身体、金钱、现实建设", "action": "把问题落到资源、时间和习惯上"},
}

RANKS = {
    "王牌": {"en": "Ace", "keywords": ["种子", "机会", "潜能"], "shadow": ["尚未落地", "只停留在可能性"], "prompt": "这个新机会需要怎样被接住？"},
    "二": {"en": "Two", "keywords": ["平衡", "选择", "互动"], "shadow": ["摇摆", "僵持", "回避决定"], "prompt": "我正在平衡哪两个方向？"},
    "三": {"en": "Three", "keywords": ["发展", "协作", "初步成果"], "shadow": ["分散", "沟通不齐", "期待落差"], "prompt": "这件事需要谁或什么资源协作？"},
    "四": {"en": "Four", "keywords": ["稳定", "边界", "结构"], "shadow": ["停滞", "封闭", "安全感过度"], "prompt": "稳定和开放之间如何拿捏？"},
    "五": {"en": "Five", "keywords": ["冲突", "挑战", "失衡"], "shadow": ["消耗", "执拗", "受困感"], "prompt": "冲突真正暴露了什么需求？"},
    "六": {"en": "Six", "keywords": ["修复", "过渡", "互助"], "shadow": ["停留过去", "不平等给予", "依赖"], "prompt": "我如何从失衡走向修复？"},
    "七": {"en": "Seven", "keywords": ["评估", "防守", "选择压力"], "shadow": ["怀疑", "拖延", "过度防御"], "prompt": "现在最需要评估哪项风险？"},
    "八": {"en": "Eight", "keywords": ["推进", "练习", "调整"], "shadow": ["机械重复", "焦躁", "过劳"], "prompt": "哪项重复练习会带来改变？"},
    "九": {"en": "Nine", "keywords": ["成熟", "临界", "个人成果"], "shadow": ["孤立", "守成", "最后一关焦虑"], "prompt": "我离阶段成果还差哪一步？"},
    "十": {"en": "Ten", "keywords": ["完成", "负荷", "循环终点"], "shadow": ["过载", "难以放手", "责任堆积"], "prompt": "什么已经到达上限，需要结束或分担？"},
    "侍从": {"en": "Page", "keywords": ["学习", "消息", "好奇"], "shadow": ["稚嫩", "不稳定", "只会试探"], "prompt": "我需要以学习者姿态探索什么？"},
    "骑士": {"en": "Knight", "keywords": ["推进", "追求", "动能"], "shadow": ["莽撞", "偏执", "节奏失衡"], "prompt": "我的推进速度是否匹配现实条件？"},
    "皇后": {"en": "Queen", "keywords": ["内在掌握", "滋养", "成熟回应"], "shadow": ["情绪化控制", "过度承担", "封闭"], "prompt": "我如何成熟地承接这一元素的力量？"},
    "国王": {"en": "King", "keywords": ["外在掌控", "责任", "领导"], "shadow": ["僵硬控制", "权威压迫", "脱离感受"], "prompt": "我需要如何负责地使用影响力？"},
}


ALIASES: dict[str, str] = {}
for name, data in MAJORS.items():
    ALIASES[name.lower()] = name
    ALIASES[str(data["number"])] = name
    ALIASES[str(data["en"]).lower()] = name
    ALIASES[str(data["en"]).lower().replace("the ", "")] = name
for suit, suit_data in SUITS.items():
    for rank, rank_data in RANKS.items():
        canonical = f"{suit}{rank}"
        ALIASES[canonical.lower()] = canonical
        ALIASES[f"{rank}{suit}".lower()] = canonical
        ALIASES[f"{rank_data['en']} of {suit_data['en']}".lower()] = canonical
        ALIASES[f"{suit_data['en']} {rank_data['en']}".lower()] = canonical


def canonicalize(card_name: str) -> str:
    key = card_name.strip().lower()
    if key in ALIASES:
        return ALIASES[key]
    raise ValueError(f"unknown tarot card: {card_name}")


def lookup_card(card_name: str, orientation: str = "upright", position: str = "") -> dict[str, Any]:
    canonical = canonicalize(card_name)
    orientation = orientation.strip().lower() or "upright"
    if orientation in {"正位", "正"}:
        orientation = "upright"
    if orientation in {"逆位", "逆", "reverse"}:
        orientation = "reversed"
    if orientation not in {"upright", "reversed"}:
        raise ValueError(f"unknown orientation: {orientation}")

    if canonical in MAJORS:
        data = MAJORS[canonical]
        upright = data["keywords"]
        reversed_keywords = data["shadow"]
        return {
            "card": canonical,
            "english_name": data["en"],
            "arcana": "major",
            "number": data["number"],
            "orientation": orientation,
            "position": position,
            "upright_keywords": upright,
            "reversed_keywords": reversed_keywords,
            "active_keywords": reversed_keywords if orientation == "reversed" else upright,
            "reflection_prompt": data["prompt"],
            "action_guidance": "把牌义当作象征提醒，结合牌位和现实处境提出一个小行动。",
            "safety_note": "不把塔罗牌义作为医疗、法律、财务或人身安全判断。",
        }

    suit = next(s for s in SUITS if canonical.startswith(s))
    rank = canonical.replace(suit, "", 1)
    suit_data = SUITS[suit]
    rank_data = RANKS[rank]
    upright = list(rank_data["keywords"]) + [suit_data["theme"]]
    reversed_keywords = list(rank_data["shadow"]) + [f"{suit}能量阻滞或过度"]
    return {
        "card": canonical,
        "english_name": f"{rank_data['en']} of {suit_data['en']}",
        "arcana": "minor",
        "suit": suit,
        "rank": rank,
        "element": suit_data["element"],
        "orientation": orientation,
        "position": position,
        "upright_keywords": upright,
        "reversed_keywords": reversed_keywords,
        "active_keywords": reversed_keywords if orientation == "reversed" else upright,
        "reflection_prompt": rank_data["prompt"],
        "action_guidance": suit_data["action"],
        "safety_note": "把小牌解释为现实层面的状态提醒，不作为确定预言。",
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.card:
        return {"card": args.card, "orientation": args.orientation, "position": args.position}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"card": raw}
    raise ValueError("Provide --card, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--card", help="Card name, e.g. 愚者 or Three of Swords.")
    parser.add_argument("--orientation", default="upright", help="upright/reversed/正位/逆位")
    parser.add_argument("--position", default="", help="Optional spread position.")
    parser.add_argument("--json", help="JSON input with card, orientation, position.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        payload = load_payload(args)
        result = lookup_card(str(payload.get("card", "")), str(payload.get("orientation", "upright")), str(payload.get("position", "")))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

