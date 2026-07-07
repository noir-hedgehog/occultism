# Tool Spec：interaction_surface_matrix_builder

## 目的

生成“交互可用化矩阵”，把当前项目的给人入口、Web API、可程序化工具和 Agent/人工接管边界放在同一张表里。

它用于回答：

- 哪些能力已经有 Web UI 入口。
- 哪些能力可通过 API/CLI 稳定运行。
- 哪些能力只适合跑安全子集。
- 哪些能力必须由 Agent、用户或人工审校补齐。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/交互可用化矩阵.md`。

## 输出

遵循 [interaction-surface-matrix-builder.schema.json](../schemas/interaction-surface-matrix-builder.schema.json)。

关键字段：

- `surface_count`：交互入口数量。
- `api_endpoint_count`：API endpoint 数量。
- `automation_counts`：按自动化等级分布。
- `surfaces`：每个入口的用户界面、API、工具、证据文档和 Agent 边界。

## 命令

```bash
python3 agent-tools/scripts/interaction_surface_matrix_builder.py --format markdown
python3 agent-tools/scripts/interaction_surface_matrix_builder.py --format markdown --write
```
