# Tool Spec：oracle_lot_record_builder

## 目的

记录求签/签文咨询中的问题、签文、签号、签等、来源和抽签方法。工具只记录用户提供的材料，不伪造签本来源或签诗全文。

## 输入

- `question_text` / `request_text`
- `lot_text`
- `source_type`
- `source_label`
- `lot_number`
- `lot_grade`

## 输出

遵循 [oracle-lot-record-builder.schema.json](../schemas/oracle-lot-record-builder.schema.json)。

## 规则

1. 先复用 `oracle_lot_request_guard` 判断风险。
2. 来源不明时标记 `missing_fields`，不得升格为寺庙权威。
3. 模拟抽签必须标记为模拟，不等同真实寺庙签。

## 命令

```bash
python3 agent-tools/scripts/oracle_lot_record_builder.py --question "关系下一步怎么沟通" --lot-text "第十二签 上签 云开月明" --source-type temple
```
