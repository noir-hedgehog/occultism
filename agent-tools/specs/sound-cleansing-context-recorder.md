# Tool Spec：sound_cleansing_context_recorder

## 作用

记录低风险声响净化/空间复位请求中的空间、声音工具、意图、音量时长、身体感受、邻里/宠物/婴儿边界、收尾动作、复盘时间和停止条件。

## 输入

- `context_text` / `request_text` / `text`
- `space_context`
- `sound_tools`
- `practice_intention`
- `volume_duration`
- `safety_boundaries`
- `sensory_notes`
- `grounding_actions`
- `review_time`
- `stop_condition`
- `focus`

## 输出

- `is_valid`
- `can_continue_sound_cleansing`
- `missing_fields`
- `risk_flags`
- `safety_notes`
- `next_steps`

## 边界

只记录用户可控、低音量、短时、可停止的空间复位语境，不确认灵体、疾病原因或净化效果。
