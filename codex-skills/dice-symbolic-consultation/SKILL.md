---
name: dice-symbolic-consultation
description: Use when the user asks about 星骰, 占星骰, 占卜骰, 骰子占卜, astrodice, astro dice, divination dice, or planet/sign/house dice symbolic consultation. Blocks gambling, investment, professional replacement, fate certainty, third-party mind reading, coercion, and repeated dependency.
---

# Dice Symbolic Consultation

## Use When

- The user asks about 星骰, 占星骰, 占卜骰, 骰子占卜, astrodice, astro dice, or divination dice.
- The user has dice faces to record, wants cultural learning, or wants low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `dice_request_guard`.
3. If blocked, pause dice consultation and reframe to safety, professional support, privacy, budget/risk support, or grounding.
4. If allowed, run `dice_roll_recorder`.
5. Run `dice_symbol_lookup` for known faces.
6. Run `dice_interpretation_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/dice_request_guard.py`
- `agent-tools/scripts/dice_roll_recorder.py`
- `agent-tools/scripts/dice_symbol_lookup.py`
- `agent-tools/scripts/dice_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: dice are symbolic prompts, not facts or predictions.
- Roll summary: question, dice system, faces, source, focus, and missing fields.
- Symbol layer: face-by-face prompts and a cautious combination summary.
- Reality layer: evidence checks, communication, practical next step, and stop conditions.

## Hard Stops

- Gambling, investment, loans, lottery, medical, legal, safety, or mental-health replacement.
- Fate certainty, repeated rolling until satisfied, or treating dice as commands.
- Third-party mind reading, privacy invasion, coercion, revenge, or forced reunion.

## References

- `知识库/SOP/27-星骰占卜骰象征咨询.md`
- `知识库/流派/星骰与占卜骰.md`
