---
name: liuyao-symbolic-consultation
description: Use when a user asks Codex for Liuyao, six-line divination, 六爻, 六爻盘, 盘式记录, 六亲, 六神, 世爻, 应爻, 用神, 候选用神, 官鬼, 妻财, 青龙, 白虎, or six-line chart symbolic consultation with one-question-at-a-time, method-source, privacy, and non-deterministic safety boundaries.
---

# Liuyao Symbolic Consultation

Use this skill for safe, structured Liuyao six-line consultation. Treat the chart as symbolic change analysis and question framing, not deterministic prediction, professional advice, coercion, or third-party surveillance.

## Workflow

1. Run general intake using `agent-tools/scripts/mystic_intake_triage.py` when available.
2. Run `yijing_question_guard` when available because Liuyao still requires one matter, no repeated divination, and high-risk screening.
3. Continue only when the question is one matter, not repeated, and not crisis/professional/coercive.
4. Confirm the reframed question before any casting or interpretation.
5. If the user has no chart, ask them to provide an external chart or explicitly choose a casting workflow; do not invent line roles.
6. Run `liuyao_chart_recorder` when the user provides an external chart, base/changed hexagrams, changing lines, self/other lines, six kinship, six spirits, focus spirit or focus logic.
7. Run `liuyao_focus_selector` after chart recording, or before chart interpretation, to generate candidate focus spirits and confirm they are only candidates.
8. Record or ask for method, source, base hexagram, changed hexagram, changing lines, subject/object lines, six kinship, six spirits, and focus spirit when available.
9. Use `liuyao_symbol_lookup` when explaining six kinship, six spirits, subject/object roles, focus/support/blocking roles, or line positions.
10. Interpret by layers: source limits, question boundary, focus logic, line-role symbols, real-world mapping, observable signals, low-risk next steps.
11. Draft the answer, then run or mentally apply `mystic_output_lint`.
12. End with method limits, non-determinism, privacy and professional-advice limits.

## Tool Hooks

Run general intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain liuyao
```

Guard the question:

```bash
python3 agent-tools/scripts/yijing_question_guard.py --text "<user request>"
```

Record Liuyao chart fields:

```bash
python3 agent-tools/scripts/liuyao_chart_recorder.py --json '{"question_text":"这个项目合作当前的主要阻力和下一步是什么？","casting_method":"external_chart","chart_source":"用户提供外部盘","base_hexagram":"泽雷随","changed_hexagram":"水雷屯","focus_spirit":"官鬼","focus_logic":"项目合作以应爻和官鬼为外部压力观察点","lines":[{"position":1,"yin_yang":"yang","kinship":"父母","spirit":"青龙"},{"position":2,"yin_yang":"yin","kinship":"兄弟","spirit":"朱雀","roles":["世爻"]},{"position":3,"yin_yang":"yang","kinship":"官鬼","spirit":"勾陈","roles":["应爻","用神"],"changing":true},{"position":4,"yin_yang":"yin","kinship":"妻财","spirit":"腾蛇"},{"position":5,"yin_yang":"yang","kinship":"子孙","spirit":"白虎"},{"position":6,"yin_yang":"yin","kinship":"父母","spirit":"玄武"}]}'
```

Select candidate Liuyao focus spirits:

```bash
python3 agent-tools/scripts/liuyao_focus_selector.py --json '{"question_text":"这个项目合作当前的主要阻力和下一步是什么？","casting_method":"external_chart","chart_source":"用户提供外部盘","base_hexagram":"泽雷随","changed_hexagram":"水雷屯","focus_spirit":"官鬼","focus_logic":"项目合作以应爻和官鬼为外部压力观察点","lines":[{"position":1,"yin_yang":"yang","kinship":"父母","spirit":"青龙"},{"position":2,"yin_yang":"yin","kinship":"兄弟","spirit":"朱雀","roles":["世爻"]},{"position":3,"yin_yang":"yang","kinship":"官鬼","spirit":"勾陈","roles":["应爻","用神"],"changing":true},{"position":4,"yin_yang":"yin","kinship":"妻财","spirit":"腾蛇"},{"position":5,"yin_yang":"yang","kinship":"子孙","spirit":"白虎"},{"position":6,"yin_yang":"yin","kinship":"父母","spirit":"玄武"}]}'
```

Lookup Liuyao terms:

```bash
python3 agent-tools/scripts/liuyao_symbol_lookup.py --query 官鬼 --category kinship --focus project
python3 agent-tools/scripts/liuyao_symbol_lookup.py --query 世爻 --category role
python3 agent-tools/scripts/liuyao_symbol_lookup.py --query 青龙 --category spirit
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
问题守门：
起卦/盘式来源：
盘式记录：
取用逻辑：
六亲/六神/世应：
变化结构：
现实映射：
可观察信号：
低风险建议：
限制与提醒：
```

## References

- `知识库/SOP/10-六爻占问.md`
- `知识库/流派/六爻.md`
- `知识库/SOP/04-易经占问.md`
- `知识库/流派/易经.md`
