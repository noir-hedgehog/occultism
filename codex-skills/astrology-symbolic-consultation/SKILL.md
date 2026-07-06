---
name: astrology-symbolic-consultation
description: Use when a user asks Codex for astrology, zodiac signs, natal chart, birth chart, Sun/Moon/Rising, houses, aspects, synastry-style reflection, 星座, 占星, 星盘, 太阳/月亮/上升, 宫位, 相位, or non-deterministic astrology consultation, especially when birth data privacy, third-party consent, compatibility, or fatalistic prediction boundaries matter.
---

# Astrology Symbolic Consultation

Use this skill for safe, structured astrology and natal-chart symbolic consultation. Treat chart symbols as reflection prompts and pattern language, not deterministic fate, diagnosis, compatibility proof, or professional advice.

## Workflow

1. Run general intake using `agent-tools/scripts/mystic_intake_triage.py` when available.
2. Continue only when professional-risk, crisis, coercion, privacy and fatalistic-prediction checks pass.
3. Confirm whether the user wants cultural learning, self-understanding, relationship reflection, career reflection, or a daily symbolic prompt.
4. If exact birth data or a full chart is needed, ask the user to provide external chart placements and source; do not invent or calculate a precise chart.
5. For synastry, compatibility, relationship fate, ex-partner or "does they love me" requests, use `astrology_compatibility_guard` before any chart interpretation.
6. If third-party or minor data appears, require consent and minimize exact birth details; without consent, provide only anonymous cultural explanation or self-reflection.
7. Use `astrology_chart_record` to record externally provided placements, source, consent and privacy limits before interpreting a personal chart.
8. Use `astrology_symbol_lookup` when explaining signs, planets, points, houses or aspects.
9. Interpret by layers: data/source limits, symbol layer, real-world mapping, observable signals, low-risk next steps.
10. Draft the answer, then run or mentally apply `mystic_output_lint`.
11. End with non-determinism, privacy and professional-advice limits.

## Tool Hooks

Run general intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain astrology
```

Lookup astrology symbols:

```bash
python3 agent-tools/scripts/astrology_compatibility_guard.py --text "用合盘看我和前任是不是命中注定的绝配"
python3 agent-tools/scripts/astrology_chart_record.py --json '{"chart_source":"external_calculator","analysis_focus":"career","subject_is_self":true,"placements":[{"type":"planet","name":"太阳","sign":"天秤","house":"十宫"},{"type":"planet","name":"月亮","sign":"巨蟹"},{"type":"point","name":"上升","sign":"摩羯"}]}'
python3 agent-tools/scripts/astrology_symbol_lookup.py --query 天秤 --category sign --focus relationship
python3 agent-tools/scripts/astrology_symbol_lookup.py --query 月亮 --category planet --focus self_understanding
python3 agent-tools/scripts/astrology_symbol_lookup.py --query 十宫 --category house --focus career
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
资料来源与同意：
问题重述：
符号清单：
象征解释：
现实映射：
可观察信号：
低风险建议：
限制与提醒：
```

## References

- `知识库/SOP/09-占星星盘象征咨询.md`
- `知识库/流派/占星.md`
