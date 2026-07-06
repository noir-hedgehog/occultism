---
name: naming-symbolic-consultation
description: Use when a user asks Codex for Chinese naming, 姓名学, 取名, 起名, 改名, 宝宝名, 小名, 艺名, 笔名, 品牌名, 店名, 商号, 品牌名评分, 候选名字比较, 字义, 字音, 字形, 五行取名, 生肖避讳, 谐音避讳, or safe non-deterministic name symbolism and usage-context consultation.
---

# Naming Symbolic Consultation

Use this skill for safe Chinese naming and name-reflection consultation. Treat names as cultural symbols and real-world usage artifacts, not as deterministic fate, health, wealth, relationship or disaster predictors.

## Workflow

1. Run `mystic_intake_triage.py`, using `--domain naming` when the request is clearly about names.
2. Pause or reframe professional-risk, crisis, coercive, fatalistic, privacy or minor-labeling requests before any name interpretation.
3. Confirm the name type: formal name, nickname, stage name, pen name, brand name or another use case.
4. Ask for the candidate name, surname if relevant, desired tone, avoided characters, dialect or regional concerns and the user's main decision criterion.
5. Use `naming_symbol_lookup` for dimensions such as 字义, 字音, 字形, 五行意象, 生肖避讳, 用字避讳, 场景匹配, 谐音 or 生僻字.
6. When the user provides one or more candidate names and wants comparison, run `naming_candidate_comparator` to build a candidate table before writing recommendations.
7. For brand names, shop names, or commercial names, run `naming_brand_scenario_scorer` when category, audience, tone, channels and candidates are available; never claim registration, uniqueness, legal clearance or commercial success.
8. Interpret in two layers: cultural-symbolic associations and observable usage costs.
9. For minors, avoid fixed personality or destiny labels; for brands, remind the user to do trademark, domain, platform and competitor checks.
10. Draft the answer, then run or mentally apply `mystic_output_lint`.
11. End with non-determinism, professional-advice and registration/search limits.

## Tool Hooks

Run general intake:

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "<user request>" --domain naming
```

Lookup naming dimensions:

```bash
python3 agent-tools/scripts/naming_symbol_lookup.py --query 字义 --category dimension --focus baby_name
python3 agent-tools/scripts/naming_symbol_lookup.py --query 木 --category element --focus name_tone
python3 agent-tools/scripts/naming_symbol_lookup.py --query 谐音 --category cultural_check --focus brand_name
```

Compare candidate names:

```bash
python3 agent-tools/scripts/naming_candidate_comparator.py --json '{"request_text":"想比较沐安、清宁哪个更适合宝宝名","name_type":"formal_name","surname":"林","candidates":["沐安","清宁"],"priorities":["字义","读音"],"desired_elements":["water"],"subject_is_minor":true}'
```

Score brand-name scenario fit:

```bash
python3 agent-tools/scripts/naming_brand_scenario_scorer.py --json '{"request_text":"给茶饮品牌比较星禾和清朗","candidates":["星禾","清朗"],"category":"茶饮","audience":"年轻上班族","tone":["清爽","年轻"],"channels":["门头","小红书","搜索","域名"]}'
```

Lint the final draft before sending:

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "<draft answer>"
```

## Output Shape

```text
安全分级：
使用场景与目标：
候选名字：
维度检查：
候选比较表：
品牌场景评分：
文化象征层：
现实使用层：
可保留点：
需谨慎点：
调整方向：
限制与提醒：
```

## References

- `知识库/SOP/12-姓名学命名咨询.md`
- `知识库/流派/姓名学.md`
