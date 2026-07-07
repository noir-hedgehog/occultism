# Tool Spec：web_ui_surface_smoke_runner

## 目的

启动本地 Web UI server，并对主要 HTTP API surface 执行代表请求 smoke 验证。

它验证“交互可用化矩阵”里的入口不仅有文档和脚本，还能通过本地 HTTP API 被调用。

## 输入

- `root`：仓库根目录，默认当前目录。
- `case_id`：可选，可重复；只运行指定 smoke case。
- `timeout`：HTTP 请求超时秒数。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/WebUISurfaceSmoke验证.md`。

## 输出

遵循 [web-ui-surface-smoke-runner.schema.json](../schemas/web-ui-surface-smoke-runner.schema.json)。

关键字段：

- `case_count`、`passed_count`、`failed_count`：smoke case 结果。
- `covered_surface_ids`：覆盖到的交互矩阵 surface。
- `matrix_surface_count`：交互矩阵中定义的 surface 数。
- `results`：每个 HTTP 请求的 endpoint、状态码、摘要和错误。

## 命令

```bash
python3 agent-tools/scripts/web_ui_surface_smoke_runner.py
python3 agent-tools/scripts/web_ui_surface_smoke_runner.py --format markdown --write
python3 agent-tools/scripts/web_ui_surface_smoke_runner.py --case-id health --case-id interaction_surface_matrix
```
