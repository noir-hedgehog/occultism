---
name: color-symbolic-consultation
description: Use when the user asks about 五行颜色, 开运色, 幸运色, lucky color, color symbolism, outfit color, desk color, room color, or low-risk symbolic color planning. Blocks fate certainty, wealth promises, professional replacement, appearance shaming, identity labels, expensive purchase pressure, and dependency.
---

# Color Symbolic Consultation

## Use When

- The user asks about 五行颜色, 开运色, 幸运色, lucky color, outfit color, room color, desk color, brand color, or color symbolism.
- The user wants cultural learning, low-risk outfit planning, workspace reminders, emotional anchors, or symbolic palette planning.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `color_request_guard`.
3. If blocked, pause color consultation and reframe to safety, professional support, budget support, body-neutral language, or grounding.
4. If allowed, run `color_profile_recorder`.
5. Run `color_symbol_lookup` for candidate colors or desired elements.
6. Run `color_palette_planner`.
7. Draft with cultural and symbolic language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/color_request_guard.py`
- `agent-tools/scripts/color_profile_recorder.py`
- `agent-tools/scripts/color_symbol_lookup.py`
- `agent-tools/scripts/color_palette_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: colors are cultural symbols, emotional anchors, scene language, or low-risk reminders.
- Context summary: scene, candidate colors, desired element, existing items, budget note, and practical constraints.
- Symbol layer: color, element, keywords, and prohibited uses.
- Reality layer: existing item first, low-cost adjustment, comfort, safety, budget, and situation fit.

## Hard Stops

- Fate certainty, wealth promises, disaster prevention, medical treatment, romance guarantee, or professional replacement.
- Appearance shaming, identity labels, body comments, skin-tone judgment, or social-value ranking.
- Expensive purchase pressure, mandatory wardrobe changes, paid color cures, or repeated dependency.

## References

- `知识库/SOP/26-五行颜色开运色象征咨询.md`
- `知识库/流派/五行颜色与开运色.md`
