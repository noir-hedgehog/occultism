# Tool Spec：codex_skill_blueprint_validator

## 目的

检查 `codex-skills/*/SKILL.md` 是否具备迁移到 Codex Skills 的基本条件：

- frontmatter 只有 `name` 和 `description`
- `name` 与目录名一致
- `description` 含触发语义
- `Workflow`、`Tool Hooks`、`Output Shape`、`References` 章节齐全
- 引用的 `知识库/*.md` 文件存在
- 工具钩子脚本存在
- `codex-skills/index.md` 的依赖工具与 SKILL.md 的工具钩子一致

它是 Skill 蓝图静态验证器，不替代回放测试或人工前向测试。

## 输入

- `root`：可选，仓库根目录，默认当前目录。

## 输出

遵循 [codex-skill-blueprint-validator.schema.json](../schemas/codex-skill-blueprint-validator.schema.json)。

关键字段：

- `skills[].frontmatter_keys`
- `skills[].referenced_tools`
- `skills[].index_declared_tools`
- `skills[].missing_references`
- `skills[].missing_tool_scripts`
- `skills[].errors`
- `skills[].warnings`

## 规则

1. frontmatter 不允许除 `name`、`description` 外的其他字段。
2. SKILL.md 中出现的 `agent-tools/scripts/*.py` 必须存在。
3. References 中出现的 `知识库/*.md` 必须存在。
4. index 中列出的工具应与 SKILL.md 工具钩子保持一致。
5. 通过静态验证后仍需运行 `skill_replay_runner` 和 `skill_transcript_runner`。

## 命令

```bash
python3 agent-tools/scripts/codex_skill_blueprint_validator.py
```
