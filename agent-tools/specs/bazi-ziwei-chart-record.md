# Tool Spec：bazi_ziwei_chart_record

## 目的

记录八字、四柱、紫微斗数排盘前的参数与方法假设。此工具不排盘、不计算干支、星曜或宫位，只保证后续排盘或人工录入时有可审计的出生资料、历法、时区、真太阳时策略、派别和资料来源。

## 输入

- `system`：`bazi` 或 `ziwei`
- `birth_date`、`birth_time`、`birth_place`
- `calendar_type`：`solar` / `lunar`
- `timezone`
- `solar_time_strategy`：`not_applied`、`true_solar_time`、`local_mean_time`、`unknown`
- `school`：八字或紫微的派别/方法标签
- `chart_source`：人工提供、外部排盘器、未来工具生成或文化解释
- `analysis_focus`
- `subject_is_self`、`subject_consent`、`subject_is_minor`

## 输出

- `birth_data`
- `method`
- `privacy_flags`
- `is_valid`
- `errors`、`warnings`、`assumptions`
- `required_before_interpretation`
- `limits`、`next_steps`

## 安全规则

1. 第三方资料必须有同意。
2. 不记录身份证、手机号、住址、完整真实姓名等直接身份字段。
3. 未成年人只允许支持性、非标签化解释。
4. 未确认历法、时区、真太阳时策略时，不得声称精确排盘。
5. 本工具只记录参数，不输出命运断言。

## 命令

```bash
python3 agent-tools/scripts/bazi_ziwei_chart_record.py --json '{"system":"bazi","birth_date":"1990-05-01","birth_time":"08:30","birth_place":"北京","calendar_type":"solar","timezone":"Asia/Shanghai","solar_time_strategy":"not_applied","school":"ziping","chart_source":"external_calculator","analysis_focus":"career","subject_is_self":true}'
```
