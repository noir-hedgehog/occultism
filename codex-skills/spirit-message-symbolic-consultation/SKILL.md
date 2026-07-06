---
name: spirit-message-symbolic-consultation
description: Use when the user asks about 通灵, 灵媒, 灵讯, 高我, 高我讯息, 守护灵, 指导灵, 天使讯息, 祖先讯息, 自动书写, channeling, spirit guides, higher self, angel messages, or automatic writing as symbolic reflection. Blocks crisis/command voices, hallucination or delusion framing, medical or mental-health replacement, spirit fact claims, third-party privacy invasion, coercion, financial/legal use, expensive session pressure, and repeated dependency.
---

# Spirit Message Symbolic Consultation

## Use When

- The user asks about 通灵、灵媒、灵讯、高我、守护灵、指导灵、天使讯息、祖先讯息、自动书写、channeling, spirit guides, higher self, or automatic writing.
- The user wants cultural learning, message journaling, symbolic writing, or low-risk inner-dialogue reflection.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `spirit_message_request_guard`.
3. If blocked, pause spirit-message consultation and reframe to immediate safety, trusted-person support, medical/mental-health support, privacy, budget, relationship-boundary, or grounding support.
4. If allowed, run `spirit_message_record_builder`.
5. Run `spirit_message_symbol_lookup` for known source metaphors, processes, or symbols.
6. Run `spirit_message_reflection_planner`.
7. Draft with symbolic writing and present-life reflection language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/spirit_message_request_guard.py`
- `agent-tools/scripts/spirit_message_record_builder.py`
- `agent-tools/scripts/spirit_message_symbol_lookup.py`
- `agent-tools/scripts/spirit_message_reflection_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: spirit messages are symbolic writing prompts, not facts, commands, diagnosis, spirit proof, or professional advice.
- Context summary: source, phrase, symbols, emotions, reality anchor, consent/privacy notes, and focus.
- Symbol layer: source/symbol prompts with cautious limits.
- Reality layer: current boundaries, care needs, privacy, relationship choices, and support limits.
- Action layer: low-cost, reversible, non-harmful journaling, grounding, communication, rest, or practical steps.

## Hard Stops

- Self-harm, harm to others, command voices, hallucinations, delusion framing, crisis claims, severe insomnia, panic, or loss of control.
- Medical treatment, diagnosis, medication replacement, mental-health replacement, or crisis support replacement.
- Spirit possession, curse, spirit fact proof, exorcism confirmation, third-party mind reading, privacy invasion, coercion, revenge, forced reunion, curse work, financial/legal outcomes, expensive session pressure, or repeated dependency.

## References

- `知识库/SOP/40-通灵高我讯息象征咨询.md`
- `知识库/流派/通灵高我与灵性讯息.md`
