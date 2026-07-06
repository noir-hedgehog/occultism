#!/usr/bin/env python3
"""Lookup safe symbolic prompts for pendulum motions and answer states."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "clockwise": ("顺时针", "motion", "确认、聚焦、推进、整合", "只能作为偏好推进提示，不写成事实证明。"),
    "counterclockwise": ("逆时针", "motion", "回看、松动、暂缓、排除", "适合提醒复核和暂缓，不写成坏预兆。"),
    "back_and_forth": ("前后摆动", "motion", "靠近、试探、往返、需要更多信息", "适合提示补证据，不当作绝对 yes。"),
    "side_to_side": ("左右摆动", "motion", "分歧、比较、边界、选择未定", "适合做选项表，不当作绝对 no。"),
    "still": ("静止", "motion", "暂停、能量不足、问题不清、需要休息", "不恐吓为被阻挡或有灵体干扰。"),
    "unclear": ("不明确", "answer_state", "信号混杂、问题过载、环境干扰、需要改写", "应暂停并改写问题，不反复追问。"),
    "yes": ("是", "answer_state", "倾向、允许、可尝试、当前偏好", "只能写成象征倾向，不作为事实或决定。"),
    "no": ("否", "answer_state", "边界、暂缓、排除、重新考虑", "只能写成提醒，不作为事实或否定人格。"),
    "maybe": ("不确定", "answer_state", "条件不足、需要证据、等待、拆分问题", "要求拆成更小问题和现实标准。"),
    "calibration": ("校准", "method_layer", "约定、记录、环境稳定、用户同意", "校准不证明外部真相，只提高记录一致性。"),
}

ALIASES = {
    "顺时针": "clockwise",
    "逆时针": "counterclockwise",
    "前后": "back_and_forth",
    "左右": "side_to_side",
    "不动": "still",
    "静止": "still",
    "乱晃": "unclear",
    "不明确": "unclear",
    "是": "yes",
    "否": "no",
    "不确定": "maybe",
    "校准": "calibration",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    if text in SYMBOLS:
        return text
    return ALIASES.get(text, text)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown pendulum symbol: {code}")
    canonical, layer, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "pendulum_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "pendulum_divination",
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为{layer}层的灵摆象征，围绕{focus}整理当前倾向、缺失证据和低风险下一步。",
        "reflection_questions": [
            "这个摆动是否已经在本次会话中校准，还是只是用户描述？",
            "问题是否被写成可反思、可验证、可撤回的低风险问题？",
            "哪些判断必须回到现实证据、专业意见或当事人沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把灵摆答案写成事实证明、专业建议或最终决定。",
            "不确认附身、邪灵、诅咒、被害或第三方真实想法。",
            "不鼓励反复问到满意为止。",
        ],
        "next_steps": ["combine_with_session_record", "rank_real_world_evidence_first", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Motion or answer state, e.g. 顺时针, yes, unclear.")
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
