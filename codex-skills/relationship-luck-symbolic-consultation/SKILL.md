---
name: relationship-luck-symbolic-consultation
description: Use when the user asks about 桃花, 姻缘, 人缘, 爱情运, 恋爱运, 旺桃花, 招桃花, 月老, 红线, 红绳, 粉晶, peach blossom luck, or romance luck as symbolic self-presentation, consent-aware communication, social action planning, boundary setting, and low-risk reminder-object use. Blocks stalking, harassment, coercive love spells, third-party mind reading, relationship crisis, professional replacement, guaranteed romance claims, expensive ritual pressure, and repeated dependency.
---

# Relationship Luck Symbolic Consultation

## Use When

- The user asks about 桃花、姻缘、人缘、爱情运、恋爱运、旺桃花、招桃花、月老、红线、红绳、粉晶, peach blossom luck, or romance luck.
- The user wants symbolic self-presentation, consent-aware communication, social action planning, boundary setting, or low-risk reminder-object use.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `relationship_luck_request_guard`.
3. If blocked, pause relationship-luck interpretation and reframe to consent, boundaries, safety support, qualified mental-health/legal/emergency support, or grounded self-care.
4. If allowed, run `relationship_luck_context_recorder`.
5. Run `relationship_luck_symbol_lookup`.
6. Run `relationship_luck_action_planner`.
7. Draft with symbolic romance, consent, communication-boundary, and grounded-action language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/relationship_luck_request_guard.py`
- `agent-tools/scripts/relationship_luck_context_recorder.py`
- `agent-tools/scripts/relationship_luck_symbol_lookup.py`
- `agent-tools/scripts/relationship_luck_action_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: relationship-luck language is symbolic action planning, not a promise of dating, reconciliation, marriage, affection, soulmate arrival, or third-party thoughts.
- Context summary: relationship focus, current context, consent scope, communication boundaries, existing symbols, practical actions, risk notes, review time, and stop condition.
- Symbol layer: peach-blossom and relationship motifs with cautious prompts.
- Action layer: self-presentation, consent-aware communication, social activity, boundary, and review actions.
- Review layer: review time and stopping condition to avoid repeated checking, message flooding, stalking, or coercive tactics.

## Hard Stops

- Stalking, harassment, doxxing, surveillance, coercive love spells, forced reconciliation, third-party mind reading, abuse or threats, self-harm/other-harm, professional replacement, guaranteed romance claims, expensive ritual pressure, or repeated dependency.

## References

- `知识库/SOP/52-桃花姻缘人缘象征咨询.md`
- `知识库/流派/桃花姻缘与人缘象征.md`
