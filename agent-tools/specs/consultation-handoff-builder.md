# Tool Spec：consultation_handoff_builder

## 目的

把咨询工作单、结构化工具预览、可选草稿和输出安全检查合并成 Agent/审校者可接管的交接包。

它位于 Web UI 结构化输入之后、Agent 生成最终回答之前，用于回答“现在能不能交给 Agent 综合？还缺哪些字段？草稿是否被安全 lint 阻断？”。

## 输入

- `request_text`：用户原始请求。
- `requested_domain`：可选，用户指定流派。
- `preview_result`：可选，来自 `/api/tool-preview` 或可信白名单工具的结构化结果。
- `draft_output`：可选，Agent 草稿；提供后会运行 `mystic_output_lint`。
- `root`：仓库根目录，默认当前目录。

## 输出

遵循 [consultation-handoff-builder.schema.json](../schemas/consultation-handoff-builder.schema.json)。

关键字段：

- `handoff_status`：是否暂停、缺结构化结果、可交给 Agent、可进入审校、需要改写或被 lint 阻断。
- `packet`：由 `consultation_packet_builder` 生成的咨询工作单。
- `preview`：结构化工具结果摘要。
- `input_status`：仍需补齐的结构化工具。
- `lint_result`：可选草稿的安全措辞检查结果。
- `agent_resume_prompt`：给 Agent 接管时使用的操作提示。
- `review_checklist`：给人类审校者看的复核清单。

## 命令

```bash
python3 agent-tools/scripts/consultation_handoff_builder.py --text "帮我做一个塔罗三张牌，看看工作状态"
```
