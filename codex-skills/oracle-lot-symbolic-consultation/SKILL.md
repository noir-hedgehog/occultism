---
name: oracle-lot-symbolic-consultation
description: Use when a user asks Codex to interpret 求签, 解签, 签文, 签诗, 签号, 观音签, 月老签, 灵签, 寺庙签, 抽签, 模拟抽签, or asks whether a lot means a definite outcome, while keeping the answer symbolic, source-aware, non-deterministic, and non-professional.
---

# Oracle Lot Symbolic Consultation

Use this skill for oracle-lot, temple-lot, and 签文 interpretation as cultural symbolism, reflection, or low-risk decision sorting. Do not treat a lot as a command, guarantee, prophecy, professional decision basis, or proof of another person's thoughts.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain oracle_lot` when the request is clearly about 求签/解签/签文.
2. Run `oracle_lot_request_guard` to block professional replacement, deterministic fate, coercion, third-party privacy, and dependency loops.
3. Ask for the lot source, lot text, lot number, grade, draw method, and one focused question.
4. If the user wants a simulated draw, state that simulation is entertainment/reflection and ask for consent before simulating.
5. Run `oracle_lot_record_builder` to structure source and lot material.
6. Run `oracle_lot_symbol_lookup` for grade, text/source/topic symbols.
7. Run `oracle_lot_interpretation_planner` to build interpretation layers.
8. Interpret in layers: source, text keywords, symbolic reminder, reality anchor, low-risk action.
9. If the user asks for guaranteed results, disaster proof, professional replacement, repeated draws, or third-party mind reading, reframe or pause.
10. Run or mentally apply `mystic_output_lint`.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain oracle_lot
```

Guard the request:

```bash
python3 agent-tools/scripts/oracle_lot_request_guard.py --text "<user request>"
```

Record the lot:

```bash
python3 agent-tools/scripts/oracle_lot_record_builder.py --question "<question>" --lot-text "<lot text>" --source-type temple
```

Look up symbols:

```bash
python3 agent-tools/scripts/oracle_lot_symbol_lookup.py --query 上签 --focus relationship_reflection
python3 agent-tools/scripts/oracle_lot_symbol_lookup.py --query 签文 --focus career_reflection
```

Plan the interpretation:

```bash
python3 agent-tools/scripts/oracle_lot_interpretation_planner.py --question "<question>" --lot-text "<lot text>" --source-type temple
```

Lint the final draft:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
签文来源：
用户问题：
签文/签号/签等：
关键词：
象征层解读：
现实锚点：
低风险行动：
不建议下的结论：
```

## References

- `知识库/SOP/17-求签与签文象征咨询.md`
- `知识库/流派/求签与签文.md`
