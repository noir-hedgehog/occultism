# Tool Spec：tarot_combination_planner

## 目的

在 `tarot_draw_recorder` 与 `tarot_interpretation_planner` 之后，专门分析多张牌之间的组合关系，帮助 agent 稳定处理逆位聚集、大牌权重、花色重复/缺席、宫廷牌聚集和牌位之间的叙事链接。

它不输出确定预测，只生成可审计的组合解读骨架。

## 输入

沿用 `tarot_draw_recorder` 的输入：

- `question_text`
- `spread_id`
- `positions`：自定义牌阵可选
- `cards`：每项包含 `card`、`orientation`、可选 `position` 和 `note`

## 输出

- `normalized_cards`：规范牌名、牌位、正逆位、大小牌、花色和关键词
- `combination_patterns`：组合模式、证据、安全说法和禁用说法
- `position_links`：相邻牌位之间的桥接关系和解读提示
- `synthesis_prompt`：组合解读顺序、开场提示和收束问题
- `risk_flags`、`limits` 与 `next_steps`

## 规则

1. 先复用 `tarot_draw_recorder` 校验牌阵和牌名，不合法时不继续组合解读。
2. 每张牌复用 `tarot_card_lookup` 的牌义素材，不临场扩写牌库。
3. 两张以上逆位且达到半数时标记 `reversal_cluster`。
4. 大牌达到两张且达到半数时标记 `major_arcana_weight`。
5. 花色重复只作为主题醒目，不作为唯一原因；缺席花色只作为补充提问方向。
6. 宫廷牌不得直接等同现实中的某个具体人物。
7. 操控/危机请求阻断组合解读；医疗、法律、财务等高风险主题只允许反思性语言并回到专业支持。

## 命令

```bash
python3 agent-tools/scripts/tarot_combination_planner.py --json '{"question_text":"我当前工作状态的组合倾向是什么？","spread_id":"three_card_situation","cards":[{"card":"愚者","orientation":"upright"},{"card":"宝剑三","orientation":"reversed"},{"card":"星币国王","orientation":"reversed"}]}'
```
