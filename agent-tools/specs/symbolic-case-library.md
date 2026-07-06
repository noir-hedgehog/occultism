# Tool Spec：symbolic_case_library

## 目的

查询跨流派深度案例库，为塔罗、易经、奇门、风水、命理、仪式安全提供安全解释样例、禁用表达、推荐工具链和审查问题。

它补足 `symbolic_depth_lookup` 的“解释层级”功能：深度矩阵回答“该按什么层级解释”，案例库回答“类似场景怎样安全写”。

## 输入

- `domain`：可选，`tarot`、`yijing`、`qimen`、`fengshui`、`mingli`、`ritual`
- `scenario`：可选，`normal`、`blocked`、`boundary_reframed`、`blocked_then_safe`、`privacy_boundary`、`limited`、`source_guard`
- `query` / `text`：可选，用户场景、术语或案例关键词
- `limit`：可选，1-18，默认 6

## 输出

遵循 [symbolic-case-library.schema.json](../schemas/symbolic-case-library.schema.json)。

关键字段：

- `cases[].safe_interpretation`
- `cases[].sample_language`
- `cases[].avoid_language`
- `cases[].recommended_tools`
- `cases[].review_questions`

## 规则

1. 案例只能提供安全写法和审查问题，不输出完整占断结论。
2. 每个案例必须有 `avoid_language`，明确哪些表达禁止复用。
3. 每个案例必须指向推荐工具链，最终输出仍需通过 `mystic_output_lint`。
4. 高风险、第三方、未成年人、专业替代场景必须作为边界或拒绝路径案例。

## 命令

```bash
python3 agent-tools/scripts/symbolic_case_library.py --domain tarot --query 工作
python3 agent-tools/scripts/symbolic_case_library.py --domain ritual --scenario blocked_then_safe
python3 agent-tools/scripts/symbolic_case_library.py --query 第三方出生资料
```
