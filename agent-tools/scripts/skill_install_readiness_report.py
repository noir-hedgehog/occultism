#!/usr/bin/env python3
"""Build a dry-run readiness report for installing mystic Codex Skills."""

from __future__ import annotations

import argparse
import json
import shlex
from pathlib import Path
from typing import Any

import codex_skill_installer
import content_review_packet_builder
import knowledge_coverage_audit


def install_command(codex_home: str, skills: list[str] | None = None, overwrite: bool = False) -> str:
    parts = ["python3", "agent-tools/scripts/codex_skill_installer.py", "--codex-home", codex_home, "--install"]
    for skill in skills or []:
        parts.extend(["--skill", skill])
    if overwrite:
        parts.append("--overwrite")
    return " ".join(shlex.quote(part) for part in parts)


def build(
    root: str | Path = ".",
    codex_home: str | Path | None = None,
    skills: list[str] | None = None,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    plan = codex_skill_installer.install_plan(root=root_path, codex_home=codex_home, skills=skills, dry_run=True)
    coverage = knowledge_coverage_audit.audit(root_path)
    review = content_review_packet_builder.build(root_path)
    conflicts = [action for action in plan["actions"] if action["conflict"]]
    creates = [action for action in plan["actions"] if action["action"] == "create"]
    already_current = [action for action in plan["actions"] if action["action"] == "already_current"]
    blocked = conflicts or not plan["validation_summary"]["is_valid"] or not coverage["is_valid"]
    status = "blocked" if blocked else "ready_for_install_approval"
    selected_skills = skills or [action["skill"] for action in plan["actions"]]
    result = {
        "tool": "skill_install_readiness_report",
        "root": str(root_path),
        "codex_home": plan["codex_home"],
        "target_root": plan["target_root"],
        "status": status,
        "is_valid": not blocked,
        "requires_explicit_approval": True,
        "skill_count": plan["skill_count"],
        "create_count": len(creates),
        "already_current_count": len(already_current),
        "conflict_count": len(conflicts),
        "content_review_approved_count": review["approved_count"],
        "content_review_ready_count": review["ready_for_review_count"],
        "coverage_is_valid": coverage["is_valid"],
        "validation_summary": plan["validation_summary"],
        "actions": plan["actions"],
        "approval_checklist": [
            "确认目标 Codex home 正确。",
            "确认将安装或覆盖的 Skill 名称正确。",
            "确认当前仓库路径会在 Skill 引用知识库和工具时保持可访问。",
            "确认真实匿名 transcript、内容审校和安装时机的开放事项是否可接受。",
            "确认如需覆盖已有 Skill，已人工检查差异并显式加入 --overwrite。",
        ],
        "install_command": install_command(plan["codex_home"], selected_skills),
        "overwrite_command": install_command(plan["codex_home"], selected_skills, overwrite=True),
        "blockers": [
            *[f"{item['skill']}: {item['reason']}" for item in conflicts],
            *(["skill_blueprint_validation_failed"] if not plan["validation_summary"]["is_valid"] else []),
            *(["knowledge_coverage_failed"] if not coverage["is_valid"] else []),
        ],
        "limits": [
            "此报告只做 dry-run 准备，不安装或覆盖任何 Skill。",
            "ready_for_install_approval 表示可请求人工确认，不表示已经安装。",
            "内容审校批准数来自审校包当前记录；没有真实审校反馈时不应视为内容已批准。",
        ],
        "next_steps": [
            "review_approval_checklist",
            "ask_user_for_explicit_install_confirmation",
            "run_install_command_only_after_confirmation",
        ],
    }
    result["generated_markdown"] = render_markdown(result)
    return result


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Skill 安装准备报告",
        "",
        "本页汇总 Codex Skill 安装前的 dry-run 证据、目标路径、冲突状态和审批清单。它不表示已经安装。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 状态 | `{result['status']}` |",
        f"| 目标 Codex home | `{result['codex_home']}` |",
        f"| 目标 skills 目录 | `{result['target_root']}` |",
        f"| Skill 数 | {result['skill_count']} |",
        f"| 将创建 | {result['create_count']} |",
        f"| 已是最新 | {result['already_current_count']} |",
        f"| 冲突 | {result['conflict_count']} |",
        f"| 内容审校批准 | {result['content_review_approved_count']} |",
        f"| 可进入内容审校 | {result['content_review_ready_count']} |",
        "",
        "## 审批清单",
        "",
    ]
    for item in result["approval_checklist"]:
        lines.append(f"- {item}")
    lines.extend(["", "## 安装命令", "", "仅在用户明确确认后运行：", "", "```bash", result["install_command"], "```", ""])
    if result["conflict_count"]:
        lines.extend(["覆盖冲突时仅在人工复核差异后运行：", "", "```bash", result["overwrite_command"], "```", ""])
    lines.extend(["## Dry-run 行动", "", "| Skill | Action | Reason |", "| --- | --- | --- |"])
    for action in result["actions"]:
        lines.append(f"| `{action['skill']}` | `{action['action']}` | {action['reason']} |")
    if result["blockers"]:
        lines.extend(["", "## Blockers", ""])
        for blocker in result["blockers"]:
            lines.append(f"- {blocker}")
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--codex-home", help="Target Codex home. Defaults to CODEX_HOME or ~/.codex.")
    parser.add_argument("--skill", action="append", help="Report only this skill. Can be repeated.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/Skill安装准备报告.md.")
    args = parser.parse_args()
    result = build(root=args.root, codex_home=args.codex_home, skills=args.skill)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "Skill安装准备报告.md"
        target.write_text(result["generated_markdown"], encoding="utf-8")
    if args.format == "markdown":
        print(result["generated_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
