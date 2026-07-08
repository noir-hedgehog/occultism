# Tool Spec：ui_action_manifest_consistency_checker

## 目的

比较 shared helper、Web UI session、咨询 handoff 和 runtime handoff 的 UI action manifest，确认 `execute`、`preview`、`handoff`、`case` 的启用状态、endpoint、surface 和说明没有漂移。

它用于把“给人使用的按钮状态”和“Agent/runtime 可执行动作边界”纳入发布质量门。

## 输入

- `root`：仓库根目录，默认当前目录。
- `format`：`json` 或 `markdown`。
- `write`：写入 `知识库/UIActionManifest一致性验证.md`。

## 输出

遵循 [ui-action-manifest-consistency-checker.schema.json](../schemas/ui-action-manifest-consistency-checker.schema.json)。

关键字段：

- `state_count`：检查的动作状态数量，目前为 ready 与 paused 两种。
- `source_count`：参与比较的来源数量。
- `comparison_count`：与 expected manifest 的比较次数。
- `comparisons`：每个状态下各来源的 manifest、匹配结果和差异。

## 命令

```bash
python3 agent-tools/scripts/ui_action_manifest_consistency_checker.py
python3 agent-tools/scripts/ui_action_manifest_consistency_checker.py --format markdown --write
```

## 局限

- 只验证动作菜单契约，不替代浏览器视觉 QA。
- 当前使用代表 ready/paused 请求，不代表所有流派文案都已逐一覆盖。
