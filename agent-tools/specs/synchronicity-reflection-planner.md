# Tool Spec：synchronicity_reflection_planner

## 作用

组合同步性事件记录和符号查询，生成非命令化、非预测、非专业替代、非读心的低风险记录与行动反思计划。

## 输出

- `is_valid`
- `can_continue_synchronicity`
- `symbol_plans`
- `reflection_plan`
- `limits`
- `next_steps`

## 边界

- 未知符号只作为私人联想，不编造来源、神谕、灵体事实或命令。
- 计划必须包含现实行动和停止条件。
- 若出现危险寻找、财务/职业/医疗/法律替代、第三方读心或反复确认风险，返回暂停计划。
