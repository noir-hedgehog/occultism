# Tool Spec：casting_lots_symbol_lookup

## 作用

查询符物抛掷中的常见物件、区域和关系象征，输出安全解释提示。

## 输入

- `query` / `symbol` / `object`
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

## 边界

- 未知符物必须回到用户约定含义，不编造权威解释。
- 不确认诅咒、附身、祖灵传讯、驱邪效果、第三方真实想法或命运结果。
