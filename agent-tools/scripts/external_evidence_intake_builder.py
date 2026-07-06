#!/usr/bin/env python3
"""Build intake packets for external evidence needed before public release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import content_review_packet_builder
import knowledge_coverage_audit
import skill_install_readiness_report


def command_list(codex_home: str) -> list[str]:
    return [
        "python3 agent-tools/scripts/skill_install_readiness_report.py --codex-home "
        f"{codex_home} --format markdown",
        "python3 agent-tools/scripts/transcript_anonymizer.py --skill tarot --source-label real-001 --text '<raw transcript>'",
        "python3 agent-tools/scripts/transcript_fixture_builder.py --skill tarot --source-label real-001 "
        "--reviewer reviewer-a --review-approved --scores '{\"safety\":2,\"clarification\":1,"
        "\"workflow_fit\":1,\"symbol_accuracy\":1,\"actionability\":1,\"tone\":1}' --text '<anonymized transcript>'",
        "python3 agent-tools/scripts/content_review_feedback_recorder.py --domain tarot --reviewer tarot-reviewer "
        "--review-date 2026-07-02 --decision approved --approved-scope '塔罗 SOP、知识卡、Skill 和工具 spec'",
        "python3 agent-tools/scripts/pilot_readiness_report.py --codex-home "
        f"{codex_home} --format markdown",
    ]


def build(root: str | Path = ".", codex_home: str | Path | None = None) -> dict[str, Any]:
    root_path = Path(root).resolve()
    install = skill_install_readiness_report.build(root=root_path, codex_home=codex_home)
    coverage = knowledge_coverage_audit.audit(root_path)
    review = content_review_packet_builder.build(root_path)
    target_codex_home = install["codex_home"]
    automated_ready = bool(install["is_valid"] and coverage["is_valid"] and review["is_valid"])
    intake_items = [
        {
            "intake_id": "EXT-001",
            "blocker": "actual_skill_install_requires_user_confirmation",
            "title": "Codex Skill 实际安装确认",
            "owner": "user",
            "status": "waiting_for_user_confirmation" if install["is_valid"] else "blocked_by_install_dry_run",
            "target_artifact": "Codex skills installation record",
            "required_fields": [
                "codex_home",
                "skill_scope",
                "approver",
                "approval_date",
                "dry_run_report_reviewed",
                "target_path_confirmed",
                "install_command_approved",
            ],
            "evidence_acceptance": [
                "skill_install_readiness_report 返回 ready_for_install_approval。",
                "用户明确确认安装目标、安装范围和是否允许覆盖。",
                "codex_skill_installer 使用 --install 后记录 copied_count 或 already_current_count。",
            ],
            "commands": [
                f"python3 agent-tools/scripts/skill_install_readiness_report.py --codex-home {target_codex_home} --format markdown",
                install["install_command"],
            ],
            "kanban_ids": ["K-032"],
        },
        {
            "intake_id": "EXT-002",
            "blocker": "real_anonymized_transcripts_needed",
            "title": "真实匿名 transcript 收集与回放准入",
            "owner": "user_or_maintainer",
            "status": "waiting_for_reviewed_real_samples",
            "target_artifact": "Reviewed anonymized transcript fixtures",
            "required_fields": [
                "source_label",
                "skill",
                "raw_transcript_location",
                "consent_or_usage_basis",
                "anonymizer_output",
                "human_reviewer",
                "review_scores",
                "review_approved",
                "residual_privacy_check",
            ],
            "evidence_acceptance": [
                "transcript_anonymizer 输出 can_enter_validation_set=true 且无直接身份残留。",
                "transcript_fixture_builder 输出 ready_for_replay=true。",
                "维护者把 fixture 映射到回放集后 skill_transcript_runner 仍通过。",
            ],
            "commands": [
                "python3 agent-tools/scripts/transcript_anonymizer.py --skill tarot --source-label real-001 --text '<raw transcript>'",
                "python3 agent-tools/scripts/transcript_fixture_builder.py --skill tarot --source-label real-001 "
                "--reviewer reviewer-a --review-approved --scores '{\"safety\":2,\"clarification\":1,"
                "\"workflow_fit\":1,\"symbol_accuracy\":1,\"actionability\":1,\"tone\":1}' --text '<anonymized transcript>'",
                "python3 agent-tools/scripts/skill_transcript_runner.py",
            ],
            "kanban_ids": ["K-021"],
        },
        {
            "intake_id": "EXT-003",
            "blocker": "content_expert_approval_needed",
            "title": "内容专家审校批准",
            "owner": "domain_reviewer",
            "status": "waiting_for_reviewer_feedback",
            "target_artifact": "Structured content review approval records",
            "required_fields": [
                "domain",
                "reviewer",
                "review_date",
                "decision",
                "approved_scope",
                "required_corrections_or_no_change",
                "residual_risks",
            ],
            "evidence_acceptance": [
                "content_review_packet_builder 对目标流派返回 ready_for_human_review。",
                "content_review_feedback_recorder 返回 can_count_as_content_approval=true。",
                "如有 changes_requested，必改项先进入看板并修复后重新审校。",
            ],
            "commands": [
                "python3 agent-tools/scripts/content_review_packet_builder.py --format markdown",
                "python3 agent-tools/scripts/content_review_feedback_recorder.py --domain tarot --reviewer tarot-reviewer "
                "--review-date 2026-07-02 --decision approved --approved-scope '塔罗 SOP、知识卡、Skill 和工具 spec'",
            ],
            "kanban_ids": ["QA-009"],
        },
    ]
    return {
        "tool": "external_evidence_intake_builder",
        "root": str(root_path),
        "is_valid": automated_ready,
        "status": "ready_for_external_collection" if automated_ready else "blocked_by_automated_checks",
        "intake_count": len(intake_items),
        "open_intake_count": sum(1 for item in intake_items if item["status"].startswith("waiting")),
        "codex_home": target_codex_home,
        "intake_items": intake_items,
        "summary": {
            "coverage_is_valid": coverage["is_valid"],
            "install_readiness": install["status"],
            "review_ready_count": review["ready_for_review_count"],
            "review_approved_count": review["approved_count"],
        },
        "recommended_sequence": [
            "先确认 Skill 安装目标和范围。",
            "再收集真实 transcript 并完成脱敏、人工评分、fixture 准入。",
            "最后让内容专家按流派审校包记录批准或必改项。",
            "任一外部证据更新后重新运行 pilot_readiness_report 和 release_gate_runner。",
        ],
        "limits": [
            "此工具只生成外部证据收集入口，不表示外部证据已经存在。",
            "真实 transcript 必须由人确认脱敏和使用边界，不能只依赖规则替换。",
            "内容批准记录结构完整不等于审校人资质自动成立。",
        ],
        "next_steps": [
            "share_intake_packet_with_user_or_maintainer",
            "collect_required_fields_for_each_open_intake",
            "rerun_pilot_readiness_after_evidence_is_recorded",
        ],
        "command_templates": command_list(target_codex_home),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# 外部证据入口包",
        "",
        "本页把完整发布前仍需要人工或真实环境提供的证据整理成可执行入口。它不表示证据已经收齐，只表示收集方式、字段和验收标准已经明确。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 状态 | `{result['status']}` |",
        f"| Intake 项 | {result['intake_count']} |",
        f"| 待收集 | {result['open_intake_count']} |",
        f"| Codex home | `{result['codex_home']}` |",
        f"| 覆盖审计通过 | {result['summary']['coverage_is_valid']} |",
        f"| 安装准备 | `{result['summary']['install_readiness']}` |",
        f"| 可进入审校流派 | {result['summary']['review_ready_count']} |",
        f"| 已批准审校 | {result['summary']['review_approved_count']} |",
        "",
        "## Intake 清单",
        "",
    ]
    for item in result["intake_items"]:
        lines.extend(
            [
                f"### {item['intake_id']} {item['title']}",
                "",
                f"- Blocker：`{item['blocker']}`",
                f"- Owner：{item['owner']}",
                f"- 状态：`{item['status']}`",
                f"- 目标产物：{item['target_artifact']}",
                f"- 看板：{', '.join(f'`{kanban_id}`' for kanban_id in item['kanban_ids'])}",
                "",
                "必填字段：",
                "",
            ]
        )
        for field in item["required_fields"]:
            lines.append(f"- `{field}`")
        lines.extend(["", "验收标准：", ""])
        for evidence in item["evidence_acceptance"]:
            lines.append(f"- {evidence}")
        lines.extend(["", "命令模板：", "", "```bash"])
        lines.extend(item["commands"])
        lines.extend(["```", ""])
    lines.extend(["## 推荐顺序", ""])
    for step in result["recommended_sequence"]:
        lines.append(f"- {step}")
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--codex-home", help="Target Codex home for install-readiness commands.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/外部证据入口包.md.")
    args = parser.parse_args()
    result = build(root=args.root, codex_home=args.codex_home)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "外部证据入口包.md"
        target.write_text(render_markdown(result), encoding="utf-8")
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
