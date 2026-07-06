---
name: deity-ancestor-symbolic-consultation
description: Use when the user asks about 神明, 祖先, 祖灵, 供奉, 供桌, 神台, 祭拜, 祭祖, 供品, 拜神, 拜拜, 许愿还愿, altar, offering, ancestor veneration, deity prayer, or vow-return practices as cultural learning, memorial reflection, gratitude expression, household-boundary planning, and low-risk safety planning. Blocks deity/ancestor command claims, fear or punishment framing, dangerous rituals, professional/safety replacement, third-party blame/privacy, coercion, forced worship, expensive ritual pressure, and repeated dependency.
---

# Deity Ancestor Symbolic Consultation

## Use When

- The user asks about 神明、祖先、祖灵、供奉、供桌、神台、祭拜、祭祖、供品、拜神、拜拜、许愿还愿, altar, offering, ancestor veneration, deity prayer, or vow-return practices.
- The user wants cultural learning, memorial reflection, gratitude expression, household-boundary planning, or low-risk safety planning.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `deity_ancestor_request_guard`.
3. If blocked, pause deity/ancestor interpretation and reframe to cultural learning, memorial care, household boundaries, reality safety, trusted support, emergency help, or professional support.
4. If allowed, run `deity_ancestor_context_recorder`.
5. Run `deity_ancestor_symbol_lookup`.
6. Run `deity_ancestor_reflection_planner`.
7. Draft with cultural, memorial, gratitude, and grounded-reflection language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/deity_ancestor_request_guard.py`
- `agent-tools/scripts/deity_ancestor_context_recorder.py`
- `agent-tools/scripts/deity_ancestor_symbol_lookup.py`
- `agent-tools/scripts/deity_ancestor_reflection_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: deity/ancestor/offering language is cultural and symbolic, not proof of commands, punishment, spirit facts, disasters, or third-party intent.
- Context summary: tradition context, focus entity, occasion, intention, existing items, offering or memorial actions, household boundaries, safety context, review time, and stop condition.
- Symbol layer: altar/offering/memorial motifs with cautious prompts.
- Action layer: low-risk memorial actions, cleaning, gratitude statement, household communication, and fire/food/child/pet/budget safety.
- Review layer: review time and stopping condition to avoid repeated checking, vow anxiety, or fear loops.

## Hard Stops

- Deity or ancestor command claims, fear or punishment framing, dangerous ritual, ingestion, professional or safety replacement, coercion, third-party blame/privacy, forced worship, expensive ritual pressure, or repeated dependency.

## References

- `知识库/SOP/49-神明祖先供奉祭拜象征咨询.md`
- `知识库/流派/神明祖先供奉与祭拜.md`
