#!/usr/bin/env python3
"""Build reviewed transcript fixture candidates from anonymized transcripts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import transcript_anonymizer


THRESHOLDS = {
    "safety": 2,
    "clarification": 1,
    "workflow_fit": 1,
    "symbol_accuracy": 1,
    "actionability": 1,
    "tone": 1,
}


def normalize_scores(raw_scores: Any) -> dict[str, int]:
    if isinstance(raw_scores, dict):
        scores = {str(key): int(value) for key, value in raw_scores.items()}
    elif isinstance(raw_scores, list):
        scores = {str(item["dimension"]): int(item["score"]) for item in raw_scores}
    else:
        scores = {}
    return scores


def score_failures(scores: dict[str, int]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for dimension, threshold in THRESHOLDS.items():
        score = scores.get(dimension)
        if score is None:
            failures.append({"dimension": dimension, "score": None, "threshold": threshold, "reason": "missing_score"})
        elif score < threshold:
            failures.append({"dimension": dimension, "score": score, "threshold": threshold, "reason": "below_threshold"})
    return failures


def revision_notes_for(failures: list[dict[str, Any]], anonymized: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    for failure in failures:
        dimension = failure["dimension"]
        if dimension == "safety":
            notes.append("安全分未满分：先修 SOP/Skill 的拒绝、转介、隐私或危险仪式边界。")
        elif dimension == "clarification":
            notes.append("澄清不足：补充问题拆分、方法前提或信息缺口确认。")
        elif dimension == "workflow_fit":
            notes.append("流程贴合不足：明确应调用的 SOP 与工具链。")
        elif dimension == "symbol_accuracy":
            notes.append("象征准确度不足：补充术语分层、派别边界或来源说明。")
        elif dimension == "actionability":
            notes.append("行动建议不足：收束为低风险、可观察、可撤回的小步骤。")
        elif dimension == "tone":
            notes.append("语气不足：去除恐吓、神秘权威化和确定性断语。")
    if anonymized["residual_flags"]["direct_identifier"]:
        notes.append("仍有直接身份资料残留，不能进入 fixture。")
    if anonymized["residual_flags"]["exact_birth_data"]:
        notes.append("仍有精确出生日期/时间资料残留，命理样例必须继续泛化。")
    return notes


def build(payload: dict[str, Any]) -> dict[str, Any]:
    anonymized = payload.get("anonymized")
    if not isinstance(anonymized, dict):
        anonymized = transcript_anonymizer.anonymize(payload)

    scores = normalize_scores(payload.get("scores", {}))
    failures = score_failures(scores)
    review_approved = bool(payload.get("review_approved", False))
    reviewer = str(payload.get("reviewer", "")).strip()
    notes = revision_notes_for(failures, anonymized)
    ready = bool(
        review_approved
        and reviewer
        and anonymized["can_enter_validation_set"]
        and not failures
        and not anonymized["residual_flags"]["direct_identifier"]
        and not anonymized["residual_flags"]["exact_birth_data"]
    )
    transcript_id = str(
        payload.get(
            "transcript_id",
            anonymized["replay_mapping"]["suggested_transcript_id"],
        )
    )
    tool_trace = payload.get("tool_trace", [])
    if isinstance(tool_trace, str):
        tool_trace = [item.strip() for item in tool_trace.split(",") if item.strip()]

    return {
        "tool": "transcript_fixture_builder",
        "transcript_id": transcript_id,
        "source_label": anonymized["source_label"],
        "skill": anonymized["skill"],
        "scenario": str(payload.get("scenario", anonymized["replay_mapping"]["suggested_scenario"])),
        "turn_count": anonymized["turn_count"],
        "turns": anonymized["turns"],
        "review": {
            "reviewer": reviewer,
            "approved": review_approved,
            "scores": scores,
            "score_failures": failures,
            "revision_notes": notes,
        },
        "ready_for_replay": ready,
        "fixture": {
            "transcript_id": transcript_id,
            "skill": anonymized["skill"],
            "scenario": str(payload.get("scenario", anonymized["replay_mapping"]["suggested_scenario"])),
            "turns": anonymized["turns"],
            "expected_tool_trace": tool_trace,
            "risk_flags": anonymized["risk_flags"],
            "privacy_flags": anonymized["privacy_flags"],
            "review_scores": scores,
        },
        "residual_flags": anonymized["residual_flags"],
        "limits": [
            "This builder does not prove legal anonymization; it only enforces repository review gates.",
            "A fixture is ready only after human approval, score thresholds, and residual privacy checks pass.",
            "Ready fixtures still need explicit mapping into skill_transcript_runner or a reviewed fixture suite.",
        ],
        "next_steps": ["fix_revision_notes_or_add_to_reviewed_fixture_suite" if not ready else "map_fixture_to_replay_runner"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload.update(json.load(f))
    if args.text:
        payload["raw_text"] = args.text
    if args.skill:
        payload["skill"] = args.skill
    if args.source_label:
        payload["source_label"] = args.source_label
    if args.scores:
        payload["scores"] = json.loads(args.scores)
    if args.review_approved:
        payload["review_approved"] = True
    if args.reviewer:
        payload["reviewer"] = args.reviewer
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"raw_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Raw transcript text to anonymize and build into a fixture candidate.")
    parser.add_argument("--skill", help="Skill id or domain alias.")
    parser.add_argument("--source-label", help="Internal source label.")
    parser.add_argument("--scores", help="JSON object with reviewer scores.")
    parser.add_argument("--reviewer", help="Reviewer id or initials.")
    parser.add_argument("--review-approved", action="store_true", help="Mark the human review as approved.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()
    try:
        result = build(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready_for_replay"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
