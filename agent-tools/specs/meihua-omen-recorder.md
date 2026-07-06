# Tool Spec：meihua_omen_recorder

## 目的

把梅花易数里的外应先记录为事实观察，再进入象征取象。此工具不确认天意、灾祸、成败或他人真实想法，只帮助 agent 区分“看见/听见了什么”和“可以如何低风险联想”。

## 输入

- `question_text` / `question`：用户问题
- `omen_text` / `external_omen` / `text`：外应文本
- `observations`：可选，外应观察数组
- `source_type`：`self_observed`、`image_notes`、`audio_notes`、`third_party_report`、`dream`、`online_claim`、`unknown`
- `timing_relation`：`before_question`、`during_question`、`after_question`、`unknown`
- `direction`、`location`、`notes`：可选上下文

## 输出

遵循 [meihua-omen-recorder.schema.json](../schemas/meihua-omen-recorder.schema.json)。

关键字段：

- `source_type`
- `timing_relation`
- `observations`
- `risk_flags`
- `can_use_as_meihua_omen`
- `grounding_questions`
- `warnings`
- `limits`

## 规则

1. 缺少问题、外应文本或来源类型时，不进入取象。
2. 身体感受类外应先按现实身心状态处理，不作疾病或灾祸解释。
3. 第三方转述、梦境、网络说法只能作为弱材料，不能升格为事实证明。
4. 出现医疗、法律、财务、危机、隐私或操控风险时，暂停梅花外应解读。
5. 出现“天意、显灵、一定有灾”等表达时，先降级为观察事实和安定支持。

## 命令

```bash
python3 agent-tools/scripts/meihua_omen_recorder.py --question "这个项目沟通当前的主要阻力和下一步是什么？" --text "刚问完手机响了一声，客户群里有人发来延期消息" --source-type self_observed --timing after_question
```

## 与 Skill 的关系

`meihua-symbolic-consultation` 应在用户提供外应时先调用本工具；若外应被用于起卦，再用 `meihua_casting_recorder` 记录完整体用、动爻、互卦和变卦字段。最终草稿仍需通过 `mystic_output_lint`。
