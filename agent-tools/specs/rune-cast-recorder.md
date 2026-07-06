# rune_cast_recorder

记录低风险卢恩符文抽取会话，包括问题、牌阵、符文列表、位置和来源。

## 输入

- `question_text` / `request_text` / `text`
- `runes` 或 `drawn_runes`
- `spread_type`：`single_rune`、`three_rune`、`past_present_future`
- `orientation_policy`

## 输出

- `spread_type`、`positions`、`runes`、`rune_count`
- `missing_fields`
- `risk_flags`
- `next_steps`

## 边界

不自动生成随机抽取，不补造未知符文；用户没有提供抽取结果时只记录缺失字段。
