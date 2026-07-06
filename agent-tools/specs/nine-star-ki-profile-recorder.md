# Tool Spec：nine_star_ki_profile_recorder

## 目的

记录九星气学咨询中的出生年份或已知命星、体系来源、年星、方位焦点、现实约束和缺失字段。

## 输入

- `question_text`、`request_text` 或 `text`：用户问题。
- `birth_year`、`birth_month`：出生时间线索，可为空。
- `home_star`、`month_star`、`annual_star`：用户已知命星或外部资料。
- `system_variant`、`source`、`current_year`、`directions`、`focus`、`reality_constraints`、`notes`：可选上下文。

## 输出

- `can_continue_nine_star_ki`
- `birth_year`
- `home_star`
- `month_star`
- `annual_star`
- `directions`
- `reality_constraints`
- `missing_fields`
- `safety_notes`
- `next_steps`

## 安全边界

- 不自行制造节气边界或派别精算权威；资料不全时标注缺失。
- 不把本命星写成人格定论、关系筛选或命运证明。
- 若守门器阻断，则暂停 profile 解释流程。
