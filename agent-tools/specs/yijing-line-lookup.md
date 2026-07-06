# Tool Spec：yijing_line_lookup

## 目的

为易经卦爻解读提供 64 卦 × 6 爻的动爻索引。此工具不提供原文爻辞或传统注疏，而是给出爻位、阴阳、位置匹配、变卦和现代解释骨架，避免 agent 在“动爻层”临场编造。

## 输入

- `number` / `hexagram_number`：1-64
- `query` / `hexagram` / `name`：卦名、简称
- `line`：1-6，必填

## 输出

- `hexagram`：本卦摘要
- `line_label`、`line_stage`、`line_focus`
- `line_nature`、`position_nature`、`fit_note`
- `changing_to`：该爻变动后的变卦
- `interpretation_scaffold`：提问、行动、变化方向和本卦/动爻/变卦比较提示
- `source_level`、`limits`、`next_steps`

## 规则

1. 只接受 1-6 爻。
2. 变卦由本卦 `bits_bottom_to_top` 中对应爻位翻转得到。
3. 输出必须标明 `modern_line_index_not_classical_text`，不能冒充原文爻辞。
4. 最终解读仍需结合 `yijing_question_guard`、`yijing_hexagram_record` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/yijing_line_lookup.py --number 1 --line 1
python3 agent-tools/scripts/yijing_line_lookup.py --query 既济 --line 3
```
