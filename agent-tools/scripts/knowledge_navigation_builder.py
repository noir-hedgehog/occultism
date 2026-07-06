#!/usr/bin/env python3
"""Build a human-readable navigation index for the mystic knowledge base."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import knowledge_coverage_audit
import tool_manifest_builder


KANBAN_SECTIONS = ["Backlog", "Doing", "Review", "Done"]
TABLE_ROW_RE = re.compile(r"^\|\s*(?P<id>[A-Z]+-\d+|INIT-\d+)\s*\|")


def markdown_title(path: Path) -> str:
    if not path.exists():
        return path.stem
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    return path.stem


def nav_target(path: str) -> str:
    if path.startswith("知识库/"):
        return path.removeprefix("知识库/")
    return f"../{path}"


def link(path: str) -> str:
    title = Path(path).stem
    return f"[{title}]({nav_target(path)})"


def count_kanban(root: Path) -> dict[str, int]:
    path = root / "知识库" / "看板.md"
    counts = {section: 0 for section in KANBAN_SECTIONS}
    if not path.exists():
        return counts
    current = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            current = stripped.removeprefix("## ").strip()
            continue
        if current in counts and TABLE_ROW_RE.match(stripped):
            counts[current] += 1
    return counts


def list_markdown(root: Path, directory: str) -> list[dict[str, str]]:
    base = root / directory
    if not base.exists():
        return []
    return [
        {"title": markdown_title(path), "path": str(path.relative_to(root))}
        for path in sorted(base.glob("*.md"))
    ]


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    coverage = knowledge_coverage_audit.audit(root_path)
    manifest = tool_manifest_builder.build(root_path)
    markdown_files = sorted((root_path / "知识库").rglob("*.md")) if (root_path / "知识库").exists() else []
    domains = [
        {
            "domain": domain["domain"],
            "display_name": domain["display_name"],
            "level": domain["level"],
            "sop": domain["sections"]["sop"]["present"],
            "knowledge": domain["sections"]["knowledge"]["present"],
            "skill": domain["sections"]["skill"]["present"],
            "tools": [item["tool"] for item in domain["sections"]["tools"]["present"]],
        }
        for domain in coverage.get("domains", [])
    ]
    result = {
        "tool": "knowledge_navigation_builder",
        "root": str(root_path),
        "is_valid": bool(coverage.get("is_valid")) and bool(manifest.get("is_valid")),
        "document_count": len(markdown_files),
        "domain_count": coverage.get("domain_count", 0),
        "complete_domain_count": coverage.get("complete_domain_count", 0),
        "tool_count": manifest.get("tool_count", 0),
        "skill_count": manifest.get("skill_count", 0),
        "kanban_counts": count_kanban(root_path),
        "primary_navigation": [
            {"title": "总览", "path": "知识库/00-总览.md"},
            {"title": "安全边界", "path": "知识库/01-安全边界.md"},
            {"title": "流派地图", "path": "知识库/02-流派地图.md"},
            {"title": "质量检查清单", "path": "知识库/04-质量检查清单.md"},
            {"title": "看板", "path": "知识库/看板.md"},
            {"title": "仪表盘", "path": "知识库/仪表盘.md"},
            {"title": "发布验收", "path": "知识库/发布验收.md"},
            {"title": "外部证据入口包", "path": "知识库/外部证据入口包.md"},
            {"title": "Agent 运行时交接包", "path": "知识库/Agent运行时交接包.md"},
        ],
        "sections": {
            "sop": list_markdown(root_path, "知识库/SOP"),
            "schools": list_markdown(root_path, "知识库/流派"),
            "templates": list_markdown(root_path, "知识库/模板"),
        },
        "domains": domains,
        "limits": [
            "导航索引证明文件结构和自动证据可被读取，不替代内容质量审校。",
            "看板计数来自 Markdown 表格结构，任务含义仍需维护者复核。",
            "真实匿名 transcript 和实际 Skill 安装仍按独立流程验收。",
        ],
        "next_steps": [
            "review_navigation_index_after_large_content_changes",
            "run_release_gate_runner_before_publishing",
            "use_tool_manifest_builder_before_agent_runtime_integration",
        ],
    }
    result["generated_markdown"] = render_markdown(result)
    return result


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# 导航索引",
        "",
        "本页是给维护者和使用者看的知识库入口。它按阅读顺序、流派、SOP、工具和发布证据组织当前资料。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 文档 | {result['document_count']} |",
        f"| 覆盖领域 | {result['complete_domain_count']}/{result['domain_count']} |",
        f"| 工具 | {result['tool_count']} |",
        f"| Skill | {result['skill_count']} |",
        f"| 看板 Backlog | {result['kanban_counts'].get('Backlog', 0)} |",
        f"| 看板 Doing | {result['kanban_counts'].get('Doing', 0)} |",
        f"| 看板 Review | {result['kanban_counts'].get('Review', 0)} |",
        f"| 看板 Done | {result['kanban_counts'].get('Done', 0)} |",
        "",
        "## 推荐阅读顺序",
        "",
    ]
    for item in result["primary_navigation"]:
        lines.append(f"- [{item['title']}]({nav_target(item['path'])})")
    lines.extend(["", "## 流派入口", "", "| 流派 | 等级 | SOP | 知识卡 | Skill | 工具数 |", "| --- | --- | --- | --- | --- | --- |"])
    for domain in result["domains"]:
        sop = "、".join(link(path) for path in domain["sop"]) or "-"
        knowledge = "、".join(link(path) for path in domain["knowledge"]) or "-"
        skill = "、".join(f"[{Path(path).parts[1]}]({nav_target(path)})" for path in domain["skill"]) or "-"
        lines.append(
            f"| {domain['display_name']} | {domain['level']} | {sop} | {knowledge} | {skill} | {len(domain['tools'])} |"
        )
    lines.extend(["", "## SOP", ""])
    for item in result["sections"]["sop"]:
        lines.append(f"- [{item['title']}]({nav_target(item['path'])})")
    lines.extend(["", "## 工具与验证", ""])
    lines.extend(
        [
            "- [Agent Tool Catalog](../agent-tools/tool-catalog.md)",
            "- [Codex Skill Index](../codex-skills/index.md)",
            "- [Agent 路由冒烟验证](Agent路由冒烟验证.md)",
            "- [Agent Runtime Dry-run 验证](Agent运行时DryRun验证.md)",
            "- [Agent Tool Wrapper Manifest](Agent工具WrapperManifest.md)",
            "- [Agent Tool Definition Export](Agent工具定义导出.md)",
            "- [Agent Tool Definition Validation](Agent工具定义验证.md)",
            "- [Agent Tool Registry](Agent工具注册表.md)",
            "- [Agent Tool Registry Validation](Agent工具注册表验证.md)",
            "- [工具与 Skill Manifest 规范](工具与Skill Manifest规范.md)",
            "- [内容审校包](内容审校包.md)",
            "- [内容审校反馈记录规范](内容审校反馈记录规范.md)",
            "- [Skill 安装准备报告](Skill安装准备报告.md)",
            "- [SOP/Tool/Skill 追踪矩阵](SOP-Tool-Skill追踪矩阵.md)",
            "- [试运行准备度报告](试运行准备度报告.md)",
            "- [外部证据入口包](外部证据入口包.md)",
            "- [Agent 运行时交接包](Agent运行时交接包.md)",
            "- [维护审计](维护审计.md)",
            "- [版本记录](版本记录.md)",
            "- [维护节奏](维护节奏.md)",
        ]
    )
    lines.extend(["", "## 维护提醒", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/导航索引.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "导航索引.md"
        target.write_text(result["generated_markdown"], encoding="utf-8")
    if args.format == "markdown":
        print(result["generated_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
