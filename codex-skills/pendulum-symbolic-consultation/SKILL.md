---
name: pendulum-symbolic-consultation
description: Use when a user asks Codex about 灵摆, 摆锤, pendulum, yes/no 摆动, 顺时针/逆时针/左右/前后摆动, 灵摆校准, or repeated pendulum questions, while keeping the answer symbolic, non-deterministic, reality-first, and non-professional.
---

# Pendulum Symbolic Consultation

Use this skill for pendulum and dowsing-style questions as symbolic self-reflection, preference clarification, and low-risk session recording. Do not present pendulum motion as fact, diagnosis, prediction, professional advice, spirit confirmation, or final decision.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain pendulum` when the request is clearly about 灵摆/摆锤/pendulum.
2. Run `pendulum_request_guard` to block professional replacement, deterministic decisions, financial speculation, third-party control, spirit-fear confirmation, and repeated dependency.
3. Ask whether the user wants cultural learning, calibration guidance, or a low-risk reflection.
4. Reframe yes/no questions into evidence, preference, boundary, and next-step questions.
5. Run `pendulum_session_recorder` to structure the question, calibration notes, motion, consent, and missing fields.
6. Run `pendulum_symbol_lookup` for the answer motion or answer state.
7. Run `pendulum_interpretation_planner` to build the layered answer.
8. Interpret in layers: boundary, question rewrite, session record, symbolic motion, real-world evidence, low-risk action, stop condition.
9. If the user asks for medical/legal/financial decisions, spirit confirmation, third-party control, or repeated reassurance, pause and reframe.
10. Run or mentally apply `mystic_output_lint`.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain pendulum
```

Guard the request:

```bash
python3 agent-tools/scripts/pendulum_request_guard.py --text "<user request>"
```

Record the session:

```bash
python3 agent-tools/scripts/pendulum_session_recorder.py --text "<question>" --answer-motion "<motion>" --calibration-notes "<notes>" --consent-confirmed
```

Look up symbols:

```bash
python3 agent-tools/scripts/pendulum_symbol_lookup.py --query "左右" --focus boundary_reflection
python3 agent-tools/scripts/pendulum_symbol_lookup.py --query "calibration" --focus session_setup
```

Plan the interpretation:

```bash
python3 agent-tools/scripts/pendulum_interpretation_planner.py --text "<question>" --answer-motion "<motion>" --calibration-notes "<notes>"
```

Lint the final draft:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
问题改写：
会话记录：
摆动象征：
现实核查：
低风险下一步：
停止追问条件：
不建议下的结论：
```

## References

- `知识库/SOP/19-灵摆占卜象征咨询.md`
- `知识库/流派/灵摆占卜.md`
