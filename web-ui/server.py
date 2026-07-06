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
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = Path(__file__).resolve().parent / "static"
SCRIPTS_DIR = ROOT / "agent-tools" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import agent_workflow_router  # noqa: E402
import agent_runtime_dry_run_runner  # noqa: E402
import consultation_packet_builder  # noqa: E402
import knowledge_coverage_audit  # noqa: E402
import paradigm_selector  # noqa: E402
import tool_manifest_builder  # noqa: E402


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
        "id": "space",
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
    return {
        "tool": "web_ui_session",
        "is_valid": bool(route["is_valid"]),
        "request_text": text,
        "domain": route["domain"],
        "domain_display_name": names.get(route["domain"], route["domain"]),
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
        "context": context,
        "initial_tool_commands": commands,
        "raw_route": route,
    }


def doc_index() -> dict[str, Any]:
    docs = []
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
    return {"tool": "web_ui_doc_index", "count": len(docs), "docs": docs}


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
            elif path == "/api/docs":
                query = parsed.query
                if query.startswith("path="):
                    self.send_json(read_doc(unquote(query.removeprefix("path="))))
                else:
                    self.send_json(doc_index())
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
