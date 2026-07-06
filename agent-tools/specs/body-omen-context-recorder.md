# Tool Spec：body_omen_context_recorder

## 目的

记录一次低风险身体征兆民俗象征语境，保留征兆类型、身体位置、时间、持续频率、普通诱因、健康边界和停止条件。

## 输入

- `question_text`、`request_text` 或 `text`
- 可选：`omen_type`、`body_location`、`timing`、`duration`、`sensation_notes`、`health_context`、`mundane_context`、`focus`、`reality_constraints`、`stop_condition`

## 输出

- `can_continue_body_omen`
- `omen_type`
- `body_location`
- `timing`
- `sensation_notes`
- `health_context`
- `mundane_context`
- `missing_fields`
- `safety_notes`

## 安全边界

- 只记录用户本人自愿提供的低风险身体征兆，不诊断、不治疗、不替代检查。
- 持续、突发、严重或影响功能的症状必须优先转向现实医疗支持。
