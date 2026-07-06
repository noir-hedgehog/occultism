# Tool Spec：numerology_symbol_lookup

## 目的

查询 0-9 数字、手机号尾号、车牌、门牌和生命灵数等数字象征的安全解释骨架。

## 输入

- `query` / `symbol`
- `focus`

## 输出

遵循 [numerology-symbol-lookup.schema.json](../schemas/numerology-symbol-lookup.schema.json)。

## 规则

1. 数字解释只作为文化联想和偏好提示。
2. 现实约束优先于数字象征。
3. 不承诺财富、运势、关系、健康或命运结果。

## 命令

```bash
python3 agent-tools/scripts/numerology_symbol_lookup.py --query 8 --focus phone_suffix
```
