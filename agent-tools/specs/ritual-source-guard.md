# Tool Spec：ritual_source_guard

## 目的

对民俗仪式、驱邪、净化、护身等资料做来源分级和安全转译。此工具不验证超自然真实性，只判断资料应如何标注、能否作为文化背景、能否提供步骤，以及如何改写成低风险象征性支持。

## 输入

- `request_text` / `source_text`：用户请求或资料片段
- `source_type`：可选，`regional_folk`、`religious_tradition`、`modern_wellness`、`commercial_new_age`、`personal_preference`、`unknown`

## 输出

- `source_type`、`source_claim_level`
- `missing_source_fields`
- `certainty_flags`
- `safety_result`：内嵌 `ritual_safety_check` 结果
- `can_use_as_cultural_context`
- `can_offer_steps`
- `required_framing`、`prohibited_framing`
- `safe_symbolic_protocol`

## 规则

1. 地域民俗、宗教传统、商业新灵性和个人经验必须分开标注。
2. 缺少地区、传承、出处或上下文时，只能写成“未验证说法/文化材料”，不能写成普遍传统。
3. 含火、烟、血、刀具、摄入、密闭燃烧、操控他人时，不提供原步骤。
4. 不能确认鬼、诅咒、附身、必然灾祸或保证效果。
5. 输出草稿仍需经过 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/ritual_source_guard.py --text "老人说搬家后点蜡烛烧纸能驱邪" --source-type regional_folk
```
