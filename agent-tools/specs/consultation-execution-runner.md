# Tool Spec：consultation_execution_runner

## 目的

执行一次咨询工作单中可安全自动运行的子集，并明确标出剩余哪些步骤需要结构化输入、Agent 草稿或人工/Agent 接管。

它把“程序化自动运行的部分”和“需要 Agent 接入的部分”拆开，避免 Web UI 只显示命令但不运行，也避免本地 API 执行任意 shell 或误跑需要上下文的领域工具。

## 输入

- `request_text`：用户原始请求。
- `requested_domain`：可选，用户指定流派。
- `root`：仓库根目录，默认当前目录。

## 安全执行白名单

- `consultation_packet_builder`
- `paradigm_selector`
- `mystic_intake_triage`

其余工具只在输出中标记为 skipped，说明需要 UI 结构化输入、Agent 草稿、输出 lint 或安全暂停。

## 输出

遵循 [consultation-execution-runner.schema.json](../schemas/consultation-execution-runner.schema.json)。

关键字段：

- `run_status`：安全子集是否执行完成，是否需要 Agent handoff，或是否因安全/专业边界暂停。
- `execution_summary`：工具链总数、已执行数、跳过数、结构化输入数、草稿需求数、错误数。
- `executed_tools`：白名单工具的执行结果和摘要。
- `skipped_tools`：未执行工具的原因和下一步动作。
- `agent_handoff`：是否需要 Agent 接管，以及接管原因。

## 命令

```bash
python3 agent-tools/scripts/consultation_execution_runner.py --text "帮我做一个塔罗三张牌，看看工作状态"
```
