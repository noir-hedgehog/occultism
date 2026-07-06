# Tool Spec：scrying_observation_recorder

## 作用

记录水晶球/镜面/水面凝视咨询中的问题、观察来源、安全状态、媒介、视觉符号、表面状态、感受记录和缺失字段。

## 输出

- `is_valid`
- `observation_source`
- `observation_state`
- `medium`
- `visual_notes`
- `surface_notes`
- `feeling_notes`
- `missing_fields`

## 边界

- 不引导继续凝视或追求特殊状态。
- 若请求被 `scrying_request_guard` 阻断，不继续进入象征解释。
