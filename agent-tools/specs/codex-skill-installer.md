# Tool Spec：codex_skill_installer

## 目的

把 `codex-skills/*/SKILL.md` 蓝图迁移到 Codex 的 Skills 目录，默认只做 dry-run 安装计划，避免无意覆盖用户已有 Skill。

## 输入

- `root`：仓库根目录，默认当前目录。
- `codex_home`：目标 Codex home，默认 `CODEX_HOME` 或 `~/.codex`。
- `skill`：可选，限制安装某几个 Skill。
- `install`：命令行显式写入开关；不传时为 dry-run。
- `overwrite`：命令行显式覆盖开关；目标已存在且内容不同，默认标记 conflict。

## 输出

遵循 [codex-skill-installer.schema.json](../schemas/codex-skill-installer.schema.json)。

关键字段：

- `actions[].action`：`create`、`already_current`、`overwrite`、`conflict_existing` 或 `invalid_blueprint`
- `actions[].conflict`：是否需要人工处理
- `actions[].copied`：本次是否实际写入
- `validation_summary`：安装前蓝图验证结果

## 规则

1. 安装前必须调用 `codex_skill_blueprint_validator`，只有有效蓝图才可写入。
2. 默认 dry-run，不创建或覆盖任何目标目录。
3. 目标目录不存在时，计划为 `create`。
4. 目标目录与蓝图完全一致时，计划为 `already_current`。
5. 目标目录存在且内容不同，未传 `--overwrite` 时，计划为 `conflict_existing`。
6. 只有同时传 `--install` 和必要时的 `--overwrite` 才写入目标目录。

## 命令

```bash
python3 agent-tools/scripts/codex_skill_installer.py
python3 agent-tools/scripts/codex_skill_installer.py --codex-home /tmp/codex-home --install
python3 agent-tools/scripts/codex_skill_installer.py --skill tarot-symbolic-reading --install --overwrite
```
