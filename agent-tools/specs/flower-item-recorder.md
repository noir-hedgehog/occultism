# Tool Spec：flower_item_recorder

## 作用

记录一次低风险花语/植物象征咨询的花材、颜色、场景、对象、来源、预算和安全约束。

## 输入

- `intention_text` / `request_text` / `text`
- `flowers` / `items`
- `colors`
- `scene`
- `recipient`
- `source`
- `budget_note`
- `safety_constraints`
- `focus`

## 输出

- `can_continue_flower`
- `flowers`
- `colors`
- `scene`
- `recipient`
- `budget_note`
- `safety_constraints`
- `missing_fields`
- `safety_notes`

## 边界

- 缺少花材或场景时只标注缺失，不编造花语。
- 若守门器发现风险，记录器必须暂停后续解释。
