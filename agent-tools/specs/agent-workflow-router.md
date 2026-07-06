# Tool Spec：agent_workflow_router

## 目的

把用户请求路由到对应流派、Skill、SOP、知识卡和初始工具链；遇到高风险请求时输出暂停流程，而不是继续占卜、排盘或仪式。

它承接 `mystic_intake_triage`，并使用覆盖审计和工具 manifest 生成 agent 可执行的下一步计划。

## 输入

- `request_text`：用户请求文本。
- `requested_domain`：可选，用户指定的流派。
- `root`：仓库根目录，默认当前目录。

## 输出

遵循 [agent-workflow-router.schema.json](../schemas/agent-workflow-router.schema.json)。

关键字段：

- `route_status`
- `can_continue_mystic_workflow`
- `skill`
- `sop`
- `knowledge`
- `initial_tools`
- `agent_instructions`

## 判定

- `ready_to_run_skill`：低风险请求，可加载 Skill/SOP 并执行初始工具链。
- `paused_for_professional_boundary`：医疗、法律、财务、精神健康等高风险边界，暂停玄学流程。
- `blocked_safety`：即时危险或危险仪式，停止玄学流程并给安全支持。
- `needs_domain_selection`：未识别流派，先澄清。

## 命令

```bash
python3 agent-tools/scripts/agent_workflow_router.py --text "帮我做一个塔罗三张牌，看看工作状态"
```
