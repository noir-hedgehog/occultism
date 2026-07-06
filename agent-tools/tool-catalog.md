# Agent Tool Catalog

## 通用工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `agent_route_smoke_runner` | runnable | 批量验证 61 个流派代表请求和高风险边界的路由结果 |
| `agent_runtime_dry_run_runner` | runnable | 用代表请求验证 ready/paused/blocked 路径是否满足 runtime 工具契约 |
| `agent_runtime_handoff_builder` | runnable | 汇总 agent runtime 接入入口、Skill、工具 manifest、安全不变量和验证命令 |
| `agent_tool_definition_exporter` | runnable | 将 wrapper manifest 导出为 agent tool definition 和 OpenAI-style function tool |
| `agent_tool_definition_validator` | runnable | 注册前验证 agent tool definition、OpenAI-style function tool 和本地引用 |
| `agent_tool_registry_builder` | runnable | 生成 runtime 注册顺序、流派/Skill 索引和安全启动工具注册表 |
| `agent_tool_registry_validator` | runnable | 注册前验证 runtime 注册表、Skill 索引和安全 bootstrap 一致性 |
| `agent_tool_wrapper_manifest_builder` | runnable | 生成 agent runtime/MCP/API wrapper 元数据清单 |
| `agent_workflow_router` | runnable | 将用户请求路由到对应流派、Skill、SOP、知识卡和初始工具链 |
| `codex_skill_blueprint_validator` | runnable | 静态检查 Skill 蓝图 frontmatter、章节、引用、工具钩子和索引依赖 |
| `codex_skill_installer` | runnable | 将验证通过的 Skill 蓝图 dry-run 或显式安装到 Codex skills 目录 |
| `content_review_feedback_recorder` | runnable | 记录内容专家反馈、批准范围、必改项和看板更新建议 |
| `content_review_packet_builder` | runnable | 汇总各流派 SOP、知识卡、Skill、工具 spec 和审校问题，生成内容审校包 |
| `external_evidence_intake_builder` | runnable | 生成实际安装确认、真实匿名 transcript 和内容专家批准的外部证据入口包 |
| `mystic_intake_triage` | runnable | 收集请求类型、风险信号、用户目标，输出安全分级 |
| `mystic_output_lint` | runnable | 检查输出是否包含确定性恐吓、危险仪式、专业替代错误 |
| `knowledge_coverage_audit` | runnable | 审计知识库、SOP、Skill、工具三件套、回放和看板覆盖度 |
| `knowledge_navigation_builder` | runnable | 汇总覆盖审计、工具 manifest、看板和知识库目录，生成给人看的导航索引 |
| `pilot_readiness_report` | runnable | 汇总自动证据和外部阻塞项，判断内部试运行与完整发布状态 |
| `release_gate_runner` | runnable | 运行发布前一键质量门并输出结构化验收报告 |
| `release_manifest_builder` | runnable | 汇总质量门、覆盖审计、开放事项和维护节奏，生成版本 manifest |
| `skill_install_readiness_report` | runnable | 汇总 Codex Skill 安装 dry-run、目标路径、冲突状态和审批清单 |
| `sop_traceability_matrix_builder` | runnable | 生成 SOP、知识卡、Skill、工具链和验证证据的追踪矩阵 |
| `tool_manifest_builder` | runnable | 汇总工具脚本、schema、spec 和 Skill 依赖关系，生成 agent runtime manifest |
| `symbolic_case_library` | runnable | 检索跨流派深度案例，返回安全写法、禁用表达和审查问题 |
| `symbolic_depth_lookup` | runnable | 检索跨流派深度解释矩阵，返回边界、案例、SOP 链接和工具链 |
| `transcript_anonymizer` | runnable | 为真实 transcript 做脱敏、隐私/风险打标、评分量表和回放映射准备 |
| `transcript_fixture_builder` | runnable | 将脱敏 transcript 与人工评分合成可审阅 fixture 草稿，并判断是否可进入回放 |
| `skill_replay_runner` | runnable | 对首批 61 个 Skill 蓝图运行 normal/blocked 前向回放 |
| `skill_transcript_runner` | runnable | 对首批 61 个 Skill 蓝图运行多轮 transcript 回放 |

Schema：`schemas/agent-route-smoke-runner.schema.json`

Schema：`schemas/agent-runtime-dry-run-runner.schema.json`

Schema：`schemas/agent-runtime-handoff-builder.schema.json`

Schema：`schemas/agent-tool-definition-exporter.schema.json`

Schema：`schemas/agent-tool-definition-validator.schema.json`

Schema：`schemas/agent-tool-registry-builder.schema.json`

Schema：`schemas/agent-tool-wrapper-manifest-builder.schema.json`

Schema：`schemas/agent-workflow-router.schema.json`

Schema：`schemas/codex-skill-blueprint-validator.schema.json`

Schema：`schemas/codex-skill-installer.schema.json`

Schema：`schemas/content-review-feedback-recorder.schema.json`

Schema：`schemas/content-review-packet-builder.schema.json`

Schema：`schemas/external-evidence-intake-builder.schema.json`

Schema：`schemas/mystic-intake.schema.json`

Schema：`schemas/mystic-output-lint.schema.json`

Schema：`schemas/knowledge-coverage-audit.schema.json`

Schema：`schemas/knowledge-navigation-builder.schema.json`

Schema：`schemas/pilot-readiness-report.schema.json`

Schema：`schemas/release-gate-runner.schema.json`

Schema：`schemas/release-manifest-builder.schema.json`

Schema：`schemas/skill-install-readiness-report.schema.json`

Schema：`schemas/sop-traceability-matrix-builder.schema.json`

Schema：`schemas/tool-manifest-builder.schema.json`

Schema：`schemas/symbolic-case-library.schema.json`

Schema：`schemas/symbolic-depth-lookup.schema.json`

Schema：`schemas/transcript-anonymizer.schema.json`

Schema：`schemas/transcript-fixture-builder.schema.json`

Schema：`schemas/skill-replay-runner.schema.json`

Schema：`schemas/skill-transcript-runner.schema.json`

## 择日/黄历工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `date_selection_guard` | runnable | 守门择日请求中的专业替代、医疗/财务择时、危险仪式和决定论风险 |
| `almanac_symbol_lookup` | runnable | 查询宜、忌、冲、煞、黄道吉日等黄历术语的来源限制和安全解释 |
| `date_constraint_recorder` | runnable | 记录事件类型、候选日期、不可用日期、参与人、现实约束和黄历来源 |
| `date_option_ranker` | runnable | 按现实约束优先、象征偏好次之排序候选日期，不计算权威黄历 |

Schema：`schemas/date-selection-guard.schema.json`

Schema：`schemas/almanac-symbol-lookup.schema.json`

Schema：`schemas/date-constraint-recorder.schema.json`

Schema：`schemas/date-option-ranker.schema.json`

## 求签/签文工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `oracle_lot_request_guard` | runnable | 守门求签/解签中的专业替代、决定论、操控、第三方隐私和反复抽签依赖 |
| `oracle_lot_record_builder` | runnable | 记录用户问题、签文、签号、签等、来源和抽签方法 |
| `oracle_lot_symbol_lookup` | runnable | 查询签等、签文、寺庙来源、月老签、事业签和抽签方法的安全解释骨架 |
| `oracle_lot_interpretation_planner` | runnable | 组合签文记录和符号查询，生成非保证、非恐吓、非专业替代的解签计划 |

Schema：`schemas/oracle-lot-request-guard.schema.json`

Schema：`schemas/oracle-lot-record-builder.schema.json`

Schema：`schemas/oracle-lot-symbol-lookup.schema.json`

Schema：`schemas/oracle-lot-interpretation-planner.schema.json`

## 神谕卡工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `oracle_card_request_guard` | runnable | 守门神谕卡请求中的专业替代、命运断言、财务投机、第三方隐私/操控、超自然恐惧和反复依赖风险 |
| `oracle_card_draw_recorder` | runnable | 记录神谕卡问题、牌组名称、牌阵、牌名/关键词、位置、来源和缺失字段 |
| `oracle_card_symbol_lookup` | runnable | 查询门、桥、种子、河流、月亮、羽毛等常见神谕卡图像母题的安全解释提示 |
| `oracle_card_interpretation_planner` | runnable | 组合抽牌记录和图像母题，生成不编造牌组权威牌义、现实证据优先的神谕卡咨询计划 |

Schema：`schemas/oracle-card-request-guard.schema.json`

Schema：`schemas/oracle-card-draw-recorder.schema.json`

Schema：`schemas/oracle-card-symbol-lookup.schema.json`

Schema：`schemas/oracle-card-interpretation-planner.schema.json`

## 扑克牌占卜工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `cartomancy_request_guard` | runnable | 守门扑克牌占卜请求中的专业替代、财务投机、重复抽牌依赖和决定论风险 |
| `cartomancy_draw_recorder` | runnable | 记录扑克牌问题、牌组类型、牌阵、牌面、抽牌来源和缺失字段 |
| `cartomancy_card_lookup` | runnable | 查询红桃、黑桃、方片、梅花、A-10、J/Q/K 和 Joker 的安全象征提示 |
| `cartomancy_interpretation_planner` | runnable | 组合抽牌记录和牌面查询，生成现实证据优先、低风险的纸牌占卜反思计划 |

Schema：`schemas/cartomancy-request-guard.schema.json`

Schema：`schemas/cartomancy-draw-recorder.schema.json`

Schema：`schemas/cartomancy-card-lookup.schema.json`

Schema：`schemas/cartomancy-interpretation-planner.schema.json`

## 星骰/占卜骰工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `dice_request_guard` | runnable | 守门星骰/占卜骰请求中的专业替代、财务投机、重复掷骰依赖和决定论风险 |
| `dice_roll_recorder` | runnable | 记录星骰或占卜骰问题、骰面、来源、体系和缺失字段 |
| `dice_symbol_lookup` | runnable | 查询行星、星座、宫位和常见占卜骰面象征，不确认预言或外部事实 |
| `dice_interpretation_planner` | runnable | 组合骰面记录和象征查询，生成现实证据优先、低风险的骰面反思计划 |

Schema：`schemas/dice-request-guard.schema.json`

Schema：`schemas/dice-roll-recorder.schema.json`

Schema：`schemas/dice-symbol-lookup.schema.json`

Schema：`schemas/dice-interpretation-planner.schema.json`

## 茶叶/咖啡渣占卜工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `tasseography_request_guard` | runnable | 守门茶叶/咖啡渣占卜请求中的专业替代、财务投机、重复观察依赖、不安全摄入和决定论风险 |
| `tasseography_pattern_recorder` | runnable | 记录问题、媒介、杯底区域、图案来源、观察形状和缺失字段 |
| `tasseography_symbol_lookup` | runnable | 查询鸟、路、山、树、心形、圆环、星、鱼、钥匙等常见杯底图案象征 |
| `tasseography_interpretation_planner` | runnable | 组合图案记录和象征查询，生成现实证据优先、低风险的杯底图案反思计划 |

Schema：`schemas/tasseography-request-guard.schema.json`

Schema：`schemas/tasseography-pattern-recorder.schema.json`

Schema：`schemas/tasseography-symbol-lookup.schema.json`

Schema：`schemas/tasseography-interpretation-planner.schema.json`

## 雷诺曼卡工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `lenormand_request_guard` | runnable | 守门雷诺曼卡请求中的专业替代、命运断言、财务投机、第三方隐私/操控、超自然恐惧和反复依赖风险 |
| `lenormand_draw_recorder` | runnable | 记录雷诺曼问题、牌阵、牌名、位置、来源和缺失字段 |
| `lenormand_card_lookup` | runnable | 查询 36 张雷诺曼牌的中文/英文别名、关键词、安全解释提示和禁止用途 |
| `lenormand_interpretation_planner` | runnable | 组合抽牌记录、逐牌牌义和相邻牌对，生成现实证据优先、非决定论的雷诺曼咨询计划 |

Schema：`schemas/lenormand-request-guard.schema.json`

Schema：`schemas/lenormand-draw-recorder.schema.json`

Schema：`schemas/lenormand-card-lookup.schema.json`

Schema：`schemas/lenormand-interpretation-planner.schema.json`

## 水晶/能量石工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `crystal_request_guard` | runnable | 守门水晶/能量石请求中的专业替代、医疗疗愈、财务承诺、危险摄入、高价购买、超自然恐惧和反复依赖风险 |
| `crystal_item_recorder` | runnable | 记录水晶意图、已有或候选物件、使用场景、来源、预算或已有物件说明 |
| `crystal_symbol_lookup` | runnable | 查询白水晶、紫水晶、粉晶、黄水晶、黑曜石等常见水晶的象征解释提示和禁止用途 |
| `crystal_use_planner` | runnable | 组合物件记录和象征查询，生成低成本、可逆、非伤害的水晶提醒物使用计划 |

Schema：`schemas/crystal-request-guard.schema.json`

Schema：`schemas/crystal-item-recorder.schema.json`

Schema：`schemas/crystal-symbol-lookup.schema.json`

Schema：`schemas/crystal-use-planner.schema.json`

## 蜡烛火焰/蜡泪工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `candle_request_guard` | runnable | 守门蜡烛火焰/蜡泪请求中的明火步骤、危险仪式、专业替代、财务投机、鬼神恐惧、第三方隐私、操控和反复依赖风险 |
| `candle_observation_recorder` | runnable | 记录已安全结束、LED 蜡烛或照片笔记中的火焰、蜡泪、烟和观察来源 |
| `candle_symbol_lookup` | runnable | 查询稳定火焰、摇曳火焰、烟、河流状蜡泪、山形蜡泪等常见观察的安全象征解释 |
| `candle_interpretation_planner` | runnable | 组合观察记录和符号查询，生成火源安全优先、非预言、非驱邪证明的蜡烛象征咨询计划 |

Schema：`schemas/candle-request-guard.schema.json`

Schema：`schemas/candle-observation-recorder.schema.json`

Schema：`schemas/candle-symbol-lookup.schema.json`

Schema：`schemas/candle-interpretation-planner.schema.json`

## 香火/香灰/烟形工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `incense_request_guard` | runnable | 守门香火/香灰/烟形请求中的明火燃烧、危险仪式、摄入香灰、专业替代、财务投机、鬼神恐惧、第三方隐私、操控、高价购买和反复依赖风险 |
| `incense_observation_recorder` | runnable | 记录已安全结束、照片记录或无烟替代中的香灰形状、烟雾描述、香头余光和观察来源 |
| `incense_symbol_lookup` | runnable | 查询直上烟、飘散烟、旋卷烟、塔形香灰、断裂香灰、桥形香灰等常见观察的安全象征解释 |
| `incense_interpretation_planner` | runnable | 组合观察记录和符号查询，生成火源/通风安全优先、非预言、非驱邪证明的香火象征咨询计划 |

Schema：`schemas/incense-request-guard.schema.json`

Schema：`schemas/incense-observation-recorder.schema.json`

Schema：`schemas/incense-symbol-lookup.schema.json`

Schema：`schemas/incense-interpretation-planner.schema.json`

## 芳香/精油/气味象征工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `aroma_request_guard` | runnable | 守门芳香、香薰、精油、气味和扩香请求中的医疗替代、内服涂抹、孕婴宠物过敏、消防、驱邪、结果保证、高价购买和反复依赖风险 |
| `aroma_context_recorder` | runnable | 记录气味物件、来源、使用方式、空间、时长、通风、安全背景、现实约束和缺失字段 |
| `aroma_symbol_lookup` | runnable | 查询薰衣草、玫瑰、柑橘、薄荷、乳香、檀香、雪松、迷迭香、香包、扩香、闻香纸和通风等安全象征提示 |
| `aroma_practice_planner` | runnable | 组合气味语境和符号查询，生成短时、非接触、可停止、低成本、非治疗的气味象征计划 |

Schema：`schemas/aroma-request-guard.schema.json`

Schema：`schemas/aroma-context-recorder.schema.json`

Schema：`schemas/aroma-symbol-lookup.schema.json`

Schema：`schemas/aroma-practice-planner.schema.json`

## 草本/香草/植物魔法象征工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `herbal_request_guard` | runnable | 守门草本、香草、草药、植物魔法和草药袋请求中的医疗替代、内服外敷、孕婴宠物过敏、野采辨毒、消防烟雾、驱邪、爱情咒诅咒、高价购买和反复依赖风险 |
| `herbal_context_recorder` | runnable | 记录植物物件、来源、使用方式、容器形式、空间、时长、安全背景、现实约束和缺失字段 |
| `herbal_symbol_lookup` | runnable | 查询迷迭香、鼠尾草、月桂叶、艾草、薄荷、洋甘菊、罗勒、薰衣草、荨麻、盐碗、草药袋和植物意图卡等安全象征提示 |
| `herbal_practice_planner` | runnable | 组合草本语境和符号查询，生成非接触、无火、可停止、低成本、非治疗的植物象征计划 |

Schema：`schemas/herbal-request-guard.schema.json`

Schema：`schemas/herbal-context-recorder.schema.json`

Schema：`schemas/herbal-symbol-lookup.schema.json`

Schema：`schemas/herbal-practice-planner.schema.json`

## Sigil/符号印记/魔法阵象征工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `sigil_request_guard` | runnable | 守门 sigil、符号印记、魔法阵和 seal 请求中的血、身体伤害、纹身永久化、焚烧、召唤驱邪、诅咒操控、结果保证、专业替代、违法财务、高价购买和反复依赖风险 |
| `sigil_context_recorder` | runnable | 记录意图短句、符号元素、来源、媒介、激活方式、展示位置、时长、安全背景、现实约束和缺失字段 |
| `sigil_symbol_lookup` | runnable | 查询圆、线、三角、方形、螺旋、十字/交叉、星形、眼睛、钥匙、种子、字母合并和日志激活等安全象征提示 |
| `sigil_practice_planner` | runnable | 组合 sigil 语境和符号查询，生成纸面/数字草稿、可擦除、无火、不接触身体、不永久化、低成本、可停止的符号象征计划 |

Schema：`schemas/sigil-request-guard.schema.json`

Schema：`schemas/sigil-context-recorder.schema.json`

Schema：`schemas/sigil-symbol-lookup.schema.json`

Schema：`schemas/sigil-practice-planner.schema.json`

## 占杖/寻水杖/探测棒象征工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `dowsing_request_guard` | runnable | 守门占杖、寻水杖、探测棒、dowsing rods 和 L-rods 请求中的地下管线、开挖打井、水源资源、医疗地气、专业替代、房产合同、第三方定位、驱邪、高价购买和反复依赖风险 |
| `dowsing_context_recorder` | runnable | 记录工具类型、观察目标、空间/地图、动作记录、授权范围、安全背景、现实约束、时长和缺失字段 |
| `dowsing_symbol_lookup` | runnable | 查询双杆交叉、双杆张开、双杆平行、单杆摆动、地图标记、门槛、角落、路线、暂停标记和记录网格等安全象征提示 |
| `dowsing_practice_planner` | runnable | 组合占杖语境和符号查询，生成本人授权空间、非开挖、非定位、非治疗、低成本、可停止的空间象征计划 |

Schema：`schemas/dowsing-request-guard.schema.json`

Schema：`schemas/dowsing-context-recorder.schema.json`

Schema：`schemas/dowsing-symbol-lookup.schema.json`

Schema：`schemas/dowsing-practice-planner.schema.json`

## 身体征兆/眼跳/耳鸣/喷嚏象征工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `body_omen_request_guard` | runnable | 守门眼跳、耳鸣、喷嚏、耳热、脸热、手心痒和肉跳请求中的医疗红旗、专业替代、灾祸恐吓、彩票投资、第三方标签、驱邪、危险试验和反复依赖风险 |
| `body_omen_context_recorder` | runnable | 记录征兆类型、身体位置、时间、持续频率、感受、健康背景、普通诱因、现实约束和停止条件 |
| `body_omen_symbol_lookup` | runnable | 查询左眼跳、右眼跳、耳鸣/耳响、耳热、喷嚏、脸热、手心痒、肉跳、时辰和身体照料备注等安全象征提示 |
| `body_omen_reflection_planner` | runnable | 组合身体征兆语境和符号查询，生成非诊断、非灾祸、非彩票投资、低成本、可停止的身体照料反思计划 |

Schema：`schemas/body-omen-request-guard.schema.json`

Schema：`schemas/body-omen-context-recorder.schema.json`

Schema：`schemas/body-omen-symbol-lookup.schema.json`

Schema：`schemas/body-omen-reflection-planner.schema.json`

## 水晶球/镜面/水面凝视工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `scrying_request_guard` | runnable | 守门水晶球/镜面/水面凝视请求中的长时间凝视、追求幻觉、专业替代、财务投机、鬼神恐惧、第三方隐私、操控、身份标签和反复依赖风险 |
| `scrying_observation_recorder` | runnable | 记录短时已结束、照片或记忆记录中的媒介、视觉符号、表面状态、感受和观察来源 |
| `scrying_symbol_lookup` | runnable | 查询雾面、清晰表面、波纹、门、道路、鸟、山、圆环、影子等常见观察的安全象征解释 |
| `scrying_interpretation_planner` | runnable | 组合观察记录和符号查询，生成 grounding 优先、非预言、非灵体证明的凝视象征咨询计划 |

Schema：`schemas/scrying-request-guard.schema.json`

Schema：`schemas/scrying-observation-recorder.schema.json`

Schema：`schemas/scrying-symbol-lookup.schema.json`

Schema：`schemas/scrying-interpretation-planner.schema.json`

## 骨/贝壳/石子/符物抛掷工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `casting_lots_request_guard` | runnable | 守门骨、贝壳、石子、符物/小物抛掷请求中的专业替代、财务赌博、灵异恐惧、遗骸/动物伤害、第三方隐私、操控和反复依赖风险 |
| `casting_lots_layout_recorder` | runnable | 记录符物抛掷体系、投掷垫/区域、来源、物件、方位、关系和缺失字段 |
| `casting_lots_symbol_lookup` | runnable | 查询骨片、贝壳、石子、钥匙、硬币、戒指、羽毛、种子、线、小镜和区域/关系的安全象征解释 |
| `casting_lots_interpretation_planner` | runnable | 组合盘面记录和符号查询，生成非预言、非灵异证明、材料安全优先的符物抛掷象征咨询计划 |

Schema：`schemas/casting-lots-request-guard.schema.json`

Schema：`schemas/casting-lots-layout-recorder.schema.json`

Schema：`schemas/casting-lots-symbol-lookup.schema.json`

Schema：`schemas/casting-lots-interpretation-planner.schema.json`

## 测字/拆字工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `cezi_request_guard` | runnable | 守门测字/拆字请求中的专业替代、财务赌博、确定预言、第三方隐私、操控、灵异恐惧、寿命/人格标签、儿童标签和反复依赖风险 |
| `cezi_character_recorder` | runnable | 记录字例、来源、部件/结构、可见特征、用户第一联想、关注主题和缺失字段 |
| `cezi_symbol_lookup` | runnable | 查询木、水、火、土、金、心、口、言、人、手、日、月、门、辶、宀、山、田、艹和常见结构/形态的安全象征解释 |
| `cezi_interpretation_planner` | runnable | 组合字例记录和部件查询，生成非预言、非灵异证明、反标签的测字/拆字象征咨询计划 |

Schema：`schemas/cezi-request-guard.schema.json`

Schema：`schemas/cezi-character-recorder.schema.json`

Schema：`schemas/cezi-symbol-lookup.schema.json`

Schema：`schemas/cezi-interpretation-planner.schema.json`

## 花语/植物象征工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `flower_request_guard` | runnable | 守门花语、花占、送花和植物象征请求中的专业替代、医疗疗愈、过敏/宠物安全判断、财务投机、灵异恐惧、第三方读心、高价购买和反复依赖风险 |
| `flower_item_recorder` | runnable | 记录花材、颜色、数量、用途、来源、预算、过敏/宠物安全备注和缺失字段 |
| `flower_symbol_lookup` | runnable | 查询玫瑰、百合、向日葵、薰衣草、雏菊、莲花、松、竹等常见花材/植物的安全象征解释 |
| `flower_interpretation_planner` | runnable | 组合花材记录和象征查询，生成非疗愈、非预言、现实关系边界优先的花语/植物象征咨询计划 |

Schema：`schemas/flower-request-guard.schema.json`

Schema：`schemas/flower-item-recorder.schema.json`

Schema：`schemas/flower-symbol-lookup.schema.json`

Schema：`schemas/flower-interpretation-planner.schema.json`

## 动物征兆/鸟兽虫鱼工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `animal_omen_request_guard` | runnable | 守门动物征兆、鸟兽虫鱼和动物预兆请求中的动物伤害、危险接触、公共卫生/虫害替代、确定灾祸、灵异恐惧、财务赌博、第三方读心和反复依赖风险 |
| `animal_omen_observation_recorder` | runnable | 记录动物、行为、地点、时间、频率、来源、安全背景和反思焦点 |
| `animal_omen_symbol_lookup` | runnable | 查询鸟、乌鸦、猫头鹰、燕子、蝴蝶、飞蛾、蜘蛛、蜜蜂、蛇、猫狗、蝙蝠和老鼠等常见动物征兆象征 |
| `animal_omen_interpretation_planner` | runnable | 组合观察记录和象征查询，生成现实安全优先、非预言、非灵异证明的动物征兆解释计划 |

Schema：`schemas/animal-omen-request-guard.schema.json`

Schema：`schemas/animal-omen-observation-recorder.schema.json`

Schema：`schemas/animal-omen-symbol-lookup.schema.json`

Schema：`schemas/animal-omen-interpretation-planner.schema.json`

## 气场/脉轮/能量感受工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `aura_chakra_request_guard` | runnable | 守门气场、脉轮、灵气和能量感受请求中的医疗/心理健康替代、灵异攻击、身份标签、财务赌博、第三方读心、付费疗愈压力和反复依赖风险 |
| `aura_chakra_sensation_recorder` | runnable | 记录中心/脉轮、颜色、身体感受、场景、持续时间、强度、grounding 备注和反思焦点 |
| `aura_chakra_symbol_lookup` | runnable | 查询海底轮、脐轮、太阳神经丛、心轮、喉轮、眉心轮、顶轮、气场颜色和常见感受的安全象征解释 |
| `aura_chakra_reflection_planner` | runnable | 组合感受记录和符号查询，生成身体感受优先、非诊断、非灵异证明的气场/脉轮反思计划 |

Schema：`schemas/aura-chakra-request-guard.schema.json`

Schema：`schemas/aura-chakra-sensation-recorder.schema.json`

Schema：`schemas/aura-chakra-symbol-lookup.schema.json`

Schema：`schemas/aura-chakra-reflection-planner.schema.json`

## 前世/阿卡西/灵魂课题工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `past_life_request_guard` | runnable | 守门前世、阿卡西、灵魂契约和业力关系请求中的记忆恢复、创伤确认、专业替代、宿命论、第三方隐私、关系操控、付费压力和反复依赖风险 |
| `past_life_narrative_recorder` | runnable | 记录来源语境、场景、角色、符号、情绪、当下现实锚点和同意/隐私备注 |
| `past_life_symbol_lookup` | runnable | 查询阿卡西图书馆、门槛、水、战场、寺院、契约、同行者、流放、疗愈者、工匠和孩子等安全象征 |
| `past_life_reflection_planner` | runnable | 组合叙事记录和符号查询，生成非事实确认、非记忆恢复、现实锚点优先的前世/阿卡西反思计划 |

Schema：`schemas/past-life-request-guard.schema.json`

Schema：`schemas/past-life-narrative-recorder.schema.json`

Schema：`schemas/past-life-symbol-lookup.schema.json`

Schema：`schemas/past-life-reflection-planner.schema.json`

## 月相/月亮周期工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `moon_phase_request_guard` | runnable | 守门月相、月亮周期、新月许愿和满月释放请求中的专业替代、医疗/生育、危险仪式、显化保证、财务赌博、第三方操控、付费压力和反复依赖风险 |
| `moon_phase_context_recorder` | runnable | 记录月相、主题、意图、现实约束、日期备注、来源备注和反思焦点 |
| `moon_phase_symbol_lookup` | runnable | 查询新月、娥眉月、上弦月、盈凸月、满月、亏凸月、下弦月、残月、月食、蓝月和超级月亮等安全象征 |
| `moon_phase_reflection_planner` | runnable | 组合月相上下文和符号查询，生成非显化保证、无危险仪式、现实行动优先的周期反思计划 |

Schema：`schemas/moon-phase-request-guard.schema.json`

Schema：`schemas/moon-phase-context-recorder.schema.json`

Schema：`schemas/moon-phase-symbol-lookup.schema.json`

Schema：`schemas/moon-phase-reflection-planner.schema.json`

## 通灵/高我/灵性讯息工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `spirit_message_request_guard` | runnable | 守门通灵、高我、守护灵、天使讯息和自动书写请求中的命令式声音、幻听幻视、专业替代、灵体事实确认、第三方隐私、财务法律、付费压力和反复依赖风险 |
| `spirit_message_record_builder` | runnable | 记录讯息来源、原句、符号、情绪、现实锚点、同意/隐私备注和反思焦点 |
| `spirit_message_symbol_lookup` | runnable | 查询高我、守护灵、天使讯息、祖先意象、内在声音、自动书写、羽毛、光、门和名字等安全象征解释 |
| `spirit_message_reflection_planner` | runnable | 组合讯息记录和符号查询，生成非事实确认、非命令、现实锚点优先的通灵/高我讯息象征写作计划 |

Schema：`schemas/spirit-message-request-guard.schema.json`

Schema：`schemas/spirit-message-record-builder.schema.json`

Schema：`schemas/spirit-message-symbol-lookup.schema.json`

Schema：`schemas/spirit-message-reflection-planner.schema.json`

## 物品感应/触物占卜工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `psychometry_request_guard` | runnable | 守门物品感应、触物占卜和 object reading 请求中的失踪犯罪、第三方隐私、未经同意、灵体事实、专业替代、医疗安全、财务法律、真伪归属、付费净化和反复依赖风险 |
| `psychometry_object_recorder` | runnable | 记录物件类型、来源备注、拥有/同意状态、可见特征、第一联想、情绪、现实锚点和反思焦点 |
| `psychometry_symbol_lookup` | runnable | 查询戒指、项链/吊坠、手表、钥匙、照片、旧书、衣物、石头、遗物和二手物等安全象征解释 |
| `psychometry_reflection_planner` | runnable | 组合物件记录和象征查询，生成非事实确认、非鉴定、非隐私读取的物品感应象征反思计划 |

Schema：`schemas/psychometry-request-guard.schema.json`

Schema：`schemas/psychometry-object-recorder.schema.json`

Schema：`schemas/psychometry-symbol-lookup.schema.json`

Schema：`schemas/psychometry-reflection-planner.schema.json`

## 书占/随机翻书工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `bibliomancy_request_guard` | runnable | 守门书占、随机翻书和 bibliomancy 请求中的专业替代、医疗心理健康、财务法律、决定论、第三方隐私、经文/经典权威命令、长段版权文本和反复依赖风险 |
| `bibliomancy_source_recorder` | runnable | 记录书名/来源、来源类型、抽取方式、页码/位置、用户自提供短句、关键词、情绪、现实锚点和反思焦点 |
| `bibliomancy_symbol_lookup` | runnable | 查询页码、随机翻开、句子、关键词、诗、经典/经文、小说、笔记、门和道路等安全象征解释 |
| `bibliomancy_reflection_planner` | runnable | 组合来源记录和象征查询，生成非决定论、非权威命令、非版权文本获取的书占反思计划 |

Schema：`schemas/bibliomancy-request-guard.schema.json`

Schema：`schemas/bibliomancy-source-recorder.schema.json`

Schema：`schemas/bibliomancy-symbol-lookup.schema.json`

Schema：`schemas/bibliomancy-reflection-planner.schema.json`

## 天象/云形征兆工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `sky_omen_request_guard` | runnable | 守门天象、云形、彩虹、日月晕和天气征兆请求中的灾祸恐吓、天气安全替代、危险暴露、专业替代、第三方隐私、灵体事实和反复依赖风险 |
| `sky_omen_observation_recorder` | runnable | 记录观察对象、形状、颜色、地点时间、天气安全背景、情绪、现实锚点和反思焦点 |
| `sky_omen_symbol_lookup` | runnable | 查询云、龙形云、鸟形云、彩虹、日晕、月晕、闪电、雷声、霞光和雾等安全象征提示 |
| `sky_omen_reflection_planner` | runnable | 组合天空观察记录和象征查询，生成非灾祸预言、非天气预报、非灵体事实的低风险反思计划 |

Schema：`schemas/sky-omen-request-guard.schema.json`

Schema：`schemas/sky-omen-observation-recorder.schema.json`

Schema：`schemas/sky-omen-symbol-lookup.schema.json`

Schema：`schemas/sky-omen-reflection-planner.schema.json`

## 祈愿/显化/愿望仪式工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `manifestation_request_guard` | runnable | 守门祈愿、许愿、显化、愿望清单和意图设定请求中的结果保证、专业替代、财务投机、医疗生育、第三方操控、诅咒报复、危险仪式、高价购买、灵体事实和反复依赖风险 |
| `manifestation_intention_recorder` | runnable | 记录愿望主题、意图句、象征物、情绪、现实锚点、可控行动、复盘时间和停止条件 |
| `manifestation_symbol_lookup` | runnable | 查询意图、祈愿纸、月亮、种子、钥匙、水杯、红绳、蜡烛、镜子和感恩等安全象征提示 |
| `manifestation_reflection_planner` | runnable | 组合意图记录和象征查询，生成非结果保证、非专业替代、非第三方控制的低风险行动/复盘计划 |

Schema：`schemas/manifestation-request-guard.schema.json`

Schema：`schemas/manifestation-intention-recorder.schema.json`

Schema：`schemas/manifestation-symbol-lookup.schema.json`

Schema：`schemas/manifestation-reflection-planner.schema.json`

## 宠物沟通/动物灵性讯息工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `pet_communication_request_guard` | runnable | 守门宠物沟通、动物沟通、宠物灵性讯息和亡宠怀念请求中的兽医替代/急症、走失定位、真实讯息保证、亡宠事实、第三方指认、高价付费和反复依赖风险 |
| `pet_communication_context_recorder` | runnable | 记录宠物种类、关系、可见行为、时间背景、健康/兽医边界、用户情绪、照护动作和现实锚点 |
| `pet_communication_symbol_lookup` | runnable | 查询猫、狗、躲起来、呼噜、叫声、尾巴、食欲、门口、亡宠怀念和照片等安全象征提示 |
| `pet_communication_reflection_planner` | runnable | 组合宠物语境记录和象征查询，生成非兽医替代、非真实讯息确认、非走失定位的低风险照护/怀念计划 |

Schema：`schemas/pet-communication-request-guard.schema.json`

Schema：`schemas/pet-communication-context-recorder.schema.json`

Schema：`schemas/pet-communication-symbol-lookup.schema.json`

Schema：`schemas/pet-communication-reflection-planner.schema.json`

## 同步性/天使数字/重复征兆工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `synchronicity_request_guard` | runnable | 守门同步性、天使数字、重复数字、重复征兆和宇宙讯号请求中的危险寻找、专业决策替代、宇宙命令、第三方读心、焦虑反复确认、灵体事实和高价付费风险 |
| `synchronicity_event_recorder` | runnable | 记录重复符号、出现频率、出现场景、情绪、现实锚点、可控行动和停止条件 |
| `synchronicity_symbol_lookup` | runnable | 查询 1111、222、333、444、555、镜像时间、反复出现的歌、名字、动物和羽毛等同步性象征提示 |
| `synchronicity_reflection_planner` | runnable | 组合重复征兆记录和象征查询，生成非命令化、非预测、非专业替代、非读心的低风险记录与行动反思计划 |

Schema：`schemas/synchronicity-request-guard.schema.json`

Schema：`schemas/synchronicity-event-recorder.schema.json`

Schema：`schemas/synchronicity-symbol-lookup.schema.json`

Schema：`schemas/synchronicity-reflection-planner.schema.json`

## 水逆/行星逆行/星象天气工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `planetary_retrograde_request_guard` | runnable | 守门水逆、行星逆行、星象天气和逆行周期请求中的专业替代、宿命归因、第三方读心/操控、危险仪式、高价转运、恐慌依赖和灵体事实风险 |
| `planetary_retrograde_context_recorder` | runnable | 记录逆行主题、关注领域、现实事项、情绪、现实限制、可控行动、复盘时间和停止查询条件 |
| `planetary_retrograde_symbol_lookup` | runnable | 查询水星逆行/水逆、金星逆行、火星逆行、木星逆行、土星逆行、逆行阴影期、顺行转向和星象天气等象征提示 |
| `planetary_retrograde_reflection_planner` | runnable | 组合逆行语境记录和象征查询，生成非宿命化、非专业替代、非读心、非恐慌依赖的复盘与行动检查计划 |

Schema：`schemas/planetary-retrograde-request-guard.schema.json`

Schema：`schemas/planetary-retrograde-context-recorder.schema.json`

Schema：`schemas/planetary-retrograde-symbol-lookup.schema.json`

Schema：`schemas/planetary-retrograde-reflection-planner.schema.json`

## 恶眼/能量防护/断联工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `spiritual_protection_request_guard` | runnable | 守门恶眼、能量防护、灵性防护、能量断联和防小人请求中的迫害确认、诅咒报复、危险仪式、专业/现实安全替代、第三方指认、关系操控、高价购买和反复依赖风险 |
| `spiritual_protection_context_recorder` | runnable | 记录防护主题、触发场景、身体/情绪感受、现实安全背景、边界动作、提醒物、复盘时间和停止条件 |
| `spiritual_protection_symbol_lookup` | runnable | 查询恶眼、蓝眼护符、保护罩/防护罩、能量断联、盐、黑色石、镜子和 grounding 等防护象征提示 |
| `spiritual_protection_reflection_planner` | runnable | 组合防护语境记录和象征查询，生成非指认、非报复、非危险仪式、非专业替代、非高价购买的边界整理与现实安全检查计划 |

Schema：`schemas/spiritual-protection-request-guard.schema.json`

Schema：`schemas/spiritual-protection-context-recorder.schema.json`

Schema：`schemas/spiritual-protection-symbol-lookup.schema.json`

Schema：`schemas/spiritual-protection-reflection-planner.schema.json`

## 神明/祖先/供奉/祭拜工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `deity_ancestor_request_guard` | runnable | 守门神明、祖先、供奉、祭拜、祭祖、供桌和还愿请求中的神谕命令、灾祸恐吓、危险仪式、专业替代、第三方指认、强迫家人、高价法事和反复依赖风险 |
| `deity_ancestor_context_recorder` | runnable | 记录来源传统、对象、场合、意图、已有物件、纪念/供奉动作、家庭边界、安全背景、复盘时间和停止条件 |
| `deity_ancestor_symbol_lookup` | runnable | 查询供桌/神台、香、清水、水果供品、祖先牌位/照片、还愿、祈祷和清洁整理等供奉纪念象征提示 |
| `deity_ancestor_reflection_planner` | runnable | 组合供奉语境记录和象征查询，生成非神谕命令、非危险仪式、非强迫供奉、非高价法事的文化纪念与感恩计划 |

Schema：`schemas/deity-ancestor-request-guard.schema.json`

Schema：`schemas/deity-ancestor-context-recorder.schema.json`

Schema：`schemas/deity-ancestor-symbol-lookup.schema.json`

Schema：`schemas/deity-ancestor-reflection-planner.schema.json`

## 鬼压床/梦魇/睡前灵异恐惧工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `sleep_paralysis_request_guard` | runnable | 守门鬼压床、压床、睡眠瘫痪、梦魇、夜惊和床边人影请求中的身体风险、严重睡眠受损、幻听幻视、自伤伤人、危险仪式、专业替代、灵体事实、高价法事和反复依赖风险 |
| `sleep_paralysis_context_recorder` | runnable | 记录发生模式、醒来状态、身体感、夜间印象、房间环境、近期压力、睡眠背景、安定动作、白天影响、复盘时间和停止条件 |
| `sleep_paralysis_symbol_lookup` | runnable | 查询鬼压床/睡眠瘫痪体验、胸口压迫、黑影/床边人影、动不了、门窗、床边灯、呼吸锚点和睡眠记录等夜间恐惧象征提示 |
| `sleep_paralysis_reflection_planner` | runnable | 组合睡眠体验语境记录和象征查询，生成非灵体确认、非危险仪式、非专业替代的睡眠记录、醒后安定和现实安全检查计划 |

Schema：`schemas/sleep-paralysis-request-guard.schema.json`

Schema：`schemas/sleep-paralysis-context-recorder.schema.json`

Schema：`schemas/sleep-paralysis-symbol-lookup.schema.json`

Schema：`schemas/sleep-paralysis-reflection-planner.schema.json`

## 招财/财运/财库工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `wealth_luck_request_guard` | runnable | 守门招财、财运、求财、财库、财神、貔貅、金蟾和聚宝盆请求中的投资赌博借贷、收益保证、债务压力、违法诈骗、高价法事、神明命令、操控他人和反复依赖风险 |
| `wealth_luck_context_recorder` | runnable | 记录求财焦点、当前处境、收入渠道、预算边界、已有象征物、可控行动、风险备注、复盘时间和停止条件 |
| `wealth_luck_symbol_lookup` | runnable | 查询财运/招财、财库、财神、貔貅、金蟾、聚宝盆、红包和账本/记账等求财象征提示 |
| `wealth_luck_action_planner` | runnable | 组合求财语境记录和象征查询，生成非投资建议、非收益保证、非高价法事的预算、收入渠道和行动复盘计划 |

Schema：`schemas/wealth-luck-request-guard.schema.json`

Schema：`schemas/wealth-luck-context-recorder.schema.json`

Schema：`schemas/wealth-luck-symbol-lookup.schema.json`

Schema：`schemas/wealth-luck-action-planner.schema.json`

## 桃花/姻缘/人缘工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `relationship_luck_request_guard` | runnable | 守门桃花、姻缘、人缘、月老、红线、红绳和粉晶请求中的跟踪骚扰、操控和合、第三方读心、关系危机、专业替代、结果保证、高价法事和反复依赖风险 |
| `relationship_luck_context_recorder` | runnable | 记录关系焦点、当前语境、同意范围、沟通边界、已有象征物、可控行动、风险备注、复盘时间和停止条件 |
| `relationship_luck_symbol_lookup` | runnable | 查询桃花/人缘、姻缘/正缘、月老、红线/红绳、粉晶、花、镜子和消息/邀约等关系象征提示 |
| `relationship_luck_action_planner` | runnable | 组合关系语境记录和象征查询，生成非读心、非操控、非骚扰、非结果保证的自我呈现、沟通边界和社交行动计划 |

Schema：`schemas/relationship-luck-request-guard.schema.json`

Schema：`schemas/relationship-luck-context-recorder.schema.json`

Schema：`schemas/relationship-luck-symbol-lookup.schema.json`

Schema：`schemas/relationship-luck-action-planner.schema.json`

## 开光/加持/净物工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `consecration_request_guard` | runnable | 守门开光、加持、净物、圣化和物件照料请求中的危险仪式、摄入伤身、专业替代、灵验保证、高价法事、神明恐吓和反复依赖风险 |
| `consecration_context_recorder` | runnable | 记录物件焦点、来源语境、当前用途、已有物件、安全边界、象征动作、风险备注、复盘时间和停止条件 |
| `consecration_symbol_lookup` | runnable | 查询开光、加持、净物、清洁布、清水擦拭、意图卡、固定收纳等低风险物件照料象征提示 |
| `consecration_care_planner` | runnable | 组合开光/净物语境记录和象征查询，生成无火、非摄入、非灵验保证的物件照料和用途提醒计划 |

Schema：`schemas/consecration-request-guard.schema.json`

Schema：`schemas/consecration-context-recorder.schema.json`

Schema：`schemas/consecration-symbol-lookup.schema.json`

Schema：`schemas/consecration-care-planner.schema.json`

## 失物/寻物工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `lost_object_request_guard` | runnable | 守门失物、寻物、找东西和占卜定位请求中的寻人/走失宠物、犯罪证据、专业渠道替代、保证定位、隐私跟踪和反复依赖风险 |
| `lost_object_context_recorder` | runnable | 记录物品描述、最后看见、路线语境、可能区域、已查区域、联系渠道、现实行动、风险备注、复盘时间和停止条件 |
| `lost_object_symbol_lookup` | runnable | 查询最后看见、路线回溯、门口/玄关、口袋/包、桌面/抽屉、交通/座位、联系渠道和复盘停止等搜索线索 |
| `lost_object_search_planner` | runnable | 组合失物语境记录和搜索线索，生成非定位保证、非犯罪指认、非隐私追踪的现实寻物计划 |

Schema：`schemas/lost-object-request-guard.schema.json`

Schema：`schemas/lost-object-context-recorder.schema.json`

Schema：`schemas/lost-object-symbol-lookup.schema.json`

Schema：`schemas/lost-object-search-planner.schema.json`

## 声响净化/铃钵工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `sound_cleansing_request_guard` | runnable | 守门声响净化、铃钵、铃铛、音叉、拍手和诵念请求中的医疗/心理替代、强制驱灵、声音暴露、扰民、效果保证、高价器具和反复依赖风险 |
| `sound_cleansing_context_recorder` | runnable | 记录空间、时段、声音工具、练习意图、音量时长、身体感受、宠物/婴儿/邻里边界、收尾动作、复盘时间和停止条件 |
| `sound_cleansing_symbol_lookup` | runnable | 查询铃钵/颂钵、铃铛/手铃、音叉、拍手/轻叩、诵念、安静收尾、开窗/通风和计时器等低风险声响符号 |
| `sound_cleansing_practice_planner` | runnable | 组合声响净化语境和符号，生成短时、低音量、可停止、非驱邪保证、非治疗替代的空间复位计划 |

Schema：`schemas/sound-cleansing-request-guard.schema.json`

Schema：`schemas/sound-cleansing-context-recorder.schema.json`

Schema：`schemas/sound-cleansing-symbol-lookup.schema.json`

Schema：`schemas/sound-cleansing-practice-planner.schema.json`

## 西洋土占/盾形盘工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `western_geomancy_request_guard` | runnable | 守门西洋土占、盾形占、盾盘和 geomantic figure 请求中的专业替代、投资赌博、确定预言、灵异恐惧、第三方隐私、操控和反复起盘风险 |
| `western_geomancy_chart_recorder` | runnable | 记录起盘来源、生成方式、母亲图、女儿图、侄子图、见证者、裁判者、缺失字段和风险边界 |
| `western_geomancy_figure_lookup` | runnable | 查询 16 个常见 geomantic figures、见证者和裁判者等低风险象征提示 |
| `western_geomancy_interpretation_planner` | runnable | 组合盾形盘记录和图形查询，生成非预测、非投资、非读心、非反复起盘的低风险解释计划 |

Schema：`schemas/western-geomancy-request-guard.schema.json`

Schema：`schemas/western-geomancy-chart-recorder.schema.json`

Schema：`schemas/western-geomancy-figure-lookup.schema.json`

Schema：`schemas/western-geomancy-interpretation-planner.schema.json`

## 九星气学/九宫命星工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `nine_star_ki_request_guard` | runnable | 守门九星气学、九宫命星、本命星、年星和方位请求中的专业替代、投资赌博、关系标签、方位恐吓、高价化解、第三方隐私、操控、确定预言和反复依赖风险 |
| `nine_star_ki_profile_recorder` | runnable | 记录出生年份或已知本命星、月命星、年星、方位焦点、体系来源、节气边界、现实约束和缺失字段 |
| `nine_star_ki_symbol_lookup` | runnable | 查询一白到九紫、本命星、月命星、年星、方位和中宫等低风险象征提示 |
| `nine_star_ki_interpretation_planner` | runnable | 组合九星资料和符号查询，生成非预测、非关系标签、非方位恐吓、非高价化解、非反复依赖的低风险解释计划 |

Schema：`schemas/nine-star-ki-request-guard.schema.json`

Schema：`schemas/nine-star-ki-profile-recorder.schema.json`

Schema：`schemas/nine-star-ki-symbol-lookup.schema.json`

Schema：`schemas/nine-star-ki-interpretation-planner.schema.json`

## 人类图/Human Design 工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `human_design_request_guard` | runnable | 守门人类图、Human Design、bodygraph、类型、策略、内在权威、人生角色、中心、通道和闸门请求中的出生资料隐私、专业替代、诊断、职业财务保证、关系筛选、第三方窥探、操控、付费压力和反复依赖风险 |
| `human_design_chart_recorder` | runnable | 记录资料来源、出生资料最小化范围、类型、策略、内在权威、人生角色、定义中心、通道、闸门、现实约束和缺失字段 |
| `human_design_symbol_lookup` | runnable | 查询显示者、生产者、显示生产者、投射者、反映者、权威、人生角色、中心、通道和闸门等低风险象征提示 |
| `human_design_interpretation_planner` | runnable | 组合人类图资料和符号查询，生成非诊断、非人格定论、非关系筛选、非职业财务保证、非付费压力的低风险解释计划 |

Schema：`schemas/human-design-request-guard.schema.json`

Schema：`schemas/human-design-chart-recorder.schema.json`

Schema：`schemas/human-design-symbol-lookup.schema.json`

Schema：`schemas/human-design-interpretation-planner.schema.json`

## 护符/符箓工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `talisman_request_guard` | runnable | 守门护符/符箓请求中的危险仪式、专业替代、医疗疗愈、诅咒操控、超自然恐惧、摄入和高价购买风险 |
| `talisman_record_builder` | runnable | 记录护符/符箓意图、已有或候选物件、来源、可见符号、使用场景、预算或已有物件说明 |
| `talisman_symbol_lookup` | runnable | 查询平安符、红绳、香囊、门符、纸符等常见护符/符箓象征解释和禁用用途 |
| `talisman_use_planner` | runnable | 组合请求守门、物件记录和符号查询，生成低成本、可逆、非危险的护符/符箓提醒物计划 |

Schema：`schemas/talisman-request-guard.schema.json`

Schema：`schemas/talisman-record-builder.schema.json`

Schema：`schemas/talisman-symbol-lookup.schema.json`

Schema：`schemas/talisman-use-planner.schema.json`

## 生肖/太岁工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `zodiac_request_guard` | runnable | 守门生肖/太岁请求中的专业替代、灾祸恐吓、关系歧视、第三方标签、高价化解和反复依赖风险 |
| `zodiac_profile_recorder` | runnable | 记录生肖/太岁咨询中的年份、生肖、关注主题、本人或第三方范围、来源说明和缺失字段 |
| `zodiac_symbol_lookup` | runnable | 查询十二生肖、本命年、太岁、三合/六合、六冲/相冲等符号的安全解释提示 |
| `zodiac_interpretation_planner` | runnable | 组合生肖资料记录和符号查询，生成文化语境清楚、现实证据优先、低风险的生肖/太岁咨询计划 |

Schema：`schemas/zodiac-request-guard.schema.json`

Schema：`schemas/zodiac-profile-recorder.schema.json`

Schema：`schemas/zodiac-symbol-lookup.schema.json`

Schema：`schemas/zodiac-interpretation-planner.schema.json`

## 五行颜色/开运色工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `color_request_guard` | runnable | 守门五行颜色/开运色请求中的专业替代、财富保证、外貌标签、高价购买和反复依赖风险 |
| `color_profile_recorder` | runnable | 记录颜色咨询中的场景、候选颜色、期望五行、已有物件、预算说明和现实约束 |
| `color_symbol_lookup` | runnable | 查询绿色/青色、红色、黄色/土色、白色/金色、黑色/蓝色等五行颜色象征 |
| `color_palette_planner` | runnable | 组合颜色资料记录和符号查询，生成低成本、可撤回、现实约束优先的配色计划 |

Schema：`schemas/color-request-guard.schema.json`

Schema：`schemas/color-profile-recorder.schema.json`

Schema：`schemas/color-symbol-lookup.schema.json`

Schema：`schemas/color-palette-planner.schema.json`

## 解梦工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `dream_record_builder` | runnable | 记录梦境素材、醒后情绪、现实背景、符号候选和风险信号 |
| `dream_symbol_lookup` | runnable | 查询常见梦境符号的象征层、反思问题和禁止用途 |
| `dream_interpretation_planner` | runnable | 生成非诊断、非预言的解梦分层计划和现实锚点 |

Schema：`schemas/dream-record-builder.schema.json`

Schema：`schemas/dream-symbol-lookup.schema.json`

Schema：`schemas/dream-interpretation-planner.schema.json`

## 民俗工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `folk_custom_lookup` | runnable | 查询节令、禁忌、象征物和人生礼俗的安全文化解释骨架 |
| `folk_source_recorder` | runnable | 记录家人口述、地区来源、宗教语境、文献、网络和商业民俗说法的来源层级与缺失字段 |
| `folk_taboo_reframer` | runnable | 将犯忌倒霉、招鬼、冲撞、害家人等恐吓式禁忌降级为文化解释和现实安全提示 |

Schema：`schemas/folk-custom-lookup.schema.json`

Schema：`schemas/folk-source-recorder.schema.json`

Schema：`schemas/folk-taboo-reframer.schema.json`

## 塔罗工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `tarot_spread_selector` | runnable | 根据问题类型推荐牌阵 |
| `tarot_draw_recorder` | runnable | 记录抽牌、正逆位、牌位 |
| `tarot_draw_simulator` | runnable | 按牌阵随机模拟抽牌，并输出可复现 seed 与 recorder 校验结果 |
| `tarot_card_lookup` | runnable | 检索 78 张塔罗牌义素材 |
| `tarot_interpretation_planner` | runnable | 把牌阵和抽牌记录转成牌位、正逆位、互动和行动解读计划 |
| `tarot_combination_planner` | runnable | 分析多牌组合、逆位聚集、大牌权重、花色/宫廷牌聚集和牌位链接 |

Schema：`schemas/tarot-spread-selector.schema.json`

Schema：`schemas/tarot-draw-recorder.schema.json`

Schema：`schemas/tarot-draw-simulator.schema.json`

Schema：`schemas/tarot-card-lookup.schema.json`

Schema：`schemas/tarot-interpretation-planner.schema.json`

Schema：`schemas/tarot-combination-planner.schema.json`

## 风水工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `fengshui_school_guard` | runnable | 守门玄空飞星、八宅、三合/三元和择日等理气派别请求 |
| `fengshui_observation_recorder` | runnable | 记录图片/文字中的可见空间事实，先事实后术语 |
| `fengshui_space_checklist` | runnable | 根据空间类型生成检查清单 |
| `fengshui_yangzhai_case_library` | runnable | 检索卧室、玄关、厨房、书房/办公室和店铺阳宅安全案例 |
| `fengshui_bagua_mapper` | runnable | 将方位映射为八卦象征、观察问题和低风险调整 |
| `fengshui_recommendation_ranker` | runnable | 按成本、风险、可逆性排序建议 |

Schema：`schemas/fengshui-school-guard.schema.json`

Schema：`schemas/fengshui-observation-recorder.schema.json`

Schema：`schemas/fengshui-space-checklist.schema.json`

Schema：`schemas/fengshui-yangzhai-case-library.schema.json`

Schema：`schemas/fengshui-bagua-mapper.schema.json`

Schema：`schemas/fengshui-recommendation-ranker.schema.json`

## 易经工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `yijing_question_guard` | runnable | 检查一事一问、重复占问、高风险请求并改写问题 |
| `yijing_casting_method_advisor` | runnable | 选择或校验起卦方式，要求模拟起卦同意、外部卦来源，并处理重复占问边界 |
| `yijing_casting_simulator` | runnable | 按三枚铜钱或蓍草概率模型模拟起卦，并输出可复现 seed |
| `yijing_hexagram_record` | runnable | 记录起卦方法、本卦、变爻、变卦 |
| `yijing_hexagram_lookup` | runnable | 按卦号、卦名或上下卦检索 64 卦结构和解读骨架 |
| `yijing_line_lookup` | runnable | 检索 384 爻位索引、阴阳位置关系和变卦骨架 |
| `yijing_source_reference_guard` | runnable | 区分经文、十翼、注疏、现代译注、网络断语和师承说法的引用边界 |

Schema：`schemas/yijing-question-guard.schema.json`

Schema：`schemas/yijing-casting-method-advisor.schema.json`

Schema：`schemas/yijing-casting-simulator.schema.json`

Schema：`schemas/yijing-hexagram-record.schema.json`

Schema：`schemas/yijing-hexagram-lookup.schema.json`

Schema：`schemas/yijing-line-lookup.schema.json`

Schema：`schemas/yijing-source-reference-guard.schema.json`

## 六爻工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `liuyao_chart_recorder` | runnable | 记录外部六爻盘、本卦、变卦、动爻、世应、六亲、六神和取用逻辑，不自动起卦 |
| `liuyao_focus_selector` | runnable | 按问题类型生成候选用神和读盘顺序，并把候选映射到已记录爻位、世应和动爻 |
| `liuyao_symbol_lookup` | runnable | 查询六亲、六神、世应/用神角色和爻位的安全解释骨架 |

Schema：`schemas/liuyao-chart-recorder.schema.json`

Schema：`schemas/liuyao-focus-selector.schema.json`

Schema：`schemas/liuyao-symbol-lookup.schema.json`

## 梅花易数工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `meihua_casting_recorder` | runnable | 记录报数、时间、外应、外部卦盘、体用、动爻、互卦和变卦字段，不自动排卦 |
| `meihua_omen_recorder` | runnable | 记录外应事实、来源、时间关系和取象边界，阻断天意/灾祸式解释 |
| `meihua_relation_interpreter` | runnable | 将有效体用生克关系转成资源、压力、证据问题和低风险行动 |
| `meihua_symbol_lookup` | runnable | 查询体用结构、起卦来源、外应、五行生克和八卦象征的安全解释骨架 |

Schema：`schemas/meihua-casting-recorder.schema.json`

Schema：`schemas/meihua-omen-recorder.schema.json`

Schema：`schemas/meihua-relation-interpreter.schema.json`

Schema：`schemas/meihua-symbol-lookup.schema.json`

## 奇门工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `qimen_method_guard` | runnable | 记录并校验排盘方法、派别、时间、真太阳时策略和节气来源 |
| `qimen_school_reference` | runnable | 查询置闰、拆补、茅山、飞盘、转盘等派别/盘式差异和混用风险 |
| `qimen_chart_record` | runnable | 记录起局信息、九宫盘式、用神和方法限制 |
| `qimen_focus_selector` | runnable | 从盘式字段选择候选用神、相关宫位和读盘顺序 |
| `qimen_chart_generator` | backlog | 在已声明派别和策略后生成盘式 |

Schema：`schemas/qimen-method-guard.schema.json`

Schema：`schemas/qimen-school-reference.schema.json`

Schema：`schemas/qimen-chart-record.schema.json`

Schema：`schemas/qimen-focus-selector.schema.json`

## 命理工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `bazi_ziwei_intake_guard` | runnable | 检查八字/紫微请求的出生资料、隐私同意、未成年人和宿命论风险 |
| `bazi_ziwei_chart_record` | runnable | 记录八字/紫微排盘参数、历法、时区、真太阳时策略、派别和来源 |
| `mingli_school_reference` | runnable | 查询子平、传统八字、现代综合、三合、四化、中州等派别差异和跨系统混用风险 |
| `mingli_symbol_lookup` | runnable | 查询干支、十神、紫微宫位和主星的安全解释骨架 |
| `naming_symbol_lookup` | runnable | 查询姓名学维度、五行意象、名字类型和文化避讳的安全解释骨架 |
| `naming_candidate_comparator` | runnable | 生成候选名字比较表，分开评估字义、字音、字形、文化避讳和现实使用成本 |
| `naming_brand_scenario_scorer` | runnable | 为品牌名、店名和商号候选评估品类、受众、渠道、搜索和风险边界 |

Schema：`schemas/bazi-ziwei-intake-guard.schema.json`

Schema：`schemas/bazi-ziwei-chart-record.schema.json`

Schema：`schemas/mingli-school-reference.schema.json`

Schema：`schemas/mingli-symbol-lookup.schema.json`

Schema：`schemas/naming-symbol-lookup.schema.json`

Schema：`schemas/naming-candidate-comparator.schema.json`

Schema：`schemas/naming-brand-scenario-scorer.schema.json`

## 数字象征/号码工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `numerology_request_guard` | runnable | 守门数字能量、生命灵数和号码请求中的敏感标识、财富承诺、专业替代和第三方标签风险 |
| `numerology_profile_recorder` | runnable | 记录脱敏数字片段、使用场景、数字列表和现实优先条件 |
| `numerology_symbol_lookup` | runnable | 查询 0-9、手机号尾号、车牌、门牌和生命灵数的安全象征解释 |
| `numerology_interpretation_planner` | runnable | 组合数字记录和象征查询，生成隐私优先、现实条件优先的号码咨询计划 |

Schema：`schemas/numerology-request-guard.schema.json`

Schema：`schemas/numerology-profile-recorder.schema.json`

Schema：`schemas/numerology-symbol-lookup.schema.json`

Schema：`schemas/numerology-interpretation-planner.schema.json`

## 灵摆/摆锤工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `pendulum_request_guard` | runnable | 守门灵摆请求中的专业替代、最终决定、财务投机、第三方操控、超自然恐惧和反复依赖风险 |
| `pendulum_session_recorder` | runnable | 记录灵摆问题、校准说明、摆动结果、用户同意和缺失字段 |
| `pendulum_symbol_lookup` | runnable | 查询顺时针、逆时针、前后、左右、静止、不明确和校准的安全象征解释 |
| `pendulum_interpretation_planner` | runnable | 组合会话记录和摆动象征，生成现实证据优先、非决定论的灵摆咨询计划 |

Schema：`schemas/pendulum-request-guard.schema.json`

Schema：`schemas/pendulum-session-recorder.schema.json`

Schema：`schemas/pendulum-symbol-lookup.schema.json`

Schema：`schemas/pendulum-interpretation-planner.schema.json`

## 卢恩符文工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `rune_request_guard` | runnable | 守门卢恩符文请求中的专业替代、命运断言、财务投机、第三方隐私/操控、超自然恐惧和反复依赖风险 |
| `rune_cast_recorder` | runnable | 记录符文问题、牌阵、符文列表、位置、来源和缺失字段 |
| `rune_symbol_lookup` | runnable | 查询 Elder Futhark 符文名和中文别名的安全象征解释 |
| `rune_interpretation_planner` | runnable | 组合抽取记录和符文象征，生成现实证据优先、非决定论的符文咨询计划 |

Schema：`schemas/rune-request-guard.schema.json`

Schema：`schemas/rune-cast-recorder.schema.json`

Schema：`schemas/rune-symbol-lookup.schema.json`

Schema：`schemas/rune-interpretation-planner.schema.json`

## 手相/面相工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `physiognomy_request_guard` | runnable | 守门手相/面相请求中的本人同意、健康寿命、外貌歧视、第三方隐私和筛人风险 |
| `physiognomy_observation_recorder` | runnable | 记录用户自述或授权的掌纹/五官/痣相观察，不做照片分析或敏感推断 |
| `physiognomy_symbol_lookup` | runnable | 查询生命线、事业线、掌丘、鼻相、眉眼、痣相等符号的安全象征解释 |
| `physiognomy_interpretation_planner` | runnable | 组合观察和符号查询，生成非诊断、非寿命、非外貌标签的相术象征计划 |

Schema：`schemas/physiognomy-request-guard.schema.json`

Schema：`schemas/physiognomy-observation-recorder.schema.json`

Schema：`schemas/physiognomy-symbol-lookup.schema.json`

Schema：`schemas/physiognomy-interpretation-planner.schema.json`

## 占星工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `astrology_compatibility_guard` | runnable | 守门合盘/比较盘/关系命运请求，处理同意、第三方隐私和决定论风险 |
| `astrology_chart_record` | runnable | 记录外部星盘字段、来源、同意和出生资料最小化要求 |
| `astrology_symbol_lookup` | runnable | 查询星座、行星、四轴点、宫位和相位的安全解释骨架 |

Schema：`schemas/astrology-compatibility-guard.schema.json`

Schema：`schemas/astrology-chart-record.schema.json`

Schema：`schemas/astrology-symbol-lookup.schema.json`

## 仪式安全工具

| Tool | 状态 | 作用 |
| --- | --- | --- |
| `ritual_safety_check` | runnable | 检查材料、动作、环境是否危险 |
| `ritual_source_guard` | runnable | 标注民俗/宗教/现代/个人来源，阻断危险步骤并生成低风险替代 |
| `ritual_low_risk_protocol` | runnable | 为搬家、睡眠、告别、空间压迫等场景选择低风险象征性流程 |
| `ritual_source_example_lookup` | runnable | 查询地区/宗教/商业/个人等来源分类样例和安全写法 |

Schema：`schemas/ritual-safety.schema.json`

Schema：`schemas/ritual-source-guard.schema.json`

Schema：`schemas/ritual-low-risk-protocol.schema.json`

Schema：`schemas/ritual-source-example-lookup.schema.json`
