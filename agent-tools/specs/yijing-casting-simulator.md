# Tool Spec：yijing_casting_simulator

## 目的

当用户没有自行起卦，且问题已经通过 `yijing_question_guard` 与 `yijing_casting_method_advisor` 时，模拟易经起卦并生成可复现、可审计的六爻记录。输出会直接调用 `yijing_hexagram_record`，得到本卦、动爻和变卦结构。

## 输入

- `casting_method` / `method`：`three_coins` 或 `yarrow_stalk`
- `question_text`
- `seed`：可选；提供后同一输入会得到同一组六爻
- `cast_time`、`timezone`：可选

## 输出

- `generated_lines`：自下而上的六爻，值为 6、7、8、9
- `recorded_cast`：由 `yijing_hexagram_record` 校验后的起卦记录
- `seed`、`seed_generated`
- `limits`、`next_steps`

## 方法说明

- 三枚铜钱法：每爻模拟三枚硬币，字面保留 coin trace，概率为 6:1/8、7:3/8、8:3/8、9:1/8。
- 蓍草概率模拟：使用传统分布 6:1/16、7:5/16、8:7/16、9:3/16；这是概率模型，不模拟完整分蓍过程。

## 安全规则

1. 起卦前必须先确认一事一问、高风险边界、用户同意和重复占问边界。
2. 随机起卦只是象征反思入口，不是确定预测证据。
3. 最终解释必须接 `yijing_hexagram_lookup` 和 `mystic_output_lint`。

## 命令

```bash
python3 agent-tools/scripts/yijing_casting_simulator.py --method three_coins --seed demo --question "我当前工作局势的主要变化是什么？"
```
