# Tool Spec：physiognomy_request_guard

## 目的

在手相、面相、痣相或相术咨询前做边界判断。该工具只允许本人或已获同意的象征反思与文化学习，阻断健康诊断、寿命判断、颜值歧视、第三方隐私分析和筛人用途。

## 输入

- `request_text` / `text`
- `subject_is_self`
- `consent_obtained`
- `cultural_learning_only`

## 输出

遵循 [physiognomy-request-guard.schema.json](../schemas/physiognomy-request-guard.schema.json)。

## 规则

1. 缺少本人/同意信息时不得继续具体相术解读。
2. 任何健康、寿命、死亡、旺克、贵贱、人品、招聘筛选或第三方隐私请求都必须暂停或改写。
3. 可继续的请求只能进入象征、文化、叙事和低风险行动层。

## 命令

```bash
python3 agent-tools/scripts/physiognomy_request_guard.py --text "看我的生命线和事业线代表什么" --subject-is-self
```
