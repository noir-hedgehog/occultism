#!/usr/bin/env python3
"""Lookup safe symbolic prompts for the 36 Lenormand cards."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


CARDS = {
    "rider": ("骑士", "消息、到来、行动、开端", "不承诺消息一定会来。"),
    "clover": ("三叶草", "短期机会、轻松、运气、转瞬即逝", "不承诺好运或中奖。"),
    "ship": ("船", "远方、移动、贸易、距离", "不保证出行或交易结果。"),
    "house": ("房屋", "家庭、空间、安全感、根基", "不替代房屋安全或法律判断。"),
    "tree": ("树", "成长、健康感、长期、根系", "不作医疗或健康诊断。"),
    "clouds": ("云", "混乱、不清、疑虑、遮蔽", "不恐吓灾祸。"),
    "snake": ("蛇", "复杂、绕行、诱惑、警惕", "不贴第三方人品标签。"),
    "coffin": ("棺材", "结束、暂停、收尾、释放", "不写成死亡预言。"),
    "bouquet": ("花束", "邀请、欣赏、礼貌、好感", "不承诺关系结果。"),
    "scythe": ("镰刀", "切断、快速决定、风险、收割", "不鼓励冲动或危险行动。"),
    "whip": ("鞭子", "争执、重复、压力、节律", "不正常化暴力。"),
    "birds": ("鸟", "对话、焦虑、消息往返、社交", "不把传言当事实。"),
    "child": ("孩子", "新开始、稚嫩、小规模、学习", "不贴未成年人命运标签。"),
    "fox": ("狐狸", "策略、工作、谨慎、自保", "不指控欺骗或犯罪。"),
    "bear": ("熊", "力量、资源、保护、权威", "不替代财务或权力判断。"),
    "stars": ("星星", "愿景、网络、灵感、方向", "不承诺梦想成真。"),
    "stork": ("鹳", "变化、迁移、更新、调整", "不作怀孕判断。"),
    "dog": ("狗", "朋友、忠诚、支持、陪伴", "不替第三方承诺忠诚。"),
    "tower": ("塔", "机构、边界、孤立、规则", "不替代法律或机构流程。"),
    "garden": ("花园", "公开场域、社群、人脉、活动", "不曝光隐私。"),
    "mountain": ("山", "阻碍、延迟、距离、坚持", "不写成不可改变的命运。"),
    "crossroads": ("岔路", "选择、分叉、替代方案、自由度", "不替用户做最终决定。"),
    "mice": ("老鼠", "损耗、焦虑、细小问题、侵蚀", "不制造恐慌。"),
    "heart": ("心", "情感、喜爱、价值、温度", "不读取第三方真实感情。"),
    "ring": ("戒指", "承诺、循环、协议、绑定", "不替代合同或婚姻法律判断。"),
    "book": ("书", "知识、秘密、学习、未揭示", "不鼓励窥探隐私。"),
    "letter": ("信", "文本、通知、文件、消息", "不替代正式文件审查。"),
    "man": ("男人", "男性人物、当事人、阳性角色", "不贴性别本质标签。"),
    "woman": ("女人", "女性人物、当事人、阴性角色", "不贴性别本质标签。"),
    "lily": ("百合", "成熟、和平、慢节奏、尊重", "不作性或年龄判断。"),
    "sun": ("太阳", "清晰、活力、成功感、显现", "不承诺成功。"),
    "moon": ("月亮", "情绪、声誉、想象、周期", "不把情绪当事实。"),
    "key": ("钥匙", "开启、重点、答案感、可行性", "不写成唯一答案。"),
    "fish": ("鱼", "流动、交易、资源、现金流", "不替代财务建议。"),
    "anchor": ("锚", "稳定、坚持、工作、固定", "不承诺长期结果。"),
    "cross": ("十字", "负担、责任、信念、考验", "不恐吓为惩罚或宿命。"),
}

ALIASES = {
    "骑士": "rider", "三叶草": "clover", "船": "ship", "房屋": "house", "树": "tree", "云": "clouds",
    "蛇": "snake", "棺材": "coffin", "花束": "bouquet", "镰刀": "scythe", "鞭子": "whip", "鸟": "birds",
    "孩子": "child", "狐狸": "fox", "熊": "bear", "星星": "stars", "鹳": "stork", "狗": "dog",
    "塔": "tower", "花园": "garden", "山": "mountain", "岔路": "crossroads", "老鼠": "mice",
    "心": "heart", "戒指": "ring", "书": "book", "信": "letter", "男人": "man", "女人": "woman",
    "百合": "lily", "太阳": "sun", "月亮": "moon", "钥匙": "key", "鱼": "fish", "锚": "anchor", "十字": "cross",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower()
    if lowered in CARDS:
        return lowered
    return ALIASES.get(text, lowered)


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("card", "")))
    if not code:
        raise ValueError("query or card is required")
    if code not in CARDS:
        raise ValueError(f"unknown Lenormand card: {code}")
    canonical, keywords_raw, action = CARDS[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "lenormand_card_lookup",
        "query": str(payload.get("query", payload.get("card", code))).strip(),
        "canonical_name": canonical,
        "system": "lenormand_divination",
        "card_code": code,
        "card_set": "lenormand_36",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为雷诺曼牌义，围绕{focus}整理事件线索、现实证据、边界和低风险下一步。",
        "reflection_questions": [
            "这张牌在本轮位置里指向现实中的哪类事件、人物、资源或阻力？",
            "相邻牌是否改变了动作方向、对象或现实条件？",
            "哪些内容必须回到事实、当事人沟通、专业意见或安全措施？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把雷诺曼牌写成事实证明、专业建议、诊断、预测或最终决定。",
            "不读取第三方真实想法，不确认诅咒、附身或被害。",
            "不鼓励反复抽取直到满意。",
        ],
        "next_steps": ["combine_with_draw_record", "check_adjacent_card_pairs", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Lenormand card name, e.g. rider, heart, key, 骑士.")
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
