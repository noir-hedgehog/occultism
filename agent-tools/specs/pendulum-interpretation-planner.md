# Tool Spec：pendulum_interpretation_planner

## 目的

把灵摆会话记录和摆动象征查询组合成安全解读计划。计划优先现实证据、专业边界和用户价值排序，再给象征性反思。

## 输入

- `question_text` / `request_text` / `text`
- `answer_motion`：可选
- `calibration_notes`：可选
- `focus`：可选

## 输出

遵循 [pendulum-interpretation-planner.schema.json](../schemas/pendulum-interpretation-planner.schema.json)。

## 规则

1. 不把灵摆结果当成事实、诊断、预测或行动指令。
2. 对 yes/no 结果必须补现实核查动作。
3. 高风险请求必须暂停并改写。

## 命令

```bash
python3 agent-tools/scripts/pendulum_interpretation_planner.py --text "我想用灵摆反思要不要先沟通" --answer-motion "左右" --calibration-notes "左右=需要比较" --consent-confirmed
```
