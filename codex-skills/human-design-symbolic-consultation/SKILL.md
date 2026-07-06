---
name: human-design-symbolic-consultation
description: Use when the user asks about 人类图, Human Design, bodygraph, 类型, 策略, 内在权威, 人生角色, 中心, 通道, 闸门, manifestor, generator, projector, reflector, or low-risk symbolic chart reflection. Blocks birth-data privacy misuse, professional replacement, diagnosis, financial/career guarantees, deterministic identity labels, relationship discrimination, third-party mind reading, coercion, paid pressure, and repeated dependency.
---

# Human Design Symbolic Consultation

## Use When

- The user asks about 人类图、Human Design、bodygraph、类型、策略、内在权威、人生角色、中心、通道、闸门, or common type names such as manifestor, generator, projector, reflector.
- The user has an existing Human Design chart and wants cultural learning, record cleanup, or low-risk symbolic reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `human_design_request_guard`.
3. If blocked, pause Human Design consultation and reframe to privacy, professional support, consent, reality checks, budget boundaries, or low-risk planning.
4. If allowed, run `human_design_chart_recorder`.
5. Run `human_design_symbol_lookup` for type, authority, profile, centers, channels, or gates.
6. Run `human_design_interpretation_planner`.
7. Draft with symbolic and possibility language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/human_design_request_guard.py`
- `agent-tools/scripts/human_design_chart_recorder.py`
- `agent-tools/scripts/human_design_symbol_lookup.py`
- `agent-tools/scripts/human_design_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: Human Design symbols are reflective prompts, not facts, diagnoses, commands, destiny, relationship filters, or career/financial guarantees.
- Context summary: question, chart source, data scope, type, strategy, authority, profile, centers, channels, gates, constraints, and missing fields.
- Symbol layer: type/authority/profile/center/channel/gate prompts with cautious combination notes.
- Reality layer: evidence checks, privacy consent, communication boundaries, budget/time limits, low-risk next step, stop conditions, and dependency guardrails.

## Hard Stops

- Medical, legal, financial, safety, mental-health, emergency, career, or professional replacement.
- Requesting, inferring, or using third-party birth data without consent.
- Deterministic identity labels, relationship screening, discrimination labels, or treating chart type as destiny.
- Investment, gambling, loans, resignation, hiring/firing, promotion, or career outcome guarantees.
- Third-party mind reading, coercion, revenge, forced reunion, or controlling another person.
- Paid-course pressure, high-price readings, certification pressure, or repeated chart checking until satisfied.

## References

- `知识库/SOP/58-人类图象征咨询.md`
- `知识库/流派/人类图.md`
