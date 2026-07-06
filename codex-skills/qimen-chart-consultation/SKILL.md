---
name: qimen-chart-consultation
description: Use when a user asks Codex for Qimen Dunjia, 奇门遁甲, chart recording, nine-palace analysis, 用神, 值符, 值使, 门星神干 interpretation, 置闰, 拆补, 飞盘, 转盘, 派别差异, or symbolic situation analysis from a provided Qimen chart with safety boundaries.
---

# Qimen Chart Consultation

Use this skill to structure a Qimen Dunjia consultation from a provided or externally generated chart. Do not invent a chart when the chart data or casting method is missing.

## Workflow

1. Run intake using `agent-tools/scripts/mystic_intake_triage.py` when available.
2. Refuse or redirect medical, legal, financial, coercive, or crisis requests.
3. Confirm question, chart time, timezone, location, chart method, school, true solar time strategy, and solar-term source.
4. Run `qimen_school_reference` when the user asks about school differences, mentions zhirun/chaibu/feipan/turning-plate, or tries to mix conventions.
5. Run `qimen_method_guard` when available. If it returns blocking errors and no external chart is provided, do not generate a chart.
6. Record the chart with `qimen_chart_record` when available.
7. If the chart is incomplete, state missing fields before interpreting.
8. Run `qimen_focus_selector` when available to identify candidate focus targets and relevant palaces.
9. Use `symbolic_depth_lookup` when available to select the safe depth pattern for method limits, focus targets, or palace layering.
10. Interpret by palace: door, star, deity, stems, relation to focus target, practical action.
11. Draft the answer, then run or mentally apply `mystic_output_lint`.

## Tool Hooks

Run general intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain qimen
```

Guard chart-generation assumptions:

```bash
python3 agent-tools/scripts/qimen_method_guard.py --json '{"method":"time_chart","school":"zhirun","chart_time":"<YYYY-MM-DD HH:MM>","timezone":"Asia/Shanghai","location":"<location>","solar_time_strategy":"unknown","solar_term_source":"external_calendar"}'
```

Look up school differences:

```bash
python3 agent-tools/scripts/qimen_school_reference.py --query "置闰和拆补有什么区别"
python3 agent-tools/scripts/qimen_school_reference.py --schools 飞盘 转盘
```

Record the chart:

```bash
python3 agent-tools/scripts/qimen_chart_record.py --json '{"question_text":"<question>","palaces":[{"palace":1,"trigram":"坎","earth_stem":"戊","heaven_stem":"乙","door":"休门","star":"天蓬","deity":"值符"}]}'
```

Select focus targets:

```bash
python3 agent-tools/scripts/qimen_focus_selector.py --json '{"question_text":"<question>","day_stem":"<日干>","hour_stem":"<时干>","duty_door":"<值使门>","duty_star":"<值符星>","palaces":[{"palace":1,"trigram":"坎","earth_stem":"戊","heaven_stem":"乙","door":"休门","star":"天蓬","deity":"值符"}]}'
```

Look up the depth pattern:

```bash
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain qimen --query "<method limit, focus target, or palace layer>"
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
问题重述：
起局信息：
盘式完整性：
用神与相关宫位：
象意分析：
现实映射：
建议行动：
限制与提醒：
```

## References

- `知识库/SOP/05-奇门遁甲局势分析.md`
- `知识库/流派/奇门遁甲.md`
- `知识库/流派/奇门用神与盘式解读骨架.md`
- `知识库/流派/跨流派深度解读矩阵.md`
