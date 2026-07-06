# Tool Spec：liuyao_focus_selector

## 目的

按六爻问题类型生成候选用神、世应观察点和读盘顺序。若输入已记录的六爻盘，本工具会把候选用神落到具体爻位、动爻、六亲和六神字段上；若没有盘式，只输出候选取用方向，不进入爻位解读。

## 输入

- `question_text` / `request_text`：用户问题
- `chart_record`：可选，`liuyao_chart_recorder` 的输出
- 或直接提供 `liuyao_chart_recorder` 可接受的字段：
  - `casting_method`
  - `chart_source`
  - `base_hexagram`
  - `changed_hexagram`
  - `focus_spirit`
  - `focus_logic`
  - `lines`

## 输出

遵循 [liuyao-focus-selector.schema.json](../schemas/liuyao-focus-selector.schema.json)。

关键字段：

- `question_domain`：问题类型
- `risk_flags`：专业替代、危机、隐私、操控或决定论风险
- `can_select_focus`
- `can_continue_liuyao_focus`
- `chart_is_valid`
- `focus_candidates`
- `interpretation_order`
- `warnings`
- `limits`

## 规则

1. 若传入原始盘式字段，先复用 `liuyao_chart_recorder` 校验盘式。
2. 优先保留用户、外部盘或上游记录已标注的 `focus_spirit`。
3. 总是把世爻和应爻作为基础观察点，但不把应爻写成对方真实想法。
4. 再按事项类型生成六亲候选：项目/合作偏官鬼、父母、兄弟；资源经营偏妻财、兄弟、子孙；文书学习偏父母；关系类先看世应，再谨慎处理官鬼/妻财。
5. 高风险专业替代、危机、隐私或操控请求不继续取用。
6. 输出必须写“候选用神/需确认”，不得声称唯一正统取法。

## 命令

```bash
python3 agent-tools/scripts/liuyao_focus_selector.py --json '{"question_text":"这个项目合作当前的主要阻力和下一步是什么？","casting_method":"external_chart","chart_source":"用户提供外部盘","base_hexagram":"泽雷随","changed_hexagram":"水雷屯","focus_spirit":"官鬼","focus_logic":"项目合作以应爻和官鬼为外部压力观察点","lines":[{"position":1,"yin_yang":"yang","kinship":"父母","spirit":"青龙"},{"position":2,"yin_yang":"yin","kinship":"兄弟","spirit":"朱雀","roles":["世爻"]},{"position":3,"yin_yang":"yang","kinship":"官鬼","spirit":"勾陈","roles":["应爻","用神"],"changing":true},{"position":4,"yin_yang":"yin","kinship":"妻财","spirit":"腾蛇"},{"position":5,"yin_yang":"yang","kinship":"子孙","spirit":"白虎"},{"position":6,"yin_yang":"yin","kinship":"父母","spirit":"玄武"}]}'
```

## 与 Skill 的关系

`liuyao-symbolic-consultation` 应在 `yijing_question_guard` 和 `liuyao_chart_recorder` 之后调用本工具，再用 `liuyao_symbol_lookup` 解释已确认的六亲、世应、用神和动爻。最终草稿仍需通过 `mystic_output_lint`。
