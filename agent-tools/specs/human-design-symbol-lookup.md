# Tool Spec：human_design_symbol_lookup

## 目的

查询人类图类型、内在权威、人生角色、中心、通道和闸门层级的低风险象征提示。

## 输入

- `query`、`symbol` 或 `type`
- `focus`

## 输出

- `canonical_name`
- `symbol_code`
- `category`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `action_guidance`
- `prohibited_uses`
- `next_steps`

## 安全边界

- 对未知符号抛错，由 planner 作为外部或自定义术语处理。
- 不把类型、权威、中心、通道或闸门写成确定人格、诊断、关系筛选或职业/财务保证。
