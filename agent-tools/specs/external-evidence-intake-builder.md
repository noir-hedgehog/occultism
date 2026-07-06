# Tool Spec：external_evidence_intake_builder

## 目的

把完整发布前仍需要外部提供的证据转成可收集、可验收、可放进看板追踪的 intake 包。

## 输入

- `root`：仓库根目录，默认当前目录。
- `codex_home`：可选，生成 Skill 安装确认命令时使用的 Codex home。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/外部证据入口包.md`。

## 输出

遵循 [external-evidence-intake-builder.schema.json](../schemas/external-evidence-intake-builder.schema.json)。

关键字段：

- `status`
- `intake_items`
- `required_fields`
- `evidence_acceptance`
- `command_templates`

## 判定

- `ready_for_external_collection`：覆盖审计、Skill 安装 dry-run 和内容审校包自动证据可以支撑开始收集外部证据。
- `blocked_by_automated_checks`：自动证据仍有缺口，应先修复仓库内产物。

## 命令

```bash
python3 agent-tools/scripts/external_evidence_intake_builder.py --codex-home /tmp/mystic-codex-home-preview --format markdown
```
