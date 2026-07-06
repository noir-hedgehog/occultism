---
name: physiognomy-symbolic-consultation
description: Use when a user asks Codex about 手相, 面相, 相术, 掌纹, 生命线, 智慧线, 感情线, 事业线, 掌丘, 五官, 鼻相, 眉眼, 额头, 下巴, 痣相, or wants palmistry/physiognomy symbolism, while avoiding health, lifespan, appearance discrimination, third-party profiling, and deterministic fate claims.
---

# Physiognomy Symbolic Consultation

Use this skill for palmistry, physiognomy, mole-reading, and appearance-symbol questions as cultural symbolism, self-reflection, or creative reference. Do not infer health, lifespan, morality, social worth, wealth, relationship outcome, or professional suitability from appearance.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain physiognomy` when the request is clearly about 手相/面相/相术.
2. Run `physiognomy_request_guard` to check consent and block health, lifespan, appearance discrimination, third-party profiling, coercive use, and deterministic fate claims.
3. If consent is missing, ask whether the subject is the user, whether consent exists, or whether the user wants anonymous cultural learning only.
4. Ask for user-provided observations. Do not analyze photos or invent unprovided facial/body details.
5. Run `physiognomy_observation_recorder` to structure observations and feature codes.
6. Run `physiognomy_symbol_lookup` for each main feature.
7. Run `physiognomy_interpretation_planner` to build the layered answer.
8. Interpret in layers: consent/source, observation, traditional symbol, reality anchor, reflection question, low-risk action.
9. If the user asks for health, lifespan, wealth certainty, marriage fate, morality, hiring, or third-party privacy, explicitly reframe or pause.
10. Run or mentally apply `mystic_output_lint`.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain physiognomy
```

Guard the request:

```bash
python3 agent-tools/scripts/physiognomy_request_guard.py --text "<user request>" --subject-is-self
```

Record observations:

```bash
python3 agent-tools/scripts/physiognomy_observation_recorder.py --text "<user-provided observations>" --subject-is-self
```

Look up symbols:

```bash
python3 agent-tools/scripts/physiognomy_symbol_lookup.py --query 生命线 --focus self_reflection
python3 agent-tools/scripts/physiognomy_symbol_lookup.py --query 鼻相 --focus cultural_learning
```

Plan the interpretation:

```bash
python3 agent-tools/scripts/physiognomy_interpretation_planner.py --text "<user-provided observations>" --subject-is-self
```

Lint the final draft:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
同意状态：
用户提供的观察：
主要符号：
象征层解读：
现实锚点：
可自查问题：
低风险行动：
不建议下的结论：
```

## References

- `知识库/SOP/16-手相面相象征咨询.md`
- `知识库/流派/手相与面相.md`
