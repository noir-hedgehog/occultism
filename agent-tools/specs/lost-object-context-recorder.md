# Tool Spec：lost_object_context_recorder

## 作用

记录低风险失物/寻物请求中的物品描述、最后看见时间地点、路线语境、可能区域、已搜索区域、可联系渠道、现实行动、风险备注、复盘时间和停止条件。

## 输入

- `context_text` / `request_text` / `text`
- `item_description`
- `last_seen`
- `route_context`
- `possible_areas`
- `checked_areas`
- `contact_channels`
- `practical_actions`
- `risk_notes`
- `review_time`
- `stop_condition`

## 输出

- 结构化寻物语境
- `risk_flags`
- `missing_fields`
- `safety_notes`
- `next_steps`

## 边界

- 缺字段时只提示补充，不编造地点、嫌疑人或方位。
- 若触发寻人、走失宠物急症、犯罪证据、隐私定位、专业替代或保证找到，必须暂停。
