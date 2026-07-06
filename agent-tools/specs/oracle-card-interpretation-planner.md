# oracle_card_interpretation_planner

把神谕卡抽牌记录、图像母题查找和现实锚点整理成可审查的解释计划。

## 输入

- `question_text` 或 `text`：用户问题。
- `deck_name`：牌组名称或来源。
- `spread_type`：牌阵类型。
- `cards`：用户已有抽牌、关键词或图像母题。
- `source`：抽牌来源。

## 输出

- `is_valid` / `can_continue_oracle_card`：是否可继续。
- `symbol_plans`：逐牌/逐母题解释计划。
- `interpretation_layers`：建议回答层次。
- `synthesis`：核心提示、母题数和现实落地动作。
- `limits`：输出限制。

## 边界

规划器不证明牌面对应现实事实，不替用户做医疗、法律、财务、安全或第三方关系决定。若守门器阻断，规划器必须保留阻断状态。
