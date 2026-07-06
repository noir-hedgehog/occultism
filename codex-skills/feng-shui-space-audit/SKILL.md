---
name: feng-shui-space-audit
description: Use when a user asks Codex to review home, bedroom, office, shop, desk, layout, placement, energy flow, feng shui, Flying Star, Eight Mansions, compass direction, Xuan Kong, 八宅, 玄空飞星, 罗盘, 坐向, 阳宅 concerns, or wants comparable Yangzhai case patterns, especially when the answer should combine traditional feng shui language with practical space, school-boundary, and safety advice.
---

# Feng Shui Space Audit

Use this skill to review a physical space through practical comfort, safety, layout, and traditional feng shui vocabulary.

## Workflow

1. Run intake using `agent-tools/scripts/mystic_intake_triage.py` when available.
2. Check safety first: gas, mold, fire, electrical hazards, severe sleep disruption, or stalking/security concerns.
3. If the user asks for Xuan Kong, Flying Star, Eight Mansions, compass, sitting/facing direction, auspicious/inauspicious sectors, or other school-specific liqi methods, run `fengshui_school_guard` before interpreting.
4. If images, image notes, or layout text are provided, record observable facts with `fengshui_observation_recorder` when available.
5. Generate a checklist with `fengshui_space_checklist` when available.
6. For home/shop scenario examples, look up comparable Yangzhai cases with `fengshui_yangzhai_case_library` when available.
7. If the user gives a direction, use `fengshui_bagua_mapper` as a symbolic compass-Bagua reference.
8. Rank candidate adjustments with `fengshui_recommendation_ranker` when available.
9. Use `symbolic_depth_lookup` when available to select the safe depth pattern for Bagua, visible facts, or recommendation ranking.
10. Ask for the minimum useful context: space type, main concern, door/window/bed/desk/stove placement, light, noise, clutter, and optional direction.
11. If images are provided, describe observable layout before interpreting.
12. Separate:
   - Practical observation.
   - Traditional feng shui framing.
   - School/method limits.
   - Low-cost reversible adjustment.
13. Rank suggestions by safety, effort, cost, and reversibility.
14. Run or mentally apply `mystic_output_lint`.
15. Avoid deterministic claims about disaster, illness, wealth, marriage, or fate.

## Tool Hooks

Use the intake tool before auditing:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain feng_shui
```

Continue only when `risk_level` is `green` or `yellow`. For `orange` or `red`, handle the real-world safety issue before any feng shui interpretation.

Record observable facts:

```bash
python3 agent-tools/scripts/fengshui_school_guard.py --text "用玄空飞星看厨房五黄是不是会破财生病"
python3 agent-tools/scripts/fengshui_observation_recorder.py --text "<image notes or space description>"
```

Generate the space checklist:

```bash
python3 agent-tools/scripts/fengshui_space_checklist.py --text "<user space description>"
```

If `can_continue_fengshui` is false, prioritize the returned safety notes before any traditional interpretation.

Look up comparable Yangzhai cases:

```bash
python3 agent-tools/scripts/fengshui_yangzhai_case_library.py --query "<home, bedroom, office, shop, entrance, or kitchen scenario>"
```

Map optional Bagua direction:

```bash
python3 agent-tools/scripts/fengshui_bagua_mapper.py --text "<space direction and concern>"
```

Rank recommendations:

```bash
python3 agent-tools/scripts/fengshui_recommendation_ranker.py --json '{"recommendations":[{"recommendation":"清理门后杂物"}]}'
```

Look up the depth pattern:

```bash
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain fengshui --query "<direction, visible fact, or adjustment type>"
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
空间类型：
主要困扰：
观察到的格局：
传统术语解释：
现实体验映射：
建议优先级：
限制与提醒：
```

## References

- `知识库/SOP/02-风水空间审视.md`
- `知识库/SOP/07-风水观察记录规范.md`
- `知识库/流派/风水.md`
- `知识库/流派/风水阳宅案例库.md`
- `知识库/流派/风水八卦方位映射.md`
- `知识库/流派/风水理气派别边界.md`
- `知识库/流派/跨流派深度解读矩阵.md`
