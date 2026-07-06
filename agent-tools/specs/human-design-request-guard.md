# Tool Spec：human_design_request_guard

## 目的

识别人类图、Human Design、bodygraph、类型、策略、内在权威、人生角色、中心、通道和闸门请求，判断是否能继续低风险象征咨询。

## 输入

- `request_text` 或 `text`

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_human_design`
- `required_boundaries`
- `clarifying_questions`
- `next_steps`

## 安全边界

- 不把人类图写成事实证明、人格定论、诊断、关系筛选、职业保证、财富结果或专业意见。
- 不处理第三方出生资料窥探、读心、操控、关系歧视、高价解读压力或反复依赖。
- 优先使用用户已有 bodygraph 或最小化出生资料。
