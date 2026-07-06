---
name: rune-symbolic-consultation
description: Use when a user asks Codex about 卢恩符文, rune, runes, Elder Futhark, 单符/三符抽取, 符文含义, or repeated rune divination, while keeping the answer symbolic, reality-first, non-deterministic, and non-professional.
---

# Rune Symbolic Consultation

Use this skill for rune questions as cultural learning, symbolic self-reflection, and low-risk cast recording. Do not present rune results as fact, diagnosis, prediction, curse confirmation, professional advice, third-party mind reading, or final decision.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain rune` when the request is clearly about 卢恩符文/rune/Elder Futhark.
2. Run `rune_request_guard` to block professional replacement, deterministic fate claims, financial speculation, third-party privacy/control, spirit-fear confirmation, and repeated dependency.
3. Ask whether the user wants cultural learning, recording an existing cast, or a low-risk reflection.
4. Reframe yes/no and fate questions into resource, obstacle, boundary, evidence, and next-step questions.
5. Run `rune_cast_recorder` to structure the question, spread, runes, positions, source, and missing fields.
6. Run `rune_symbol_lookup` for each rune.
7. Run `rune_interpretation_planner` to build the layered answer.
8. Interpret in layers: boundary, question rewrite, cast record, rune-by-rune symbols, real-world evidence, low-risk action, stop condition.
9. If the user asks for medical/legal/financial decisions, curse confirmation, third-party control, or repeated reassurance, pause and reframe.
10. Run or mentally apply `mystic_output_lint`.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain rune
```

Guard the request:

```bash
python3 agent-tools/scripts/rune_request_guard.py --text "<user request>"
```

Record the cast:

```bash
python3 agent-tools/scripts/rune_cast_recorder.py --text "<question>" --spread-type three_rune --runes "fehu ansuz raidho"
```

Look up symbols:

```bash
python3 agent-tools/scripts/rune_symbol_lookup.py --query "fehu" --focus work_reflection
python3 agent-tools/scripts/rune_symbol_lookup.py --query "algiz" --focus boundary_reflection
```

Plan the interpretation:

```bash
python3 agent-tools/scripts/rune_interpretation_planner.py --text "<question>" --spread-type three_rune --runes "fehu ansuz raidho"
```

Lint the final draft:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
问题改写：
抽取记录：
逐符象征：
现实核查：
低风险下一步：
停止追问条件：
不建议下的结论：
```

## References

- `知识库/SOP/20-卢恩符文象征咨询.md`
- `知识库/流派/卢恩符文.md`
