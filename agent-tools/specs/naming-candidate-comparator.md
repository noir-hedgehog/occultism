# Tool Spec：naming_candidate_comparator

## 目标

把多个中文候选名整理成安全、可比较的候选名字表。工具只评估文化象征和现实使用成本，不做财富、婚恋、健康、寿命、学业或转运判断。

## 输入

- `request_text`：用户原始请求。
- `name_type`：`formal_name`、`nickname`、`stage_name`、`pen_name`、`brand_name` 或中文别名。
- `candidates`：候选名数组，或用顿号/逗号/空格分隔的字符串。
- `surname`：正式人名可选姓氏。
- `priorities`：用户主要关注维度，如字义、字音、谐音、五行、品牌传播。
- `desired_elements`：可选五行民俗偏好，只作象征参考。
- `avoid_characters`：用户明确避开的字。
- `subject_is_minor`：是否涉及未成年人。

## 输出

- `can_compare_names`：是否可以继续做候选比较。
- `evaluations`：每个候选的字义、字音、字形、文化避讳和现实使用分数。
- `ranked_candidates`：按粗筛分数排序的候选名。
- `risk_flags`：宿命论、未成年人标签、注册承诺或第三方隐私风险。
- `warnings` / `limits`：非决定论、专业边界和品牌检索提醒。

## 安全边界

- 不承诺“旺财、旺夫、改名转运、补命、避灾”。
- 不替代法律登记、商标检索、品牌调研、医疗、心理或财务建议。
- 涉及未成年人时只谈使用体验、家庭偏好和文化联想，不贴固定人格标签。
- 品牌名只给传播和可用性粗筛，不承诺可注册、可商用或不侵权。

## 示例

```bash
python3 agent-tools/scripts/naming_candidate_comparator.py --json '{"request_text":"想比较沐安、清宁哪个更适合宝宝名","name_type":"formal_name","surname":"林","candidates":["沐安","清宁"],"priorities":["字义","读音"],"desired_elements":["water"],"subject_is_minor":true}'
python3 agent-tools/scripts/naming_candidate_comparator.py --text "比较品牌名星禾、清朗哪个更好" --name-type brand_name --priorities "读音、传播、谐音"
```
