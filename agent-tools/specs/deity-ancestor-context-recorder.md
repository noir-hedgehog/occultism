# Tool Spec：deity_ancestor_context_recorder

## 作用

记录低风险神明/祖先/供奉/祭拜/还愿请求中的来源传统、对象、场合、意图、已有物件、纪念或供奉动作、家庭边界、安全背景、复盘时间和停止条件。

## 输出

- `tradition_context`
- `focus_entity`
- `occasion`
- `user_intention`
- `existing_items`
- `offering_or_memorial_actions`
- `household_boundaries`
- `safety_context`
- `review_time`
- `stop_condition`
- `missing_fields`

## 边界

- 记录来源和语境，不把私人或地方传统写成普遍命令。
- 保留家庭同意、消防、食品、儿童、宠物和预算边界。
- 风险请求直接返回暂停和安全转译。
