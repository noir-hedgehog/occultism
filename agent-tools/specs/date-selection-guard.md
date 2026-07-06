# Tool Spec：date_selection_guard

## 目的

识别择日、黄历、吉日选择请求中的专业替代、决定论和危险仪式风险。此工具只决定是否可以继续做民俗象征层面的择日整理，不负责计算黄历。

## 输入

- `request_text` / `text`：用户原始请求
- `event_type`：可选，`moving`、`opening`、`wedding`、`travel`、`contract` 等

## 输出

遵循 [date-selection-guard.schema.json](../schemas/date-selection-guard.schema.json)。

关键字段：

- `event_type`
- `can_continue_date_selection`
- `risk_flags`
- `required_boundaries`
- `clarifying_questions`

## 规则

1. 医疗、财务、危险仪式或专业替代请求必须暂停择日。
2. 不承诺必发财、必顺利、必旺、必成或必凶。
3. 合同、消防、交通、证件、场地和人身安全等现实约束优先于民俗偏好。
4. 外部黄历或师承说法必须标注来源，不升级为通用事实。

## 命令

```bash
python3 agent-tools/scripts/date_selection_guard.py --text "想选一个搬家吉日，周末最好"
```
