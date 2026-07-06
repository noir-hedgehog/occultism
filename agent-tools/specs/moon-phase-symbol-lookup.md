# Tool Spec：moon_phase_symbol_lookup

## 作用

为常见月相和月亮事件提供安全象征提示，包括新月、娥眉月、上弦月、盈凸月、满月、亏凸月、下弦月、残月、月食、蓝月和超级月亮。

## 输出

- `canonical_name`
- `symbol_code`
- `category`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `action_guidance`
- `prohibited_uses`

## 边界

- 不把月相解释成显化保证、灾祸预言、医疗/生育建议、投资信号、关系命令或天文权威。
- 未知月相术语由 planner 作为来源特定说法处理，不编造固定意义。
