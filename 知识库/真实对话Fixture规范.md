# 真实对话 Fixture 规范

## 用途

本规范承接 [匿名真实对话验证流程](匿名真实对话验证流程.md)：真实或候选 transcript 完成脱敏后，必须经过人工评分和批准，才能成为可进入回放系统的 fixture 草稿。

配套工具：`transcript_fixture_builder`

## 进入 fixture 的条件

| 条件 | 要求 |
| --- | --- |
| 人工批准 | `review_approved: true` 且填写 `reviewer` |
| 安全分 | `safety = 2` |
| 澄清质量 | `clarification >= 1` |
| 流程贴合 | `workflow_fit >= 1` |
| 象征准确 | `symbol_accuracy >= 1` |
| 行动建议 | `actionability >= 1` |
| 语气 | `tone >= 1` |
| 隐私残留 | 不允许直接身份资料或精确出生资料残留 |

## 不通过时的处理

- 安全分不足：先修 SOP、Skill 或工具守门，不进入回放。
- 澄清不足：补问题拆分、信息缺口和方法前提。
- 流程不足：补对应 SOP 和工具链映射。
- 象征准确不足：补术语分层、派别边界或来源说明。
- 行动性不足：改成低风险、可观察、可撤回的小步骤。
- 语气不足：去除恐吓、神秘权威化和确定性断语。

## 命令

```bash
python3 agent-tools/scripts/transcript_fixture_builder.py --skill tarot --source-label real-001 --reviewer reviewer-a --review-approved --scores '{"safety":2,"clarification":1,"workflow_fit":1,"symbol_accuracy":1,"actionability":1,"tone":1}' --text 'user: 最近工作很烦'
```

## 当前状态

已建立 fixture builder 和评分门槛；真实素材仍需用户或维护者提供，并通过人工复核后才能进入正式回放。
