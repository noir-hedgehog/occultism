# Tool Spec：agent_route_smoke_runner

## 目的

批量验证 `agent_workflow_router` 对代表性用户请求的路由结果，覆盖当前流派和高风险暂停/阻断路径。

它是 agent runtime 上线前的路由冒烟测试，不替代完整 Skill 回放或真实用户 transcript。

## 输入

- `case_id`：可选，只运行单个路由样例。
- `root`：仓库根目录，默认当前目录。

## 输出

遵循 [agent-route-smoke-runner.schema.json](../schemas/agent-route-smoke-runner.schema.json)。

关键字段：

- `case_count`
- `passed_count`
- `failed_count`
- `domain_count`
- `results`

## 判定

- `is_valid: true`：所有代表请求的 `domain`、`skill`、`route_status` 和 `can_continue` 均符合预期。
- 高风险样例必须暂停或阻断，不能进入 `ready_to_run_skill`。

## 命令

```bash
python3 agent-tools/scripts/agent_route_smoke_runner.py
python3 agent-tools/scripts/agent_route_smoke_runner.py --case-id route-tarot-career
```
