#!/usr/bin/env python3
"""Lookup safe classification examples for folk ritual source material."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import ritual_source_guard


EXAMPLES = {
    "regional_folk": {
        "display_name": "地域民俗样例",
        "classification_cues": ["某地", "地方", "村里", "老人说", "家里流传", "民间"],
        "required_context": ["地区/社群", "口述或文本来源", "适用场景", "是否涉及危险材料"],
        "safe_use": "可写作某地或某社群流传的文化材料；缺上下文时只说未验证民俗说法。",
        "not_allowed": "不可写成全国通用规则、真实驱邪机制或必须执行的仪式。",
        "example_records": [
            {
                "source_text": "资料声称某地搬家后会先清扫入口、开灯并说一句安定话。",
                "safe_framing": "可表述为局部民俗或家庭习惯中的空间安定象征。",
                "needs": ["具体地区", "来源形式", "是否只是家庭经验"],
            },
            {
                "source_text": "老人说搬家后点蜡烛烧纸能驱邪。",
                "safe_framing": "只能作为未验证民俗说法，并转译为无火清洁、通风和开灯。",
                "needs": ["地区", "来源上下文", "明火风险说明"],
            },
        ],
    },
    "religious_tradition": {
        "display_name": "宗教传统样例",
        "classification_cues": ["寺", "道观", "法事", "神明", "佛", "道教", "宗教"],
        "required_context": ["具体传统/机构", "授权或公开资料", "宗教语境", "是否适合外部复述"],
        "safe_use": "可写作特定传统中的文化或宗教语境，提醒尊重传承和现场规范。",
        "not_allowed": "不可简化成通用驱邪教程，不可冒充宗教人士给法事步骤。",
        "example_records": [
            {
                "source_text": "资料提到某寺院会在特定仪轨中做洒净。",
                "safe_framing": "只说明这是特定宗教语境中的仪轨概念，不复述执行步骤。",
                "needs": ["寺院/传统", "公开来源", "适用边界"],
            },
            {
                "source_text": "有人说去道观请符就一定能解决问题。",
                "safe_framing": "不能保证效果；可建议尊重宗教场域，并优先处理现实安全与心理支持。",
                "needs": ["来源", "是否商业化", "风险筛查"],
            },
        ],
    },
    "modern_wellness": {
        "display_name": "现代身心实践样例",
        "classification_cues": ["冥想", "呼吸", "音乐", "灯光", "疗愈", "身心"],
        "required_context": ["目标", "风险人群", "是否替代专业支持", "可中止条件"],
        "safe_use": "可作为现代象征性安定流程，强调自我调节和现实检查。",
        "not_allowed": "不可声称治疗疾病、消灾、替代心理/医疗支持或保证效果。",
        "example_records": [
            {
                "source_text": "睡前用柔和灯光、白噪音和写担忧做安定流程。",
                "safe_framing": "可作为低风险睡前安定流程。",
                "needs": ["持续失眠时的求助路径", "不替代治疗说明"],
            },
            {
                "source_text": "搬家后用清洁、通风和整理物品建立新空间感。",
                "safe_framing": "可作为现代空间复位流程。",
                "needs": ["燃气/电路/霉菌检查", "体力和时间限制"],
            },
        ],
    },
    "commercial_new_age": {
        "display_name": "商业新灵性样例",
        "classification_cues": ["水晶", "能量", "课程", "疗愈师", "开运", "显化"],
        "required_context": ["售卖方/课程", "价格和利益关系", "效果声明", "风险承诺"],
        "safe_use": "可作为商业或现代改编说法审视，不应当作传统或事实。",
        "not_allowed": "不可背书收费效果、保证开运、治疗、复合、发财或驱邪成功。",
        "example_records": [
            {
                "source_text": "某课程说摆水晶阵能清理负能量并保证转运。",
                "safe_framing": "标注为商业化效果声明，不能保证效果；可改成低风险空间整理。",
                "needs": ["课程/机构", "收费关系", "效果证据", "替代专业风险"],
            },
            {
                "source_text": "疗愈师说买指定物品能解除诅咒。",
                "safe_framing": "标注为商业风险和恐惧营销信号，不确认诅咒。",
                "needs": ["收费信息", "恐惧诱导", "用户脆弱状态"],
            },
        ],
    },
    "personal_preference": {
        "display_name": "个人经验样例",
        "classification_cues": ["我习惯", "我自己", "个人", "我家", "我的方法"],
        "required_context": ["个人适用原因", "是否有危险步骤", "是否推广给他人"],
        "safe_use": "可写作个人偏好或自我安定方法，不推广成普遍规则。",
        "not_allowed": "不可说成所有人都该做，或证明超自然因果。",
        "example_records": [
            {
                "source_text": "我个人搬家后会擦桌子、开灯、放一杯水。",
                "safe_framing": "可作为个人空间安定偏好，适合低风险复用。",
                "needs": ["无火无摄入确认", "个人化说明"],
            },
            {
                "source_text": "我习惯把担忧写下来收进盒子。",
                "safe_framing": "可作为情绪收束象征动作。",
                "needs": ["不替代现实沟通或专业支持"],
            },
        ],
    },
    "unknown": {
        "display_name": "未知来源样例",
        "classification_cues": ["网上说", "听说", "据说", "有人说", "不知道出处"],
        "required_context": ["来源类型", "出处", "地区/社群", "是否含危险步骤"],
        "safe_use": "只作为待核材料；可转向安全替代，不进入强结论。",
        "not_allowed": "不可写成传统、事实、指南或有效方法。",
        "example_records": [
            {
                "source_text": "网上说烧纸能赶走不干净的东西。",
                "safe_framing": "未知来源且含明火风险；不提供烧纸步骤，转为无火整理。",
                "needs": ["来源", "明火风险", "用户恐惧程度"],
            },
            {
                "source_text": "听说睡前念几句就不会做噩梦。",
                "safe_framing": "未知来源，不保证效果；可改成睡前安定语和睡眠监测。",
                "needs": ["是否持续失眠", "是否出现幻听幻视"],
            },
        ],
    },
}


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("source_text", ""))).strip()
    requested = str(payload.get("source_type", "")).strip()
    if requested:
        source_type = ritual_source_guard.normalize_source_type(requested, text)
    elif text:
        source_type = ritual_source_guard.normalize_source_type("", text)
    else:
        source_type = "unknown"
    item = EXAMPLES[source_type]
    guard_result = ritual_source_guard.guard({"request_text": text or item["example_records"][0]["source_text"], "source_type": source_type})
    return {
        "source_type": source_type,
        "display_name": item["display_name"],
        "classification_cues": item["classification_cues"],
        "required_context": item["required_context"],
        "safe_use": item["safe_use"],
        "not_allowed": item["not_allowed"],
        "example_records": item["example_records"],
        "guard_summary": {
            "source_claim_level": guard_result["source_claim_level"],
            "missing_source_fields": guard_result["missing_source_fields"],
            "certainty_flags": guard_result["certainty_flags"],
            "risk_level": guard_result["safety_result"]["risk_level"],
            "can_use_as_cultural_context": guard_result["can_use_as_cultural_context"],
            "can_offer_steps": guard_result["can_offer_steps"],
        },
        "next_steps": [
            "classify_with_ritual_source_guard",
            "ask_for_required_context_when_missing",
            "convert_to_low_risk_protocol_when_needed",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload.update(json.load(f))
    if args.text:
        payload["request_text"] = args.text
    if args.source_type:
        payload["source_type"] = args.source_type
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Ritual source text.")
    parser.add_argument("--source-type", help="Optional source type.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
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
