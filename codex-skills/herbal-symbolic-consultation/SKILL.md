---
name: herbal-symbolic-consultation
description: Use when the user asks about 草本, 香草, 草药, 药草, 植物魔法, 绿巫, herbal symbolism, herb magic, green witchcraft, herbal bundles, sachets, or plant-based low-risk reminder objects. Blocks medical/mental-health claims, ingestion, topical use, pregnancy/baby/pet/allergy scenarios, foraging or poisoning risk, fire/smoke/mold misuse, professional replacement, exorcism claims, outcome guarantees, love spells, curses, third-party coercion, purchase pressure, and repeated dependency.
---

# Herbal Symbolic Consultation

## Use When

- The user asks about 草本、香草、草药、药草、植物魔法、绿巫、herbal symbolism、herb magic、green witchcraft、herbal bundles, or plant-based reminder objects.
- The user wants cultural learning, to record an existing herb/plant object, or to make a low-risk symbolic reminder.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `herbal_request_guard`.
3. If blocked, pause herbal consultation and reframe to safety, professional support, non-contact alternatives, consent, low-cost options, or stopping conditions.
4. If allowed, run `herbal_context_recorder`.
5. Run `herbal_symbol_lookup` for plant items, objects, methods, containers, or safety layers.
6. Run `herbal_practice_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/herbal_request_guard.py`
- `agent-tools/scripts/herbal_context_recorder.py`
- `agent-tools/scripts/herbal_symbol_lookup.py`
- `agent-tools/scripts/herbal_practice_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: herbs and plant magic symbols are cultural prompts and reminder objects, not treatment, diagnosis, exorcism, purification guarantees, luck guarantees, love spells, curses, or professional advice.
- Context summary: plant items, source, use mode, container/form, space, duration, safety context, constraints, and missing fields.
- Symbol layer: plant/object/method prompts with cautious combination notes.
- Reality layer: non-contact, no-fire, no-ingestion, no-topical option; budget/no-purchase option; stop conditions; professional-support boundaries.

## Hard Stops

- Medical, mental-health, veterinary, pregnancy, allergy, food-safety, fire/smoke, legal, emergency, or professional replacement.
- Ingestion, herbal tea instructions, swallowing, topical use, bath use, wound/eye/ear/private-area use, or specific safety advice for pregnant people, babies, children, pets, allergies, asthma, or seizures.
- Foraging, unknown-plant identification for use, poisonous plants, mushrooms, or edible/safe-to-use determinations.
- Exorcism, spirit-clearing, purification guarantees, outcome guarantees, love spells, curses, third-party coercion, or mind reading.
- Expensive kits, MLM or agency pressure, course pressure, hoarding, or repeated ritual use until emotionally satisfied.

## References

- `知识库/SOP/60-草本香草植物魔法象征咨询.md`
- `知识库/流派/草本香草与植物魔法象征.md`
