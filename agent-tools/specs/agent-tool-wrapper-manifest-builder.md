# Tool Spec：agent_tool_wrapper_manifest_builder

## 目的

把 `agent-tools/scripts` 中的可运行脚本转成 agent runtime 可消费的 wrapper manifest，标明命令、输入 schema、所属流派、关联 Skill 和安全标签。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/Agent工具WrapperManifest.md`。

## 输出

遵循 [agent-tool-wrapper-manifest-builder.schema.json](../schemas/agent-tool-wrapper-manifest-builder.schema.json)。

关键字段：

- `wrappers[].command`
- `wrappers[].input_schema_path`
- `wrappers[].domains`
- `wrappers[].skills`
- `wrappers[].safety_tags`
- `runtime_contract`

## 判定

- `is_valid: true`：所有工具来自 `tool_manifest_builder` 且处于 ready，可生成 wrapper 元数据。
- `blocked_count > 0`：至少一个工具缺少脚本、schema 或 spec，不应进入 runtime wrapper。

## 命令

```bash
python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py
python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py --format markdown
```
