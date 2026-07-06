# Tool Spec：mystic_intake_triage

## 目的

为所有玄学类请求提供统一 intake 和安全分级，避免 agent 在高风险场景直接进入占卜或仪式建议。

## 输入

- `request_text`：用户原始请求
- `known_context`：可选，用户已提供的背景
- `requested_domain`：可选，用户指定的流派

## 输出

遵循 [mystic-intake.schema.json](../schemas/mystic-intake.schema.json)。

## 运行

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "帮我做一个塔罗三张牌，看看工作状态"
```

## 规则

1. 出现即时伤害、自伤他伤、危险仪式，输出 `red`。
2. 出现医疗、法律、财务、精神危机，输出 `orange`。
3. 出现重大关系/职业决定且用户焦虑明显，输出 `yellow`。
4. 普通娱乐、文化学习、低风险反思，输出 `green`。
5. `orange` 和 `red` 的 `allowed_next_steps` 不得包含占卜执行。
