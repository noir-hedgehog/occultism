# Tool Spec：mingli_school_reference

## 目的

查询八字和紫微斗数的派别、传承标签和综合口径差异，帮助 agent 在排盘或解释前说明方法边界。此工具不生成命盘、不补造干支、宫位、星曜或四化字段，只说明子平、传统八字、现代综合、三合、四化、中州等标签会影响哪些字段、需要哪些前提、哪些口径不能混用。

## 输入

- `query`：自然语言查询，如 `子平和紫微三合能混着看事业吗`
- `system`：`bazi` 或 `ziwei`，用于只知道系统但未声明具体派别时
- `school`：单个派别或口径标签
- `schools`：多个派别或口径标签
- `question_text` / `request_text` / `focus`：可选，用于风险标记

## 输出

遵循 [mingli-school-reference.schema.json](../schemas/mingli-school-reference.schema.json)。

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

1. 只说明八字/紫微派别差异，不生成命盘。
2. 子平、传统八字、现代综合会影响十神、格局、旺衰、调候和解释语言的权重。
3. 紫微三合、四化、中州和现代综合会影响宫位、星曜、四化、飞化路径和资料来源要求。
4. 八字和紫微斗数属于不同系统；可以并列比较主题倾向，不能混成一张盘或一个断法。
5. 传统、古法、中州等标签需要来源说明，不凭名称推断完整算法。
6. 派别差异不支持富贵、婚恋、寿命、疾病、财富、灾祸或重大决策确定断语。

## 命令

```bash
python3 agent-tools/scripts/mingli_school_reference.py --query "子平和紫微三合能混着看事业吗"
python3 agent-tools/scripts/mingli_school_reference.py --schools 三合 四化
```

## 与 Skill 的关系

`mingli-bazi-ziwei-consultation` 在用户询问派别差异、方法混用、子平/三合/四化/中州等口径，或只给宽泛派别标签时，应先调用本工具，再调用 `bazi_ziwei_intake_guard` 和 `bazi_ziwei_chart_record`。若用户已有外部命盘，仍用 `bazi_ziwei_chart_record` 记录来源和字段；最终答复必须通过 `mystic_output_lint`。
