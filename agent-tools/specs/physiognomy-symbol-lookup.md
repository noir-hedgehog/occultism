# Tool Spec：physiognomy_symbol_lookup

## 目的

查询手相/面相符号的安全象征层、反思问题和禁止用途，供 Skill 生成非宿命论的文化解释。

## 输入

- `query` / `symbol` / `feature_code`
- `focus`

## 输出

遵循 [physiognomy-symbol-lookup.schema.json](../schemas/physiognomy-symbol-lookup.schema.json)。

## 规则

1. 支持掌纹、掌丘、额头、眉、眼、鼻、嘴、下巴和痣相等符号。
2. 所有解释必须标为传统象征或文化叙事，不升级为事实断言。
3. 禁止健康、寿命、财富保证、婚恋结论、人品判断和歧视性用途。

## 命令

```bash
python3 agent-tools/scripts/physiognomy_symbol_lookup.py --query "生命线" --focus "self_reflection"
```
