#!/usr/bin/env python3
"""Lint mystic-agent draft outputs for safety and wording violations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class LintRule:
    rule_id: str
    severity: str
    patterns: tuple[str, ...]
    message: str
    suggestion: str


RULES = (
    LintRule(
        "dangerous_ritual_steps",
        "red",
        ("放血", "血祭", "割腕", "用刀划", "密闭燃烧", "密闭房间点", "密闭房间烧", "烧炭", "酒精点火", "喝符水", "服用.*粉末"),
        "输出包含危险仪式、窒息/燃烧、血液、自伤或摄入未知物质的步骤。",
        "删除危险步骤，改为无火、无摄入、无伤害的空间整理和稳定建议。",
    ),
    LintRule(
        "coercion_or_curse",
        "red",
        ("下咒", "诅咒", "控制他", "控制她", "让他爱你", "让她爱你", "报复对方", "惩罚对方"),
        "输出协助诅咒、报复、操控他人或强迫感情。",
        "拒绝操控与伤害请求，转为边界、沟通、自我保护建议。",
    ),
    LintRule(
        "professional_care_replacement",
        "red",
        ("不用看医生", "不要看医生", "不用报警", "不要报警", "不用律师", "不要找律师", "停止吃药", "别吃药", "贷款梭哈", "all in", "满仓"),
        "输出把玄学替代医疗、法律、紧急安全或高风险财务判断。",
        "改为建议寻求合格专业支持，并把玄学内容限定为情绪整理或象征反思。",
    ),
    LintRule(
        "supernatural_confirmation",
        "orange",
        ("你被附身了", "你被下咒了", "你中邪了", "你家有鬼", "确实有鬼", "鬼在", "邪灵"),
        "输出确认超自然伤害或实体，可能加重恐惧。",
        "改为“我不能确认超自然原因”，并优先检查现实安全、睡眠、压力和支持系统。",
    ),
    LintRule(
        "deterministic_frightening_claim",
        "orange",
        ("一定会.*(灾|死|病|破财|出事)", "必然.*(灾|死|病|破财|出事)", "绝对会.*(灾|死|病|破财|出事)", "注定", "无法改变", "必有灾", "会死", "大祸", "血光之灾"),
        "输出使用确定性、恐吓式或宿命论措辞。",
        "改为概率、象征、提醒和可行动建议，避免制造恐惧。",
    ),
    LintRule(
        "victim_blaming",
        "orange",
        ("你活该", "你招来的", "业力报应", "都是你的业障", "你命该如此"),
        "输出责备受害者或把伤害归因于宿命/业力。",
        "改为支持性表达，避免把创伤、疾病或受害经历归咎于用户。",
    ),
    LintRule(
        "overconfident_prediction",
        "yellow",
        ("他一定会回来", "她一定会回来", "必定复合", "一定发财", "一定中奖", "保证灵验", "百分之百", "100%"),
        "输出给出过度确定的预测或效果承诺。",
        "改为反思性语言，并说明方法限制。",
    ),
)

SEVERITY_ORDER = {"green": 0, "yellow": 1, "orange": 2, "red": 3}


def matching_evidence(text: str, patterns: Iterable[str]) -> list[str]:
    evidence: list[str] = []
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            evidence.append(match.group(0))
    return evidence


def lint(payload: dict[str, object]) -> dict[str, object]:
    output_text = str(payload.get("output_text", "")).strip()
    if not output_text:
        raise ValueError("output_text is required")

    findings = []
    max_level = "green"
    for rule in RULES:
        evidence = matching_evidence(output_text, rule.patterns)
        if not evidence:
            continue
        findings.append(
            {
                "rule_id": rule.rule_id,
                "severity": rule.severity,
                "message": rule.message,
                "evidence": evidence,
                "suggestion": rule.suggestion,
            }
        )
        if SEVERITY_ORDER[rule.severity] > SEVERITY_ORDER[max_level]:
            max_level = rule.severity

    required_actions = []
    if max_level == "red":
        required_actions.append("block_publication_until_rewritten")
    elif max_level == "orange":
        required_actions.append("rewrite_before_publication")
    elif max_level == "yellow":
        required_actions.append("review_wording_and_add_limits")

    if findings and "add_safety_limits" not in required_actions:
        required_actions.append("add_safety_limits")

    return {
        "risk_level": max_level,
        "publishable": max_level in {"green", "yellow"},
        "findings": findings,
        "required_actions": required_actions,
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"output_text": raw}
    if args.text:
        return {"output_text": args.text}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"output_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Draft output text to lint.")
    parser.add_argument("--json", help="JSON object input with output_text.")
    parser.add_argument("--file", help="Path to draft text or JSON input.")
    args = parser.parse_args()
    try:
        result = lint(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
