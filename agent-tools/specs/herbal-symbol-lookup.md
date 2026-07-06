# Tool Spec：herbal_symbol_lookup

## 目的

查询常见草本、香草、叶片、草药袋、盐碗和植物意图卡等低风险象征提示。

## 输入

- `query`、`symbol` 或 `plant`
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

- 对未知植物抛错，由 planner 作为私人联想、地方俗称、品牌名或自定义组合处理。
- 不把任何草本写成疗效、驱邪、净化保证、开运、爱情咒、诅咒、关系操控或购买必要。
