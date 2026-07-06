# Tool Spec：dream_record_builder

## 目的

把用户的梦境叙述整理成可审计的梦境素材记录：梦境片段、醒后情绪、主要符号、现实背景、风险信号和澄清问题。此工具不解释梦，也不把梦当成诊断或预兆。

## 输入

- `dream_text` / `request_text`：梦境或请求原文
- `waking_context`：可选，最近现实背景
- `emotions`：可选，用户明确给出的醒后情绪
- `symbols`：可选，用户明确指出的梦境符号
- `user_goal`：可选，`symbolic_reflection`、`cultural_learning`、`creative_prompt` 等

## 输出

遵循 [dream-record-builder.schema.json](../schemas/dream-record-builder.schema.json)。

关键字段：

- `can_continue_dream_reflection`
- `emotion_labels`
- `symbol_candidates`
- `risk_flags`
- `missing_fields`
- `clarifying_questions`

## 规则

1. 反复噩梦、严重失眠、创伤困扰或诊断请求应暂停解梦，优先建议现实支持。
2. 不补写用户没说的梦境细节。
3. 不把梦写成死亡、灾祸、疾病、诅咒或他人真实意图的证据。
4. 最终解读前必须再运行 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/dream_record_builder.py --text "梦见在海边被浪追着跑" --context "最近工作交付压力很大"
```
