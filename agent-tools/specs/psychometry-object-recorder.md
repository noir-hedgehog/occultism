# Tool Spec：psychometry_object_recorder

## 作用

记录获授权物件的低风险咨询上下文，包括物件类型、来源备注、拥有/同意状态、可见特征、第一联想、情绪、现实锚点和反思焦点。

## 输出

- `object_types`
- `source_notes`
- `ownership_status`
- `visible_features`
- `impressions`
- `emotions`
- `reality_anchor`
- `missing_fields`
- `can_continue_psychometry`

## 边界

- 未经同意、第三方隐私、失踪犯罪、灵体事实或专业替代请求不进入有效记录。
- 缺少物件类型、拥有/授权状态或特征/联想/情绪时标记缺失字段。
