# Tool Spec：crystal_item_recorder

## 作用

记录水晶/能量石咨询中的意图、物件名称、使用场景、来源、预算或已有物件说明，并继承请求守门风险。

## 输入

- `intention_text`：用户意图或咨询问题。
- `items`：已有或候选水晶名称、颜色或商家名。
- `use_context`：佩戴、桌面、床头、礼物、冥想等场景。
- `budget_note`：已有物件、预算或不购买说明。

## 输出

- `is_valid`
- `can_continue_crystal`
- `items`
- `use_context`
- `budget_note`
- `missing_fields`
- `risk_flags`
- `next_steps`

## 边界

记录不等于推荐购买；缺少预算或已有物件说明时必须追问，避免制造购买压力。
