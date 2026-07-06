# Tool Spec：tool_manifest_builder

## 目的

生成 agent 可消费的工具与 Skill manifest，把 `codex-skills/index.md`、工具脚本、schema 和 spec 编译成一份结构化 JSON。

它用于 MCP/API wrapper、安装器、看板和发布审计之间的对账；不执行工具，也不安装 Skill。

## 输入

- `root`：仓库根目录，默认当前目录。

## 输出

遵循 [tool-manifest-builder.schema.json](../schemas/tool-manifest-builder.schema.json)。

关键字段：

- `tools`：每个工具的脚本、schema、spec、关联 Skill、领域和缺失项。
- `skills`：从 `codex-skills/index.md` 解析出的 Skill 依赖工具。
- `missing`：缺失的 script/schema/spec 三件套证据。
- `is_valid`：所有工具三件套齐全时为 `true`。

## 判定

- `status: ready`：工具脚本、schema 和 spec 均存在。
- `status: incomplete`：至少缺少一个三件套文件。

## 命令

```bash
python3 agent-tools/scripts/tool_manifest_builder.py
```
