# Tool Spec：cezi_character_recorder

## 作用

记录一次低风险测字/拆字咨询的字例信息，包括问题、字、字例来源、部件/结构、可见特征、用户联想和缺失字段。

## 输入

- `question_text` / `request_text` / `text`
- `character` / `zi` / `word`
- `character_source`
- `components` / `radicals`
- `visible_features` / `features`
- `user_association` / `association`
- `focus`

## 输出

- `can_continue_cezi`
- `character`
- `character_source`
- `components`
- `visible_features`
- `user_association`
- `missing_fields`
- `safety_notes`

## 边界

- 缺少字例、部件或用户联想时只标注缺失，不编造字源或权威拆解。
- 若守门器发现风险，记录器必须暂停后续解释。
