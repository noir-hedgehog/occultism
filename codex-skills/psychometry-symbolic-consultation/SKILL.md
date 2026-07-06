---
name: psychometry-symbolic-consultation
description: Use when the user asks about 物品感应, 触物占卜, 物件能量, old object energy, jewelry/object readings, psychometry, or object reading as symbolic reflection. Blocks missing-person/crime use, unauthorized objects, third-party privacy invasion, spirit fact claims, professional replacement, medical/safety claims, financial/legal use, authenticity/ownership claims, paid cleansing pressure, and repeated dependency.
---

# Psychometry Symbolic Consultation

## Use When

- The user asks about 物品感应、触物占卜、物件能量、旧物能量、首饰能量、遗物能量, psychometry, or object reading.
- The user wants cultural learning, authorized object journaling, memory reflection, symbolic writing, or low-risk object-based reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `psychometry_request_guard`.
3. If blocked, pause psychometry consultation and reframe to consent, privacy, real-world evidence, safety, professional support, or emergency/legal channels.
4. If allowed, run `psychometry_object_recorder`.
5. Run `psychometry_symbol_lookup` for known object motifs or source types.
6. Run `psychometry_reflection_planner`.
7. Draft with symbolic object-reflection language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/psychometry_request_guard.py`
- `agent-tools/scripts/psychometry_object_recorder.py`
- `agent-tools/scripts/psychometry_symbol_lookup.py`
- `agent-tools/scripts/psychometry_reflection_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: object impressions are symbolic prompts, not facts, identification, ownership, authenticity, spirit proof, or professional advice.
- Context summary: object type, source, ownership/consent, visible features, impressions, emotions, reality anchor, and focus.
- Symbol layer: object/source prompts with cautious limits.
- Reality layer: consent, privacy, evidence, professional鉴定/安全检测/法律 or support limits.
- Action layer: low-cost, reversible, non-harmful cleaning, journaling, storage, return, donation, communication, memorial, or evidence-checking steps.

## Hard Stops

- Missing-person, crime, location, remains, perpetrator, or safety-evidence requests.
- Unauthorized objects, stolen/secretly obtained items, third-party privacy, partner/ex true-thought checks, coercion, or surveillance.
- Spirit possession, curse, ghost, deceased-person facts, exorcism, object history/owner/authenticity claims, medical/safety/legal/financial replacement, paid cleansing/opening pressure, or repeated dependency.

## References

- `知识库/SOP/41-物品感应触物占卜象征咨询.md`
- `知识库/流派/物品感应与触物占卜.md`
