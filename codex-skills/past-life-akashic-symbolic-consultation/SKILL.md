---
name: past-life-akashic-symbolic-consultation
description: Use when the user asks about 前世, 前生, 累世, 宿世, 阿卡西记录, 阿卡莎, 灵魂契约, 灵魂课题, 业力关系, 灵魂伴侣, past life, Akashic records, or soul contracts as symbolic narrative reflection. Blocks hypnosis, recovered-memory claims, trauma confirmation, medical or mental-health replacement, fatalism, third-party privacy invasion, relationship coercion, financial/legal use, expensive session pressure, and repeated dependency.
---

# Past Life Akashic Symbolic Consultation

## Use When

- The user asks about 前世、前生、累世、宿世、阿卡西、阿卡莎、灵魂契约、灵魂课题、业力关系、灵魂伴侣、past life、Akashic records, or soul contracts.
- The user wants cultural learning, dream/meditation narrative records, or low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `past_life_request_guard`.
3. If blocked, pause past-life/Akashic consultation and reframe to reality evidence, trauma-informed support, medical/mental-health support, safety, privacy, budget, relationship-boundary, or grounding support.
4. If allowed, run `past_life_narrative_recorder`.
5. Run `past_life_symbol_lookup` for known scenes, roles, symbols, or motifs.
6. Run `past_life_reflection_planner`.
7. Draft with symbolic narrative and present-life reflection language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/past_life_request_guard.py`
- `agent-tools/scripts/past_life_narrative_recorder.py`
- `agent-tools/scripts/past_life_symbol_lookup.py`
- `agent-tools/scripts/past_life_reflection_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: past-life/Akashic content is symbolic narrative, not fact, recovered memory, trauma proof, fate proof, or professional advice.
- Context summary: source context, scenes, roles, symbols, emotions, present-life anchor, and consent/privacy notes.
- Symbol layer: motifs and themes with cautious combination notes.
- Reality layer: current boundaries, care needs, relationship choices, privacy, budget, and professional-support limits.
- Action layer: low-cost, reversible, non-harmful journaling, grounding, or communication steps.

## Hard Stops

- Hypnosis, past-life regression guidance, recovered-memory claims, sealed-memory claims, trauma confirmation, abuse confirmation, or identifying a perpetrator.
- Medical treatment, diagnosis, medication replacement, trauma therapy replacement, severe insomnia, panic, hallucinations, or crisis claims.
- Fatalism, karmic debt coercion, soul rank, guilt labels, irreversible identity claims, or fate certainty.
- Third-party past-life reading, soul-contract reading, mind reading, privacy invasion, coercion, forced reunion, revenge, or cutting off a third party.
- Gambling, investment, loans, lottery, legal outcomes, wealth guarantees, relationship guarantees, expensive session pressure, or repeated dependency.

## References

- `知识库/SOP/38-前世阿卡西灵魂课题象征咨询.md`
- `知识库/流派/前世阿卡西与灵魂课题.md`
