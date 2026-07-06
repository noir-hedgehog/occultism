# oracle_card_draw_recorder

记录神谕卡牌组、牌阵、牌名/关键词、位置、来源和缺失字段，供后续图像母题查询与解释规划使用。

## 输入

- `question_text` 或 `text`：用户问题。
- `deck_name`：牌组名称或来源。
- `spread_type`：`single_card`、`three_card_reflection`、`past_present_next`。
- `cards`：用户已有抽牌、牌名、关键词或图像母题。
- `source`：抽牌来源，默认 `user_reported_or_manual_draw`。

## 输出

- `is_valid`：记录是否完整且未触发阻断。
- `can_continue_oracle_card`：是否可继续神谕卡流程。
- `positions`：牌阵位置列表。
- `cards` / `card_count`：标准记录后的牌名或关键词列表。
- `missing_fields`：需要补充的牌组、牌名或牌阵字段。

## 边界

记录工具不抽牌、不生成随机结果、不宣称牌组权威。专业替代、第三方窥探、财务投机、超自然恐惧和反复依赖请求应保留阻断状态。
