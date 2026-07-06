# Tool Spec：pendulum_session_recorder

## 目的

记录一次低风险灵摆会话的问题、问题类型、校准说明、摆动结果和缺失字段。该工具不解释结果，只把材料整理成可审计的输入。

## 输入

- `question_text` / `request_text` / `text`
- `answer_motion`：可选，顺时针、逆时针、前后、左右、不动、不明确等
- `calibration_notes`：可选
- `consent_confirmed`：可选

## 输出

遵循 [pendulum-session-recorder.schema.json](../schemas/pendulum-session-recorder.schema.json)。

## 规则

1. yes/no 问题必须提示改写成开放反思问题。
2. 未校准或结果不明确时不能强行解释。
3. 有专业替代、第三方操控、恐惧确认或依赖迹象时暂停。

## 命令

```bash
python3 agent-tools/scripts/pendulum_session_recorder.py --text "我想用灵摆反思要不要先沟通" --answer-motion "左右" --calibration-notes "顺时针=倾向推进，左右=需要比较" --consent-confirmed
```
