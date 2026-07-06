#!/usr/bin/env python3
"""Lookup safe symbolic prompts for number-symbol consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "0": ("0", "digit", "空白、起点、循环、留白", "适合表达重置和空间，不写成虚无或坏运。"),
    "1": ("1", "digit", "开始、独立、行动、明确", "适合表达启动和主线，不写成必胜。"),
    "2": ("2", "digit", "关系、配合、平衡、选择", "适合讨论协作和边界，不断言姻缘。"),
    "3": ("3", "digit", "表达、创意、扩展、社交", "适合讨论表达和传播，不保证出名。"),
    "4": ("4", "digit", "结构、秩序、稳定、现实", "可谈稳定和规则，不恐吓谐音灾祸。"),
    "5": ("5", "digit", "变化、自由、流动、试错", "适合提醒弹性，不鼓励冲动。"),
    "6": ("6", "digit", "照顾、顺滑、责任、家庭", "不把 6 写成必顺或必旺。"),
    "7": ("7", "digit", "探索、内省、分析、距离", "适合讨论思考深度，不贴孤僻标签。"),
    "8": ("8", "digit", "资源、循环、经营、可见成果", "不把 8 写成发财保证。"),
    "9": ("9", "digit", "完成、愿景、总结、释放", "适合讨论收束和愿景，不写成极端结局。"),
    "phone_suffix": ("手机号尾号", "usage_context", "记忆度、隐私、沟通、个人偏好", "只讨论脱敏尾号和现实使用成本。"),
    "license_plate": ("车牌号", "usage_context", "识别度、读音、地域规则、个人偏好", "不替代交通法规、价格和可用性判断。"),
    "house_number": ("门牌号", "usage_context", "居住叙事、记忆、读音、家庭偏好", "不把门牌写成居住吉凶保证。"),
    "life_path": ("生命灵数", "method_layer", "生日加总、个人叙事、反思标签", "只作自我提问，不贴命运或性格定论。"),
}

ALIASES = {
    "零": "0", "一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9",
    "手机号": "phone_suffix", "尾号": "phone_suffix", "车牌": "license_plate", "门牌": "house_number", "生命灵数": "life_path",
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
        raise ValueError(f"unknown numerology symbol: {code}")
    canonical, layer, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "numerology_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "number_symbolism",
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为{layer}层的数字象征，围绕{focus}整理文化联想、现实使用成本和低风险偏好。",
        "reflection_questions": [
            "这些数字是否已经脱敏，是否只保留必要片段？",
            "用户真正要优化的是记忆度、价格、读音、隐私、偏好，还是情绪安定？",
            "哪些说法是文化联想，哪些是现实可验证条件？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不承诺发财、转运、复合、健康或成功。",
            "不收集或展示身份证、银行卡、验证码、密码或完整手机号。",
            "不通过号码判断第三方人品、性格、隐私或命运。",
        ],
        "next_steps": ["combine_with_number_record", "rank_real_world_constraints_first", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Digit or context, e.g. 8, 手机号, 生命灵数.")
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
