---
name: incense-symbolic-consultation
description: Use when the user asks about 香火占卜, 香灰占卜, 看香, 香谱, 香灰, 香烟形状, incense reading, incense ash reading, or smoke reading. Blocks active burning instructions, dangerous rituals, ash ingestion, professional replacement, fate certainty, spirit fear claims, third-party mind reading, coercion, gambling, investment, expensive purchase pressure, and repeated dependency.
---

# Incense Symbolic Consultation

## Use When

- The user asks about 香火占卜, 香灰占卜, 看香, 香谱, 烟形观察, incense reading, incense ash reading, or smoke reading.
- The user has an already-safe observation to record, wants cultural learning, or wants low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `incense_request_guard`.
3. If blocked, pause incense consultation and reframe to fire/smoke safety, professional support, privacy, budget/risk support, grounding, or no-smoke alternatives.
4. If allowed, run `incense_observation_recorder`.
5. Run `incense_symbol_lookup` for known ash, smoke, or ember observations.
6. Run `incense_interpretation_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/incense_request_guard.py`
- `agent-tools/scripts/incense_observation_recorder.py`
- `agent-tools/scripts/incense_symbol_lookup.py`
- `agent-tools/scripts/incense_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: only already-safe, photo, or no-smoke observations are handled; no ignition or burning instructions.
- Observation summary: question, source, safety state, ash/smoke/ember notes, focus, and missing fields.
- Symbol layer: observation-by-observation prompts and a cautious combination summary.
- Reality layer: fire and ventilation checks, evidence checks, communication, practical next step, and stop conditions.

## Hard Stops

- Active burning instructions, unattended fire, enclosed combustion, burning paper/talismans, ash ingestion, blood, alcohol/fuel, or dangerous ritual steps.
- Medical, legal, safety, mental-health, gambling, investment, loans, or lottery replacement.
- Fate certainty, exorcism proof, deity instruction, spirit fear confirmation, repeated lighting until satisfied, or treating observations as commands.
- Third-party mind reading, privacy invasion, coercion, revenge, curse, forced reunion, or expensive purchase pressure.

## References

- `知识库/SOP/31-香火香灰烟形象征咨询.md`
- `知识库/流派/香火香灰与烟形.md`
