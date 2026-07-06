# Tool Spec：sop_traceability_matrix_builder

## 目的

生成 SOP、知识卡、Skill、工具链和验证工具之间的追踪矩阵，确认每个流派不是只有文件存在，而是能从流程追踪到工具和验证证据。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/SOP-Tool-Skill追踪矩阵.md`。

## 输出

遵循 [sop-traceability-matrix-builder.schema.json](../schemas/sop-traceability-matrix-builder.schema.json)。

关键字段：

- `rows`
- `tool_chain`
- `mentioned_in_sop`
- `mentioned_in_skill`
- `unmentioned_tools`
- `missing_links`

## 判定

- `is_valid: true`：覆盖审计、工具 manifest 均通过，且每个领域工具至少在 SOP 或 Skill 中被提及。
- `missing_links`：工具链中未在 SOP 或 Skill 中出现的工具，需要补流程引用或修正索引。

## 命令

```bash
python3 agent-tools/scripts/sop_traceability_matrix_builder.py --format markdown
```
