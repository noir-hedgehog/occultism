# Tool Spec：dowsing_context_recorder

## 目的

记录低风险占杖/寻水杖/探测棒象征咨询所需的工具类型、观察目标、授权空间、动作记录、安全背景和现实约束。

## 输入

- `question_text`、`request_text` 或 `text`
- `tool_type`
- `observation_target`
- `space_or_map`
- `movement_notes`
- `authorization_context`
- `focus`
- `safety_context`
- `reality_constraints`
- `duration`

## 输出

- `can_continue_dowsing`
- `tool_type`
- `observation_target`
- `space_or_map`
- `movement_notes`
- `authorization_context`
- `missing_fields`
- `risk_flags`

## 安全边界

- 记录不等于定位；若文本涉及地下管线、开挖打井、水源矿脉、医疗地气、房产合同、第三方定位、驱邪恐惧、高价购买或反复依赖，必须暂停。
