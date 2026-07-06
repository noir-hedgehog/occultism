# rune_interpretation_planner

组合符文抽取记录和符号查询，生成现实优先、非决定论的卢恩符文解读计划。

## 输入

- `question_text`
- `runes`
- `spread_type`
- `focus`

## 输出

- `symbol_plans`
- `interpretation_layers`
- `synthesis`
- `limits`
- `next_steps`

## 边界

未知符文只提示确认来源；高风险请求由 `rune_request_guard` 暂停，不进入解读。
