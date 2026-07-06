#!/usr/bin/env python3
"""Translate Meihua body-use relations into safe reflection and action prompts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Iterable

import meihua_casting_recorder


BLOCKING_RISKS = {"professional_finance", "medical_or_crisis", "legal_or_emergency", "coercion_or_privacy"}

DOMAIN_PATTERNS = {
    "project_career": ("项目", "工作", "合作", "沟通", "客户", "团队", "交付", "职场", "事业"),
    "relationship": ("感情", "恋爱", "伴侣", "关系", "复合", "分手", "喜欢", "婚姻"),
    "money_resources": ("预算", "资源", "收入", "生意", "报价", "成本", "资金", "钱"),
    "study_documents": ("学习", "考试", "论文", "文书", "材料", "证书", "申请"),
    "travel_move": ("出行", "搬家", "迁移", "旅行", "交通", "行程"),
    "health_safety": ("身体", "健康", "睡眠", "焦虑", "安全", "不舒服"),
    "legal_dispute": ("合同", "纠纷", "投诉", "仲裁", "法院", "律师", "证据"),
}

RELATION_FRAMES = {
    "生体": {
        "code": "support_body",
        "summary": "用方生体方，可读作外部条件、资源或他人配合正在补充主体。",
        "resource": "先确认支持是否真实可用：谁能给资源、信息、时间或承诺。",
        "pressure": "支持也可能带条件、依赖或期待，需要看清交换成本。",
        "agency": "把助力转成可验证的小承接，不把好兆头当成免行动保证。",
        "questions": ["这份支持来自谁或什么渠道？", "支持能在什么时候、以什么形式落地？", "承接支持会带来哪些义务或边界？"],
        "actions": ["向关键支持方确认具体资源和时间。", "列出自己需要承接的最小动作。", "保留一个替代方案，避免完全依赖外部助力。"],
    },
    "克体": {
        "code": "pressure_body",
        "summary": "用方克体方，可读作外部压力、约束、风险或对主体的牵制。",
        "resource": "资源在于尽早看见约束：规则、延期、误解、信息差或权责不清。",
        "pressure": "压力点可能来自外部对象、环境条件或未明确的责任边界。",
        "agency": "先降风险，再求推进；把压力拆成能核实、能协商、能缓冲的部分。",
        "questions": ["压力具体来自哪一方或哪条规则？", "哪些信息仍未确认？", "最小的缓冲或求助动作是什么？"],
        "actions": ["核实关键事实和截止时间。", "向相关方澄清责任边界。", "预留时间、资源或沟通缓冲。"],
    },
    "体生用": {
        "code": "body_supports_use",
        "summary": "体方生用方，可读作主体正在投入、付出或把资源送向事件对象。",
        "resource": "资源在主体手上，但正在外流，需要看清投入是否有效。",
        "pressure": "风险是过度付出、范围膨胀或回收信号不清。",
        "agency": "保留主动性：设定投入上限、验收信号和停止条件。",
        "questions": ["现在投入的是时间、情绪、金钱还是专业能力？", "什么迹象说明投入值得继续？", "什么时候需要暂停或缩小范围？"],
        "actions": ["为下一轮投入设定上限。", "写下一个可观察的回收信号。", "把模糊付出改成明确请求或交付物。"],
    },
    "体克用": {
        "code": "body_controls_use",
        "summary": "体方克用方，可读作主体有机会约束、整理或推动事件对象。",
        "resource": "资源在于可控杠杆：流程、话术、边界、选择权或执行节奏。",
        "pressure": "可控不等于全控，过度用力可能带来反弹或忽略他人条件。",
        "agency": "选择一个最小可控点试行，用反馈修正，而不是一次性压结论。",
        "questions": ["现在最可控的一个环节是什么？", "怎样做能低成本验证效果？", "哪里需要避免过度控制？"],
        "actions": ["选择一个可控动作先试 24-72 小时。", "把要求写成清晰边界或流程。", "收集反馈后再决定是否加码。"],
    },
    "比和": {
        "code": "same_element",
        "summary": "体用同气，可读作同类、同频、拉平、僵持或彼此条件相近。",
        "resource": "资源在共同语言、相似目标或已经存在的默契。",
        "pressure": "同气也可能变成原地等待、互相观望或缺少决定性信号。",
        "agency": "区分协同与停滞：补一个决策规则或下一步信号。",
        "questions": ["双方或内外条件哪里同频？", "哪里因为太相似而卡住？", "下一个能打破观望的信号是什么？"],
        "actions": ["明确共同目标和分工。", "设一个简单决策规则。", "约定下一次复盘或确认节点。"],
    },
}

DOMAIN_ACTIONS = {
    "project_career": {
        "lens": "把体用关系落到沟通、交付、责任边界和延期风险。",
        "actions": ["同步项目状态和阻塞点。", "确认下一轮交付口径。"],
        "warning": "",
    },
    "relationship": {
        "lens": "只谈互动模式、边界和自我表达，不替对方下确定心理结论。",
        "actions": ["把猜测改成一次温和确认。", "先说明自己的感受和边界。"],
        "warning": "关系议题不能用体用关系确定对方真实想法或承诺。",
    },
    "money_resources": {
        "lens": "只谈预算、资源分配和商务沟通，不给投资、借贷或交易建议。",
        "actions": ["核对预算口径和责任人。", "把资源缺口写成可协商清单。"],
        "warning": "涉及投资、借贷、交易或高风险财务决策时必须暂停占问。",
    },
    "study_documents": {
        "lens": "把体用关系落到材料准备、知识盲点和反馈节奏。",
        "actions": ["列出最需要补证据的一段材料。", "请可信读者先看一个小版本。"],
        "warning": "",
    },
    "travel_move": {
        "lens": "把体用关系落到行程核实、时间缓冲和安全边界。",
        "actions": ["复核路线、票据和备用方案。", "为变动预留时间缓冲。"],
        "warning": "",
    },
    "health_safety": {
        "lens": "只做身心状态记录和支持建议，不做诊断或治疗判断。",
        "actions": ["记录身体信号并联系现实支持。", "必要时寻求专业医疗或危机支持。"],
        "warning": "健康、安全或危机议题不可用梅花关系替代专业帮助。",
    },
    "legal_dispute": {
        "lens": "只做材料整理和沟通风险提示，不给法律策略或胜负判断。",
        "actions": ["整理事实时间线和证据清单。", "向合格法律专业人士确认下一步。"],
        "warning": "法律纠纷不可用梅花关系替代法律意见。",
    },
    "general": {
        "lens": "把体用关系落到资源、压力、边界和下一步验证。",
        "actions": ["写下一个可观察信号。", "选择一个低风险小动作。"],
        "warning": "",
    },
}


def normalize_str(value: Any) -> str:
    return str(value or "").strip()


def text_contains_any(text: str, values: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def detect_domain(text: str, focus: str = "") -> str:
    combined = f"{text} {focus}".strip()
    for domain, patterns in DOMAIN_PATTERNS.items():
        if text_contains_any(combined, patterns):
            return domain
    return "general"


def casting_from(payload: dict[str, Any]) -> dict[str, Any]:
    record = payload.get("casting_record")
    if isinstance(record, dict) and record.get("tool") == "meihua_casting_recorder":
        return record
    cast_payload = dict(payload)
    cast_payload.pop("casting_record", None)
    if not normalize_str(cast_payload.get("question_text")):
        cast_payload["question_text"] = normalize_str(payload.get("request_text", payload.get("question", "")))
    return meihua_casting_recorder.record(cast_payload)


def relation_from(cast: dict[str, Any]) -> str:
    computed = normalize_str(cast.get("computed_body_use_relation"))
    provided = normalize_str(cast.get("body_use_relation"))
    return computed or provided


def merge_risk_flags(payload: dict[str, Any], cast: dict[str, Any]) -> list[str]:
    flags = list(cast.get("risk_flags", []))
    extra_flags = meihua_casting_recorder.detect_risk_flags(
        {
            "question_text": payload.get("question_text", payload.get("request_text", "")),
            "interpretation_request": payload.get("interpretation_request", payload.get("focus", "")),
            "notes": payload.get("notes", ""),
        }
    )
    for flag in extra_flags:
        if flag not in flags:
            flags.append(flag)
    return flags


def build_frame(relation: str, domain: str) -> dict[str, Any]:
    frame = RELATION_FRAMES[relation]
    domain_frame = DOMAIN_ACTIONS[domain]
    actions = list(frame["actions"])
    for action in domain_frame["actions"]:
        if action not in actions:
            actions.append(action)
    prohibited = [
        "不把体用生克写成成败、财富、疾病、关系或灾祸的确定结论。",
        "不替代医疗、法律、财务、心理健康、职业或紧急安全建议。",
        "不以体用关系确认他人真实想法、隐私、命运或超自然原因。",
    ]
    if domain_frame["warning"]:
        prohibited.append(domain_frame["warning"])
    return {
        "relation_code": frame["code"],
        "relation_summary": frame["summary"],
        "domain_lens": domain_frame["lens"],
        "resource_reading": frame["resource"],
        "pressure_reading": frame["pressure"],
        "agency_reading": frame["agency"],
        "evidence_questions": frame["questions"],
        "low_risk_actions": actions[:5],
        "prohibited_framing": prohibited,
    }


def interpret(payload: dict[str, Any]) -> dict[str, Any]:
    cast = casting_from(payload)
    question_text = normalize_str(cast.get("question_text")) or normalize_str(payload.get("question_text", payload.get("request_text", "")))
    focus = normalize_str(payload.get("focus", payload.get("interpretation_request", "")))
    domain = detect_domain(question_text, focus)
    relation = relation_from(cast)
    risk_flags = merge_risk_flags(payload, cast)
    warnings = list(cast.get("warnings", []))
    if any(flag in risk_flags for flag in ("deterministic_claim", "supernatural_fear")):
        warning = "先把确定性或超自然恐惧表达降级为象征反思，再解释体用关系。"
        if warning not in warnings:
            warnings.append(warning)
    if any(flag in risk_flags for flag in BLOCKING_RISKS):
        warnings.append("高风险议题需暂停梅花体用解释，转向现实支持或专业帮助。")

    can_interpret = bool(cast.get("is_valid")) and relation in RELATION_FRAMES and not any(flag in risk_flags for flag in BLOCKING_RISKS)
    frame = build_frame(relation, domain) if can_interpret else {}
    if not relation:
        warnings.append("missing body-use relation prevents interpretation; ask for body/use trigrams or relation.")
    elif relation not in RELATION_FRAMES:
        warnings.append(f"unknown body-use relation: {relation}")

    return {
        "tool": "meihua_relation_interpreter",
        "system": "meihua_yishu",
        "question_text": question_text,
        "question_domain": domain,
        "risk_flags": risk_flags,
        "casting_is_valid": bool(cast.get("is_valid")),
        "can_interpret_relation": can_interpret,
        "missing_fields": cast.get("missing_fields", []),
        "body_trigram": cast.get("body_trigram", ""),
        "use_trigram": cast.get("use_trigram", ""),
        "moving_line": cast.get("moving_line"),
        "base_hexagram": cast.get("base_hexagram", ""),
        "mutual_hexagram": cast.get("mutual_hexagram", ""),
        "changed_hexagram": cast.get("changed_hexagram", ""),
        "body_use_relation": cast.get("body_use_relation", ""),
        "computed_body_use_relation": cast.get("computed_body_use_relation", ""),
        "trigram_elements": cast.get("trigram_elements", {"body": "", "use": ""}),
        "interpretation_frame": frame,
        "warnings": warnings,
        "limits": [
            "此工具只解释已记录的体用关系，不自动排卦、不补数字、不替用户决定。",
            "体用生克只能作为象征反思框架，必须落到可观察事实、边界和低风险行动。",
            "涉及医疗、法律、财务、危机、人身安全、隐私或操控他人时，暂停占问并转现实支持。",
        ],
        "next_steps": [
            "draft_meihua_answer_from_relation_frame" if can_interpret else "ask_for_missing_or_safer_context_before_interpretation",
            "include_casting_source_and_method_limits",
            "run_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --json, --file, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON input with casting_record or Meihua casting fields.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = interpret(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
