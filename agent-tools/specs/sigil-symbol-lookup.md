# Tool Spec：sigil_symbol_lookup

## 目的

查询 sigil/符号印记中的常见形状、图像母题和低风险使用方式，把它们转成边界、方向、聚焦、许可、开始、复盘和现实行动提示。

## 输入

- `query`、`symbol` 或 `element`
- `focus` 可选

## 输出

- `canonical_name`
- `symbol_code`
- `category`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `action_guidance`
- `prohibited_uses`

## 安全边界

- 只提供象征提示，不解释成召唤、封印、驱邪、诅咒、操控、显化保证、纹身建议或专业意见。
