# Tool Spec：bibliomancy_request_guard

## 作用

在书占、随机翻书、书页占卜和 bibliomancy 请求进入咨询前，识别专业替代、医疗心理健康、财务法律、决定论、第三方隐私、经文/经典权威命令、长段版权文本和反复依赖风险。

## 输出

- `can_continue_bibliomancy`
- `consultation_intent`
- `risk_flags`
- `reframed_question`
- `required_boundaries`
- `next_steps`

## 边界

- 书占只作为阅读触发的象征反思。
- 不把书页、经典、经文或随机句子写成事实证明、命令、天意、惩罚或专业建议。
- 不提供整本书、全章或长段受版权保护文本。
