# Tool Spec：planetary_retrograde_context_recorder

## 作用

记录低风险水逆/行星逆行请求中的逆行主题、关注领域、现实事项、情绪、现实限制、可控行动、复盘时间和停止查询条件。

## 输出

- `can_continue_planetary_retrograde`
- `retrograde_focus`
- `affected_areas`
- `current_events`
- `emotions`
- `reality_constraints`
- `practical_actions`
- `review_time`
- `stop_condition`
- `missing_fields`

## 边界

- 只记录用户提供的星象语境和现实事项。
- 缺少现实限制、可控行动、复盘时间或停止条件时，标记 `missing_fields`。
- 若守门器识别宿命归因、专业替代或恐慌依赖风险，则暂停后续解释。
