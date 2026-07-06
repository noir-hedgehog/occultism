# Tool Spec：knowledge_coverage_audit

## 目的

审计玄学 agent 知识库的覆盖度，检查每个首批流派是否具备：

- SOP
- 流派知识卡/深度资料
- Codex Skill 蓝图
- 可运行工具、schema、spec
- Skill 回放和多轮 transcript 验证证据

它面向维护者，用于让 [仪表盘](../../知识库/仪表盘.md) 和 [看板](../../知识库/看板.md) 不只靠人工记忆维护。

## 输入

- `root`：可选，仓库根目录，默认当前目录。

## 输出

遵循 [knowledge-coverage-audit.schema.json](../schemas/knowledge-coverage-audit.schema.json)。

关键字段：

- `domains[].level`
- `domains[].sections`
- `domains[].missing`
- `common.sections`
- `quality_gates`
- `limits`

## 规则

1. 每个流派至少检查 SOP、知识卡、Skill、工具链和验证证据。
2. 工具链要求 script、schema、spec 三件套齐全。
3. `is_valid` 只代表关键文件覆盖齐全，不代表内容已经完整穷尽。
4. 真实匿名 transcript 仍需人工复核，不能由覆盖度审计替代。

## 命令

```bash
python3 agent-tools/scripts/knowledge_coverage_audit.py
```
