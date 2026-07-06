# 工具与 Skill Manifest 规范

## 用途

`tool_manifest_builder` 将工具脚本、schema、spec 和 `codex-skills/index.md` 中的 Skill 依赖关系编译成机器可读 JSON。

它用于后续 MCP/API wrapper、Skill 安装前检查、看板同步和发布审计之间的对账。

## 运行方式

```bash
python3 agent-tools/scripts/tool_manifest_builder.py
```

## 检查内容

| 范围 | 检查方式 |
| --- | --- |
| 工具三件套 | 每个工具必须有 `agent-tools/scripts/*.py`、`agent-tools/schemas/*.schema.json` 和 `agent-tools/specs/*.md` |
| Skill 依赖 | 从 `codex-skills/index.md` 读取每个 Skill 的工具钩子 |
| 领域归属 | 根据工具前缀、覆盖审计需求和 Skill 依赖映射领域 |
| 缺失项 | 输出 `missing`，标明缺失的 `script`、`schema` 或 `spec` |

## 解读方式

- `is_valid: true`：当前工具和 Skill 索引可以作为 agent runtime 的清单来源。
- `tools[].status: ready`：工具三件套齐全。
- `tools[].skills`：该工具被哪些 Skill 依赖。
- `tools[].domains`：该工具服务的流派或共享层。
- `missing`：新增、删除或重命名工具时需要优先修复的漂移项。

## 维护规则

- 新增工具时，先补 script/schema/spec，再把需要的 Skill 钩子写入 `codex-skills/index.md`。
- 重命名工具时，同步修改 Skill 蓝图、索引、spec、schema、测试和知识库引用。
- manifest 通过不代表工具语义正确，仍需单元测试、Skill 回放和人工审校。
- backlog 工具不进入 manifest，直到三件套齐全并可运行。
