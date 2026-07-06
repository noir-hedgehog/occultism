# Tool Spec：dream_interpretation_planner

## 目的

基于梦境素材记录和主要符号查询结果，生成安全的解梦计划。计划只用于象征反思、情绪整理、创作启发或文化学习，不提供诊断、预言或超自然确认。

## 输入

接受 `dream_record_builder` 的输入字段：

- `dream_text` / `request_text`
- `waking_context`
- `emotions`
- `symbols`
- `user_goal`

## 输出

遵循 [dream-interpretation-planner.schema.json](../schemas/dream-interpretation-planner.schema.json)。

关键字段：

- `can_continue_dream_reflection`
- `symbol_plans`
- `interpretation_layers`
- `synthesis`
- `limits`
- `next_steps`

## 规则

1. 若记录器发现睡眠严重受损、诊断请求或高风险信号，计划器必须暂停解梦。
2. 解读必须先重述素材，再解释符号层，最后落到现实锚点和低风险行动。
3. 不宣称梦境揭示未来、疾病、死亡、灾祸、诅咒或他人真实想法。
4. 最终输出必须使用可能性语言，并运行 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/dream_interpretation_planner.py --text "梦见考试迟到又找不到教室" --context "最近准备面试，担心表现不好"
```
