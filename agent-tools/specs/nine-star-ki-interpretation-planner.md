# Tool Spec：nine_star_ki_interpretation_planner

## 目的

把九星气学 profile、已知命星、年星和方位焦点转成低风险象征解释计划。

## 输入

- 与 `nine_star_ki_profile_recorder` 相同。

## 输出

- `can_continue_nine_star_ki`
- `symbol_plans`
- `interpretation_plan`
- `limits`
- `next_steps`

## 安全边界

- 先声明九星只作象征反思，不作确定预言、方位恐吓、关系标签或专业建议。
- 保留体系来源、节气边界和缺失字段。
- 解释必须收束到现实证据、预算/时间约束、沟通边界和可撤回小动作。
