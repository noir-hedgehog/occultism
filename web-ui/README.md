# 玄学大典 Web UI

这是给人使用的本地 Web UI 和轻量 API。它不会尝试直接跑完整 61 个流派的咨询流程，而是先覆盖当前项目最重要的运行主干：

- 请求路由和安全分流
- 从具体问题推导适用范式
- 在范式面板中展示程序化、Agent 和人工审校分工
- 通过 6 条主干示例请求快速试运行范式推导
- 汇总主干、范式、自动化步骤、Agent 接管点和必读文档的工作台总览
- 从工作台总览直接触发安全执行、结构化预览、Agent 交接和案例候选
- 工作台动作会按风险状态动态禁用不合适的领域预览和案例记录
- 结构化输入和案例记录独立面板复用同一风险守门逻辑
- `/api/session` 返回 UI action manifest，供 Web UI 和外部 agent/runtime 共用动作边界
- `/api/handoff` 携带同一动作边界，供 Agent 接管后继续判断下一步
- 从工作台和上下文面板直接打开必读文档
- 生成给人和 Agent 共读的咨询工作单
- 按可直接运行、需结构化输入和需 Agent 草稿分组展示工具链
- 一键复制工具链命令，但不在浏览器内执行 shell
- 一键复制全部可直接运行命令，方便转入终端执行安全子集
- 执行工作单中安全、确定、无副作用的程序化子集
- 展示 61 个领域的证据矩阵摘要和 P0/P1/P2 工作流
- 为塔罗和风水生成结构化工具输入并预览结果
- 生成 Agent 交接包，并对可选草稿执行安全措辞检查
- 生成回访、审校和脱敏后的案例候选记录
- 领域、Skill、SOP、知识卡和初始工具链展示
- 知识库文档站浏览
- 知识库文档站正文渲染 Markdown 标题、列表、表格、代码块和链接
- 当前覆盖度、工具数量和验证状态概览
- 展示案例、来源和边界反例验证 backlog
- 按领域生成案例、来源或边界反例采集模板
- 展示 UI/API/工具/Agent 接管边界的交互可用化矩阵
- 可用 `web_ui_surface_smoke_runner` 对本地 HTTP surface 做 smoke 验证
- 代表性命令生成，方便从 UI 进入程序化执行

## 启动

```bash
python3 web-ui/server.py --port 8765
```

然后打开：

```text
http://127.0.0.1:8765
```

## API

```bash
curl http://127.0.0.1:8765/api/health
curl http://127.0.0.1:8765/api/summary
curl http://127.0.0.1:8765/api/examples
curl http://127.0.0.1:8765/api/evidence-matrix
curl http://127.0.0.1:8765/api/validation-backlog
curl "http://127.0.0.1:8765/api/validation-template?domain=fengshui"
curl http://127.0.0.1:8765/api/interaction-surface-matrix
curl http://127.0.0.1:8765/api/docs
curl "http://127.0.0.1:8765/api/docs?q=%E9%A3%8E%E6%B0%B4"
curl "http://127.0.0.1:8765/api/docs?path=%E7%9F%A5%E8%AF%86%E5%BA%93/07-%E9%97%AE%E9%A2%98%E5%88%B0%E8%8C%83%E5%BC%8F%E6%98%A0%E5%B0%84.md"
curl -X POST http://127.0.0.1:8765/api/paradigm \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态"}'
curl -X POST http://127.0.0.1:8765/api/packet \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态"}'
curl -X POST http://127.0.0.1:8765/api/execute-safe \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态"}'
curl -X POST http://127.0.0.1:8765/api/tool-preview \
  -H 'Content-Type: application/json' \
  -d '{"mode":"tarot","payload":{"question_text":"最近工作很烦，想做三张牌看看状态","spread_id":"three_card_situation","cards":[{"position":"现状","card":"魔术师","orientation":"upright"},{"position":"阻碍","card":"宝剑八","orientation":"reversed"},{"position":"建议","card":"星币三","orientation":"upright"}]}}'
curl -X POST http://127.0.0.1:8765/api/tool-preview \
  -H 'Content-Type: application/json' \
  -d '{"mode":"fengshui","payload":{"request_text":"卧室床对门，最近睡不好","space_type":"bedroom","space_description":"卧室床尾正对门，镜子在床侧，晚上容易被通知灯打扰，最近睡不好","observation_text":"卧室床尾正对门，镜子在床侧，晚上容易被通知灯打扰，最近睡不好","concerns":["sleep","pressure"]}}'
curl -X POST http://127.0.0.1:8765/api/handoff \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态","draft_output":"这只是工作状态反思：先整理事实和下一步，不保证结果。"}'
curl -X POST http://127.0.0.1:8765/api/case-record \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态","draft_output":"这只是工作状态反思：先整理事实和下一步，不保证结果。","follow_up_text":"两天后复盘：建议有部分可用。","validation_result":"mixed","reviewer":"internal-reviewer"}'
curl -X POST http://127.0.0.1:8765/api/session \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态"}'
python3 agent-tools/scripts/web_ui_surface_smoke_runner.py --format markdown
```

## 边界

- UI 只在本地运行，不提供鉴权、多用户会话或远程托管安全模型。
- API 不执行任意 shell 命令；`/api/examples`、`/api/evidence-matrix`、`/api/validation-backlog`、`/api/validation-template` 和 `/api/interaction-surface-matrix` 只读取、路由或分类本地知识库覆盖信息，`/api/execute-safe` 只运行安全白名单函数，`/api/tool-preview` 只运行塔罗和风水白名单函数，`/api/handoff` 只组合工作单、预览结果和 lint，`/api/case-record` 只生成候选案例记录。
- 当路由结果为 orange/red 风险时，UI 会暂停玄学流程并显示安全边界。
