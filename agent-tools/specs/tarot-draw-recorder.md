# Tool Spec：tarot_draw_recorder

## 目的

记录并校验塔罗抽牌结果，包括牌阵、牌位、牌名、正逆位和备注。这个工具用于把用户或模拟抽牌的结果转成可复盘的结构化 reading record。

这个工具不负责解释牌义，也不负责随机抽牌；随机模拟后续可由独立工具实现。

## 输入

JSON 对象：

```json
{
  "question_text": "我当前的工作局势、阻碍和下一步重点是什么？",
  "spread_id": "three_card_situation",
  "cards": [
    {"card": "The Fool", "orientation": "upright"},
    {"card": "宝剑三", "orientation": "逆位"},
    {"card": "星币国王", "orientation": "正位"}
  ]
}
```

可选字段：

- `positions`：自定义牌位，覆盖内置牌阵位置
- `note`：单张牌备注

## 输出

遵循 [tarot-draw-recorder.schema.json](../schemas/tarot-draw-recorder.schema.json)。

## 校验规则

- 牌数必须匹配牌位数。
- 牌名必须能识别为 78 张塔罗之一。
- 正逆位默认为 `upright`，也支持 `正位`、`逆位`、`reversed`。
- 同一次抽牌不允许重复同一张牌。

## 运行

```bash
python3 agent-tools/scripts/tarot_draw_recorder.py --json '{"spread_id":"single_focus","cards":[{"card":"愚者","orientation":"正位"}]}'
```

