# Tool Spec：cartomancy_draw_recorder

## 作用

记录扑克牌占卜中的问题、牌阵、牌组类型、抽牌来源、牌面和缺失字段。

## 输出

- `is_valid`
- `deck_type`
- `spread_type`
- `draw_source`
- `cards`
- `missing_fields`

## 边界

- 只记录用户提供、模拟同意或外部应用牌面，不自动补造缺失牌。
- 若请求被 `cartomancy_request_guard` 阻断，不继续进入牌面解释。
