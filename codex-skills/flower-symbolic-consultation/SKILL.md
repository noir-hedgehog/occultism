---
name: flower-symbolic-consultation
description: Use when the user asks about 花语, 花占, 花卜, 花签, 花牌, 植物象征, 送花, 花束, flower language, floriography, or symbolic flower/plant consultation. Blocks professional replacement, medical healing, allergy/toxicity/pet-safety judgment, gambling/investment, fate certainty, spirit fear, exorcism confirmation, third-party mind reading, coercion, expensive purchase pressure, and repeated dependency.
---

# Flower Symbolic Consultation

## Use When

- The user asks about 花语, 花占, 花卜, 花签, 花牌, 植物象征, 送花, 花束, flower language, floriography, or flower divination.
- The user has flowers or plants to record, wants cultural learning, or wants low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `flower_request_guard`.
3. If blocked, pause flower consultation and reframe to safety, professional support, allergy/toxicity/pet-safety resources, privacy, budget support, or low-risk planning.
4. If allowed, run `flower_item_recorder`.
5. Run `flower_symbol_lookup` for known flowers, plants, or colors.
6. Run `flower_interpretation_planner`.
7. Draft with cultural, symbolic, and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/flower_request_guard.py`
- `agent-tools/scripts/flower_item_recorder.py`
- `agent-tools/scripts/flower_symbol_lookup.py`
- `agent-tools/scripts/flower_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: flowers are cultural/symbolic prompts, not facts, healing tools, safety judgments, or predictions.
- Context summary: intention, flowers, colors, scene, recipient, source, budget, and safety constraints.
- Symbol layer: flower-by-flower and color-by-color prompts with cautious combination notes.
- Reality layer: allergy, pet, child, scent, venue, budget, consent, and communication constraints first.
- Action layer: low-cost, reversible, non-harmful expression or reflection steps.

## Hard Stops

- Medical treatment, medication replacement, pregnancy, surgery, severe insomnia, anxiety, depression, or crisis claims.
- Allergy, toxicity, pet safety, ingestion, herbal medicine, or poison-identification requests.
- Gambling, investment, loans, lottery, wealth guarantees, romance guarantees, or fate certainty.
- Spirit possession, curses, exorcism confirmation, disaster-blocking proof, or supernatural proof.
- Third-party mind reading, privacy invasion, coercion, revenge, forced reunion, expensive purchase pressure, or repeated dependency.

## References

- `知识库/SOP/35-花语植物象征咨询.md`
- `知识库/流派/花语与植物象征.md`
