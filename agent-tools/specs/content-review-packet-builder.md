# Tool Spec：content_review_packet_builder

## 目的

生成内容专家审校包，把每个流派的 SOP、知识卡、Skill、工具 spec、审校问题和开放事项汇总到一处。

它解决“材料已经自动验证，但还需要人工审校”的交接问题；不会把 `ready_for_human_review` 误写成内容已批准。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：输出格式，`json` 或 `markdown`，默认 `json`。
- `write`：可选，把 Markdown 输出写入 `知识库/内容审校包.md`。

## 输出

遵循 [content-review-packet-builder.schema.json](../schemas/content-review-packet-builder.schema.json)。

关键字段：

- `packets`
- `review_questions`
- `required_evidence`
- `open_items`
- `approved_count`
- `generated_markdown`

## 判定

- `is_valid: true`：覆盖审计和工具 manifest 均通过，材料可进入人工审校。
- `review_status: ready_for_human_review`：该流派材料齐全，但仍未获内容专家批准。
- `approved_count: 0`：当前工具不记录专家签字，只准备审校包。

## 命令

```bash
python3 agent-tools/scripts/content_review_packet_builder.py
python3 agent-tools/scripts/content_review_packet_builder.py --format markdown
```
