---
name: character-divination-symbolic-consultation
description: Use when the user asks about 测字, 拆字, 字占, 字测, 看字, 测一个字, 拆一个字, character divination, or Chinese character symbolic consultation. Blocks professional replacement, gambling/investment, fate certainty, spirit fear, curse/exorcism confirmation, lifespan/personality labels, minor labeling, third-party mind reading, coercion, and repeated dependency.
---

# Character Divination Symbolic Consultation

## Use When

- The user asks about 测字, 拆字, 字占, 字测, 看字, 测一个字, 拆一个字, character divination, or Chinese character divination.
- The user has a character to record, wants cultural learning, or wants low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `cezi_request_guard`.
3. If blocked, pause cezi consultation and reframe to safety, professional support, privacy, anti-labeling, grounding, budget/risk support, or low-risk planning.
4. If allowed, run `cezi_character_recorder`.
5. Run `cezi_symbol_lookup` for known components, structures, or form features.
6. Run `cezi_interpretation_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/cezi_request_guard.py`
- `agent-tools/scripts/cezi_character_recorder.py`
- `agent-tools/scripts/cezi_symbol_lookup.py`
- `agent-tools/scripts/cezi_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: character features are symbolic prompts, not facts, spirit proof, personality labels, or predictions.
- Character summary: question, character, source, components, visible features, user association, focus, and missing fields.
- Symbol layer: component-by-component and structure-by-structure prompts with cautious combination notes.
- Reality layer: evidence checks, communication, practical next step, anti-labeling stop conditions, and dependency stop conditions.

## Hard Stops

- Lifespan, illness, personality ranking, family-harm labels, minor labeling, or destiny hierarchy.
- Spirit possession, curses, exorcism confirmation, ancestor/spirit messages, or supernatural proof.
- Gambling, investment, loans, lottery, medical, legal, safety, or mental-health replacement.
- Fate certainty, repeated character readings until satisfied, or treating the character as a command.
- Third-party mind reading, privacy invasion, coercion, revenge, or forced reunion.

## References

- `知识库/SOP/34-测字拆字象征咨询.md`
- `知识库/流派/测字与拆字.md`
