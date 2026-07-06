# Codex Skill 模板

```markdown
---
name: skill-name
description: Use when a user asks Codex to ...
---

# Skill Title

Use this skill to ...

## Workflow

1. Check safety boundaries.
2. Load only the relevant reference files.
3. Collect minimum required input.
4. Execute the domain workflow.
5. Lint the final draft with `mystic_output_lint` or an equivalent safety check.
6. Produce structured output with limits.

## Output Shape

\```text
安全分级：
问题重述：
方法：
结果：
建议：
限制：
输出检查：
\```

## References

- `知识库/...`
```
