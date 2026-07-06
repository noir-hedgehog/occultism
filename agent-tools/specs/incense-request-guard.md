# Tool Spec：incense_request_guard

## 作用

守门香火、香灰、烟形、看香和 incense reading 请求，识别明火燃烧、危险仪式、摄入香灰、专业替代、财务赌博、鬼神恐惧、第三方隐私、操控、高价购买和反复依赖风险。

## 输出

- `can_continue_incense`
- `risk_flags`
- `reframed_question`
- `required_boundaries`
- `next_steps`

## 边界

- 只处理已经安全结束、照片记录或无烟替代观察。
- 不提供点香、燃烧、烧纸、烧符、摄入香灰、放血、密闭燃烧或无人看管火源步骤。
- 不确认鬼神、神罚、诅咒或驱邪效果。
