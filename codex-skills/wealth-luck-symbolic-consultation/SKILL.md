---
name: wealth-luck-symbolic-consultation
description: Use when the user asks about 招财, 财运, 求财, 旺财, 开财库, 补财库, 财库, 财神, 貔貅, 金蟾, 聚宝盆, prosperity, wealth luck, abundance, or money-luck symbols as symbolic budgeting, income-channel reflection, career action planning, spending-boundary setting, and low-risk reminder-object use. Blocks investment/gambling/debt advice, guaranteed wealth claims, debt desperation, expensive ritual pressure, fraud/illegal action, deity-command fear, coercion, and repeated dependency.
---

# Wealth Luck Symbolic Consultation

## Use When

- The user asks about 招财、财运、求财、旺财、开财库、补财库、财库、财神、貔貅、金蟾、聚宝盆, prosperity, wealth luck, abundance, or money-luck symbols.
- The user wants symbolic budgeting, income-channel reflection, career action planning, spending-boundary setting, or low-risk reminder-object use.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `wealth_luck_request_guard`.
3. If blocked, pause wealth-luck interpretation and reframe to budgeting, debt support, qualified financial/legal/tax support, emergency support, or grounded action.
4. If allowed, run `wealth_luck_context_recorder`.
5. Run `wealth_luck_symbol_lookup`.
6. Run `wealth_luck_action_planner`.
7. Draft with symbolic prosperity, budget, income-channel, and grounded-action language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/wealth_luck_request_guard.py`
- `agent-tools/scripts/wealth_luck_context_recorder.py`
- `agent-tools/scripts/wealth_luck_symbol_lookup.py`
- `agent-tools/scripts/wealth_luck_action_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: wealth-luck language is symbolic action planning, not a promise of wealth, returns, deity support, or luck changes.
- Context summary: wealth focus, current context, income channels, budget boundaries, existing symbols, practical actions, risk notes, review time, and stop condition.
- Symbol layer: prosperity/wealth motifs with cautious prompts.
- Action layer: budget, income-channel, client/career, spending-boundary, and review actions.
- Review layer: review time and stopping condition to avoid repeated checking, ritual loops, or impulse spending.

## Hard Stops

- Investment, gambling, lottery, debt, tax, legal, illegal-profit, fraud, guaranteed wealth, deity-command fear, expensive ritual pressure, coercion, or repeated dependency.

## References

- `知识库/SOP/51-招财财运财库象征咨询.md`
- `知识库/流派/招财财运与财库象征.md`
