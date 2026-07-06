# Tool Spec：bazi_ziwei_intake_guard

## 目的

为八字、四柱、紫微斗数等命理请求做出生资料、隐私同意、宿命论和专业替代守门。此工具不排盘、不判断命格，只决定是否可以进入低风险命理咨询流程。

## 输入

- `request_text` 或 `question_text`：用户原始请求
- `requested_domain`：可选，`bazi`、`ziwei`、`mingli`
- `birth_date`、`birth_time`、`birth_place`、`calendar_type`：可选结构化出生资料
- `subject_consent`：第三方资料是否已获同意
- `subject_is_self`、`subject_is_minor`：可选隐私标记

## 输出

- `domain`：`bazi`、`ziwei` 或 `mingli`
- `analysis_focus`：事业、关系、自我理解、阶段、家庭、高风险专业类别或通用
- `data_status`：出生资料完整度
- `missing_fields`：继续前应补齐或确认的字段
- `privacy_flags`：精确出生资料、第三方、未成年人、敏感身份信息
- `risk_flags`：危机、医疗、财务、法律、宿命伤害、操控他人
- `can_continue_mingli`：是否可继续命理咨询
- `reframed_question`：非宿命论问题重述
- `allowed_scope`、`limits`、`warnings`、`next_steps`

## 安全规则

1. 寿命、灾祸、疾病、财富、婚育等确定性断言必须阻断。
2. 第三方命盘必须要求同意；否则只能做匿名文化解释。
3. 未成年人只做支持性、非标签化表述。
4. 不收集身份证、手机号、住址或完整真实姓名。
5. 医疗、法律、财务问题必须转为现实信息整理和专业支持。

## 命令

```bash
python3 agent-tools/scripts/bazi_ziwei_intake_guard.py --text "本人公历1990年5月1日08:30北京出生，想用八字看看事业倾向"
```
