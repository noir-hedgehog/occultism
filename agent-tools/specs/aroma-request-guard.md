# Tool Spec：aroma_request_guard

## 目的

识别芳香、香薰、精油、香氛、气味、嗅觉、aromatherapy、essential oil 和 diffuser 请求，判断是否能继续低风险气味象征咨询。

## 输入

- `request_text` 或 `text`

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_aroma`
- `required_boundaries`
- `clarifying_questions`
- `next_steps`

## 安全边界

- 不把精油、香薰或气味写成治疗、诊断、驱邪、净化保证、开运招财、关系结果或专业意见。
- 不提供内服、入口、原液直接涂抹、孕婴宠物过敏等具体安全适用判断。
- 不制造高价购买、囤货、代理课程或反复依赖。
