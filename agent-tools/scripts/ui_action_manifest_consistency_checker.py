#!/usr/bin/env python3
"""Compare UI action manifests across Web UI, handoff, and runtime surfaces."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import agent_runtime_handoff_builder
import consultation_handoff_builder
from _ui_action_manifest import build_ui_actions


READY_REQUEST = "帮我做一个塔罗三张牌，看看工作状态"
PAUSED_REQUEST = "用塔罗看看我明天要不要贷款梭哈股票"
STATES = [
    {"state": "ready_to_continue", "request_text": READY_REQUEST, "expected": build_ui_actions(True)},
    {"state": "paused_for_boundary", "request_text": PAUSED_REQUEST, "expected": build_ui_actions(False)},
]


def load_web_ui_server(root: Path):
    server_path = root / "web-ui" / "server.py"
    spec = importlib.util.spec_from_file_location("mystic_web_ui_server_for_action_check", server_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {server_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def compare_manifest(actual: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if actual != expected:
        expected_actions = sorted(expected)
        actual_actions = sorted(actual)
        if actual_actions != expected_actions:
            errors.append(f"actions differ: expected {expected_actions}, got {actual_actions}")
        for action in expected_actions:
            if actual.get(action) != expected[action]:
                errors.append(f"{action} differs")
    return errors


def collect_sources(root: Path, web_server: Any, state: dict[str, Any], runtime: dict[str, Any]) -> list[dict[str, Any]]:
    request_text = state["request_text"]
    session = web_server.build_session({"request_text": request_text})
    handoff = consultation_handoff_builder.build({"request_text": request_text}, root=root)
    runtime_key = state["state"]
    return [
        {
            "source_id": "shared_helper",
            "surface": "shared_helper",
            "manifest": build_ui_actions(state["state"] == "ready_to_continue"),
        },
        {
            "source_id": "web_ui_session",
            "surface": "/api/session",
            "manifest": session["ui_actions"],
        },
        {
            "source_id": "consultation_handoff",
            "surface": "/api/handoff",
            "manifest": handoff["ui_actions"],
        },
        {
            "source_id": "runtime_handoff",
            "surface": "/api/runtime-handoff",
            "manifest": runtime["ui_action_manifests"][runtime_key],
        },
    ]


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    web_server = load_web_ui_server(root_path)
    with tempfile.TemporaryDirectory(prefix="mystic-action-manifest-") as codex_home:
        runtime = agent_runtime_handoff_builder.build(root=root_path, codex_home=codex_home)

    comparisons: list[dict[str, Any]] = []
    all_errors: list[str] = []
    for state in STATES:
        state_errors: list[str] = []
        sources = []
        for source in collect_sources(root_path, web_server, state, runtime):
            errors = compare_manifest(source["manifest"], state["expected"])
            if errors:
                state_errors.extend(f"{source['source_id']}: {error}" for error in errors)
            sources.append({**source, "matches_expected": not errors, "errors": errors})
        comparisons.append(
            {
                "state": state["state"],
                "request_text": state["request_text"],
                "expected_manifest": state["expected"],
                "sources": sources,
                "matches_all_sources": not state_errors,
                "errors": state_errors,
            }
        )
        all_errors.extend(f"{state['state']}: {error}" for error in state_errors)

    return {
        "tool": "ui_action_manifest_consistency_checker",
        "root": str(root_path),
        "is_valid": not all_errors,
        "state_count": len(comparisons),
        "source_count": sum(len(item["sources"]) for item in comparisons),
        "comparison_count": sum(len(item["sources"]) - 1 for item in comparisons),
        "comparisons": comparisons,
        "errors": all_errors,
        "limits": [
            "此检查验证 Web UI session、咨询 handoff 和 runtime handoff 的动作菜单一致，不替代真实浏览器视觉 QA。",
            "检查使用代表 ready/paused 请求，不覆盖所有领域文案变化。",
        ],
        "next_steps": [
            "rerun_after_action_manifest_changes",
            "keep_session_handoff_runtime_actions_in_sync",
            "add_browser_visual_qa_for_runtime_panel_when_browser_binary_is_available",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# UI Action Manifest 一致性验证",
        "",
        "本页比较 shared helper、Web UI session、咨询 handoff 和 runtime handoff 的动作菜单，防止 execute/preview/handoff/case 的启用状态、endpoint 或说明漂移。",
        "",
        "## 摘要",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 状态 | {result['state_count']} |",
        f"| 来源 | {result['source_count']} |",
        f"| 比较 | {result['comparison_count']} |",
        f"| 通过 | {result['is_valid']} |",
        "",
        "## 比较结果",
        "",
        "| State | Source | Matches | Enabled Actions | Disabled Actions | Errors |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in result["comparisons"]:
        for source in item["sources"]:
            enabled = [key for key, action in source["manifest"].items() if action["enabled"]]
            disabled = [key for key, action in source["manifest"].items() if not action["enabled"]]
            errors = "; ".join(source["errors"]) or "-"
            lines.append(
                f"| `{item['state']}` | `{source['source_id']}` | {source['matches_expected']} | {', '.join(enabled)} | {', '.join(disabled)} | {errors} |"
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
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/UIActionManifest一致性验证.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "UIActionManifest一致性验证.md"
        target.write_text(render_markdown(result), encoding="utf-8")
    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
