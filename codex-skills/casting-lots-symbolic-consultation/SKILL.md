---
name: casting-lots-symbolic-consultation
description: Use when the user asks about 骨占, 贝壳占卜, 石子占卜, 符物占卜, 小物占卜, 抛掷占卜, 撒骨, casting lots, charm casting, bone casting, shell divination, or symbolic object-casting consultation. Blocks professional replacement, gambling/investment, fate certainty, spirit fear, curse/exorcism confirmation, human remains, animal harm, blood sacrifice, third-party mind reading, coercion, and repeated dependency.
---

# Casting Lots Symbolic Consultation

## Use When

- The user asks about 骨占, 贝壳占卜, 石子占卜, 符物占卜, 小物占卜, 抛掷占卜, 撒骨, casting lots, charm casting, bone casting, or shell divination.
- The user has a cast layout to record, wants cultural learning, or wants low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `casting_lots_request_guard`.
3. If blocked, pause casting-lots consultation and reframe to safety, professional support, privacy, materials safety, grounding, budget/risk support, or low-risk planning.
4. If allowed, run `casting_lots_layout_recorder`.
5. Run `casting_lots_symbol_lookup` for known objects, zones, or relationships.
6. Run `casting_lots_interpretation_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/casting_lots_request_guard.py`
- `agent-tools/scripts/casting_lots_layout_recorder.py`
- `agent-tools/scripts/casting_lots_symbol_lookup.py`
- `agent-tools/scripts/casting_lots_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: cast objects are symbolic prompts, not facts, spirit proof, or predictions.
- Layout summary: question, system, casting surface, source, objects, zones, relationships, focus, and missing fields.
- Symbol layer: object-by-object and zone-by-zone prompts with cautious combination notes.
- Reality layer: evidence checks, communication, practical next step, materials-safety stop conditions, and dependency stop conditions.

## Hard Stops

- Human remains, animal harm, blood sacrifice, illegal materials, or unsafe materials.
- Spirit possession, curses, exorcism confirmation, ancestor/spirit messages, or supernatural proof.
- Gambling, investment, loans, lottery, medical, legal, safety, or mental-health replacement.
- Fate certainty, repeated casting until satisfied, or treating the layout as a command.
- Third-party mind reading, privacy invasion, coercion, revenge, or forced reunion.

## References

- `知识库/SOP/33-骨贝石子符物抛掷象征咨询.md`
- `知识库/流派/骨贝石子与符物抛掷.md`
