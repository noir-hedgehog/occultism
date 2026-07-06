#!/usr/bin/env python3
"""Lookup Yijing hexagram structure and symbolic interpretation prompts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from yijing_hexagram_record import HEXAGRAM_MATRIX, TRIGRAMS


HEXAGRAM_THEMES = [
    (1, "乾为天", "乾", ("开创", "主动", "自强", "原则"), "我需要如何使用主动性而不过度强硬？", "明确目标、节奏和责任边界。"),
    (2, "坤为地", "坤", ("承载", "顺势", "滋养", "配合"), "我需要承载什么，并在哪里保持柔顺？", "先稳定基础，再逐步响应变化。"),
    (3, "水雷屯", "屯", ("初生", "混乱", "困难开局", "蓄势"), "新局面里最需要先理顺哪一件事？", "降低预期，先处理资源和秩序。"),
    (4, "山水蒙", "蒙", ("启蒙", "未知", "学习", "求教"), "我在哪些地方需要先学习而不是急着判断？", "请教可靠的人，建立基本规则。"),
    (5, "水天需", "需", ("等待", "准备", "耐心", "时机"), "这件事需要等待什么条件成熟？", "准备资源，避免仓促推进。"),
    (6, "天水讼", "讼", ("争执", "分歧", "边界", "证据"), "冲突真正卡在事实、利益还是表达？", "整理证据和边界，避免升级对立。"),
    (7, "地水师", "师", ("组织", "纪律", "协作", "执行"), "我需要怎样组织人力和步骤？", "明确角色、规则和责任。"),
    (8, "水地比", "比", ("亲近", "联盟", "选择同伴", "归属"), "我应与谁建立更稳固的合作？", "选择可信关系，避免盲目依附。"),
    (9, "风天小畜", "小畜", ("小积累", "克制", "蓄养", "细节"), "哪些小调整会累积成真实变化？", "先做可控的小修正。"),
    (10, "天泽履", "履", ("礼节", "谨慎", "位置", "分寸"), "我现在应如何拿捏分寸？", "遵守规则，避免踩过界。"),
    (11, "地天泰", "泰", ("通达", "交流", "平衡", "顺畅"), "当前顺畅来自哪些条件的配合？", "维护流动，不因顺势而松懈。"),
    (12, "天地否", "否", ("闭塞", "不通", "隔阂", "停滞"), "哪里已经不再流通，需要暂停硬推？", "保存实力，先找阻塞点。"),
    (13, "天火同人", "同人", ("共同体", "公开", "合作", "共识"), "我与他人的共同目标是什么？", "把目标说清楚，寻找共同语言。"),
    (14, "火天大有", "大有", ("丰盛", "资源", "责任", "可见成果"), "资源增多后，我要如何负责地使用？", "整理资源，避免炫耀或浪费。"),
    (15, "地山谦", "谦", ("谦逊", "低位", "节制", "修正"), "哪里需要放低姿态以获得空间？", "收敛锋芒，先补短板。"),
    (16, "雷地豫", "豫", ("预备", "动员", "情绪", "乐观"), "我的兴奋是否有足够准备支撑？", "把热情转为计划和节奏。"),
    (17, "泽雷随", "随", ("跟随", "适应", "响应", "选择"), "我在跟随什么，是否值得继续？", "顺势调整，但保留判断。"),
    (18, "山风蛊", "蛊", ("积弊", "修复", "旧问题", "整顿"), "哪个旧问题已经需要认真修复？", "追根溯源，分步骤清理。"),
    (19, "地泽临", "临", ("临近", "关照", "督导", "机会"), "我该如何靠近并承担影响力？", "主动关注，但避免压迫。"),
    (20, "风地观", "观", ("观察", "审视", "示范", "全局"), "我需要退后一步观察什么？", "先看结构，再做判断。"),
    (21, "火雷噬嗑", "噬嗑", ("咬合", "规则", "惩戒", "清障"), "哪里需要明确规则才能继续？", "处理障碍，建立可执行约束。"),
    (22, "山火贲", "贲", ("修饰", "形式", "表达", "美化"), "形式与实质是否匹配？", "优化表达，但别让包装盖过本质。"),
    (23, "山地剥", "剥", ("剥落", "消耗", "衰退", "减损"), "什么正在被消耗，需要停止流失？", "减少负担，保护核心。"),
    (24, "地雷复", "复", ("返回", "恢复", "新循环", "初心"), "我需要回到哪个基本点？", "从小的恢复动作开始。"),
    (25, "天雷无妄", "无妄", ("自然", "不妄为", "真实", "意外"), "我是否在强行制造不属于自己的结果？", "按事实行动，减少妄念。"),
    (26, "山天大畜", "大畜", ("大积累", "约束", "储备", "能力"), "我正在积累什么长期能力？", "先蓄力和训练，再求突破。"),
    (27, "山雷颐", "颐", ("滋养", "言语", "输入", "养成"), "我用什么滋养自己，也用什么消耗自己？", "调整输入、饮食、语言和习惯。"),
    (28, "泽风大过", "大过", ("过载", "承担", "非常态", "临界"), "哪里已经超出承载，需要重配重量？", "减压、分担或改变结构。"),
    (29, "坎为水", "坎", ("险陷", "重复风险", "流动", "警觉"), "我反复遇到的风险模式是什么？", "谨慎推进，建立安全路径。"),
    (30, "离为火", "离", ("明辨", "依附", "看见", "表达"), "我需要照亮什么，也依附于什么？", "澄清事实，保持清醒表达。"),
    (31, "泽山咸", "咸", ("感应", "吸引", "互动", "触动"), "这份触动来自真实交流还是投射？", "观察互动质量，避免急于定义。"),
    (32, "雷风恒", "恒", ("持续", "稳定", "长期", "节律"), "什么值得长期坚持，什么只是惯性？", "建立可持续节奏。"),
    (33, "天山遁", "遁", ("退避", "保存", "距离", "策略"), "我需要从哪里暂时后退以保存力量？", "有策略地拉开距离。"),
    (34, "雷天大壮", "大壮", ("强盛", "力量", "推进", "节制"), "力量变强后，如何不被力量带偏？", "推进时保留规则和节制。"),
    (35, "火地晋", "晋", ("上升", "进展", "认可", "显现"), "我有哪些进展正在浮出水面？", "把成果清楚呈现出来。"),
    (36, "地火明夷", "明夷", ("受伤之明", "隐藏", "低调", "保护"), "我需要保护哪部分清醒和价值？", "低调行事，先护住核心。"),
    (37, "风火家人", "家人", ("家内秩序", "角色", "亲密责任", "边界"), "亲近关系里角色和责任是否清楚？", "整理家庭/团队内部规则。"),
    (38, "火泽睽", "睽", ("分歧", "异中求同", "看法不同", "疏离"), "差异在哪里，哪些差异可以共存？", "承认不同，再找可合作处。"),
    (39, "水山蹇", "蹇", ("阻碍", "艰难", "求助", "绕行"), "当前障碍提示我需要哪种帮助？", "停下硬闯，寻找替代路径。"),
    (40, "雷水解", "解", ("解除", "松绑", "释放", "化解"), "有什么可以先被解开或放下？", "解决关键结，给系统松绑。"),
    (41, "山泽损", "损", ("减少", "取舍", "节用", "牺牲"), "我需要减少什么以保全更重要的东西？", "做清晰取舍，降低消耗。"),
    (42, "风雷益", "益", ("增益", "助力", "投入", "成长"), "哪里值得增加投入以带来成长？", "把资源投向能放大的地方。"),
    (43, "泽天夬", "夬", ("决断", "宣告", "去除", "突破"), "我需要做出什么清楚但不鲁莽的决断？", "公开边界，果断处理阻碍。"),
    (44, "天风姤", "姤", ("相遇", "突发接触", "诱因", "边界"), "这个相遇带来机会还是扰动？", "保持边界，观察来意。"),
    (45, "泽地萃", "萃", ("聚集", "汇合", "群体", "资源"), "哪些人和资源正在聚合？", "组织聚合点，避免混乱。"),
    (46, "地风升", "升", ("上升", "渐进", "积累推进", "成长"), "我可以通过什么路径稳步上升？", "循序渐进，保持根基。"),
    (47, "泽水困", "困", ("困顿", "受限", "消耗", "内在坚守"), "限制中还有什么原则可守？", "减少外耗，保留核心判断。"),
    (48, "水风井", "井", ("公共资源", "供养", "结构", "取用"), "我依赖的资源结构是否仍然可用？", "维护基础系统，改善取用方式。"),
    (49, "泽火革", "革", ("变革", "更新", "更替", "时机"), "什么已经到了必须更新的时候？", "先确认时机和正当性，再变革。"),
    (50, "火风鼎", "鼎", ("承载转化", "制度", "养成", "新器"), "我需要建立什么容器来承载变化？", "重建流程、制度或支持结构。"),
    (51, "震为雷", "震", ("震动", "惊醒", "启动", "警讯"), "这次震动提醒我看见什么？", "先稳住，再把警讯转为行动。"),
    (52, "艮为山", "艮", ("止", "边界", "静定", "停顿"), "哪里需要停下来，不再继续消耗？", "设下边界，练习暂停。"),
    (53, "风山渐", "渐", ("渐进", "次序", "成长", "积累"), "这件事合理的成长次序是什么？", "按阶段推进，不跳步骤。"),
    (54, "雷泽归妹", "归妹", ("位置不正", "关系调整", "仓促结合", "角色"), "这段关系或合作的位置是否清楚？", "慢下来确认角色和承诺。"),
    (55, "雷火丰", "丰", ("丰盛", "高峰", "照见", "盛极"), "高峰期里我需要看见什么阴影？", "利用高能量，也准备退潮。"),
    (56, "火山旅", "旅", ("旅途", "临时状态", "异地", "适应"), "我当前是否处在临时而非扎根的状态？", "轻装、守礼、适应环境。"),
    (57, "巽为风", "巽", ("进入", "渗透", "柔顺", "反复"), "我需要用什么柔和方式持续进入？", "用细致沟通和重复动作推进。"),
    (58, "兑为泽", "兑", ("喜悦", "交流", "表达", "交换"), "什么交流带来真实喜悦，什么只是讨好？", "保持开放表达，同时守住诚实。"),
    (59, "风水涣", "涣", ("涣散", "疏解", "分离", "重聚"), "什么需要先散开，才可能重新组织？", "疏通卡点，重建连接。"),
    (60, "水泽节", "节", ("节制", "界限", "制度", "限度"), "我需要设置什么限度才可持续？", "制定规则和节奏。"),
    (61, "风泽中孚", "中孚", ("诚信", "内在真实", "信任", "共鸣"), "我真正相信什么，也如何让人可信？", "回到真诚和可验证承诺。"),
    (62, "雷山小过", "小过", ("小过度", "细节谨慎", "低飞", "修正"), "哪里需要小心修正而不是大动作？", "处理细节，避免冒进。"),
    (63, "水火既济", "既济", ("已成", "完成", "平衡后风险", "收尾"), "完成之后还有哪些维护风险？", "做好收尾和复盘，防止松散。"),
    (64, "火水未济", "未济", ("未成", "过渡", "临门一脚", "调整"), "这件事还差哪一步才能成形？", "校准顺序，完成最后衔接。"),
]

THEMES_BY_NUMBER = {entry[0]: entry for entry in HEXAGRAM_THEMES}
THEMES_BY_NAME = {entry[1]: entry for entry in HEXAGRAM_THEMES}


def normalize_query(value: str) -> str:
    return value.strip().replace(" ", "").replace("　", "")


def build_hexagrams() -> list[dict[str, Any]]:
    by_number: dict[int, dict[str, Any]] = {}
    trigram_by_name = {data["name"]: {"bits": bits, **data} for bits, data in TRIGRAMS.items()}
    for lower_name, uppers in HEXAGRAM_MATRIX.items():
        for upper_name, (number, canonical_name) in uppers.items():
            theme = THEMES_BY_NUMBER[number]
            by_number[number] = {
                "number": number,
                "name": canonical_name,
                "short_name": theme[2],
                "keywords": list(theme[3]),
                "reflection_prompt": theme[4],
                "action_guidance": theme[5],
                "lower_trigram": trigram_by_name[lower_name],
                "upper_trigram": trigram_by_name[upper_name],
                "image_name": f"{trigram_by_name[upper_name]['image']}{trigram_by_name[lower_name]['image']}",
                "bits_bottom_to_top": trigram_by_name[lower_name]["bits"] + trigram_by_name[upper_name]["bits"],
            }
    return [by_number[number] for number in sorted(by_number)]


HEXAGRAMS = build_hexagrams()
BY_NUMBER = {item["number"]: item for item in HEXAGRAMS}
ALIASES: dict[str, int] = {}
for item in HEXAGRAMS:
    ALIASES[str(item["number"])] = item["number"]
    ALIASES[normalize_query(item["name"])] = item["number"]
    ALIASES[normalize_query(item["short_name"])] = item["number"]


def line_scope(line: int | None) -> dict[str, Any] | None:
    if line is None:
        return None
    if line < 1 or line > 6:
        raise ValueError("line must be between 1 and 6")
    labels = {
        1: "初爻：事情的起点、根基、潜在动因",
        2: "二爻：内在位置、配合方式、可持续基础",
        3: "三爻：转换压力、行动风险、临界选择",
        4: "四爻：接近外部、试探推进、资源连接",
        5: "五爻：主位、决策核心、责任承担",
        6: "上爻：阶段尾声、过度风险、转入下一局",
    }
    return {
        "line": line,
        "focus": labels[line],
        "note": "这是爻位解释层级提示，不是原文爻辞。详细动爻骨架请使用 yijing_line_lookup。",
    }


def find_by_trigrams(lower: str, upper: str) -> dict[str, Any]:
    lower = normalize_query(lower)
    upper = normalize_query(upper)
    for item in HEXAGRAMS:
        if item["lower_trigram"]["name"] == lower and item["upper_trigram"]["name"] == upper:
            return item
    raise ValueError("unknown lower/upper trigram combination")


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    method = ""
    if payload.get("number") is not None:
        number = int(payload["number"])
        method = "number"
        if number not in BY_NUMBER:
            raise ValueError("hexagram number must be between 1 and 64")
        item = BY_NUMBER[number]
    elif payload.get("lower_trigram") and payload.get("upper_trigram"):
        item = find_by_trigrams(str(payload["lower_trigram"]), str(payload["upper_trigram"]))
        method = "trigrams"
    else:
        query = normalize_query(str(payload.get("query", payload.get("name", ""))))
        if not query:
            raise ValueError("provide number, query/name, or lower_trigram + upper_trigram")
        if query not in ALIASES:
            raise ValueError(f"unknown hexagram query: {query}")
        item = BY_NUMBER[ALIASES[query]]
        method = "query"

    active_line = payload.get("line")
    line = int(active_line) if active_line not in (None, "") else None
    result = {
        **item,
        "lookup_method": method,
        "line_scope": line_scope(line),
        "limits": [
            "此工具提供卦名、上下卦结构和现代反思关键词，不替代原典注解。",
            "卦义应与具体问题、起卦记录、变爻和现实处境一起解释。",
            "不得把卦象解释为确定预言或专业建议。",
        ],
        "next_steps": [
            "connect_to_question_context",
            "compare_with_changing_hexagram_when_present",
            "map_symbols_to_observable_actions",
            "lint_final_output_with_mystic_output_lint",
        ],
    }
    return result


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload.update(json.load(f))
    if args.number is not None:
        payload["number"] = args.number
    if args.query:
        payload["query"] = args.query
    if args.lower_trigram:
        payload["lower_trigram"] = args.lower_trigram
    if args.upper_trigram:
        payload["upper_trigram"] = args.upper_trigram
    if args.line is not None:
        payload["line"] = args.line
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --number, --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--number", type=int, help="King Wen sequence number, 1-64.")
    parser.add_argument("--query", help="Hexagram name, short name, or number.")
    parser.add_argument("--lower-trigram", help="Lower trigram name, e.g. 乾.")
    parser.add_argument("--upper-trigram", help="Upper trigram name, e.g. 坤.")
    parser.add_argument("--line", type=int, help="Optional changing line number, 1-6.")
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
