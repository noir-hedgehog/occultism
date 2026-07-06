#!/usr/bin/env python3
"""Lookup safe symbolic prompts for Chinese character components and structures."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "wood": ("木", "component", "生长、支撑、方向、学习", "不把木部写成必然旺运或性格定论。"),
    "water": ("水/氵", "component", "流动、适应、沟通、情绪", "不把水象写成情绪事实或医疗判断。"),
    "fire": ("火/灬", "component", "明亮、表达、行动、消耗", "不承诺成功、热度或灾祸。"),
    "earth": ("土", "component", "稳定、承载、边界、现实条件", "不把稳定写成停滞命定。"),
    "metal": ("金/钅", "component", "规则、价值、边界、清晰", "不用于投资、赌博或财富承诺。"),
    "heart": ("心/忄", "component", "感受、在意、关系、自我照料", "不读取第三方真实想法。"),
    "mouth": ("口", "component", "表达、入口、承诺、沟通", "不把一句话写成事实证明。"),
    "speech": ("言/讠", "component", "语言、说明、协议、误解", "涉及合同或法律时必须转向专业意见。"),
    "person": ("人/亻", "component", "角色、支持、互动、责任", "不做人格优劣或身份标签。"),
    "hand": ("手/扌", "component", "行动、触达、执行、可控步骤", "不鼓励操控他人。"),
    "sun": ("日", "component", "可见、节奏、时间、清晰", "不承诺具体日期或结果。"),
    "moon": ("月", "component", "周期、照料、身体感受、隐微", "不作健康、怀孕或身体判断。"),
    "door": ("门", "component", "入口、边界、许可、选择", "不承诺机会必然打开。"),
    "walk": ("辶", "component", "移动、路径、过程、递进", "不保证出行、项目或关系必顺。"),
    "roof": ("宀", "component", "居所、保护、内部秩序、安放", "不替代风水、法律或安全判断。"),
    "mountain": ("山", "component", "阻力、稳定、视角、界限", "不恐吓灾祸或不可改变。"),
    "field": ("田", "component", "范围、资源、分区、耕耘", "不承诺收益或收成。"),
    "grass": ("艹", "component", "生发、柔韧、日常照料、环境", "不把植物象征写成疗愈功效。"),
    "left_right": ("左右结构", "structure", "并列、协作、内外分工、平衡", "结构只作观察线索，不证明关系事实。"),
    "top_bottom": ("上下结构", "structure", "承接、层次、优先级、支撑", "不写成等级高低或身份优劣。"),
    "enclosure": ("包围结构", "structure", "边界、容纳、限制、保护", "不把包围写成被困命定。"),
    "single_body": ("独体字", "structure", "集中、简洁、核心、独立", "不把独立写成孤立命运。"),
    "open_form": ("开口", "form", "通道、表达、外部交换、未封闭", "不承诺机会或消息。"),
    "closed_form": ("封闭", "form", "保存、边界、内收、待整理", "不恐吓封闭、停滞或坏结果。"),
}

ALIASES = {
    "木": "wood",
    "木部": "wood",
    "氵": "water",
    "三点水": "water",
    "水": "water",
    "火": "fire",
    "灬": "fire",
    "火底": "fire",
    "土": "earth",
    "金": "metal",
    "钅": "metal",
    "心": "heart",
    "忄": "heart",
    "竖心旁": "heart",
    "口": "mouth",
    "言": "speech",
    "讠": "speech",
    "言字旁": "speech",
    "人": "person",
    "亻": "person",
    "单人旁": "person",
    "手": "hand",
    "扌": "hand",
    "提手旁": "hand",
    "日": "sun",
    "月": "moon",
    "门": "door",
    "辶": "walk",
    "走之": "walk",
    "宀": "roof",
    "宝盖": "roof",
    "山": "mountain",
    "田": "field",
    "艹": "grass",
    "草字头": "grass",
    "左右": "left_right",
    "左右结构": "left_right",
    "上下": "top_bottom",
    "上下结构": "top_bottom",
    "包围": "enclosure",
    "包围结构": "enclosure",
    "独体": "single_body",
    "独体字": "single_body",
    "开口": "open_form",
    "半开": "open_form",
    "封闭": "closed_form",
    "闭合": "closed_form",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("component", ""))))
    if not code:
        raise ValueError("query, symbol, or component is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown cezi symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "cezi_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("component", code)))).strip(),
        "canonical_name": canonical,
        "system": "character_divination_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为测字/拆字象征，围绕{focus}整理字形联想、现实证据、可控行动和表达边界。",
        "reflection_questions": [
            "这个部件或结构在本字里是显眼线索，还是用户自己的第一联想？",
            "它能提示哪类资源、阻力、沟通方式或低风险下一步？",
            "哪些判断必须回到现实证据、当事人沟通、专业意见或安全支持？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把测字写成事实证明、专业建议、诊断、预测、寿命判断、人格优劣或最终决定。",
            "不确认诅咒、附身、被害、驱邪效果或第三方真实想法。",
            "不鼓励反复测字直到满意。",
        ],
        "next_steps": ["combine_with_cezi_character_record", "rank_real_world_evidence_first", "run_mystic_output_lint"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.query:
        return {"query": args.query, "focus": args.focus}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Character component/structure, e.g. 木, 口, 左右结构.")
    parser.add_argument("--focus", help="Optional focus.")
    parser.add_argument("--json", help="JSON object input.")
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
