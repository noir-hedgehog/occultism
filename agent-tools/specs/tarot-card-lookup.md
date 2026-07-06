# Tool Spec：tarot_card_lookup

## 目的

按牌名检索塔罗象征素材，包括正位关键词、逆位提醒、反思问题和行动提示。工具覆盖完整 78 张牌：大阿尔卡那使用固定条目，小阿尔卡那由花色主题和数字/宫廷主题组合生成。

## 输入

```bash
python3 agent-tools/scripts/tarot_card_lookup.py --card "Three of Swords" --orientation reversed --position "阻碍"
```

也可传入 JSON：

```json
{
  "card": "宝剑三",
  "orientation": "逆位",
  "position": "阻碍"
}
```

## 输出

遵循 [tarot-card-lookup.schema.json](../schemas/tarot-card-lookup.schema.json)。

## 边界

- 牌义只作为象征素材，不直接生成完整解读。
- 最终解读必须结合问题、牌位和牌间关系。
- 不把塔罗牌义作为医疗、法律、财务或人身安全判断。

