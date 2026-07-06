---
name: numerology-symbolic-consultation
description: Use when a user asks Codex about 数字能量, 数字象征, 数字占卜, 生命灵数, 幸运数字, 手机号尾号, 车牌号, 门牌号, 号码比较, or whether a number brings wealth or bad luck, while keeping the answer privacy-preserving, symbolic, non-deterministic, and reality-first.
---

# Numerology Symbolic Consultation

Use this skill for numerology and number-symbol questions as cultural symbolism, preference sorting, and low-risk number selection. Do not collect sensitive identifiers or promise wealth, luck, health, relationship, career, or fate outcomes.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain numerology` when the request is clearly about 数字/号码/灵数.
2. Run `numerology_request_guard` to block sensitive identifiers, financial promises, professional replacement, third-party profiling, and deterministic fate claims.
3. Ask the user to redact full phone numbers, ID numbers, bank cards, account numbers, passwords, and verification codes.
4. Ask for the usage context: phone suffix, license plate, house number, life path, or lucky number.
5. Run `numerology_profile_recorder` to structure digits and context.
6. Run `numerology_symbol_lookup` for the main digits and context.
7. Run `numerology_interpretation_planner` to build the layered answer.
8. Interpret in layers: privacy check, real-world constraints, number symbolism, preference ranking, low-risk action.
9. If the user asks for wealth guarantees, bad-luck fear, professional replacement, or third-party labels, reframe or pause.
10. Run or mentally apply `mystic_output_lint`.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain numerology
```

Guard the request:

```bash
python3 agent-tools/scripts/numerology_request_guard.py --text "<user request>"
```

Record number material:

```bash
python3 agent-tools/scripts/numerology_profile_recorder.py --text "<redacted number material>"
```

Look up symbols:

```bash
python3 agent-tools/scripts/numerology_symbol_lookup.py --query 8 --focus phone_suffix
python3 agent-tools/scripts/numerology_symbol_lookup.py --query 手机号 --focus preference_sorting
```

Plan the interpretation:

```bash
python3 agent-tools/scripts/numerology_interpretation_planner.py --text "<redacted number material>"
```

Lint the final draft:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
脱敏状态：
数字材料：
现实优先条件：
数字象征：
偏好比较：
低风险行动：
不建议下的结论：
```

## References

- `知识库/SOP/18-数字象征与号码咨询.md`
- `知识库/流派/数字象征与号码.md`
