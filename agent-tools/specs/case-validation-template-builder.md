# Tool Spec：case_validation_template_builder

## 目的

把 `case_validation_backlog_builder` 的 backlog 项转成可填写的采集模板。

它解决的问题是：维护者看到一个 P0/P1/P2 待验证项后，知道下一条真实或匿名材料应该怎么填、交给哪些工具、按什么标准验收。

## 输入

- `root`：仓库根目录，默认当前目录。
- `domain`：可选，按领域 id 生成模板，例如 `fengshui`。
- `backlog_id`：可选，按精确 backlog id 生成模板。
- `priority`：可选，`P0`、`P1` 或 `P2`。
- `limit`：可选，限制模板数量。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/案例采集模板.md`。

## 输出

遵循 [case-validation-template-builder.schema.json](../schemas/case-validation-template-builder.schema.json)。

关键字段：

- `template_count`：生成模板数量。
- `templates`：每个 backlog 项对应的采集模板。
- `collection_template.fields`：字段名、类型、提示、示例和流向工具。
- `collection_template.example_payload`：可复制到后续工具的示例 payload。
- `recommended_tool_flow`：建议执行链路。

## 命令

```bash
python3 agent-tools/scripts/case_validation_template_builder.py --domain fengshui --format markdown
python3 agent-tools/scripts/case_validation_template_builder.py --priority P2 --limit 3
python3 agent-tools/scripts/case_validation_template_builder.py --format markdown --write
```
