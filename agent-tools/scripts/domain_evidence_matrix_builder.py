#!/usr/bin/env python3
"""Build the domain evidence matrix for scientific, provenance, mystical, and case-validation work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import knowledge_coverage_audit
import paradigm_selector


PROVENANCE_EXTENSION = {
    "oracle_card",
    "cartomancy",
    "dice",
    "date_selection",
    "tasseography",
    "casting_lots",
    "character_divination",
    "bibliomancy",
    "western_geomancy",
    "moon_phase",
    "planetary_retrograde",
    "sky_omen",
    "animal_omen",
    "flower",
    "physiognomy",
    "numerology",
    "talisman",
    "crystal",
    "candle",
    "incense",
    "sigil",
}

MYSTICAL_EXTENSION = {
    "crystal",
    "candle",
    "incense",
    "talisman",
    "sigil",
    "aura_chakra",
    "sleep_paralysis",
    "synchronicity",
}

PRACTICAL_EXTENSION = {
    "flower",
    "physiognomy",
    "aura_chakra",
}


def evidence_mode(tracks: dict[str, bool]) -> str:
    practical = tracks["scientific_or_practical_validation"]
    provenance = tracks["provenance_audit"]
    mystical = tracks["mystical_boundary_priority"]
    if practical and not mystical:
        return "scientific_or_practical"
    if provenance and not practical and not mystical:
        return "provenance_correction"
    if mystical and not practical and not provenance:
        return "mystical_boundary"
    return "mixed"


def priority_for(mode: str, tracks: dict[str, bool]) -> str:
    if tracks["scientific_or_practical_validation"]:
        return "P0"
    if mode == "provenance_correction" or tracks["provenance_audit"]:
        return "P1"
    if tracks["mystical_boundary_priority"]:
        return "P2"
    return "P1"


def mystical_intensity(tracks: dict[str, bool]) -> str:
    score = sum(
        1
        for key in ("mystical_boundary_priority", "provenance_audit", "scientific_or_practical_validation")
        if tracks[key]
    )
    if tracks["mystical_boundary_priority"] and score == 1:
        return "high"
    if tracks["mystical_boundary_priority"]:
        return "medium_high"
    if tracks["provenance_audit"] and not tracks["scientific_or_practical_validation"]:
        return "medium"
    return "low"


def case_template(mode: str, trunk_id: str) -> str:
    if mode == "scientific_or_practical":
        return "before_after_or_diary_with_scores"
    if mode == "provenance_correction":
        return "source_comparison_and_interpretation_path"
    if mode == "mystical_boundary":
        return "boundary_counterexample_and_safe_rewrite"
    if trunk_id == "body_mind":
        return "experience_diary_red_flags_and_care_action"
    if trunk_id == "space_environment":
        return "before_after_or_safety_observation"
    return "mixed_case_with_source_and_follow_up"


def next_action(mode: str, priority: str) -> str:
    if priority == "P0":
        return "add_practical_case_with_follow_up_metrics"
    if mode == "provenance_correction":
        return "add_source_audit_table_and_school_variants"
    if mode == "mystical_boundary":
        return "add_boundary_counterexample_and_safe_rewrite"
    return "add_mixed_case_with_provenance_and_outcome"


def extend_tracks(domain: str, tracks: dict[str, bool]) -> dict[str, bool]:
    updated = dict(tracks)
    if domain in PRACTICAL_EXTENSION:
        updated["scientific_or_practical_validation"] = True
    if domain in PROVENANCE_EXTENSION:
        updated["provenance_audit"] = True
    if domain in MYSTICAL_EXTENSION:
        updated["mystical_boundary_priority"] = True
    return updated


def count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item[key])
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    audit = knowledge_coverage_audit.audit(root_path)
    domains: list[dict[str, Any]] = []
    for domain_info in audit["domains"]:
        domain = domain_info["domain"]
        tracks = extend_tracks(domain, paradigm_selector.evidence_track(domain))
        trunk = paradigm_selector.trunk_for_domain(domain)
        mode = evidence_mode(tracks)
        priority = priority_for(mode, tracks)
        domains.append(
            {
                "domain": domain,
                "display_name": domain_info["display_name"],
                "trunk": trunk,
                "evidence_mode": mode,
                "priority": priority,
                "mystical_intensity": mystical_intensity(tracks),
                "tracks": tracks,
                "case_template": case_template(mode, trunk["id"]),
                "next_action": next_action(mode, priority),
                "docs": {
                    "sop": domain_info["sections"]["sop"]["present"],
                    "knowledge": domain_info["sections"]["knowledge"]["present"],
                    "skill": domain_info["sections"]["skill"]["present"],
                },
                "tool_count": len(domain_info["sections"]["tools"]["present"]),
            }
        )
    domains = sorted(domains, key=lambda item: (item["priority"], item["trunk"]["id"], item["domain"]))
    result = {
        "tool": "domain_evidence_matrix_builder",
        "root": str(root_path),
        "is_valid": bool(audit["is_valid"]) and len(domains) == audit["domain_count"],
        "domain_count": len(domains),
        "trunk_count": len({item["trunk"]["id"] for item in domains}),
        "priority_counts": count_by(domains, "priority"),
        "evidence_mode_counts": count_by(domains, "evidence_mode"),
        "mystical_intensity_counts": count_by(domains, "mystical_intensity"),
        "track_counts": {
            "scientific_or_practical_validation": sum(
                1 for item in domains if item["tracks"]["scientific_or_practical_validation"]
            ),
            "provenance_audit": sum(1 for item in domains if item["tracks"]["provenance_audit"]),
            "mystical_boundary_priority": sum(
                1 for item in domains if item["tracks"]["mystical_boundary_priority"]
            ),
            "case_validation_recommended": sum(
                1 for item in domains if item["tracks"]["case_validation_recommended"]
            ),
        },
        "domains": domains,
        "workstreams": [
            {
                "id": "P0_practical_validation",
                "priority": "P0",
                "description": "先补可观察、可低成本实践、可回访评分的案例。",
                "domain_count": sum(1 for item in domains if item["priority"] == "P0"),
            },
            {
                "id": "P1_provenance_correction",
                "priority": "P1",
                "description": "补来源层级、派别差异、经典/现代/网络说法边界。",
                "domain_count": sum(1 for item in domains if item["priority"] == "P1"),
            },
            {
                "id": "P2_mystical_boundary",
                "priority": "P2",
                "description": "先做恐吓、依赖、替代专业支持和高价承诺的反例与安全改写。",
                "domain_count": sum(1 for item in domains if item["priority"] == "P2"),
            },
        ],
        "limits": [
            "证据矩阵只安排审计和案例工作，不证明任何玄学体系客观有效。",
            "P0 表示更适合做实用/科学化对照，不表示已经完成验证。",
            "P1 表示优先溯源勘误，不表示存在唯一正统解释。",
            "P2 表示神秘叙事边界优先，应先做风险反例和安全改写。",
        ],
        "next_steps": [
            "use_P0_domains_for_case_recorder_follow_up_templates",
            "use_P1_domains_for_source_audit_backlog",
            "use_P2_domains_for_boundary_counterexample_library",
            "rebuild_matrix_after_changing_paradigm_or_domain_sets",
        ],
    }
    result["generated_markdown"] = render_markdown(result)
    return result


def render_count_map(values: dict[str, int]) -> str:
    return "、".join(f"`{key}` {value}" for key, value in values.items())


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# 证据矩阵",
        "",
        "本页把 61 个领域按主干、证据模式、优先级、神秘强度和案例补强方向收束成一张维护矩阵。它用于决定先做哪些科学化/实用验证、哪些溯源勘误、哪些边界反例，而不是继续横向扩散新分支。",
        "",
        "## 摘要",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 领域 | {result['domain_count']} |",
        f"| 主干 | {result['trunk_count']} |",
        f"| 优先级 | {render_count_map(result['priority_counts'])} |",
        f"| 证据模式 | {render_count_map(result['evidence_mode_counts'])} |",
        f"| 神秘强度 | {render_count_map(result['mystical_intensity_counts'])} |",
        f"| 科学/实用轨道 | {result['track_counts']['scientific_or_practical_validation']} |",
        f"| 溯源勘误轨道 | {result['track_counts']['provenance_audit']} |",
        f"| 神秘边界轨道 | {result['track_counts']['mystical_boundary_priority']} |",
        "",
        "## 工作流",
        "",
    ]
    for stream in result["workstreams"]:
        lines.append(
            f"- `{stream['id']}`：{stream['description']}（{stream['domain_count']} 个领域）"
        )
    lines.extend(
        [
            "",
            "## 领域矩阵",
            "",
            "| 优先级 | 领域 | 主干 | 证据模式 | 神秘强度 | 案例模板 | 下一步 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in result["domains"]:
        lines.append(
            f"| {item['priority']} | {item['display_name']} (`{item['domain']}`) | {item['trunk']['title']} | `{item['evidence_mode']}` | `{item['mystical_intensity']}` | `{item['case_template']}` | `{item['next_action']}` |"
        )
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.extend(["", "## 下一步", ""])
    for step in result["next_steps"]:
        lines.append(f"- `{step}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/证据矩阵.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "证据矩阵.md"
        target.write_text(result["generated_markdown"], encoding="utf-8")
    if args.format == "markdown":
        print(result["generated_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
