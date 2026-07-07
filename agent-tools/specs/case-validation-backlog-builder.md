# Tool Spec：case_validation_backlog_builder

## 目的

把 `domain_evidence_matrix_builder` 生成的 P0/P1/P2 证据矩阵转成可执行 backlog。

它回答维护者下一步应该收集什么：

- P0：实用/科学化对照案例，含 baseline、低风险行动、follow-up 和验证结果。
- P1：来源审计和勘误，含来源类型、流派/地区/时代限制和审校记录。
- P2：神秘边界反例，含不安全原句、风险类别、安全改写和专业边界。

## 输入

- `root`：仓库根目录，默认当前目录。
- `priority`：可选，`P0`、`P1` 或 `P2`。
- `limit`：可选，限制输出项数量。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/案例验证Backlog.md`。

## 输出

遵循 [case-validation-backlog-builder.schema.json](../schemas/case-validation-backlog-builder.schema.json)。

关键字段：

- `backlog_count`：生成的 backlog 项数量。
- `priority_counts`：P0/P1/P2 分布。
- `target_artifact_counts`：目标产物分布。
- `items`：每个领域的采集字段、验收标准、推荐工具和状态。
- `workstreams`：三条主工作流。

## 命令

```bash
python3 agent-tools/scripts/case_validation_backlog_builder.py --format markdown --write
python3 agent-tools/scripts/case_validation_backlog_builder.py --priority P0 --limit 5
```
