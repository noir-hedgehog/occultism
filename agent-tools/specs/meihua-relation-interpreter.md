# Tool Spec：meihua_relation_interpreter

## 目的

把梅花易数的体用生克关系转译成安全的资源、压力、行动提示。此工具不自动排卦、不补数字、不判断成败吉凶，只在已有 `meihua_casting_recorder` 记录有效时生成解释框架。

## 输入

- `casting_record`：可选，`meihua_casting_recorder` 的输出。
- 或直接传入 `meihua_casting_recorder` 支持的起卦字段：`question_text`、`casting_method`、`numbers`、`body_trigram`、`use_trigram`、`moving_line` 等。
- `focus` / `interpretation_request`：可选，本次解释关注点。

## 输出

遵循 [meihua-relation-interpreter.schema.json](../schemas/meihua-relation-interpreter.schema.json)。

关键字段：

- `question_domain`
- `body_use_relation`
- `computed_body_use_relation`
- `interpretation_frame`
- `can_interpret_relation`
- `risk_flags`
- `warnings`
- `limits`

## 规则

1. 起卦字段缺失或 `casting_record` 无效时，不解释体用关系，只返回缺失字段和追问方向。
2. 优先使用可计算的 `computed_body_use_relation`，以减少用户手填关系错误带来的漂移。
3. `生体`、`克体`、`体生用`、`体克用`、`比和` 分别转译为资源进入、外压约束、主体投入、主体可控、同气/僵持。
4. 解释必须包含现实证据问题和低风险行动，不允许输出必成、必败、疾病、财富、婚恋或灾祸确定断言。
5. 涉及医疗、法律、财务、危机、人身安全、隐私或操控他人时，暂停体用解释并转现实支持。

## 命令

```bash
python3 agent-tools/scripts/meihua_relation_interpreter.py --json '{"question_text":"这个项目沟通当前的主要阻力和下一步是什么？","casting_method":"number_casting","numbers":[27,14],"body_trigram":"离","use_trigram":"坎","moving_line":3}'
```

## 与 Skill 的关系

`meihua-symbolic-consultation` 在完成 `meihua_casting_recorder` 后，若体卦、用卦、动爻和体用关系有效，应调用本工具生成解释框架；若用户只提供外应，仍先用 `meihua_omen_recorder` 记录事实观察。最终答复必须通过 `mystic_output_lint`。
