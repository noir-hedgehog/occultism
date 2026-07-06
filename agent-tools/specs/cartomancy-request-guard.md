# Tool Spec：cartomancy_request_guard

## 作用

守门扑克牌占卜、纸牌占卜和 cartomancy 请求，识别专业替代、财务赌博、第三方隐私、操控、确定预言和反复抽牌依赖风险。

## 输出

- `can_continue_cartomancy`
- `risk_flags`
- `reframed_question`
- `required_boundaries`
- `next_steps`

## 边界

- 扑克牌只作为象征反思，不证明事实或预测结果。
- 医疗、法律、财务、安全、心理健康、赌博、第三方窥探、操控和反复依赖请求必须暂停。
