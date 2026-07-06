#!/usr/bin/env python3
"""Lookup safe symbolic prompts for casting-lots objects and layout zones."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "bone": ("骨片", "material", "结构、遗留、支撑、旧模式", "不使用真实遗骸、血祭或动物伤害；只处理无害复制品或已合法取得的材料。"),
    "shell": ("贝壳", "object", "边界、保护、潮汐、内外", "不声称海洋或祖灵传讯；回到边界和节奏。"),
    "stone": ("石子", "object", "稳定、重量、阻力、耐心", "不把阻滞说成命定惩罚。"),
    "key": ("钥匙", "object", "入口、许可、资源、解锁", "不承诺机会必然打开。"),
    "coin": ("硬币", "object", "交换、价值、选择、成本", "不用于投资、赌博或贷款决策。"),
    "ring": ("戒指", "object", "承诺、循环、关系边界、约定", "不替用户读取第三方真实想法。"),
    "feather": ("羽毛", "object", "轻盈、讯息、移动、放下", "不声称收到神灵或逝者信息。"),
    "seed": ("种子", "object", "潜能、播种、等待、照料", "不承诺怀孕、丰收或事业结果。"),
    "thread": ("线", "object", "连接、牵引、纠结、修补", "不鼓励操控或强迫关系。"),
    "mirror": ("小镜", "object", "反照、自省、投射、看见", "不用于偷窥第三方隐私。"),
    "center": ("中心", "zone", "当前焦点、核心议题、优先处理", "中心区只表示本轮聚焦，不证明客观事实。"),
    "left": ("左侧", "zone", "过往、内在、已知资源、保留", "方位含义依体系而变，需记录所用规则。"),
    "right": ("右侧", "zone", "未来、外显、行动、外部互动", "不把方位写成确定预言。"),
    "near": ("近身区", "zone", "可控范围、短期行动、近处支持", "近处不等于马上发生。"),
    "far": ("远端区", "zone", "长期背景、外部条件、暂不可控", "远端不等于无法改变。"),
    "crossing": ("交叠/相交", "relationship", "交集、摩擦、需要协调", "不把交叠写成冲突必然升级。"),
    "isolation": ("孤立", "relationship", "分离、暂停、独立处理、边界", "不把孤立写成被抛弃或诅咒。"),
}

ALIASES = {
    "骨": "bone",
    "骨片": "bone",
    "贝": "shell",
    "贝壳": "shell",
    "石头": "stone",
    "石子": "stone",
    "钥匙": "key",
    "硬币": "coin",
    "铜钱": "coin",
    "戒指": "ring",
    "羽毛": "feather",
    "种子": "seed",
    "线": "thread",
    "红线": "thread",
    "镜子": "mirror",
    "小镜": "mirror",
    "中心": "center",
    "中央": "center",
    "左": "left",
    "左侧": "left",
    "右": "right",
    "右侧": "right",
    "近": "near",
    "近身": "near",
    "远": "far",
    "远端": "far",
    "交叠": "crossing",
    "相交": "crossing",
    "孤立": "isolation",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", payload.get("object", ""))))
    if not code:
        raise ValueError("query, symbol, or object is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown casting lots symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "casting_lots_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", payload.get("object", code)))).strip(),
        "canonical_name": canonical,
        "system": "casting_lots_symbolic_reflection",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为符物抛掷象征，围绕{focus}整理资源、边界、阻力、可控行动和现实验证。",
        "reflection_questions": [
            "这个物件或位置在本轮体系里代表资源、阻力、边界还是下一步？",
            "盘面关系有没有被记录为观察，而不是被直接写成事实？",
            "哪些内容必须回到当事人沟通、现实证据、专业意见或安全措施？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把符物盘面写成事实证明、专业建议、诊断、预测或最终决定。",
            "不确认诅咒、附身、被害、祖灵传讯、驱邪效果或第三方真实想法。",
            "不使用真实遗骸、动物伤害、血祭、违法材料或反复抛掷直到满意。",
        ],
        "next_steps": ["combine_with_casting_lots_layout_record", "rank_real_world_evidence_first", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Casting object, zone, or relationship, e.g. shell, key, center.")
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
