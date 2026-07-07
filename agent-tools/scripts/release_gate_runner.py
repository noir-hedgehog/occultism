#!/usr/bin/env python3
"""Run release-readiness gates for the mystic-agent knowledge base."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable


GateFn = Callable[[Path], dict[str, Any]]


def gate_result(
    gate_id: str,
    command: str,
    passed: bool,
    started: float,
    summary: dict[str, Any] | None = None,
    errors: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "command": command,
        "passed": passed,
        "duration_ms": int((time.perf_counter() - started) * 1000),
        "summary": summary or {},
        "errors": errors or [],
    }


def run_subprocess(root: Path, command: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=root, text=True, capture_output=True, timeout=timeout)


def gate_schema_json(root: Path) -> dict[str, Any]:
    started = time.perf_counter()
    schema_paths = sorted((root / "agent-tools/schemas").glob("*.json"))
    errors: list[str] = []
    for path in schema_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - defensive path
            errors.append(f"{path.relative_to(root)}: {exc}")
    return gate_result(
        "schema_json",
        "python3 -m json.tool agent-tools/schemas/*.json",
        not errors,
        started,
        {"schema_count": len(schema_paths)},
        errors,
    )


def gate_unittest(root: Path) -> dict[str, Any]:
    started = time.perf_counter()
    command = [sys.executable, "-m", "unittest", "discover", "-s", "agent-tools/tests"]
    completed = run_subprocess(root, command)
    output = completed.stdout + completed.stderr
    return gate_result(
        "unit_tests",
        "python3 -m unittest discover -s agent-tools/tests",
        completed.returncode == 0,
        started,
        {"returncode": completed.returncode, "tail": output[-1000:]},
        [] if completed.returncode == 0 else [output[-2000:]],
    )


def gate_json_script(root: Path, gate_id: str, script: str, expected_tool: str) -> dict[str, Any]:
    started = time.perf_counter()
    command = [sys.executable, f"agent-tools/scripts/{script}.py"]
    completed = run_subprocess(root, command)
    errors: list[str] = []
    summary: dict[str, Any] = {"returncode": completed.returncode}
    if completed.returncode != 0:
        errors.append((completed.stdout + completed.stderr)[-2000:])
    else:
        try:
            payload = json.loads(completed.stdout)
            summary.update(
                {
                    "tool": payload.get("tool", payload.get("suite", "")),
                    "is_valid": payload.get("is_valid"),
                }
            )
            if expected_tool and payload.get("tool", payload.get("suite")) != expected_tool:
                errors.append(f"expected tool/suite {expected_tool}")
            if payload.get("is_valid") is False:
                errors.append("script returned is_valid=false")
        except Exception as exc:
            errors.append(f"invalid JSON output: {exc}")
    return gate_result(gate_id, " ".join(command).replace(sys.executable, "python3"), not errors, started, summary, errors)


def gate_codex_skill_validator(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "codex_skill_blueprint_validator", "codex_skill_blueprint_validator", "codex_skill_blueprint_validator")


def gate_codex_skill_installer(root: Path) -> dict[str, Any]:
    started = time.perf_counter()
    command = [
        sys.executable,
        "agent-tools/scripts/codex_skill_installer.py",
        "--codex-home",
        str(root / ".release-gate-codex-home"),
    ]
    completed = run_subprocess(root, command)
    errors: list[str] = []
    summary: dict[str, Any] = {"returncode": completed.returncode}
    if completed.returncode != 0:
        errors.append((completed.stdout + completed.stderr)[-2000:])
    else:
        try:
            payload = json.loads(completed.stdout)
            summary.update(
                {
                    "tool": payload.get("tool"),
                    "is_valid": payload.get("is_valid"),
                    "dry_run": payload.get("dry_run"),
                    "skill_count": payload.get("skill_count"),
                }
            )
            if payload.get("tool") != "codex_skill_installer":
                errors.append("expected tool codex_skill_installer")
            if payload.get("is_valid") is False:
                errors.append("installer dry-run returned is_valid=false")
            if payload.get("dry_run") is not True:
                errors.append("installer gate must be dry-run")
        except Exception as exc:
            errors.append(f"invalid JSON output: {exc}")
    return gate_result(
        "codex_skill_installer",
        "python3 agent-tools/scripts/codex_skill_installer.py --codex-home .release-gate-codex-home",
        not errors,
        started,
        summary,
        errors,
    )


def gate_knowledge_coverage(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "knowledge_coverage_audit", "knowledge_coverage_audit", "knowledge_coverage_audit")


def gate_external_evidence_intake(root: Path) -> dict[str, Any]:
    started = time.perf_counter()
    command = [
        sys.executable,
        "agent-tools/scripts/external_evidence_intake_builder.py",
        "--codex-home",
        str(root / ".release-gate-codex-home"),
    ]
    completed = run_subprocess(root, command)
    errors: list[str] = []
    summary: dict[str, Any] = {"returncode": completed.returncode}
    if completed.returncode != 0:
        errors.append((completed.stdout + completed.stderr)[-2000:])
    else:
        try:
            payload = json.loads(completed.stdout)
            summary.update(
                {
                    "tool": payload.get("tool"),
                    "is_valid": payload.get("is_valid"),
                    "status": payload.get("status"),
                    "intake_count": payload.get("intake_count"),
                    "open_intake_count": payload.get("open_intake_count"),
                }
            )
            if payload.get("tool") != "external_evidence_intake_builder":
                errors.append("expected tool external_evidence_intake_builder")
            if payload.get("is_valid") is False:
                errors.append("external evidence intake builder returned is_valid=false")
        except Exception as exc:
            errors.append(f"invalid JSON output: {exc}")
    return gate_result(
        "external_evidence_intake_builder",
        "python3 agent-tools/scripts/external_evidence_intake_builder.py --codex-home .release-gate-codex-home",
        not errors,
        started,
        summary,
        errors,
    )


def gate_agent_runtime_handoff(root: Path) -> dict[str, Any]:
    started = time.perf_counter()
    command = [
        sys.executable,
        "agent-tools/scripts/agent_runtime_handoff_builder.py",
        "--codex-home",
        str(root / ".release-gate-codex-home"),
    ]
    completed = run_subprocess(root, command)
    errors: list[str] = []
    summary: dict[str, Any] = {"returncode": completed.returncode}
    if completed.returncode != 0:
        errors.append((completed.stdout + completed.stderr)[-2000:])
    else:
        try:
            payload = json.loads(completed.stdout)
            summary.update(
                {
                    "tool": payload.get("tool"),
                    "is_valid": payload.get("is_valid"),
                    "handoff_status": payload.get("handoff_status"),
                    "skill_count": payload.get("skill_count"),
                    "tool_count": payload.get("tool_count"),
                    "open_external_count": len(payload.get("open_external_items", [])),
                }
            )
            if payload.get("tool") != "agent_runtime_handoff_builder":
                errors.append("expected tool agent_runtime_handoff_builder")
            if payload.get("is_valid") is False:
                errors.append("agent runtime handoff returned is_valid=false")
        except Exception as exc:
            errors.append(f"invalid JSON output: {exc}")
    return gate_result(
        "agent_runtime_handoff_builder",
        "python3 agent-tools/scripts/agent_runtime_handoff_builder.py --codex-home .release-gate-codex-home",
        not errors,
        started,
        summary,
        errors,
    )


def gate_web_ui_surface_smoke(root: Path) -> dict[str, Any]:
    started = time.perf_counter()
    command = [sys.executable, "agent-tools/scripts/web_ui_surface_smoke_runner.py"]
    completed = run_subprocess(root, command, timeout=60)
    errors: list[str] = []
    summary: dict[str, Any] = {"returncode": completed.returncode}
    if completed.returncode != 0:
        errors.append((completed.stdout + completed.stderr)[-2000:])
    else:
        try:
            payload = json.loads(completed.stdout)
            summary.update(
                {
                    "tool": payload.get("tool"),
                    "is_valid": payload.get("is_valid"),
                    "case_count": payload.get("case_count"),
                    "passed_count": payload.get("passed_count"),
                    "failed_count": payload.get("failed_count"),
                    "covered_surface_count": len(payload.get("covered_surface_ids", [])),
                    "matrix_surface_count": payload.get("matrix_surface_count"),
                }
            )
            if payload.get("tool") != "web_ui_surface_smoke_runner":
                errors.append("expected tool web_ui_surface_smoke_runner")
            if payload.get("is_valid") is False:
                errors.append("web ui surface smoke returned is_valid=false")
        except Exception as exc:
            errors.append(f"invalid JSON output: {exc}")
    return gate_result(
        "web_ui_surface_smoke_runner",
        "python3 agent-tools/scripts/web_ui_surface_smoke_runner.py",
        not errors,
        started,
        summary,
        errors,
    )


def gate_agent_runtime_dry_run(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "agent_runtime_dry_run_runner", "agent_runtime_dry_run_runner", "agent_runtime_dry_run_runner")


def gate_agent_tool_wrapper_manifest(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "agent_tool_wrapper_manifest_builder", "agent_tool_wrapper_manifest_builder", "agent_tool_wrapper_manifest_builder")


def gate_agent_tool_definition_export(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "agent_tool_definition_exporter", "agent_tool_definition_exporter", "agent_tool_definition_exporter")


def gate_agent_tool_definition_validation(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "agent_tool_definition_validator", "agent_tool_definition_validator", "agent_tool_definition_validator")


def gate_agent_tool_registry(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "agent_tool_registry_builder", "agent_tool_registry_builder", "agent_tool_registry_builder")


def gate_agent_tool_registry_validation(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "agent_tool_registry_validator", "agent_tool_registry_validator", "agent_tool_registry_validator")


def gate_skill_replay(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "skill_replay_runner", "skill_replay_runner", "skill_replay_runner")


def gate_skill_transcript(root: Path) -> dict[str, Any]:
    return gate_json_script(root, "skill_transcript_runner", "skill_transcript_runner", "skill_transcript_runner")


def gate_markdown_links(root: Path) -> dict[str, Any]:
    started = time.perf_counter()
    import re

    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    missing: list[str] = []
    checked = 0
    for path in root.rglob("*.md"):
        if any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        checked += 1
        text = path.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "app://")):
                continue
            target_path = target.split("#", 1)[0].strip("<>")
            if not target_path:
                continue
            if not (path.parent / target_path).resolve().exists():
                missing.append(f"{path.relative_to(root)} -> {target}")
    return gate_result(
        "markdown_links",
        "README 本地链接检查",
        not missing,
        started,
        {"markdown_file_count": checked},
        missing,
    )


GATES: list[tuple[str, GateFn]] = [
    ("schema_json", gate_schema_json),
    ("codex_skill_blueprint_validator", gate_codex_skill_validator),
    ("codex_skill_installer", gate_codex_skill_installer),
    ("knowledge_coverage_audit", gate_knowledge_coverage),
    ("external_evidence_intake_builder", gate_external_evidence_intake),
    ("agent_runtime_dry_run_runner", gate_agent_runtime_dry_run),
    ("agent_tool_wrapper_manifest_builder", gate_agent_tool_wrapper_manifest),
    ("agent_tool_definition_exporter", gate_agent_tool_definition_export),
    ("agent_tool_definition_validator", gate_agent_tool_definition_validation),
    ("agent_tool_registry_builder", gate_agent_tool_registry),
    ("agent_tool_registry_validator", gate_agent_tool_registry_validation),
    ("agent_runtime_handoff_builder", gate_agent_runtime_handoff),
    ("web_ui_surface_smoke_runner", gate_web_ui_surface_smoke),
    ("skill_replay_runner", gate_skill_replay),
    ("skill_transcript_runner", gate_skill_transcript),
    ("markdown_links", gate_markdown_links),
    ("unit_tests", gate_unittest),
]


def run(root: str | Path = ".", gates: list[str] | None = None) -> dict[str, Any]:
    root_path = Path(root).resolve()
    selected = set(gates or [gate_id for gate_id, _ in GATES])
    unknown = sorted(selected - {gate_id for gate_id, _ in GATES})
    if unknown:
        raise ValueError(f"unknown release gate(s): {', '.join(unknown)}")

    started = time.perf_counter()
    results = [gate_fn(root_path) for gate_id, gate_fn in GATES if gate_id in selected]
    failed = [item for item in results if not item["passed"]]
    return {
        "tool": "release_gate_runner",
        "root": str(root_path),
        "gate_count": len(results),
        "passed_count": len(results) - len(failed),
        "failed_count": len(failed),
        "is_valid": not failed,
        "gates": results,
        "duration_ms": int((time.perf_counter() - started) * 1000),
        "limits": [
            "发布验收只证明当前自动质量门通过，不代表真实匿名 transcript 已经扩充完成。",
            "Skill 仍需在迁移到真实环境前做人工前向测试。",
            "覆盖度和静态验证不替代内容专家对派别差异的审校。",
        ],
        "next_steps": [
            "review_failed_gates_if_any",
            "update_dashboard_quality_gate_results",
            "forward_test_skills_before_installation",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to validate.")
    parser.add_argument("--gate", action="append", choices=[gate_id for gate_id, _ in GATES], help="Run only this gate. Can be repeated.")
    args = parser.parse_args()
    try:
        result = run(args.root, args.gate)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
