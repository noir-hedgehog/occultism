---
name: candle-symbolic-consultation
description: Use when the user asks about 蜡烛占卜, 蜡泪占卜, 火焰占卜, 烛火占卜, 蜡烛火焰, 蜡泪, 烛泪, candle reading, ceromancy, or candle wax reading. Blocks active fire instructions, dangerous rituals, professional replacement, fate certainty, spirit fear claims, third-party mind reading, coercion, gambling, investment, and repeated dependency.
---

# Candle Symbolic Consultation

## Use When

- The user asks about 蜡烛占卜, 蜡泪占卜, 火焰占卜, 烛火占卜, candle reading, ceromancy, or candle wax reading.
- The user has an already-safe observation to record, wants cultural learning, or wants low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `candle_request_guard`.
3. If blocked, pause candle consultation and reframe to fire safety, professional support, privacy, budget/risk support, grounding, or no-fire alternatives.
4. If allowed, run `candle_observation_recorder`.
5. Run `candle_symbol_lookup` for known flame, wax, or smoke observations.
6. Run `candle_interpretation_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/candle_request_guard.py`
- `agent-tools/scripts/candle_observation_recorder.py`
- `agent-tools/scripts/candle_symbol_lookup.py`
- `agent-tools/scripts/candle_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: only already-safe or no-fire observations are handled; no ignition or burning instructions.
- Observation summary: question, source, safety state, flame/wax/smoke notes, focus, and missing fields.
- Symbol layer: observation-by-observation prompts and a cautious combination summary.
- Reality layer: fire safety checks, evidence checks, communication, practical next step, and stop conditions.

## Hard Stops

- Active fire instructions, unattended flame, enclosed combustion, burning paper/talismans, blood, alcohol/fuel, or dangerous ritual steps.
- Medical, legal, safety, mental-health, gambling, investment, loans, or lottery replacement.
- Fate certainty, exorcism proof, spirit fear confirmation, repeated lighting until satisfied, or treating observations as commands.
- Third-party mind reading, privacy invasion, coercion, revenge, curse, or forced reunion.

## References

- `知识库/SOP/30-蜡烛火焰蜡泪象征咨询.md`
- `知识库/流派/蜡烛火焰与蜡泪.md`
