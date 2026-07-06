# Tool Spec：meihua_symbol_lookup

## 目的

查询梅花易数常见取象术语的安全解释骨架，包括体卦、用卦、互卦、变卦、动爻、报数起卦、外应、五行生克和八卦象征。此工具不自动排卦、不判断成败吉凶，只提供低风险的象征语言、反思问题和行动提示。

## 输入

- `query` / `symbol`：术语，例如 `体卦`、`外应`、`生体`、`离`
- `category` / `symbol_type`：可选，`structure`、`method`、`relation`、`trigram`
- `focus`：可选，用户分析焦点，如 `career`、`relationship`、`project`

## 输出

遵循 [meihua-symbol-lookup.schema.json](../schemas/meihua-symbol-lookup.schema.json)。

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

1. 单一梅花易数术语只能作为解释入口，不能写成成败、疾病、财富或关系结局断言。
2. 解释前必须声明起卦方法、数字/时间/外应来源和方法限制。
3. 仍需用 `yijing_question_guard` 检查一事一问、重复占问和高风险请求。
4. 不输出医疗、法律、财务、婚育、寿命或灾祸的确定性判断。
5. 最终梅花解读仍需通过 `mystic_intake_triage` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/meihua_symbol_lookup.py --query 体卦 --category structure --focus project
python3 agent-tools/scripts/meihua_symbol_lookup.py --query 外应 --category method
python3 agent-tools/scripts/meihua_symbol_lookup.py --query 生体 --category relation
```
