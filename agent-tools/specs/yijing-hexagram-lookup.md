# Tool Spec：yijing_hexagram_lookup

## 目的

按卦号、卦名、简称或上下卦检索易经 64 卦的结构和现代反思骨架。此工具不提供原典全文，不做确定预测；它用于把 `yijing_hexagram_record` 的计算结果接到可复用的解释素材。

## 输入

- `number`：1-64 的卦序号
- `query` / `name`：卦名、简称或数字字符串
- `lower_trigram` + `upper_trigram`：下卦和上卦名称
- `line`：可选，1-6，用于返回爻位解释层级提示

## 输出

- `number`、`name`、`short_name`
- `lower_trigram`、`upper_trigram`、`bits_bottom_to_top`
- `keywords`、`reflection_prompt`、`action_guidance`
- `line_scope`：可选爻位提示，不含原文爻辞
- `limits`、`next_steps`

## 安全规则

1. 只作为象征结构索引，不作为确定预言。
2. 必须结合用户问题、起卦方法、本卦/变卦和现实处境解释。
3. 医疗、法律、财务、人身安全问题仍走通用安全边界。

## 命令

```bash
python3 agent-tools/scripts/yijing_hexagram_lookup.py --number 1
python3 agent-tools/scripts/yijing_hexagram_lookup.py --query 既济 --line 3
python3 agent-tools/scripts/yijing_hexagram_lookup.py --lower-trigram 离 --upper-trigram 坎
```
