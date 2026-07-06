# Tool Spec：crystal_request_guard

## 作用

识别水晶/能量石咨询意图，并在治病、专业替代、招财保证、危险摄入、高价购买压力、操控他人、超自然恐惧或反复依赖时暂停流程。

## 输入

- `request_text`：用户请求文本。

## 输出

- `can_continue_crystal`
- `risk_flags`
- `reframed_question`
- `required_boundaries`
- `clarifying_questions`
- `next_steps`

## 边界

- 水晶只作为象征、审美、提醒物和低风险仪式感辅助。
- 不替代医疗、法律、财务、安全或心理健康支持。
- 不鼓励摄入、磨粉、贴伤口、身体侵入式使用、高价购买压力或反复依赖。
