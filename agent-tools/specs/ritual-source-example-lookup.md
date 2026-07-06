# Tool Spec：ritual_source_example_lookup

## 目的

查询民俗仪式来源分类样例，帮助 agent 判断资料应如何标注、缺哪些上下文、能否作为文化背景、不能如何表述。此工具提供分类模板和安全写法，不提供真实地区民俗断言。

## 输入

- `source_type`：可选，`regional_folk`、`religious_tradition`、`modern_wellness`、`commercial_new_age`、`personal_preference`、`unknown`
- `request_text` / `source_text`：可选，资料片段；工具会自动推断来源类型

## 输出

- `source_type`
- `classification_cues`
- `required_context`
- `safe_use`
- `not_allowed`
- `example_records`
- `guard_summary`

## 规则

1. 样例只用于分类和写法训练，不应当作真实民俗资料来源。
2. 若需要真实地区/宗教材料，必须另行记录来源、地区、语境和可复述范围。
3. 输出应继续交给 `ritual_source_guard` 和 `ritual_low_risk_protocol`。

## 命令

```bash
python3 agent-tools/scripts/ritual_source_example_lookup.py --source-type religious_tradition
python3 agent-tools/scripts/ritual_source_example_lookup.py --text "某课程说买水晶阵能保证转运"
```
