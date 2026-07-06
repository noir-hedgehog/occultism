# Tool Spec：agent_tool_definition_exporter

## 目的

把 `agent_tool_wrapper_manifest_builder` 的 wrapper 元数据导出为 agent tool definitions 和 OpenAI-style function tool 形状，方便 runtime 注册工具。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：`json`、`markdown` 或 `openai`。
- `write`：写入 `知识库/Agent工具定义导出.md`。

## 输出

遵循 [agent-tool-definition-exporter.schema.json](../schemas/agent-tool-definition-exporter.schema.json)。

关键字段：

- `definitions`
- `definitions[].input_schema`
- `definitions[].command`
- `definitions[].metadata`
- `openai_tools`

## 判定

- `is_valid: true`：wrapper manifest 有效，且每个可包装工具都导出了 definition。
- `format=openai`：只输出 OpenAI-style function tool 数组。

## 命令

```bash
python3 agent-tools/scripts/agent_tool_definition_exporter.py
python3 agent-tools/scripts/agent_tool_definition_exporter.py --format openai
python3 agent-tools/scripts/agent_tool_definition_exporter.py --format markdown
```
