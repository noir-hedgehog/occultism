#!/usr/bin/env python3
"""Local web UI and lightweight API for the mystic-agent knowledge base."""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = Path(__file__).resolve().parent / "static"
SCRIPTS_DIR = ROOT / "agent-tools" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import agent_workflow_router  # noqa: E402
import agent_runtime_dry_run_runner  # noqa: E402
import case_validation_backlog_builder  # noqa: E402
import case_validation_template_builder  # noqa: E402
import consultation_case_recorder  # noqa: E402
import consultation_execution_runner  # noqa: E402
import consultation_handoff_builder  # noqa: E402
import consultation_packet_builder  # noqa: E402
import domain_evidence_matrix_builder  # noqa: E402
import fengshui_observation_recorder  # noqa: E402
import fengshui_space_checklist  # noqa: E402
import interaction_surface_matrix_builder  # noqa: E402
import knowledge_coverage_audit  # noqa: E402
import paradigm_selector  # noqa: E402
import tarot_interpretation_planner  # noqa: E402
import tool_manifest_builder  # noqa: E402
from _ui_action_manifest import build_ui_actions  # noqa: E402


TRUNKS = [
    {
        "id": "decision",
        "title": "占问与决策框架",
        "domains": [
            "tarot",
            "yijing",
            "liuyao",
            "meihua",
            "qimen",
            "mingli",
            "astrology",
            "date_selection",
            "naming",
            "numerology",
            "nine_star_ki",
            "human_design",
        ],
    },
    {
        "id": "symbolic_media",
        "title": "随机媒介与符号读取",
        "domains": [
            "oracle_lot",
            "oracle_card",
            "cartomancy",
            "dice",
            "tasseography",
            "lenormand",
            "rune",
            "pendulum",
            "western_geomancy",
            "casting_lots",
            "scrying",
            "character_divination",
            "bibliomancy",
            "sigil",
        ],
    },
    {
        "id": "space_environment",
        "title": "空间、环境与居住体验",
        "domains": [
            "fengshui",
            "ritual",
            "sound_cleansing",
            "aroma",
            "herbal",
            "crystal",
            "talisman",
            "consecration",
            "lost_object",
            "dowsing",
        ],
    },
    {
        "id": "ritual_objects",
        "title": "仪式、象征物与护持叙事",
        "domains": [
            "spiritual_protection",
            "deity_ancestor",
            "manifestation",
            "wealth_luck",
            "relationship_luck",
            "candle",
            "incense",
            "flower",
            "color",
            "zodiac",
        ],
    },
    {
        "id": "body_mind",
        "title": "身体、睡眠、梦境与心理叙事",
        "domains": [
            "dream",
            "sleep_paralysis",
            "body_omen",
            "aura_chakra",
            "physiognomy",
            "spirit_message",
            "past_life",
            "psychometry",
            "pet_communication",
        ],
    },
    {
        "id": "folk_omens",
        "title": "民俗、时令与征兆",
        "domains": [
            "folk_custom",
            "moon_phase",
            "planetary_retrograde",
            "animal_omen",
            "sky_omen",
            "synchronicity",
        ],
    },
]


EXAMPLE_REQUESTS = [
    {
        "id": "tarot_work_reflection",
        "trunk_id": "decision",
        "title": "塔罗工作状态",
        "request_text": "帮我做一个塔罗三张牌，看看最近工作状态和下一步",
        "requested_domain": "tarot",
        "expected_paradigm": "decision_reflection",
    },
    {
        "id": "rune_project_signal",
        "trunk_id": "symbolic_media",
        "title": "符文项目提示",
        "request_text": "我抽到三枚卢恩符文，想把它当作项目沟通的象征反思",
        "requested_domain": "rune",
        "expected_paradigm": "symbolic_media",
    },
    {
        "id": "fengshui_sleep_audit",
        "trunk_id": "space_environment",
        "title": "卧室睡眠风水",
        "request_text": "卧室床尾对门，镜子在床侧，最近睡不好，想从风水和现实环境一起看看",
        "requested_domain": "fengshui",
        "expected_paradigm": "practical_audit",
    },
    {
        "id": "protection_boundary",
        "trunk_id": "ritual_objects",
        "title": "能量防护边界",
        "request_text": "我总觉得被别人影响，想做一个低风险的能量防护和边界整理",
        "requested_domain": "spiritual_protection",
        "expected_paradigm": "symbolic_reflection",
    },
    {
        "id": "sleep_paralysis_support",
        "trunk_id": "body_mind",
        "title": "鬼压床安定",
        "request_text": "最近睡前容易鬼压床和害怕，想要一个不吓人的睡前安定流程",
        "requested_domain": "sleep_paralysis",
        "expected_paradigm": "somatic_reflection",
    },
    {
        "id": "synchronicity_record",
        "trunk_id": "folk_omens",
        "title": "重复数字记录",
        "request_text": "这几天总看到 11:11，想记录一下它对我当前计划的象征提醒",
        "requested_domain": "synchronicity",
        "expected_paradigm": "cultural_omen",
    },
]


def first_heading(path: Path) -> str:
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def relative_doc(path: str) -> dict[str, str]:
    if not path:
        return {"path": "", "title": ""}
    full = ROOT / path
    return {"path": path, "title": first_heading(full)}


def shell_command(parts: list[str]) -> str:
    def quote(value: str) -> str:
        if not value:
            return "''"
        safe = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./:-=")
        if all(char in safe for char in value):
            return value
        return "'" + value.replace("'", "'\"'\"'") + "'"

    return " ".join(quote(part) for part in parts)


def tool_command(tool: str, request_text: str) -> str:
    script = f"agent-tools/scripts/{tool}.py"
    if tool == "mystic_intake_triage":
        return shell_command(["python3", script, "--text", request_text])
    if tool == "agent_workflow_router":
        return shell_command(["python3", script, "--text", request_text])
    if tool == "paradigm_selector":
        return shell_command(["python3", script, "--text", request_text])
    if tool == "mystic_output_lint":
        return shell_command(["python3", script, "--text", "<draft output>"])
    return shell_command(["python3", script, "--help"])


def domain_names() -> dict[str, str]:
    audit = knowledge_coverage_audit.audit(ROOT)
    return {item["domain"]: item["display_name"] for item in audit["domains"]}


def build_summary() -> dict[str, Any]:
    audit = knowledge_coverage_audit.audit(ROOT)
    manifest = tool_manifest_builder.build(ROOT)
    dry_run = agent_runtime_dry_run_runner.run(root=ROOT)
    names = {item["domain"]: item["display_name"] for item in audit["domains"]}
    trunks = []
    for trunk in TRUNKS:
        trunks.append(
            {
                "id": trunk["id"],
                "title": trunk["title"],
                "domains": [
                    {"domain": domain, "display_name": names.get(domain, domain)}
                    for domain in trunk["domains"]
                    if domain in names
                ],
            }
        )
    return {
        "project": "玄学大典 / Occultism Agent Toolkit",
        "description": "A safety-first occultism knowledge base, toolchain, Codex Skill blueprint set, and local UI for symbolic consultation agents.",
        "goal": "从知识库、Skill 和 agent-tools 原型推进到可交互、可审计、可发布的本地 agent 工作台。",
        "metrics": {
            "domains": audit["domain_count"],
            "complete_domains": audit["complete_domain_count"],
            "skills": manifest["skill_count"],
            "tools": manifest["tool_count"],
            "dry_run_cases": dry_run["case_count"],
            "ready_cases": dry_run["ready_case_count"],
            "paused_or_blocked_cases": dry_run["paused_or_blocked_case_count"],
        },
        "trunks": trunks,
        "entry_docs": [
            relative_doc("知识库/项目目标.md"),
            relative_doc("知识库/03-主干生成发展史.md"),
            relative_doc("知识库/06-体系盘点与主干路线.md"),
            relative_doc("知识库/07-问题到范式映射.md"),
            relative_doc("知识库/证据矩阵.md"),
            relative_doc("知识库/案例验证Backlog.md"),
            relative_doc("知识库/案例采集模板.md"),
            relative_doc("知识库/交互可用化矩阵.md"),
            relative_doc("知识库/看板.md"),
            relative_doc("知识库/仪表盘.md"),
            relative_doc("知识库/Agent运行时交接包.md"),
            relative_doc("知识库/SOP-Tool-Skill追踪矩阵.md"),
        ],
        "limits": [
            "当前 UI 是本地工作台，不是公开托管产品。",
            "API 只做路由、上下文和命令建议，不执行任意 shell 命令。",
            "orange/red 风险必须暂停玄学流程。",
        ],
    }


def build_examples() -> dict[str, Any]:
    trunk_titles = {trunk["id"]: trunk["title"] for trunk in TRUNKS}
    names = domain_names()
    examples = []
    for example in EXAMPLE_REQUESTS:
        payload = {
            "request_text": example["request_text"],
            "requested_domain": example["requested_domain"],
        }
        route = agent_workflow_router.route(payload, root=ROOT)
        paradigm = paradigm_selector.select(payload, root=ROOT)
        expected_matches = (
            route["domain"] == example["requested_domain"]
            and paradigm["trunk"]["id"] == example["trunk_id"]
            and paradigm["recommended_paradigm"]["id"] == example["expected_paradigm"]
        )
        examples.append(
            {
                **example,
                "trunk_title": trunk_titles.get(example["trunk_id"], example["trunk_id"]),
                "domain_display_name": names.get(example["requested_domain"], example["requested_domain"]),
                "route_status": route["route_status"],
                "risk_level": route["risk_level"],
                "actual_domain": route["domain"],
                "actual_paradigm": paradigm["recommended_paradigm"]["id"],
                "expected_matches": expected_matches,
            }
        )
    is_valid = all(example["expected_matches"] for example in examples)
    return {
        "tool": "web_ui_example_requests",
        "is_valid": is_valid,
        "example_count": len(examples),
        "trunk_count": len({example["trunk_id"] for example in examples}),
        "examples": examples,
        "limits": [
            "示例请求只用于试运行和理解范式，不代表真实案例已经验证。",
            "点击示例仍需经过完整路由、安全分流和工作台总览。",
        ],
    }


def build_session(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", "")).strip()
    if not text:
        raise ValueError("request_text is required")
    route_payload = {"request_text": text}
    if payload.get("requested_domain"):
        route_payload["requested_domain"] = str(payload["requested_domain"])
    route = agent_workflow_router.route(route_payload, root=ROOT)
    paradigm = paradigm_selector.select(route_payload, root=ROOT)
    packet = consultation_packet_builder.build(route_payload, root=ROOT)
    names = domain_names()
    context = {
        "skill": relative_doc(route.get("skill_path", "")),
        "sop": [relative_doc(path) for path in route.get("sop", [])],
        "knowledge": [relative_doc(path) for path in route.get("knowledge", [])],
    }
    commands = [
        {
            "tool": "paradigm_selector",
            "command": tool_command("paradigm_selector", text),
            "runs_now": True,
        },
    ]
    commands.extend(
        [
        {
            "tool": tool,
            "command": tool_command(tool, text),
            "runs_now": tool in {"mystic_intake_triage", "agent_workflow_router"},
        }
        for tool in route.get("initial_tools", [])
        ]
    )
    if route["route_status"] == "ready_to_run_skill":
        workflow_steps = [
            {"step": "route", "status": "done", "label": "识别流派、意图和风险"},
            {"step": "load_context", "status": "next", "label": "读取 Skill、SOP 和知识卡"},
            {"step": "run_tools", "status": "next", "label": "按 initial_tools 执行可用工具"},
            {"step": "lint_output", "status": "next", "label": "输出前做安全措辞检查"},
        ]
    else:
        workflow_steps = [
            {"step": "route", "status": "done", "label": "识别流派、意图和风险"},
            {"step": "pause", "status": "next", "label": "暂停玄学流程，给出安全或专业边界"},
        ]
    domain_display_name = names.get(route["domain"], route["domain"])
    ui_actions = build_ui_actions(route["can_continue_mystic_workflow"])
    return {
        "tool": "web_ui_session",
        "is_valid": bool(route["is_valid"]),
        "request_text": text,
        "domain": route["domain"],
        "domain_display_name": domain_display_name,
        "intent": route["intent"],
        "risk_level": route["risk_level"],
        "route_status": route["route_status"],
        "can_continue_mystic_workflow": route["can_continue_mystic_workflow"],
        "risk_signals": route["risk_signals"],
        "required_clarifications": route["required_clarifications"],
        "allowed_next_steps": route["allowed_next_steps"],
        "agent_instructions": route["agent_instructions"],
        "workflow_steps": workflow_steps,
        "paradigm": paradigm,
        "packet": packet,
        "ui_actions": ui_actions,
        "workbench_overview": build_workbench_overview(route, paradigm, packet, domain_display_name),
        "context": context,
        "initial_tool_commands": commands,
        "raw_route": route,
    }

def doc_index(query: str = "") -> dict[str, Any]:
    docs = []
    normalized_query = query.strip().casefold()
    for path in sorted((ROOT / "知识库").rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        docs.append(
            {
                "path": rel,
                "title": first_heading(path),
                "section": path.relative_to(ROOT / "知识库").parts[0] if len(path.relative_to(ROOT / "知识库").parts) > 1 else "知识库",
            }
        )
    docs.extend(
        [
            {"path": "README.md", "title": first_heading(ROOT / "README.md"), "section": "项目"},
            {"path": "web-ui/README.md", "title": first_heading(ROOT / "web-ui/README.md"), "section": "项目"},
            {"path": "agent-tools/README.md", "title": first_heading(ROOT / "agent-tools/README.md"), "section": "项目"},
        ]
    )
    total_count = len(docs)
    if normalized_query:
        docs = [
            doc
            for doc in docs
            if normalized_query in f"{doc['path']} {doc['title']} {doc['section']}".casefold()
        ]
    return {
        "tool": "web_ui_doc_index",
        "query": query.strip(),
        "count": len(docs),
        "total_count": total_count,
        "docs": docs,
    }


def read_doc(path: str) -> dict[str, Any]:
    if not path or "\x00" in path:
        raise ValueError("path is required")
    target = (ROOT / path).resolve()
    if ROOT.resolve() not in target.parents and target != ROOT.resolve():
        raise ValueError("path must stay inside repository")
    if target.suffix != ".md":
        raise ValueError("only markdown documents can be read")
    if not target.exists() or not target.is_file():
        raise ValueError("document not found")
    rel = target.relative_to(ROOT).as_posix()
    content = target.read_text(encoding="utf-8")
    return {
        "tool": "web_ui_doc_reader",
        "path": rel,
        "title": first_heading(target),
        "content": content,
        "line_count": len(content.splitlines()),
    }


def build_tool_preview(payload: dict[str, Any]) -> dict[str, Any]:
    mode = str(payload.get("mode", "")).strip()
    tool_payload = payload.get("payload", {})
    if not isinstance(tool_payload, dict):
        raise ValueError("payload must be an object")
    if mode == "tarot":
        result = tarot_interpretation_planner.plan(tool_payload)
        tool_name = "tarot_interpretation_planner"
    elif mode == "fengshui":
        observation = fengshui_observation_recorder.record(tool_payload)
        checklist = fengshui_space_checklist.build_checklist(tool_payload)
        result = {"observation_record": observation, "space_checklist": checklist}
        tool_name = "fengshui_observation_recorder+fengshui_space_checklist"
    else:
        raise ValueError("mode must be tarot or fengshui")
    return {
        "tool": "web_ui_tool_preview",
        "mode": mode,
        "tool_name": tool_name,
        "is_valid": bool(result.get("is_valid", True)) if isinstance(result, dict) else True,
        "input_payload": tool_payload,
        "result": result,
        "limits": [
            "工具预览只运行白名单内的结构化函数，不执行任意 shell 命令。",
            "预览结果仍需 Agent 按 SOP 综合，并在输出前执行或等价执行 mystic_output_lint。",
        ],
    }


def build_workbench_overview(
    route: dict[str, Any],
    paradigm: dict[str, Any],
    packet: dict[str, Any],
    domain_display_name: str,
) -> dict[str, Any]:
    runnable_tools = [item for item in packet["tool_chain"] if item["execution_status"] == "runnable_now"]
    structured_tools = [item for item in packet["tool_chain"] if item["execution_status"] == "requires_structured_input"]
    draft_tools = [item for item in packet["tool_chain"] if item["execution_status"] == "requires_draft_output"]
    agent_steps = [
        step
        for step in packet["workflow_steps"]
        if step["status"] in {"agent", "required", "recommended", "next"}
    ]
    if route["can_continue_mystic_workflow"]:
        next_actions = [
            "运行安全子集，先完成可自动化的路由和范式步骤。",
            "补齐结构化输入，再运行对应领域工具预览。",
            "由 Agent 读取上下文并综合象征层、现实约束和低风险行动。",
            "输出前运行或人工等价执行 mystic_output_lint。",
        ]
    else:
        next_actions = [
            "暂停占卜、仪式或排盘流程。",
            "解释安全或专业边界，并保留低风险替代支持。",
            "只运行 intake/route 等安全工具，不生成确定性玄学结论。",
        ]
    return {
        "mode": "guided_consultation_workbench",
        "title": f"{domain_display_name} · {paradigm['recommended_paradigm']['title']}",
        "trunk": paradigm["trunk"],
        "question_type": paradigm["question_type"],
        "automation_mode": paradigm["execution_boundary"]["automation_mode"],
        "risk_level": route["risk_level"],
        "route_status": route["route_status"],
        "counts": {
            "runnable_tools": len(runnable_tools),
            "structured_input_tools": len(structured_tools),
            "draft_required_tools": len(draft_tools),
            "agent_or_review_steps": len(agent_steps),
            "context_docs": len(packet["context_docs"]),
        },
        "machine_runnable": runnable_tools,
        "needs_structured_input": structured_tools,
        "agent_handoff_steps": agent_steps,
        "required_docs": packet["context_docs"][:6],
        "next_actions": next_actions,
    }


class MysticUIHandler(BaseHTTPRequestHandler):
    server_version = "MysticUI/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))

    def send_json(self, data: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_static(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        if not raw:
            return {}
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object")
        return payload

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        try:
            if path == "/api/health":
                self.send_json({"ok": True, "root": str(ROOT)})
            elif path == "/api/summary":
                self.send_json(build_summary())
            elif path == "/api/examples":
                self.send_json(build_examples())
            elif path == "/api/evidence-matrix":
                self.send_json(domain_evidence_matrix_builder.build(ROOT))
            elif path == "/api/validation-backlog":
                self.send_json(case_validation_backlog_builder.build(ROOT))
            elif path == "/api/validation-template":
                query = parse_qs(parsed.query)
                limit_values = query.get("limit", [])
                self.send_json(
                    case_validation_template_builder.build(
                        ROOT,
                        domain=(query.get("domain", [""])[0] or None),
                        backlog_id=(query.get("backlog_id", [""])[0] or None),
                        priority=(query.get("priority", [""])[0] or None),
                        limit=int(limit_values[0]) if limit_values and limit_values[0] else None,
                    )
                )
            elif path == "/api/interaction-surface-matrix":
                self.send_json(interaction_surface_matrix_builder.build(ROOT))
            elif path == "/api/docs":
                query = parse_qs(parsed.query)
                if query.get("path"):
                    self.send_json(read_doc(query["path"][0]))
                else:
                    self.send_json(doc_index(query.get("q", [""])[0]))
            elif path == "/" or path == "/index.html":
                self.send_static(STATIC_DIR / "index.html")
            elif path.startswith("/static/"):
                target = (STATIC_DIR / path.removeprefix("/static/")).resolve()
                if STATIC_DIR.resolve() not in target.parents and target != STATIC_DIR.resolve():
                    self.send_error(HTTPStatus.FORBIDDEN, "Forbidden")
                else:
                    self.send_static(target)
            else:
                self.send_error(HTTPStatus.NOT_FOUND, "Not found")
        except Exception as exc:
            self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            payload = self.read_json()
            if parsed.path in {"/api/session", "/api/route"}:
                self.send_json(build_session(payload))
            elif parsed.path == "/api/paradigm":
                self.send_json(paradigm_selector.select(payload, root=ROOT))
            elif parsed.path == "/api/packet":
                self.send_json(consultation_packet_builder.build(payload, root=ROOT))
            elif parsed.path == "/api/execute-safe":
                self.send_json(consultation_execution_runner.build(payload, root=ROOT))
            elif parsed.path == "/api/tool-preview":
                self.send_json(build_tool_preview(payload))
            elif parsed.path == "/api/handoff":
                self.send_json(consultation_handoff_builder.build(payload, root=ROOT))
            elif parsed.path == "/api/case-record":
                self.send_json(consultation_case_recorder.build(payload, root=ROOT))
            else:
                self.send_error(HTTPStatus.NOT_FOUND, "Not found")
        except ValueError as exc:
            self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except Exception as exc:
            self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind.")
    parser.add_argument("--port", default=8765, type=int, help="Port to bind.")
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), MysticUIHandler)
    print(f"Serving 玄学大典 Web UI at http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
