#!/usr/bin/env python3
"""Record provenance for folk-custom claims without upgrading weak sources into tradition."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Iterable


SOURCE_ALIASES = {
    "family_oral": "family_oral",
    "family": "family_oral",
    "家人": "family_oral",
    "家庭": "family_oral",
    "老人说": "family_oral",
    "regional_oral": "regional_oral",
    "regional": "regional_oral",
    "地方": "regional_oral",
    "本地": "regional_oral",
    "地方口述": "regional_oral",
    "religious_context": "religious_context",
    "religious": "religious_context",
    "寺庙": "religious_context",
    "宗教": "religious_context",
    "published_reference": "published_reference",
    "published": "published_reference",
    "book": "published_reference",
    "paper": "published_reference",
    "书": "published_reference",
    "文献": "published_reference",
    "internet_claim": "internet_claim",
    "internet": "internet_claim",
    "网络": "internet_claim",
    "网上": "internet_claim",
    "短视频": "internet_claim",
    "commercial_claim": "commercial_claim",
    "commercial": "commercial_claim",
    "课程": "commercial_claim",
    "商家": "commercial_claim",
    "personal_preference": "personal_preference",
    "personal": "personal_preference",
    "个人": "personal_preference",
    "unknown": "unknown",
    "未知": "unknown",
}

SOURCE_RELIABILITY = {
    "family_oral": "local_oral_context",
    "regional_oral": "regional_oral_context",
    "religious_context": "bounded_religious_context",
    "published_reference": "documented_reference",
    "internet_claim": "unverified_internet_claim",
    "commercial_claim": "commercial_interest_claim",
    "personal_preference": "personal_preference",
    "unknown": "unknown",
}

USAGE_CONTEXTS = {
    "cultural_learning",
    "family_communication",
    "event_planning",
    "writing",
    "self_soothing",
    "source_audit",
}

CUSTOM_HINTS = {
    "端午": "端午习俗",
    "艾草": "艾草",
    "香囊": "香囊",
    "搬家": "搬家习俗",
    "乔迁": "搬家习俗",
    "入宅": "搬家习俗",
    "开灯": "搬家习俗",
    "清扫": "清扫入口",
    "筷子": "筷子插饭",
    "吹口哨": "夜里吹口哨",
    "中元": "中元禁忌",
    "烧纸": "烧纸习俗",
    "正月剪": "正月剪发",
    "剪头发": "正月剪发",
    "孕妇": "孕妇禁忌",
}

RISK_PATTERNS = {
    "dangerous_action": ("密闭烧", "密闭房间", "烧纸", "点火", "火盆", "放血", "割", "刀", "喝符水", "吞符", "通宵不睡"),
    "supernatural_certainty": ("一定有鬼", "真的有鬼", "必定", "百分百", "必遭", "一定会", "肯定冲撞", "必倒霉", "一定倒霉"),
    "professional_replacement": ("不用看医生", "不用去医院", "不用报警", "不用消防", "不用检查", "不用律师"),
    "commercial_interest": ("课程", "开运物", "法物", "购买", "套餐", "收费", "老师说买", "保证转运"),
    "universal_authority_claim": ("全国都", "所有地区", "必须遵守", "祖传绝对", "唯一正统"),
}


def contains_any(text: str, values: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def normalize_source_type(raw: object, text: str) -> str:
    key = str(raw or "").strip().lower()
    if key in SOURCE_ALIASES:
        return SOURCE_ALIASES[key]
    if contains_any(text, ("家里老人", "奶奶说", "爷爷说", "长辈说", "家里说")):
        return "family_oral"
    if contains_any(text, ("本地", "村里", "地方", "江南", "闽南", "岭南", "东北", "川西")):
        return "regional_oral"
    if contains_any(text, ("寺", "庙", "道观", "法师", "僧人", "宗教")):
        return "religious_context"
    if contains_any(text, ("书里", "论文", "地方志", "作者", "出版社", "页")):
        return "published_reference"
    if contains_any(text, ("网上", "短视频", "帖子", "公众号", "小红书", "抖音")):
        return "internet_claim"
    if contains_any(text, ("课程", "商家", "套餐", "购买", "开运物")):
        return "commercial_claim"
    if contains_any(text, ("我自己习惯", "个人觉得", "我喜欢")):
        return "personal_preference"
    return "unknown"


def infer_custom_name(text: str, explicit: object) -> str:
    value = str(explicit or "").strip()
    if value:
        return value
    for hint, name in CUSTOM_HINTS.items():
        if hint in text:
            return name
    return ""


def normalize_evidence(raw: object) -> list[str]:
    if raw is None or raw == "":
        return []
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    return [part.strip() for part in str(raw).split(";") if part.strip()]


def normalize_usage(raw: object) -> str:
    value = str(raw or "").strip()
    aliases = {
        "文化学习": "cultural_learning",
        "家庭沟通": "family_communication",
        "活动安排": "event_planning",
        "写作": "writing",
        "安定自己": "self_soothing",
        "来源审计": "source_audit",
    }
    value = aliases.get(value, value)
    return value if value in USAGE_CONTEXTS else "cultural_learning"


def detect_risk_flags(text: str, source_type: str) -> list[str]:
    flags = [name for name, patterns in RISK_PATTERNS.items() if contains_any(text, patterns)]
    if source_type == "commercial_claim" and "commercial_interest" not in flags:
        flags.append("commercial_interest")
    return flags


def missing_fields(payload: dict[str, Any], source_type: str, custom_name: str, evidence_items: list[str]) -> list[str]:
    missing = []
    region = str(payload.get("region", "")).strip()
    community = str(payload.get("community", "")).strip()
    label = str(payload.get("informant_or_source_label", payload.get("source_label", ""))).strip()
    date_or_generation = str(payload.get("source_date_or_generation", payload.get("date_or_generation", ""))).strip()

    if not custom_name:
        missing.append("custom_name")
    if source_type == "unknown":
        missing.append("source_type")
    if source_type in {"family_oral", "regional_oral", "religious_context"} and not region:
        missing.append("region")
    if source_type in {"regional_oral", "religious_context"} and not community:
        missing.append("community_or_lineage")
    if source_type in {"family_oral", "regional_oral", "religious_context", "published_reference", "internet_claim", "commercial_claim"} and not label:
        missing.append("informant_or_source_label")
    if source_type in {"family_oral", "regional_oral"} and not date_or_generation:
        missing.append("source_date_or_generation")
    if source_type in {"published_reference", "internet_claim", "commercial_claim"} and not evidence_items:
        missing.append("evidence_items")
    return missing


def build_questions(missing: list[str], source_type: str) -> list[str]:
    questions = []
    if "custom_name" in missing:
        questions.append("这个说法具体对应哪个民俗条目或禁忌名称？")
    if "source_type" in missing:
        questions.append("它来自家人口述、地方口述、宗教语境、公开文献、网络说法、商业课程还是个人习惯？")
    if "region" in missing:
        questions.append("这个说法对应哪个地区、家庭迁徙背景或宗教地点？")
    if "community_or_lineage" in missing:
        questions.append("它属于哪个社区、村镇、庙观、宗教支派或人群语境？")
    if "informant_or_source_label" in missing:
        questions.append("能否给来源标签，例如“外婆口述”“某地地方志”“某寺公告”或“某平台帖子”？")
    if "source_date_or_generation" in missing:
        questions.append("大概是哪一代人口述，或是哪一年/哪段时期听到的？")
    if "evidence_items" in missing:
        questions.append("是否有书名、作者、页码、链接、截图说明或可复核出处？")
    if not questions and source_type in {"internet_claim", "commercial_claim"}:
        questions.append("这个来源有没有独立出处，还是只是一条网络/营销说法？")
    return questions


def record(payload: dict[str, Any]) -> dict[str, Any]:
    claim_text = str(payload.get("claim_text", payload.get("request_text", payload.get("source_text", "")))).strip()
    if not claim_text:
        raise ValueError("claim_text, request_text, or source_text is required")

    source_type = normalize_source_type(payload.get("source_type"), claim_text)
    custom_name = infer_custom_name(claim_text, payload.get("custom_name", payload.get("custom", "")))
    evidence_items = normalize_evidence(payload.get("evidence_items", payload.get("evidence", [])))
    usage_context = normalize_usage(payload.get("usage_context", payload.get("goal", "")))
    risk_flags = detect_risk_flags(claim_text, source_type)
    missing = missing_fields(payload, source_type, custom_name, evidence_items)

    can_use_as_context = "dangerous_action" not in risk_flags and "professional_replacement" not in risk_flags
    can_treat_as_tradition = (
        source_type in {"family_oral", "regional_oral", "religious_context", "published_reference"}
        and "source_type" not in missing
        and source_type != "commercial_claim"
        and source_type != "internet_claim"
    )
    if source_type in {"internet_claim", "commercial_claim", "unknown"}:
        can_treat_as_tradition = False
    if "supernatural_certainty" in risk_flags or "universal_authority_claim" in risk_flags:
        can_treat_as_tradition = False

    authority_warnings = [
        "来源记录只说明“这个说法从哪里来”，不证明鬼神、冲撞、犯忌灾祸或全国通用性。",
        "地方、家庭、宗教、文献、网络和商业来源必须分层标注，不互相冒充。",
    ]
    if source_type in {"internet_claim", "commercial_claim", "unknown"}:
        authority_warnings.append("网络、商业或未知来源只能作为待核查材料，不能直接写成传统民俗。")
    if risk_flags:
        authority_warnings.append("含危险动作、专业替代、结果承诺或绝对权威时，先转安全边界，不输出执行步骤。")

    source_record = {
        "custom_name": custom_name or "未命名民俗说法",
        "claim_summary": claim_text,
        "source_type": source_type,
        "region": str(payload.get("region", "")).strip(),
        "community": str(payload.get("community", "")).strip(),
        "informant_or_source_label": str(payload.get("informant_or_source_label", payload.get("source_label", ""))).strip(),
        "source_date_or_generation": str(payload.get("source_date_or_generation", payload.get("date_or_generation", ""))).strip(),
        "usage_context": usage_context,
        "evidence_items": evidence_items,
        "status": "usable_context" if can_use_as_context else "safety_review_needed",
    }

    return {
        "tool": "folk_source_recorder",
        "system": "chinese_folk_custom",
        "claim_text": claim_text,
        "custom_name": custom_name,
        "source_type": source_type,
        "source_reliability": SOURCE_RELIABILITY[source_type],
        "usage_context": usage_context,
        "risk_flags": risk_flags,
        "missing_fields": missing,
        "can_use_as_context": can_use_as_context,
        "can_treat_as_tradition": can_treat_as_tradition,
        "source_record": source_record,
        "recommended_framing": [
            "把该说法写成有来源边界的文化材料，而不是事实证明或必须执行的规则。",
            "说明地区、家庭、宗教或文本语境；缺失字段用“未提供/待核查”。",
            "网络和商业说法只做待核查引用，不替用户背书其传统性或效果。",
            "若涉及安全、孕期、疾病、消防、交通或法律，现实支持优先。",
        ],
        "questions_to_ask": build_questions(missing, source_type),
        "authority_warnings": authority_warnings,
        "next_steps": [
            "ask_missing_source_fields",
            "lookup_related_custom_with_folk_custom_lookup_if_needed",
            "run_folk_taboo_reframer_if_fear_or_disaster_claims_appear",
            "route_dangerous_ritual_parts_to_ritual_safety_tools",
            "lint_final_output_with_mystic_output_lint",
        ],
        "limits": [
            "不把来源记录等同于学术证明、宗教权威或地方共识。",
            "不确认鬼神、诅咒、冲撞、犯忌必灾、开运保证或治疗效果。",
            "不输出明火密闭燃烧、摄入、刀具、放血、控制他人或专业替代步骤。",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["claim_text"] = args.text
    if args.custom_name:
        payload["custom_name"] = args.custom_name
    if args.source_type:
        payload["source_type"] = args.source_type
    if args.region:
        payload["region"] = args.region
    if args.community:
        payload["community"] = args.community
    if args.source_label:
        payload["informant_or_source_label"] = args.source_label
    if args.source_date:
        payload["source_date_or_generation"] = args.source_date
    if args.usage_context:
        payload["usage_context"] = args.usage_context
    if args.evidence:
        payload["evidence_items"] = args.evidence
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"claim_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Folk-custom source claim text.")
    parser.add_argument("--custom-name", help="Optional canonical custom or taboo name.")
    parser.add_argument("--source-type", help="family_oral, regional_oral, religious_context, published_reference, internet_claim, commercial_claim, personal_preference, unknown.")
    parser.add_argument("--region", help="Region or family migration context.")
    parser.add_argument("--community", help="Community, lineage, village, temple, or audience context.")
    parser.add_argument("--source-label", help="Informant or source label.")
    parser.add_argument("--source-date", help="Date, generation, or period when source was recorded.")
    parser.add_argument("--usage-context", help="cultural_learning, family_communication, event_planning, writing, self_soothing, source_audit.")
    parser.add_argument("--evidence", action="append", help="Repeatable evidence item such as title, URL, page, or screenshot note.")
    parser.add_argument("--json", help="JSON input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = record(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
