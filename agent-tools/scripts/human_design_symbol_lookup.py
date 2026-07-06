#!/usr/bin/env python3
"""Lookup safe symbolic prompts for Human Design symbols."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "manifestor": ("显示者 / Manifestor", "type", "启动、影响、告知、边界、独立行动", "不写成天生领导、可忽视他人或必须独自行动。"),
    "generator": ("生产者 / Generator", "type", "回应、体力、持续投入、满意感、现实反馈", "不写成只能等待、不能主动或必须劳累。"),
    "manifesting_generator": ("显示生产者 / Manifesting Generator", "type", "回应后行动、试错、多线程、调整路径", "不把多变写成不可靠或必须同时做很多事。"),
    "projector": ("投射者 / Projector", "type", "识别、引导、邀请、节奏、能量管理", "不写成低能量、不能工作或必须等别人认可。"),
    "reflector": ("反映者 / Reflector", "type", "环境映照、周期观察、开放性、月亮节奏", "不写成没有自我、脆弱或必须等待一个月做所有决定。"),
    "emotional_authority": ("情绪权威", "authority", "情绪波、等待清晰、避免高峰低谷即时定案", "不替代心理健康支持或把情绪写成病理。"),
    "sacral_authority": ("荐骨权威", "authority", "身体回应、是/否感、体感反馈、逐步验证", "不写成身体感觉永远正确或可替代事实核查。"),
    "splenic_authority": ("脾脏权威", "authority", "当下直觉、安全感、细微信号、一次性提醒", "不把直觉写成事实证明或安全判断替代。"),
    "ego_authority": ("意志/自我权威", "authority", "承诺、资源、欲望、可持续交换", "不鼓励强撑、控制或以自我为唯一标准。"),
    "self_projected_authority": ("自我投射权威", "authority", "说出来听见自己、方向感、身份一致性", "不把表达感受写成客观事实。"),
    "mental_projector_authority": ("环境/心智投射者权威", "authority", "环境取样、对话回声、空间支持", "不让环境选择替代专业或重大现实判断。"),
    "lunar_authority": ("月亮权威", "authority", "周期观察、阶段记录、环境变化中的稳定感", "不把等待周期写成拖延命令。"),
    "profile": ("人生角色 / Profile", "profile_layer", "学习方式、互动位置、生活主题、观察视角", "不把 profile 写成人格定论或关系筛选。"),
    "defined_center": ("定义中心", "center_layer", "稳定表达、可观察惯性、资源使用方式", "不写成固定人格或不能改变。"),
    "undefined_center": ("未定义中心", "center_layer", "环境放大、学习空间、边界练习", "不写成缺陷、漏洞或低频。"),
    "channel": ("通道", "circuit_layer", "主题连线、能量路径、稳定议题", "不把通道写成能力保证或命运证明。"),
    "gate": ("闸门", "circuit_layer", "具体主题、触发语汇、细节提醒", "不把单个闸门孤立成断语。"),
}

ALIASES = {
    "显示者": "manifestor",
    "manifestor": "manifestor",
    "生产者": "generator",
    "generator": "generator",
    "显生": "manifesting_generator",
    "显示生产者": "manifesting_generator",
    "manifesting generator": "manifesting_generator",
    "manifesting_generator": "manifesting_generator",
    "投射者": "projector",
    "projector": "projector",
    "反映者": "reflector",
    "reflector": "reflector",
    "情绪权威": "emotional_authority",
    "emotional": "emotional_authority",
    "荐骨权威": "sacral_authority",
    "sacral": "sacral_authority",
    "脾脏权威": "splenic_authority",
    "splenic": "splenic_authority",
    "意志权威": "ego_authority",
    "自我权威": "ego_authority",
    "自我投射权威": "self_projected_authority",
    "环境权威": "mental_projector_authority",
    "月亮权威": "lunar_authority",
    "人生角色": "profile",
    "profile": "profile",
    "定义中心": "defined_center",
    "未定义中心": "undefined_center",
    "开放中心": "undefined_center",
    "通道": "channel",
    "channel": "channel",
    "闸门": "gate",
    "gate": "gate",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered.replace(" ", "_")))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("type", ""))))
    if not code:
        raise ValueError("query, symbol, or type is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown human design symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "human_design_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("type", code)))).strip(),
        "canonical_name": canonical,
        "system": "human_design_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "human_design_types_authorities_profile_centers_channels_gates",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为人类图象征，围绕{focus}整理自我观察、现实证据、边界和低风险下一步。",
        "reflection_questions": [
            "这是类型、策略、权威、人生角色、中心、通道还是闸门？",
            "它更像决策节奏、能量管理、沟通方式、环境反馈还是边界提醒？",
            "哪些结论必须回到现实证据、专业支持、隐私同意、预算和当事人沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把人类图写成确定预言、人格定论、诊断、关系筛选、职业保证、财富结果或专业意见。",
            "不使用出生资料窥探第三方、操控他人或替别人做重大决定。",
            "不制造必须高价解读、必须报课或反复看图依赖。",
        ],
        "next_steps": ["combine_with_human_design_chart_record", "prefer_reality_check_and_low_risk_action", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Human Design symbol, e.g. 投射者, 情绪权威, profile.")
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
