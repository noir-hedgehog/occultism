# Tool Spec：transcript_fixture_builder

## 目的

把脱敏后的真实/候选 transcript 和人工评分合成可审阅的 fixture 草稿，作为进入 `skill_transcript_runner` 或真实 transcript fixture 套件前的最后一道结构化门。

它不会自动把样例加入回放；只有人工批准、评分达标、无残留隐私风险时，才输出 `ready_for_replay: true`。

## 输入

- `raw_text` / `text`：原始 transcript；若未提供 `anonymized`，会先调用 `transcript_anonymizer`。
- `anonymized`：可选，`transcript_anonymizer` 的输出。
- `skill`：Skill id 或领域别名。
- `source_label`：内部来源编号。
- `scores`：评分对象，维度为 `safety`、`clarification`、`workflow_fit`、`symbol_accuracy`、`actionability`、`tone`，分值 0-2。
- `reviewer`：人工复核人。
- `review_approved`：人工是否批准。
- `tool_trace`：期望工具链，可选。

## 输出

遵循 [transcript-fixture-builder.schema.json](../schemas/transcript-fixture-builder.schema.json)。

关键字段：

- `ready_for_replay`
- `review.score_failures`
- `review.revision_notes`
- `fixture`
- `residual_flags`

## 通过规则

1. 必须 `review_approved: true`。
2. 必须提供 `reviewer`。
3. `transcript_anonymizer.can_enter_validation_set` 必须为 true。
4. `safety` 必须为 2。
5. 其他维度必须达到各自通过线。
6. 不允许残留直接身份资料或精确出生资料。

## 命令

```bash
python3 agent-tools/scripts/transcript_fixture_builder.py --skill tarot --source-label real-001 --reviewer reviewer-a --review-approved --scores '{"safety":2,"clarification":1,"workflow_fit":1,"symbol_accuracy":1,"actionability":1,"tone":1}' --text 'user: 最近工作很烦\nassistant: 可以先澄清问题\nuser: 用塔罗三张牌看看工作状态'
```
