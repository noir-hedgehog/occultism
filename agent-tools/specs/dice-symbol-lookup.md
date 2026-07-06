# Tool Spec：dice_symbol_lookup

## 作用

查询星骰常见行星、星座和宫位骰面的安全解释提示。

## 输出

- `canonical_name`
- `symbol_code`
- `category`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `prohibited_uses`

## 边界

- 不把骰面写成确定预言、诊断、财富结果、赌博建议或第三方事实。
- 自定义骰面必须先要求体系说明，不编造固定权威含义。
