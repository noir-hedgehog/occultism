# Tool Spec：date_option_ranker

## 目的

在候选日期已知的前提下，按现实约束和用户提供的象征偏好排序。此工具不计算权威黄历，不承诺吉凶结果。

## 输入

接受 `date_constraint_recorder` 的输入字段，并额外支持：

- `symbolic_preferences`：例如 `纪念`、`避开冲`

## 输出

遵循 [date-option-ranker.schema.json](../schemas/date-option-ranker.schema.json)。

关键字段：

- `can_rank_dates`
- `candidate_count`
- `ranked_dates`
- `selection_guidance`
- `limits`

## 规则

1. 现实不可用日期必须排在后面或标出 caution。
2. 现实安全、手续、场地和参与人约束优先于象征偏好。
3. 输出只能使用“更适合”“可优先考虑”“需确认”一类措辞。
4. 不使用“必吉”“必凶”“保证顺利”“一定发财”等措辞。

## 命令

```bash
python3 agent-tools/scripts/date_option_ranker.py --text "想在 2026-08-08 或 2026-08-15 搬家，周末最好" --candidate-date 2026-08-08 --candidate-date 2026-08-15
```
