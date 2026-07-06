# Tool Spec：herbal_request_guard

## 目的

识别草本、香草、草药、药草、植物魔法、绿巫、herbal、herb magic 和 green witchcraft 请求，判断是否能继续低风险草本象征咨询。

## 输入

- `request_text` 或 `text`

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_herbal`
- `required_boundaries`
- `clarifying_questions`
- `next_steps`

## 安全边界

- 不把草本、香草、草药包或植物魔法写成治疗、诊断、驱邪、净化保证、开运招财、爱情咒、诅咒、关系结果或专业意见。
- 不提供内服、泡水喝、吞服、外敷、药浴、野外采摘、辨毒、未知植物食用、孕婴宠物过敏等具体安全适用判断。
- 不制造高价购买、囤货、代理课程、爱情咒/诅咒或反复依赖。
