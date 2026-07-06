#!/usr/bin/env python3
"""Dry-run representative mystic requests through runtime routing contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import agent_route_smoke_runner
import agent_workflow_router
import tool_manifest_builder


def manifest_tool_status(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {tool["name"]: tool for tool in manifest.get("tools", [])}


def missing_runtime_assets(route: dict[str, Any], root: Path, tool_status: dict[str, dict[str, Any]]) -> list[str]:
    missing: list[str] = []
    for path in route.get("sop", []) + route.get("knowledge", []):
        if not (root / path).exists():
            missing.append(path)
    if route.get("skill_path") and not (root / route["skill_path"]).exists():
        missing.append(route["skill_path"])
    for tool in route.get("initial_tools", []):
        record = tool_status.get(tool)
        if not record or record.get("status") != "ready":
            missing.append(f"tool:{tool}")
    return missing


def evaluate_case(case: dict[str, Any], root: Path, tool_status: dict[str, dict[str, Any]]) -> dict[str, Any]:
    route = agent_workflow_router.route({"request_text": case["request_text"]}, root=root)
    missing_assets = missing_runtime_assets(route, root, tool_status)
    invariant_checks = {
        "route_matches_expected_status": route["route_status"] == case["expected_status"],
        "route_matches_expected_skill": route["skill"] == case["expected_skill"],
        "can_continue_matches_expected": route["can_continue_mystic_workflow"] == case["can_continue"],
        "initial_tools_exist": not missing_assets,
    }
    if route["can_continue_mystic_workflow"]:
        invariant_checks.update(
            {
                "has_skill": bool(route["skill"] and route["skill_path"]),
                "has_sop": bool(route["sop"]),
                "has_output_lint": "mystic_output_lint" in route["initial_tools"],
                "has_domain_tools": bool(route["domain_tools"]),
                "initial_tools_include_domain_tool": any(tool in route["initial_tools"] for tool in route["domain_tools"]),
            }
        )
    else:
        invariant_checks.update(
            {
                "no_domain_tools_in_initial_tools": all(tool not in route["initial_tools"] for tool in route["domain_tools"]),
                "only_intake_runs_before_pause": route["initial_tools"] == ["mystic_intake_triage"],
                "pause_next_step_present": any(step in route["next_steps"] for step in ["pause_workflow", "offer_safe_alternative_support"]),
            }
        )
    failed = [name for name, passed in invariant_checks.items() if not passed]
    return {
        "case_id": case["case_id"],
        "request_text": case["request_text"],
        "passed": not failed,
        "failed_checks": failed,
        "missing_assets": missing_assets,
        "route_status": route["route_status"],
        "domain": route["domain"],
        "skill": route["skill"],
        "can_continue_mystic_workflow": route["can_continue_mystic_workflow"],
        "initial_tools": route["initial_tools"],
        "next_steps": route["next_steps"],
        "invariant_checks": invariant_checks,
    }


def run(case_id: str | None = None, root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    manifest = tool_manifest_builder.build(root_path)
    tool_status = manifest_tool_status(manifest)
    selected_cases = agent_route_smoke_runner.ROUTE_CASES
    if case_id:
        selected_cases = [case for case in selected_cases if case["case_id"] == case_id]
        if not selected_cases:
            raise ValueError(f"unknown runtime dry-run case: {case_id}")
    results = [evaluate_case(case, root_path, tool_status) for case in selected_cases]
    failed = [result for result in results if not result["passed"]]
    ready_cases = [result for result in results if result["can_continue_mystic_workflow"]]
    paused_or_blocked_cases = [result for result in results if not result["can_continue_mystic_workflow"]]
    return {
        "tool": "agent_runtime_dry_run_runner",
        "root": str(root_path),
        "is_valid": bool(manifest["is_valid"]) and not failed,
        "case_count": len(results),
        "passed_count": len(results) - len(failed),
        "failed_count": len(failed),
        "ready_case_count": len(ready_cases),
        "paused_or_blocked_case_count": len(paused_or_blocked_cases),
        "case_ids": [result["case_id"] for result in results],
        "results": results,
        "runtime_invariants": [
            "ready_to_run_skill 路径必须有 Skill、SOP、领域工具和 mystic_output_lint。",
            "paused/blocked 路径只能先运行 mystic_intake_triage，不能继续领域工具。",
            "initial_tools 中的工具必须在 tool_manifest_builder 中为 ready。",
            "SOP、知识卡和 Skill 路径必须存在。",
        ],
        "limits": [
            "runtime dry-run 验证代表请求和工具契约，不执行真实多轮咨询。",
            "此验证不表示 Skill 已安装到真实 Codex home。",
            "真实用户表达和真实 transcript 仍需外部证据流程扩充。",
        ],
        "next_steps": [
            "wire_runtime_wrapper_to_agent_workflow_router",
            "run_again_after_tool_or_skill_changes",
            "pair_with_skill_replay_runner_and_skill_transcript_runner",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--case-id", help="Run one runtime dry-run case.")
    args = parser.parse_args()
    try:
        result = run(case_id=args.case_id, root=args.root)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
