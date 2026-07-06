---
name: scrying-symbolic-consultation
description: Use when the user asks about 水晶球占卜, 镜占, 黑镜占卜, 水占, 凝视占卜, 水晶球, 黑镜, 镜面凝视, 水面凝视, scrying, crystal ball reading, mirror scrying, or water scrying. Blocks long-staring or trance induction, professional replacement, fate certainty, spirit fear claims, third-party mind reading, coercion, gambling, investment, identity labels, and repeated dependency.
---

# Scrying Symbolic Consultation

## Use When

- The user asks about 水晶球占卜, 镜占, 黑镜占卜, 水占, 凝视占卜, scrying, crystal ball reading, mirror scrying, or water scrying.
- The user has a short, completed observation to record, wants cultural learning, or wants low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `scrying_request_guard`.
3. If blocked, pause scrying consultation and reframe to grounding, rest, professional support, privacy, risk support, or non-gazing alternatives.
4. If allowed, run `scrying_observation_recorder`.
5. Run `scrying_symbol_lookup` for known visual, surface, or feeling observations.
6. Run `scrying_interpretation_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/scrying_request_guard.py`
- `agent-tools/scripts/scrying_observation_recorder.py`
- `agent-tools/scripts/scrying_symbol_lookup.py`
- `agent-tools/scripts/scrying_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: only short, completed observations or cultural learning are handled; no long-gazing or trance instructions.
- Observation summary: question, source, safety state, medium, visual/surface/feeling notes, focus, and missing fields.
- Symbol layer: observation-by-observation prompts and a cautious combination summary.
- Reality layer: grounding checks, evidence checks, communication, practical next step, and stop conditions.

## Hard Stops

- Long staring, trance induction, sleep deprivation, hallucination seeking, or repeated gazing until satisfied.
- Medical, legal, safety, mental-health, gambling, investment, loans, or lottery replacement.
- Fate certainty, exorcism proof, spirit message, possession/curse confirmation, or treating visuals as commands.
- Third-party mind reading, privacy invasion, coercion, revenge, curse, forced reunion, identity labels, or appearance-based judgments.

## References

- `知识库/SOP/32-水晶球镜面水面凝视象征咨询.md`
- `知识库/流派/水晶球镜面与水面凝视.md`
