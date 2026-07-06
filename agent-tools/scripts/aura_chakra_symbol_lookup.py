#!/usr/bin/env python3
"""Lookup safe symbolic prompts for aura colors, chakras, and energy sensations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "root": ("海底轮", "chakra", "身体、稳定、边界、现实资源", "不替代创伤、焦虑或安全问题的专业支持。"),
    "sacral": ("脐轮", "chakra", "感受、流动、创造、关系界限", "不把情绪或亲密关系写成命运证明。"),
    "solar_plexus": ("太阳神经丛", "chakra", "行动、意志、消化经验、选择感", "不诊断消化、内分泌或焦虑问题。"),
    "heart": ("心轮", "chakra", "连接、照料、悲伤、开放与边界", "不承诺复合、疗愈或第三方情感结果。"),
    "throat": ("喉轮", "chakra", "表达、倾听、边界、未说出口", "不把沉默或表达困难诊断成疾病或灵性缺陷。"),
    "third_eye": ("眉心轮", "chakra", "观察、想象、模式识别、内在图像", "不确认预言、幻觉、通灵或外部事实。"),
    "crown": ("顶轮", "chakra", "意义、连结、敬畏、开放问题", "不确认神谕、附身、灵体命令或身份等级。"),
    "white": ("白色", "aura_color", "简化、留白、清理、边界", "不承诺净化、驱邪或能量清零。"),
    "blue": ("蓝色", "aura_color", "表达、安静、秩序、距离", "不把颜色写成性格或命运标签。"),
    "green": ("绿色", "aura_color", "修复、关系、空间、节奏", "不替代医疗恢复或心理治疗。"),
    "yellow": ("黄色", "aura_color", "清晰、注意、行动、学习", "不承诺成功、财富或考试结果。"),
    "purple": ("紫色", "aura_color", "想象、象征、深度、边界", "不把颜色写成灵性等级。"),
    "warmth": ("发热", "sensation", "注意力、激活、紧张或温度变化", "身体不适、持续疼痛或发热优先现实检查。"),
    "heaviness": ("沉重", "sensation", "压力、负担、需要放慢", "不把沉重写成附身、低频或业障。"),
    "tingling": ("麻感", "sensation", "注意力集中、身体信号、边界提醒", "持续麻木、疼痛或功能异常优先就医。"),
}

ALIASES = {
    "海底轮": "root",
    "根轮": "root",
    "root": "root",
    "脐轮": "sacral",
    "生殖轮": "sacral",
    "sacral": "sacral",
    "太阳神经丛": "solar_plexus",
    "太阳轮": "solar_plexus",
    "solar plexus": "solar_plexus",
    "心轮": "heart",
    "heart": "heart",
    "喉轮": "throat",
    "throat": "throat",
    "眉心轮": "third_eye",
    "第三眼": "third_eye",
    "third eye": "third_eye",
    "顶轮": "crown",
    "crown": "crown",
    "白": "white",
    "白色": "white",
    "蓝": "blue",
    "蓝色": "blue",
    "绿": "green",
    "绿色": "green",
    "黄": "yellow",
    "黄色": "yellow",
    "紫": "purple",
    "紫色": "purple",
    "发热": "warmth",
    "热": "warmth",
    "沉": "heaviness",
    "沉重": "heaviness",
    "麻": "tingling",
    "麻感": "tingling",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("center", ""))))
    if not code:
        raise ValueError("query, symbol, or center is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown aura/chakra symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "aura_chakra_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("center", code)))).strip(),
        "canonical_name": canonical,
        "system": "aura_chakra_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为气场/脉轮象征，围绕{focus}整理身体感受、情绪线索、边界提醒和低风险行动。",
        "reflection_questions": [
            "这是文化学习、冥想记录、身体感受整理，还是在寻找诊断或确定性证明？",
            "感受是否持续、强烈、伴随疼痛/失眠/惊恐/幻听幻视或影响功能？",
            "哪些内容可以作为象征提醒，哪些必须回到身体照护、专业支持或现实沟通？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把气场、脉轮或颜色写成诊断、疗愈承诺、灵体证明、身份等级或命运标签。",
            "不替代医疗、心理健康、药物、紧急安全、法律或财务建议。",
            "不读取第三方真实想法，不制造付费疗愈或反复检测依赖。",
        ],
        "next_steps": ["combine_with_sensation_record", "rank_real_world_body_context_first", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Aura color, chakra, or sensation symbol.")
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
