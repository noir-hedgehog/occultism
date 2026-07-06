# Tool Spec：casting_lots_interpretation_planner

## 作用

把符物抛掷记录和象征查询结果组合成安全、可审计的解释计划。

## 输入

与 `casting_lots_layout_recorder` 相同。

## 输出

- `is_valid`
- `can_continue_casting_lots`
- `symbol_plans`
- `interpretation_plan`
- `limits`
- `next_steps`

## 边界

- 解释必须使用象征性、可能性语言。
- 不输出确定预言、专业建议、灵异事实确认、赌博/投资建议、第三方读心或操控建议。
- 不鼓励反复抛掷直到满意。
