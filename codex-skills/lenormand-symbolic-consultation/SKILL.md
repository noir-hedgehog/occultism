---
name: lenormand-symbolic-consultation
description: Use when a user asks Codex about 雷诺曼, Lenormand, 雷诺曼卡, 36 张牌, 三张线, 五张线, 九宫格, card combinations, or Lenormand symbolic readings, while keeping the answer symbolic, reality-first, non-deterministic, and non-professional.
---

# Lenormand Symbolic Consultation

Use this skill for Lenormand questions as cultural learning, symbolic self-reflection, and low-risk draw recording. Do not present Lenormand cards as fact, diagnosis, prediction, curse confirmation, professional advice, third-party mind reading, or final decision.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain lenormand` when the request is clearly about 雷诺曼/Lenormand/36 张牌/九宫格.
2. Run `lenormand_request_guard` to block professional replacement, deterministic fate claims, financial speculation, third-party privacy/control, spirit-fear confirmation, and repeated dependency.
3. Ask whether the user wants cultural learning, recording an existing draw, or a low-risk reflection.
4. Reframe yes/no and fate questions into event clues, reality evidence, boundaries, options, and next-step questions.
5. Run `lenormand_draw_recorder` to structure the question, spread, cards, positions, source, and missing fields.
6. Run `lenormand_card_lookup` for each card.
7. Run `lenormand_interpretation_planner` to build the layered answer and adjacent pair prompts.
8. Interpret in layers: boundary, question rewrite, draw record, card-by-card symbols, adjacent combinations, real-world evidence, low-risk action, stop condition.
9. If the user asks for medical/legal/financial decisions, curse confirmation, third-party control, or repeated reassurance, pause and reframe.
10. Run or mentally apply `mystic_output_lint`.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain lenormand
```

Guard the request:

```bash
python3 agent-tools/scripts/lenormand_request_guard.py --text "<user request>"
```

Record the draw:

```bash
python3 agent-tools/scripts/lenormand_draw_recorder.py --text "<question>" --spread-type three_card_line --cards "骑士 信 钥匙"
```

Look up cards:

```bash
python3 agent-tools/scripts/lenormand_card_lookup.py --query "骑士" --focus project_reflection
python3 agent-tools/scripts/lenormand_card_lookup.py --query "信" --focus project_reflection
```

Plan the interpretation:

```bash
python3 agent-tools/scripts/lenormand_interpretation_planner.py --text "<question>" --spread-type three_card_line --cards "骑士 信 钥匙"
```

Lint the final draft:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
问题改写：
抽牌记录：
逐牌象征：
相邻组合：
现实核查：
低风险下一步：
停止追问条件：
不建议下的结论：
```

## References

- `知识库/SOP/21-雷诺曼卡象征咨询.md`
- `知识库/流派/雷诺曼卡.md`
