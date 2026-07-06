# Tool Spec：lost_object_request_guard

## 作用

识别失物、寻物、找东西、遗失物件和“占卜找物”请求，判断是否能继续低风险象征咨询。

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_lost_object`
- `reframed_question`
- `required_boundaries`
- `next_steps`

## 边界

- 只处理本人有权寻找的物品，不处理寻人、儿童/老人走失、跟踪、隐私定位或犯罪定责。
- 不承诺准确方位、一定找到、灵验定位或神秘指认。
- 疑似盗窃、证件财物风险、紧急走失或安全风险时，优先现实渠道和专业支持。
- 输出必须转成最后接触记录、路径复盘、区域搜索、联系渠道、复盘时间和停止条件。
