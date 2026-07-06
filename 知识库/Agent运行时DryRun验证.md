# Agent 运行时 Dry-run 验证

本页记录 `agent_runtime_dry_run_runner` 的用途：用代表请求验证 agent runtime 的基本契约，而不生成真实玄学结论。

## 验证范围

- ready 路径必须有 Skill、SOP、领域工具和 `mystic_output_lint`。
- paused/blocked 路径只能先运行 `mystic_intake_triage`，不能继续调用领域工具。
- `initial_tools` 中的工具必须在 `tool_manifest_builder` 中处于 ready。
- SOP、知识卡和 Skill 路径必须存在。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| 代表请求 | 13 |
| 通过 | 13 |
| ready 路径 | 11 |
| paused/blocked 路径 | 2 |

## 命令

```bash
python3 agent-tools/scripts/agent_runtime_dry_run_runner.py
python3 agent-tools/scripts/agent_runtime_dry_run_runner.py --case-id route-tarot-career
```

## 与其他验证的关系

- `agent_route_smoke_runner` 验证路由结果是否符合预期。
- `agent_runtime_dry_run_runner` 验证路由结果能否满足 runtime 运行约束。
- `skill_replay_runner` 和 `skill_transcript_runner` 验证 Skill 蓝图的前向和多轮行为。

## 限制

- dry-run 不执行真实多轮咨询。
- dry-run 不表示 Skill 已安装到真实 Codex home。
- 真实用户表达仍需要通过匿名 transcript 流程持续扩充。
