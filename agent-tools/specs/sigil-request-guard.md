# Tool Spec：sigil_request_guard

## 目的

识别 sigil、符号印记、魔法印记、意图符号、seal magic、魔法阵和 symbol circle 请求，判断是否能继续低风险符号印记象征咨询。

## 输入

- `request_text` 或 `text`

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_sigil`
- `required_boundaries`
- `clarifying_questions`
- `next_steps`

## 安全边界

- 不把 sigil、符号印记、魔法阵或 seal 写成召唤、驱邪、诅咒、爱情咒、显化保证、灵验证明或专业建议。
- 不提供滴血、割伤、刻皮肤、纹身刺青、烙印、焚烧、密闭燃烧或危险销毁步骤。
- 不协助操控第三方、违法财务、逃避现实责任、高价课程购买或反复依赖。
