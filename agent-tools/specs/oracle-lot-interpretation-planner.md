# Tool Spec：oracle_lot_interpretation_planner

## 目的

把签文记录和符号查询组合成安全解签计划。计划只用于文化象征、情绪整理和低风险行动，不输出命令式或确定性结论。

## 输入

接受 `oracle_lot_record_builder` 的输入字段：

- `question_text`
- `lot_text`
- `source_type`
- `lot_number`
- `lot_grade`
- `focus`

## 输出

遵循 [oracle-lot-interpretation-planner.schema.json](../schemas/oracle-lot-interpretation-planner.schema.json)。

## 规则

1. 记录器阻断时，计划器必须阻断。
2. 解读层必须包含来源、签文关键词、象征提醒、现实锚点和低风险行动。
3. 不承诺应验，不把签文作为专业决策依据。

## 命令

```bash
python3 agent-tools/scripts/oracle_lot_interpretation_planner.py --question "关系下一步怎么沟通" --lot-text "第十二签 上签 云开月明" --source-type temple
```
