#!/usr/bin/env python3
"""Select the consultation paradigm for a concrete mystic-agent question."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import agent_workflow_router
import knowledge_coverage_audit


TRUNKS = {
    "decision": {
        "title": "占问与决策框架",
        "domains": {
            "tarot",
            "yijing",
            "liuyao",
            "meihua",
            "qimen",
            "mingli",
            "astrology",
            "date_selection",
            "naming",
            "numerology",
            "nine_star_ki",
            "human_design",
        },
    },
    "symbolic_media": {
        "title": "随机媒介与符号读取",
        "domains": {
            "oracle_lot",
            "oracle_card",
            "cartomancy",
            "dice",
            "tasseography",
            "lenormand",
            "rune",
            "pendulum",
            "western_geomancy",
            "casting_lots",
            "scrying",
            "character_divination",
            "bibliomancy",
            "sigil",
        },
    },
    "space_environment": {
        "title": "空间、环境与居住体验",
        "domains": {
            "fengshui",
            "ritual",
            "sound_cleansing",
            "aroma",
            "herbal",
            "crystal",
            "talisman",
            "consecration",
            "lost_object",
            "dowsing",
        },
    },
    "ritual_objects": {
        "title": "仪式、象征物与护持叙事",
        "domains": {
            "spiritual_protection",
            "deity_ancestor",
            "manifestation",
            "wealth_luck",
            "relationship_luck",
            "candle",
            "incense",
            "flower",
            "color",
            "zodiac",
        },
    },
    "body_mind": {
        "title": "身体、睡眠、梦境与心理叙事",
        "domains": {
            "dream",
            "sleep_paralysis",
            "body_omen",
            "aura_chakra",
            "physiognomy",
            "spirit_message",
            "past_life",
            "psychometry",
            "pet_communication",
        },
    },
    "folk_omens": {
        "title": "民俗、时令与征兆",
        "domains": {
            "folk_custom",
            "moon_phase",
            "planetary_retrograde",
            "animal_omen",
            "sky_omen",
            "synchronicity",
        },
    },
}

PRACTICAL_DOMAINS = {
    "fengshui",
    "ritual",
    "sound_cleansing",
    "aroma",
    "herbal",
    "color",
    "naming",
    "lost_object",
    "sleep_paralysis",
    "dream",
    "body_omen",
    "pet_communication",
}
PROVENANCE_DOMAINS = {
    "yijing",
    "liuyao",
    "meihua",
    "qimen",
    "mingli",
    "astrology",
    "tarot",
    "rune",
    "lenormand",
    "oracle_lot",
    "folk_custom",
    "zodiac",
    "deity_ancestor",
    "nine_star_ki",
    "human_design",
}
MYSTICAL_BOUNDARY_DOMAINS = {
    "spirit_message",
    "past_life",
    "psychometry",
    "pendulum",
    "dowsing",
    "scrying",
    "manifestation",
    "spiritual_protection",
    "consecration",
    "wealth_luck",
    "relationship_luck",
    "ritual",
}


def domain_display_names(root: Path) -> dict[str, str]:
    audit = knowledge_coverage_audit.audit(root)
    return {item["domain"]: item["display_name"] for item in audit["domains"]}


def trunk_for_domain(domain: str) -> dict[str, str]:
    for trunk_id, trunk in TRUNKS.items():
        if domain in trunk["domains"]:
            return {"id": trunk_id, "title": trunk["title"]}
    return {"id": "unclassified", "title": "未归类"}


def question_type(route: dict[str, Any], text: str) -> str:
    domain = route["domain"]
    intent = route["intent"]
    if route["route_status"] in {"blocked_safety", "paused_for_professional_boundary"}:
        return "safety_or_professional_boundary"
    if any(word in text for word in ("来源", "历史", "发展", "是什么", "介绍", "学习")):
        return "source_and_context_learning"
    if domain in {"fengshui", "ritual", "sound_cleansing", "aroma", "herbal", "lost_object"}:
        return "practical_environment_or_search"
    if domain in {"dream", "sleep_paralysis", "body_omen", "aura_chakra"}:
        return "body_sleep_or_experience_reflection"
    if domain in TRUNKS["symbolic_media"]["domains"]:
        return "symbolic_media_reading"
    if intent in {"decision_support", "prediction"} or domain in TRUNKS["decision"]["domains"]:
        return "decision_reflection"
    if domain in TRUNKS["folk_omens"]["domains"]:
        return "cultural_omen_context"
    return "symbolic_reflection"


def paradigm_for(route: dict[str, Any], text: str) -> dict[str, str]:
    qtype = question_type(route, text)
    if qtype == "safety_or_professional_boundary":
        return {
            "id": "safety_pause",
            "title": "安全/专业边界暂停范式",
            "why": "请求触发 orange/red 风险，必须先暂停玄学流程。",
        }
    if qtype == "source_and_context_learning":
        return {
            "id": "source_context",
            "title": "来源语境与勘误范式",
            "why": "用户在问来源、历史或体系解释，优先做出处、派别和边界说明。",
        }
    if qtype == "practical_environment_or_search":
        return {
            "id": "practical_audit",
            "title": "现实观察与低风险行动范式",
            "why": "请求可落到空间、物件、搜索路线或低风险实践，适合做清单和复盘。",
        }
    if qtype == "body_sleep_or_experience_reflection":
        return {
            "id": "somatic_reflection",
            "title": "身体/睡眠体验记录范式",
            "why": "请求涉及身体、睡眠或异常体验，先记录普通诱因和红旗，再做象征反思。",
        }
    if qtype == "symbolic_media_reading":
        return {
            "id": "symbolic_media",
            "title": "媒介记录与象征反思范式",
            "why": "请求依赖牌、签、骰、图案或符物等媒介，需要先记录来源再解释。",
        }
    if qtype == "decision_reflection":
        return {
            "id": "decision_reflection",
            "title": "问题澄清与决策镜像范式",
            "why": "请求围绕选择、局势或自我理解，适合拆问题、列现实约束和复盘点。",
        }
    if qtype == "cultural_omen_context":
        return {
            "id": "cultural_omen",
            "title": "民俗语境与安全回应范式",
            "why": "请求围绕时令、征兆或民俗解释，优先做地区来源和非恐吓回应。",
        }
    return {
        "id": "symbolic_reflection",
        "title": "低风险象征反思范式",
        "why": "请求可作为象征语言处理，但不适合生成确定预言。",
    }


def evidence_track(domain: str) -> dict[str, bool]:
    return {
        "scientific_or_practical_validation": domain in PRACTICAL_DOMAINS,
        "provenance_audit": domain in PROVENANCE_DOMAINS,
        "mystical_boundary_priority": domain in MYSTICAL_BOUNDARY_DOMAINS,
        "case_validation_recommended": True,
    }


def execution_boundary(route: dict[str, Any], paradigm: dict[str, str]) -> dict[str, Any]:
    if route["route_status"] == "blocked_safety":
        mode = "blocked_safety"
        automated = ["mystic_intake_triage", "agent_workflow_router", "paradigm_selector"]
        agent_required = ["给安全支持、紧急资源或现实帮助建议"]
        human_review = True
    elif route["route_status"] == "paused_for_professional_boundary":
        mode = "pause_for_professional_boundary"
        automated = ["mystic_intake_triage", "agent_workflow_router", "paradigm_selector"]
        agent_required = ["解释专业边界", "提供低风险替代反思或现实支持路径"]
        human_review = True
    elif paradigm["id"] in {"practical_audit", "somatic_reflection"}:
        mode = "automated_scaffold_then_agent_synthesis"
        automated = ["路由", "风险分级", "资料字段记录", "清单/计划草案", "输出 lint"]
        agent_required = ["根据用户补充信息做综合解释", "把工具结果转成自然语言行动计划"]
        human_review = False
    else:
        mode = "agent_required_for_symbolic_synthesis"
        automated = ["路由", "风险分级", "媒介/盘面/来源记录", "术语查询", "输出 lint"]
        agent_required = ["选择解释层级", "连接现实约束", "避免确定预言和编造来源"]
        human_review = paradigm["id"] == "source_context"
    return {
        "automation_mode": mode,
        "automated_parts": automated,
        "agent_required_parts": agent_required,
        "human_review_recommended": human_review,
    }


def select(payload: dict[str, Any], root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    text = str(payload.get("request_text", "")).strip()
    if not text:
        raise ValueError("request_text is required")
    route_payload = {"request_text": text}
    if payload.get("requested_domain"):
        route_payload["requested_domain"] = str(payload["requested_domain"])
    route = agent_workflow_router.route(route_payload, root_path)
    names = domain_display_names(root_path)
    domain = route["domain"]
    paradigm = paradigm_for(route, text)
    trunk = trunk_for_domain(domain)
    boundary = execution_boundary(route, paradigm)
    return {
        "tool": "paradigm_selector",
        "root": str(root_path),
        "is_valid": bool(route["is_valid"]),
        "request_text": text,
        "domain": domain,
        "domain_display_name": names.get(domain, domain),
        "intent": route["intent"],
        "risk_level": route["risk_level"],
        "route_status": route["route_status"],
        "trunk": trunk,
        "question_type": question_type(route, text),
        "recommended_paradigm": paradigm,
        "execution_boundary": boundary,
        "evidence_track": evidence_track(domain),
        "context_files": {
            "skill": route.get("skill_path", ""),
            "sop": route.get("sop", []),
            "knowledge": route.get("knowledge", []),
        },
        "initial_tools": route.get("initial_tools", []),
        "limits": [
            "范式选择只决定处理框架，不直接生成玄学结论。",
            "orange/red 风险必须暂停占卜、排盘或仪式流程。",
            "自动化部分负责结构化和守门；象征综合仍需要 agent 按 SOP 执行。",
        ],
        "next_steps": next_steps(route, paradigm, boundary),
    }


def next_steps(route: dict[str, Any], paradigm: dict[str, str], boundary: dict[str, Any]) -> list[str]:
    if boundary["automation_mode"] == "blocked_safety":
        return ["stop_mystic_workflow", "offer_safety_support"]
    if boundary["automation_mode"] == "pause_for_professional_boundary":
        return ["pause_mystic_workflow", "explain_professional_boundary", "offer_low_risk_alternative"]
    return [
        "load_context_files",
        "run_initial_tools",
        f"apply_{paradigm['id']}_paradigm",
        "run_or_equivalent_mystic_output_lint",
    ]


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.text:
        payload: dict[str, Any] = {"request_text": args.text}
        if args.domain:
            payload["requested_domain"] = args.domain
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--text", help="User request text.")
    parser.add_argument("--domain", help="Optional requested domain.")
    parser.add_argument("--json", help="JSON object input.")
    args = parser.parse_args()
    try:
        result = select(load_payload(args), root=args.root)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

