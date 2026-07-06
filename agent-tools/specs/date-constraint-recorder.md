# Tool Spec：date_constraint_recorder

## 目的

记录择日请求中的现实约束：事件类型、候选日期、不可用日期、参与人、场地/交通/证件/长辈时间、安全要求和外部黄历来源。此工具不排序，只建立可审计输入。

## 输入

- `request_text` / `text`：用户请求或约束描述
- `event_type`：可选事件类型
- `candidate_dates`：候选日期，格式 `YYYY-MM-DD`
- `unavailable_dates`：不可用日期
- `participants`：参与人标签
- `practical_constraints`：现实约束
- `source_notes`：黄历或师承来源说明

## 输出

遵循 [date-constraint-recorder.schema.json](../schemas/date-constraint-recorder.schema.json)。

关键字段：

- `candidate_dates`
- `unavailable_dates`
- `practical_constraints`
- `source_notes`
- `risk_flags`
- `missing_fields`

## 规则

1. 候选日期必须来自用户、现实窗口或外部来源，不凭空生成“权威吉日”。
2. 现实约束缺失时先补问。
3. 风险守门失败时不继续排序。

## 命令

```bash
python3 agent-tools/scripts/date_constraint_recorder.py --text "想在 2026-08-08 或 2026-08-15 搬家，周末最好，老人也要方便"
```
