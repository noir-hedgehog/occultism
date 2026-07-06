---
name: western-geomancy-symbolic-consultation
description: Use when the user asks about 西洋土占, 盾形占, 盾盘, 土占盘, geomancy, Western geomancy, shield chart, geomantic figure, mother figures, witnesses, judge, or low-risk symbolic shield-chart reflection. Blocks professional replacement, gambling/investment, fate certainty, spirit fear, curse/exorcism confirmation, third-party mind reading, coercion, and repeated dependency.
---

# Western Geomancy Symbolic Consultation

## Use When

- The user asks about 西洋土占、盾形占、盾盘、土占盘、geomancy、Western geomancy、shield chart, geomantic figure, witnesses, judge, or the 16 common geomantic figures.
- The user has a shield chart to record, wants cultural learning, or wants low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `western_geomancy_request_guard`.
3. If blocked, pause Western geomancy consultation and reframe to safety, professional support, privacy, budget/risk support, grounding, or low-risk planning.
4. If allowed, run `western_geomancy_chart_recorder`.
5. Run `western_geomancy_figure_lookup` for figures and chart positions.
6. Run `western_geomancy_interpretation_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/western_geomancy_request_guard.py`
- `agent-tools/scripts/western_geomancy_chart_recorder.py`
- `agent-tools/scripts/western_geomancy_figure_lookup.py`
- `agent-tools/scripts/western_geomancy_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: Western geomancy figures are symbolic prompts, not facts, commands, spirit proof, or predictions.
- Chart summary: question, chart source, generation method, mothers, daughters, nieces, witnesses, judge, focus, and missing fields.
- Symbol layer: figure-by-figure prompts with cautious combination notes.
- Reality layer: evidence checks, communication, practical next step, stop conditions, and dependency guardrails.

## Hard Stops

- Medical, legal, financial, safety, mental-health, emergency, or professional replacement.
- Gambling, investment, loans, lottery, or high-risk money decisions.
- Fate certainty, repeated charting until satisfied, or treating the judge as a command.
- Spirit possession, curses, exorcism confirmation, or supernatural proof.
- Third-party mind reading, privacy invasion, coercion, revenge, or forced reunion.

## References

- `知识库/SOP/56-西洋土占盾形盘象征咨询.md`
- `知识库/流派/西洋土占与盾形盘.md`
