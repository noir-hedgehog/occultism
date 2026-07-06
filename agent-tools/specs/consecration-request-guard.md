# Tool Spec：consecration_request_guard

## 作用

识别开光、加持、净物、净化物件、净化水晶、过香火和祝福物件请求，判断是否能继续低风险象征咨询。

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_consecration`
- `reframed_question`
- `required_boundaries`
- `next_steps`

## 边界

- 不承诺灵验、挡灾、转运、发财、平安保证或神明命令。
- 不提供放血、摄入、刀具、密闭燃烧、通宵明火或伤身做法。
- 不替代医疗、法律、报警、心理或财务专业支持。
- 不制造高价开光、加持套餐、贷款买法事或反复依赖。
