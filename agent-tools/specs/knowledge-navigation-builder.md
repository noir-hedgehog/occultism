# Tool Spec：knowledge_navigation_builder

## 目的

生成给维护者阅读的知识库导航摘要，并输出可测试的结构化证据。

它把覆盖审计、工具 manifest、看板和知识库目录整合为一个入口，用于确认“给人看的知识库和看板”能被快速浏览和维护。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：输出格式，`json` 或 `markdown`，默认 `json`。
- `write`：可选，把 Markdown 输出写入 `知识库/导航索引.md`。

## 输出

遵循 [knowledge-navigation-builder.schema.json](../schemas/knowledge-navigation-builder.schema.json)。

关键字段：

- `document_count`
- `domain_count`
- `complete_domain_count`
- `tool_count`
- `skill_count`
- `kanban_counts`
- `primary_navigation`
- `domains`
- `generated_markdown`

## 判定

- `is_valid: true`：覆盖审计和工具 manifest 都通过，导航数据可作为当前知识库入口。
- `is_valid: false`：先修覆盖审计或工具 manifest 缺口。

## 命令

```bash
python3 agent-tools/scripts/knowledge_navigation_builder.py
python3 agent-tools/scripts/knowledge_navigation_builder.py --format markdown
```
