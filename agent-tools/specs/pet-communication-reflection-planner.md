# Tool Spec：pet_communication_reflection_planner

## 作用

组合宠物沟通语境记录和象征查询，生成低风险的行为观察、照护动作、情绪安放和兽医边界计划。

## 输出

- `symbol_plans`
- `reflection_plan`
- `care_actions`
- `limits`
- `next_steps`

## 边界

- 计划只能落到观察、照护、复盘和现实支持。
- 急症、走失定位、亡宠事实确认、第三方指认、高价付费或反复依赖必须暂停。
