# Tool Spec：crystal_use_planner

## 作用

组合水晶物件记录和象征查询，生成低风险使用计划：审美、提醒物、空间秩序、自我照顾动作和现实核查。

## 输入

- `intention_text`
- `items`
- `use_context`
- `budget_note`
- `focus`

## 输出

- `is_valid`
- `can_continue_crystal`
- `symbol_plans`
- `use_plan`
- `limits`
- `next_steps`

## 边界

- 优先已有物件或低成本替代。
- 使用方式限于外部佩戴、摆放、记录或短时反思。
- 不建议水晶水、吞服、磨粉、贴伤口、身体侵入式做法、危险充能或高价购买。
