#!/usr/bin/env python3
"""Lookup safe symbolic prompts for aroma and scent symbols."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "lavender": ("薰衣草 / Lavender", "scent", "安静、收束、柔和、睡前边界、放松提醒", "不写成治疗失眠、焦虑或替代药物。"),
    "rose": ("玫瑰 / Rose", "scent", "温柔、关系表达、自我照料、心意、审美", "不写成保证桃花、复合或操控关系。"),
    "citrus": ("柑橘 / Citrus", "scent", "清新、启动、明亮、整理、上午节奏", "不写成保证提神、治抑郁或必须日晒使用。"),
    "peppermint": ("薄荷 / Peppermint", "scent", "清醒、边界、呼吸空间、停顿、集中", "不写成治疗头痛、感冒或可给孕婴宠物使用。"),
    "frankincense": ("乳香 / Frankincense", "scent", "沉静、仪式感、呼吸、纪念、内在空间", "不写成驱邪、神迹、治疗或必须购买。"),
    "sandalwood": ("檀香 / Sandalwood", "scent", "稳定、慢下来、专注、空间沉淀、收心", "不写成宗教保证、驱灵或适合所有人。"),
    "cedarwood": ("雪松 / Cedarwood", "scent", "结构、根基、收纳、边界、长期感", "不写成保护结界或驱邪保证。"),
    "rosemary": ("迷迭香 / Rosemary", "scent", "记忆、清理、准备、学习、复盘", "不写成治疗认知、疾病或考试保证。"),
    "sachet": ("香包/香囊", "object", "携带提醒、边界物、季节感、祝愿、低成本象征", "不写成护身保证或必须高价开光。"),
    "diffuser": ("扩香/香薰机", "method", "空间气味、时长边界、通风、环境切换", "不建议整夜、密闭、无人看管或连续依赖。"),
    "smelling_strip": ("闻香纸/试香", "method", "短时观察、偏好记录、非接触、可停止", "不写成必须反复闻到满意。"),
    "ventilation": ("通风/开窗", "safety_layer", "现实安全、结束动作、环境更新、可撤回", "不把通风写成能量净化保证。"),
}

ALIASES = {
    "薰衣草": "lavender",
    "lavender": "lavender",
    "玫瑰": "rose",
    "rose": "rose",
    "柑橘": "citrus",
    "甜橙": "citrus",
    "橙花": "citrus",
    "citrus": "citrus",
    "薄荷": "peppermint",
    "peppermint": "peppermint",
    "乳香": "frankincense",
    "frankincense": "frankincense",
    "檀香": "sandalwood",
    "sandalwood": "sandalwood",
    "雪松": "cedarwood",
    "cedarwood": "cedarwood",
    "迷迭香": "rosemary",
    "rosemary": "rosemary",
    "香包": "sachet",
    "香囊": "sachet",
    "sachet": "sachet",
    "扩香": "diffuser",
    "香薰机": "diffuser",
    "diffuser": "diffuser",
    "闻香纸": "smelling_strip",
    "试香": "smelling_strip",
    "smelling strip": "smelling_strip",
    "通风": "ventilation",
    "开窗": "ventilation",
    "ventilation": "ventilation",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered.replace(" ", "_")))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("scent", ""))))
    if not code:
        raise ValueError("query, symbol, or scent is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown aroma symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "aroma_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("scent", code)))).strip(),
        "canonical_name": canonical,
        "system": "aroma_scent_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "aroma_scents_objects_methods_safety_layers",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为气味象征，围绕{focus}整理感受、环境线索、现实安全边界和低风险下一步。",
        "reflection_questions": [
            "这是气味、物件、使用方式还是安全层？",
            "它更像启动、收束、安定、边界、纪念、空间切换还是偏好记录？",
            "哪些判断必须回到现实安全、通风、预算、专业支持和停止条件？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把精油或气味写成治疗、诊断、驱邪、净化保证、开运招财、关系操控或专业建议。",
            "不提供内服、原液涂抹、孕婴宠物过敏等具体安全适用判断。",
            "不制造必须购买、高价套装、会员囤货、代理课程或反复依赖。",
        ],
        "next_steps": ["combine_with_aroma_context", "prefer_non_contact_low_risk_action", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Aroma symbol, e.g. 薰衣草, 玫瑰, 扩香.")
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
