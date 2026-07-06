# Tool Spec：liuyao_chart_recorder

## 目的

记录和校验六爻盘式字段，包括起卦方法、外部卦盘来源、本卦、变卦、动爻、世应、六亲、六神、用神和取用逻辑。此工具不自动起卦、不补世应、不编造用神，只把用户或外部工具提供的字段转成可复盘记录。

## 输入

- `question_text`：已通过一事一问改写的问题。
- `casting_method` / `method`：`coin_casting`、`manual_record`、`external_chart`、`time_casting`、`unknown`。
- `chart_source` / `external_chart_source`：外部排盘工具、人工记录或来源标签。
- `cast_time`、`timezone`：起卦或记录时间。
- `base_hexagram`、`changed_hexagram`：本卦和变卦名称。
- `focus_spirit` / `focus_kinship`：用神或主要观察点。
- `focus_logic`：取用逻辑说明，如“项目合作以应爻/官鬼为外部压力观察点”。
- `lines`：六条爻，从初爻到上爻，每条可含：
  - `position` / `line` / `index`：1-6 或初爻/二爻/三爻/四爻/五爻/上爻。
  - `yin_yang` / `value`：`yin` / `yang`。
  - `kinship`：父母、兄弟、子孙、妻财、官鬼。
  - `spirit`：青龙、朱雀、勾陈、腾蛇、白虎、玄武。
  - `roles` / `role`：世爻、应爻、用神、原神、忌神、仇神。
  - `branch`、`element`、`changing`、`hidden_kinship`、`notes`。

## 输出

- `lines`：标准化六爻字段，含爻位标签、六亲、六神、角色和动爻。
- `changing_lines`：动爻位置。
- `missing_fields`：继续解释前需要补的字段。
- `risk_flags`：财务、医疗/危机、法律/紧急、操控/隐私、决定论、超自然恐惧风险。
- `is_valid`：盘式字段是否完整且无格式错误。
- `can_interpret_liuyao`：是否可以继续做六爻象征解释。

## 安全边界

- 不自动起卦，不补世应、六亲、六神、用神或变卦。
- 不把六亲、六神、世应、用神、动爻写成成败、疾病、财富、关系或灾祸的确定断言。
- 涉及医疗、法律、财务、危机、人身安全、第三方隐私或操控他人时，先暂停占问并转现实支持。
- 术语解释交给 `liuyao_symbol_lookup`，最终输出仍需 `mystic_output_lint`。

## 示例

```bash
python3 agent-tools/scripts/liuyao_chart_recorder.py --json '{"question_text":"这个项目合作当前的主要阻力和下一步是什么？","casting_method":"external_chart","chart_source":"用户提供外部盘","base_hexagram":"泽雷随","changed_hexagram":"水雷屯","focus_spirit":"官鬼","focus_logic":"项目合作以应爻和官鬼为外部压力观察点","lines":[{"position":1,"yin_yang":"yang","kinship":"父母","spirit":"青龙"},{"position":2,"yin_yang":"yin","kinship":"兄弟","spirit":"朱雀","roles":["世爻"]},{"position":3,"yin_yang":"yang","kinship":"官鬼","spirit":"勾陈","roles":["应爻","用神"],"changing":true},{"position":4,"yin_yang":"yin","kinship":"妻财","spirit":"腾蛇"},{"position":5,"yin_yang":"yang","kinship":"子孙","spirit":"白虎"},{"position":6,"yin_yang":"yin","kinship":"父母","spirit":"玄武"}]}'
python3 agent-tools/scripts/liuyao_chart_recorder.py --json '{"question_text":"用六爻看我该不该贷款梭哈股票","casting_method":"external_chart","chart_source":"外部盘","base_hexagram":"泽雷随","focus_spirit":"妻财","focus_logic":"财务投资以妻财为观察点","lines":[{"position":1},{"position":2,"roles":["世爻"]},{"position":3,"roles":["应爻"]},{"position":4},{"position":5},{"position":6}]}'
```
