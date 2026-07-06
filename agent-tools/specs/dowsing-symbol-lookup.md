# Tool Spec：dowsing_symbol_lookup

## 目的

查询占杖/寻水杖中的常见动作、地图记录和空间位置象征，把它们转成暂停、方向、边界、分区、动线和现实核查提示。

## 输入

- `query`、`symbol` 或 `movement`
- `focus` 可选

## 输出

- `canonical_name`
- `symbol_code`
- `symbol_layer`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `action_guidance`
- `prohibited_uses`

## 安全边界

- 只提供象征提示，不解释成地下管线、水源、矿脉、疾病、灵体、事实位置、专业探测或资源定位。
