# Tool Spec：content_review_feedback_recorder

## 目的

记录内容专家对某个流派审校包的结构化反馈，包括批准范围、必改项、残余风险和是否可计入内容批准。

它承接 `content_review_packet_builder`，用于把审校人的口头或文档反馈转成可审计 JSON。

## 输入

- `domain`：流派 id，例如 `tarot`、`fengshui`、`ritual`。
- `reviewer`：审校人姓名、角色或内部编号。
- `review_date`：审校日期，格式 `YYYY-MM-DD`。
- `decision`：`approved`、`changes_requested` 或 `rejected`。
- `approved_scope`：批准范围，可多项。
- `required_corrections`：必改项，可多项。
- `residual_risks`：残余风险，可多项。
- `notes`：审校备注，可多项。

## 输出

遵循 [content-review-feedback-recorder.schema.json](../schemas/content-review-feedback-recorder.schema.json)。

关键字段：

- `is_valid`
- `status`
- `can_count_as_content_approval`
- `approved_scope`
- `required_corrections`
- `kanban_updates`
- `errors`

## 判定

- `can_count_as_content_approval: true`：审校人、日期、批准范围、`decision: approved` 齐全，且没有必改项。
- `status: needs_revision`：审校人要求修改，输出可转入看板的 `kanban_updates`。
- `status: not_approved`：拒绝、缺字段或证据不合格。

## 命令

```bash
python3 agent-tools/scripts/content_review_feedback_recorder.py --domain tarot --reviewer "tarot-reviewer" --review-date 2026-07-02 --decision approved --approved-scope "塔罗 SOP、知识卡、Skill 和工具 spec"
```
