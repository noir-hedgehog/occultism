# Tool Spec：talisman_record_builder

## 作用

记录护符/符箓咨询中的意图、物件名称或可见符号、来源、使用场景、预算或已有物件说明，并继承请求守门风险。

## 输入

- `intention_text`
- `items`
- `source_type`
- `source_label`
- `use_context`
- `budget_note`

## 输出

- `is_valid`
- `can_continue_talisman`
- `items`
- `source_type`
- `use_context`
- `missing_fields`
- `risk_flags`

## 边界

记录来源不等于证明灵验；缺少来源或预算说明时必须追问。
