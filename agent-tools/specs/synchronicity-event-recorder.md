# Tool Spec：synchronicity_event_recorder

## 作用

记录低风险同步性请求中的重复符号、出现频率、出现场景、情绪、现实锚点、可控行动和停止条件。

## 输出

- `can_continue_synchronicity`
- `repeated_signs`
- `frequency_context`
- `situation_context`
- `emotions`
- `reality_anchor`
- `practical_actions`
- `stop_condition`
- `missing_fields`

## 边界

- 只记录自然出现的符号和用户语境。
- 缺少现实锚点、可控行动或停止条件时，标记 `missing_fields`。
- 若守门器识别危险寻找、命令化或专业替代风险，则暂停后续解读。
