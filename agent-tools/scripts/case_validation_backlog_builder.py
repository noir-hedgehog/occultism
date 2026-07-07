#!/usr/bin/env python3
"""Build a validation backlog from the domain evidence matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import domain_evidence_matrix_builder


TEMPLATE_FIELDS = {
    "before_after_or_diary_with_scores": [
        "request_text",
        "baseline_observation",
        "low_risk_action",
        "follow_up_window_days",
        "before_score",
        "after_score",
        "observed_changes",
        "validation_result",
        "reviewer",
    ],
    "experience_diary_red_flags_and_care_action": [
        "experience_text",
        "duration_or_frequency",
        "ordinary_triggers",
        "red_flags_checked",
        "care_action",
        "follow_up_window_days",
        "observed_changes",
        "validation_result",
        "reviewer",
    ],
    "before_after_or_safety_observation": [
        "space_or_object_description",
        "safety_constraints",
        "baseline_observation",
        "low_risk_action",
        "follow_up_window_days",
        "observed_changes",
        "validation_result",
        "reviewer",
    ],
    "source_comparison_and_interpretation_path": [
        "claim_text",
        "source_type",
        "source_title_or_url",
        "school_or_region",
        "primary_or_secondary_source",
        "conflicting_interpretations",
        "correction_note",
        "reviewer",
    ],
    "boundary_counterexample_and_safe_rewrite": [
        "unsafe_request_or_claim",
        "risk_category",
        "why_blocked_or_reframed",
        "safe_rewrite",
        "professional_boundary",
        "reviewer",
    ],
    "mixed_case_with_source_and_follow_up": [
        "request_text",
        "source_or_school_note",
        "interpretation_path",
        "low_risk_action",
        "follow_up_window_days",
        "observed_changes",
        "validation_result",
        "reviewer",
    ],
}


def acceptance_for(item: dict[str, Any]) -> list[str]:
    priority = item["priority"]
    if priority == "P0":
        return [
            "包含 baseline 与 follow-up，不只记录一次性解读。",
            "至少一个行动是低成本、可撤回、可现实观察的。",
            "用 consultation_case_recorder 生成候选记录，且 validation_result 不再是 unverified。",
        ]
    if priority == "P1":
        return [
            "至少区分原典/注疏/地区传统/现代作者/网络二手/用户自述中的一种。",
            "明确哪些说法无法确认或只属于特定流派。",
            "有 reviewer 记录，不把单一来源写成唯一正统。",
        ]
    return [
        "包含不安全原句或风险场景，不只写正向样例。",
        "给出安全改写，且不确认灵体事实、诅咒、操控他人或结果保证。",
        "如涉及医疗、法律、财务、精神危机或现实安全，明确专业边界。",
    ]


def recommended_tools(item: dict[str, Any]) -> list[str]:
    priority = item["priority"]
    tools = ["domain_evidence_matrix_builder"]
    if priority == "P0":
        tools.extend(["consultation_execution_runner", "consultation_handoff_builder", "consultation_case_recorder"])
    elif priority == "P1":
        tools.extend(["content_review_packet_builder", "content_review_feedback_recorder"])
    else:
        tools.extend(["mystic_intake_triage", "mystic_output_lint", "consultation_case_recorder"])
    return tools


def target_artifact(item: dict[str, Any]) -> str:
    if item["priority"] == "P0":
        return "reviewed_practical_case_candidate"
    if item["priority"] == "P1":
        return "source_audit_or_correction_note"
    return "boundary_counterexample_and_safe_rewrite"


def build_item(domain_item: dict[str, Any], rank: int) -> dict[str, Any]:
    template = domain_item["case_template"]
    return {
        "backlog_id": f"CV-{domain_item['priority']}-{rank:03d}-{domain_item['domain']}",
        "domain": domain_item["domain"],
        "display_name": domain_item["display_name"],
        "priority": domain_item["priority"],
        "trunk": domain_item["trunk"],
        "evidence_mode": domain_item["evidence_mode"],
        "mystical_intensity": domain_item["mystical_intensity"],
        "case_template": template,
        "target_artifact": target_artifact(domain_item),
        "required_fields": TEMPLATE_FIELDS.get(template, TEMPLATE_FIELDS["mixed_case_with_source_and_follow_up"]),
        "acceptance_criteria": acceptance_for(domain_item),
        "recommended_tools": recommended_tools(domain_item),
        "source_docs": domain_item["docs"],
        "status": "open",
    }


def build(root: str | Path = ".", priority: str | None = None, limit: int | None = None) -> dict[str, Any]:
    root_path = Path(root).resolve()
    matrix = domain_evidence_matrix_builder.build(root_path)
    domains = matrix["domains"]
    if priority:
        allowed = {"P0", "P1", "P2"}
        normalized = priority.strip().upper()
        if normalized not in allowed:
            raise ValueError("priority must be one of: P0, P1, P2")
        domains = [item for item in domains if item["priority"] == normalized]
    if limit is not None:
        domains = domains[: max(0, limit)]
    items = [build_item(item, index) for index, item in enumerate(domains, start=1)]
    priority_counts: dict[str, int] = {}
    artifact_counts: dict[str, int] = {}
    for item in items:
        priority_counts[item["priority"]] = priority_counts.get(item["priority"], 0) + 1
        artifact_counts[item["target_artifact"]] = artifact_counts.get(item["target_artifact"], 0) + 1
    result = {
        "tool": "case_validation_backlog_builder",
        "root": str(root_path),
        "is_valid": bool(matrix["is_valid"]) and bool(items),
        "source_matrix_domain_count": matrix["domain_count"],
        "backlog_count": len(items),
        "priority_filter": priority.strip().upper() if priority else "",
        "priority_counts": dict(sorted(priority_counts.items())),
        "target_artifact_counts": dict(sorted(artifact_counts.items())),
        "items": items,
        "workstreams": [
            {
                "id": "P0_practical_cases",
                "description": "补低风险实践、before/after、日记和 follow-up 评分案例。",
                "recommended_tool": "consultation_case_recorder",
            },
            {
                "id": "P1_source_audits",
                "description": "补来源层级、派别差异、地区/时代限制和勘误记录。",
                "recommended_tool": "content_review_feedback_recorder",
            },
            {
                "id": "P2_boundary_counterexamples",
                "description": "补恐吓、依赖、专业替代、高价承诺和操控他人的反例改写。",
                "recommended_tool": "mystic_output_lint",
            },
        ],
        "limits": [
            "此 backlog 是采集计划，不表示案例或来源已经收齐。",
            "真实 transcript、照片、个人经历和审校意见必须先脱敏并取得使用边界。",
            "P0/P1/P2 是工作优先级，不是玄学有效性等级。",
        ],
        "next_steps": [
            "collect_P0_follow_up_cases_with_consultation_case_recorder",
            "collect_P1_source_notes_with_content_review_feedback_recorder",
            "collect_P2_boundary_counterexamples_before_positive_mystical_cases",
            "rerun_release_gate_after_backlog_items_become_fixtures_or_docs",
        ],
    }
    result["generated_markdown"] = render_markdown(result)
    return result


def render_count_map(values: dict[str, int]) -> str:
    return "、".join(f"`{key}` {value}" for key, value in values.items()) or "-"


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# 案例验证 Backlog",
        "",
        "本页把证据矩阵转成可执行的案例、来源和边界反例采集清单。它用于推动实用案例、对照验证、溯源勘误和神秘边界审校，不用于证明玄学体系客观有效。",
        "",
        "## 摘要",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 来源矩阵领域 | {result['source_matrix_domain_count']} |",
        f"| Backlog 项 | {result['backlog_count']} |",
        f"| 优先级 | {render_count_map(result['priority_counts'])} |",
        f"| 目标产物 | {render_count_map(result['target_artifact_counts'])} |",
        "",
        "## 工作流",
        "",
    ]
    for stream in result["workstreams"]:
        lines.append(f"- `{stream['id']}`：{stream['description']} 推荐工具：`{stream['recommended_tool']}`")
    lines.extend(
        [
            "",
            "## Backlog",
            "",
            "| ID | 优先级 | 领域 | 目标产物 | 必填字段 | 推荐工具 |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in result["items"]:
        fields = ", ".join(f"`{field}`" for field in item["required_fields"])
        tools = ", ".join(f"`{tool}`" for tool in item["recommended_tools"])
        lines.append(
            f"| `{item['backlog_id']}` | {item['priority']} | {item['display_name']} (`{item['domain']}`) | `{item['target_artifact']}` | {fields} | {tools} |"
        )
    lines.extend(["", "## 验收标准", ""])
    for item in result["items"]:
        lines.append(f"### {item['backlog_id']} {item['display_name']}")
        for criterion in item["acceptance_criteria"]:
            lines.append(f"- {criterion}")
        lines.append("")
    lines.extend(["## 限制", ""])
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
    parser.add_argument("--priority", choices=["P0", "P1", "P2", "p0", "p1", "p2"], help="Optional priority filter.")
    parser.add_argument("--limit", type=int, help="Optional item limit.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/案例验证Backlog.md.")
    args = parser.parse_args()
    try:
        result = build(args.root, priority=args.priority, limit=args.limit)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "案例验证Backlog.md"
        target.write_text(result["generated_markdown"], encoding="utf-8")
    if args.format == "markdown":
        print(result["generated_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
