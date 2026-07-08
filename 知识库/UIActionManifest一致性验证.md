# UI Action Manifest 一致性验证

本页比较 shared helper、Web UI session、咨询 handoff 和 runtime handoff 的动作菜单，防止 execute/preview/handoff/case 的启用状态、endpoint 或说明漂移。

## 摘要

| 指标 | 当前值 |
| --- | --- |
| 状态 | 2 |
| 来源 | 8 |
| 比较 | 6 |
| 通过 | True |

## 比较结果

| State | Source | Matches | Enabled Actions | Disabled Actions | Errors |
| --- | --- | --- | --- | --- | --- |
| `ready_to_continue` | `shared_helper` | True | execute, preview, handoff, case |  | - |
| `ready_to_continue` | `web_ui_session` | True | execute, preview, handoff, case |  | - |
| `ready_to_continue` | `consultation_handoff` | True | execute, preview, handoff, case |  | - |
| `ready_to_continue` | `runtime_handoff` | True | execute, preview, handoff, case |  | - |
| `paused_for_boundary` | `shared_helper` | True | execute, handoff | preview, case | - |
| `paused_for_boundary` | `web_ui_session` | True | execute, handoff | preview, case | - |
| `paused_for_boundary` | `consultation_handoff` | True | execute, handoff | preview, case | - |
| `paused_for_boundary` | `runtime_handoff` | True | execute, handoff | preview, case | - |

## 限制

- 此检查验证 Web UI session、咨询 handoff 和 runtime handoff 的动作菜单一致，不替代真实浏览器视觉 QA。
- 检查使用代表 ready/paused 请求，不覆盖所有领域文案变化。

## 下一步

- `rerun_after_action_manifest_changes`
- `keep_session_handoff_runtime_actions_in_sync`
- `add_browser_visual_qa_for_runtime_panel_when_browser_binary_is_available`
