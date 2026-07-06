# Tool Spec：agent_runtime_dry_run_runner

## 目的

用代表请求 dry-run agent runtime 契约：请求进入 `agent_workflow_router` 后，ready 路径必须具备 Skill、SOP、领域工具和输出 lint；paused/blocked 路径不能继续调用领域工具。

## 输入

- `root`：仓库根目录，默认当前目录。
- `case_id`：可选，只运行一个代表请求。

## 输出

遵循 [agent-runtime-dry-run-runner.schema.json](../schemas/agent-runtime-dry-run-runner.schema.json)。

关键字段：

- `case_count`
- `ready_case_count`
- `paused_or_blocked_case_count`
- `results[].invariant_checks`
- `results[].missing_assets`

## 判定

- `is_valid: true`：所有代表请求通过运行时不变量检查，且工具 manifest 有效。
- ready 路径必须包含 `mystic_output_lint` 和至少一个领域工具。
- paused/blocked 路径只能先运行 `mystic_intake_triage`，并包含暂停/安全替代下一步。

## 命令

```bash
python3 agent-tools/scripts/agent_runtime_dry_run_runner.py
python3 agent-tools/scripts/agent_runtime_dry_run_runner.py --case-id route-tarot-career
```
