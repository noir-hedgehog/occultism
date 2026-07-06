# Tool Spec：fengshui_school_guard

## 目的

在处理玄空飞星、八宅、三合/三元、择日等风水理气派别请求前，记录派别、方位来源、坐向、时间依据和风险边界。此工具不排飞星盘、不算宅命、不择日，只判断是否能进入方法受限的理气解释，或应退回形法/八卦象征审视。

## 输入

- `request_text` / `space_description`：用户风水请求
- `school`：可选，`xingfa`、`symbolic_bagua`、`xuankong_feixing`、`bazhai`、`sanhe_sanyuan`、`date_selection`
- `facing_direction` / `sitting_direction`：可选
- `direction_source`：可选，例如 `compass`、`floor_plan`、`estimate`
- `build_year` / `move_in_year` / `period` / `external_liqi_chart`：玄空飞星前提
- `occupant_birth_year` / `occupant_mingua`：八宅前提

## 输出

遵循 [fengshui-school-guard.schema.json](../schemas/fengshui-school-guard.schema.json)。

关键字段：

- `detected_schools`
- `requested_school`
- `method_level`
- `required_fields`
- `missing_fields`
- `risk_flags`
- `can_continue_liqi`
- `can_continue_fengshui`
- `reframed_scope`

## 规则

1. 未声明派别、坐向、方位来源或时间依据时，不排盘、不补盘、不下吉凶结论。
2. 不混用玄空、八宅、三合、三元、择日等派别规则。
3. 五黄、二黑、宅命、飞星和方位不能写成发财、破财、生病、婚恋或灾祸保证。
4. 承重、燃气、电路、消防、门锁和结构安全问题优先交给现实专业人员。
5. 字段不足时可退回 `fengshui_observation_recorder`、`fengshui_space_checklist` 和 `fengshui_bagua_mapper` 做低风险审视。

## 命令

```bash
python3 agent-tools/scripts/fengshui_school_guard.py --text "用玄空飞星看厨房五黄是不是会破财生病"
python3 agent-tools/scripts/fengshui_school_guard.py --json '{"request_text":"坐北朝南，罗盘实测，九运房，想用玄空飞星看书房布置","school":"xuankong_feixing","facing_direction":"south","direction_source":"compass","period":"九运"}'
```
