# astrology_chart_record

## Purpose

Record and validate externally provided astrology chart fields without calculating a chart. This tool lets an agent preserve source, consent, privacy and placement structure before using `astrology_symbol_lookup`.

## Input

```json
{
  "chart_source": "external_calculator",
  "analysis_focus": "career",
  "subject_is_self": true,
  "placements": [
    { "type": "planet", "name": "太阳", "sign": "天秤", "house": "十宫" },
    { "type": "planet", "name": "月亮", "sign": "巨蟹" },
    { "type": "point", "name": "上升", "sign": "摩羯" }
  ]
}
```

## Output

The tool returns:

- normalized chart source and focus
- subject consent and minor flags
- normalized placements
- privacy flags
- validity, errors, warnings and required pre-interpretation actions
- limits and next workflow steps

## Boundaries

- This tool does not calculate a chart.
- It records only fields already provided by the user or an external source.
- Exact birth data should be minimized once placements are available.
- Third-party chart fields require consent.
- Interpretations must remain symbolic and non-deterministic.
