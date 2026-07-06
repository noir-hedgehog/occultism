# Tool Spec：moon_phase_context_recorder

## 作用

记录月相/月亮周期请求中的低风险上下文，包括月相、主题、意图、现实约束、日期备注、来源备注和反思焦点。

## 输出

- `can_continue_moon_phase`
- `phases`
- `themes`
- `intentions`
- `practical_constraints`
- `date_note`
- `source_note`
- `risk_flags`
- `missing_fields`

## 边界

- 记录只证明用户提供了月相或周期信息，不进行实时天文计算。
- 涉及专业替代、危险仪式、显化保证、操控或付费压力时标记为不可继续。
