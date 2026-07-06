# Tool Spec：numerology_request_guard

## 目的

在数字能量、生命灵数、手机号/车牌号/门牌号象征咨询前做安全守门。工具允许低风险文化联想和偏好整理，阻断敏感标识、财富保证、专业替代和第三方标签化。

## 输入

- `request_text` / `text`

## 输出

遵循 [numerology-request-guard.schema.json](../schemas/numerology-request-guard.schema.json)。

## 规则

1. 不收集身份证、银行卡、验证码、密码或完整手机号。
2. 不承诺发财、转运、健康、复合或成功。
3. 不通过号码判断第三方人品、隐私、职业适配或命运。

## 命令

```bash
python3 agent-tools/scripts/numerology_request_guard.py --text "比较手机号尾号 168 和 739，只做数字象征和记忆度分析"
```
