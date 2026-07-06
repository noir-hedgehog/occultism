# Tool Spec：body_omen_request_guard

## 目的

识别眼跳、耳鸣、喷嚏、耳热、脸热、手心痒、肉跳和 body omen 请求，判断是否能继续低风险身体征兆象征咨询。

## 输入

- `request_text` 或 `text`

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_body_omen`
- `required_boundaries`
- `clarifying_questions`
- `next_steps`

## 安全边界

- 不把身体征兆写成疾病、灾祸、灵体、财运、他人想法或事实结果证明。
- 不替代医疗诊断、检查、用药、急症处理、心理健康支持或专业建议。
- 不协助彩票赌博、投资择时、第三方身体标签、驱邪恐惧、危险身体试验或反复依赖。
