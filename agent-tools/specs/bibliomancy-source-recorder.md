# Tool Spec：bibliomancy_source_recorder

## 作用

记录书占来源和短摘录上下文，包括书名/来源、来源类型、抽取方式、页码/位置、用户自提供短句、关键词、情绪、现实锚点和反思焦点。

## 输出

- `source_title`
- `source_type`
- `selection_method`
- `page_or_location`
- `excerpt`
- `keywords`
- `emotions`
- `missing_fields`
- `can_continue_bibliomancy`

## 边界

- 不补写用户未提供的原文。
- 摘录过长时标记 `excerpt_too_long_for_bibliomancy_record` 并暂停有效记录。
- 专业替代、第三方隐私、经文权威命令、长段版权文本或反复依赖请求不进入有效记录。
