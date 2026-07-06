# Tool Spec：ritual_low_risk_protocol

## 目的

为常见驱邪、净化、护身、睡前安定、搬家入住、分手告别等请求选择低风险象征性流程。此工具不确认超自然原因，不提供危险仪式步骤，而是把请求映射到可执行、可监测、可升级求助的安全协议。

## 输入

- `request_text`：用户请求
- `scenario`：可选，`moving_home`、`sleep_grounding`、`relationship_closure`、`space_pressure`
- `source_type`：可选，传给 `ritual_source_guard`

## 输出

- `scenario_id`、`scenario_name`
- `risk_level`、`can_continue_symbolic_support`
- `goal`
- `protocol_steps`
- `do_not_do`
- `monitoring`
- `safety_result`
- `source_guard`
- `escalation`

## 规则

1. 先复用 `ritual_safety_check` 判断风险。
2. 再复用 `ritual_source_guard` 标注来源。
3. Orange/Red 场景必须在步骤首位暂停原危险仪式动作。
4. 所有协议必须无火、无血、无刀具、无摄入、无密闭燃烧、无操控他人。
5. 输出草稿仍需通过 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/ritual_low_risk_protocol.py --text "搬进新家后想做一个不用火的净化流程"
python3 agent-tools/scripts/ritual_low_risk_protocol.py --text "分手后想做告别仪式" --scenario relationship_closure
```
