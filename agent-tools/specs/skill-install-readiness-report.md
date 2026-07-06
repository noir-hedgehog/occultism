# Tool Spec：skill_install_readiness_report

## 目的

生成 Codex Skill 安装前的 dry-run 准备报告，汇总目标路径、将创建/已存在/冲突的 Skill、审批清单和安装命令。

它不会安装或覆盖任何文件，只用于把“待用户显式确认”的安装步骤变成可审阅证据。

## 输入

- `root`：仓库根目录，默认当前目录。
- `codex_home`：目标 Codex home，默认 `CODEX_HOME` 或 `~/.codex`。
- `skill`：可选，只报告指定 Skill，可重复。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/Skill安装准备报告.md`。

## 输出

遵循 [skill-install-readiness-report.schema.json](../schemas/skill-install-readiness-report.schema.json)。

关键字段：

- `status`
- `requires_explicit_approval`
- `actions`
- `approval_checklist`
- `install_command`
- `blockers`

## 判定

- `ready_for_install_approval`：dry-run、蓝图验证和覆盖审计通过，可请求用户显式安装确认。
- `blocked`：目标已有冲突、蓝图验证失败或覆盖审计失败。
- `requires_explicit_approval: true`：无论状态如何，此工具都不应自动安装。

## 命令

```bash
python3 agent-tools/scripts/skill_install_readiness_report.py --format markdown
```
