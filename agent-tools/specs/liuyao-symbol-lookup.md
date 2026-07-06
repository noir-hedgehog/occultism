# Tool Spec：liuyao_symbol_lookup

## 目的

查询六爻常见读盘术语的安全解释骨架，包括六亲、六神、世应/用神角色和六个爻位。此工具不排卦、不定旺衰、不判断吉凶成败，只提供低风险的象征语言、反思问题和行动提示。

## 输入

- `query` / `symbol`：术语，例如 `官鬼`、`兄弟爻`、`世爻`、`青龙`、`三爻`
- `category` / `symbol_type`：可选，`kinship`、`spirit`、`role`、`position`
- `focus`：可选，用户分析焦点，如 `career`、`relationship`、`project`

## 输出

遵循 [liuyao-symbol-lookup.schema.json](../schemas/liuyao-symbol-lookup.schema.json)。

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

1. 单一六爻术语只能作为解释入口，不能写成成败、疾病、财富或关系结局断言。
2. 解释前必须声明取用逻辑、外部卦盘来源和派别/方法限制。
3. 仍需用 `yijing_question_guard` 检查一事一问、重复占问和高风险请求。
4. 不输出医疗、法律、财务、婚育、寿命或灾祸的确定性判断。
5. 最终六爻解读仍需通过 `mystic_intake_triage` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/liuyao_symbol_lookup.py --query 官鬼 --category kinship --focus project
python3 agent-tools/scripts/liuyao_symbol_lookup.py --query 世爻 --category role
python3 agent-tools/scripts/liuyao_symbol_lookup.py --query 青龙 --category spirit
```
