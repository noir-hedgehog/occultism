# Tool Spec：agent_tool_registry_builder

## 目的

把已验证的 agent tool definitions 组织成 runtime 注册表，提供注册顺序、按流派索引、按 Skill 索引和安全启动工具列表。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/Agent工具注册表.md`。

## 输出

遵循 [agent-tool-registry-builder.schema.json](../schemas/agent-tool-registry-builder.schema.json)。

关键字段：

- `registration_order`
- `entries`
- `by_domain`
- `by_skill`
- `safety_bootstrap`
- `runtime_contract`

## 判定

- `ready_for_runtime_registration`：工具定义验证通过，注册表包含所有有效定义。
- 注册顺序优先放置 intake、router、output lint 和安全守门工具，再放领域工具和验证/维护工具。

## 命令

```bash
python3 agent-tools/scripts/agent_tool_registry_builder.py
python3 agent-tools/scripts/agent_tool_registry_builder.py --format markdown
```
