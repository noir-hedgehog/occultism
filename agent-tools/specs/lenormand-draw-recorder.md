# lenormand_draw_recorder

记录雷诺曼牌阵、位置、牌名、抽牌来源和缺失字段，供后续牌义查找与组合规划使用。

## 输入

- `question_text` 或 `text`：用户问题。
- `spread_type`：`three_card_line`、`five_card_line`、`nine_card_box` 等。
- `cards`：用户已有抽牌，可用空格、逗号或中文顿号分隔。
- `source`：抽牌来源，默认 `user_reported_or_manual_draw`。

## 输出

- `is_valid`：记录是否完整且未触发阻断。
- `can_continue_lenormand`：是否可继续雷诺曼流程。
- `positions`：牌阵位置列表。
- `cards` / `card_count`：标准记录后的牌列表和数量。
- `missing_fields`：需要补充的问题、牌阵或牌名字段。

## 边界

记录工具不抽牌、不生成随机结果、不判断事实。专业替代、第三方窥探、财务投机、超自然恐惧和反复依赖请求应保留阻断状态。
