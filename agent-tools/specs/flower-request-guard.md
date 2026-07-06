# Tool Spec：flower_request_guard

## 作用

在花语、花占、花签、花牌、植物象征、送花和花束请求进入咨询前，识别专业替代、医疗疗愈、过敏/毒性/宠物安全、财务赌博、确定预言、第三方隐私、操控、灵异恐惧、高价购买和反复依赖风险。

## 输出

- `can_continue_flower`
- `consultation_intent`
- `risk_flags`
- `reframed_question`
- `required_boundaries`
- `next_steps`

## 边界

- 花语和植物象征只作为文化、审美、表达、提醒和低风险反思。
- 不用于医疗、药用、过敏/毒性/宠物安全判断、投资赌博、驱邪证明、第三方窥探、操控或确定预言。
