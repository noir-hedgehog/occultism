# Tool Spec：paradigm_selector

## 目的

把一个具体用户问题映射到适用的咨询范式，并明确哪些部分可以程序化自动运行，哪些部分需要 agent 结合 SOP 和知识卡完成，哪些部分建议人工审校。

它位于 `mystic_intake_triage` 和具体流派工具之间，解决“用户的问题到底该用哪种处理框架”的中间层问题。

## 输入

- `request_text`：用户请求文本。
- `requested_domain`：可选，用户指定的流派。
- `root`：仓库根目录，默认当前目录。

## 输出

遵循 [paradigm-selector.schema.json](../schemas/paradigm-selector.schema.json)。

关键字段：

- `trunk`：六条主干之一。
- `question_type`：具体问题类型。
- `recommended_paradigm`：推荐范式。
- `execution_boundary`：自动化、agent 和人工审校边界。
- `evidence_track`：科学化/实用验证、溯源审计、神秘边界和案例验证标记。

## 范式

- `safety_pause`：安全/专业边界暂停范式。
- `source_context`：来源语境与勘误范式。
- `practical_audit`：现实观察与低风险行动范式。
- `somatic_reflection`：身体/睡眠体验记录范式。
- `symbolic_media`：媒介记录与象征反思范式。
- `decision_reflection`：问题澄清与决策镜像范式。
- `cultural_omen`：民俗语境与安全回应范式。
- `symbolic_reflection`：低风险象征反思范式。

## 命令

```bash
python3 agent-tools/scripts/paradigm_selector.py --text "帮我做一个塔罗三张牌，看看工作状态"
```

