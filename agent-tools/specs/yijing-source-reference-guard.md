# Tool Spec：yijing_source_reference_guard

## 目的

给易经/周易咨询建立原典、注疏、现代译注、网络断语和师承/个人经验的来源分级。它帮助 agent 在引用卦辞、爻辞、十翼、王弼/程朱等注疏或现代转述时，明确来源层级、引用边界、必要归属和安全改写。

此工具不提供完整原文库，不替代文献校勘，也不让卦爻来源变成确定预言。

## 输入

- `source_text` / `text` / `query`：用户提供的易经原文、注疏、现代译文、网络说法或断语。
- `source_type`：可选，支持 `jingwen`、`shiyi`、`wangbi`、`chengzhu`、`modern_translation`、`internet_claim`、`personal_lineage`。

## 输出

- `source_type`、`source_label`、`source_level`
- `can_use_as_reference`
- `risk_flags`
- `quote_policy`
- `use_scope`
- `required_attribution`
- `safe_reframes`
- `citation_template`
- `limits` 与 `next_steps`

## 规则

1. 原典经文/卦辞/爻辞可短引，但必须标注卦名/卦号、爻位或卦辞、版本/出处。
2. 十翼、王弼、程朱等注疏必须标注为解释层，不冒充卦爻原文。
3. 现代译注只能概括解释方向，不大段照搬。
4. 网络断语、短视频说法和师承/个人经验不能升格为原典或通行注疏。
5. 出现灾祸、疾病、财富、操控或唯一正统断言时，必须降级为风险提醒、来源辨析或现实支持。

## 命令

```bash
python3 agent-tools/scripts/yijing_source_reference_guard.py --text "王弼注说此处重在守中" --source-type wangbi
python3 agent-tools/scripts/yijing_source_reference_guard.py --text "短视频说这个爻必有大灾、股票必发财" --source-type internet_claim
```
