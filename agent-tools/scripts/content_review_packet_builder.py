#!/usr/bin/env python3
"""Build human content-review packets for each mystic domain."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import knowledge_coverage_audit
import tool_manifest_builder


COMMON_CHECKS = [
    "安全边界：不替代医疗、法律、紧急安全或高风险财务建议。",
    "非决定论：不使用必然、注定、必死、必破财、一定有灾等恐吓式表达。",
    "来源透明：区分传统说法、现代解释、师承经验、网络断语和工具输出。",
    "流程一致：SOP、Skill、工具 spec/schema 和测试样例之间没有互相矛盾。",
    "行动建议：建议低成本、可逆、非伤害，并保留用户自主决策。",
]

DOMAIN_REVIEW_FOCUS = {
    "tarot": ["牌位优先于单牌关键词", "逆位不写成坏事定论", "多牌组合保留张力而非单一答案"],
    "fengshui": ["先描述可见事实再使用术语", "现实安全和动线优先", "理气派别字段不足时不硬排盘"],
    "ritual": ["不提供明火、烟雾、密闭空间、放血或危险材料步骤", "不确认鬼神实体伤害", "低风险替代流程清晰"],
    "folk_custom": ["民俗禁忌转成文化解释和家庭沟通", "网络/商业说法不升格", "孕期和儿童议题不替代专业建议"],
    "yijing": ["一事一问", "本卦、动爻、变卦分层", "原典/注疏/现代译注来源不混写"],
    "liuyao": ["不自动补造盘式", "候选用神保留派别限制", "世应、六亲、六神解释不写成绝对断事"],
    "meihua": ["外应先记录事实再取象", "体用关系转成资源/压力/证据问题", "不把偶然事件写成天意证明"],
    "qimen": ["排盘方法、派别和时间策略完整", "用神选择不混派", "没有完整盘式时不生成断语"],
    "mingli": ["出生资料最小化和同意", "不做寿命、灾祸、婚育定论", "八字和紫微跨系统边界清楚"],
    "naming": ["字义/读音/字形/文化偏好优先", "不承诺改名转运", "品牌名不替代商标/合规审查"],
    "astrology": ["出生资料和第三方隐私边界", "合盘不写成绝配或操控建议", "行星/宫位/相位解释保持象征性"],
}


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    coverage = knowledge_coverage_audit.audit(root_path)
    manifest = tool_manifest_builder.build(root_path)
    tool_status = {tool["name"]: tool["status"] for tool in manifest.get("tools", [])}
    packets: list[dict[str, Any]] = []
    for domain in coverage.get("domains", []):
        sections = domain["sections"]
        tools = [item["tool"] for item in sections["tools"]["present"]]
        incomplete_tools = [tool for tool in tools if tool_status.get(tool) != "ready"]
        packets.append(
            {
                "domain": domain["domain"],
                "display_name": domain["display_name"],
                "review_status": "ready_for_human_review" if domain["is_complete"] and not incomplete_tools else "blocked",
                "level": domain["level"],
                "files_to_review": {
                    "sop": sections["sop"]["present"],
                    "knowledge": sections["knowledge"]["present"],
                    "skill": sections["skill"]["present"],
                    "tool_specs": [item["spec"] for item in sections["tools"]["present"]],
                },
                "tool_chain": tools,
                "review_questions": COMMON_CHECKS + DOMAIN_REVIEW_FOCUS.get(domain["domain"], []),
                "required_evidence": [
                    "reviewer_name_or_role",
                    "review_date",
                    "approved_scope",
                    "required_corrections_or_no_change",
                    "residual_risks",
                ],
                "open_items": [
                    "content_expert_approval_missing",
                    "real_anonymized_examples_needed",
                ],
            }
        )
    result = {
        "tool": "content_review_packet_builder",
        "root": str(root_path),
        "is_valid": bool(coverage.get("is_valid")) and bool(manifest.get("is_valid")),
        "domain_count": len(packets),
        "ready_for_review_count": sum(1 for packet in packets if packet["review_status"] == "ready_for_human_review"),
        "approved_count": 0,
        "packets": packets,
        "common_review_checks": COMMON_CHECKS,
        "limits": [
            "审校包只准备人工审校材料，不表示内容已经由专家批准。",
            "ready_for_human_review 表示自动证据齐全，仍需审校人逐项签字或反馈。",
            "真实匿名 transcript、实际 Skill 安装和内容专家批准仍是独立开放事项。",
        ],
        "next_steps": [
            "assign_domain_reviewers",
            "record_reviewer_feedback",
            "convert_required_corrections_to_kanban_tasks",
        ],
    }
    result["generated_markdown"] = render_markdown(result)
    return result


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# 内容审校包",
        "",
        "本页把各流派的 SOP、知识卡、Skill 和工具 spec 汇总为人工审校入口。它证明材料已准备好被审，不证明已经审完。",
        "",
        "## 当前状态",
        "",
        "| 指标 | 当前值 |",
        "| --- | --- |",
        f"| 覆盖领域 | {result['domain_count']} |",
        f"| 可进入人工审校 | {result['ready_for_review_count']} |",
        f"| 已获内容批准 | {result['approved_count']} |",
        "",
        "## 通用审校问题",
        "",
    ]
    for check in result["common_review_checks"]:
        lines.append(f"- {check}")
    lines.extend(["", "## 流派审校清单", ""])
    for packet in result["packets"]:
        lines.extend(
            [
                f"### {packet['display_name']}",
                "",
                f"- 状态：`{packet['review_status']}`",
                f"- 成熟度：{packet['level']}",
                f"- 工具链：{', '.join(f'`{tool}`' for tool in packet['tool_chain'])}",
                "- 待审 SOP：" + ("、".join(f"[{Path(path).stem}]({path.removeprefix('知识库/')})" for path in packet["files_to_review"]["sop"]) or "无"),
                "- 待审知识卡：" + ("、".join(f"[{Path(path).stem}]({path.removeprefix('知识库/')})" for path in packet["files_to_review"]["knowledge"]) or "无"),
                "- 待审 Skill：" + ("、".join(f"[{Path(path).parts[1]}](../{path})" for path in packet["files_to_review"]["skill"]) or "无"),
                "",
                "审校问题：",
                "",
            ]
        )
        for question in packet["review_questions"]:
            lines.append(f"- {question}")
        lines.extend(["", "需要记录的证据：", ""])
        for evidence in packet["required_evidence"]:
            lines.append(f"- `{evidence}`")
        lines.extend(["", "开放项：", ""])
        for item in packet["open_items"]:
            lines.append(f"- `{item}`")
        lines.append("")
    lines.extend(["## 限制", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    parser.add_argument("--write", action="store_true", help="Write markdown output to 知识库/内容审校包.md.")
    args = parser.parse_args()
    result = build(args.root)
    if args.write:
        target = Path(args.root).resolve() / "知识库" / "内容审校包.md"
        target.write_text(result["generated_markdown"], encoding="utf-8")
    if args.format == "markdown":
        print(result["generated_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
