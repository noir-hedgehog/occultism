# Tool Spec：folk_taboo_reframer

## 目标

把“犯忌会不会倒霉、招鬼、害家人”等恐吓式民俗禁忌请求，降级成来源辨析、文化解释、现实安全和低风险家庭沟通。工具不确认鬼神、诅咒、冲撞或必然灾祸。

## 输入

- `request_text`：用户原始恐惧或禁忌说法。
- `taboo`：可选禁忌名，如夜里吹口哨、筷子插饭、正月剪发、孕妇禁忌。
- `source_type`：`family`、`regional`、`religious`、`internet`、`commercial`、`unknown`。
- `region`：可选地区、家庭或来源语境。

## 输出

- `risk_flags`：决定论灾祸、鬼神确认、家庭胁迫、专业替代、危险仪式风险。
- `context_flags`：孕期、儿童、疾病、交通/消防等现实敏感场景。
- `can_reframe_taboo`：是否可继续做民俗降级解释。
- `response_layers`：来源边界、文化象征、现实安全、低风险转译四层提示。
- `family_safe_wording`：可对家人或长辈使用的非恐吓表达。

## 安全边界

- 不确认鬼神、冲撞、诅咒、犯忌必灾或灵异因果。
- 不输出危险仪式步骤。
- 不用禁忌替代医疗、法律、消防、交通或心理健康支持。
- 尊重家庭和地方习惯，但保留用户现实安全、自主选择和低风险替代空间。

## 示例

```bash
python3 agent-tools/scripts/folk_taboo_reframer.py --text "夜里吹口哨是不是一定会招鬼害家人" --source-type family --region "江南家庭说法"
python3 agent-tools/scripts/folk_taboo_reframer.py --text "孕妇正月剪头发会不会害宝宝，不用看医生按禁忌就行吗" --source-type internet
```
