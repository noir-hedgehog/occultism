# Tool Spec：qimen_chart_record

## 目的

记录并校验奇门遁甲盘式字段，包括起局时间、地点、阴阳遁、局数、值符/值使、日干/时干、用神和九宫信息。

这个工具不负责排盘或解盘；它只把用户或外部排盘工具提供的盘式转成可复盘结构。

## 输入

```bash
python3 agent-tools/scripts/qimen_chart_record.py --json '{"question_text":"这个项目下一步怎么推进？","chart_time":"2026-06-30T21:00:00+08:00","timezone":"Asia/Shanghai","location":"Shanghai","dun":"阳遁","ju":3,"palaces":[{"palace":1,"trigram":"坎","earth_stem":"戊","heaven_stem":"乙","door":"休门","star":"天蓬","deity":"值符"}]}'
```

## 输出

遵循 [qimen-chart-record.schema.json](../schemas/qimen-chart-record.schema.json)。

## 校验规则

- 宫位必须是 1-9。
- 九宫不完整时输出 warning，不直接判为 invalid。
- 重复宫位、非法天干、非法门/星/神、非法局数会使 `is_valid` 为 `false`。
- 线下或外部排盘来源应写入 `method`。

## 边界

- 不确定派别、真太阳时、拆补/置闰等规则时，必须记录为方法限制。
- 不把奇门输出作为医疗、法律、财务或安全决策替代。

