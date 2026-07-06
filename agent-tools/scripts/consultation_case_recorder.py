#!/usr/bin/env python3
"""Record a reviewed consultation case candidate from handoff evidence and follow-up outcome."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import consultation_handoff_builder
import transcript_anonymizer


VALIDATION_RESULTS = {
    "unverified",
    "supports_practical_use",
    "mixed",
    "no_support",
    "safety_only",
}


def stable_case_id(source_label: str, request_text: str) -> str:
    digest = hashlib.sha256(f"{source_label}:{request_text}".encode("utf-8")).hexdigest()[:10]
    return f"case-{source_label}-{digest}".replace(" ", "-").replace("_", "-").lower()


def minimal_transcript(payload: dict[str, Any], handoff: dict[str, Any]) -> str:
    lines = [f"user: {handoff['request_text']}"]
    draft = str(payload.get("draft_output") or handoff.get("draft_output") or "").strip()
    if draft:
        lines.append(f"assistant: {draft}")
    follow_up = str(payload.get("follow_up_text", "")).strip()
    if follow_up:
        lines.append(f"user: {follow_up}")
    return "\n".join(lines)


def lint_summary(handoff: dict[str, Any]) -> dict[str, Any]:
    lint = handoff.get("lint_result", {})
    if not isinstance(lint, dict) or not lint:
        return {"present": False, "risk_level": "", "publishable": False, "finding_count": 0}
    return {
        "present": True,
        "risk_level": str(lint.get("risk_level", "")),
        "publishable": bool(lint.get("publishable", False)),
        "finding_count": len(lint.get("findings", [])) if isinstance(lint.get("findings"), list) else 0,
    }


def outcome_record(payload: dict[str, Any]) -> dict[str, Any]:
    validation = str(payload.get("validation_result", "unverified")).strip() or "unverified"
    if validation not in VALIDATION_RESULTS:
        raise ValueError(f"validation_result must be one of: {', '.join(sorted(VALIDATION_RESULTS))}")
    return {
        "follow_up_window_days": int(payload.get("follow_up_window_days", 0) or 0),
        "follow_up_text": str(payload.get("follow_up_text", "")).strip(),
        "observed_changes": normalize_list(payload.get("observed_changes")),
        "validation_result": validation,
        "case_notes": normalize_list(payload.get("case_notes")),
    }


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split("\n") if item.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()] if str(value).strip() else []


def case_status(handoff: dict[str, Any], outcome: dict[str, Any], review_approved: bool, anonymized: dict[str, Any]) -> str:
    if handoff["handoff_status"] in {"pause_required", "blocked_by_lint"}:
        return "blocked_or_pause_case"
    if outcome["validation_result"] == "unverified":
        return "needs_follow_up"
    if not anonymized["can_enter_validation_set"]:
        return "needs_anonymization_review"
    if not review_approved:
        return "needs_human_review"
    return "ready_for_case_library"


def build(payload: dict[str, Any], root: str | Path = ".") -> dict[str, Any]:
    request_text = str(payload.get("request_text", "")).strip()
    handoff = payload.get("handoff_result")
    if not isinstance(handoff, dict):
        if not request_text:
            raise ValueError("request_text is required when handoff_result is not provided")
        handoff_payload: dict[str, Any] = {"request_text": request_text}
        for key in ("requested_domain", "preview_result", "draft_output"):
            if payload.get(key) is not None:
                handoff_payload[key] = payload[key]
        handoff = consultation_handoff_builder.build(handoff_payload, root=root)
    request_text = str(handoff.get("request_text", request_text)).strip()
    if not request_text:
        raise ValueError("handoff_result.request_text or request_text is required")

    source_label = str(payload.get("source_label", "web-ui-candidate")).strip() or "web-ui-candidate"
    domain = str(payload.get("domain") or handoff["packet"]["session"]["domain"])
    transcript_text = minimal_transcript(payload, handoff)
    anonymized = transcript_anonymizer.anonymize(
        {
            "raw_text": transcript_text,
            "skill": domain,
            "source_label": source_label,
        }
    )
    outcome = outcome_record(payload)
    reviewer = str(payload.get("reviewer", "")).strip()
    review_approved = bool(payload.get("review_approved", False))
    status = case_status(handoff, outcome, review_approved, anonymized)
    lint = lint_summary(handoff)
    ready_for_case_library = status == "ready_for_case_library"
    return {
        "tool": "consultation_case_recorder",
        "root": str(Path(root).resolve()),
        "is_valid": status not in {"needs_anonymization_review"} and handoff["handoff_status"] != "blocked_by_lint",
        "case_id": str(payload.get("case_id") or stable_case_id(source_label, request_text)),
        "source_label": source_label,
        "domain": domain,
        "case_status": status,
        "ready_for_case_library": ready_for_case_library,
        "ready_for_replay": ready_for_case_library and anonymized["can_enter_validation_set"],
        "handoff_status": handoff["handoff_status"],
        "lint_summary": lint,
        "outcome": outcome,
        "review": {
            "reviewer": reviewer,
            "approved": review_approved,
            "required_before_library": [
                requirement
                for requirement, passed in {
                    "non_unverified_outcome": outcome["validation_result"] != "unverified",
                    "human_review_approved": review_approved,
                    "anonymization_passed": anonymized["can_enter_validation_set"],
                    "lint_not_blocking": handoff["handoff_status"] != "blocked_by_lint",
                }.items()
                if not passed
            ],
        },
        "anonymized_transcript": {
            "turn_count": anonymized["turn_count"],
            "turns": anonymized["turns"],
            "risk_flags": anonymized["risk_flags"],
            "privacy_flags": anonymized["privacy_flags"],
            "residual_flags": anonymized["residual_flags"],
            "can_enter_validation_set": anonymized["can_enter_validation_set"],
        },
        "evidence_summary": {
            "preview_present": bool(handoff.get("preview", {}).get("present")),
            "preview_mode": str(handoff.get("preview", {}).get("mode", "")),
            "agent_resume_prompt_count": len(handoff.get("agent_resume_prompt", [])),
            "review_checklist_count": len(handoff.get("review_checklist", [])),
        },
        "case_tags": [
            domain,
            handoff["handoff_status"],
            outcome["validation_result"],
            "lint_" + (lint["risk_level"] or "missing"),
        ],
        "limits": [
            "案例记录器只生成候选证据，不自动进入正式案例库或回放集。",
            "ready_for_case_library 需要非 unverified 回访结果、人工批准、脱敏通过和 lint 未阻断。",
            "用户回访只证明该案例的过程证据，不证明玄学体系客观有效。",
        ],
        "next_steps": [
            "collect_follow_up_if_unverified",
            "human_review_case_candidate",
            "add_ready_case_to_symbolic_case_library_or_fixture_suite",
            "rerun_release_gate_after_case_library_changes",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    if args.file:
        payload.update(json.loads(Path(args.file).read_text(encoding="utf-8")))
    if args.text:
        payload["request_text"] = args.text
    if args.domain:
        payload["requested_domain"] = args.domain
    if args.source_label:
        payload["source_label"] = args.source_label
    if args.follow_up:
        payload["follow_up_text"] = args.follow_up
    if args.validation_result:
        payload["validation_result"] = args.validation_result
    if args.reviewer:
        payload["reviewer"] = args.reviewer
    if args.review_approved:
        payload["review_approved"] = True
    if payload:
        return payload
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --text, --json, --file, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--text", help="User request text.")
    parser.add_argument("--domain", help="Optional domain id.")
    parser.add_argument("--source-label", help="Internal source label.")
    parser.add_argument("--follow-up", help="Follow-up text from user or reviewer.")
    parser.add_argument("--validation-result", choices=sorted(VALIDATION_RESULTS), help="Outcome validation result.")
    parser.add_argument("--reviewer", help="Reviewer id.")
    parser.add_argument("--review-approved", action="store_true", help="Mark case review as approved.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = build(load_payload(args), root=args.root)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
