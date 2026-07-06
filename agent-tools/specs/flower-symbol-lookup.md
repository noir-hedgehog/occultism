# Tool Spec：flower_symbol_lookup

## 作用

查询常见花材、植物和花色的安全象征解释。

## 输入

- `query` / `symbol` / `flower`
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

- 未收录花材必须回到实际花材、场景和用户第一联想，不编造固定花语。
- 不输出医疗疗愈、毒性/宠物安全、财富承诺、复合保证、驱邪证明或第三方读心。
