---
name: bibliomancy-symbolic-consultation
description: Use when the user asks about 书占, 书籍占卜, 随机翻书, 翻书占卜, book divination, bibliomancy, or random book oracle as symbolic reflection. Blocks medical/mental-health/legal/financial replacement, deterministic fate, third-party privacy invasion, religious/scriptural authority commands, long copyrighted text or piracy requests, and repeated dependency.
---

# Bibliomancy Symbolic Consultation

## Use When

- The user asks about 书占、书籍占卜、随机翻书、翻书占卜、book divination, bibliomancy, or random book oracle.
- The user wants cultural learning, a short user-provided passage/keyword record, symbolic reading reflection, or low-risk journaling.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `bibliomancy_request_guard`.
3. If blocked, pause bibliomancy consultation and reframe to professional support, privacy, real-world evidence, short user-provided excerpts, copyright-compliant summary, or stopping repeated dependency.
4. If allowed, run `bibliomancy_source_recorder`.
5. Run `bibliomancy_symbol_lookup` for source, selection, text-unit, or motif symbols.
6. Run `bibliomancy_reflection_planner`.
7. Draft with symbolic reading-reflection language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/bibliomancy_request_guard.py`
- `agent-tools/scripts/bibliomancy_source_recorder.py`
- `agent-tools/scripts/bibliomancy_symbol_lookup.py`
- `agent-tools/scripts/bibliomancy_reflection_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: the passage is a symbolic prompt, not fate, divine command, diagnosis, legal/financial advice, third-party mind reading, or professional replacement.
- Context summary: source title/type, selection method, page/location, short user-provided excerpt or keywords, emotions, reality anchor, and focus.
- Symbol layer: source/selection/text motifs with cautious limits.
- Reality layer: evidence, consent, copyright, professional-support and repeated-use limits.
- Action layer: low-cost, reversible, non-harmful journaling, reading reflection, communication, reality check, or stopping condition.

## Hard Stops

- Medical, mental-health, legal, financial, emergency, or safety replacement.
- Third-party mind reading, coercion, revenge, forced reunion, deterministic fate, divine punishment, scripture/classic as absolute command, long copyrighted excerpts, full chapters/books, piracy, invented source text, or repeated dependency.

## References

- `知识库/SOP/42-书占随机翻书象征咨询.md`
- `知识库/流派/书占与随机翻书.md`
