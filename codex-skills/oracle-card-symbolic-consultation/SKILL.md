---
name: oracle-card-symbolic-consultation
description: Use when a user asks Codex about 神谕卡, 神谕牌, oracle cards, oracle decks, 天使卡, 动物灵性卡, 能量卡, card keywords, or open-ended oracle-card symbolic readings, while keeping the answer symbolic, reality-first, non-deterministic, and non-professional.
---

# Oracle Card Symbolic Consultation

Use this skill for oracle-card questions as cultural learning, symbolic self-reflection, and low-risk draw recording. Do not present oracle cards as fact, diagnosis, prediction, spirit command, professional advice, third-party mind reading, or final decision.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain oracle_card` when the request is clearly about 神谕卡/oracle cards/oracle decks/天使卡/能量卡.
2. Run `oracle_card_request_guard` to block professional replacement, deterministic fate claims, financial speculation, third-party privacy/control, spirit-fear confirmation, and repeated dependency.
3. Ask whether the user wants cultural learning, recording an existing draw, or a low-risk reflection.
4. Ask for deck name, card title, card text, keywords, or visible image motifs. Do not invent deck-specific meanings.
5. Run `oracle_card_draw_recorder` to structure the question, deck/source, spread, cards, positions, and missing fields.
6. Run `oracle_card_symbol_lookup` for recognizable motifs or keywords.
7. Run `oracle_card_interpretation_planner` to build the layered answer.
8. Interpret in layers: boundary, question rewrite, draw record, card/motif symbols, real-world evidence, low-risk action, stop condition.
9. If the user asks for medical/legal/financial decisions, spirit commands, third-party control, or repeated reassurance, pause and reframe.
10. Run or mentally apply `mystic_output_lint`.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain oracle_card
```

Guard the request:

```bash
python3 agent-tools/scripts/oracle_card_request_guard.py --text "<user request>"
```

Record the draw:

```bash
python3 agent-tools/scripts/oracle_card_draw_recorder.py --text "<question>" --deck-name "<deck/source>" --spread-type three_card_reflection --cards "门 桥 种子"
```

Look up motifs:

```bash
python3 agent-tools/scripts/oracle_card_symbol_lookup.py --query "门" --focus project_reflection
python3 agent-tools/scripts/oracle_card_symbol_lookup.py --query "桥" --focus communication_reflection
```

Plan the interpretation:

```bash
python3 agent-tools/scripts/oracle_card_interpretation_planner.py --text "<question>" --deck-name "<deck/source>" --spread-type three_card_reflection --cards "门 桥 种子"
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
牌面/母题象征：
现实核查：
低风险下一步：
停止追问条件：
不建议下的结论：
```

## References

- `知识库/SOP/22-神谕卡象征咨询.md`
- `知识库/流派/神谕卡.md`
