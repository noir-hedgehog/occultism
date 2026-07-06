# Tool Spec：nine_star_ki_request_guard

## 目的

识别九星气学、九宫命星、本命星、年星和方位请求，判断是否能继续低风险象征咨询。

## 输入

- `request_text` 或 `text`：用户原始请求。

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_nine_star_ki`
- `reframed_question`
- `required_boundaries`
- `clarifying_questions`
- `next_steps`

## 安全边界

- 不替代医疗、法律、财务、安全、心理健康、紧急支持、搬迁决策或当事人沟通。
- 不用于投资赌博、关系贴标签、第三方窥探、操控、确定预言、方位恐吓、高价化解或反复依赖。
- 允许文化学习、已知命星/年星记录和低风险象征反思。
