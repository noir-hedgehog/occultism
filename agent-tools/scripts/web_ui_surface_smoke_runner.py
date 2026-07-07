#!/usr/bin/env python3
"""Run HTTP smoke checks against the local Web UI API surfaces."""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import interaction_surface_matrix_builder


REQUEST_TEXT = "帮我做一个塔罗三张牌，看看工作状态"


def json_payload(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def smoke_cases() -> list[dict[str, Any]]:
    return [
        {"case_id": "health", "surface_id": "health", "method": "GET", "path": "/api/health", "expected": {"ok": True}},
        {"case_id": "home", "surface_id": "home", "method": "GET", "path": "/", "content_type": "text/html", "expected_text": "玄学大典"},
        {"case_id": "docs_index", "surface_id": "knowledge_docs_site", "method": "GET", "path": "/api/docs", "expected": {"tool": "web_ui_doc_index"}},
        {
            "case_id": "docs_read",
            "surface_id": "knowledge_docs_site",
            "method": "GET",
            "path": "/api/docs?" + urlencode({"path": "知识库/交互可用化矩阵.md"}),
            "expected": {"tool": "web_ui_doc_reader", "path": "知识库/交互可用化矩阵.md"},
        },
        {
            "case_id": "summary",
            "surface_id": "summary",
            "method": "GET",
            "path": "/api/summary",
            "expected": {"project": "玄学大典 / Occultism Agent Toolkit"},
        },
        {
            "case_id": "examples",
            "surface_id": "example_presets",
            "method": "GET",
            "path": "/api/examples",
            "expected": {"tool": "web_ui_example_requests", "is_valid": True, "example_count": 6, "trunk_count": 6},
        },
        {
            "case_id": "evidence_matrix",
            "surface_id": "evidence_matrix",
            "method": "GET",
            "path": "/api/evidence-matrix",
            "expected": {"tool": "domain_evidence_matrix_builder", "domain_count": 61},
        },
        {
            "case_id": "validation_backlog",
            "surface_id": "validation_backlog",
            "method": "GET",
            "path": "/api/validation-backlog",
            "expected": {"tool": "case_validation_backlog_builder", "backlog_count": 61},
        },
        {
            "case_id": "validation_template",
            "surface_id": "validation_template",
            "method": "GET",
            "path": "/api/validation-template?domain=fengshui",
            "expected": {"tool": "case_validation_template_builder", "template_count": 1},
        },
        {
            "case_id": "interaction_surface_matrix",
            "surface_id": "interaction_surface_matrix",
            "method": "GET",
            "path": "/api/interaction-surface-matrix",
            "expected": {"tool": "interaction_surface_matrix_builder", "surface_count": 13},
        },
        {
            "case_id": "session",
            "surface_id": "request_router",
            "method": "POST",
            "path": "/api/session",
            "payload": {"request_text": REQUEST_TEXT},
            "expected": {
                "tool": "web_ui_session",
                "route_status": "ready_to_run_skill",
                "workbench_overview": {"mode": "guided_consultation_workbench"},
            },
        },
        {
            "case_id": "paradigm",
            "surface_id": "paradigm_selection",
            "method": "POST",
            "path": "/api/paradigm",
            "payload": {"request_text": REQUEST_TEXT},
            "expected": {"tool": "paradigm_selector"},
        },
        {
            "case_id": "packet",
            "surface_id": "consultation_packet",
            "method": "POST",
            "path": "/api/packet",
            "payload": {"request_text": REQUEST_TEXT},
            "expected": {"tool": "consultation_packet_builder"},
        },
        {
            "case_id": "execute_safe",
            "surface_id": "safe_execution_subset",
            "method": "POST",
            "path": "/api/execute-safe",
            "payload": {"request_text": REQUEST_TEXT},
            "expected": {"tool": "consultation_execution_runner"},
        },
        {
            "case_id": "tool_preview_fengshui",
            "surface_id": "structured_tool_preview",
            "method": "POST",
            "path": "/api/tool-preview",
            "payload": {
                "mode": "fengshui",
                "payload": {
                    "request_text": "卧室床对门，最近睡不好",
                    "space_type": "bedroom",
                    "space_description": "卧室床尾正对门，镜子在床侧，晚上容易被通知灯打扰。",
                    "observation_text": "卧室床尾正对门，镜子在床侧。",
                    "concerns": ["sleep", "pressure"],
                },
            },
            "expected": {"tool": "web_ui_tool_preview", "mode": "fengshui"},
        },
        {
            "case_id": "handoff",
            "surface_id": "agent_handoff",
            "method": "POST",
            "path": "/api/handoff",
            "payload": {
                "request_text": REQUEST_TEXT,
                "draft_output": "这只是工作状态反思：先整理事实和下一步，不保证结果。",
            },
            "expected": {"tool": "consultation_handoff_builder"},
        },
        {
            "case_id": "case_record",
            "surface_id": "case_recording",
            "method": "POST",
            "path": "/api/case-record",
            "payload": {
                "request_text": REQUEST_TEXT,
                "draft_output": "这只是工作状态反思：先整理事实和下一步，不保证结果。",
                "follow_up_text": "两天后复盘：建议有部分可用。",
                "validation_result": "mixed",
                "reviewer": "internal-reviewer",
            },
            "expected": {"tool": "consultation_case_recorder"},
        },
    ]


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def start_server(root: Path, port: int) -> subprocess.Popen[str]:
    return subprocess.Popen(
        [sys.executable, "web-ui/server.py", "--port", str(port)],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def wait_for_server(base_url: str, timeout_seconds: float) -> None:
    deadline = time.monotonic() + timeout_seconds
    last_error = ""
    while time.monotonic() < deadline:
        try:
            with urlopen(base_url + "/api/health", timeout=1) as response:
                if response.status == 200:
                    return
        except (OSError, HTTPError, URLError) as exc:
            last_error = str(exc)
        time.sleep(0.1)
    raise TimeoutError(f"server did not become ready: {last_error}")


def fetch_case(base_url: str, case: dict[str, Any], timeout_seconds: float) -> dict[str, Any]:
    url = base_url + case["path"]
    headers = {"Accept": "application/json"}
    data = None
    if case["method"] == "POST":
        data = json_payload(case.get("payload", {}))
        headers["Content-Type"] = "application/json"
    request = Request(url, data=data, headers=headers, method=case["method"])
    with urlopen(request, timeout=timeout_seconds) as response:
        raw = response.read()
        content_type = response.headers.get("Content-Type", "")
        text = raw.decode("utf-8")
        if "application/json" in content_type:
            body: Any = json.loads(text)
        else:
            body = text
        return {"status_code": response.status, "content_type": content_type, "body": body}


def matches_value(actual: Any, expected: Any, path: str) -> list[str]:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [f"{path}: expected object, got {type(actual).__name__}"]
        errors: list[str] = []
        for key, expected_value in expected.items():
            nested_path = f"{path}.{key}" if path else key
            errors.extend(matches_value(actual.get(key), expected_value, nested_path))
        return errors
    if actual != expected:
        return [f"{path}: expected {expected!r}, got {actual!r}"]
    return []


def matches_expected(body: Any, expected: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(body, dict):
        return ["response_body_not_json_object"]
    for key, expected_value in expected.items():
        errors.extend(matches_value(body.get(key), expected_value, key))
    return errors


def run_case(base_url: str, case: dict[str, Any], timeout_seconds: float) -> dict[str, Any]:
    errors: list[str] = []
    status_code = 0
    content_type = ""
    body_summary: dict[str, Any] = {}
    try:
        response = fetch_case(base_url, case, timeout_seconds)
        status_code = int(response["status_code"])
        content_type = str(response["content_type"])
        body = response["body"]
        if status_code != 200:
            errors.append(f"status_code_not_200:{status_code}")
        if case.get("expected"):
            errors.extend(matches_expected(body, case["expected"]))
        if case.get("expected_text") and str(case["expected_text"]) not in str(body):
            errors.append("expected_text_missing")
        if case.get("content_type") and str(case["content_type"]) not in content_type:
            errors.append("content_type_mismatch")
        if isinstance(body, dict):
            body_summary = {
                key: body.get(key)
                for key in (
                    "tool",
                    "is_valid",
                    "ok",
                    "project",
                    "route_status",
                    "domain",
                    "template_count",
                    "surface_count",
                    "backlog_count",
                    "domain_count",
                    "example_count",
                    "trunk_count",
                    "mode",
                )
                if key in body
            }
            if isinstance(body.get("workbench_overview"), dict):
                body_summary["workbench_mode"] = body["workbench_overview"].get("mode")
        else:
            body_summary = {"text_length": len(str(body))}
    except Exception as exc:
        errors.append(str(exc))
    return {
        "case_id": case["case_id"],
        "surface_id": case["surface_id"],
        "method": case["method"],
        "path": case["path"],
        "status_code": status_code,
        "content_type": content_type,
        "passed": not errors,
        "errors": errors,
        "body_summary": body_summary,
    }


def select_cases(case_ids: list[str] | None) -> list[dict[str, Any]]:
    cases = smoke_cases()
    if not case_ids:
        return cases
    wanted = set(case_ids)
    selected = [case for case in cases if case["case_id"] in wanted]
    missing = sorted(wanted - {case["case_id"] for case in selected})
    if missing:
        raise ValueError(f"unknown case_ids: {', '.join(missing)}")
    return selected


def build(root: str | Path = ".", case_ids: list[str] | None = None, timeout_seconds: float = 10.0) -> dict[str, Any]:
    root_path = Path(root).resolve()
    cases = select_cases(case_ids)
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    process = start_server(root_path, port)
    server_stdout = ""
    server_stderr = ""
    try:
        wait_for_server(base_url, timeout_seconds)
        results = [run_case(base_url, case, timeout_seconds) for case in cases]
    finally:
        process.terminate()
        try:
            server_stdout, server_stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            server_stdout, server_stderr = process.communicate(timeout=5)
    passed_count = sum(1 for result in results if result["passed"])
    surface_matrix = interaction_surface_matrix_builder.build(root_path)
    covered_surface_ids = sorted({result["surface_id"] for result in results if result["surface_id"] not in {"health", "home", "summary"}})
    matrix_surface_ids = sorted({surface["surface_id"] for surface in surface_matrix["surfaces"]})
    result = {
        "tool": "web_ui_surface_smoke_runner",
        "root": str(root_path),
        "base_url": base_url,
        "is_valid": passed_count == len(results),
        "case_count": len(results),
        "passed_count": passed_count,
        "failed_count": len(results) - passed_count,
        "covered_surface_ids": covered_surface_ids,
        "matrix_surface_count": surface_matrix["surface_count"],
        "matrix_surface_ids": matrix_surface_ids,
        "results": results,
        "server": {
            "returncode": process.returncode,
            "stdout_tail": server_stdout[-500:],
            "stderr_tail": server_stderr[-500:],
        },
        "limits": [
            "此 smoke runner 验证本地 HTTP surface 和代表 payload，不替代浏览器视觉 QA。",
            "通过 smoke 不代表真实素材、专家审校或生产托管已经完成。",
            "测试服务只绑定 127.0.0.1，并在运行结束后关闭。",
        ],
        "next_steps": [
            "run_browser_visual_qa_for_layout_changes",
            "rerun_web_ui_surface_smoke_runner_after_endpoint_changes",
            "extend_smoke_cases_when_new_api_surfaces_are_added",
        ],
    }
    result["generated_markdown"] = render_markdown(result)
    return result


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Web UI Surface Smoke 验证",
        "",
        "本页记录本地 Web UI/API surface 的 HTTP smoke 验证结果。它用于确认给人使用的入口和轻量 API 能用代表 payload 打通。",
        "",
        "## 摘要",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| Case | {result['passed_count']}/{result['case_count']} |",
        f"| Matrix surface | {len(result['covered_surface_ids'])}/{result['matrix_surface_count']} |",
        f"| Failed | {result['failed_count']} |",
        "",
        "## Cases",
        "",
        "| Case | Surface | Method | Path | Passed | Summary | Errors |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in result["results"]:
        summary = ", ".join(f"{key}={value}" for key, value in item["body_summary"].items()) or "-"
        errors = "; ".join(item["errors"]) or "-"
        lines.append(
            f"| `{item['case_id']}` | `{item['surface_id']}` | `{item['method']}` | `{item['path']}` | {item['passed']} | {summary} | {errors} |"
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
    parser.add_argument("--case-id", action="append", help="Run one smoke case id. Can be repeated.")
    parser.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout in seconds.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/WebUISurfaceSmoke验证.md.")
    args = parser.parse_args()
    try:
        result = build(args.root, case_ids=args.case_id, timeout_seconds=args.timeout)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "WebUISurfaceSmoke验证.md"
        target.write_text(result["generated_markdown"], encoding="utf-8")
    if args.format == "markdown":
        print(result["generated_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
