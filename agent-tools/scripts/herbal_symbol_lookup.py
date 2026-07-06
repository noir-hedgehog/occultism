#!/usr/bin/env python3
"""Lookup safe symbolic prompts for herbs, plants, and green witchcraft items."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "rosemary": ("迷迭香 / Rosemary", "herb", "记忆、整理、学习、复盘、清晰边界", "不写成治疗认知、消炎、驱邪或考试保证。"),
    "sage": ("鼠尾草 / Sage", "herb", "清理、结束、空间复位、谨慎来源、文化尊重", "不写成驱灵保证、烟熏步骤、文化挪用或必须焚烧。"),
    "bay_leaf": ("月桂叶 / Bay Leaf", "leaf", "愿望书写、目标、确认、短句、可撤回提醒", "不写成显化保证、烧叶步骤或必然成真。"),
    "mugwort": ("艾草/艾蒿 / Mugwort", "herb", "边界、季节、门槛、梦境记录、民俗记忆", "不写成催梦、治疗、孕婴可用或驱邪保证。"),
    "mint": ("薄荷 / Mint", "herb", "清醒、边界、空间感、停顿、轻快", "不写成治疗头痛、感冒、消化或适合孕婴宠物。"),
    "chamomile": ("洋甘菊 / Chamomile", "flower_herb", "柔和、收束、睡前仪式感、安静提醒", "不写成治疗失眠、焦虑或替代药物。"),
    "basil": ("罗勒 / Basil", "herb", "保护边界、日常照料、厨房记忆、实际行动", "不写成招财保证、护身保证或必须食用。"),
    "lavender": ("薰衣草 / Lavender", "flower_herb", "安静、整理、柔和、睡前边界、温和提醒", "不写成治疗失眠、焦虑或可直接用于皮肤/入口。"),
    "nettle": ("荨麻 / Nettle", "herb", "边界、刺痛感、保护自己、现实距离", "不写成治疗、采摘建议、食用建议或攻击他人。"),
    "salt_bowl": ("盐碗/盐罐", "container", "边界、吸纳隐喻、收纳、定点提醒、结束后清理", "不写成吸走邪气、治疗、食用或保证净化。"),
    "sachet": ("草药袋/香草包", "object", "携带提醒、低成本物件、边界、祝愿、可停止", "不写成护身保证、爱情咒或必须高价开光。"),
    "journal_card": ("植物意图卡/标签", "method", "书写、命名、复盘、非接触、可撤回", "不写成咒语命令、操控他人或结果保证。"),
}

ALIASES = {
    "迷迭香": "rosemary",
    "rosemary": "rosemary",
    "鼠尾草": "sage",
    "sage": "sage",
    "月桂": "bay_leaf",
    "月桂叶": "bay_leaf",
    "bay leaf": "bay_leaf",
    "bay_leaf": "bay_leaf",
    "艾草": "mugwort",
    "艾蒿": "mugwort",
    "mugwort": "mugwort",
    "薄荷": "mint",
    "mint": "mint",
    "洋甘菊": "chamomile",
    "chamomile": "chamomile",
    "罗勒": "basil",
    "basil": "basil",
    "薰衣草": "lavender",
    "lavender": "lavender",
    "荨麻": "nettle",
    "nettle": "nettle",
    "盐碗": "salt_bowl",
    "盐罐": "salt_bowl",
    "salt bowl": "salt_bowl",
    "草药袋": "sachet",
    "香草包": "sachet",
    "草本包": "sachet",
    "sachet": "sachet",
    "意图卡": "journal_card",
    "植物意图卡": "journal_card",
    "植物标签": "journal_card",
    "journal card": "journal_card",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered.replace(" ", "_")))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("plant", ""))))
    if not code:
        raise ValueError("query, symbol, or plant is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown herbal symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "herbal_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("plant", code)))).strip(),
        "canonical_name": canonical,
        "system": "herbal_plant_magic_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "herbal_plants_objects_methods_safety_layers",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为草本/植物象征，围绕{focus}整理感受、物件来源、现实安全边界和低风险下一步。",
        "reflection_questions": [
            "这是草本、叶片、花草、容器、使用方式还是私人联想？",
            "它更像启动、收束、边界、记忆、祝愿、空间复位还是书写提醒？",
            "哪些判断必须回到现实安全、非接触、预算、专业支持和停止条件？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把草本或植物包写成治疗、诊断、驱邪、净化保证、开运招财、爱情咒、诅咒或专业建议。",
            "不提供内服、泡水喝、外敷、药浴、孕婴宠物过敏、野采辨毒或未知植物食用判断。",
            "不制造必须购买、高价套装、会员囤货、代理课程或反复依赖。",
        ],
        "next_steps": ["combine_with_herbal_context", "prefer_non_contact_low_risk_action", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Herbal symbol, e.g. 迷迭香, 鼠尾草, 月桂叶.")
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
