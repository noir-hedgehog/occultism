# Tool Spec：fengshui_recommendation_ranker

## 目的

把风水空间审视建议按安全、成本、可逆性和影响排序。它用于把 `fengshui_space_checklist` 的候选调整变成可执行优先级，避免 agent 把危险、高成本、不可逆建议说成“马上照做”。

## 输入

可直接传入 `fengshui_space_checklist` 输出中的 `checklist`：

```bash
python3 agent-tools/scripts/fengshui_recommendation_ranker.py --json '{"checklist":[{"item_id":"light_air","category":"光线与通风","priority":"high","low_risk_adjustments":["每天短时通风","检查霉菌和异味源"]}]}'
```

也可传入人工建议：

```json
{
  "recommendations": [
    {"recommendation": "检查燃气和通风"},
    {"recommendation": "清理门后杂物"},
    {"recommendation": "拆墙改门"}
  ]
}
```

## 输出

遵循 [fengshui-recommendation-ranker.schema.json](../schemas/fengshui-recommendation-ranker.schema.json)。

## 排序原则

1. 涉及燃气、电路、霉菌、门锁、人身安全的建议优先，但标记为 `professional_check`。
2. 低成本、高可逆性的整理、通风、遮挡、移动类建议优先执行。
3. 高成本或不可逆的装修类建议降级为 `plan_before_action`。
4. 最终回答仍需通过 `mystic_output_lint`。

