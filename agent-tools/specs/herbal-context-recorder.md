# Tool Spec：herbal_context_recorder

## 目的

记录草本/香草/植物魔法咨询中的植物物件、来源、使用方式、容器形式、空间、时长、安全背景、现实约束和缺失字段。

## 输入

- `question_text`、`request_text` 或 `text`
- `plant_items`、`herbs` 或 `items`
- `plant_source` 或 `source`
- `use_mode` 或 `method`
- `container_or_form` 或 `form`
- `space` 或 `location`
- `duration` 或 `time_limit`
- `focus`
- `safety_context` 或 `safety_notes`
- `reality_constraints` 或 `constraints`
- `notes` 或 `context_notes`

## 输出

- `can_continue_herbal`
- `plant_items`
- `plant_source`
- `use_mode`
- `container_or_form`
- `space`
- `duration`
- `safety_context`
- `missing_fields`
- `next_steps`

## 安全边界

- 记录安全背景，不做具体医疗、孕婴、宠物、过敏、采摘辨毒、内服或外敷判断。
- 缺字段时标注，不强行生成草药配方、咒语或灵验承诺。
- 守门失败时不继续使用计划。
