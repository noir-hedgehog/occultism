# Tool Spec：qimen_focus_selector

## 目的

从已记录的奇门盘式中选择候选用神、相关宫位和读盘顺序。此工具不排盘、不宣称唯一正统用神，只把用户或外部盘中已有字段转成可审计的解释入口。

## 输入

- `question_text` / `request_text`：用户问题
- `chart_record`：可选，`qimen_chart_record` 的输出
- 或直接提供 `qimen_chart_record` 可接受的字段：
  - `palaces`
  - `focus_targets`
  - `day_stem`
  - `hour_stem`
  - `duty_door`
  - `duty_star`
  - `question_text`

## 输出

遵循 [qimen-focus-selector.schema.json](../schemas/qimen-focus-selector.schema.json)。

关键字段：

- `question_domain`：问题类型
- `risk_flags`：医疗、法律、财务、危机或操控风险
- `can_continue_qimen_focus`
- `missing_fields`
- `focus_candidates`
- `interpretation_order`
- `warnings`
- `limits`

## 规则

1. 若传入原始盘式字段，先复用 `qimen_chart_record` 校验盘式。
2. 若盘式无效，不选择用神。
3. 优先使用用户或外部盘已标注的 `focus_targets`。
4. 再按日干、时干、值使门、值符星、生门、开门、休门等字段生成候选。
5. 不同派别用神法可能不同，输出必须标注“候选”而不是“定论”。
6. 高风险专业替代或操控请求不继续读盘。

## 命令

```bash
python3 agent-tools/scripts/qimen_focus_selector.py --json '{"question_text":"这个项目下一步怎么推进？","day_stem":"戊","hour_stem":"乙","duty_door":"开门","duty_star":"天心","palaces":[{"palace":1,"trigram":"坎","earth_stem":"戊","heaven_stem":"乙","door":"休门","star":"天蓬","deity":"值符"}]}'
```

## 与 Skill 的关系

`qimen-chart-consultation` 应在 `qimen_method_guard` 和 `qimen_chart_record` 之后调用本工具，再进入门、星、神、干组合解释。最终草稿仍需通过 `mystic_output_lint`。
