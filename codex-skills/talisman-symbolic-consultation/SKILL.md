---
name: talisman-symbolic-consultation
description: Use when the user asks about 护符, 符箓, 符咒, 灵符, 平安符, 红绳, 香囊, amulet, talisman, charm, or low-risk talisman cultural and symbolic consultation. Blocks dangerous rituals, talisman water, curses, coercion, spirit-fear proof, professional replacement, expensive purchase pressure, and dependency.
---

# Talisman Symbolic Consultation

## Use When

- The user asks about 护符, 符箓, 符咒, 灵符, 平安符, 红绳, 香囊, amulet, talisman, or charm.
- The user wants cultural learning, source recording, storage advice, or symbolic reminder use.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `talisman_request_guard`.
3. If blocked, pause talisman consultation and reframe to safety, professional support, budget support, or grounding.
4. If allowed, run `talisman_record_builder`.
5. Run `talisman_symbol_lookup` for known motifs.
6. Run `talisman_use_planner`.
7. Draft with cultural and symbolic language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/talisman_request_guard.py`
- `agent-tools/scripts/talisman_record_builder.py`
- `agent-tools/scripts/talisman_symbol_lookup.py`
- `agent-tools/scripts/talisman_use_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: talismans are cultural objects, symbolic reminders, or low-risk comfort objects.
- Source summary: source type, source label, visible symbols, use context, and budget/existing-item note.
- Symbol layer: known talisman motifs or explicit unknown/source-specific caveat.
- Reality layer: safe storage, respectful handling, low-risk action, and stop conditions.

## Hard Stops

- Burning talismans, talisman water, swallowing paper, blood rituals, sealed burning, or dangerous ritual steps.
- Medical, legal, safety, financial, or mental-health replacement.
- Curses, revenge, coercion, forced reunion, or third-party privacy.
- Spirit proof, curse confirmation, possession, disaster-blocking proof, or expensive purchase pressure.

## References

- `知识库/SOP/24-护符符箓象征咨询.md`
- `知识库/流派/护符符箓.md`
