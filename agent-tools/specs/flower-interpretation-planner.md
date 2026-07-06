# Tool Spec：flower_interpretation_planner

## 作用

把花材记录和花语象征查询结果组合成安全、可审计的花语/植物象征解释计划。

## 输入

与 `flower_item_recorder` 相同。

## 输出

- `is_valid`
- `can_continue_flower`
- `symbol_plans`
- `flower_plan`
- `limits`
- `next_steps`

## 边界

- 解释必须使用文化、象征和可能性语言。
- 现实约束优先于花语，包括过敏、宠物、儿童、香味、场合和预算。
- 不输出确定预言、专业建议、医疗疗愈、毒性判断、复合保证、驱邪证明、第三方读心或高价购买压力。
