# Tool Spec：cezi_interpretation_planner

## 作用

把测字/拆字记录和部件象征查询结果组合成安全、可审计的解释计划。

## 输入

与 `cezi_character_recorder` 相同。

## 输出

- `is_valid`
- `can_continue_cezi`
- `symbol_plans`
- `interpretation_plan`
- `limits`
- `next_steps`

## 边界

- 解释必须使用象征性、可能性语言。
- 不输出确定预言、专业建议、灵异事实确认、寿命判断、人格优劣、儿童标签、第三方读心或操控建议。
- 不鼓励反复测字直到满意。
