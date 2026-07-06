---
name: dowsing-symbolic-consultation
description: Use when the user asks about 占杖, 寻水杖, 探测棒, 探测杆, dowsing rods, divining rods, L-rods, map dowsing, or radiesthesia as low-risk symbolic route or space reflection. Blocks utility locating, excavation, well drilling, resource guarantees, medical/geopathic claims, professional replacement, property/legal decisions, trespass/privacy violations, exorcism claims, financial misuse, purchase pressure, and repeated dependency.
---

# Dowsing Symbolic Consultation

## Use When

- The user asks about 占杖、寻水杖、探测棒、探测杆、dowsing rods、divining rods、L-rods、map dowsing, or radiesthesia.
- The user wants cultural learning, to record an existing dowsing observation, or to make a low-risk symbolic route/space reflection in an authorized space.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `dowsing_request_guard`.
3. If blocked, pause dowsing consultation and reframe to safety, professional support, consent/authorization, reality checks, low-cost observation, or stopping conditions.
4. If allowed, run `dowsing_context_recorder`.
5. Run `dowsing_symbol_lookup` for movement notes, map marks, spaces, or safety layers.
6. Run `dowsing_practice_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/dowsing_request_guard.py`
- `agent-tools/scripts/dowsing_context_recorder.py`
- `agent-tools/scripts/dowsing_symbol_lookup.py`
- `agent-tools/scripts/dowsing_practice_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: dowsing rods are cultural prompts and low-risk observation aids, not utility locating, water finding, diagnosis, spirit detection, missing-person locating, or professional advice.
- Context summary: tool type, observation target, space/map, movement notes, authorization context, safety context, constraints, duration, and missing fields.
- Symbol layer: movement/space/method prompts with cautious combination notes.
- Reality layer: authorized space only, no digging, no trespass, no professional replacement, no purchase pressure, stop conditions, and reality-check list.

## Hard Stops

- Underground utility locating, excavation, drilling, well digging, water/resource guarantees, medical or geopathic claims, property/legal decisions, trespass, tracking or locating people, exorcism, investment/gambling, expensive tools/courses, or repeated dependency.
- Any request that would replace engineers, licensed locators, doctors, lawyers, emergency services, police, property managers, or other qualified support.

## References

- `知识库/SOP/62-占杖寻水杖探测棒象征咨询.md`
- `知识库/流派/占杖寻水杖与探测棒象征.md`
