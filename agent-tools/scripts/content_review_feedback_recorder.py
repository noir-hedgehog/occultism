#!/usr/bin/env python3
"""Record structured human content-review feedback for a mystic domain."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

import content_review_packet_builder


DECISIONS = {"approved", "changes_requested", "rejected"}


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()] if str(value).strip() else []


def build_kanban_updates(domain: str, corrections: list[str]) -> list[dict[str, str]]:
    return [
        {
            "suggested_id": f"REV-{domain.upper()}-{index:03d}",
            "task": correction,
            "target_column": "Doing",
            "reason": "content_review_correction",
        }
        for index, correction in enumerate(corrections, start=1)
    ]


def record(payload: dict[str, Any], root: str | Path = ".") -> dict[str, Any]:
    packets = content_review_packet_builder.build(root)
    packet_by_domain = {packet["domain"]: packet for packet in packets["packets"]}
    domain = str(payload.get("domain", "")).strip()
    packet = packet_by_domain.get(domain)
    reviewer = str(payload.get("reviewer", "")).strip()
    review_date = str(payload.get("review_date", "")).strip()
    decision = str(payload.get("decision", "")).strip()
    approved_scope = normalize_list(payload.get("approved_scope"))
    required_corrections = normalize_list(payload.get("required_corrections"))
    residual_risks = normalize_list(payload.get("residual_risks"))
    notes = normalize_list(payload.get("notes"))

    errors: list[str] = []
    if not packet:
        errors.append("unknown_domain")
    if not reviewer:
        errors.append("missing_reviewer")
    if not review_date:
        errors.append("missing_review_date")
    else:
        try:
            date.fromisoformat(review_date)
        except ValueError:
            errors.append("invalid_review_date")
    if decision not in DECISIONS:
        errors.append("invalid_decision")
    if not approved_scope:
        errors.append("missing_approved_scope")
    if decision == "approved" and required_corrections:
        errors.append("approved_with_required_corrections")
    if decision in {"changes_requested", "rejected"} and not required_corrections:
        errors.append("missing_required_corrections")

    can_count_as_content_approval = not errors and decision == "approved"
    status = "approved" if can_count_as_content_approval else ("needs_revision" if decision == "changes_requested" else "not_approved")

    return {
        "tool": "content_review_feedback_recorder",
        "root": str(Path(root).resolve()),
        "is_valid": not errors,
        "domain": domain,
        "display_name": packet["display_name"] if packet else "",
        "reviewer": reviewer,
        "review_date": review_date,
        "decision": decision,
        "status": status,
        "can_count_as_content_approval": can_count_as_content_approval,
        "approved_scope": approved_scope,
        "required_corrections": required_corrections,
        "residual_risks": residual_risks,
        "notes": notes,
        "errors": errors,
        "kanban_updates": build_kanban_updates(domain or "unknown", required_corrections),
        "evidence": {
            "packet_status": packet["review_status"] if packet else "",
            "packet_level": packet["level"] if packet else "",
            "packet_open_items": packet["open_items"] if packet else [],
        },
        "limits": [
            "此工具只记录审校反馈，不判断审校人的资质。",
            "can_count_as_content_approval 为 true 只表示结构化证据齐全，仍需维护者决定是否更新版本状态。",
            "changes_requested 和 rejected 不应被计入内容批准。",
        ],
        "next_steps": ["update_review_log", "apply_required_corrections", "rerun_release_gate_runner"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--json", help="Review feedback JSON payload.")
    parser.add_argument("--domain", help="Domain id, e.g. tarot.")
    parser.add_argument("--reviewer", help="Reviewer name, initials, or role.")
    parser.add_argument("--review-date", help="Review date in YYYY-MM-DD format.")
    parser.add_argument("--decision", choices=sorted(DECISIONS), help="Review decision.")
    parser.add_argument("--approved-scope", action="append", help="Approved scope item. Can be repeated.")
    parser.add_argument("--required-correction", action="append", help="Required correction. Can be repeated.")
    parser.add_argument("--residual-risk", action="append", help="Residual risk. Can be repeated.")
    parser.add_argument("--note", action="append", help="Review note. Can be repeated.")
    args = parser.parse_args()
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    for key, value in {
        "domain": args.domain,
        "reviewer": args.reviewer,
        "review_date": args.review_date,
        "decision": args.decision,
        "approved_scope": args.approved_scope,
        "required_corrections": args.required_correction,
        "residual_risks": args.residual_risk,
        "notes": args.note,
    }.items():
        if value is not None:
            payload[key] = value
    result = record(payload, root=args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
