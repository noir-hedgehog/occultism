---
name: crystal-symbolic-consultation
description: Use when the user asks about crystal, energy-stone, quartz, amethyst, rose quartz, bracelet, pendant, desk stone, cleansing, or symbolic crystal-use requests. Keeps crystals as aesthetic/symbolic reminders and blocks medical, wealth, spirit-fear, ingestion, coercion, expensive-purchase, and dependency claims.
---

# Crystal Symbolic Consultation

## Use When

- The user asks about 水晶, 能量石, 晶石, crystal, quartz, amethyst, rose quartz, 手串, 吊坠, 摆件, 佩戴, 净化, 消磁, or symbolic crystal use.
- The user wants a low-risk reminder object, space object, gift, or self-care ritual.

## Workflow

1. Run or emulate `mystic_intake_triage`.
2. Run `crystal_request_guard`.
3. If blocked, pause crystal consultation and reframe to professional, safety, budget, or grounding support.
4. If allowed, run `crystal_item_recorder` to record intention, items, use context, source, and budget/existing-item note.
5. Run `crystal_symbol_lookup` for known crystals.
6. Run `crystal_use_planner`.
7. Draft with symbolic language only, then run or emulate `mystic_output_lint`.

## Tool Hooks

- `agent-tools/scripts/mystic_intake_triage.py`
- `agent-tools/scripts/crystal_request_guard.py`
- `agent-tools/scripts/crystal_item_recorder.py`
- `agent-tools/scripts/crystal_symbol_lookup.py`
- `agent-tools/scripts/crystal_use_planner.py`
- `agent-tools/scripts/mystic_output_lint.py`

## Output Shape

- Boundary statement: crystals are symbolic, aesthetic, reflective, or reminder objects.
- Context summary: intention, crystal items, use context, source, and budget/existing-item note.
- Symbol layer: known crystal meanings or an explicit unknown/trade-name caveat.
- Reality layer: low-cost, reversible, non-harmful actions tied to the user's actual context.
- Stop conditions: pause for medical issues, crisis, fear escalation, shopping pressure, or repeated dependency.

## Output Rules

- Say crystals are symbolic, aesthetic, reflective, or reminder objects.
- Prefer existing items and low-cost alternatives.
- Tie each crystal to one realistic action or reflection prompt.
- Include stop conditions for fear, shopping pressure, repeated dependency, or professional issues.

## Hard Stops

- Medical treatment, medication replacement, pregnancy, surgery, severe insomnia, anxiety, depression, or crisis claims.
- Wealth guarantees, investment decisions, lottery, gambling, loans, or "must buy this to get rich".
- Drinking crystal water, swallowing, grinding, wound contact, or body insertion.
- Spirit proof, curse confirmation, possession, disaster-blocking proof, or coercing another person.
- Expensive purchase pressure, debt, or repeated buying/cleansing dependency.

## References

- `知识库/SOP/23-水晶与能量石象征咨询.md`
- `知识库/流派/水晶与能量石.md`
