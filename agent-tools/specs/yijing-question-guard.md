# Tool Spec：yijing_question_guard

## 目的

检查易经卦爻类占问是否适合进入起卦流程，并把问题改写为“一事一问、非决定论、可行动”的形式。

这个工具不负责起卦、排卦、解卦；它只负责问题守门。

## 输入

```bash
python3 agent-tools/scripts/yijing_question_guard.py --text "我该不该跳槽？"
```

也可传入 JSON：

```json
{
  "question_text": "我该不该跳槽？",
  "previous_questions": ["我该不该跳槽？"]
}
```

## 输出

遵循 [yijing-question-guard.schema.json](../schemas/yijing-question-guard.schema.json)。

## 规则

- 一事一问：复合问题需要拆分。
- 不反复占问：同一问题只有在事实或行动选择发生变化后才适合重新占问。
- 高风险分流：医疗、法律、财务、危机和操控他人的请求不得直接进入占问。
- 改写方向：从“会不会/一定吗”改为“当前变化结构、阻碍、下一步”。
