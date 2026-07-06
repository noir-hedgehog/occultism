# Tool Spec：domain_evidence_matrix_builder

## 目的

把已有 61 个领域收束成可维护的证据矩阵，避免继续新增碎分支而忽略主干。

矩阵按主干、证据模式、优先级、神秘强度、案例模板和下一步工作分类，帮助维护者判断：

- 哪些领域适合先做科学化/实用验证。
- 哪些领域需要优先做来源审计和勘误。
- 哪些领域神秘色彩强，必须先做边界反例和安全改写。
- 哪些领域应该补对照案例、回访记录和验证字段。

## 输入

- `root`：仓库根目录。默认当前目录。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/证据矩阵.md`。

## 输出

遵循 [domain-evidence-matrix-builder.schema.json](../schemas/domain-evidence-matrix-builder.schema.json)。

关键字段：

- `priority_counts`：P0/P1/P2 数量。
- `evidence_mode_counts`：科学/实用、溯源勘误、神秘边界、混合模式数量。
- `track_counts`：科学/实用、溯源、神秘边界、案例验证轨道数量。
- `domains`：每个领域的主干、证据模式、优先级、案例模板和下一步。
- `workstreams`：下一阶段应推进的三个主工作流。

## 命令

```bash
python3 agent-tools/scripts/domain_evidence_matrix_builder.py --format markdown --write
```
