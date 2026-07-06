#!/usr/bin/env python3
"""Compare Chinese name candidates as safe cultural and usage artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


DIMENSIONS = ["meaning", "sound", "form", "culture", "usage"]

POSITIVE_CHARS = {
    "安": ("安定、平和、可亲", "earth"),
    "宁": ("安宁、从容、稳定", "earth"),
    "清": ("清澈、清朗、边界感", "water"),
    "朗": ("明朗、开阔、表达", "fire"),
    "沐": ("润泽、更新、亲和", "water"),
    "言": ("表达、沟通、文气", "metal"),
    "知": ("理解、学习、清醒", "water"),
    "禾": ("生长、收获、朴素", "wood"),
    "林": ("成长、连接、自然感", "wood"),
    "予": ("给予、开放、温和", "earth"),
    "一": ("简洁、起点、专注", "water"),
    "辰": ("时间感、展开、传统意象", "earth"),
    "星": ("可见度、希望、辨识", "fire"),
    "然": ("自然、接纳、完整感", "fire"),
    "景": ("视野、明亮、环境感", "fire"),
    "书": ("学习、文本、秩序", "wood"),
    "远": ("开阔、长期感、行旅", "water"),
}

CAUTION_CHARS = {
    "病": "疾病负面联想",
    "死": "死亡负面联想",
    "穷": "贫困负面联想",
    "灾": "灾祸负面联想",
    "凶": "凶险负面联想",
    "煞": "恐吓式民俗联想",
    "破": "破损或破败联想",
    "孤": "孤立联想",
    "怨": "怨怼联想",
}

RARE_OR_COSTLY_CHARS = {
    "龘": "极高识别和输入成本",
    "靐": "极高识别和输入成本",
    "燚": "较高识别和书写成本",
    "赟": "较易误读，证件和输入需确认",
    "翀": "较易误读，需确认长期使用舒适度",
    "垚": "较易误读或被问询",
    "淼": "辨识度高但书写和重名需确认",
}

FATALISTIC_PATTERNS = [
    "必发财",
    "一定发财",
    "旺财",
    "旺夫",
    "克父母",
    "克夫",
    "招灾",
    "影响寿命",
    "婚姻不顺",
    "命不好",
    "改名转运",
]

PROFESSIONAL_PATTERNS = ["可注册", "商标一定", "不会侵权", "包过", "登记一定", "上户口一定"]


def normalize_name_type(raw: object) -> str:
    text = str(raw or "").strip()
    aliases = {
        "大名": "formal_name",
        "正式名": "formal_name",
        "宝宝名": "formal_name",
        "小名": "nickname",
        "乳名": "nickname",
        "艺名": "stage_name",
        "笔名": "pen_name",
        "网名": "stage_name",
        "品牌名": "brand_name",
        "品牌": "brand_name",
    }
    if text in {"formal_name", "nickname", "stage_name", "pen_name", "brand_name", "general"}:
        return text
    return aliases.get(text, "general")


def normalize_candidates(raw: object, request_text: str = "") -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                name = str(item.get("name", "")).strip()
                notes = str(item.get("notes", "")).strip()
            else:
                name = str(item).strip()
                notes = ""
            if name:
                candidates.append({"name": name, "notes": notes})
    elif isinstance(raw, str) and raw.strip():
        candidates = [{"name": part.strip(), "notes": ""} for part in re.split(r"[、,，/| ]+", raw) if part.strip()]

    if not candidates and request_text:
        extracted = extract_candidates_from_text(request_text)
        candidates = [{"name": name, "notes": ""} for name in extracted]

    seen: set[str] = set()
    unique = []
    for item in candidates:
        if item["name"] not in seen:
            seen.add(item["name"])
            unique.append(item)
    return unique


def extract_candidates_from_text(text: str) -> list[str]:
    matches: list[str] = []
    for segment in re.split(r"[；;。！？\n]", text):
        if not any(key in segment for key in ["候选", "比较", "看看", "叫", "名字", "取名"]):
            continue
        for token in re.split(r"[、,，/|和还是与 ]+", segment):
            token = re.sub(r"^(候选|比较|看看|名字|叫|取名|宝宝|品牌|大名|小名|为|给)", "", token).strip("：:")
            token = re.sub(r"(好不好|怎么样|哪个更好|更好|吗)$", "", token)
            if re.fullmatch(r"[\u4e00-\u9fff]{2,6}", token):
                matches.append(token)
    return matches[:8]


def detect_risks(text: str, payload: dict[str, Any], name_type: str) -> list[str]:
    risk_flags: list[str] = []
    if any(pattern in text for pattern in FATALISTIC_PATTERNS):
        risk_flags.append("deterministic_fate_claim")
    if bool(payload.get("subject_is_minor")) and any(pattern in text for pattern in ["性格一定", "将来一定", "必须成", "天生"]):
        risk_flags.append("minor_labeling")
    if name_type == "brand_name" and any(pattern in text for pattern in PROFESSIONAL_PATTERNS):
        risk_flags.append("professional_registration_claim")
    if str(payload.get("relationship_to_subject", "")).strip() == "third_party_without_consent":
        risk_flags.append("third_party_privacy")
    return risk_flags


def score_candidate(candidate: dict[str, Any], payload: dict[str, Any], name_type: str) -> dict[str, Any]:
    name = candidate["name"]
    surname = str(payload.get("surname", "")).strip()
    desired_elements = set(payload.get("desired_elements") or [])
    avoid_characters = set(str(payload.get("avoid_characters") or ""))
    priorities = [str(item) for item in (payload.get("priorities") or [])]
    full_name = f"{surname}{name}" if surname and not name.startswith(surname) and name_type != "brand_name" else name

    scores = {dimension: 3 for dimension in DIMENSIONS}
    strengths: list[str] = []
    cautions: list[str] = []
    adjustments: list[str] = []
    element_hints: list[str] = []

    for char in name:
        if char in POSITIVE_CHARS:
            meaning, element = POSITIVE_CHARS[char]
            strengths.append(f"{char}：{meaning}")
            element_hints.append(element)
        if char in CAUTION_CHARS:
            scores["meaning"] -= 2
            scores["culture"] -= 2
            cautions.append(f"{char}：{CAUTION_CHARS[char]}")
        if char in RARE_OR_COSTLY_CHARS:
            scores["form"] -= 1
            scores["usage"] -= 1
            cautions.append(f"{char}：{RARE_OR_COSTLY_CHARS[char]}")
        if char in avoid_characters:
            scores["culture"] -= 2
            cautions.append(f"{char}：命中用户明确避开的用字")

    if strengths:
        scores["meaning"] += 1
    if len(name) in {2, 3}:
        scores["sound"] += 1
        scores["usage"] += 1
    elif len(name) > 4:
        scores["sound"] -= 1
        scores["usage"] -= 1
        adjustments.append("若长期口头使用，考虑缩短或准备稳定简称。")

    unique_chars = len(set(full_name))
    if unique_chars == len(full_name):
        scores["form"] += 1
    else:
        scores["form"] -= 1
        cautions.append("全名存在重复字形，需确认视觉节奏是否符合偏好。")

    if desired_elements:
        matched = sorted(desired_elements & set(element_hints))
        if matched:
            scores["culture"] += 1
            strengths.append(f"五行意象可作为民俗参考：{', '.join(matched)}")
        else:
            adjustments.append("若用户坚持五行民俗偏好，可另备含对应意象的候选，但不能写成补命。")

    if name_type == "brand_name":
        if len(name) <= 4:
            scores["usage"] += 1
        adjustments.append("品牌名需另做商标、域名、平台账号和竞品搜索。")
    elif name_type == "formal_name":
        adjustments.append("正式名建议补做方言读音、证件系统和常见误读检查。")

    if "谐音" in priorities or "sound" in priorities:
        adjustments.append("按主要方言和普通话各读三遍，记录可能被开玩笑的读法。")
    if "字义" in priorities or "meaning" in priorities:
        adjustments.append("把每个字的本义、引申义和家庭期待分开写，避免给孩子贴固定标签。")

    bounded_scores = {key: max(1, min(5, value)) for key, value in scores.items()}
    total = round(sum(bounded_scores.values()) / len(DIMENSIONS), 2)
    if not strengths:
        strengths.append("未发现明显负面字义，可继续按偏好和使用场景细化。")
    if not cautions:
        cautions.append("未发现明显硬风险；仍需做方言、重名和现实使用复核。")
    if not adjustments:
        adjustments.append("保留为候选，下一步按用户最看重维度做人工取舍。")

    return {
        "name": name,
        "full_name": full_name,
        "dimension_scores": bounded_scores,
        "overall_score": total,
        "element_hints": sorted(set(element_hints)),
        "strengths": strengths[:5],
        "cautions": cautions[:5],
        "adjustments": adjustments[:5],
    }


def compare(payload: dict[str, Any]) -> dict[str, Any]:
    request_text = str(payload.get("request_text", "")).strip()
    name_type = normalize_name_type(payload.get("name_type", payload.get("type", "")))
    candidates = normalize_candidates(payload.get("candidates", ""), request_text)
    risk_flags = detect_risks(request_text, payload, name_type)
    evaluations = [score_candidate(candidate, payload, name_type) for candidate in candidates]
    ranked = sorted(evaluations, key=lambda item: (-item["overall_score"], item["name"]))

    missing_fields: list[str] = []
    if not candidates:
        missing_fields.append("candidates")
    if name_type == "general":
        missing_fields.append("name_type")
    if not payload.get("priorities"):
        missing_fields.append("priorities")

    can_compare = bool(candidates) and "third_party_privacy" not in risk_flags
    warnings = [
        "评分是候选名的文化象征和现实使用粗筛，不是命运、健康、财富、婚恋或学业判断。",
        "五行、生肖、笔画和字形只能作为民俗参考，不得写成补命、转运或灾祸规避算法。",
    ]
    if name_type == "brand_name":
        warnings.append("品牌名必须另做商标、域名、平台账号和竞品检索，本工具不承诺可注册或可商用。")
    if "deterministic_fate_claim" in risk_flags:
        warnings.append("已将发财、旺夫、克亲属、招灾等说法降级为不可采用的宿命论请求。")
    if "minor_labeling" in risk_flags:
        warnings.append("涉及未成年人时，只能谈使用体验和家庭偏好，不能贴固定人格或人生角色标签。")

    return {
        "tool": "naming_candidate_comparator",
        "system": "chinese_naming",
        "request_text": request_text,
        "name_type": name_type,
        "candidate_count": len(candidates),
        "dimensions": DIMENSIONS,
        "risk_flags": risk_flags,
        "missing_fields": missing_fields,
        "can_compare_names": can_compare,
        "evaluations": evaluations,
        "ranked_candidates": [item["name"] for item in ranked],
        "comparison_summary": build_summary(ranked, risk_flags, missing_fields),
        "warnings": warnings,
        "next_steps": [
            "confirm_user_priorities_and_context",
            "review_top_candidate_strengths_and_cautions",
            "check_homophones_dialect_rare_characters_and_duplicates",
            "for_brand_names_run_trademark_domain_and_platform_searches_outside_this_tool",
            "lint_final_output_with_mystic_output_lint",
        ],
        "limits": [
            "不做命运保证、五行补救承诺、疾病/财富/婚恋结论或灾祸断言。",
            "不替代法律登记、商标检索、品牌调研、心理健康、医疗、财务或职业建议。",
            "真实命名还需要家庭偏好、地域读音、重名密度和长期使用反馈。",
        ],
    }


def build_summary(ranked: list[dict[str, Any]], risk_flags: list[str], missing_fields: list[str]) -> str:
    if not ranked:
        return "缺少候选名，先补候选、使用场景和主要评价维度。"
    top = ranked[0]
    caution = "；".join(top["cautions"][:2])
    risk_note = "；需先降级宿命论或隐私风险" if risk_flags else ""
    missing_note = f"；仍需补充 {', '.join(missing_fields)}" if missing_fields else ""
    return f"当前粗筛优先候选为「{top['name']}」，优势集中在：{'；'.join(top['strengths'][:2])}；谨慎点：{caution}{risk_note}{missing_note}。"


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
    if args.name_type:
        payload["name_type"] = args.name_type
    if args.surname:
        payload["surname"] = args.surname
    if args.priorities:
        payload["priorities"] = [part.strip() for part in re.split(r"[、,，/| ]+", args.priorities) if part.strip()]
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
    parser.add_argument("--text", help="Request text containing candidate names.")
    parser.add_argument("--candidates", help="Candidate names split by 、, comma, slash or space.")
    parser.add_argument("--name-type", help="formal_name, nickname, stage_name, pen_name, brand_name, or Chinese aliases.")
    parser.add_argument("--surname", help="Optional surname for formal personal names.")
    parser.add_argument("--priorities", help="Main priorities split by 、, comma, slash or space.")
    parser.add_argument("--json", help="JSON input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = compare(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
