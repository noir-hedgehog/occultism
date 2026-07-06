# Tool Spec：transcript_anonymizer

## 目的

为 K-021 匿名真实对话扩展建立入口：对原始 transcript 做规则脱敏、风险/隐私打标、turn 解析、评分量表附加和回放映射准备。

此工具不声称完成法律意义匿名化，也不把样例自动加入验证集。所有输出都必须人工复核。

## 输入

- `raw_text` / `text`：原始对话文本，可用 `user:`、`assistant:`、`用户：`、`助手：` 标注轮次。
- `skill`：可选，Skill id 或领域别名，例如 `tarot`、`feng_shui`、`ritual_safety`、`bazi`。
- `source_label`：可选，内部样例编号，例如 `review-001`。

## 输出

遵循 [transcript-anonymizer.schema.json](../schemas/transcript-anonymizer.schema.json)。

关键字段：

- `turns`
- `redactions`
- `privacy_flags`
- `risk_flags`
- `residual_flags`
- `replay_mapping`
- `scoring_rubric`
- `reviewer_checklist`

## 规则

1. 手机号、邮箱、身份证、微信/QQ、姓名声明会替换为 `[REDACTED_*]`。
2. 精确日期、出生日期、时间、地址提示会做上下文脱敏。
3. 命理精确出生资料、第三方、未成年人、高风险仪式、医疗/财务/操控/宿命论风险会打标。
4. `can_enter_validation_set` 只表示规则检查未发现残留直接身份资料或精确出生资料；仍需人工复核。
5. 高风险 transcript 可以进入拒绝/转安全验证，但不能作为继续执行的普通咨询样例。

## 命令

```bash
python3 agent-tools/scripts/transcript_anonymizer.py --skill mingli --source-label review-001 --text '用户：我叫张三，想看前任1991年2月3日10:00上海出生的紫微感情'
python3 agent-tools/scripts/transcript_anonymizer.py --skill ritual --text 'user: 我想在密闭房间点蜡烛烧纸驱邪'
```
