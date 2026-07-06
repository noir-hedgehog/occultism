#!/usr/bin/env python3
"""Build a pilot-readiness report from automated evidence and external blockers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import agent_route_smoke_runner
import content_review_packet_builder
import knowledge_coverage_audit
import skill_install_readiness_report
import sop_traceability_matrix_builder


EXTERNAL_BLOCKERS = [
    {
        "blocker": "actual_skill_install_requires_user_confirmation",
        "owner": "user",
        "required_evidence": "用户明确确认安装目标和执行 --install 后的安装记录。",
    },
    {
        "blocker": "real_anonymized_transcripts_needed",
        "owner": "user_or_maintainer",
        "required_evidence": "真实 transcript 经脱敏、人工评分和批准后进入 fixture 或回放记录。",
    },
    {
        "blocker": "content_expert_approval_needed",
        "owner": "domain_reviewer",
        "required_evidence": "content_review_feedback_recorder 记录可计入批准的专家反馈。",
    },
]


def build(root: str | Path = ".", codex_home: str | Path | None = None) -> dict[str, Any]:
    root_path = Path(root).resolve()
    coverage = knowledge_coverage_audit.audit(root_path)
    route_smoke = agent_route_smoke_runner.run(root=root_path)
    traceability = sop_traceability_matrix_builder.build(root_path)
    install = skill_install_readiness_report.build(root=root_path, codex_home=codex_home)
    review = content_review_packet_builder.build(root_path)
    automated_checks = [
        {
            "check": "knowledge_coverage",
            "passed": bool(coverage["is_valid"]),
            "summary": f"{coverage['complete_domain_count']}/{coverage['domain_count']} domains complete",
        },
        {
            "check": "route_smoke",
            "passed": bool(route_smoke["is_valid"]),
            "summary": f"{route_smoke['passed_count']}/{route_smoke['case_count']} route cases passed",
        },
        {
            "check": "traceability",
            "passed": bool(traceability["is_valid"]),
            "summary": f"{traceability['traceable_domain_count']}/{traceability['domain_count']} domains traceable",
        },
        {
            "check": "skill_install_dry_run",
            "passed": bool(install["is_valid"]),
            "summary": f"{install['skill_count']} skills, {install['conflict_count']} conflicts",
        },
        {
            "check": "content_review_packet",
            "passed": bool(review["is_valid"]),
            "summary": f"{review['ready_for_review_count']}/{review['domain_count']} domains ready for human review",
        },
    ]
    automated_ready = all(check["passed"] for check in automated_checks)
    external_blockers = list(EXTERNAL_BLOCKERS)
    if review["approved_count"] > 0:
        external_blockers = [item for item in external_blockers if item["blocker"] != "content_expert_approval_needed"]
    return {
        "tool": "pilot_readiness_report",
        "root": str(root_path),
        "is_valid": automated_ready,
        "pilot_status": "ready_for_internal_dry_run" if automated_ready else "blocked_by_automated_checks",
        "public_release_status": "blocked_by_external_evidence",
        "automated_ready": automated_ready,
        "automated_checks": automated_checks,
        "external_blocker_count": len(external_blockers),
        "external_blockers": external_blockers,
        "summary": {
            "domain_count": coverage["domain_count"],
            "complete_domain_count": coverage["complete_domain_count"],
            "route_case_count": route_smoke["case_count"],
            "route_passed_count": route_smoke["passed_count"],
            "traceable_domain_count": traceability["traceable_domain_count"],
            "skill_install_readiness": install["status"],
            "content_review_ready_count": review["ready_for_review_count"],
            "content_review_approved_count": review["approved_count"],
        },
        "limits": [
            "ready_for_internal_dry_run 表示自动证据足够内部试运行，不表示可公开发布。",
            "public_release_status 在真实安装、真实 transcript 和专家批准前保持阻塞。",
            "此报告汇总现有证据，不替代逐项人工复核。",
        ],
        "next_steps": [
            "request_explicit_skill_install_confirmation",
            "collect_and_anonymize_real_transcripts",
            "assign_content_reviewers_and_record_feedback",
            "use_external_evidence_intake_package",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# 试运行准备度报告",
        "",
        "本页汇总自动证据和外部阻塞项，用于判断玄学 agent 是否可进入内部试运行，以及为什么仍不能视为完整发布。",
        "",
        "## 状态",
        "",
        "| 项目 | 当前值 |",
        "| --- | --- |",
        f"| 内部试运行 | `{result['pilot_status']}` |",
        f"| 完整发布 | `{result['public_release_status']}` |",
        f"| 自动证据通过 | {result['automated_ready']} |",
        f"| 外部阻塞项 | {result['external_blocker_count']} |",
        "",
        "## 自动证据",
        "",
        "| Check | Passed | Summary |",
        "| --- | --- | --- |",
    ]
    for check in result["automated_checks"]:
        lines.append(f"| `{check['check']}` | {check['passed']} | {check['summary']} |")
    lines.extend(["", "## 外部阻塞项", "", "| Blocker | Owner | Required Evidence |", "| --- | --- | --- |"])
    for blocker in result["external_blockers"]:
        lines.append(f"| `{blocker['blocker']}` | {blocker['owner']} | {blocker['required_evidence']} |")
    lines.extend(
        [
            "",
            "## 外部证据入口",
            "",
            "这些阻塞项的字段、命令模板和验收标准集中维护在 [外部证据入口包](外部证据入口包.md)。",
        ]
    )
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--codex-home", help="Target Codex home for install dry-run.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/试运行准备度报告.md.")
    args = parser.parse_args()
    result = build(root=args.root, codex_home=args.codex_home)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "试运行准备度报告.md"
        target.write_text(render_markdown(result), encoding="utf-8")
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
