# Tool Spec：consecration_context_recorder

## 作用

记录低风险开光/加持/净物请求中的物件焦点、来源语境、当前用途、已有物件、安全边界、象征动作、风险备注、复盘时间和停止条件。

## 输出

- `object_focus`
- `source_context`
- `current_use`
- `existing_items`
- `safety_boundaries`
- `symbolic_actions`
- `risk_notes`
- `review_time`
- `stop_condition`
- `missing_fields`

## 边界

- 记录物件来源和照料计划，不确认邪气、封印、神明命令或灵验效果。
- 缺少安全边界、象征动作、复盘时间或停止条件时必须标记缺失。
- 守门器标记高风险时，记录结果不可作为有效咨询语境继续。
