# Tool Spec：aroma_symbol_lookup

## 目的

查询常见气味、精油、香包、扩香、闻香纸和通风等安全层的低风险象征提示。

## 输入

- `query`、`symbol` 或 `scent`
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

- 对未知气味抛错，由 planner 作为私人联想、品牌名或自定义混香处理。
- 不把任何气味写成疗效、驱邪、净化保证、开运、关系操控或购买必要。
