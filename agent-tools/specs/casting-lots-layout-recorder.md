# Tool Spec：casting_lots_layout_recorder

## 作用

记录一次低风险骨、贝壳、石子、符物/小物抛掷咨询的盘面信息，包括体系、投掷垫/区域、来源、物件、方位和关系。

## 输入

- `question_text` / `request_text` / `text`
- `casting_system`
- `casting_surface`
- `layout_source`
- `objects` / `items`
- `zones`
- `relationships` / `layout_notes`
- `focus`

## 输出

- `can_continue_casting_lots`
- `objects`
- `zones`
- `relationships`
- `missing_fields`
- `safety_notes`
- `next_steps`

## 边界

- 缺少物件、区域或关系时只标注缺失，不编造盘面。
- 若守门器发现风险，记录器必须暂停后续解释。
