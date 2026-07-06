# Tool Spec：yijing_hexagram_record

## 目的

记录并校验易经起卦结果，包括起卦方法、六爻阴阳、动爻、本卦和变卦。

这个工具不负责随机起卦或解卦；它只负责把已经得到的六爻结果结构化。

## 输入

六爻必须自下而上输入。支持 6/7/8/9：

- `6`：老阴，动爻
- `7`：少阳
- `8`：少阴
- `9`：老阳，动爻

```bash
python3 agent-tools/scripts/yijing_hexagram_record.py --json '{"question_text":"我该不该跳槽？","casting_method":"three_coins","lines":[7,7,7,7,7,7]}'
```

也支持对象：

```json
{
  "lines": [
    {"value": "yang", "changing": true},
    {"value": "yin"},
    {"value": "yang"},
    {"value": "yin"},
    {"value": "yang"},
    {"value": "yin"}
  ]
}
```

## 输出

遵循 [yijing-hexagram-record.schema.json](../schemas/yijing-hexagram-record.schema.json)。

## 校验规则

- 必须正好六爻。
- 线序固定为自下而上。
- 可选传入 `expected_hexagram_number` 或 `expected_hexagram_name`，工具会与计算结果对照并输出 warning。
- 没有动爻时 `changed_hexagram` 为 `null`。
