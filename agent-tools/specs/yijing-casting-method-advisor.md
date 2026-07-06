# Tool Spec：yijing_casting_method_advisor

## 目的

在易经起卦前选择或记录起卦方式，并处理重复占问边界。此工具不生成卦、不解释卦，只判断是否可以进入起卦/记录流程，推荐三枚铜钱、蓍草概率模拟、用户手动起卦或外部卦记录，并列出必须保留的审计字段。

## 输入

- `question_text` / `request_text`：用户问题
- `requested_method` / `casting_method` / `method`：用户指定的起卦方式
- `user_consent_to_simulation`：用户是否同意 agent 模拟起卦
- `user_has_cast` / `has_external_cast`：用户是否已有卦或外部结果
- `chart_source` / `source_label`：外部卦来源
- `previous_questions` / `previous_casts`：用于识别重复占问
- `new_facts`：重复占问是否已有新增事实或行动选择

## 输出

遵循 [yijing-casting-method-advisor.schema.json](../schemas/yijing-casting-method-advisor.schema.json)。

关键字段：

- `recommended_method`
- `method_profile`
- `is_repeat_question`
- `has_new_facts`
- `can_continue_casting`
- `casting_mode`
- `required_record_fields`
- `missing_fields`
- `warnings`

## 规则

1. 起卦前仍必须通过 `yijing_question_guard` 做一事一问和高风险守门。
2. 用户未自行起卦时，agent 模拟起卦必须先取得用户同意，并保留 seed、时间、方法和时区。
3. 外部卦只记录来源和字段；字段不足时不补造六爻、本卦、动爻或变卦。
4. 重复占问只有在新增事实、行动选择或问题边界变化后才允许重新进入流程。
5. 高风险、专业替代、危机或操控请求先暂停占问并改写。

## 命令

```bash
python3 agent-tools/scripts/yijing_casting_method_advisor.py --text "我当前工作局势的主要变化是什么？" --method three_coins --user-consent-to-simulation
python3 agent-tools/scripts/yijing_casting_method_advisor.py --text "刚刚问过跳槽，再问一次" --json '{"previous_questions":["我该不该跳槽？"]}'
```

## 与 Skill 的关系

`yijing-symbolic-consultation` 在 `yijing_question_guard` 通过后、任何起卦或卦记录之前调用本工具。若返回 `can_continue_casting=false`，先补问方法、同意、来源或新增事实；若返回 `ready_to_cast`，再调用 `yijing_casting_simulator`；若返回 `record_existing`，再调用 `yijing_hexagram_record`。
