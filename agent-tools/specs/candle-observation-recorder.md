# Tool Spec：candle_observation_recorder

## 作用

记录蜡烛火焰/蜡泪咨询中的问题、观察来源、安全状态、火焰描述、蜡泪形状、烟雾描述和缺失字段。

## 输出

- `is_valid`
- `observation_source`
- `observation_state`
- `flame_notes`
- `wax_shapes`
- `smoke_notes`
- `missing_fields`

## 边界

- 不生成点火或燃烧建议。
- 若请求被 `candle_request_guard` 阻断，不继续进入象征解释。
