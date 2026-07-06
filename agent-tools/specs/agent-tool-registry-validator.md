# Tool Spec：agent_tool_registry_validator

## 目的

验证 `agent_tool_registry_builder` 生成的 runtime 工具注册表是否适合注册。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/Agent工具注册表验证.md`。

## 输出

遵循 [agent-tool-registry-validator.schema.json](../schemas/agent-tool-registry-validator.schema.json)。

关键字段：

- `bootstrap_prefix`
- `safety_bootstrap`
- `skill_results`
- `errors`

## 判定

- `registration_order` 必须覆盖所有 entries。
- 前三项必须是 `mystic_intake_triage`、`agent_workflow_router`、`mystic_output_lint`。
- 每个注册工具必须保留 `professional_boundary_required` 安全标签。
- `by_domain` 和 `by_skill` 索引必须指向存在的工具。
- 每个 Skill 必须包含 `mystic_intake_triage` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/agent_tool_registry_validator.py
python3 agent-tools/scripts/agent_tool_registry_validator.py --format markdown
```
