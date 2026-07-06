#!/usr/bin/env python3
"""Build a versioned maintenance manifest from current release evidence."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import knowledge_coverage_audit
import release_gate_runner


DEFAULT_OPEN_ITEMS = [
    "实际安装稳定 Skill 到 Codex skills 目录需要用户显式确认。",
    "真实匿名 transcript 需要用户或维护者提供素材并人工复核。",
    "更多真实案例、派别差异和内容专家审校仍需持续扩展。",
]

CADENCE = [
    {
        "cadence": "每次变更",
        "actions": [
            "更新对应 SOP、知识卡、Skill、工具 spec/schema 和测试。",
            "运行 agent_runtime_dry_run_runner，确认代表请求满足 runtime 契约。",
            "运行 agent_tool_wrapper_manifest_builder，确认工具 wrapper 元数据完整。",
            "运行 agent_tool_definition_validator，确认工具定义可注册。",
            "运行 agent_tool_registry_builder，确认工具注册顺序和安全启动工具。",
            "运行 agent_tool_registry_validator，确认注册顺序、Skill 索引和安全 bootstrap 一致。",
            "运行 release_gate_runner。",
            "运行 agent_runtime_handoff_builder，确认运行时交接入口仍完整。",
            "用 release_manifest_builder 生成或更新版本记录。",
        ],
    },
    {
        "cadence": "每周或每批素材",
        "actions": [
            "处理真实匿名 transcript，使用 transcript_anonymizer 和 transcript_fixture_builder。",
            "把失败评分回写到 SOP、Skill 或工具修订任务。",
            "复查看板 Doing/Backlog 是否仍反映真实状态。",
        ],
    },
    {
        "cadence": "每月",
        "actions": [
            "抽查各流派边界和禁用表达。",
            "扩展跨流派深度矩阵和案例库。",
            "确认稳定 Skill 是否需要安装、覆盖或下线。",
            "复核外部证据入口包、工具 wrapper manifest、工具定义验证、工具注册表、工具注册表验证和运行时交接包是否仍反映真实状态。",
        ],
    },
]


def gate_summary(gate_report: dict[str, Any]) -> dict[str, Any]:
    counts: dict[str, Any] = {}
    for gate in gate_report.get("gates", []):
        gate_id = gate.get("gate_id", "")
        summary = gate.get("summary", {})
        if gate_id == "schema_json":
            counts["schema_count"] = summary.get("schema_count")
        elif gate_id == "markdown_links":
            counts["markdown_file_count"] = summary.get("markdown_file_count")
        elif gate_id == "unit_tests":
            tail = str(summary.get("tail", ""))
            counts["unit_test_tail"] = tail.strip().splitlines()[-1] if tail.strip() else ""
        elif gate_id == "codex_skill_installer":
            counts["skill_install_dry_run_count"] = summary.get("skill_count")
    return counts


def build(
    root: str | Path = ".",
    version: str = "0.1.0",
    release_id: str | None = None,
    release_type: str = "maintenance",
    gate_report: dict[str, Any] | None = None,
    coverage_report: dict[str, Any] | None = None,
    open_items: list[str] | None = None,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    gates = gate_report or release_gate_runner.run(root_path)
    coverage = coverage_report or knowledge_coverage_audit.audit(root_path)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stable_release_id = release_id or f"mystic-agent-v{version}"
    gates_valid = bool(gates.get("is_valid"))
    coverage_valid = bool(coverage.get("is_valid"))
    status = "ready_for_review" if gates_valid and coverage_valid else "blocked"
    open_item_list = open_items if open_items is not None else DEFAULT_OPEN_ITEMS
    domain_count = coverage.get("domain_count")
    return {
        "tool": "release_manifest_builder",
        "release_id": stable_release_id,
        "version": version,
        "release_type": release_type,
        "generated_at": generated_at,
        "root": str(root_path),
        "status": status,
        "summary": {
            "domain_count": coverage.get("domain_count"),
            "complete_domain_count": coverage.get("complete_domain_count"),
            "gate_count": gates.get("gate_count"),
            "passed_gate_count": gates.get("passed_count"),
            "failed_gate_count": gates.get("failed_count"),
            **gate_summary(gates),
        },
        "quality_evidence": {
            "release_gate_is_valid": gates_valid,
            "knowledge_coverage_is_valid": coverage_valid,
            "gate_ids": [gate.get("gate_id") for gate in gates.get("gates", [])],
            "failed_gates": [gate.get("gate_id") for gate in gates.get("gates", []) if not gate.get("passed")],
        },
        "open_items": open_item_list,
        "maintenance_cadence": CADENCE,
        "release_notes": [
            f"首批 {domain_count} 个玄学 Skill 蓝图、SOP、知识卡和工具链处于自动质量门通过状态。",
            "发布门禁覆盖 schema、Skill 静态验证、Skill 安装 dry-run、覆盖审计、外部证据入口包、运行时 dry-run、工具 wrapper manifest、工具定义导出/验证、工具注册表/注册表验证、运行时交接包、回放、链接和单元测试。",
            "真实匿名对话已有脱敏、评分和 fixture 准入工具，但真实素材尚未纳入。",
        ],
        "limits": [
            "版本 manifest 汇总自动证据，不替代人工内容审校。",
            "ready_for_review 表示可进入人工发布复核，不表示已经安装到真实 Codex Skills。",
            "open_items 应在每次发布前复核，不能机械沿用。",
        ],
        "next_steps": ["review_open_items", "archive_manifest", "run_release_gate_after_next_change"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--version", default="0.1.0", help="Version string for the manifest.")
    parser.add_argument("--release-id", help="Stable release id. Defaults to mystic-agent-v<version>.")
    parser.add_argument("--release-type", default="maintenance", help="Release type label.")
    parser.add_argument("--open-item", action="append", help="Known open item. Can be repeated.")
    args = parser.parse_args()
    result = build(
        root=args.root,
        version=args.version,
        release_id=args.release_id,
        release_type=args.release_type,
        open_items=args.open_item,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "ready_for_review" else 1


if __name__ == "__main__":
    raise SystemExit(main())
