#!/usr/bin/env python3
"""Score brand-name candidates for scenario fit without legal or fate claims."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


DIMENSIONS = ["memorability", "pronunciation", "category_fit", "audience_fit", "searchability", "risk_control"]

TONE_KEYWORDS = {
    "温和": {"安", "宁", "予", "禾", "清"},
    "清爽": {"清", "朗", "禾", "沐"},
    "专业": {"知", "言", "一", "清", "正"},
    "年轻": {"星", "沐", "一", "然", "小"},
    "高端": {"清", "朗", "辰", "景", "知"},
    "东方": {"禾", "辰", "清", "安", "山"},
    "科技": {"星", "知", "一", "云", "智"},
}

CATEGORY_HINTS = {
    "茶饮": {"清", "沐", "禾", "茗", "茶"},
    "餐饮": {"禾", "安", "味", "食", "小"},
    "服饰": {"清", "朗", "予", "然", "景"},
    "教育": {"知", "书", "言", "一", "朗"},
    "咨询": {"知", "言", "清", "正", "一"},
    "科技": {"星", "云", "智", "一", "知"},
    "疗愈": {"安", "宁", "沐", "清", "予"},
    "文创": {"书", "言", "景", "予", "星"},
}

HIGH_RISK_TERMS = {
    "第一": "绝对化宣传风险",
    "国家": "公共权威联想风险",
    "官方": "公共权威联想风险",
    "包治": "医疗功效承诺风险",
    "治愈": "医疗功效承诺风险",
    "发财": "财富承诺风险",
    "暴富": "财富承诺风险",
    "必胜": "结果保证风险",
    "无敌": "绝对化宣传风险",
}

RARE_OR_SEARCH_COSTLY = {
    "龘": "输入和搜索成本极高",
    "靐": "输入和搜索成本极高",
    "燚": "识别成本较高",
    "赟": "误读和输入成本较高",
    "翀": "误读和输入成本较高",
}

REGISTRATION_CLAIMS = ["一定可注册", "可注册", "不会侵权", "包过", "商标一定", "域名一定", "全网唯一"]
FATE_CLAIMS = ["旺财", "招财", "转运", "改运", "必火", "必爆"]
PROFESSIONAL_DOMAINS = ["医疗", "药", "理财", "投资", "证券", "保险"]


def normalize_candidates(raw: object, request_text: str = "") -> list[str]:
    if isinstance(raw, list):
        candidates = [str(item.get("name", "") if isinstance(item, dict) else item).strip() for item in raw]
    elif isinstance(raw, str) and raw.strip():
        candidates = [part.strip() for part in re.split(r"[、,，/| ]+", raw) if part.strip()]
    else:
        candidates = extract_candidates(request_text)
    seen: set[str] = set()
    unique = []
    for name in candidates:
        if name and name not in seen:
            seen.add(name)
            unique.append(name)
    return unique[:10]


def extract_candidates(text: str) -> list[str]:
    results: list[str] = []
    for segment in re.split(r"[；;。！？\n]", text):
        if not any(key in segment for key in ["品牌", "店名", "商号", "名字", "比较", "叫"]):
            continue
        for token in re.split(r"[、,，/|和还是与 ]+", segment):
            token = re.sub(r"^(品牌名|品牌|店名|商号|名字|比较|叫|看看|用)", "", token).strip("：:")
            token = re.sub(r"(哪个好|哪个更好|怎么样|好不好|吗)$", "", token)
            if any(word in token for word in ["帮我", "想个", "取个", "品牌名", "名字"]):
                continue
            if re.fullmatch(r"[\u4e00-\u9fffA-Za-z0-9]{2,12}", token):
                results.append(token)
    return results


def normalize_list(raw: object) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    if isinstance(raw, str) and raw.strip():
        return [part.strip() for part in re.split(r"[、,，/| ]+", raw) if part.strip()]
    return []


def detect_risks(text: str, category: str, candidates: list[str]) -> list[str]:
    joined = text + "".join(candidates) + category
    risks: list[str] = []
    if any(claim in joined for claim in REGISTRATION_CLAIMS):
        risks.append("professional_registration_claim")
    if any(claim in joined for claim in FATE_CLAIMS):
        risks.append("deterministic_fate_or_virality_claim")
    if any(term in joined for term in PROFESSIONAL_DOMAINS) and any(term in joined for term in ["功效", "治疗", "收益", "稳赚"]):
        risks.append("regulated_industry_claim")
    return risks


def score_candidate(name: str, payload: dict[str, Any], category: str, audience: str, tones: list[str], channels: list[str]) -> dict[str, Any]:
    scores = {dimension: 3 for dimension in DIMENSIONS}
    strengths: list[str] = []
    cautions: list[str] = []
    checks: list[str] = []

    length = len(name)
    if 2 <= length <= 4:
        scores["memorability"] += 1
        scores["pronunciation"] += 1
        strengths.append("长度适合口头传播和招牌展示")
    elif length > 6:
        scores["memorability"] -= 1
        scores["pronunciation"] -= 1
        cautions.append("名称偏长，需准备简称或英文/拼音展示策略")

    if len(set(name)) == length:
        scores["searchability"] += 1
    else:
        cautions.append("重复字形可能降低搜索区分度，需要检索同名密度")

    category_chars = CATEGORY_HINTS.get(category, set())
    if category_chars and set(name) & category_chars:
        scores["category_fit"] += 1
        strengths.append(f"含有与「{category}」场景相近的字义线索")
    elif category:
        checks.append(f"确认「{name}」是否能让目标用户快速联想到 {category}")

    matched_tones = [tone for tone in tones if set(name) & TONE_KEYWORDS.get(tone, set())]
    if matched_tones:
        scores["audience_fit"] += 1
        strengths.append(f"可支持的语气：{', '.join(matched_tones)}")
    elif tones:
        checks.append("用户指定语气与字面联想不强，需要通过视觉和文案补足")

    if audience:
        scores["audience_fit"] += 1
        checks.append(f"用目标受众「{audience}」做 5 秒记忆和误读测试")

    if any(channel in channels for channel in ["小红书", "抖音", "搜索", "电商", "域名"]):
        scores["searchability"] += 1
        checks.append("做平台搜索、账号名、域名和竞品同名检查")
    if any(channel in channels for channel in ["门头", "包装", "招牌"]):
        scores["memorability"] += 1
        checks.append("检查门头、包装和缩略图里的字形清晰度")

    for term, reason in HIGH_RISK_TERMS.items():
        if term in name:
            scores["risk_control"] -= 2
            cautions.append(f"{term}：{reason}")
    for char, reason in RARE_OR_SEARCH_COSTLY.items():
        if char in name:
            scores["searchability"] -= 2
            scores["pronunciation"] -= 1
            cautions.append(f"{char}：{reason}")

    if re.fullmatch(r"[A-Za-z0-9]+", name):
        checks.append("英文/数字名需额外检查读音、拼写和跨平台可搜性")
    if not strengths:
        strengths.append("未发现明显硬伤，可继续用场景测试验证")
    if not cautions:
        cautions.append("未发现明显高风险词；仍需做商标、域名、平台和竞品检索")

    bounded = {key: max(1, min(5, value)) for key, value in scores.items()}
    total = round(sum(bounded.values()) / len(DIMENSIONS), 2)
    return {
        "name": name,
        "dimension_scores": bounded,
        "overall_score": total,
        "strengths": strengths[:5],
        "cautions": cautions[:5],
        "external_checks": checks[:6],
    }


def score(payload: dict[str, Any]) -> dict[str, Any]:
    request_text = str(payload.get("request_text", "")).strip()
    category = str(payload.get("category", payload.get("industry", ""))).strip()
    audience = str(payload.get("audience", "")).strip()
    tones = normalize_list(payload.get("tone", payload.get("tones", [])))
    channels = normalize_list(payload.get("channels", []))
    candidates = normalize_candidates(payload.get("candidates", ""), request_text)
    risk_flags = detect_risks(request_text, category, candidates)

    missing_fields: list[str] = []
    if not candidates:
        missing_fields.append("candidates")
    if not category:
        missing_fields.append("category")
    if not audience:
        missing_fields.append("audience")
    if not channels:
        missing_fields.append("channels")

    evaluations = [score_candidate(name, payload, category, audience, tones, channels) for name in candidates]
    ranked = sorted(evaluations, key=lambda item: (-item["overall_score"], item["name"]))
    can_score = bool(candidates) and not missing_fields and "regulated_industry_claim" not in risk_flags

    warnings = [
        "品牌名评分是传播和场景粗筛，不是商标、域名、工商登记、侵权或商业成功结论。",
        "五行、吉凶、招财、转运等说法不得作为品牌名可用性的证明。",
    ]
    if "professional_registration_claim" in risk_flags:
        warnings.append("已检测到可注册/不侵权承诺类表述，必须改为外部检索待确认。")
    if "deterministic_fate_or_virality_claim" in risk_flags:
        warnings.append("已检测到必火、招财或转运类表述，只能降级为营销愿望或文化联想。")
    if "regulated_industry_claim" in risk_flags:
        warnings.append("医疗、金融等受监管行业的功效或收益表述需先暂停，并转专业合规审查。")

    return {
        "tool": "naming_brand_scenario_scorer",
        "system": "chinese_naming",
        "request_text": request_text,
        "category": category,
        "audience": audience,
        "tones": tones,
        "channels": channels,
        "candidate_count": len(candidates),
        "dimensions": DIMENSIONS,
        "risk_flags": risk_flags,
        "missing_fields": missing_fields,
        "can_score_brand_names": can_score,
        "evaluations": evaluations,
        "ranked_candidates": [item["name"] for item in ranked],
        "scenario_summary": build_summary(ranked, missing_fields, risk_flags),
        "warnings": warnings,
        "next_steps": [
            "confirm_category_audience_tone_and_channels",
            "review_ranked_candidate_scores",
            "run_trademark_domain_platform_and_competitor_searches_outside_this_tool",
            "test_pronunciation_memory_and_visual_display_with_target_users",
            "lint_final_output_with_mystic_output_lint",
        ],
        "limits": [
            "不承诺商标可注册、域名可用、平台账号可用、不会侵权或商业成功。",
            "不把品牌名写成招财、转运、必火、疗效或收益保证。",
            "受监管行业、药品保健、金融投资等名称需另做专业合规审查。",
        ],
    }


def build_summary(ranked: list[dict[str, Any]], missing_fields: list[str], risk_flags: list[str]) -> str:
    if not ranked:
        return "缺少品牌名候选，先补候选、品类、受众和传播渠道。"
    top = ranked[0]
    missing = f"；仍需补充 {', '.join(missing_fields)}" if missing_fields else ""
    risk = "；先处理注册承诺、受监管行业或必火招财等风险表述" if risk_flags else ""
    return f"当前场景粗筛优先候选为「{top['name']}」，优势：{'；'.join(top['strengths'][:2])}；谨慎点：{'；'.join(top['cautions'][:2])}{missing}{risk}。"


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["request_text"] = args.text
    if args.candidates:
        payload["candidates"] = args.candidates
    if args.category:
        payload["category"] = args.category
    if args.audience:
        payload["audience"] = args.audience
    if args.tone:
        payload["tone"] = args.tone
    if args.channels:
        payload["channels"] = args.channels
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Brand naming request text.")
    parser.add_argument("--candidates", help="Candidate brand names split by 、, comma, slash or space.")
    parser.add_argument("--category", help="Brand category or industry.")
    parser.add_argument("--audience", help="Target audience.")
    parser.add_argument("--tone", help="Desired tone words.")
    parser.add_argument("--channels", help="Primary channels, e.g. 小红书、门头、域名.")
    parser.add_argument("--json", help="JSON input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = score(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
