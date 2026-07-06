# Tool Spec：folk_source_recorder

## 目标

记录民俗节令、禁忌和地方说法的来源信息，帮助 agent 区分家人口述、地方口述、宗教语境、公开文献、网络传闻、商业说法和个人习惯。工具只做 provenance 记录和边界判断，不把来源记录升级成学术证明、宗教权威或全国通用传统。

## 输入

- `claim_text` / `request_text` / `source_text`：用户提供的民俗说法。
- `custom_name`：可选民俗条目名，如搬家习俗、夜里吹口哨、端午习俗。
- `source_type`：`family_oral`、`regional_oral`、`religious_context`、`published_reference`、`internet_claim`、`commercial_claim`、`personal_preference`、`unknown`。
- `region`：地区、家庭迁徙背景或宗教地点。
- `community`：村镇、社区、庙观、宗教支派或人群语境。
- `informant_or_source_label`：来源标签，如外婆口述、某地地方志、某寺公告、某平台帖子。
- `source_date_or_generation`：来源年代、记录日期或第几代人口述。
- `usage_context`：`cultural_learning`、`family_communication`、`event_planning`、`writing`、`self_soothing`、`source_audit`。
- `evidence_items`：书名、作者、页码、链接、截图说明等可复核材料。

## 输出

- `source_reliability`：来源层级，不代表真伪证明。
- `risk_flags`：危险动作、灵异确定性、专业替代、商业利益、绝对权威风险。
- `missing_fields`：继续记录前需要补充的字段。
- `can_use_as_context`：是否可作为咨询上下文继续使用。
- `can_treat_as_tradition`：是否可保守写成有边界的传统/口述材料。
- `source_record`：可写入知识库的标准化来源记录。
- `questions_to_ask`：缺字段时的追问。

## 安全边界

- 网络、商业和未知来源不能直接写成传统民俗。
- 宗教语境不得被改写成全国民俗或所有家庭通用规则。
- 含明火、密闭燃烧、放血、摄入、刀具或专业替代表述时，先转仪式安全或现实支持。
- 不确认鬼神、诅咒、冲撞、犯忌必灾、开运保证或治疗效果。

## 示例

```bash
python3 agent-tools/scripts/folk_source_recorder.py --text "家里老人说江南搬家要先开灯和清扫入口" --custom-name 搬家习俗 --source-type family_oral --region 江南 --source-label 外婆口述 --source-date "上一辈口述" --usage-context family_communication
python3 agent-tools/scripts/folk_source_recorder.py --text "短视频说中元必须密闭烧纸才不会冲撞" --source-type internet_claim --source-label "短视频平台说法"
```
