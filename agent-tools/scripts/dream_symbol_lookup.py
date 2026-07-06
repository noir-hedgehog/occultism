#!/usr/bin/env python3
"""Lookup safe symbolic prompts for dream images and motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "water": {
        "aliases": ("水", "海", "河", "湖", "雨", "洪水", "游泳"),
        "canonical_name": "水",
        "symbol_layer": "emotion_and_flow",
        "keywords": ["情绪", "流动", "承载", "边界"],
        "action": "把梦里的水势对应到最近情绪强度、边界感和恢复空间。",
    },
    "chase": {
        "aliases": ("追", "逃", "躲", "追赶"),
        "canonical_name": "被追赶/逃跑",
        "symbol_layer": "avoidance_and_pressure",
        "keywords": ["压力", "回避", "紧迫", "自我保护"],
        "action": "辨认现实中被推迟、被压迫或需要面对的小问题。",
    },
    "falling": {
        "aliases": ("坠落", "掉下", "摔下", "掉进"),
        "canonical_name": "坠落",
        "symbol_layer": "control_and_instability",
        "keywords": ["失控感", "不稳定", "放手", "惊醒"],
        "action": "检查最近哪些事情让用户觉得缺少支撑或节奏太快。",
    },
    "teeth": {
        "aliases": ("牙", "牙齿", "掉牙"),
        "canonical_name": "牙齿/掉牙",
        "symbol_layer": "expression_and_vulnerability",
        "keywords": ["表达", "脆弱", "形象", "变化焦虑"],
        "action": "把它读作表达、形象或变化焦虑的象征，不写成亲人灾祸预兆。",
    },
    "exam": {
        "aliases": ("考试", "迟到", "作业", "学校", "老师"),
        "canonical_name": "考试/迟到",
        "symbol_layer": "evaluation_and_readiness",
        "keywords": ["评估", "准备", "期限", "自我要求"],
        "action": "整理现实中的评估压力、准备不足感和可补上的一小步。",
    },
    "house": {
        "aliases": ("房子", "家", "房间", "门", "窗", "地下室"),
        "canonical_name": "房子/房间",
        "symbol_layer": "self_space_and_boundaries",
        "keywords": ["自我空间", "边界", "安全感", "私人区域"],
        "action": "把不同房间视为生活领域或心理空间的隐喻。",
    },
    "snake": {
        "aliases": ("蛇",),
        "canonical_name": "蛇",
        "symbol_layer": "instinct_and_change",
        "keywords": ["本能", "警觉", "变化", "边界"],
        "action": "先问用户对蛇的个人联想，再讨论警觉、变化或边界主题。",
    },
    "death": {
        "aliases": ("死亡", "去世", "葬礼", "死了"),
        "canonical_name": "死亡/葬礼",
        "symbol_layer": "ending_and_transition",
        "keywords": ["结束", "转变", "告别", "失去感"],
        "action": "只作为结束和转变的象征处理，不写成死亡预告。",
    },
    "flying": {
        "aliases": ("飞", "飞起来", "漂浮"),
        "canonical_name": "飞行/漂浮",
        "symbol_layer": "freedom_and_perspective",
        "keywords": ["自由", "视角", "脱离限制", "轻盈"],
        "action": "观察用户是否需要空间、视角转换或更轻的行动方案。",
    },
    "lost": {
        "aliases": ("迷路", "找不到", "丢了"),
        "canonical_name": "迷路/找不到",
        "symbol_layer": "orientation_and_uncertainty",
        "keywords": ["方向感", "不确定", "选择压力", "信息缺口"],
        "action": "把梦转成现实中的方向、信息和下一步澄清问题。",
    },
}


def normalize(query: str) -> str:
    text = query.strip()
    for code, item in SYMBOLS.items():
        if text == code or text in item["aliases"] or item["canonical_name"] == text:
            return code
    for code, item in SYMBOLS.items():
        if any(alias in text for alias in item["aliases"]):
            return code
    raise ValueError(f"unknown dream symbol: {query}")


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    query = str(payload.get("query", payload.get("symbol", ""))).strip()
    if not query:
        raise ValueError("query or symbol is required")
    code = normalize(query)
    item = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "dream_symbol_lookup",
        "query": query,
        "canonical_name": item["canonical_name"],
        "symbol_code": code,
        "system": "dream_symbolic_reflection",
        "symbol_layer": item["symbol_layer"],
        "keywords": item["keywords"],
        "interpretation_prompt": f"把「{item['canonical_name']}」作为梦境象征，围绕 {focus} 讨论感受、现实关联和可观察线索。",
        "reflection_questions": [
            "这个符号在梦里带来的第一感受是什么？",
            "它和最近现实中的压力、关系、变化或身体疲劳有什么相似处？",
            "如果把它当作提醒，下一步最小、低风险的现实动作是什么？",
        ],
        "action_guidance": item["action"],
        "prohibited_uses": [
            "不把梦写成疾病诊断、死亡预告、灾祸预兆或诅咒证据。",
            "不替代心理健康、医疗、睡眠或创伤支持。",
            "不宣称梦揭示他人真实想法或未来必然事件。",
        ],
        "next_steps": [
            "combine_with_dream_record_context",
            "state_symbolic_and_non_diagnostic_limits",
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
    parser.add_argument("--query", help="Dream symbol query.")
    parser.add_argument("--focus", help="Reflection focus.")
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
