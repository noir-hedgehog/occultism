# Tool Spec：incense_observation_recorder

## 作用

记录香火/香灰/烟形咨询中的问题、观察来源、安全状态、香灰形状、烟雾描述、香头余光和缺失字段。

## 输出

- `is_valid`
- `observation_source`
- `observation_state`
- `ash_shapes`
- `smoke_notes`
- `ember_notes`
- `missing_fields`

## 边界

- 不生成点香、燃烧或烟熏建议。
- 若请求被 `incense_request_guard` 阻断，不继续进入象征解释。
