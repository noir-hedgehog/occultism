# Tool Spec：fengshui_yangzhai_case_library

## 目的

检索阳宅风水安全案例，把卧室、玄关、厨房、书房/办公室、店铺等高频空间请求转成可复用的观察顺序、传统术语、现实体验映射、低风险调整和禁用表达。

此工具不排盘、不做吉凶断语，也不证明财富、疾病、婚姻、灾祸或命运结果。

## 输入

- `query` 或 `request_text`：用户空间描述或案例检索语句
- `space_type`：可选，如 `bedroom`、`entrance`、`kitchen`、`office`、`shop`
- `concern`：可选，如 `sleep`、`focus`、`money`、`safety`
- `limit`：可选，1-10

## 输出

- `cases`：匹配案例
  - `observable_facts`
  - `traditional_terms`
  - `practical_mapping`
  - `low_risk_adjustments`
  - `avoid_language`
  - `recommended_tools`
  - `review_questions`
  - `safety_boundary`
- `can_continue_fengshui`
- `warnings`
- `limits` 与 `next_steps`

## 规则

1. 先把案例当作类比参考，不把它当成用户住宅事实。
2. 输出最终建议前仍需使用 `fengshui_observation_recorder` 记录用户实际可见事实。
3. 厨房燃气、电路、火花、霉菌、门锁和严重睡眠/精神状态风险必须先暂停风水解释。
4. “财位”“气口”“靠山”等词必须转译为主位、入口、支撑、动线、展示、收纳或安全感。
5. 禁止承诺发财、治病、避灾、旺婚、转运或替代专业检修/法律/财务/医疗判断。

## 命令

```bash
python3 agent-tools/scripts/fengshui_yangzhai_case_library.py --query "卧室床正对门，镜子对床，睡不好"
python3 agent-tools/scripts/fengshui_yangzhai_case_library.py --query "店铺入口被货架挡住，客流和业绩不好" --space-type shop --concern money
```
