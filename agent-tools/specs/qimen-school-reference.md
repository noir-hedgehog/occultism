# Tool Spec：qimen_school_reference

## 目的

查询奇门遁甲派别和盘式约定差异，帮助 agent 在排盘或解释前说明方法边界。此工具不生成奇门盘、不补造宫位，只说明置闰、拆补、茅山、飞盘、转盘等标签会影响哪些字段、需要哪些前提、哪些口径不能混用。

## 输入

- `query`：自然语言查询，如 `置闰和拆补有什么区别`、`飞盘 vs 转盘`
- `school`：单个派别或盘式标签
- `schools`：多个派别或盘式标签
- `question_text` / `request_text` / `focus`：可选，用于风险标记

## 输出

遵循 [qimen-school-reference.schema.json](../schemas/qimen-school-reference.schema.json)。

关键字段：

- `comparison_mode`
- `schools`
- `school_profiles`
- `conflict_points`
- `required_method_fields`
- `risk_flags`
- `warnings`
- `safe_usage`

## 规则

1. 只说明派别和盘式约定，不生成盘式。
2. 置闰/拆补属于节气边界和局数口径差异；飞盘/转盘属于盘式布列约定差异。
3. 比较有冲突的口径时，必须分盘并列，不能把不同口径字段混成一个结论。
4. 茅山等传承标签必须记录资料来源，不凭名称推断完整算法。
5. 派别差异不支持必成、必败、疾病、财富、婚恋或灾祸确定断语。

## 命令

```bash
python3 agent-tools/scripts/qimen_school_reference.py --query "置闰和拆补有什么区别"
python3 agent-tools/scripts/qimen_school_reference.py --schools 飞盘 转盘
```

## 与 Skill 的关系

`qimen-chart-consultation` 在用户询问派别差异、方法前提不清、或同时提到置闰/拆补、飞盘/转盘时，应先调用本工具，再调用 `qimen_method_guard`。若用户已有外部盘，仍用 `qimen_chart_record` 记录来源和字段；最终答复必须通过 `mystic_output_lint`。
