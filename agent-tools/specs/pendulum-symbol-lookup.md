# Tool Spec：pendulum_symbol_lookup

## 目的

查询灵摆摆动、yes/no/不确定和校准层的安全象征解释，帮助 agent 使用倾向、提醒、证据缺口和低风险行动语言。

## 输入

- `query` / `symbol`
- `focus`：可选

## 输出

遵循 [pendulum-symbol-lookup.schema.json](../schemas/pendulum-symbol-lookup.schema.json)。

## 规则

1. 摆动只作为象征提示，不作为事实证明。
2. 不把不动、乱晃写成有邪灵、被阻挡或坏预兆。
3. 不把 yes/no 写成专业建议或最终决定。

## 命令

```bash
python3 agent-tools/scripts/pendulum_symbol_lookup.py --query "左右" --focus "relationship_boundary"
```
