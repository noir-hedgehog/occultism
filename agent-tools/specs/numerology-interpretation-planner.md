# Tool Spec：numerology_interpretation_planner

## 目的

把数字材料记录和数字象征查询组合成安全解释计划。计划用于文化学习、偏好整理和低风险号码选择，不用于命运定论或专业决策。

## 输入

接受 `numerology_profile_recorder` 的输入字段：

- `number_text`
- `digits`
- `number_context`
- `focus`

## 输出

遵循 [numerology-interpretation-planner.schema.json](../schemas/numerology-interpretation-planner.schema.json)。

## 规则

1. 记录器阻断时，计划器必须阻断。
2. 输出前先确认脱敏，不展示完整敏感号码。
3. 解释顺序必须是现实条件优先，数字象征次之。

## 命令

```bash
python3 agent-tools/scripts/numerology_interpretation_planner.py --text "比较手机号尾号 168 和 739，只看象征和记忆度"
```
