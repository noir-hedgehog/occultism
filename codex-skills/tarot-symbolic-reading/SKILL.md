---
name: tarot-symbolic-reading
description: Use when a user asks Codex for Tarot reading, Tarot spread selection, card interpretation, multi-card combination reading, reversal cluster analysis, symbolic reflection, relationship/work/self tarot analysis, or wants a structured non-deterministic tarot session with safety boundaries.
---

# Tarot Symbolic Reading

Use this skill to run a safe, structured Tarot session. Treat Tarot as symbolic reflection, not deterministic prediction.

## Workflow

1. Run intake using `agent-tools/scripts/mystic_intake_triage.py` when available; otherwise apply `知识库/01-安全边界.md`.
2. Refuse or redirect medical, legal, financial, self-harm, coercive, or crisis requests.
3. Restate the user's question in a non-deterministic form.
4. Select a spread with `tarot_spread_selector` when available:
   - One card: quick focus.
   - Three cards: situation, obstacle, advice.
   - Two paths: option A, option B, shared guidance.
   - Relationship mirror: user state, other person's possible state, interaction pattern, boundary advice.
5. If cards are not provided, ask whether the user wants to provide cards or wants a simulated draw.
6. Simulate cards with `tarot_draw_simulator` when the user accepts randomization; retain the seed.
7. Record provided cards with `tarot_draw_recorder` when available, or use the simulator's `recorded_draw`.
8. Look up card symbolism with `tarot_card_lookup` when available.
9. Build an interpretation plan with `tarot_interpretation_planner` when available.
10. For spreads with 2+ cards, build a combination plan with `tarot_combination_planner` when available.
11. Use `symbolic_depth_lookup` when available to select the safe depth pattern for reversals, spread positions, or multi-card interaction.
12. Interpret cards by position, card symbolism, reversal strategy, interactions, reality mapping, and action.
13. Draft the answer, then run or mentally apply `mystic_output_lint`.
14. End with limits and 1-3 grounded next steps.

## Tool Hooks

Use the intake tool before interpreting:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain tarot
```

Continue only when `risk_level` is `green` or `yellow`. For `orange` or `red`, pause Tarot and follow the tool's `allowed_next_steps`.

Select the spread:

```bash
python3 agent-tools/scripts/tarot_spread_selector.py --text "<user request>"
```

Simulate a draw when the user wants agent-randomized cards:

```bash
python3 agent-tools/scripts/tarot_draw_simulator.py --spread-id three_card_situation --seed "<optional seed>"
```

Record the draw:

```bash
python3 agent-tools/scripts/tarot_draw_recorder.py --json '{"spread_id":"single_focus","cards":[{"card":"The Fool","orientation":"upright"}]}'
```

Look up card symbolism:

```bash
python3 agent-tools/scripts/tarot_card_lookup.py --card "<card name>" --orientation "<upright|reversed>"
```

Build an interpretation plan:

```bash
python3 agent-tools/scripts/tarot_interpretation_planner.py --json '{"question_text":"<question>","spread_id":"three_card_situation","cards":[{"card":"The Fool","orientation":"upright"},{"card":"Three of Swords","orientation":"reversed"},{"card":"King of Pentacles","orientation":"upright"}]}'
```

Build a combination plan for multi-card spreads:

```bash
python3 agent-tools/scripts/tarot_combination_planner.py --json '{"question_text":"<question>","spread_id":"three_card_situation","cards":[{"card":"The Fool","orientation":"upright"},{"card":"Three of Swords","orientation":"reversed"},{"card":"King of Pentacles","orientation":"reversed"}]}'
```

Look up the depth pattern:

```bash
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain tarot --query "<spread position, reversal, or interaction>"
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
问题重述：
牌阵：
牌面记录：
象征解读：
现实映射：
建议行动：
限制与提醒：
```

## References

- `知识库/SOP/01-塔罗解读.md`
- `知识库/流派/塔罗.md`
- `知识库/流派/塔罗牌义速查.md`
- `知识库/流派/塔罗牌阵案例与逆位策略.md`
- `知识库/流派/跨流派深度解读矩阵.md`
