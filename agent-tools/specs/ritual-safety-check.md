# Tool Spec：ritual_safety_check

## 目的

检查用户请求的仪式是否包含危险材料、危险环境或伤害性意图，并给出安全替代方向。

## 危险信号

- 明火、密闭燃烧、酒精助燃
- 刀具、血液、自伤、他伤
- 草药摄入、未知粉末、禁食、极端熬夜
- 诅咒、报复、控制他人
- 要求停止医疗、心理、法律支持

## 输出字段

遵循 [ritual-safety.schema.json](../schemas/ritual-safety.schema.json)。

- `risk_level`
- `blocked_steps`
- `safe_alternatives`
- `referral_message`
- `can_continue_symbolic_support`

## 运行

```bash
python3 agent-tools/scripts/ritual_safety_check.py --text "搬家后想做一个不用火的空间净化"
```
