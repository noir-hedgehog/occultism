# Tool Spec：dream_symbol_lookup

## 目的

查询常见梦境符号的安全解释骨架，包括水、追赶、坠落、掉牙、考试、房子、蛇、死亡、飞行和迷路等。此工具只提供象征层、反思问题和低风险行动提示。

## 输入

- `query` / `symbol`：梦境符号，例如 `水`、`掉牙`、`考试`、`蛇`
- `focus`：可选，用户关注点，例如 `relationship`、`career`、`self_reflection`

## 输出

遵循 [dream-symbol-lookup.schema.json](../schemas/dream-symbol-lookup.schema.json)。

关键字段：

- `canonical_name`
- `symbol_code`
- `symbol_layer`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `action_guidance`
- `prohibited_uses`

## 规则

1. 梦境符号只能作为象征提示，不能写成预言或诊断。
2. 同一符号必须优先结合用户个人联想和现实背景。
3. 与死亡、灾祸、疾病、诅咒、第三方意图相关的解释必须降级为可能的感受或转变象征。
4. 最终解读仍需通过 `mystic_intake_triage` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/dream_symbol_lookup.py --query 掉牙 --focus self_reflection
python3 agent-tools/scripts/dream_symbol_lookup.py --query 海 --focus emotional_pressure
```
