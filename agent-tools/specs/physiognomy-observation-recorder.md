# Tool Spec：physiognomy_observation_recorder

## 目的

记录用户自述或已获同意的手相/面相观察，提取可安全查询的特征代码。工具不做照片分析，不补写用户未提供的外貌细节。

## 输入

- `observation_text` / `request_text` / `text`
- `features`
- `modality`
- `subject_is_self`
- `consent_obtained`

## 输出

遵循 [physiognomy-observation-recorder.schema.json](../schemas/physiognomy-observation-recorder.schema.json)。

## 规则

1. 先复用 `physiognomy_request_guard` 判断是否可继续。
2. 只提取符号特征，如 `life_line`、`fate_line`、`nose`、`mole`。
3. 不输出健康、寿命、颜值、阶层、人品或第三方人格判断。

## 命令

```bash
python3 agent-tools/scripts/physiognomy_observation_recorder.py --text "我的生命线比较浅，事业线断续" --subject-is-self
```
