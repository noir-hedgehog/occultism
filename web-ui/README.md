# 玄学大典 Web UI

这是给人使用的本地 Web UI 和轻量 API。它不会尝试直接跑完整 61 个流派的咨询流程，而是先覆盖当前项目最重要的运行主干：

- 请求路由和安全分流
- 从具体问题推导适用范式
- 生成给人和 Agent 共读的咨询工作单
- 为塔罗和风水生成结构化工具输入并预览结果
- 领域、Skill、SOP、知识卡和初始工具链展示
- 知识库文档站浏览
- 当前覆盖度、工具数量和验证状态概览
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
curl http://127.0.0.1:8765/api/docs
curl "http://127.0.0.1:8765/api/docs?path=%E7%9F%A5%E8%AF%86%E5%BA%93/07-%E9%97%AE%E9%A2%98%E5%88%B0%E8%8C%83%E5%BC%8F%E6%98%A0%E5%B0%84.md"
curl -X POST http://127.0.0.1:8765/api/paradigm \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态"}'
curl -X POST http://127.0.0.1:8765/api/packet \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态"}'
curl -X POST http://127.0.0.1:8765/api/tool-preview \
  -H 'Content-Type: application/json' \
  -d '{"mode":"tarot","payload":{"question_text":"最近工作很烦，想做三张牌看看状态","spread_id":"three_card_situation","cards":[{"position":"现状","card":"魔术师","orientation":"upright"},{"position":"阻碍","card":"宝剑八","orientation":"reversed"},{"position":"建议","card":"星币三","orientation":"upright"}]}}'
curl -X POST http://127.0.0.1:8765/api/tool-preview \
  -H 'Content-Type: application/json' \
  -d '{"mode":"fengshui","payload":{"request_text":"卧室床对门，最近睡不好","space_type":"bedroom","space_description":"卧室床尾正对门，镜子在床侧，晚上容易被通知灯打扰，最近睡不好","observation_text":"卧室床尾正对门，镜子在床侧，晚上容易被通知灯打扰，最近睡不好","concerns":["sleep","pressure"]}}'
curl -X POST http://127.0.0.1:8765/api/session \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态"}'
```

## 边界

- UI 只在本地运行，不提供鉴权、多用户会话或远程托管安全模型。
- API 不执行任意 shell 命令；`/api/tool-preview` 只运行塔罗和风水白名单函数。
- 当路由结果为 orange/red 风险时，UI 会暂停玄学流程并显示安全边界。
