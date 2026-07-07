#!/usr/bin/env python3
"""Build collection templates for validation backlog items."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import case_validation_backlog_builder


FIELD_DETAILS: dict[str, dict[str, str]] = {
    "request_text": {
        "type": "string",
        "prompt": "用户原始请求或脱敏后的等价请求。",
        "example": "卧室床尾对门，最近睡不好，想知道能不能做低风险调整。",
    },
    "baseline_observation": {
        "type": "string",
        "prompt": "行动前可观察的现实状态、评分或频率。",
        "example": "连续 7 天睡眠主观评分 4/10，夜间通知灯和门口走动声会打断睡眠。",
    },
    "low_risk_action": {
        "type": "string",
        "prompt": "低成本、可撤回、不替代专业判断的现实行动。",
        "example": "遮挡通知灯、调整镜子角度、睡前 30 分钟整理床边杂物。",
    },
    "follow_up_window_days": {
        "type": "integer",
        "prompt": "回访窗口，单位为天。",
        "example": "14",
    },
    "before_score": {
        "type": "number",
        "prompt": "行动前的主观或行为评分。",
        "example": "4",
    },
    "after_score": {
        "type": "number",
        "prompt": "行动后的同口径评分。",
        "example": "6",
    },
    "observed_changes": {
        "type": "array<string>",
        "prompt": "回访中观察到的变化，必须允许无变化或反向变化。",
        "example": "夜间醒来次数减少；仍不能排除工作压力影响。",
    },
    "validation_result": {
        "type": "enum",
        "prompt": "验证结果：supports_practical_use、mixed、no_support、safety_only 或 unverified。",
        "example": "mixed",
    },
    "reviewer": {
        "type": "string",
        "prompt": "审校人、维护者或角色名。",
        "example": "internal-reviewer",
    },
    "experience_text": {
        "type": "string",
        "prompt": "用户体验的脱敏描述，避免把感受直接确认为超自然事实。",
        "example": "入睡前反复觉得有人在房间里，醒来后仍然紧张。",
    },
    "duration_or_frequency": {
        "type": "string",
        "prompt": "持续时长、发生频率或触发周期。",
        "example": "近两周每周 3 次，主要发生在熬夜后。",
    },
    "ordinary_triggers": {
        "type": "array<string>",
        "prompt": "可先排查的普通诱因。",
        "example": "睡眠不足；咖啡因；近期压力；药物变化。",
    },
    "red_flags_checked": {
        "type": "array<string>",
        "prompt": "已检查的身体、心理或现实安全红旗。",
        "example": "自伤风险为否；持续幻听为否；睡眠严重受损需现实支持。",
    },
    "care_action": {
        "type": "string",
        "prompt": "现实照料动作或专业支持边界。",
        "example": "先记录睡眠和压力触发；若持续恶化，建议寻求专业支持。",
    },
    "space_or_object_description": {
        "type": "string",
        "prompt": "空间、物件或环境的可观察描述。",
        "example": "书桌背后是走廊，屏幕反光明显，插线板靠近水杯。",
    },
    "safety_constraints": {
        "type": "array<string>",
        "prompt": "不能触碰的安全约束。",
        "example": "不移动承重结构；不使用明火；不遮挡消防通道。",
    },
    "claim_text": {
        "type": "string",
        "prompt": "待审计的具体说法，不能只写主题名。",
        "example": "三张牌阵可以稳定判断未来三个月的具体结果。",
    },
    "source_type": {
        "type": "enum",
        "prompt": "来源类型：classical_text、commentary、regional_tradition、modern_author、web_secondary、user_report 等。",
        "example": "modern_author",
    },
    "source_title_or_url": {
        "type": "string",
        "prompt": "来源标题、版本、链接或可复查描述。",
        "example": "某现代塔罗教材，第二章三张牌阵说明。",
    },
    "school_or_region": {
        "type": "string",
        "prompt": "适用流派、地区、时代或牌系。",
        "example": "RWS 系，现代心理塔罗语境。",
    },
    "primary_or_secondary_source": {
        "type": "enum",
        "prompt": "原典、注疏、二手整理、现代作者、用户自述或网络转述。",
        "example": "secondary_source",
    },
    "conflicting_interpretations": {
        "type": "array<string>",
        "prompt": "不同流派、来源或实践者的差异解释。",
        "example": "部分教材将三张牌用于趋势反思，不支持具体结果断言。",
    },
    "correction_note": {
        "type": "string",
        "prompt": "勘误或限定写法。",
        "example": "改为：三张牌阵适合梳理现状、阻碍和建议，不保证未来结果。",
    },
    "unsafe_request_or_claim": {
        "type": "string",
        "prompt": "不安全请求、断言或原始高风险说法。",
        "example": "你身边一定有灵体作祟，需要马上付费处理。",
    },
    "risk_category": {
        "type": "string",
        "prompt": "风险类别，如恐吓、专业替代、第三方操控、依赖、高价承诺。",
        "example": "恐吓与高价承诺",
    },
    "why_blocked_or_reframed": {
        "type": "string",
        "prompt": "为什么阻断或降级改写。",
        "example": "它确认不可证实的灵体事实，并用恐惧推动付费行动。",
    },
    "safe_rewrite": {
        "type": "string",
        "prompt": "可发布的安全改写。",
        "example": "先把不安感当作体验记录，检查睡眠、噪音和压力来源，再做低风险整理。",
    },
    "professional_boundary": {
        "type": "string",
        "prompt": "医疗、法律、财务、心理危机或现实安全边界。",
        "example": "若出现持续失眠、惊恐或伤害念头，优先寻求现实支持。",
    },
    "source_or_school_note": {
        "type": "string",
        "prompt": "来源、派别或解释传统的限定说明。",
        "example": "此说法只作为现代象征实践，不作为传统共识。",
    },
    "interpretation_path": {
        "type": "array<string>",
        "prompt": "从输入到输出的解释路径。",
        "example": "记录问题；说明来源；拆分象征；转成低风险行动。",
    },
}


PRIORITY_EXAMPLES = {
    "P0": {
        "follow_up_window_days": 14,
        "before_score": 4,
        "after_score": 6,
        "validation_result": "mixed",
    },
    "P1": {
        "review_date": "2026-07-07",
        "decision": "changes_requested",
        "approved_scope": ["只批准限定为象征反思的表述"],
    },
    "P2": {
        "lint_text": "你一定被灵体缠上了，不处理会出大事。",
        "validation_result": "safety_only",
    },
}


def field_detail(field: str, priority: str) -> dict[str, Any]:
    fallback = {
        "type": "string",
        "prompt": f"填写 {field}。",
        "example": f"{field}_example",
    }
    detail = FIELD_DETAILS.get(field, fallback)
    return {
        "field": field,
        "required": True,
        "type": detail["type"],
        "prompt": detail["prompt"],
        "example": detail["example"],
        "feeds": feeds_for(field, priority),
    }


def feeds_for(field: str, priority: str) -> list[str]:
    if priority == "P0":
        mapping = {
            "request_text": ["consultation_execution_runner", "consultation_case_recorder"],
            "low_risk_action": ["consultation_handoff_builder", "consultation_case_recorder"],
            "follow_up_window_days": ["consultation_case_recorder"],
            "observed_changes": ["consultation_case_recorder"],
            "validation_result": ["consultation_case_recorder"],
            "reviewer": ["consultation_case_recorder"],
        }
        return mapping.get(field, ["consultation_case_recorder"])
    if priority == "P1":
        mapping = {
            "claim_text": ["content_review_packet_builder", "content_review_feedback_recorder"],
            "correction_note": ["content_review_feedback_recorder"],
            "reviewer": ["content_review_feedback_recorder"],
        }
        return mapping.get(field, ["content_review_feedback_recorder"])
    mapping = {
        "unsafe_request_or_claim": ["mystic_intake_triage", "mystic_output_lint"],
        "safe_rewrite": ["mystic_output_lint", "consultation_case_recorder"],
        "professional_boundary": ["mystic_output_lint"],
        "reviewer": ["consultation_case_recorder"],
    }
    return mapping.get(field, ["mystic_output_lint"])


def example_value(field: str, priority: str) -> Any:
    if field in PRIORITY_EXAMPLES.get(priority, {}):
        return PRIORITY_EXAMPLES[priority][field]
    value = FIELD_DETAILS.get(field, {}).get("example", f"{field}_example")
    if field in {"observed_changes", "ordinary_triggers", "red_flags_checked", "safety_constraints", "conflicting_interpretations", "interpretation_path"}:
        return [item.strip() for item in value.replace("；", ";").split(";") if item.strip()]
    if FIELD_DETAILS.get(field, {}).get("type") == "integer":
        return 14
    if FIELD_DETAILS.get(field, {}).get("type") == "number":
        return 5
    return value


def tool_flow_for(item: dict[str, Any]) -> list[dict[str, Any]]:
    priority = item["priority"]
    required = set(item["required_fields"])
    request_field = "request_text" if "request_text" in required else item["required_fields"][0]
    action_field = "low_risk_action" if "low_risk_action" in required else ("care_action" if "care_action" in required else request_field)
    if priority == "P0":
        return [
            {
                "tool": "consultation_execution_runner",
                "purpose": "先执行安全白名单子集，确认哪些步骤可程序化、哪些需要 Agent 或人工补字段。",
                "input_from_fields": [request_field],
            },
            {
                "tool": "consultation_handoff_builder",
                "purpose": "把低风险行动、草稿和复核点整理成 Agent/审校交接包。",
                "input_from_fields": sorted({request_field, action_field}),
            },
            {
                "tool": "consultation_case_recorder",
                "purpose": "记录回访、验证结果、脱敏摘要和人工审校状态。",
                "input_from_fields": [
                    field
                    for field in [request_field, "follow_up_window_days", "observed_changes", "validation_result", "reviewer"]
                    if field in required
                ],
            },
        ]
    if priority == "P1":
        return [
            {
                "tool": "content_review_packet_builder",
                "purpose": "取出对应领域的 SOP、知识卡、Skill 和工具审校包。",
                "input_from_fields": ["domain"],
            },
            {
                "tool": "content_review_feedback_recorder",
                "purpose": "记录来源审计、勘误、批准范围和必改项。",
                "input_from_fields": ["claim_text", "source_title_or_url", "correction_note", "reviewer"],
            },
        ]
    return [
        {
            "tool": "mystic_intake_triage",
            "purpose": "识别高风险请求是否应阻断、暂停或降级到现实支持。",
            "input_from_fields": ["unsafe_request_or_claim"],
        },
        {
            "tool": "mystic_output_lint",
            "purpose": "检查安全改写是否仍含恐吓、保证、专业替代或操控他人。",
            "input_from_fields": ["safe_rewrite", "professional_boundary"],
        },
        {
            "tool": "consultation_case_recorder",
            "purpose": "把安全边界样本沉淀为 safety_only 或 blocked_or_pause_case 候选记录。",
            "input_from_fields": ["unsafe_request_or_claim", "safe_rewrite", "validation_result", "reviewer"],
        },
    ]


def review_checklist_for(item: dict[str, Any]) -> list[str]:
    priority = item["priority"]
    if priority == "P0":
        return [
            "baseline 与 follow-up 使用同一观察口径。",
            "低风险行动可停止、可撤回、不会替代医疗/法律/财务/现实安全建议。",
            "记录无变化、负向变化或普通诱因，不能只保留支持性案例。",
        ]
    if priority == "P1":
        return [
            "来源层级、版本、地区或流派限制可复查。",
            "冲突解释被并列记录，不把单一来源写成唯一正统。",
            "勘误写法明确区分事实、传统说法、现代解释和用户体验。",
        ]
    return [
        "原始高风险说法被保留为反例，但不作为可发布建议。",
        "安全改写没有确认灵体事实、诅咒、操控他人、结果保证或专业替代。",
        "professional/safety boundary 明确说明需要现实支持的情形。",
    ]


def build_template(item: dict[str, Any]) -> dict[str, Any]:
    priority = item["priority"]
    fields = [field_detail(field, priority) for field in item["required_fields"]]
    example_payload = {field["field"]: example_value(field["field"], priority) for field in fields}
    example_payload["domain"] = item["domain"]
    return {
        "template_id": f"template-{item['backlog_id']}",
        "source_backlog_id": item["backlog_id"],
        "domain": item["domain"],
        "display_name": item["display_name"],
        "priority": priority,
        "trunk": item["trunk"],
        "evidence_mode": item["evidence_mode"],
        "mystical_intensity": item["mystical_intensity"],
        "target_artifact": item["target_artifact"],
        "collection_template": {
            "fields": fields,
            "example_payload": example_payload,
            "review_checklist": review_checklist_for(item),
            "acceptance_criteria": item["acceptance_criteria"],
        },
        "recommended_tool_flow": tool_flow_for(item),
        "source_docs": item["source_docs"],
        "next_steps": [
            "fill_template_with_real_or_anonymized_material",
            "run_recommended_tool_flow",
            "review_result_before_case_library_or_content_update",
            "rerun_release_gate_after_approved_fixture_or_doc_changes",
        ],
    }


def select_items(backlog: dict[str, Any], domain: str | None, backlog_id: str | None, limit: int | None) -> list[dict[str, Any]]:
    items = backlog["items"]
    if backlog_id:
        items = [item for item in items if item["backlog_id"] == backlog_id]
        if not items:
            raise ValueError(f"unknown backlog_id: {backlog_id}")
    if domain:
        items = [item for item in items if item["domain"] == domain]
        if not items:
            raise ValueError(f"unknown domain: {domain}")
    if limit is not None:
        items = items[: max(0, limit)]
    return items


def build(
    root: str | Path = ".",
    domain: str | None = None,
    backlog_id: str | None = None,
    priority: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    backlog = case_validation_backlog_builder.build(root_path, priority=priority)
    items = select_items(backlog, domain, backlog_id, limit)
    templates = [build_template(item) for item in items]
    priority_counts: dict[str, int] = {}
    target_artifact_counts: dict[str, int] = {}
    for template in templates:
        priority_counts[template["priority"]] = priority_counts.get(template["priority"], 0) + 1
        target_artifact_counts[template["target_artifact"]] = target_artifact_counts.get(template["target_artifact"], 0) + 1
    result = {
        "tool": "case_validation_template_builder",
        "root": str(root_path),
        "is_valid": bool(templates),
        "source_backlog_count": backlog["backlog_count"],
        "template_count": len(templates),
        "domain_filter": domain or "",
        "backlog_id_filter": backlog_id or "",
        "priority_filter": priority.strip().upper() if priority else "",
        "priority_counts": dict(sorted(priority_counts.items())),
        "target_artifact_counts": dict(sorted(target_artifact_counts.items())),
        "templates": templates,
        "limits": [
            "模板只定义采集字段和工具流，不表示案例、来源或边界反例已经通过审校。",
            "真实材料必须脱敏，且不得把个人经历、照片或信仰信息用于超出授权的用途。",
            "P0/P1/P2 仍是工作优先级，不是玄学有效性等级。",
        ],
        "next_steps": [
            "choose_one_backlog_item_before_adding_new_domains",
            "collect_real_or_anonymized_material_with_template",
            "run_recommended_tool_flow_and_human_review",
            "promote_approved_results_to_case_library_source_notes_or_boundary_examples",
        ],
    }
    result["generated_markdown"] = render_markdown(result)
    return result


def render_field_table(fields: list[dict[str, Any]]) -> list[str]:
    lines = ["| 字段 | 类型 | 提示 | 示例 | 流向 |", "| --- | --- | --- | --- | --- |"]
    for field in fields:
        feeds = ", ".join(f"`{tool}`" for tool in field["feeds"])
        lines.append(f"| `{field['field']}` | `{field['type']}` | {field['prompt']} | {field['example']} | {feeds} |")
    return lines


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# 案例采集模板",
        "",
        "本页把案例验证 Backlog 转成可填写的采集模板。模板用于收集实用案例、来源审计和边界反例，随后再交给对应工具与人工审校。",
        "",
        "## 摘要",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 来源 Backlog | {result['source_backlog_count']} |",
        f"| 模板 | {result['template_count']} |",
        f"| 优先级 | {case_validation_backlog_builder.render_count_map(result['priority_counts'])} |",
        f"| 目标产物 | {case_validation_backlog_builder.render_count_map(result['target_artifact_counts'])} |",
        "",
        "## 模板",
        "",
    ]
    for template in result["templates"]:
        lines.extend(
            [
                f"### {template['template_id']} {template['display_name']}",
                "",
                f"- 来源 Backlog：`{template['source_backlog_id']}`",
                f"- 领域：`{template['domain']}`",
                f"- 优先级：`{template['priority']}`",
                f"- 目标产物：`{template['target_artifact']}`",
                f"- 证据模式：`{template['evidence_mode']}`",
                "",
                "#### 采集字段",
                "",
            ]
        )
        lines.extend(render_field_table(template["collection_template"]["fields"]))
        lines.extend(["", "#### 推荐工具流", ""])
        for step in template["recommended_tool_flow"]:
            fields = ", ".join(f"`{field}`" for field in step["input_from_fields"])
            lines.append(f"- `{step['tool']}`：{step['purpose']} 输入字段：{fields}")
        lines.extend(["", "#### 复核清单", ""])
        for item in template["collection_template"]["review_checklist"]:
            lines.append(f"- {item}")
        lines.extend(["", "#### 验收标准", ""])
        for item in template["collection_template"]["acceptance_criteria"]:
            lines.append(f"- {item}")
        lines.extend(["", "#### 示例 Payload", "", "```json"])
        lines.append(json.dumps(template["collection_template"]["example_payload"], ensure_ascii=False, indent=2))
        lines.extend(["```", ""])
    lines.extend(["## 限制", ""])
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
    parser.add_argument("--domain", help="Optional domain id, e.g. fengshui.")
    parser.add_argument("--backlog-id", help="Optional exact backlog id.")
    parser.add_argument("--priority", choices=["P0", "P1", "P2", "p0", "p1", "p2"], help="Optional priority filter.")
    parser.add_argument("--limit", type=int, help="Optional template limit.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/案例采集模板.md.")
    args = parser.parse_args()
    try:
        result = build(args.root, domain=args.domain, backlog_id=args.backlog_id, priority=args.priority, limit=args.limit)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "案例采集模板.md"
        target.write_text(result["generated_markdown"], encoding="utf-8")
    if args.format == "markdown":
        print(result["generated_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
