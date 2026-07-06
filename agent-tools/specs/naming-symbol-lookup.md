# naming_symbol_lookup

## Purpose

Return safe symbolic prompts for Chinese naming and name-reflection work. The tool covers name dimensions, five-phase imagery, use types and cultural risk checks without claiming that a name determines fate.

## Input

```json
{
  "query": "字义",
  "category": "dimension",
  "focus": "baby_name"
}
```

`category` may be `dimension`, `element`, `name_type` or `cultural_check`. Common Chinese aliases such as `含义`, `读音`, `生肖`, `乳名`, `谐音` and `生僻字` are normalized.

## Output

The tool returns:

- canonical symbol name and category
- symbolic layer and code
- keywords
- interpretation prompt
- reflection questions
- action guidance
- prohibited uses
- next workflow steps

## Boundaries

- Do not claim a name guarantees destiny, wealth, health, relationship outcome or disaster avoidance.
- Do not replace legal registration, trademark search, branding research or professional advice.
- For minors, avoid fixed personality labels and preserve the child's future autonomy.
