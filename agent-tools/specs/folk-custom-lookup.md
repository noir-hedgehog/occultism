# folk_custom_lookup

## Purpose

Return safe cultural prompts for Chinese folk festivals, taboos, symbols and life-event customs. The tool helps an agent explain a custom as cultural material while separating source limits, regional variation, real-world safety and low-risk alternatives.

## Input

```json
{
  "query": "端午",
  "category": "festival",
  "focus": "cultural_learning"
}
```

`category` may be `festival`, `taboo`, `symbol` or `life_event`. Common aliases such as `端午节`, `鬼节`, `插筷子`, `乔迁`, `开业` and `怀孕禁忌` are normalized.

## Output

- canonical custom name and category
- cultural symbol layer and code
- keywords
- interpretation prompt
- reflection questions
- action guidance
- prohibited uses
- next workflow steps

## Boundaries

- Do not claim a taboo inevitably causes disaster or that a symbol guarantees blessing, health, wealth or protection.
- Route dangerous ritual elements to `ritual_safety_check`, `ritual_source_guard` or `ritual_low_risk_protocol`.
- Unknown or local customs must be marked as source-limited rather than universal rules.
