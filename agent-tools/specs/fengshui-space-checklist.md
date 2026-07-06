# Tool Spec：fengshui_space_checklist

## 目的

根据用户的空间类型、空间描述和主要困扰生成风水空间审视清单。工具优先处理现实安全、动线、光线、通风、收纳、隐私和压迫感，再提供传统形法术语作为解释语言。

这个工具不负责罗盘、飞星、八宅或择日推算；首版聚焦可见空间形法和低风险调整。

## 输入

可用纯文本：

```bash
python3 agent-tools/scripts/fengshui_space_checklist.py --text "卧室睡不好，床正对门，镜子对床"
```

也可用 JSON：

```json
{
  "space_type": "bedroom",
  "concerns": ["sleep"],
  "space_description": "床正对门，镜子对床，晚上睡不好"
}
```

## 输出

遵循 [fengshui-space-checklist.schema.json](../schemas/fengshui-space-checklist.schema.json)。

## 风险处理

- 出现燃气、电路、霉菌、异味、门锁、人身安全、严重失眠或精神危机时，`can_continue_fengshui` 为 `false`。
- 此时先处理现实安全，不继续做传统风水解释。

## 设计边界

- 不说“必然破财”“一定伤身”等确定性恐吓。
- 不把疾病、关系冲突、财务损失直接归因于空间格局。
- 所有建议应低成本、可逆、非危险。

