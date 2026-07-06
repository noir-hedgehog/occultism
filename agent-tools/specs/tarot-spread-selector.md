# Tool Spec：tarot_spread_selector

## 目的

根据用户的塔罗问题选择合适牌阵、生成牌位结构、改写非决定论问题，并标记不适合继续塔罗的风险。

这个工具不负责抽牌、洗牌、解牌或牌义检索；它只负责“选牌阵”和“整理问题”。

## 输入

- `question_text`：用户塔罗问题
- `request_text`：兼容字段，等价于 `question_text`

## 输出

遵循 [tarot-spread-selector.schema.json](../schemas/tarot-spread-selector.schema.json)。

## 推荐规则

| 问题类型 | 推荐牌阵 |
| --- | --- |
| 每日提醒、轻量聚焦 | 单张聚焦 |
| 普通关系/事业/自我整理 | 三张状态牌阵 |
| 关系中涉及对方状态或复合 | 关系镜像 |
| 二选一、搬家、方案比较 | 二选一路径 |
| 专业高风险决策 | 只做资源/风险/下一步重述，不替代专业判断 |

## 风险处理

- `crisis`：不得继续塔罗，先处理即时安全。
- `coercion`：不得继续操控型占问，改为边界和自我保护。
- `professional_decision`：可做情绪和准备度整理，但不得给决定性建议。

## 运行

```bash
python3 agent-tools/scripts/tarot_spread_selector.py --text "我该选 A offer 还是 B offer？"
```

