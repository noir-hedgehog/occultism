# Tool Spec：consultation_packet_builder

## 目的

把一个用户请求整理成“人和 Agent 都能读”的咨询工作单。它合并 `agent_workflow_router`、`paradigm_selector`、上下文文档、工具链、Agent brief 和复核清单，作为 Web UI、命令行和未来 runtime wrapper 的共同契约。

这个工具不直接生成玄学结论，也不执行任意 shell 命令；它只做流程组织、边界说明和交接。

## 输入

- `request_text`：用户请求文本。
- `requested_domain`：可选，用户指定的流派。
- `root`：仓库根目录，默认当前目录。

## 输出

遵循 [consultation-packet-builder.schema.json](../schemas/consultation-packet-builder.schema.json)。

关键字段：

- `session`：流派、意图、风险、路由状态和澄清点。
- `paradigm`：主干、问题类型、推荐范式、证据轨道和执行边界。
- `context_docs`：Skill、SOP、知识卡、主干与范式文档。
- `workflow_steps`：从 intake 到 lint/review 的执行步骤。
- `tool_chain`：可直接运行、需结构化输入或需草稿输出的工具命令。
- `agent_brief`：Agent 执行指令、复核清单和交接摘要。

## 执行状态

- `runnable_now`：当前请求文本足够运行。
- `requires_structured_input`：需要 UI、Agent 或用户补齐专门字段。
- `requires_draft_output`：需要先生成草稿，再执行输出安全检查。

## 命令

```bash
python3 agent-tools/scripts/consultation_packet_builder.py --text "帮我做一个塔罗三张牌，看看工作状态"
```
