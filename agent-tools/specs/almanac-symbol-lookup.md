# Tool Spec：almanac_symbol_lookup

## 目的

解释择日和黄历常见术语，例如 `宜`、`忌`、`冲`、`煞`、`黄道吉日`、`黑道日`、`建除十二神`、`值神`。此工具只提供术语层解释和安全边界，不判断某日是否权威吉凶。

## 输入

- `query` / `term`：黄历术语
- `source_type`：可选，`user_provided_almanac`、`family_oral`、`online_claim`、`unknown`

## 输出

遵循 [almanac-symbol-lookup.schema.json](../schemas/almanac-symbol-lookup.schema.json)。

关键字段：

- `canonical_name`
- `symbol_layer`
- `source_type`
- `interpretation_prompt`
- `action_guidance`
- `prohibited_uses`

## 规则

1. 不把术语解释成必然结果。
2. 必须说明黄历来源、派别、地区和版本可能不一致。
3. 不替代医疗、法律、财务、合同、消防、交通或人身安全安排。

## 命令

```bash
python3 agent-tools/scripts/almanac_symbol_lookup.py --query 黄道吉日 --source-type user_provided_almanac
```
