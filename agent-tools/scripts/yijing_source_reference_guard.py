#!/usr/bin/env python3
"""Guard and classify Yijing classical text and commentary sources."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SOURCE_TYPES = {
    "jingwen": {
        "label": "经文/卦辞爻辞",
        "source_level": "classical_primary",
        "can_quote_short": True,
        "use_scope": "可作为原典文本层引用，但需短引、标注卦/爻位置，并与现代解释分层。",
        "required_attribution": ["卦名或卦号", "爻位或卦辞", "版本/出处"],
    },
    "shiyi": {
        "label": "十翼/传文",
        "source_level": "classical_commentary",
        "can_quote_short": True,
        "use_scope": "可作为传统解释层引用，需说明属于传文/解释，不等同卦爻原文。",
        "required_attribution": ["篇名", "对应卦爻", "版本/出处"],
    },
    "wangbi": {
        "label": "王弼注",
        "source_level": "historical_commentary",
        "can_quote_short": True,
        "use_scope": "可作为魏晋义理注疏参考，需说明是某家解释，不冒充唯一正统。",
        "required_attribution": ["注家", "对应卦爻", "版本/出处"],
    },
    "chengzhu": {
        "label": "程朱/宋明理学注疏",
        "source_level": "historical_commentary",
        "can_quote_short": True,
        "use_scope": "可作为宋明义理解释参考，需与象数、现代咨询语言分开。",
        "required_attribution": ["注家或书名", "对应卦爻", "版本/出处"],
    },
    "modern_translation": {
        "label": "现代译注/白话转述",
        "source_level": "modern_secondary",
        "can_quote_short": False,
        "use_scope": "可概括其解释方向，不宜大段照搬；需标注为现代译注或二手解释。",
        "required_attribution": ["作者/书名或来源", "出版/网页信息", "对应卦爻"],
    },
    "internet_claim": {
        "label": "网络断语/短视频说法",
        "source_level": "unverified_claim",
        "can_quote_short": False,
        "use_scope": "只能作为待辨析说法，不作为易经原典或可靠注疏依据。",
        "required_attribution": ["平台或来源描述", "是否可追溯原文", "对应卦爻是否明确"],
    },
    "personal_lineage": {
        "label": "师承/个人经验说法",
        "source_level": "lineage_or_personal_claim",
        "can_quote_short": False,
        "use_scope": "只能标注为某师承或个人经验，不升格为通行原典结论。",
        "required_attribution": ["传承/讲述者", "记录时间", "适用语境"],
    },
}

SOURCE_ALIASES = {
    "原文": "jingwen",
    "经文": "jingwen",
    "卦辞": "jingwen",
    "爻辞": "jingwen",
    "十翼": "shiyi",
    "彖传": "shiyi",
    "象传": "shiyi",
    "系辞": "shiyi",
    "王弼": "wangbi",
    "程朱": "chengzhu",
    "程传": "chengzhu",
    "朱熹": "chengzhu",
    "现代译注": "modern_translation",
    "白话": "modern_translation",
    "网络": "internet_claim",
    "短视频": "internet_claim",
    "师承": "personal_lineage",
    "个人经验": "personal_lineage",
}

RISK_PATTERNS = {
    "deterministic_disaster": ["必有灾", "必有大灾", "大凶", "必死", "血光", "家破", "一定出事"],
    "wealth_promise": ["必发财", "保证发财", "稳赚", "暴富", "财运大开"],
    "medical_claim": ["必病", "会得病", "不用看医生", "停药", "治病"],
    "coercion": ["控制他", "让他回来", "强迫复合", "咒"],
    "exclusive_authority": ["唯一正解", "只有这一派对", "绝对正统", "不用看上下文"],
}


def normalize_source_type(value: str) -> str:
    raw = value.strip()
    if not raw:
        return "unknown"
    if raw in SOURCE_TYPES:
        return raw
    for alias, canonical in SOURCE_ALIASES.items():
        if alias.lower() in raw.lower():
            return canonical
    return "unknown"


def detect_source_type(text: str, explicit: str = "") -> str:
    normalized = normalize_source_type(explicit)
    if normalized != "unknown":
        return normalized
    for alias, canonical in SOURCE_ALIASES.items():
        if alias.lower() in text.lower():
            return canonical
    return "unknown"


def risk_flags(text: str) -> list[str]:
    return [flag for flag, patterns in RISK_PATTERNS.items() if any(pattern in text for pattern in patterns)]


def quote_policy(text: str, source_type: str) -> dict[str, Any]:
    metadata = SOURCE_TYPES.get(source_type)
    word_count = len(text.strip())
    if not metadata:
        return {
            "can_quote": False,
            "max_quote_chars": 0,
            "policy": "来源类型不明；不要直接引用，只能先要求来源或做概括性辨析。",
        }
    if metadata["can_quote_short"]:
        return {
            "can_quote": word_count <= 80,
            "max_quote_chars": 80,
            "policy": "可短引原典/注疏片段；超过 80 个汉字时应摘短句并改用概括。",
        }
    return {
        "can_quote": False,
        "max_quote_chars": 0,
        "policy": "现代译注、网络说法或个人经验不直接照搬；用概括并标注来源层级。",
    }


def safe_reframe_for(flags: list[str], source_type: str) -> list[str]:
    reframes: list[str] = []
    if "deterministic_disaster" in flags:
        reframes.append("把灾祸断语改成风险提醒和现实检查问题。")
    if "wealth_promise" in flags:
        reframes.append("把发财承诺改成资源、决策和预算层面的反思。")
    if "medical_claim" in flags:
        reframes.append("医疗相关内容必须转向专业医疗支持，卦爻只可做情绪整理。")
    if "coercion" in flags:
        reframes.append("操控他人的说法必须改为自我边界和尊重对方意愿。")
    if "exclusive_authority" in flags:
        reframes.append("把唯一正统断言改成某来源/某注家的解释视角。")
    if source_type == "unknown":
        reframes.append("先要求补充来源类型、出处、对应卦爻和上下文。")
    return reframes or ["按来源层级标注：原典文本、传统注疏、现代译注、网络说法或个人经验。"]


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("source_text", payload.get("text", payload.get("query", "")))).strip()
    if not text:
        raise ValueError("source_text, text, or query is required")
    source_type = detect_source_type(text, str(payload.get("source_type", "")))
    metadata = SOURCE_TYPES.get(source_type, {
        "label": "未知来源",
        "source_level": "unknown",
        "can_quote_short": False,
        "use_scope": "来源不明时不能当作易经原典、注疏或可靠译注使用。",
        "required_attribution": ["来源类型", "出处", "对应卦爻", "上下文"],
    })
    flags = risk_flags(text)
    quote = quote_policy(text, source_type)
    can_use_as_reference = source_type != "unknown" and not any(
        flag in {"deterministic_disaster", "wealth_promise", "medical_claim", "coercion"} for flag in flags
    )
    return {
        "tool": "yijing_source_reference_guard",
        "source_type": source_type,
        "source_label": metadata["label"],
        "source_level": metadata["source_level"],
        "can_use_as_reference": can_use_as_reference,
        "risk_flags": flags,
        "quote_policy": quote,
        "use_scope": metadata["use_scope"],
        "required_attribution": metadata["required_attribution"],
        "safe_reframes": safe_reframe_for(flags, source_type),
        "citation_template": "《周易》<卦名><爻位/卦辞>；<注家/篇名/译注>；<版本或来源>；仅作象征解释。",
        "limits": [
            "Do not present modern translations, internet claims, or personal lineage statements as original Yijing text.",
            "Do not use Yijing sources to make deterministic disaster, illness, wealth, marriage, or legal/financial claims.",
            "Keep classical quotations short and separate original text, commentary, translation, and modern counseling language.",
        ],
        "next_steps": [
            "verify_hexagram_and_line_context",
            "separate_original_commentary_translation_and_advice",
            "run_mystic_output_lint",
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
        payload["source_text"] = args.text
    if args.source_type:
        payload["source_type"] = args.source_type
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"source_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Yijing source text, quote, or claim.")
    parser.add_argument("--source-type", help="jingwen/shiyi/wangbi/chengzhu/modern_translation/internet_claim/personal_lineage.")
    parser.add_argument("--json", help="JSON input with source_text and optional source_type.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
