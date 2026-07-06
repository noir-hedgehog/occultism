# Tool Spec：numerology_profile_recorder

## 目的

记录脱敏数字材料、使用场景、数字片段和风险标记。工具不保存完整敏感号码，只保留必要尾号或用户明确给出的非敏感数字。

## 输入

- `number_text` / `request_text` / `text`
- `digits`
- `number_context`

## 输出

遵循 [numerology-profile-recorder.schema.json](../schemas/numerology-profile-recorder.schema.json)。

## 规则

1. 超过 6 位数字时要求脱敏为尾号或片段。
2. 若出现敏感标识，必须阻断。
3. 记录现实使用条件，不直接生成命运结论。

## 命令

```bash
python3 agent-tools/scripts/numerology_profile_recorder.py --text "比较手机号尾号 168 和 739，只看象征和记忆度"
```
