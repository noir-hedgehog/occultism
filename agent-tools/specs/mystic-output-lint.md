# Tool Spec：mystic_output_lint

## 目的

检查玄学 agent 的草稿输出是否包含高风险措辞或步骤。这个工具用于“回答发布前”的最后一道安全阀，不判断占卜内容是否正确，只判断是否越过项目安全边界。

## 输入

- `output_text`：agent 草稿输出

也可直接通过 `--text`、`--file` 或 stdin 输入纯文本。

## 输出

遵循 [mystic-output-lint.schema.json](../schemas/mystic-output-lint.schema.json)。

## 检查类别

| 类别 | 级别 | 处理 |
| --- | --- | --- |
| 危险仪式步骤 | red | 阻断发布，删除危险步骤 |
| 诅咒、报复、操控他人 | red | 阻断发布，改为边界/自我保护建议 |
| 替代医疗、法律、紧急安全或高风险财务判断 | red | 阻断发布，转介专业支持 |
| 确认超自然伤害或实体 | orange | 重写，不确认超自然原因 |
| 确定性恐吓或宿命论 | orange | 重写为象征性、可行动表达 |
| 过度确定预测 | yellow | 可人工审核后发布，但需加限制 |

## 运行

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "你家有鬼，这件事一定会带来大祸。"
```

## 发布规则

- `red`：不得发布。
- `orange`：重写后重新 lint。
- `yellow`：需要人工或 agent 自检改写措辞。
- `green`：可发布。

