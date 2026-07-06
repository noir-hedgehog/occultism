# Tool Spec：release_gate_runner

## 目的

一键运行玄学大典发布前质量门，并输出结构化验收报告。它把分散在仪表盘里的命令串起来，方便维护者确认当前知识库、工具、Skill 蓝图和验证资产是否处在可发布状态。

## 默认 Gate

- `schema_json`：所有 `agent-tools/schemas/*.json` 可解析。
- `codex_skill_blueprint_validator`：Skill 蓝图静态验证。
- `codex_skill_installer`：Skill 安装器 dry-run，确认 11 个蓝图可规划到 Codex skills 目录。
- `knowledge_coverage_audit`：知识库覆盖度审计。
- `skill_replay_runner`：当前 Skill 的 normal/blocked 回放。
- `skill_transcript_runner`：当前 Skill 的多轮 transcript 回放。
- `markdown_links`：Markdown 本地链接检查。
- `unit_tests`：`python3 -m unittest discover -s agent-tools/tests`。

## 输入

- `root`：可选，仓库根目录，默认当前目录。
- `gate`：可选，只运行指定 gate；可重复传入。

## 输出

遵循 [release-gate-runner.schema.json](../schemas/release-gate-runner.schema.json)。

关键字段：

- `gate_count`
- `passed_count`
- `failed_count`
- `gates[].summary`
- `gates[].errors`

## 命令

```bash
python3 agent-tools/scripts/release_gate_runner.py
python3 agent-tools/scripts/release_gate_runner.py --gate schema_json --gate markdown_links
```

## 局限

- 自动 gate 通过不代表真实匿名 transcript 已经扩充。
- 静态覆盖度不替代内容专家审校。
- Skill 迁移前仍建议做人工前向测试。
