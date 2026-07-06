# Tool Spec：lost_object_symbol_lookup

## 作用

查询失物/寻物场景中的最后看见、路线回溯、门口/玄关、口袋/包、桌面/抽屉、交通/座位、联系渠道和复盘停止等低风险搜索线索。

## 输入

- `query` / `symbol`
- `focus`

## 输出

- `canonical_name`
- `symbol_code`
- `category`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `action_guidance`
- `prohibited_uses`

## 边界

- 符号只用于组织搜索线索，不承诺定位、找回或灵验。
- 不输出嫌疑人、他人位置、犯罪事实、寻人方向或隐私追踪。
