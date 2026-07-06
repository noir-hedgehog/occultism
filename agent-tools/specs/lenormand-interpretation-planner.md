# lenormand_interpretation_planner

把雷诺曼抽牌记录、牌义查找和相邻组合整理成可审查的解释计划。

## 输入

- `question_text` 或 `text`：用户问题。
- `spread_type`：牌阵类型。
- `cards`：用户已有抽牌。
- `source`：抽牌来源。

## 输出

- `is_valid` / `can_continue_lenormand`：是否可继续。
- `card_plans`：逐牌解释计划。
- `pair_plans`：相邻牌组合提示。
- `interpretation_layers`：建议回答层次。
- `synthesis`：核心提示、牌数、组合数和现实落地动作。
- `limits`：输出限制。

## 边界

规划器不证明牌面对应现实事实，不替用户做医疗、法律、财务、安全或第三方关系决定。若守门器阻断，规划器必须保留阻断状态。
