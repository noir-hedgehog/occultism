# Tool Spec：naming_brand_scenario_scorer

## 目标

为品牌名、店名和商号候选做场景适配粗筛。工具评估记忆度、读音、品类适配、受众适配、可搜索性和风险控制，不替代商标、域名、工商、广告法或行业合规审查。

## 输入

- `request_text`：用户原始请求。
- `candidates`：候选品牌名数组，或用顿号/逗号/空格分隔的字符串。
- `category`：品类或行业，如茶饮、教育、咨询、科技、文创。
- `audience`：目标受众。
- `tone` / `tones`：期望语气，如温和、清爽、专业、年轻、高端。
- `channels`：主要传播渠道，如门头、包装、小红书、抖音、搜索、域名、电商。

## 输出

- `can_score_brand_names`：是否可以继续做品牌名场景评分。
- `evaluations`：每个候选在六个维度上的分数、优势、谨慎点和外部检查项。
- `ranked_candidates`：按粗筛分数排序的候选。
- `risk_flags`：注册承诺、必火招财或受监管行业功效/收益风险。
- `warnings` / `limits`：商标、域名、平台和合规边界。

## 安全边界

- 不承诺商标可注册、域名可用、平台账号可用、不会侵权或商业成功。
- 不把五行、吉凶、招财、转运或“必火”写成品牌可用性证明。
- 医疗、保健、金融、投资等受监管行业必须另做专业合规审查。

## 示例

```bash
python3 agent-tools/scripts/naming_brand_scenario_scorer.py --json '{"request_text":"给茶饮品牌比较星禾和清朗","candidates":["星禾","清朗"],"category":"茶饮","audience":"年轻上班族","tone":["清爽","年轻"],"channels":["门头","小红书","搜索","域名"]}'
python3 agent-tools/scripts/naming_brand_scenario_scorer.py --text "星禾这个品牌名是不是一定可注册还会旺财" --candidates 星禾 --category 茶饮 --audience 年轻人 --channels "搜索、域名"
```
