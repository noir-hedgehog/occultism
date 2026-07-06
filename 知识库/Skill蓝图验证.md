# Skill 蓝图验证

## 用途

本页说明如何用 `codex_skill_blueprint_validator` 检查 `codex-skills` 下的 Skill 蓝图是否具备迁移到 Codex Skills 的基本条件。

## 运行方式

```bash
python3 agent-tools/scripts/codex_skill_blueprint_validator.py
```

## 检查范围

| 项目 | 要求 |
| --- | --- |
| Frontmatter | 只能包含 `name` 和 `description` |
| 命名 | `name` 必须与 skill 目录一致 |
| 触发描述 | `description` 应包含自然语言触发场景 |
| 章节 | `Workflow`、`Tool Hooks`、`Output Shape`、`References` 齐全 |
| 工具钩子 | `agent-tools/scripts/*.py` 路径存在 |
| 引用资料 | `知识库/*.md` 路径存在 |
| Skill 索引 | `codex-skills/index.md` 依赖工具与 SKILL.md 工具钩子一致 |

## 与其他验证的关系

- `codex_skill_blueprint_validator`：静态检查 Skill 蓝图结构。
- `skill_replay_runner`：检查 normal/blocked 短请求流程。
- `skill_transcript_runner`：检查多轮状态转移和边界处理。
- `knowledge_coverage_audit`：检查整个知识库和工具覆盖。

## 局限

- 静态验证不能证明真实对话质量。
- 工具路径存在不代表工具输出一定适合当前请求。
- 迁移到真实 Codex Skills 前仍需前向测试。
