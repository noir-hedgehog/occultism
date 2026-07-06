# Tool Spec：aroma_practice_planner

## 目的

把芳香 context、气味象征、使用方式和安全背景组合成非接触、短时、可停止、低成本的低风险气味象征计划。

## 输入

- 与 `aroma_context_recorder` 相同。

## 输出

- `can_continue_aroma`
- `symbol_plans`
- `practice_plan`
- `limits`
- `next_steps`

## 安全边界

- 先声明芳香/精油只作气味象征和环境提醒，不作治疗、驱邪、净化保证、开运或专业建议。
- 计划必须保留通风、时长、停止条件、预算和不购买选项。
- 遇到内服、皮肤危险用法、孕婴宠物过敏、医疗替代、驱邪恐惧、高价购买或反复依赖时暂停。
