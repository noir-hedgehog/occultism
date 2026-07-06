# Tool Spec：past_life_symbol_lookup

## 作用

为前世/阿卡西叙事中的常见场景、角色和符号提供安全象征提示，例如图书馆、门槛、水、战场、寺院、契约、同行者、流放、疗愈者、工匠和孩子。

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

- 不把符号解释成事实、记忆、创伤证据、灵魂等级、罪责、复合保证或命运判决。
- 未知符号由 planner 作为个人意象处理，不编造固定意义。
