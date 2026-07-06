---
name: yijing-symbolic-consultation
description: Use when a user asks Codex for I Ching, Yijing, Zhouyi, hexagram, 周易, 易经 divination, question framing, casting method selection, repeat-question boundaries, casting record support, classical text/commentary source attribution, or symbolic change analysis with one-question-at-a-time safety boundaries.
---

# Yijing Symbolic Consultation

Use this skill to run a safe, structured Yijing consultation. Treat the result as symbolic change analysis, not deterministic prediction. Use `liuyao-symbolic-consultation` for 六爻-specific 六亲、六神、世应 or 用神 interpretation.

## Workflow

1. Run intake using `agent-tools/scripts/mystic_intake_triage.py` when available.
2. Run `yijing_question_guard` when available.
3. Continue only when the question is one matter, not repeated, and not a crisis/professional/coercive request.
4. Confirm the reframed question before any casting or interpretation.
5. Run `yijing_casting_method_advisor` before any casting or hexagram recording to choose manual, external, three-coins, or yarrow-stalk flow and to re-check repeat-question boundaries.
6. If the user has not cast a hexagram, ask whether they want to cast manually or use `yijing_casting_simulator`; retain the seed for simulated casts.
7. Record casting method, time, timezone, original question, reframed question, base hexagram, changing lines, and changed hexagram with `yijing_hexagram_record` when available, or use the simulator's `recorded_cast`.
8. Lookup base and changed hexagram structure with `yijing_hexagram_lookup` when available.
9. Lookup each changing line with `yijing_line_lookup` when available.
10. When quoting or using classical text, commentary, modern translations, internet claims, or lineage claims, run `yijing_source_reference_guard` when available.
11. Use `symbolic_depth_lookup` when available to select the safe depth pattern for question reframing, hexagram-line layering, or changed-hexagram comparison.
12. Interpret by structure: base situation, changing lines, changed tendency, practical action.
13. Draft the answer, then run or mentally apply `mystic_output_lint`.
14. End with limits and grounded next steps.

## Tool Hooks

Run general intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain yijing
```

Guard the Yijing question:

```bash
python3 agent-tools/scripts/yijing_question_guard.py --text "<user request>"
```

Choose or validate casting method:

```bash
python3 agent-tools/scripts/yijing_casting_method_advisor.py --text "<reframed question>" --method three_coins --user-consent-to-simulation
python3 agent-tools/scripts/yijing_casting_method_advisor.py --json '{"question_text":"<reframed question>","previous_questions":["<previous question>"],"requested_method":"three_coins","user_consent_to_simulation":true}'
```

Simulate casting when the user accepts agent-randomized casting:

```bash
python3 agent-tools/scripts/yijing_casting_simulator.py --method three_coins --seed "<optional seed>" --question "<reframed question>"
```

Record the hexagram:

```bash
python3 agent-tools/scripts/yijing_hexagram_record.py --json '{"question_text":"<reframed question>","casting_method":"manual","lines":[7,7,7,7,7,7]}'
```

Lookup hexagram structure:

```bash
python3 agent-tools/scripts/yijing_hexagram_lookup.py --query "<hexagram name or number>"
```

Lookup a changing line:

```bash
python3 agent-tools/scripts/yijing_line_lookup.py --query "<hexagram name or number>" --line 3
```

Guard source attribution:

```bash
python3 agent-tools/scripts/yijing_source_reference_guard.py --text "<source quote or claim>" --source-type internet_claim
```

Look up the depth pattern:

```bash
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain yijing --query "<question boundary, hexagram, or changing line>"
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
问题守门：
问题重述：
起卦记录：
卦象结构：
变化重点：
现实映射：
建议行动：
限制与提醒：
```

## References

- `知识库/SOP/04-易经占问.md`
- `知识库/流派/易经.md`
- `知识库/流派/易经64卦速查.md`
- `知识库/流派/易经384爻索引.md`
- `知识库/流派/易经原典注疏来源规范.md`
- `知识库/流派/跨流派深度解读矩阵.md`
