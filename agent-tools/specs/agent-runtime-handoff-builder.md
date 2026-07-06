# Tool Spec：agent_runtime_handoff_builder

## 目的

汇总玄学 agent 接入运行时所需的入口、Skill、工具 manifest、安装准备、试运行准备度、外部证据入口和验证命令。

## 输入

- `root`：仓库根目录，默认当前目录。
- `codex_home`：可选，生成安装准备和外部证据命令时使用。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/Agent运行时交接包.md`。

## 输出

遵循 [agent-runtime-handoff-builder.schema.json](../schemas/agent-runtime-handoff-builder.schema.json)。

关键字段：

- `handoff_status`
- `entrypoints`
- `skills`
- `readiness_checks`
- `safety_invariants`
- `integration_contract`
- `verification_commands`

## 判定

- `ready_for_runtime_dry_run`：工具 manifest、路由冒烟、Skill 安装准备、试运行准备和外部证据入口均可生成并通过自动检查。
- `blocked_by_readiness_checks`：至少一个运行时交接前检查失败。

## 命令

```bash
python3 agent-tools/scripts/agent_runtime_handoff_builder.py --codex-home /tmp/mystic-codex-home-preview --format markdown
```
