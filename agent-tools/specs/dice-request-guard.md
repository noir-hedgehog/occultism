# Tool Spec：dice_request_guard

## 作用

在星骰、占星骰、占卜骰请求进入咨询前，识别专业替代、财务赌博、确定预言、第三方隐私、操控和反复依赖风险。

## 输出

- `can_continue_dice`
- `consultation_intent`
- `risk_flags`
- `reframed_question`
- `required_boundaries`
- `next_steps`

## 边界

- 星骰和占卜骰只作为象征性反思、问题整理和低风险行动提醒。
- 不用于赌博、投资、医疗、法律、安全、第三方窥探、操控或确定预言。
