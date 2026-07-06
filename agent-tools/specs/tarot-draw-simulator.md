# Tool Spec：tarot_draw_simulator

## 目的

当用户没有实体塔罗牌或希望 agent 随机抽牌时，生成可复现、可审计、可继续交给 `tarot_draw_recorder` 与 `tarot_card_lookup` 的模拟抽牌结果。

## 输入

- `spread_id`：已有牌阵，如 `single_focus`、`three_card_situation`、`two_paths`
- `question_text`：可选，用户问题
- `seed`：可选；提供后同一输入会得到同一抽牌
- `orientation_mode`：`upright_only`、`mixed` 或 `reversed_allowed`
- `reversal_probability`：逆位概率，0-1
- `positions` / `card_count`：自定义牌阵时使用

## 输出

- `cards`：牌名、正逆位、牌位
- `recorded_draw`：由 `tarot_draw_recorder` 校验后的结构
- `seed`、`seed_generated`、`deck_size`
- `limits`、`next_steps`

## 安全规则

1. 模拟抽牌只是随机化辅助，不是命运证据。
2. 高风险问题仍需先走 `mystic_intake_triage` 和 `tarot_spread_selector`。
3. 最终解读必须经 `mystic_output_lint` 或人工等价规则检查。

## 命令

```bash
python3 agent-tools/scripts/tarot_draw_simulator.py --spread-id three_card_situation --seed demo --orientation-mode mixed
```
