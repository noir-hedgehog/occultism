---
name: sky-omen-symbolic-consultation
description: Use when the user asks about 天象征兆, 云占, 看云, 云形, 彩虹征兆, 日晕, 月晕, 雷电征兆, weather omens, sky omens, cloud omens, or nephomancy as symbolic reflection. Blocks disaster prediction, weather-safety replacement, dangerous exposure, professional replacement, financial/legal use, third-party privacy invasion, spirit fact claims, and repeated dependency.
---

# Sky Omen Symbolic Consultation

## Use When

- The user asks about 天象征兆、云占、看云、云形、彩虹、日晕、月晕、雷电、风雨预兆, sky omens, cloud omens, weather omens, or nephomancy.
- The user wants cultural learning, observation journaling, or low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `sky_omen_request_guard`.
3. If blocked, pause sky-omen consultation and reframe to official weather/safety guidance, professional support, privacy, or grounding.
4. If allowed, run `sky_omen_observation_recorder`.
5. Run `sky_omen_symbol_lookup`.
6. Run `sky_omen_reflection_planner`.
7. Draft with symbolic sky-observation language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/sky_omen_request_guard.py`
- `agent-tools/scripts/sky_omen_observation_recorder.py`
- `agent-tools/scripts/sky_omen_symbol_lookup.py`
- `agent-tools/scripts/sky_omen_reflection_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: sky omens are symbolic observations, not disaster predictions, weather forecasts, divine commands, or professional advice.
- Context summary: phenomenon, shape, color, location/time, weather context, emotion, reality anchor, and focus.
- Symbol layer: sky motif prompts with cautious limits.
- Reality layer: official weather/safety, professional-support, privacy and stopping-condition limits.
- Action layer: low-risk observation, journaling, weather check, rest, communication, or planning step.

## Hard Stops

- Disaster, death, earthquake, apocalypse, divine punishment, weather-warning replacement, dangerous weather exposure, medical/legal/financial replacement, third-party mind reading, spirit fact claims, or repeated dependency.

## References

- `知识库/SOP/43-天象云形征兆象征咨询.md`
- `知识库/流派/天象云形与天气征兆.md`
