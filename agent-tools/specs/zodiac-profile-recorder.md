# Tool Spec：zodiac_profile_recorder

## 作用

记录生肖/太岁咨询中的年份、生肖、关注主题、本人或第三方范围、来源说明和缺失字段。

## 输出

- `birth_year`
- `zodiac`
- `focus`
- `subject_scope`
- `source_note`
- `missing_fields`
- `risk_flags`

## 边界

- 第三方资料必须限制为概括性沟通反思，不能贴人品、命运、健康或婚恋标签。
- 来源不明时必须标注为来源受限说法。
