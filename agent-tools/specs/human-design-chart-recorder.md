# Tool Spec：human_design_chart_recorder

## 目的

记录人类图咨询中的资料来源、最小化资料范围、类型、策略、内在权威、人生角色、中心、通道、闸门、现实约束和缺失字段。

## 输入

- `question_text`、`request_text` 或 `text`
- `chart_source`
- `data_scope`
- `type` 或 `human_design_type`
- `strategy`
- `authority` 或 `inner_authority`
- `profile`
- `definition`
- `centers` 或 `defined_centers`
- `channels`
- `gates`
- `focus`
- `reality_constraints` 或 `constraints`
- `notes` 或 `chart_notes`

## 输出

- `can_continue_human_design`
- 标准化后的 `type`、`authority`
- 原始策略、人生角色、中心、通道、闸门和现实约束
- `missing_fields`
- `safety_notes`
- `next_steps`

## 安全边界

- 只记录用户自愿提供或外部图表已有的资料。
- 缺字段时标注，不强行要求精确出生资料。
- 守门失败时不继续解释计划。
