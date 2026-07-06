#!/usr/bin/env python3
"""Lookup safe symbolic prompts for sigils, seals, and magic-circle elements."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "circle": ("圆 / Circle", "shape", "边界、容器、循环、完整、可撤回的范围", "不写成召唤圈、封印灵体或绝对防护。"),
    "line": ("线 / Line", "shape", "方向、连接、路径、划分、下一步", "不写成强制绑定、控制或切断他人。"),
    "triangle": ("三角 / Triangle", "shape", "意图、聚焦、三步、稳定支点", "不写成召唤符号、攻击或灵验保证。"),
    "square": ("方形 / Square", "shape", "结构、边界、容纳、现实步骤", "不写成牢笼、困住他人或绝对安全。"),
    "spiral": ("螺旋 / Spiral", "shape", "回看、迭代、深入、逐步展开", "不写成迷魂、操控或无法停止。"),
    "cross": ("十字/交叉 / Cross", "shape", "交点、选择、暂停、校准", "不写成宗教权威命令、诅咒或攻击。"),
    "star": ("星形 / Star", "shape", "方向、希望、焦点、远处目标", "不写成必然成真、召唤或开运保证。"),
    "eye": ("眼睛 / Eye", "motif", "觉察、观察、提醒、看见盲点", "不写成监视他人、读心或恶眼攻击。"),
    "key": ("钥匙 / Key", "motif", "进入、许可、选择权、解锁问题", "不写成保证开门、破解限制或违法绕过。"),
    "seed": ("种子 / Seed", "motif", "开始、小步、培育、延迟满足", "不写成必然显化或收益保证。"),
    "letter_bind": ("字母合并 / Letter Bind", "method", "缩写、归纳、去除噪音、私人记号", "不写成密令、操控他人或不可撤回。"),
    "journal_activation": ("日志激活/复盘", "method", "书写、命名、看见、复盘、行动承诺", "不写成献祭、焚烧、滴血或必须每天重复。"),
}

ALIASES = {
    "圆": "circle",
    "圆圈": "circle",
    "圆形": "circle",
    "circle": "circle",
    "线": "line",
    "直线": "line",
    "line": "line",
    "三角": "triangle",
    "三角形": "triangle",
    "triangle": "triangle",
    "方形": "square",
    "正方形": "square",
    "square": "square",
    "螺旋": "spiral",
    "spiral": "spiral",
    "十字": "cross",
    "交叉": "cross",
    "cross": "cross",
    "星形": "star",
    "星": "star",
    "star": "star",
    "眼睛": "eye",
    "眼": "eye",
    "eye": "eye",
    "钥匙": "key",
    "key": "key",
    "种子": "seed",
    "seed": "seed",
    "字母合并": "letter_bind",
    "字母组合": "letter_bind",
    "letter bind": "letter_bind",
    "letter_bind": "letter_bind",
    "日志激活": "journal_activation",
    "复盘": "journal_activation",
    "journal activation": "journal_activation",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered.replace(" ", "_")))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("element", ""))))
    if not code:
        raise ValueError("query, symbol, or element is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown sigil symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "sigil_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("element", code)))).strip(),
        "canonical_name": canonical,
        "system": "sigil_seal_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "symbol_set": "sigil_shapes_motifs_methods_safety_layers",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为 sigil/符号印记元素，围绕{focus}整理意图、边界、现实行动和停止条件。",
        "reflection_questions": [
            "这个元素是形状、字母、图像母题、排列方式还是私人联想？",
            "它更像边界、方向、聚焦、许可、开始、复盘还是暂停？",
            "哪些判断必须回到可擦除、无火、非身体伤害、非操控和现实行动？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把 sigil 写成召唤、驱邪、诅咒、爱情咒、显化保证、灵验证明或专业建议。",
            "不提供滴血、割伤、刻皮肤、纹身刺青、焚烧、密闭燃烧或危险销毁步骤。",
            "不制造高价课程、模板购买、反复依赖或对第三方的操控。",
        ],
        "next_steps": ["combine_with_sigil_context", "prefer_removable_low_risk_action", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Sigil element, e.g. 圆, 三角, 字母合并.")
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
