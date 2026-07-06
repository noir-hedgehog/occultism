---
name: folk-custom-consultation
description: Use when a user asks Codex about Chinese folk customs, 民俗, 节令, 禁忌, 习俗, 传统, 地区来源, 家人口述, 春节, 清明, 端午, 中元, 中秋, 冬至, 筷子插饭, 夜里吹口哨, 正月剪发, 搬家讲究, 犯忌会不会倒霉, 招鬼, 冲撞, 门神, 艾草, 香囊, 桃木, or safe cultural explanation, source recording and low-risk translation of folk taboos.
---

# Folk Custom Consultation

Use this skill for safe folk-custom, seasonal-festival, taboo and symbolic-object consultation. Treat customs as cultural material with source limits and regional variation, not as proof of supernatural causality or mandatory ritual law.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain folk_custom` when the request is clearly about customs, festivals or taboos.
2. Pause or reroute dangerous ritual, professional-risk, crisis, coercive or fear-escalating requests before explaining the custom.
3. Ask for source, region, family context and user goal: cultural learning, writing, event planning, family communication or self-soothing.
4. If the user provides or asks to record a source, region, family saying, internet claim, commercial claim or religious context, run `folk_source_recorder`.
5. Use `folk_custom_lookup` for festivals, taboos, folk symbols and life-event customs.
6. If the user asks whether a taboo will cause disaster, ghosts, collision, harm to family, punishment or coercive obedience, run `folk_taboo_reframer` before explaining.
7. Interpret in layers: source limits, cultural symbolism, regional/family variation, real-world safety and low-risk translation.
8. If the custom includes burning, smoke, ingestion, blades, sealed rooms, pregnancy, infants, illness or travel safety, foreground real-world safety.
9. For unknown internet claims, label them as unverified; do not upgrade them into tradition.
10. Draft the answer, then run or mentally apply `mystic_output_lint`.
11. End with cultural-source, non-determinism and professional-advice limits.

## Tool Hooks

Run intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain folk_custom
```

Lookup customs:

```bash
python3 agent-tools/scripts/folk_custom_lookup.py --query 端午 --category festival --focus cultural_learning
python3 agent-tools/scripts/folk_custom_lookup.py --query 筷子插饭 --category taboo --focus family_communication
python3 agent-tools/scripts/folk_custom_lookup.py --query 艾草 --category symbol --focus low_risk_translation
```

Record source provenance:

```bash
python3 agent-tools/scripts/folk_source_recorder.py --text "家里老人说江南搬家要先开灯和清扫入口" --custom-name 搬家习俗 --source-type family_oral --region 江南 --source-label 外婆口述 --source-date "上一辈口述" --usage-context family_communication
```

Reframe fear-escalating taboo claims:

```bash
python3 agent-tools/scripts/folk_taboo_reframer.py --text "夜里吹口哨是不是一定会招鬼害家人" --source-type family --region "江南家庭说法"
```

Lint the final draft:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
来源与地区：
来源记录：
问题重述：
民俗条目：
恐惧降级：
文化解释：
现实安全：
可保留的低风险部分：
不建议做的部分：
替代表达或行动：
限制与提醒：
```

## References

- `知识库/SOP/13-民俗节令与禁忌咨询.md`
- `知识库/流派/民俗节令与禁忌.md`
