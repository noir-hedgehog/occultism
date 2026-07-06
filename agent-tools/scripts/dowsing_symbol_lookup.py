#!/usr/bin/env python3
"""Lookup safe symbolic prompts for dowsing rod movements and contexts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "crossing_rods": ("双杆交叉", "movement", "交点、注意、暂停、需要核查", "不写成准确定位地下物或事实证明。"),
    "opening_rods": ("双杆张开", "movement", "展开、边界、选择空间、放慢观察", "不写成发现水源或资源保证。"),
    "parallel_rods": ("双杆平行", "movement", "继续、通道、方向感、保持记录", "不写成施工路线或安全确认。"),
    "single_swing": ("单杆摆动", "movement", "偏向、试探、需要二次核对", "不写成唯一答案或专业判断。"),
    "map_mark": ("地图标记", "method", "假设、区域、待验证、信息整理", "不写成远程定位、寻人或犯罪线索。"),
    "threshold": ("门槛/入口", "space", "进入、转换、边界、停顿", "不写成能量门户或灵体通道。"),
    "corner": ("角落", "space", "堆积、忽略、收纳、需要清理", "不写成邪气聚集或病因。"),
    "path": ("路线/通道", "space", "流动、动线、阻塞、可调整下一步", "不写成风水定论或施工建议。"),
    "pause_marker": ("暂停标记", "method", "停止、复核、现实证据、专业边界", "不鼓励反复探到满意。"),
    "journal_grid": ("记录网格", "method", "分区、观察、比较、复盘", "不写成准确坐标或保证定位。"),
}

ALIASES = {
    "交叉": "crossing_rods",
    "双杆交叉": "crossing_rods",
    "crossing": "crossing_rods",
    "张开": "opening_rods",
    "双杆张开": "opening_rods",
    "opening": "opening_rods",
    "平行": "parallel_rods",
    "双杆平行": "parallel_rods",
    "parallel": "parallel_rods",
    "摆动": "single_swing",
    "单杆摆动": "single_swing",
    "swing": "single_swing",
    "地图标记": "map_mark",
    "地图": "map_mark",
    "map mark": "map_mark",
    "门槛": "threshold",
    "入口": "threshold",
    "threshold": "threshold",
    "角落": "corner",
    "corner": "corner",
    "路线": "path",
    "通道": "path",
    "path": "path",
    "暂停": "pause_marker",
    "暂停标记": "pause_marker",
    "记录网格": "journal_grid",
    "网格": "journal_grid",
    "journal grid": "journal_grid",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered.replace(" ", "_")))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("movement", ""))))
    if not code:
        raise ValueError("query, symbol, or movement is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown dowsing symbol: {code}")
    canonical, layer, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "dowsing_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("movement", code)))).strip(),
        "canonical_name": canonical,
        "system": "dowsing_rod_symbolic_reflection",
        "symbol_code": code,
        "symbol_layer": layer,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为占杖/{layer}象征，围绕{focus}整理路线感、观察点、现实核查和停止条件。",
        "reflection_questions": [
            "这是杆体动作、地图标记、空间位置还是私人联想？",
            "它更像暂停、方向、边界、分区、动线还是待核查假设？",
            "哪些判断必须回到授权范围、现实证据、专业勘测和安全边界？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把占杖动作写成地下管线、水源、矿脉、疾病、灵体或事实位置证明。",
            "不替代工程勘测、施工安全、医疗、法律、物业、报警、寻人或专业探测。",
            "不鼓励闯入、开挖、打井、投资、购房合同决定、高价课程或反复依赖。",
        ],
        "next_steps": ["combine_with_dowsing_context", "prioritize_reality_checklist", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Dowsing movement or context symbol.")
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
