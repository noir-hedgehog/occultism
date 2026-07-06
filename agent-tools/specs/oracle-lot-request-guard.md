# Tool Spec：oracle_lot_request_guard

## 目的

在求签、解签、签文、观音签、月老签或在线抽签咨询前做风险守门。工具允许文化象征和低风险反思，阻断专业替代、操控、第三方隐私和反复抽签依赖。

## 输入

- `request_text` / `question_text` / `text`

## 输出

遵循 [oracle-lot-request-guard.schema.json](../schemas/oracle-lot-request-guard.schema.json)。

## 规则

1. 医疗、法律、财务、人身安全请求必须暂停解签并转向现实支持。
2. 不把签文写成必然应验、灾祸恐吓或结果保证。
3. 不鼓励反复抽到满意，不使用签文操控他人或断定第三方真实想法。

## 命令

```bash
python3 agent-tools/scripts/oracle_lot_request_guard.py --text "我抽到一支月老签，想看看关系沟通提醒"
```
