# Tool Spec：relationship_luck_context_recorder

## 作用

记录低风险桃花/姻缘/人缘请求中的关系焦点、当前语境、同意范围、沟通边界、已有象征物、可控行动、风险备注、复盘时间和停止条件。

## 输出

- `relationship_focus`
- `current_context`
- `consent_scope`
- `communication_boundaries`
- `existing_symbols`
- `practical_actions`
- `risk_notes`
- `review_time`
- `stop_condition`
- `missing_fields`

## 边界

- 记录事实和本人可控行动，不推断第三方心理。
- 缺少同意范围、沟通边界、停止条件时必须标记缺失。
- 守门器标记高风险时，记录结果不可作为有效咨询语境继续。
