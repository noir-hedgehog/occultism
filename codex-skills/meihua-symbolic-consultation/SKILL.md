---
name: meihua-symbolic-consultation
description: Use when a user asks Codex for Meihua Yishu, Plum Blossom divination, 梅花易数, 梅花占, 报数起卦, 起卦记录, 外应, 外应记录, 体卦, 用卦, 互卦, 变卦, 动爻, 体用关系解释, or body-use symbolic consultation with one-question-at-a-time, method-source, non-deterministic, and safety boundaries.
---

# Meihua Symbolic Consultation

Use this skill for safe, structured Meihua Yishu consultation. Treat the chart and omens as symbolic change analysis and question framing, not deterministic prediction, supernatural confirmation, professional advice, or coercion.

## Workflow

1. Run general intake using `agent-tools/scripts/mystic_intake_triage.py` when available.
2. Run `yijing_question_guard` when available because Meihua still requires one matter, no repeated divination, and high-risk screening.
3. Continue only when the question is one matter, not repeated, and not crisis/professional/coercive.
4. Confirm the reframed question before any casting or interpretation.
5. If the user has no source, ask for number, time, observed external omen, direction, or external chart; do not invent a trigger or chart.
6. Run `meihua_omen_recorder` when the user provides an observed external omen; record facts before any symbolic association.
7. Run `meihua_casting_recorder` when the user provides report numbers, time, omen, direction, external chart fields, body/use trigrams, moving line, mutual hexagram or changed hexagram.
8. Record or ask for source, body hexagram, use hexagram, moving line, mutual hexagram, changed hexagram, and body-use five-phase relation when available.
9. Run `meihua_relation_interpreter` when a valid body/use relation is available and the user wants the relation translated into resources, pressure, and next steps.
10. Use `meihua_symbol_lookup` when explaining body/use structure, methods, omens, five-phase relations, or trigram symbols.
11. Interpret by layers: source limits, question boundary, body-use logic, trigger symbols, real-world mapping, observable signals, low-risk next steps.
12. Draft the answer, then run or mentally apply `mystic_output_lint`.
13. End with method limits, non-determinism, anti-fear language, and professional-advice limits.

## Tool Hooks

Run general intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain meihua
```

Guard the question:

```bash
python3 agent-tools/scripts/yijing_question_guard.py --text "<user request>"
```

Record Meihua casting fields:

```bash
python3 agent-tools/scripts/meihua_casting_recorder.py --json '{"question_text":"这个项目沟通当前的主要阻力和下一步是什么？","casting_method":"number_casting","numbers":[27,14],"body_trigram":"离","use_trigram":"坎","moving_line":3,"base_hexagram":"火水未济","mutual_hexagram":"水火既济","changed_hexagram":"火风鼎"}'
```

Record Meihua external omen observations:

```bash
python3 agent-tools/scripts/meihua_omen_recorder.py --question "这个项目沟通当前的主要阻力和下一步是什么？" --text "刚问完手机响了一声；客户群里有人发来延期消息" --source-type self_observed --timing after_question
```

Interpret body-use relation:

```bash
python3 agent-tools/scripts/meihua_relation_interpreter.py --json '{"question_text":"这个项目沟通当前的主要阻力和下一步是什么？","casting_method":"number_casting","numbers":[27,14],"body_trigram":"离","use_trigram":"坎","moving_line":3}'
```

Lookup Meihua terms:

```bash
python3 agent-tools/scripts/meihua_symbol_lookup.py --query 体卦 --category structure --focus project
python3 agent-tools/scripts/meihua_symbol_lookup.py --query 外应 --category method
python3 agent-tools/scripts/meihua_symbol_lookup.py --query 生体 --category relation
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
问题守门：
起卦来源：
起卦记录：
体用与动爻：
互卦/变卦：
取象解释：
现实映射：
可观察信号：
低风险建议：
限制与提醒：
```

## References

- `知识库/SOP/11-梅花易数占问.md`
- `知识库/流派/梅花易数.md`
- `知识库/SOP/04-易经占问.md`
- `知识库/流派/易经.md`
