# Tool Spec：cartomancy_card_lookup

## 作用

查询标准 52 张扑克牌的花色和点数象征提示，包括红桃、黑桃、方片、梅花、A、2-10、J、Q、K 和 Joker。

## 输出

- `canonical_name`
- `symbol_code`
- `rank`
- `suit`
- `rank_keywords`
- `suit_keywords`
- `prohibited_uses`

## 边界

- 不把牌面写成事实、预言、诊断、财富结果或第三方真实想法。
- 未知牌面交给解释计划器以“自定义/不明牌面”处理，不编造权威含义。
