# Tool Spec：aroma_context_recorder

## 目的

记录芳香/精油/香薰咨询中的气味物件、来源、使用方式、空间、时长、通风、安全背景、现实约束和缺失字段。

## 输入

- `question_text`、`request_text` 或 `text`
- `scent_items`、`oils` 或 `scents`
- `scent_source` 或 `source`
- `use_mode` 或 `method`
- `space` 或 `location`
- `duration` 或 `time_limit`
- `ventilation`
- `focus`
- `safety_context` 或 `safety_notes`
- `reality_constraints` 或 `constraints`
- `notes` 或 `context_notes`

## 输出

- `can_continue_aroma`
- `scent_items`
- `scent_source`
- `use_mode`
- `space`
- `duration`
- `ventilation`
- `safety_context`
- `missing_fields`
- `next_steps`

## 安全边界

- 记录安全背景，不做具体医疗、孕婴、宠物、过敏或皮肤使用判断。
- 缺字段时标注，不强行生成气味处方或混香配方。
- 守门失败时不继续使用计划。
