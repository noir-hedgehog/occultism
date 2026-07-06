# Tool Spec：western_geomancy_chart_recorder

## 目的

记录低风险西洋土占盾形盘中的问题、起盘来源、生成方式、母亲图、女儿图、侄子图、见证者、裁判者和缺失字段。

## 输入

- `question_text` / `request_text` / `text`
- `chart_source`
- `generation_method`
- `mothers` / `mother_figures`
- `daughters` / `daughter_figures`
- `nieces` / `niece_figures`
- `witnesses`
- `judge`
- `chart_notes` / `notes`
- `focus`

## 输出

- 标准化后的盘面字段
- `risk_flags`
- `missing_fields`
- `safety_notes`
- `next_steps`

## 注意

记录器只保存盘面结构，不自行推导缺失图形，不把裁判者写成命令或事实证明。
