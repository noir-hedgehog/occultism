---
name: body-omen-symbolic-consultation
description: Use when the user asks about eye twitching, ear ringing, sneezing, ear heat, face heat, palm itching, muscle twitching, body omens, 身体征兆, 眼跳, 耳鸣, 喷嚏, 耳热, 脸热, 手心痒, 肉跳, and related folklore symbolism. Keep the work to low-risk cultural reflection and body-care journaling; block or reframe medical red flags, diagnosis/treatment replacement, medication changes, disaster claims, gambling or investment timing, third-party body labels, spirit fear, unsafe body tests, and repeated reassurance loops.
---

# Body Omen Symbolic Consultation

## Use When

- The user asks about eye twitching, ear ringing, sneezing, ear heat, face heat, palm itching, muscle twitching, 身体征兆、眼跳、耳鸣、喷嚏、耳热、脸热、手心痒 or 肉跳.
- The user wants cultural learning, to record a low-risk body omen, or to make a symbolic body-care reflection.

Use this Skill when the user asks about body-omen folklore such as eye twitching, ear ringing, sneezing, ear heat, face heat, palm itching, or muscle twitching. The goal is to turn a low-risk folklore question into body-care journaling, ordinary-context reflection, and non-deterministic symbolic language.

Do not use this Skill for diagnosis, treatment, medication advice, emergency triage replacement, or determining whether a symptom is medically serious. If the request includes persistent, sudden, severe, one-sided, painful, vision/hearing/breathing/neurological, fever, pregnancy, medication, or functional-impact symptoms, pause the omen workflow and recommend real-world professional support.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `body_omen_request_guard`.
3. If `can_continue_body_omen` is false, stop the omen workflow and reframe toward medical, safety, or grounding support.
4. Run `body_omen_context_recorder` to capture:
   - omen type
   - body location
   - timing
   - duration or frequency
   - sensation notes
   - health context and medical-boundary notes
   - ordinary context such as sleep, screen use, caffeine, stress, weather, or environment
   - focus and stop condition
5. Run `body_omen_symbol_lookup` for each recognizable signal.
6. Run `body_omen_reflection_planner`.
7. Draft the answer from the plan.
8. Run or emulate `mystic_output_lint` before final output.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/body_omen_request_guard.py`
- `agent-tools/scripts/body_omen_context_recorder.py`
- `agent-tools/scripts/body_omen_symbol_lookup.py`
- `agent-tools/scripts/body_omen_reflection_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary note: body omens are folklore symbolism and body-care reminders, not diagnosis, disaster proof, or decision evidence.
- Context recap: signal, location, timing, duration, ordinary context, and missing fields.
- Symbolic reflection: gentle, non-deterministic meanings such as pause, rest, rhythm, stimulus, social attention, or budget reminder.
- Reality check: rest, hydration, screen breaks, reduce irritants, observe whether symptoms persist, and seek professional support when red flags appear.
- Stop condition: one short record is enough; do not keep checking until reassured.

## Hard Stops

Stop and reframe if the user asks for:

- diagnosis, treatment, medication changes, or avoiding medical care
- sudden, severe, persistent, one-sided, painful, sensory, breathing, neurological, fever, pregnancy, or functional-impact symptoms
- disaster prediction, death omen, bloodshed omen, or certainty
- lottery, gambling, investing, trading, or financial timing
- judging another person's body, fate, feelings, or guilt
- spirit confirmation, exorcism, curse proof, possession, or evil-energy claims
- pressing eyes, bloodletting, self-harm, unsafe tests, or repeated reassurance checking

## Required Tools

- `mystic_intake_triage`
- `body_omen_request_guard`
- `body_omen_context_recorder`
- `body_omen_symbol_lookup`
- `body_omen_reflection_planner`
- `mystic_output_lint`

## References

- `知识库/SOP/63-身体征兆眼跳耳鸣喷嚏象征咨询.md`
- `知识库/流派/身体征兆眼跳耳鸣喷嚏象征.md`
