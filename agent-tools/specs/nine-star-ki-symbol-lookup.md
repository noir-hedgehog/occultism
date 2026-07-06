# Tool Spec：nine_star_ki_symbol_lookup

## 目的

查询九星气学九颗星、本命星/年星/方位层级的低风险象征提示。

## 输入

- `query`、`star` 或 `symbol`：星名、数字、层级或方位概念。
- `focus`：可选咨询焦点。

## 输出

- `canonical_name`
- `symbol_code`
- `category`
- `keywords`
- `interpretation_prompt`
- `reflection_questions`
- `action_guidance`
- `prohibited_uses`
- `next_steps`

## 安全边界

- 不把星名解释成诊断、财富结果、关系筛选、搬迁命令或专业意见。
- 不制造方位恐吓、高价化解压力或反复计算依赖。
- 未知派别写法必须先询问来源，不编造权威解释。
