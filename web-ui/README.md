# 玄学大典 Web UI

这是给人使用的本地 Web UI 和轻量 API。它不会尝试直接跑完整 61 个流派的咨询流程，而是先覆盖当前项目最重要的运行主干：

- 请求路由和安全分流
- 领域、Skill、SOP、知识卡和初始工具链展示
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
curl -X POST http://127.0.0.1:8765/api/session \
  -H 'Content-Type: application/json' \
  -d '{"request_text":"帮我做一个塔罗三张牌，看看工作状态"}'
```

## 边界

- UI 只在本地运行，不提供鉴权、多用户会话或远程托管安全模型。
- API 不执行任意 shell 命令，只返回当前路由、上下文文件和建议命令。
- 当路由结果为 orange/red 风险时，UI 会暂停玄学流程并显示安全边界。

