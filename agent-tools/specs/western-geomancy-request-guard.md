# Tool Spec：western_geomancy_request_guard

## 目的

识别西洋土占、盾形占、盾盘、geomancy、shield chart 和 geomantic figure 请求，判断是否能继续低风险象征咨询。

## 输入

- `request_text` 或 `text`：用户原始请求。

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_western_geomancy`
- `reframed_question`
- `required_boundaries`
- `clarifying_questions`
- `next_steps`

## 安全边界

- 不替代医疗、法律、财务、安全、心理健康、紧急支持或当事人沟通。
- 不用于投资赌博、第三方窥探、操控、确定预言、诅咒/驱邪证明或反复起盘依赖。
- 允许文化学习、已有盘面记录和低风险象征反思。
