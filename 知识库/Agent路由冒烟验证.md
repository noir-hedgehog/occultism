# Agent 路由冒烟验证

本页记录 `agent_route_smoke_runner` 的用途：批量验证代表性用户请求能否进入正确流派、Skill、SOP 和风险状态。

## 覆盖范围

| 类型 | 覆盖 |
| --- | --- |
| 正常流派 | 塔罗、风水、空间净化/驱邪、民俗、易经、六爻、梅花易数、奇门、八字/紫微、姓名学、占星 |
| 高风险暂停 | 塔罗财务决策 |
| 安全阻断 | 密闭明火驱邪 |

## 运行方式

```bash
python3 agent-tools/scripts/agent_route_smoke_runner.py
```

单个样例：

```bash
python3 agent-tools/scripts/agent_route_smoke_runner.py --case-id route-tarot-career
```

## 判定

- `is_valid: true`：全部代表请求的流派、Skill、路由状态和是否可继续均符合预期。
- `failed_count > 0`：检查 `results[].errors`，通常需要修正 intake 关键词、路由别名、Skill 索引或 SOP 映射。

## 限制

- 冒烟验证只覆盖代表性入口，不替代真实用户表达扩充。
- 它只验证路由，不验证最终回答质量。
- 高风险请求必须保持暂停或阻断，不允许为了覆盖率继续占卜流程。
