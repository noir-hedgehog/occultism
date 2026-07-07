#!/usr/bin/env python3
"""Build a matrix of human UI, API, programmable, and Agent handoff surfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SURFACES: list[dict[str, Any]] = [
    {
        "surface_id": "knowledge_docs_site",
        "display_name": "知识库文档站",
        "user_surface": "Web UI 文档站与侧边栏入口",
        "api_endpoint": "/api/docs",
        "primary_tool": "knowledge_navigation_builder",
        "automation_level": "human_readable",
        "agent_boundary": "Agent 可读取导航和文档，但内容理解、取舍和引用仍需遵守安全边界。",
        "proof_docs": ["知识库/导航索引.md", "知识库/06-体系盘点与主干路线.md"],
        "verification_command": "curl http://127.0.0.1:8765/api/docs",
    },
    {
        "surface_id": "request_router",
        "display_name": "请求路由与安全分流",
        "user_surface": "顶部请求框与流派选择",
        "api_endpoint": "/api/session",
        "primary_tool": "agent_workflow_router",
        "automation_level": "programmable_now",
        "agent_boundary": "可自动识别领域、风险和上下文；orange/red 风险必须暂停玄学流程。",
        "proof_docs": ["知识库/Agent路由冒烟验证.md", "知识库/Agent运行时DryRun验证.md"],
        "verification_command": "curl -X POST http://127.0.0.1:8765/api/session -H 'Content-Type: application/json' -d '{\"request_text\":\"帮我做一个塔罗三张牌，看看工作状态\"}'",
    },
    {
        "surface_id": "example_presets",
        "display_name": "主干示例请求",
        "user_surface": "请求框下方的 6 条主干示例按钮",
        "api_endpoint": "/api/examples",
        "primary_tool": "paradigm_selector",
        "automation_level": "human_readable",
        "agent_boundary": "示例用于帮助人理解主干和范式入口；点击后仍必须经过完整路由、安全分流和工作台总览。",
        "proof_docs": ["web-ui/README.md", "知识库/07-问题到范式映射.md"],
        "verification_command": "curl http://127.0.0.1:8765/api/examples",
    },
    {
        "surface_id": "paradigm_selection",
        "display_name": "问题到范式",
        "user_surface": "范式面板",
        "api_endpoint": "/api/paradigm",
        "primary_tool": "paradigm_selector",
        "automation_level": "programmable_now",
        "agent_boundary": "可程序化给出范式、证据轨道和执行边界；最终表达仍需结合上下文。",
        "proof_docs": ["知识库/07-问题到范式映射.md"],
        "verification_command": "python3 agent-tools/scripts/paradigm_selector.py --text '帮我做一个塔罗三张牌，看看工作状态'",
    },
    {
        "surface_id": "consultation_packet",
        "display_name": "咨询工作单",
        "user_surface": "工作单面板",
        "api_endpoint": "/api/packet",
        "primary_tool": "consultation_packet_builder",
        "automation_level": "programmable_now",
        "agent_boundary": "工作单可自动生成；Agent 综合前必须检查结构化输入和复核清单。",
        "proof_docs": ["知识库/07-问题到范式映射.md", "知识库/Agent运行时交接包.md"],
        "verification_command": "python3 agent-tools/scripts/consultation_packet_builder.py --text '帮我做一个塔罗三张牌，看看工作状态'",
    },
    {
        "surface_id": "safe_execution_subset",
        "display_name": "安全执行子集",
        "user_surface": "安全执行面板",
        "api_endpoint": "/api/execute-safe",
        "primary_tool": "consultation_execution_runner",
        "automation_level": "safe_subset_programmable",
        "agent_boundary": "只运行确定、无副作用、安全白名单内的子步骤；领域工具和最终解读会标为 skipped/handoff。",
        "proof_docs": ["知识库/版本记录.md", "知识库/Agent运行时DryRun验证.md"],
        "verification_command": "python3 agent-tools/scripts/consultation_execution_runner.py --text '帮我做一个塔罗三张牌，看看工作状态'",
    },
    {
        "surface_id": "structured_tool_preview",
        "display_name": "结构化工具预览",
        "user_surface": "结构化输入面板",
        "api_endpoint": "/api/tool-preview",
        "primary_tool": "tarot_interpretation_planner / fengshui_space_checklist",
        "automation_level": "requires_user_fields",
        "agent_boundary": "UI 只对白名单工具生成预览；未知牌面、照片、盘式和模糊来源需要 Agent 或用户补字段。",
        "proof_docs": ["web-ui/README.md", "知识库/工具与Skill Manifest规范.md"],
        "verification_command": "curl -X POST http://127.0.0.1:8765/api/tool-preview -H 'Content-Type: application/json' -d '{\"mode\":\"fengshui\",\"payload\":{\"request_text\":\"卧室床对门，最近睡不好\",\"space_type\":\"bedroom\",\"space_description\":\"卧室床尾正对门\",\"observation_text\":\"卧室床尾正对门\",\"concerns\":[\"sleep\"]}}'",
    },
    {
        "surface_id": "agent_handoff",
        "display_name": "Agent 交接",
        "user_surface": "Agent 交接面板",
        "api_endpoint": "/api/handoff",
        "primary_tool": "consultation_handoff_builder",
        "automation_level": "agent_handoff_required",
        "agent_boundary": "把工作单、预览、草稿和 lint 合并；ready/rewrite/blocked 状态决定 Agent 或审校者下一步。",
        "proof_docs": ["知识库/Agent运行时交接包.md", "知识库/版本记录.md"],
        "verification_command": "python3 agent-tools/scripts/consultation_handoff_builder.py --text '帮我做一个塔罗三张牌，看看工作状态'",
    },
    {
        "surface_id": "case_recording",
        "display_name": "案例候选记录",
        "user_surface": "案例记录面板",
        "api_endpoint": "/api/case-record",
        "primary_tool": "consultation_case_recorder",
        "automation_level": "human_review_required",
        "agent_boundary": "可生成候选记录，但进入案例库需要回访、脱敏、lint 和人工审校同时通过。",
        "proof_docs": ["知识库/案例采集模板.md", "知识库/匿名真实对话验证流程.md"],
        "verification_command": "python3 agent-tools/scripts/consultation_case_recorder.py --text '帮我做一个塔罗三张牌，看看工作状态' --follow-up '两天后复盘：建议部分可用' --validation-result mixed --reviewer internal-reviewer",
    },
    {
        "surface_id": "evidence_matrix",
        "display_name": "证据矩阵",
        "user_surface": "证据矩阵面板",
        "api_endpoint": "/api/evidence-matrix",
        "primary_tool": "domain_evidence_matrix_builder",
        "automation_level": "programmable_now",
        "agent_boundary": "可程序化分类 61 领域的证据模式和神秘强度；不等于真实证据已经收齐。",
        "proof_docs": ["知识库/证据矩阵.md"],
        "verification_command": "python3 agent-tools/scripts/domain_evidence_matrix_builder.py --format markdown",
    },
    {
        "surface_id": "validation_backlog",
        "display_name": "验证 Backlog",
        "user_surface": "验证 Backlog 面板",
        "api_endpoint": "/api/validation-backlog",
        "primary_tool": "case_validation_backlog_builder",
        "automation_level": "programmable_now",
        "agent_boundary": "可生成采集队列；真实素材选择和审校优先级仍由维护者决定。",
        "proof_docs": ["知识库/案例验证Backlog.md"],
        "verification_command": "python3 agent-tools/scripts/case_validation_backlog_builder.py --priority P0 --limit 5",
    },
    {
        "surface_id": "validation_template",
        "display_name": "采集模板",
        "user_surface": "采集模板面板",
        "api_endpoint": "/api/validation-template",
        "primary_tool": "case_validation_template_builder",
        "automation_level": "requires_real_material",
        "agent_boundary": "模板可自动生成；真实案例、来源审计和边界反例必须脱敏、审校后才能沉淀。",
        "proof_docs": ["知识库/案例采集模板.md"],
        "verification_command": "python3 agent-tools/scripts/case_validation_template_builder.py --domain fengshui --format markdown",
    },
    {
        "surface_id": "interaction_surface_matrix",
        "display_name": "可用化矩阵",
        "user_surface": "可用化矩阵面板",
        "api_endpoint": "/api/interaction-surface-matrix",
        "primary_tool": "interaction_surface_matrix_builder",
        "automation_level": "programmable_now",
        "agent_boundary": "可程序化盘点 UI、API、工具和接管边界；仍需 smoke runner 验证真实 HTTP 行为。",
        "proof_docs": ["知识库/交互可用化矩阵.md", "知识库/WebUISurfaceSmoke验证.md"],
        "verification_command": "python3 agent-tools/scripts/interaction_surface_matrix_builder.py --format markdown",
    },
]


AUTOMATION_GROUPS = {
    "human_readable": "给人阅读和导航，不直接执行玄学流程。",
    "programmable_now": "可通过 CLI/API 稳定运行，输出结构化结果。",
    "safe_subset_programmable": "只运行安全白名单子集，并显式标出 skipped/handoff。",
    "requires_user_fields": "需要用户或 UI 补充结构化字段后运行。",
    "agent_handoff_required": "需要 Agent 综合、草稿或审校接管。",
    "human_review_required": "必须人工审校后才能进入正式知识库或案例库。",
    "requires_real_material": "需要真实脱敏材料或来源证据填充。",
}


def endpoint_present(server_text: str, endpoint: str) -> bool:
    return endpoint in server_text


def tool_script_exists(root: Path, primary_tool: str) -> bool:
    first_tool = primary_tool.split(" / ")[0].strip()
    return (root / "agent-tools" / "scripts" / f"{first_tool}.py").exists()


def enrich_surface(root: Path, server_text: str, surface: dict[str, Any]) -> dict[str, Any]:
    proof_docs = [
        {
            "path": path,
            "exists": (root / path).exists(),
        }
        for path in surface["proof_docs"]
    ]
    endpoint_exists = endpoint_present(server_text, surface["api_endpoint"])
    script_exists = tool_script_exists(root, surface["primary_tool"])
    is_valid = endpoint_exists and script_exists and all(item["exists"] for item in proof_docs)
    return {
        **surface,
        "endpoint_registered": endpoint_exists,
        "primary_script_exists": script_exists,
        "proof_docs": proof_docs,
        "is_valid": is_valid,
        "open_items": [
            item
            for item, passed in {
                "api_endpoint_registered": endpoint_exists,
                "primary_script_exists": script_exists,
                "proof_docs_exist": all(doc["exists"] for doc in proof_docs),
            }.items()
            if not passed
        ],
    }


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    server_path = root_path / "web-ui" / "server.py"
    server_text = server_path.read_text(encoding="utf-8") if server_path.exists() else ""
    surfaces = [enrich_surface(root_path, server_text, surface) for surface in SURFACES]
    automation_counts: dict[str, int] = {}
    for surface in surfaces:
        level = surface["automation_level"]
        automation_counts[level] = automation_counts.get(level, 0) + 1
    result = {
        "tool": "interaction_surface_matrix_builder",
        "root": str(root_path),
        "is_valid": all(surface["is_valid"] for surface in surfaces),
        "surface_count": len(surfaces),
        "api_endpoint_count": len({surface["api_endpoint"] for surface in surfaces if surface["api_endpoint"]}),
        "automation_counts": dict(sorted(automation_counts.items())),
        "surfaces": surfaces,
        "automation_groups": [
            {"automation_level": key, "description": value, "surface_count": automation_counts.get(key, 0)}
            for key, value in AUTOMATION_GROUPS.items()
            if automation_counts.get(key, 0)
        ],
        "limits": [
            "此矩阵证明入口、脚本和文档证据存在，不代表真实用户素材或专家审校已经完成。",
            "programmable_now 只表示本地工具可运行，不表示可以跳过安全分流、输出 lint 或人工审校。",
            "Web UI 是本地工作台，不包含远程托管、多用户鉴权或生产权限隔离。",
        ],
        "next_steps": [
            "use_matrix_to_choose_next_ui_or_runtime_gap",
            "rerun_web_ui_surface_smoke_runner_after_endpoint_changes",
            "add_real_material_to_requires_real_material_surfaces_before_claiming_case_coverage",
        ],
    }
    result["generated_markdown"] = render_markdown(result)
    return result


def render_count_map(values: dict[str, int]) -> str:
    return "、".join(f"`{key}` {value}" for key, value in values.items()) or "-"


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# 交互可用化矩阵",
        "",
        "本页把当前项目的给人入口、API、可程序化执行部分和 Agent/人工接管边界放在同一张表里。它用于判断下一步应该补 UI、补 runtime wrapper、补结构化字段，还是补真实案例/来源材料。",
        "",
        "## 摘要",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| Surface | {result['surface_count']} |",
        f"| API endpoint | {result['api_endpoint_count']} |",
        f"| 自动化等级 | {render_count_map(result['automation_counts'])} |",
        "",
        "## 自动化等级",
        "",
        "| 等级 | 数量 | 含义 |",
        "| --- | --- | --- |",
    ]
    for group in result["automation_groups"]:
        lines.append(f"| `{group['automation_level']}` | {group['surface_count']} | {group['description']} |")
    lines.extend(
        [
            "",
            "## Surface Matrix",
            "",
            "| Surface | 用户入口 | API | 工具 | 自动化等级 | Agent/人工边界 | 证据 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for surface in result["surfaces"]:
        docs = ", ".join(f"`{item['path']}`" for item in surface["proof_docs"])
        lines.append(
            f"| {surface['display_name']} | {surface['user_surface']} | `{surface['api_endpoint']}` | `{surface['primary_tool']}` | `{surface['automation_level']}` | {surface['agent_boundary']} | {docs} |"
        )
    lines.extend(["", "## 验证命令", ""])
    for surface in result["surfaces"]:
        lines.append(f"- {surface['display_name']}：`{surface['verification_command']}`")
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
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/交互可用化矩阵.md.")
    args = parser.parse_args()
    try:
        result = build(args.root)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "交互可用化矩阵.md"
        target.write_text(result["generated_markdown"], encoding="utf-8")
    if args.format == "markdown":
        print(result["generated_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
