# Tool Spec：mingli_symbol_lookup

## 目的

查询八字/四柱和紫微斗数常见术语的安全解释骨架，包括天干、地支、十神、紫微宫位和十四主星。此工具不排盘、不判断强弱旺衰、不做命运断言，只提供低风险的象征语言、反思问题和行动提示。

## 输入

- `query` / `symbol`：术语，例如 `甲`、`七杀`、`官禄宫`、`紫微`
- `category` / `symbol_type`：可选，`stem`、`branch`、`ten_god`、`ziwei_palace`、`ziwei_star`
- `focus`：可选，用户分析焦点，如 `career`、`relationship`、`self_understanding`

## 输出

遵循 [mingli-symbol-lookup.schema.json](../schemas/mingli-symbol-lookup.schema.json)。

关键字段：

- `canonical_name`
- `system`
- `symbol_layer`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `action_guidance`
- `prohibited_uses`

## 规则

1. 单一术语只能作为象征提示，不能写成终身定性。
2. 重名或歧义术语必须要求 `category`。
3. 不输出医疗、法律、财务、婚育、寿命或灾祸的确定性判断。
4. 未成年人和第三方资料必须使用非标签化、匿名化语言。
5. 最终命理解读仍需通过 `bazi_ziwei_intake_guard`、`bazi_ziwei_chart_record` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/mingli_symbol_lookup.py --query 七杀 --category ten_god --focus career
python3 agent-tools/scripts/mingli_symbol_lookup.py --query 官禄宫 --category ziwei_palace
python3 agent-tools/scripts/mingli_symbol_lookup.py --query 紫微 --category ziwei_star
```
