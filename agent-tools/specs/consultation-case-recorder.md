# Tool Spec：consultation_case_recorder

## 目的

把一次咨询从“可运行流程”推进到“可复盘案例候选”：记录交接包状态、结构化预览证据、草稿 lint、用户回访、结果验证、脱敏状态和人工审校门槛。

它不把案例自动写入正式案例库，也不声称玄学结论被证实；它只生成可审校、可追溯的案例证据包。

## 输入

- `request_text`：用户原始请求。若提供 `handoff_result`，可从其中读取。
- `handoff_result`：可选，来自 `consultation_handoff_builder` 或 `/api/handoff`。
- `preview_result`：可选，若没有 `handoff_result`，会传给 handoff builder。
- `draft_output`：可选，若没有 `handoff_result`，会传给 handoff builder 做 lint。
- `follow_up_text`：可选，用户或维护者的回访文本。
- `follow_up_window_days`：可选，回访窗口。
- `observed_changes`：可选，现实变化或行动结果。
- `validation_result`：`unverified`、`supports_practical_use`、`mixed`、`no_support` 或 `safety_only`。
- `reviewer`、`review_approved`：人工审校信息。

## 输出

遵循 [consultation-case-recorder.schema.json](../schemas/consultation-case-recorder.schema.json)。

关键字段：

- `case_status`：案例是否还缺回访、缺审校、脱敏不足，或已可进入案例库。
- `ready_for_case_library`：是否满足非 unverified 回访结果、人工批准、脱敏通过和 lint 未阻断。
- `ready_for_replay`：是否可进一步进入 transcript/fixture 回放候选。
- `anonymized_transcript`：最小化 transcript 的脱敏和风险/隐私标记。
- `outcome`：回访与结果验证记录。
- `review.required_before_library`：进入案例库前仍需补齐的门槛。

## 命令

```bash
python3 agent-tools/scripts/consultation_case_recorder.py --text "帮我做一个塔罗三张牌，看看工作状态" --follow-up "用户回访：整理事实后沟通更清楚" --validation-result supports_practical_use --reviewer reviewer-a --review-approved
```
