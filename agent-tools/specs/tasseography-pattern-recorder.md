# Tool Spec：tasseography_pattern_recorder

## 作用

记录茶叶/咖啡渣占卜中的问题、媒介、杯底区域、图案来源、观察到的形状和缺失字段。

## 输出

- `is_valid`
- `medium`
- `cup_zone`
- `pattern_source`
- `observed_shapes`
- `missing_fields`

## 边界

- 只记录用户描述、照片说明或外部来源，不从模糊图像编造确定含义。
- 若请求被 `tasseography_request_guard` 阻断，不继续进入图案解释。
