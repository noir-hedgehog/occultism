---
name: sigil-symbolic-consultation
description: Use when the user asks about sigils, 符号印记, 印记魔法, 魔法印记, 意图符号, 愿望符号, seal magic, magical seals, 魔法阵, symbol circles, or low-risk personal symbolic marks. Blocks blood, cutting, body harm, tattoo/permanent marks, burning, summoning, exorcism, curses, coercion, outcome guarantees, professional replacement, financial/legal misuse, purchase pressure, and repeated dependency.
---

# Sigil Symbolic Consultation

## Use When

- The user asks about sigils、符号印记、印记魔法、魔法印记、意图符号、seal magic、magical seals、魔法阵, or symbol circles.
- The user wants cultural learning, to record an existing symbol, or to make a low-risk removable symbolic reminder.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `sigil_request_guard`.
3. If blocked, pause sigil consultation and reframe to safety, professional support, consent, low-cost removable alternatives, or stopping conditions.
4. If allowed, run `sigil_context_recorder`.
5. Run `sigil_symbol_lookup` for shapes, motifs, methods, or safety layers.
6. Run `sigil_practice_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/sigil_request_guard.py`
- `agent-tools/scripts/sigil_context_recorder.py`
- `agent-tools/scripts/sigil_symbol_lookup.py`
- `agent-tools/scripts/sigil_practice_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: sigils and symbolic marks are cultural prompts and reminder objects, not summoning, exorcism, curses, manifestation guarantees, relationship control, or professional advice.
- Context summary: intention text, elements, source, medium, activation mode, display location, duration, safety context, constraints, and missing fields.
- Symbol layer: shape/motif/method prompts with cautious combination notes.
- Reality layer: paper or digital draft, removable, no-fire, no-body-harm, no-permanent-mark option; budget/no-purchase option; stop conditions.

## Hard Stops

- Blood, cutting, skin carving, self-harm, body marking, tattoo/permanent marks, burning, dangerous destruction, summoning, exorcism, curses, coercion, or spirit commands.
- Medical, mental-health, legal, financial, safety, emergency, or professional replacement.
- Third-party manipulation, love spells, revenge, binding someone, illegal evasion, gambling, investment guarantees, outcome guarantees, purchase pressure, or repeated dependency.

## References

- `知识库/SOP/61-Sigil符号印记魔法阵象征咨询.md`
- `知识库/流派/Sigil符号印记与魔法阵象征.md`
