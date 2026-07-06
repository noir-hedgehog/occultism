# Tool Spec：release_manifest_builder

## 目的

生成版本发布与维护 manifest，把当前自动质量门、覆盖审计、开放事项和维护节奏汇总成可存档的结构化记录。

它用于补足“版本记录和维护节奏”，不替代 `release_gate_runner` 本身，也不表示已经安装到真实 Codex Skills。

## 输入

- `root`：仓库根目录，默认当前目录。
- `version`：版本号，默认 `0.1.0`。
- `release_id`：可选，默认 `mystic-agent-v<version>`。
- `release_type`：版本类型，默认 `maintenance`。
- `open_item`：可选开放事项，可重复传入；未传时使用默认开放事项。

## 输出

遵循 [release-manifest-builder.schema.json](../schemas/release-manifest-builder.schema.json)。

关键字段：

- `status`
- `summary`
- `quality_evidence`
- `open_items`
- `maintenance_cadence`
- `release_notes`

## 判定

- `status: ready_for_review`：`release_gate_runner` 与 `knowledge_coverage_audit` 均通过，可进入人工发布复核。
- `status: blocked`：至少一个自动证据未通过。

## 命令

```bash
python3 agent-tools/scripts/release_manifest_builder.py --version 0.1.0
```
