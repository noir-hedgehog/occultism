# Tool Spec：symbolic_depth_lookup

## 目的

查询跨流派的“深度解释矩阵”，把单个象征、牌位、卦爻、盘式字段、方位、命理术语或仪式请求转成可审计的解释层级、边界和示例表达。

它不是占断工具，也不生成结论；它帮助 agent 在写作前选取正确的 SOP、工具链和安全措辞。

## 输入

- `domain`：可选，`tarot`、`yijing`、`qimen`、`fengshui`、`mingli`、`ritual`；兼容 `feng_shui`、`bazi`、`ziwei`、`ritual_safety` 等别名
- `query` / `symbol`：可选，象征、场景或解释层关键词，例如 `逆位`、`动爻`、`用神`、`第三方同意`
- `limit`：可选，1-12，默认 5

## 输出

遵循 [symbolic-depth-lookup.schema.json](../schemas/symbolic-depth-lookup.schema.json)。

关键字段：

- `entries[].interpretation_steps`
- `entries[].boundary`
- `entries[].example`
- `entries[].sop_links`
- `entries[].toolchain`

## 规则

1. 每个条目必须有解释步骤、边界和示例表达。
2. 工具只返回解释骨架，不生成占断结论。
3. 命中条目后仍需调用对应领域工具，例如 `tarot_interpretation_planner`、`yijing_line_lookup`、`qimen_focus_selector`。
4. 最终用户输出仍需通过 `mystic_output_lint`。
5. 高风险请求以安全边界优先，不因象征解释而绕过拒绝或转介。

## 命令

```bash
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain tarot --query 逆位
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain yijing --query 动爻
python3 agent-tools/scripts/symbolic_depth_lookup.py --query 第三方同意
```
