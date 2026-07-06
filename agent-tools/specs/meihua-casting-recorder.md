# Tool Spec：meihua_casting_recorder

## 目的

记录和校验梅花易数起卦输入，包括报数、时间、外应、方位或外部卦盘来源，以及体卦、用卦、动爻、互卦、变卦和体用五行关系。此工具不自动排卦、不补数字、不编造外应，只把用户或外部工具提供的字段转成可复盘记录。

## 输入

- `question_text`：已通过一事一问改写的问题。
- `casting_method` / `method`：`number_casting`、`time_casting`、`external_omen`、`direction_symbol`、`external_chart`、`manual_record`。
- `numbers` / `reported_numbers`：报数起卦的数字列表。
- `cast_time`、`timezone`：时间起卦或记录时间。
- `external_omen` / `omen_text`：外应观察文字。
- `direction`：方位取象来源。
- `chart_source` / `external_chart_source`：外部卦盘或工具来源。
- `body_trigram` / `body`：体卦八卦名。
- `use_trigram` / `use`：用卦八卦名。
- `moving_line`：动爻，1-6 或初爻/二爻/三爻/四爻/五爻/上爻。
- `base_hexagram`、`mutual_hexagram`、`changed_hexagram`：本卦、互卦、变卦名称。
- `body_use_relation` / `relation`：可选体用关系；工具会按体用八卦五行计算并比对。

## 输出

- `trigger_source`：数字、时间、外应、方位和外部卦盘来源记录。
- `computed_body_use_relation`：由体卦和用卦五行计算出的关系。
- `risk_flags`：财务、医疗/危机、法律/紧急、操控/隐私、决定论、超自然恐惧风险。
- `missing_fields`：继续解释前需要补的字段。
- `is_valid`：字段是否完整且无格式错误。
- `can_interpret_meihua`：是否可以继续做梅花象征解释。

## 安全边界

- 不自动起卦，不替用户补数字、时间、外应或盘式。
- 不把体用、生克、外应、动爻写成成败、疾病、财富、关系或灾祸的确定断言。
- 涉及医疗、法律、财务、危机、人身安全、第三方隐私或操控他人时，先暂停占问并转现实支持。
- 术语解释交给 `meihua_symbol_lookup`，最终输出仍需 `mystic_output_lint`。

## 示例

```bash
python3 agent-tools/scripts/meihua_casting_recorder.py --json '{"question_text":"这个项目沟通当前的主要阻力和下一步是什么？","casting_method":"number_casting","numbers":[27,14],"body_trigram":"离","use_trigram":"坎","moving_line":3,"base_hexagram":"火水未济","mutual_hexagram":"水火既济","changed_hexagram":"火风鼎"}'
python3 agent-tools/scripts/meihua_casting_recorder.py --json '{"question_text":"这个合作是否必败？","casting_method":"external_omen","external_omen":"杯子突然摔碎，是不是天意必败","body_trigram":"震","use_trigram":"兑","moving_line":"上爻"}'
```
