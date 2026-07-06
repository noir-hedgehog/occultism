---
name: cartomancy-symbolic-consultation
description: Use when the user asks about 扑克牌占卜, 扑克牌算命, 纸牌占卜, 扑克牌解读, cartomancy, playing card reading, or standard playing-card symbolic consultation. Blocks gambling, investment, professional replacement, fate certainty, third-party mind reading, coercion, and repeated dependency.
---

# Cartomancy Symbolic Consultation

## Use When

- The user asks about 扑克牌占卜, 扑克牌算命, 纸牌占卜, 扑克牌解读, cartomancy, or playing card reading.
- The user has playing cards to record, wants cultural learning, or wants low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `cartomancy_request_guard`.
3. If blocked, pause cartomancy consultation and reframe to safety, professional support, privacy, budget/risk support, or grounding.
4. If allowed, run `cartomancy_draw_recorder`.
5. Run `cartomancy_card_lookup` for known cards.
6. Run `cartomancy_interpretation_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/cartomancy_request_guard.py`
- `agent-tools/scripts/cartomancy_draw_recorder.py`
- `agent-tools/scripts/cartomancy_card_lookup.py`
- `agent-tools/scripts/cartomancy_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: playing cards are symbolic prompts, not facts or predictions.
- Draw summary: question, deck type, spread, cards, source, focus, and missing fields.
- Symbol layer: card-by-card prompts and a cautious combination summary.
- Reality layer: evidence checks, communication, practical next step, and dependency stop conditions.

## Hard Stops

- Gambling, investment, loans, lottery, medical, legal, safety, or mental-health replacement.
- Fate certainty, repeated drawing until satisfied, or treating cards as commands.
- Third-party mind reading, privacy invasion, coercion, revenge, or forced reunion.

## References

- `知识库/SOP/29-扑克牌占卜象征咨询.md`
- `知识库/流派/扑克牌占卜.md`
