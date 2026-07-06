# Tool Spec：lost_object_search_planner

## 作用

组合失物语境记录和搜索线索查询，生成最后接触记录、路径复盘、区域分层、联系渠道、复盘时间和停止条件的低风险寻物计划。

## 输入

同 `lost_object_context_recorder`。

## 输出

- `symbol_plans`
- `search_plan`
- `limits`
- `next_steps`

## 边界

- 不保证准确方位或一定找到。
- 不替代报警、物业、客服、学校、医院、交通失物招领或家人协助。
- 不处理寻人、走失宠物急症、犯罪定责、隐私定位、跟踪或监视。
- 必须包含可执行行动、复盘时间和停止条件。
