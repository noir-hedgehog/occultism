# Tool Spec：body_omen_reflection_planner

## 目的

组合身体征兆语境和象征查询，生成低风险身体照料、现实核查和民俗象征反思计划。

## 输入

- `question_text`、`request_text` 或 `text`
- 可选：`omen_type`、`body_location`、`timing`、`duration`、`sensation_notes`、`health_context`、`mundane_context`、`focus`、`reality_constraints`、`stop_condition`

## 输出

- `can_continue_body_omen`
- `symbol_plans`
- `reflection_plan`
- `limits`
- `next_steps`

## 安全边界

- 不生成诊断、治疗、用药、灾祸预言、彩票投资、第三方标签、驱邪或危险身体试验建议。
- 若请求含医疗红旗或反复依赖，暂停身体征兆象征咨询并转向现实支持。
