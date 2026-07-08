"""Shared UI action manifest for Web UI and Agent handoff surfaces."""

from __future__ import annotations

from typing import Any


def ui_action(
    action: str,
    label: str,
    enabled: bool,
    reason: str,
    endpoint: str,
    surface_id: str,
) -> dict[str, Any]:
    return {
        "action": action,
        "label": label,
        "enabled": enabled,
        "status": "enabled" if enabled else "disabled",
        "reason": reason,
        "endpoint": endpoint,
        "surface_id": surface_id,
    }


def build_ui_actions(can_continue_mystic_workflow: bool) -> dict[str, dict[str, Any]]:
    can_continue = bool(can_continue_mystic_workflow)
    return {
        "execute": ui_action(
            "execute",
            "安全执行",
            True,
            "仅运行路由、范式和 intake 等安全白名单工具",
            "/api/execute-safe",
            "safe_execution_subset",
        ),
        "preview": ui_action(
            "preview",
            "结构化预览",
            can_continue,
            "补齐结构化输入后运行白名单领域工具" if can_continue else "风险暂停时不继续领域工具预览",
            "/api/tool-preview",
            "structured_tool_preview",
        ),
        "handoff": ui_action(
            "handoff",
            "Agent 交接",
            True,
            "生成 Agent 综合和审校交接包" if can_continue else "生成安全/专业边界交接包",
            "/api/handoff",
            "agent_handoff",
        ),
        "case": ui_action(
            "case",
            "案例候选",
            can_continue,
            "记录回访和审校状态作为候选案例" if can_continue else "风险暂停时不采集为普通案例",
            "/api/case-record",
            "case_recording",
        ),
    }
