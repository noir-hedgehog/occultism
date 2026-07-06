# Tool Spec：spiritual_protection_context_recorder

## 作用

记录低风险恶眼/能量防护/断联请求中的防护主题、触发场景、身体/情绪感受、现实安全背景、边界动作、提醒物、复盘时间和停止条件。

## 输出

- `can_continue_spiritual_protection`
- `protection_focus`
- `trigger_context`
- `sensations`
- `emotions`
- `reality_safety_context`
- `boundary_actions`
- `symbolic_items`
- `review_time`
- `stop_condition`
- `missing_fields`

## 边界

- 缺少现实安全背景、边界动作、复盘时间或停止条件时，标记 `missing_fields`。
- 若守门器识别第三方指认、诅咒报复、危险仪式或恐惧依赖风险，则暂停后续解释。
