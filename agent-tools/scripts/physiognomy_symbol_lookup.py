#!/usr/bin/env python3
"""Lookup safe palmistry and physiognomy symbols for cultural reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "life_line": ("生命线", "palm_line", "活力节奏、身体感受、生活韧性、自我照顾", "把生命线作为活力和节奏的象征，不判断寿命长短。"),
    "head_line": ("智慧线", "palm_line", "思考方式、学习节奏、判断偏好、注意力", "适合讨论思考风格和选择习惯，不贴智商或能力标签。"),
    "heart_line": ("感情线", "palm_line", "情感表达、关系边界、亲密需求、感受流动", "适合整理关系表达和边界，不断言桃花或婚恋结局。"),
    "fate_line": ("事业线", "palm_line", "责任感、职业叙事、阶段转折、外部结构", "适合讨论事业叙事和现实规划，不承诺成败或财富。"),
    "sun_line": ("太阳线", "palm_line", "可见度、表达、作品感、认可需求", "适合连接创作和呈现，不写成名气保证。"),
    "mount": ("掌丘", "palm_region", "资源偏好、行动气质、传统星体象征、身体化隐喻", "仅作为传统部位象征，不推断人格优劣。"),
    "forehead": ("额头", "face_region", "开阔感、计划感、早年叙事、表达入口", "只讨论传统象征和形象叙事，不判断智力或阶层。"),
    "eyebrows": ("眉", "face_feature", "边界、气势、秩序感、人际表达", "适合讨论印象管理和文化象征，不判断人品。"),
    "eyes": ("眼", "face_feature", "注意力、情绪可见度、观察方式、交流感", "不从眼睛判断心理疾病、诚实与否或危险性。"),
    "nose": ("鼻", "face_feature", "资源感、执行、中心感、传统财帛象征", "不把鼻相写成财富保证或阶层标签。"),
    "mouth": ("嘴", "face_feature", "表达、滋养、沟通方式、需求说出", "适合讨论沟通习惯，不判断口德或道德优劣。"),
    "chin": ("下巴", "face_region", "收束、承载、晚期叙事、稳定感", "不判断晚年命运或家庭结局。"),
    "mole": ("痣相", "mark_symbol", "位置叙事、记忆点、民俗联想、身体地图", "只作为民俗位置象征，不宣称灾祸、疾病或命运标记。"),
}

ALIASES = {
    "生命线": "life_line",
    "地纹": "life_line",
    "智慧线": "head_line",
    "头脑线": "head_line",
    "感情线": "heart_line",
    "天纹": "heart_line",
    "事业线": "fate_line",
    "命运线": "fate_line",
    "太阳线": "sun_line",
    "成功线": "sun_line",
    "掌丘": "mount",
    "额头": "forehead",
    "天庭": "forehead",
    "眉毛": "eyebrows",
    "眉": "eyebrows",
    "眼睛": "eyes",
    "眼": "eyes",
    "鼻相": "nose",
    "鼻子": "nose",
    "鼻": "nose",
    "嘴巴": "mouth",
    "嘴": "mouth",
    "口": "mouth",
    "下巴": "chin",
    "地阁": "chin",
    "痣": "mole",
    "痣相": "mole",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    if text in SYMBOLS:
        return text
    return ALIASES.get(text, text)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("feature_code", ""))))
    if not code:
        raise ValueError("query, symbol, or feature_code is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown physiognomy symbol: {code}")
    canonical, layer, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "self_reflection"
    return {
        "tool": "physiognomy_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "palmistry_and_physiognomy_symbolism",
        "symbol_layer": layer,
        "symbol_code": code,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为{layer}层的文化象征，围绕{focus}讨论可能的自我叙事、现实观察和低风险行动。",
        "reflection_questions": [
            "这个观察来自本人自述、授权观察，还是匿名文化学习？",
            "这个符号在用户叙事里更像资源、张力、边界，还是提醒？",
            "有哪些现实证据、身体感受或关系事实可以帮助用户自己校准？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不判断寿命、疾病、死亡、怀孕、心理状态或身体风险。",
            "不根据外貌或掌纹断定人品、阶层、富贵贫贱、旺克或婚恋结局。",
            "不把手相/面相用于第三方隐私分析、招聘筛选、身份识别或歧视性评价。",
        ],
        "next_steps": [
            "combine_with_user_observation_record",
            "draft_symbolic_non_deterministic_interpretation",
            "run_mystic_output_lint",
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
    parser.add_argument("--query", help="Symbol name, e.g. 生命线, 事业线, 鼻相.")
    parser.add_argument("--focus", help="Optional consultation focus.")
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
