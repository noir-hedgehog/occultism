# Tool Spec：pet_communication_context_recorder

## 作用

记录低风险宠物沟通请求中的宠物种类、关系、可见行为、时间背景、健康/兽医边界、用户情绪、照护动作和现实锚点。

## 输出

- `pet_type`
- `relationship`
- `observations`
- `time_context`
- `health_context`
- `emotions`
- `care_actions`
- `missing_fields`
- `risk_flags`

## 边界

- 记录行为不等于诊断疾病、确认真实讯息或证明灵体。
- 缺少健康边界或照护动作时必须标记缺失。
