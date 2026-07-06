# Tool Spec：qimen_method_guard

## 目的

在生成或解释奇门遁甲盘之前，记录并校验排盘方法假设。此工具不排盘，只判断是否具备后续调用排盘器的前提，避免混用置闰、拆补、飞盘、转盘、真太阳时和节气来源。

## 输入

- `chart_method` / `method`：`time_chart`、`event_chart`、`manual_external_chart`
- `school`：`zhirun`、`chaibu`、`maoshan`、`feipan`、`turning_plate`
- `chart_time`、`timezone`、`location`
- `solar_time_strategy`：`not_applied`、`true_solar_time`、`local_mean_time`、`unknown`
- `solar_term_source`：`manual`、`external_calendar`、`future_tool_generated`
- `dun`、`ju`：可选，若用户已经提供

## 输出

- `can_generate_chart`
- `is_external_chart_only`
- `errors`、`warnings`、`assumptions`
- `required_before_generation`
- `limits`、`next_steps`

## 安全规则

1. 没有声明派别和节气来源时，不生成盘。
2. 外部盘只记录来源和假设，不重新生成宫位。
3. 不清楚真太阳时策略时，必须标记方法限制。
4. 最终解释仍需通过 `qimen_chart_record` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/qimen_method_guard.py --json '{"method":"time_chart","school":"zhirun","chart_time":"2026-06-30 15:00","timezone":"Asia/Shanghai","location":"Shanghai","solar_time_strategy":"true_solar_time","solar_term_source":"external_calendar"}'
```
