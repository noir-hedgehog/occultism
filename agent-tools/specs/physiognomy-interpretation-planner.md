# Tool Spec：physiognomy_interpretation_planner

## 目的

把手相/面相观察记录和符号查询组合成安全解读计划。计划只用于文化学习、自我叙事和现实整理，不输出确定命运或外貌标签。

## 输入

接受 `physiognomy_observation_recorder` 的输入字段：

- `observation_text` / `request_text`
- `features`
- `subject_is_self`
- `consent_obtained`
- `focus`

## 输出

遵循 [physiognomy-interpretation-planner.schema.json](../schemas/physiognomy-interpretation-planner.schema.json)。

## 规则

1. 记录器阻断时，计划器必须阻断。
2. 解读层必须先声明资料来源和同意状态，再做符号解释，最后落到现实锚点。
3. 不从外貌或掌纹推断健康、寿命、道德、身份、财富、婚恋结果或社会价值。
4. 最终输出必须运行 `mystic_output_lint` 或等价检查。

## 命令

```bash
python3 agent-tools/scripts/physiognomy_interpretation_planner.py --text "我的生命线比较浅，事业线断续" --subject-is-self --focus "career reflection"
```
