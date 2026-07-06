---
name: sleep-paralysis-symbolic-consultation
description: Use when the user asks about 鬼压床, 压床, 睡眠瘫痪, 睡瘫, 梦魇, 梦魔, 夜惊, 半夜惊醒, 床边有人, sleep paralysis, night terror, nightmare-spirit fear, or night-fear experiences as sleep-experience logging, grounding, room-safety checking, and symbolic reflection. Blocks medical or breathing danger, severe sleep impairment, hallucination/reality confusion, self-harm or violence, dangerous rituals, professional replacement, spirit-fact claims, expensive ritual pressure, and repeated dependency.
---

# Sleep Paralysis Symbolic Consultation

## Use When

- The user asks about 鬼压床、压床、睡眠瘫痪、睡瘫、梦魇、梦魔、夜惊、半夜惊醒、床边有人, sleep paralysis, night terror, or nightmare-spirit fear.
- The user wants sleep-experience logging, grounding, room-safety checking, or low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `sleep_paralysis_request_guard`.
3. If blocked, pause symbolic interpretation and reframe to sleep safety, trusted support, emergency help, medical support, or mental-health support.
4. If allowed, run `sleep_paralysis_context_recorder`.
5. Run `sleep_paralysis_symbol_lookup`.
6. Run `sleep_paralysis_reflection_planner`.
7. Draft with sleep-experience, grounding, reality-safety, and symbolic-reflection language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/sleep_paralysis_request_guard.py`
- `agent-tools/scripts/sleep_paralysis_context_recorder.py`
- `agent-tools/scripts/sleep_paralysis_symbol_lookup.py`
- `agent-tools/scripts/sleep_paralysis_reflection_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: night-fear language is sleep-experience and symbolic reflection, not proof of spirits, possession, curses, disasters, or third-party influence.
- Context summary: episode pattern, wake state, body sensations, perceived images, room context, recent stressors, sleep context, grounding actions, daytime impact, review time, and stop condition.
- Symbol layer: sleep-paralysis/night-fear motifs with cautious prompts.
- Action layer: grounding, room-safety check, sleep log, trusted-person contact, and low-risk bedtime routine.
- Review layer: review time and stopping condition to avoid repeated checking, ritual loops, or fear escalation.

## Hard Stops

- Breathing difficulty, chest pain, seizure, injury, severe sleep impairment, hallucinations, reality confusion, self-harm, violence, dangerous ritual, ingestion, sleep deprivation, professional replacement, spirit-fact confirmation, expensive ritual pressure, or repeated dependency.

## References

- `知识库/SOP/50-鬼压床梦魇睡前灵异恐惧象征咨询.md`
- `知识库/流派/鬼压床梦魇与睡前灵异恐惧.md`
