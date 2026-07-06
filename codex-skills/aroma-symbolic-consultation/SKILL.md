---
name: aroma-symbolic-consultation
description: Use when the user asks about 芳香, 香薰, 精油, 香氛, 气味, 嗅觉, aromatherapy, essential oil, diffuser, scent symbolism, or low-risk scent-based reflection. Blocks medical/mental-health claims, ingestion, unsafe skin use, pregnancy/baby/pet/allergy scenarios, fire or diffuser safety misuse, professional replacement, exorcism claims, outcome guarantees, third-party coercion, purchase pressure, and repeated dependency.
---

# Aroma Symbolic Consultation

## Use When

- The user asks about 芳香、香薰、精油、香氛、气味、嗅觉、aromatherapy、essential oil、diffuser, or scent symbolism.
- The user wants cultural learning, to record an existing scent experience, or to make a low-risk environmental reminder.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `aroma_request_guard`.
3. If blocked, pause aroma consultation and reframe to safety, professional support, ventilation, consent, low-cost options, or stopping conditions.
4. If allowed, run `aroma_context_recorder`.
5. Run `aroma_symbol_lookup` for scent items, objects, methods, or safety layers.
6. Run `aroma_practice_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/aroma_request_guard.py`
- `agent-tools/scripts/aroma_context_recorder.py`
- `agent-tools/scripts/aroma_symbol_lookup.py`
- `agent-tools/scripts/aroma_practice_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: aroma and essential oil symbols are environmental prompts, not treatment, diagnosis, exorcism, purification guarantees, luck guarantees, or professional advice.
- Context summary: scent items, source, use mode, space, duration, ventilation, safety context, constraints, and missing fields.
- Symbol layer: scent/object/method prompts with cautious combination notes.
- Reality layer: ventilation, time box, no-contact option, budget/no-purchase option, stop conditions, and professional-support boundaries.

## Hard Stops

- Medical, mental-health, veterinary, pregnancy, allergy, fire-safety, legal, emergency, or professional replacement.
- Ingestion, mouth/eye/ear/wound use, undiluted skin use, or specific safety advice for pregnant people, babies, children, pets, allergies, asthma, or seizures.
- Exorcism, spirit-clearing, purification guarantees, outcome guarantees, relationship coercion, or third-party mind reading.
- Expensive kits, MLM or agency pressure, course pressure, hoarding, or repeated scent use until emotionally satisfied.

## References

- `知识库/SOP/59-芳香精油气味象征咨询.md`
- `知识库/流派/芳香精油与气味象征.md`
