# Tool Spec：sigil_practice_planner

## 目的

组合 sigil 语境记录和符号查询，生成纸面或数字草稿、可擦除、无火、不伤害身体、不永久化、低成本、可停止的符号印记象征计划。

## 输入

- 与 `sigil_context_recorder` 相同。

## 输出

- `can_continue_sigil`
- `symbol_plans`
- `practice_plan`
- `limits`
- `next_steps`

## 安全边界

- 若请求涉及滴血、割伤、刻皮肤、纹身、焚烧、召唤、驱邪、诅咒、操控、违法财务、专业替代、结果保证、高价购买或反复依赖，必须拒绝生成计划并改为安全改写。
