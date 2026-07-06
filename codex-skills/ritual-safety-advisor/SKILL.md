---
name: ritual-safety-advisor
description: Use when a user asks Codex about exorcism, spirit cleansing, curse removal, haunted spaces, protection rituals, folk ritual safety, or symbolic space cleansing, especially when the request may involve fear, danger, coercion, or mental health risk.
---

# Ritual Safety Advisor

Use this skill to handle exorcism, spirit-cleansing, curse-removal, and protection-ritual requests safely. Do not confirm supernatural causation.

## Workflow

1. Run `agent-tools/scripts/mystic_intake_triage.py` when available.
2. Run `agent-tools/scripts/ritual_safety_check.py` when available.
3. Screen for immediate danger, self-harm, harm to others, coercion, hallucinations, severe insomnia, or unsafe materials.
4. Run `ritual_source_example_lookup` for source classification examples when the source category is unclear.
5. Run `ritual_source_guard` when the user cites a folk, religious, commercial, online, or personal ritual source.
6. Run `ritual_low_risk_protocol` when the user wants a safe substitute practice.
7. If risk is Orange or Red, stop ritual guidance and recommend real-world support.
8. If safe to continue, reframe the request as symbolic cleansing, space reset, emotional grounding, or cultural learning.
9. Do not provide steps involving fire, blood, blades, ingestion, sealed-room smoke, sleep deprivation, or threats toward others.
10. Offer low-risk alternatives: cleaning, ventilation, light, sound, journaling, trusted-person check-in, non-flame scent, simple closing phrase.
11. Use `symbolic_depth_lookup` when available to select the safe depth pattern for fear reframing, source claims, or low-risk protocol language.
12. Run or mentally apply `mystic_output_lint`.
13. Keep the tone calm and non-escalating.

## Tool Hooks

Run the general intake triage before any ritual-specific answer:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>"
```

Use the ritual safety tool after intake triage:

```bash
python3 agent-tools/scripts/ritual_safety_check.py --text "<user request>"
```

If `can_continue_symbolic_support` is false, do not provide ritual steps. Offer only the returned safe alternatives and referral message.

Classify source and convert to safe symbolic support:

```bash
python3 agent-tools/scripts/ritual_source_example_lookup.py --text "<user ritual source or request>"
python3 agent-tools/scripts/ritual_source_guard.py --text "<user ritual source or request>" --source-type unknown
```

Select a low-risk protocol:

```bash
python3 agent-tools/scripts/ritual_low_risk_protocol.py --text "<user ritual request>"
```

Look up the depth pattern:

```bash
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain ritual --query "<fear, source claim, or safe substitute>"
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
我不能确认的部分：
可以安全处理的目标：
低风险步骤：
现实检查：
何时寻求帮助：
```

## References

- `知识库/SOP/03-空间净化与驱邪安全咨询.md`
- `知识库/流派/空间净化与驱邪.md`
- `知识库/流派/民俗仪式资料来源规范.md`
- `知识库/流派/地区宗教来源样例.md`
- `知识库/流派/仪式低风险真实案例集.md`
- `知识库/流派/跨流派深度解读矩阵.md`
