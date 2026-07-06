# Tool Spec：agent_tool_definition_validator

## 目的

验证 `agent_tool_definition_exporter` 导出的 agent tool definitions 是否适合进入 runtime 注册层。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/Agent工具定义验证.md`。

## 输出

遵循 [agent-tool-definition-validator.schema.json](../schemas/agent-tool-definition-validator.schema.json)。

关键字段：

- `definition_results`
- `openai_results`
- `duplicate_names`
- `failed_definition_count`
- `failed_openai_tool_count`

## 判定

- definition 名称必须唯一并符合函数工具命名规则。
- input schema 必须是 object。
- command 必须是 `python3 <script_path>`，且脚本、schema、spec 文件存在。
- metadata 必须包含 domains、skills 和 safety_tags。
- OpenAI-style function tool 必须包含 `type=function`、函数名、描述和 object parameters。

## 命令

```bash
python3 agent-tools/scripts/agent_tool_definition_validator.py
python3 agent-tools/scripts/agent_tool_definition_validator.py --format markdown
```
