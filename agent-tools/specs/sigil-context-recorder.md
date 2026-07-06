# Tool Spec：sigil_context_recorder

## 目的

记录低风险 sigil、符号印记、魔法阵或 seal 象征咨询所需的意图、图形元素、来源、媒介、展示位置、安全背景和现实约束。

## 输入

- `question_text`、`request_text` 或 `text`
- `intention_text`
- `symbol_elements`
- `source_context`
- `medium`
- `activation_mode`
- `display_location`
- `duration`
- `focus`
- `safety_context`
- `reality_constraints`

## 输出

- `can_continue_sigil`
- `intention_text`
- `symbol_elements`
- `source_context`
- `medium`
- `activation_mode`
- `display_location`
- `duration`
- `missing_fields`
- `risk_flags`

## 安全边界

- 记录不等于批准危险做法；若文本包含血、身体伤害、火、召唤、诅咒、操控、永久纹身、专业替代或依赖风险，必须暂停。
