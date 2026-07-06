#!/usr/bin/env python3
"""Lookup safe symbolic prompts for lost-object search motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "last_seen": ("最后看见", "memory", "时间、地点、动作、在手/离手瞬间", "把最后看见改写成现实时间线，不把它写成灵感定位。"),
    "route_retrace": ("路线回溯", "action", "路径、转场、口袋、包、交通工具", "按移动顺序复盘，不承诺某一方向一定有物品。"),
    "threshold": ("门口/玄关/出入口", "area", "进出、换手、放下、钥匙证件", "作为高概率搜索区，不写成方位神谕。"),
    "pocket_bag": ("口袋/包/夹层", "area", "随身、夹层、票据、充电线", "优先按容器和夹层逐层排查。"),
    "desk_surface": ("桌面/台面/抽屉", "area", "临时放置、遮挡、文件下方", "提醒做平面清空和拍照记录，不编造藏匿原因。"),
    "vehicle_transit": ("车内/交通/座位", "area", "座椅、脚垫、共享空间、失物招领", "转成联系交通/场所失物招领和固定搜索点。"),
    "contact_trace": ("联系渠道/失物招领", "action", "物业、前台、客服、同伴、收银台", "优先现实联系，不用占卜替代查询或报警。"),
    "stop_review": ("复盘与停止条件", "practice", "时限、二次搜索、记录、停止反复占问", "设置一次复盘和停止点，避免焦虑式反复占问。"),
}

ALIASES = {
    "最后看见": "last_seen",
    "最后一次": "last_seen",
    "离手": "last_seen",
    "路线": "route_retrace",
    "路径": "route_retrace",
    "回溯": "route_retrace",
    "门口": "threshold",
    "玄关": "threshold",
    "入口": "threshold",
    "出入口": "threshold",
    "口袋": "pocket_bag",
    "包": "pocket_bag",
    "夹层": "pocket_bag",
    "桌面": "desk_surface",
    "台面": "desk_surface",
    "抽屉": "desk_surface",
    "车": "vehicle_transit",
    "出租车": "vehicle_transit",
    "地铁": "vehicle_transit",
    "公交": "vehicle_transit",
    "失物招领": "contact_trace",
    "物业": "contact_trace",
    "客服": "contact_trace",
    "前台": "contact_trace",
    "复盘": "stop_review",
    "停止": "stop_review",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    if text in ALIASES:
        return ALIASES[text]
    for alias, code in ALIASES.items():
        if alias in text:
            return code
    return lowered


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown lost-object symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "memory_search_reflection"
    return {
        "tool": "lost_object_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "lost_object_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的低风险搜索线索，围绕最后接触、路径、区域、联系渠道、复盘时间和停止条件整理。",
        "reflection_questions": [
            "这是本人有权寻找的物品，还是寻人、宠物走失、犯罪证据、隐私定位或专业渠道替代？",
            "最后看见时间地点、移动路径、可能区域、已查位置和可联系对象是什么？",
            "怎样把方位/元素说法转成一个有限、可执行、可停止的现实搜索清单？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不承诺准确定位、一定找到、灵验方位或神秘指认。",
            "不处理寻人、儿童/老人走失、犯罪定责、隐私定位、跟踪或监视。",
            "不替代报警、物业、客服、学校、医院、交通失物招领或家人协助。",
            "不鼓励反复占问、焦虑式搜索或忽略证件/财物风险处理。",
        ],
        "next_steps": ["combine_with_lost_object_context", "turn_symbols_into_search_plan", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Lost-object motif.")
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
