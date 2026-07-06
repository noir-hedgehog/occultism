# Tool Spec：pilot_readiness_report

## 目的

汇总自动证据和外部阻塞项，判断玄学 agent 是否可进入内部试运行，以及为什么仍不能视为完整发布。

## 输入

- `root`：仓库根目录，默认当前目录。
- `codex_home`：可选，Skill 安装准备 dry-run 目标。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/试运行准备度报告.md`。

## 输出

遵循 [pilot-readiness-report.schema.json](../schemas/pilot-readiness-report.schema.json)。

关键字段：

- `pilot_status`
- `public_release_status`
- `automated_checks`
- `external_blockers`
- `summary`

## 判定

- `ready_for_internal_dry_run`：覆盖审计、路由冒烟、追踪矩阵、安装 dry-run 和审校包自动证据均通过。
- `blocked_by_external_evidence`：完整发布仍需要实际安装确认、真实匿名 transcript 和专家批准。

## 命令

```bash
python3 agent-tools/scripts/pilot_readiness_report.py --format markdown
```
