# Tool Spec：wealth_luck_context_recorder

## 作用

记录低风险招财/财运请求中的求财焦点、当前现实语境、收入渠道、预算边界、已有象征物、可控行动、风险备注、复盘时间和停止条件。

## 输出

- `wealth_focus`
- `current_context`
- `income_channels`
- `budget_boundaries`
- `existing_symbols`
- `practical_actions`
- `risk_notes`
- `review_time`
- `stop_condition`
- `missing_fields`

## 边界

- 只记录预算和行动，不记录敏感财务账号或投资建议。
- 风险请求直接返回暂停和现实支持转译。
- 招财物件必须限制为已有、低成本、可撤回的提醒物。
