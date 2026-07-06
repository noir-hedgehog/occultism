# Tool Spec：oracle_lot_symbol_lookup

## 目的

查询签等、签文层、寺庙来源、月老签、事业签和抽签方法等求签符号的安全解释骨架。

## 输入

- `query` / `symbol`
- `focus`

## 输出

遵循 [oracle-lot-symbol-lookup.schema.json](../schemas/oracle-lot-symbol-lookup.schema.json)。

## 规则

1. 好签不保证成功，差签不恐吓灾祸。
2. 签文必须连接现实约束和低风险行动。
3. 不替代专业服务，不断定第三方真实想法。

## 命令

```bash
python3 agent-tools/scripts/oracle_lot_symbol_lookup.py --query 上签 --focus relationship_reflection
```
