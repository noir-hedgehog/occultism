# Tool Spec：dowsing_request_guard

## 目的

识别占杖、寻水杖、探测棒、dowsing rods、divining rod、L-rods 和 radiesthesia 请求，判断是否能继续低风险占杖象征咨询。

## 输入

- `request_text` 或 `text`

## 输出

- `consultation_intent`
- `risk_flags`
- `can_continue_dowsing`
- `required_boundaries`
- `clarifying_questions`
- `next_steps`

## 安全边界

- 不把占杖动作写成地下管线、水源、矿脉、疾病、灵体、事实位置或资源定位证明。
- 不替代工程勘测、地下管线探测、施工安全、医疗、法律、物业、报警、寻人或专业探测。
- 不协助开挖、打井、钻孔、闯入、跟踪、投资赌博、房产合同决定、高价课程购买或反复依赖。
