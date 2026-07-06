---
name: date-selection-consultation
description: Use when a user asks Codex to choose or compare auspicious dates, 吉日, 择日, 黄历, 老黄历, 宜忌, 黄道吉日, 黑道日, 冲生肖, 搬家吉日, 开业吉日, 结婚吉日, 领证日, 开工日, 出行日, or symbolic date planning, while keeping practical constraints and professional boundaries above folk preferences.
---

# Date Selection Consultation

Use this skill for safe auspicious-date, almanac and symbolic date-planning consultation. Treat date selection as source-limited folk symbolism and practical planning support, not as a guarantee of outcome.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain date_selection` when the request is clearly about auspicious dates or almanac terms.
2. Run `date_selection_guard` to catch professional replacement, deterministic outcome, medical/financial timing, or dangerous ritual risks.
3. If risk blocks the request, pause date selection and foreground professional or safety constraints.
4. Ask for event type, candidate dates, unavailable dates, participants, location, practical constraints and almanac source.
5. Use `almanac_symbol_lookup` when the user mentions `宜`, `忌`, `冲`, `煞`, `黄道吉日`, `黑道日`, `建除十二神` or `值神`.
6. Use `date_constraint_recorder` to structure candidate dates and constraints.
7. Use `date_option_ranker` only after candidate dates are known.
8. Rank practical constraints above symbolic preferences.
9. Draft with preference language: "更适合", "可优先考虑", "需要先确认".
10. Run or mentally apply `mystic_output_lint`.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain date_selection
```

Guard the request:

```bash
python3 agent-tools/scripts/date_selection_guard.py --text "<user request>"
```

Explain almanac terms:

```bash
python3 agent-tools/scripts/almanac_symbol_lookup.py --query 黄道吉日 --source-type user_provided_almanac
```

Record constraints:

```bash
python3 agent-tools/scripts/date_constraint_recorder.py --text "<request and constraints>" --candidate-date 2026-08-08
```

Rank candidate dates:

```bash
python3 agent-tools/scripts/date_option_ranker.py --text "<request and constraints>" --candidate-date 2026-08-08 --candidate-date 2026-08-15
```

Lint the final draft:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
事件类型：
候选日期：
现实约束：
黄历/民俗来源：
术语解释：
排序建议：
需要先确认的现实事项：
不建议下的结论：
限制与提醒：
```

## References

- `知识库/SOP/15-择日与黄历象征咨询.md`
- `知识库/流派/择日与黄历.md`
