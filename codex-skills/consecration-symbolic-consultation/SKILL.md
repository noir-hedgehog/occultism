---
name: consecration-symbolic-consultation
description: Use when the user asks about 开光, 加持, 净物, 净化物件, 净化水晶, 净化手串, 过香火, 祝福物件, consecration, blessing, or object cleansing as symbolic object-care, source-recording, cleaning, low-risk reminder-object use, and review planning. Blocks dangerous rituals, ingestion/body-harm, professional replacement, guaranteed efficacy claims, expensive ritual pressure, deity-command fear, fraud/coercion, and repeated dependency.
---

# Consecration Symbolic Consultation

## Use When

- The user asks about 开光、加持、净物、净化物件、净化水晶、净化手串、过香火、祝福物件, consecration, blessing, or object cleansing.
- The user wants symbolic object-care, source-recording, cleaning, low-risk reminder-object use, or review planning.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `consecration_request_guard`.
3. If blocked, pause consecration interpretation and reframe to low-risk object care, safety support, qualified professional support, or grounded action.
4. If allowed, run `consecration_context_recorder`.
5. Run `consecration_symbol_lookup`.
6. Run `consecration_care_planner`.
7. Draft with symbolic object-care, source-recording, cleaning, and grounded-action language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/consecration_request_guard.py`
- `agent-tools/scripts/consecration_context_recorder.py`
- `agent-tools/scripts/consecration_symbol_lookup.py`
- `agent-tools/scripts/consecration_care_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: consecration language is symbolic object care, not a promise of efficacy, protection, wealth, luck changes, deity support, or supernatural object effects.
- Context summary: object focus, source context, current use, existing items, safety boundaries, symbolic actions, risk notes, review time, and stop condition.
- Symbol layer: consecration and object-cleansing motifs with cautious prompts.
- Action layer: source-recording, cleaning, storage, intention-label, low-risk reminder, and review actions.
- Review layer: review time and stopping condition to avoid repeated cleansing, paid ritual loops, or impulse purchases.

## Hard Stops

- Dangerous rituals, ingestion, blood, blades, sealed burning, self-harm, professional replacement, guaranteed efficacy, deity-command fear, expensive ritual pressure, fraud/coercion, or repeated dependency.

## References

- `知识库/SOP/53-开光加持净物象征咨询.md`
- `知识库/流派/开光加持与净物象征.md`
