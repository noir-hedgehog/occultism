---
name: lost-object-symbolic-consultation
description: Use when the user asks about 失物, 寻物, 找东西, 遗失物品, lost object, missing item, or divination-style object search as symbolic memory reconstruction, route review, area checklist, contact-channel planning, and bounded search. Blocks missing people, emergency missing pets, crime/evidence accusations, professional-channel replacement, guaranteed location claims, privacy/stalking, and repeated dependency.
---

# Lost Object Symbolic Consultation

## Use When

- The user asks about 失物、寻物、找东西、遗失物品、东西不见了, lost object, or missing item.
- The user wants symbolic memory reconstruction, route review, area checklist, contact-channel planning, or bounded search.
- The user frames a search as tarot, pendulum, hexagram, direction, omen, or intuition, but the target is a normal object they have a right to look for.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `lost_object_request_guard`.
3. If blocked, pause lost-object interpretation and reframe to real-world search, safety support, qualified channels, or privacy-respecting boundaries.
4. If allowed, run `lost_object_context_recorder`.
5. Run `lost_object_symbol_lookup`.
6. Run `lost_object_search_planner`.
7. Draft with memory, route, container, area, contact-channel, and bounded-search language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/lost_object_request_guard.py`
- `agent-tools/scripts/lost_object_context_recorder.py`
- `agent-tools/scripts/lost_object_symbol_lookup.py`
- `agent-tools/scripts/lost_object_search_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: lost-object symbolism is a search-planning aid, not a promise of location or recovery.
- Context summary: item description, last seen moment, route context, possible areas, checked areas, contact channels, practical actions, review time, and stop condition.
- Search layer: last-seen timeline, route retrace, container/area checklist, contact channels, and excluded zones.
- Action layer: 3-7 bounded practical steps ordered by low cost and urgency.
- Review layer: review time and stopping condition to avoid repeated divination loops.

## Hard Stops

- Missing person, child/elder disappearance, emergency missing pet, crime accusation/evidence, stalking/privacy location, professional-channel replacement, guaranteed location/recovery, or repeated dependency.

## References

- `知识库/SOP/54-失物寻物象征咨询.md`
- `知识库/流派/失物寻物象征.md`
