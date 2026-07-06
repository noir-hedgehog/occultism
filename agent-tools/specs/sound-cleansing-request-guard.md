# Tool Spec：sound_cleansing_request_guard

## 作用

识别声响净化、铃钵、铃铛、音叉、拍手、诵念、mantra 和 sound cleansing 请求，判断是否能继续低风险象征咨询。

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_sound_cleansing`
- `reframed_question`
- `required_boundaries`
- `next_steps`

## 边界

- 不承诺驱邪、清除负能量、治疗、入睡、转运或灵验结果。
- 不提供超大音量、贴耳、通宵、耳痛仍继续、靠近婴儿/宠物或扰民做法。
- 不替代医疗、心理、睡眠、法律、报警或其他专业支持。
- 不制造高价铃钵、课程套餐、贷款购买或反复依赖。
