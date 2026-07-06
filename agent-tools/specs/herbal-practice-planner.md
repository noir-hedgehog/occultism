# Tool Spec：herbal_practice_planner

## 目的

把草本 context、植物象征、容器形式、使用方式和安全背景组合成非接触、无火、不入口、不外敷、可停止、低成本的低风险草本象征计划。

## 输入

- 与 `herbal_context_recorder` 相同。

## 输出

- `can_continue_herbal`
- `symbol_plans`
- `practice_plan`
- `limits`
- `next_steps`

## 安全边界

- 先声明草本/植物魔法只作文化象征和提醒物，不作治疗、驱邪、净化保证、开运、爱情咒、诅咒或专业建议。
- 计划必须保留来源、非接触、无火、不入口、不外敷、时长、停止条件、预算和不购买选项。
- 遇到内服、外敷、野采辨毒、孕婴宠物过敏、医疗替代、焚烧烟熏、驱邪恐惧、高价购买、第三方操控或反复依赖时暂停。
