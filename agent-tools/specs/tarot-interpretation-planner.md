# Tool Spec：tarot_interpretation_planner

## 目的

把已经选择好的牌阵和抽牌记录转成结构化解读计划，帮助 agent 稳定处理牌位、单牌、正逆位、牌间互动和现实行动。此工具不替用户做确定预测，只生成可审计的解读骨架。

## 输入

沿用 `tarot_draw_recorder` 的输入：

- `question_text`
- `spread_id`
- `positions`：自定义牌阵可选
- `cards`：每项包含 `card`、`orientation`、可选 `position` 和 `note`

## 输出

- `card_plans`：每张牌的牌位镜头、牌义关键词、反思问题、行动提示
- `patterns`：大牌数量、正逆位数量、花色重复和重点模式
- `reversal_strategy`：本次逆位应如何处理
- `synthesis`：主题、张力点、可落地行动和收束问题
- `limits` 与 `next_steps`

## 规则

1. 先调用 `tarot_draw_recorder`，牌数、牌名或正逆位不合法时不继续解读。
2. 每张牌用 `tarot_card_lookup` 取牌义，避免临场编造。
3. 逆位不默认等于坏结果；可读作阻滞、内化、过度、延迟或提醒。
4. 关系牌位中的“对方可能状态”必须使用可能性语言。
5. 输出草稿仍需经过 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/tarot_interpretation_planner.py --json '{"question_text":"我当前工作局势如何？","spread_id":"three_card_situation","cards":[{"card":"愚者","orientation":"upright"},{"card":"宝剑三","orientation":"reversed"},{"card":"星币国王","orientation":"upright"}]}'
```
