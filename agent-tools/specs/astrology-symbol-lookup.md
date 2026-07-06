# Tool Spec：astrology_symbol_lookup

## 目的

查询占星常见符号的安全解释骨架，包括十二星座、行星、四轴点、十二宫位和基础相位。此工具不生成星盘、不计算行运、不判断合盘结果，只提供低风险的象征语言、反思问题和行动提示。

## 输入

- `query` / `symbol`：术语，例如 `天秤`、`月亮`、`上升`、`十宫`、`合相`
- `category` / `symbol_type`：可选，`sign`、`planet`、`point`、`house`、`aspect`
- `focus`：可选，用户分析焦点，如 `career`、`relationship`、`self_understanding`

## 输出

遵循 [astrology-symbol-lookup.schema.json](../schemas/astrology-symbol-lookup.schema.json)。

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

1. 单一星盘符号只能作为象征提示，不能写成终身定性。
2. 不生成或推断精确星盘；如需排盘，要求用户提供外部星盘字段和来源。
3. 不输出医疗、法律、财务、婚育、寿命、灾祸或“绝配/必分”的确定性判断。
4. 第三方、未成年人和精确出生资料必须最小化，并优先要求同意。
5. 最终占星解读仍需通过 `mystic_intake_triage` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/astrology_symbol_lookup.py --query 天秤 --category sign --focus relationship
python3 agent-tools/scripts/astrology_symbol_lookup.py --query 月亮 --category planet --focus self_understanding
python3 agent-tools/scripts/astrology_symbol_lookup.py --query 十宫 --category house --focus career
```
