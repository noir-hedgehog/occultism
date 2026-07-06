---
name: dream-symbolic-consultation
description: Use when a user asks Codex to interpret dreams, nightmares, recurring dreams, dream symbols, 梦见, 解梦, 噩梦, 掉牙, 梦见蛇, 梦见水, 梦见死亡, 梦见考试, 被追, 坠落, 飞行, 迷路, or asks whether a dream is an omen, while keeping the answer symbolic, non-diagnostic, and non-predictive.
---

# Dream Symbolic Consultation

Use this skill for dream interpretation as symbolic reflection, emotion sorting, cultural meaning, or creative prompting. Do not treat dreams as diagnosis, prophecy, supernatural proof, or proof of another person's true thoughts.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain dream` when the request is clearly about dreams.
2. Pause or reroute self-harm, severe insomnia, repeated nightmares with impairment, hallucination, trauma crisis, medical/mental-health diagnosis, or supernatural fear-escalation.
3. Ask for dream text, waking emotion, recent context and user goal.
4. Run `dream_record_builder` to structure the dream and identify risk flags.
5. Run `dream_symbol_lookup` for the main dream symbols.
6. Run `dream_interpretation_planner` to build the interpretation layers.
7. Interpret in layers: dream material, waking emotion, symbol layer, waking-life anchor, low-risk action.
8. If the user asks whether the dream is an omen, disaster sign, curse, death warning or proof someone is harming them, explicitly downgrade to symbolic and emotional language.
9. Run or mentally apply `mystic_output_lint`.
10. End with non-diagnostic, non-predictive and professional-support limits.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain dream
```

Record dream material:

```bash
python3 agent-tools/scripts/dream_record_builder.py --text "<dream text>" --context "<recent waking context>"
```

Look up symbols:

```bash
python3 agent-tools/scripts/dream_symbol_lookup.py --query 掉牙 --focus self_reflection
python3 agent-tools/scripts/dream_symbol_lookup.py --query 水 --focus emotional_pressure
```

Plan the interpretation:

```bash
python3 agent-tools/scripts/dream_interpretation_planner.py --text "<dream text>" --context "<recent waking context>"
```

Lint the final draft:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
梦境素材：
醒后感受：
现实背景：
主要符号：
象征层解读：
现实锚点：
低风险行动：
不建议下的结论：
何时寻求现实支持：
```

## References

- `知识库/SOP/14-解梦与梦境象征咨询.md`
- `知识库/流派/解梦.md`
