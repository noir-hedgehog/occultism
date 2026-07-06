---
name: mingli-bazi-ziwei-consultation
description: Use when a user asks Codex for Bazi, Four Pillars, Chinese astrology, Ziwei Dou Shu, birth chart, 生辰八字, 四柱, 紫微斗数, 命盘, 大运, 流年, 子平, 三合, 四化, 中州, or school-difference consultation, especially when birth data privacy, third-party consent, minors, mixed methods, or fatalistic prediction boundaries matter.
---

# Mingli Bazi Ziwei Consultation

Use this skill for safe, structured Bazi/Four Pillars and Ziwei Dou Shu consultation. Treat the result as symbolic self-reflection and stage review, not deterministic fate.

## Workflow

1. Run general intake using `agent-tools/scripts/mystic_intake_triage.py` when available.
2. Run `bazi_ziwei_intake_guard` when available.
3. Continue only when consent, privacy, professional-risk and fatalistic-prediction checks pass.
4. Confirm the system: Bazi, Ziwei Dou Shu, or cultural explanation only.
5. Run `mingli_school_reference` when the user asks about 子平/传统/现代综合/三合/四化/中州, asks whether methods can be mixed, or gives only a broad lineage label.
6. Confirm birth date, birth time, birth place, calendar type, timezone/solar-time strategy, and analysis focus.
7. Record chart preparation parameters with `bazi_ziwei_chart_record` when available.
8. If chart generation is not available, ask the user to provide chart fields or give a non-chart cultural explanation.
9. Use `mingli_symbol_lookup` when explaining stems, branches, ten gods, Ziwei palaces, or main stars.
10. Use `symbolic_depth_lookup` when available to select the safe depth pattern for symbols, privacy, third-party consent, or minors.
11. Interpret by layers: data certainty, symbolic structure, real-world mapping, observable signals, low-risk next steps.
12. Draft the answer, then run or mentally apply `mystic_output_lint`.
13. End with privacy and non-determinism limits.

## Tool Hooks

Run general intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain mingli
```

Guard birth-data intake:

```bash
python3 agent-tools/scripts/bazi_ziwei_intake_guard.py --text "<user request>"
```

Look up school/method differences:

```bash
python3 agent-tools/scripts/mingli_school_reference.py --query "子平和紫微三合能混着看事业吗"
python3 agent-tools/scripts/mingli_school_reference.py --schools 三合 四化
```

Record chart parameters:

```bash
python3 agent-tools/scripts/bazi_ziwei_chart_record.py --json '{"system":"bazi","birth_date":"<YYYY-MM-DD>","birth_time":"<HH:MM>","birth_place":"<place>","calendar_type":"solar","timezone":"Asia/Shanghai","solar_time_strategy":"not_applied","chart_source":"external_calculator"}'
```

Lookup symbolic terms:

```bash
python3 agent-tools/scripts/mingli_symbol_lookup.py --query 七杀 --category ten_god --focus career
python3 agent-tools/scripts/mingli_symbol_lookup.py --query 官禄宫 --category ziwei_palace
```

Look up the depth pattern:

```bash
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain mingli --query "<symbol, privacy, or consent issue>"
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
隐私与同意：
资料完整度：
问题重述：
命理体系：
资料记录：
象征结构：
现实映射：
可观察信号：
低风险建议：
限制与提醒：
```

## References

- `知识库/SOP/06-命理咨询边界.md`
- `知识库/SOP/08-命理排盘参数记录.md`
- `知识库/流派/八字与紫微斗数.md`
- `知识库/流派/命理象征索引.md`
- `知识库/流派/跨流派深度解读矩阵.md`
