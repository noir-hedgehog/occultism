---
name: zodiac-symbolic-consultation
description: Use when the user asks about 生肖, 属相, 十二生肖, 本命年, 太岁, 犯太岁, 冲太岁, 三合, 六合, 六冲, 相冲, Chinese zodiac, zodiac year, or Tai Sui symbolic consultation. Blocks fate certainty, disaster fear, zodiac compatibility discrimination, professional replacement, expensive cure pressure, and dependency.
---

# Zodiac Symbolic Consultation

## Use When

- The user asks about 生肖, 属相, 十二生肖, 本命年, 太岁, 犯太岁, 冲太岁, Chinese zodiac, zodiac year, or Tai Sui.
- The user wants cultural learning, source recording, yearly reflection, low-risk planning, or a non-scary explanation of family or internet claims.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `zodiac_request_guard`.
3. If blocked, pause zodiac consultation and reframe to safety, professional support, budget support, relationship communication, or grounding.
4. If allowed, run `zodiac_profile_recorder`.
5. Run `zodiac_symbol_lookup` for zodiac animals, benmingnian, Tai Sui, harmony, or clash motifs.
6. Run `zodiac_interpretation_planner`.
7. Draft with cultural and symbolic language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/zodiac_request_guard.py`
- `agent-tools/scripts/zodiac_profile_recorder.py`
- `agent-tools/scripts/zodiac_symbol_lookup.py`
- `agent-tools/scripts/zodiac_interpretation_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: zodiac and Tai Sui are cultural symbols and low-risk reflection prompts.
- Source summary: year/zodiac, subject scope, source note, focus, and missing fields.
- Symbol layer: zodiac animal, benmingnian, Tai Sui, harmony, or clash motif.
- Reality layer: practical constraints, communication, budget, safety, and low-risk next action.

## Hard Stops

- Fate certainty, disaster certainty, death, blood disaster, unavoidable misfortune, or Tai Sui revenge.
- Medical, legal, financial, safety, or mental-health replacement.
- Zodiac compatibility discrimination, forced breakup, marriage prohibition, or third-party personality labels.
- Expensive Tai Sui cure pressure, paid ritual pressure, or repeated dependency.

## References

- `知识库/SOP/25-生肖太岁象征咨询.md`
- `知识库/流派/生肖太岁.md`
