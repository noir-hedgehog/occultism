# Tool Spec：fengshui_bagua_mapper

## 目的

把用户提供的方位映射到八卦、五行、象征主题、可见空间观察问题和低风险调整建议。此工具不测量罗盘、不排飞星盘、不预测财富/疾病/婚恋结果，只做传统象征与现实空间体验之间的安全桥接。

## 输入

- `request_text` / `space_description`：空间描述或风水方位请求
- `direction`：可选，`north`、`northeast`、`east`、`southeast`、`south`、`southwest`、`west`、`northwest`、`center`
- `concerns`：可选，`sleep`、`focus`、`relationship`、`resources`、`pressure`

## 输出

遵循 [fengshui-bagua-mapper.schema.json](../schemas/fengshui-bagua-mapper.schema.json)。

关键字段：

- `direction`
- `trigram`
- `element`
- `symbolic_themes`
- `practical_observation_prompts`
- `low_risk_adjustments`
- `concern_guidance`
- `safety_flags`
- `limits`

## 规则

1. 没有明确方位时，不编造罗盘结果；改做形法审视。
2. 八卦方位只作为观察提示，不作为吉凶定论。
3. 财务/资源主题只能转为收纳、预算、文件、工作流和入口动线建议，不预测发财或破财。
4. 发现燃气、电路、霉菌、安防或严重睡眠/精神状态信号时，先暂停风水解释。
5. 最终建议仍需通过 `fengshui_observation_recorder`、`fengshui_space_checklist`、`fengshui_recommendation_ranker` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/fengshui_bagua_mapper.py --text "书房在东南方，文件很多，想改善工作和财务感受"
python3 agent-tools/scripts/fengshui_bagua_mapper.py --direction southwest --text "卧室在西南，最近睡不好"
```
