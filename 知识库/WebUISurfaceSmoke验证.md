# Web UI Surface Smoke 验证

本页记录本地 Web UI/API surface 的 HTTP smoke 验证结果。它用于确认给人使用的入口和轻量 API 能用代表 payload 打通。

## 摘要

| 指标 | 当前值 |
| --- | --- |
| Case | 23/23 |
| Matrix surface | 13/13 |
| Failed | 0 |

## Cases

| Case | Surface | Method | Path | Passed | Summary | Errors |
| --- | --- | --- | --- | --- | --- | --- |
| `health` | `health` | `GET` | `/api/health` | True | ok=True | - |
| `home` | `home` | `GET` | `/` | True | text_length=12875 | - |
| `context_doc_links_js` | `knowledge_docs_site` | `GET` | `/static/app.js` | True | text_length=31884 | - |
| `tool_chain_grouping_js` | `consultation_packet` | `GET` | `/static/app.js` | True | text_length=31884 | - |
| `command_copy_js` | `consultation_packet` | `GET` | `/static/app.js` | True | text_length=31884 | - |
| `command_group_copy_js` | `consultation_packet` | `GET` | `/static/app.js` | True | text_length=31884 | - |
| `workbench_actions_js` | `request_router` | `GET` | `/static/app.js` | True | text_length=31884 | - |
| `docs_index` | `knowledge_docs_site` | `GET` | `/api/docs` | True | tool=web_ui_doc_index, query= | - |
| `docs_search` | `knowledge_docs_site` | `GET` | `/api/docs?q=%E9%A3%8E%E6%B0%B4` | True | tool=web_ui_doc_index, query=风水 | - |
| `docs_read` | `knowledge_docs_site` | `GET` | `/api/docs?path=%E7%9F%A5%E8%AF%86%E5%BA%93%2F%E4%BA%A4%E4%BA%92%E5%8F%AF%E7%94%A8%E5%8C%96%E7%9F%A9%E9%98%B5.md` | True | tool=web_ui_doc_reader | - |
| `summary` | `summary` | `GET` | `/api/summary` | True | project=玄学大典 / Occultism Agent Toolkit | - |
| `examples` | `example_presets` | `GET` | `/api/examples` | True | tool=web_ui_example_requests, is_valid=True, example_count=6, trunk_count=6 | - |
| `evidence_matrix` | `evidence_matrix` | `GET` | `/api/evidence-matrix` | True | tool=domain_evidence_matrix_builder, is_valid=True, domain_count=61, trunk_count=6 | - |
| `validation_backlog` | `validation_backlog` | `GET` | `/api/validation-backlog` | True | tool=case_validation_backlog_builder, is_valid=True, backlog_count=61 | - |
| `validation_template` | `validation_template` | `GET` | `/api/validation-template?domain=fengshui` | True | tool=case_validation_template_builder, is_valid=True, template_count=1 | - |
| `interaction_surface_matrix` | `interaction_surface_matrix` | `GET` | `/api/interaction-surface-matrix` | True | tool=interaction_surface_matrix_builder, is_valid=True, surface_count=13 | - |
| `session` | `request_router` | `POST` | `/api/session` | True | tool=web_ui_session, is_valid=True, route_status=ready_to_run_skill, domain=tarot, workbench_mode=guided_consultation_workbench | - |
| `paradigm` | `paradigm_selection` | `POST` | `/api/paradigm` | True | tool=paradigm_selector, is_valid=True, route_status=ready_to_run_skill, domain=tarot | - |
| `packet` | `consultation_packet` | `POST` | `/api/packet` | True | tool=consultation_packet_builder, is_valid=True | - |
| `execute_safe` | `safe_execution_subset` | `POST` | `/api/execute-safe` | True | tool=consultation_execution_runner, is_valid=True, route_status=ready_to_run_skill, domain=tarot | - |
| `tool_preview_fengshui` | `structured_tool_preview` | `POST` | `/api/tool-preview` | True | tool=web_ui_tool_preview, is_valid=True, mode=fengshui | - |
| `handoff` | `agent_handoff` | `POST` | `/api/handoff` | True | tool=consultation_handoff_builder, is_valid=True | - |
| `case_record` | `case_recording` | `POST` | `/api/case-record` | True | tool=consultation_case_recorder, is_valid=True, domain=tarot | - |

## 限制

- 此 smoke runner 验证本地 HTTP surface 和代表 payload，不替代浏览器视觉 QA。
- 通过 smoke 不代表真实素材、专家审校或生产托管已经完成。
- 测试服务只绑定 127.0.0.1，并在运行结束后关闭。

## 下一步

- `run_browser_visual_qa_for_layout_changes`
- `rerun_web_ui_surface_smoke_runner_after_endpoint_changes`
- `extend_smoke_cases_when_new_api_surfaces_are_added`
