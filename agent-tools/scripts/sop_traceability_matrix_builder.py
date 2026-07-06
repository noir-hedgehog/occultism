#!/usr/bin/env python3
"""Build traceability matrix linking SOPs, Skills, tools, knowledge, and verification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import knowledge_coverage_audit
import tool_manifest_builder


def read_text(root: Path, paths: list[str]) -> str:
    chunks: list[str] = []
    for path in paths:
        full = root / path
        if full.exists():
            chunks.append(full.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def headings(root: Path, paths: list[str]) -> list[str]:
    found: list[str] = []
    for path in paths:
        full = root / path
        if not full.exists():
            continue
        for line in full.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("## "):
                found.append(stripped.removeprefix("## ").strip())
    return found


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    coverage = knowledge_coverage_audit.audit(root_path)
    manifest = tool_manifest_builder.build(root_path)
    tool_names = {tool["name"] for tool in manifest.get("tools", [])}
    rows: list[dict[str, Any]] = []
    missing_links: list[dict[str, str]] = []
    for domain in coverage.get("domains", []):
        sections = domain["sections"]
        sop_paths = sections["sop"]["present"]
        skill_paths = sections["skill"]["present"]
        tool_chain = [item["tool"] for item in sections["tools"]["present"]]
        sop_text = read_text(root_path, sop_paths)
        skill_text = read_text(root_path, skill_paths)
        mentioned_in_sop = sorted(tool for tool in tool_chain if tool in sop_text)
        mentioned_in_skill = sorted(tool for tool in tool_chain if tool in skill_text)
        unmentioned = sorted(tool for tool in tool_chain if tool not in sop_text and tool not in skill_text)
        for tool in unmentioned:
            missing_links.append({"domain": domain["domain"], "tool": tool, "issue": "tool_not_mentioned_in_sop_or_skill"})
        rows.append(
            {
                "domain": domain["domain"],
                "display_name": domain["display_name"],
                "level": domain["level"],
                "sop": sop_paths,
                "sop_headings": headings(root_path, sop_paths),
                "knowledge": sections["knowledge"]["present"],
                "skill": skill_paths,
                "tool_chain": tool_chain,
                "verification_tools": [item["tool"] for item in sections["verification"]["present"]],
                "tool_specs": [knowledge_coverage_audit.tool_files(tool)["spec"] for tool in tool_chain if tool in tool_names],
                "mentioned_in_sop": mentioned_in_sop,
                "mentioned_in_skill": mentioned_in_skill,
                "unmentioned_tools": unmentioned,
                "is_traceable": domain["is_complete"] and not unmentioned,
            }
        )
    result = {
        "tool": "sop_traceability_matrix_builder",
        "root": str(root_path),
        "is_valid": coverage["is_valid"] and manifest["is_valid"] and not missing_links,
        "domain_count": len(rows),
        "traceable_domain_count": sum(1 for row in rows if row["is_traceable"]),
        "missing_link_count": len(missing_links),
        "rows": rows,
        "missing_links": missing_links,
        "limits": [
            "追踪矩阵检查 SOP/Skill/工具链引用关系，不证明内容专家已经批准。",
            "工具被提到只表示流程可追踪，不代表工具调用参数已经覆盖所有真实场景。",
            "真实匿名 transcript 和实际安装状态仍由独立流程验证。",
        ],
        "next_steps": [
            "review_unmentioned_tools",
            "update_sop_or_skill_when_tool_chain_changes",
            "rerun_knowledge_coverage_audit",
        ],
    }
    result["generated_markdown"] = render_markdown(result)
    return result


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# SOP/Tool/Skill 追踪矩阵",
        "",
        "本页追踪每个流派从 SOP、知识卡、Skill、工具链到验证工具的对应关系。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 覆盖领域 | {result['domain_count']} |",
        f"| 可追踪领域 | {result['traceable_domain_count']} |",
        f"| 缺失引用 | {result['missing_link_count']} |",
        "",
        "## 矩阵",
        "",
        "| 流派 | 等级 | SOP | Skill | 工具数 | SOP 提及 | Skill 提及 | 验证 | 状态 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        sop = "、".join(f"[{Path(path).stem}]({path.removeprefix('知识库/')})" for path in row["sop"]) or "-"
        skill = "、".join(f"[{Path(path).parts[1]}](../{path})" for path in row["skill"]) or "-"
        status = "traceable" if row["is_traceable"] else "needs_update"
        lines.append(
            f"| {row['display_name']} | {row['level']} | {sop} | {skill} | {len(row['tool_chain'])} | {len(row['mentioned_in_sop'])} | {len(row['mentioned_in_skill'])} | {', '.join(row['verification_tools'])} | `{status}` |"
        )
    if result["missing_links"]:
        lines.extend(["", "## 缺失引用", ""])
        for item in result["missing_links"]:
            lines.append(f"- `{item['domain']}` / `{item['tool']}`：{item['issue']}")
    lines.extend(["", "## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/SOP-Tool-Skill追踪矩阵.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "SOP-Tool-Skill追踪矩阵.md"
        target.write_text(result["generated_markdown"], encoding="utf-8")
    if args.format == "markdown":
        print(result["generated_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
