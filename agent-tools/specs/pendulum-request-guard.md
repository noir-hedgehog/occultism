# Tool Spec：pendulum_request_guard

## 目的

在灵摆/摆锤占卜请求前做安全守门。工具允许低风险自我反思、偏好澄清和文化学习，阻断专业替代、最终决定、财务投机、第三方操控、超自然恐惧确认和反复依赖。

## 输入

- `request_text` / `text`

## 输出

遵循 [pendulum-request-guard.schema.json](../schemas/pendulum-request-guard.schema.json)。

## 规则

1. 灵摆不能替代医疗、法律、财务、安全或紧急判断。
2. 不用灵摆判断第三方隐私、真实想法或操控他人。
3. 不确认附身、邪灵、诅咒或超自然伤害。
4. 不鼓励反复问同一问题直到得到想要的答案。

## 命令

```bash
python3 agent-tools/scripts/pendulum_request_guard.py --text "用灵摆帮我做一次低风险自我反思，看看我是否更想先沟通"
```
