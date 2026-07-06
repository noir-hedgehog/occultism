# Tool Spec：dice_roll_recorder

## 作用

记录星骰/占卜骰咨询中的问题、骰子体系、骰面、掷骰来源、焦点和缺失字段。

## 输出

- `question_text`
- `dice_system`
- `dice_faces`
- `roll_source`
- `focus`
- `missing_fields`
- `risk_flags`

## 边界

- 不自动补造缺失骰面。
- 对模拟掷骰必须保留用户同意和来源说明。
