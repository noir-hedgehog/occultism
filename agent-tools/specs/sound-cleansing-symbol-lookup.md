# Tool Spec：sound_cleansing_symbol_lookup

## 作用

查询声响净化场景中的铃钵/颂钵、铃铛/手铃、音叉、拍手/轻叩、诵念/短句、安静收尾、开窗/通风和计时器等低风险象征线索。

## 输出

- `canonical_name`
- `symbol_code`
- `category`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `action_guidance`
- `prohibited_uses`

## 边界

声音符号只用于空间复位、注意力提示、收尾和复盘，不用于驱灵证明、治疗承诺、神谕命令或扰民。
