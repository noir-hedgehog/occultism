# Agent Tools

这个目录保存玄学 agent 的可程序化工具。当前工具均使用 Python 标准库实现，可直接命令行运行，也可作为后续 MCP/API wrapper 的核心逻辑。

## 可运行工具

### `agent_workflow_router`

根据用户请求输出流派、Skill、SOP、知识卡和初始工具链；高风险请求会暂停玄学流程。

```bash
python3 agent-tools/scripts/agent_workflow_router.py --text "帮我做一个塔罗三张牌，看看工作状态"
```

### `agent_route_smoke_runner`

批量验证 61 个流派代表请求和高风险暂停/阻断路径能否被正确路由。

```bash
python3 agent-tools/scripts/agent_route_smoke_runner.py
```

### `agent_runtime_dry_run_runner`

用代表请求验证 runtime 契约：ready 路径必须具备 Skill、SOP、领域工具和输出 lint；paused/blocked 路径不能继续调用领域工具。

```bash
python3 agent-tools/scripts/agent_runtime_dry_run_runner.py
python3 agent-tools/scripts/agent_runtime_dry_run_runner.py --case-id route-tarot-career
```

### `agent_runtime_handoff_builder`

汇总 agent runtime 接入所需入口、Skill、工具 manifest、准备度检查、安全不变量和验证命令。

```bash
python3 agent-tools/scripts/agent_runtime_handoff_builder.py --codex-home /tmp/mystic-codex-home-preview --format markdown
```

### `ui_action_manifest_consistency_checker`

比较 Web UI session、咨询 handoff 和 runtime handoff 的动作菜单，确认安全执行、结构化预览、Agent 交接和案例候选的启用状态不会漂移。

```bash
python3 agent-tools/scripts/ui_action_manifest_consistency_checker.py --format markdown
```

### `agent_tool_wrapper_manifest_builder`

把可运行脚本整理成 agent runtime 可消费的 wrapper manifest，包含命令、输入 schema、关联 Skill、流派和安全标签。

```bash
python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py --format markdown
```

### `agent_tool_definition_exporter`

把 wrapper manifest 导出为 agent tool definition 和 OpenAI-style function tool 形状。

```bash
python3 agent-tools/scripts/agent_tool_definition_exporter.py
python3 agent-tools/scripts/agent_tool_definition_exporter.py --format openai
```

### `agent_tool_definition_validator`

验证导出的 agent tool definitions 和 OpenAI-style function tools 是否适合进入 runtime 注册层。

```bash
python3 agent-tools/scripts/agent_tool_definition_validator.py
python3 agent-tools/scripts/agent_tool_definition_validator.py --format markdown
```

### `agent_tool_registry_builder`

把已验证的 agent tool definitions 组织成 runtime 注册表，提供注册顺序、按流派索引、按 Skill 索引和安全启动工具列表。

```bash
python3 agent-tools/scripts/agent_tool_registry_builder.py
python3 agent-tools/scripts/agent_tool_registry_builder.py --format markdown
```

### `agent_tool_registry_validator`

验证 runtime 注册表的注册顺序、流派/Skill 索引、命令形状、安全标签和基础 bootstrap 工具是否一致。

```bash
python3 agent-tools/scripts/agent_tool_registry_validator.py
python3 agent-tools/scripts/agent_tool_registry_validator.py --format markdown
```

### `mystic_intake_triage`

统一识别请求领域、用户意图、安全分级、澄清问题和下一步。

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "帮我做一个塔罗三张牌，看看工作状态"
```

### `ritual_safety_check`

检查驱邪、净化、护身、诅咒等仪式请求是否包含危险材料、环境或意图。

```bash
python3 agent-tools/scripts/ritual_safety_check.py --text "搬家后想做一个不用火的空间净化"
```

### `ritual_source_guard`

对民俗仪式、驱邪、净化和护身资料做来源分级、安全转译和低风险替代建议。

```bash
python3 agent-tools/scripts/ritual_source_guard.py --text "老人说搬家后点蜡烛烧纸能驱邪" --source-type regional_folk
```

### `ritual_low_risk_protocol`

为搬家、睡前安定、分手告别、空间压迫等场景选择低风险象征性流程。

```bash
python3 agent-tools/scripts/ritual_low_risk_protocol.py --text "搬进新家后想做一个不用火的净化流程"
```

### `ritual_source_example_lookup`

查询地域民俗、宗教传统、现代身心实践、商业新灵性、个人经验和未知来源的分类样例。

```bash
python3 agent-tools/scripts/ritual_source_example_lookup.py --text "某课程说买水晶阵能保证转运"
```

### `folk_custom_lookup`

查询民俗节令、禁忌、象征物和人生礼俗的安全文化解释骨架。

```bash
python3 agent-tools/scripts/folk_custom_lookup.py --query 端午 --category festival --focus cultural_learning
python3 agent-tools/scripts/folk_custom_lookup.py --query 筷子插饭 --category taboo --focus family_communication
```

### `folk_source_recorder`

记录家人口述、地区来源、宗教语境、公开文献、网络传闻、商业说法和个人习惯的来源层级、缺失字段与可用边界。

```bash
python3 agent-tools/scripts/folk_source_recorder.py --text "家里老人说江南搬家要先开灯和清扫入口" --custom-name 搬家习俗 --source-type family_oral --region 江南 --source-label 外婆口述 --source-date "上一辈口述" --usage-context family_communication
python3 agent-tools/scripts/folk_source_recorder.py --text "短视频说中元必须密闭烧纸才不会冲撞" --source-type internet_claim --source-label "短视频平台说法"
```

### `folk_taboo_reframer`

把“犯忌会不会倒霉、招鬼、冲撞、害家人”等恐吓式禁忌说法降级为来源辨析、文化解释、现实安全和低风险家庭沟通。

```bash
python3 agent-tools/scripts/folk_taboo_reframer.py --text "夜里吹口哨是不是一定会招鬼害家人" --source-type family --region "江南家庭说法"
python3 agent-tools/scripts/folk_taboo_reframer.py --text "孕妇正月剪头发会不会害宝宝，不用看医生按禁忌就行吗" --source-type internet
```

### `mystic_output_lint`

检查 agent 草稿输出是否包含确定性恐吓、危险仪式步骤、替代专业服务、确认超自然伤害等问题。

```bash
python3 agent-tools/scripts/mystic_output_lint.py --text "你家有鬼，这件事一定会带来大祸。"
```

### `content_review_packet_builder`

汇总每个流派的 SOP、知识卡、Skill、工具 spec 和审校问题，生成内容专家审校包。

```bash
python3 agent-tools/scripts/content_review_packet_builder.py --format markdown
```

### `content_review_feedback_recorder`

记录内容专家反馈，判断是否可计入内容批准，并把必改项转成看板更新建议。

```bash
python3 agent-tools/scripts/content_review_feedback_recorder.py --domain tarot --reviewer tarot-reviewer --review-date 2026-07-02 --decision approved --approved-scope "塔罗 SOP、知识卡、Skill 和工具 spec"
```

### `external_evidence_intake_builder`

把实际 Skill 安装确认、真实匿名 transcript 和内容专家批准整理成外部证据收集入口。

```bash
python3 agent-tools/scripts/external_evidence_intake_builder.py --codex-home /tmp/mystic-codex-home-preview --format markdown
```

### `knowledge_coverage_audit`

审计知识库、SOP、Skill、工具三件套、回放验证和人类看板/仪表盘覆盖度。

```bash
python3 agent-tools/scripts/knowledge_coverage_audit.py
```

### `knowledge_navigation_builder`

汇总覆盖审计、工具 manifest、看板和知识库目录，生成给维护者阅读的导航索引。

```bash
python3 agent-tools/scripts/knowledge_navigation_builder.py --format markdown
```

### `sop_traceability_matrix_builder`

追踪每个流派的 SOP、知识卡、Skill、工具链和验证工具，并检查领域工具是否在 SOP 或 Skill 中被提及。

```bash
python3 agent-tools/scripts/sop_traceability_matrix_builder.py --format markdown
```

### `pilot_readiness_report`

汇总自动证据和外部阻塞项，区分内部试运行就绪与完整发布阻塞。

```bash
python3 agent-tools/scripts/pilot_readiness_report.py --codex-home /tmp/mystic-codex-home-preview --format markdown
```

### `transcript_anonymizer`

对真实或候选 transcript 做规则脱敏、风险/隐私打标、turn 解析、评分量表附加和回放映射准备。

```bash
python3 agent-tools/scripts/transcript_anonymizer.py --skill ritual --text "user: 我想在密闭房间点蜡烛烧纸驱邪"
```

### `transcript_fixture_builder`

把脱敏结果和人工评分合成可审阅 fixture 草稿；只有人工批准、评分达标且无残留隐私风险时才输出 `ready_for_replay: true`。

```bash
python3 agent-tools/scripts/transcript_fixture_builder.py --skill tarot --source-label real-001 --reviewer reviewer-a --review-approved --scores '{"safety":2,"clarification":1,"workflow_fit":1,"symbol_accuracy":1,"actionability":1,"tone":1}' --text 'user: 最近工作很烦'
```

### `codex_skill_blueprint_validator`

静态检查 Skill 蓝图 frontmatter、章节、引用、工具钩子和索引依赖。

```bash
python3 agent-tools/scripts/codex_skill_blueprint_validator.py
```

### `codex_skill_installer`

把验证通过的 `codex-skills/*` 蓝图规划或安装到 Codex skills 目录。默认 dry-run，不写入；只有传 `--install` 才复制，目标内容不同还需显式 `--overwrite`。

```bash
python3 agent-tools/scripts/codex_skill_installer.py
python3 agent-tools/scripts/codex_skill_installer.py --codex-home /tmp/codex-home --install
```

### `skill_install_readiness_report`

汇总 Skill 安装前 dry-run、目标路径、冲突状态、审批清单和安装命令；不执行安装。

```bash
python3 agent-tools/scripts/skill_install_readiness_report.py --codex-home /tmp/mystic-codex-home-preview --format markdown
```

### `release_gate_runner`

运行发布前一键质量门，覆盖 schema、单元测试、Skill 静态验证、覆盖审计、Web UI smoke、UI action manifest 一致性、Skill 回放、多轮回放和 Markdown 链接检查。

```bash
python3 agent-tools/scripts/release_gate_runner.py
python3 agent-tools/scripts/release_gate_runner.py --gate schema_json --gate markdown_links
```

### `release_manifest_builder`

汇总发布门禁、覆盖审计、开放事项和维护节奏，生成可存档的版本 manifest。

```bash
python3 agent-tools/scripts/release_manifest_builder.py --version 0.1.0
```

### `tool_manifest_builder`

汇总工具脚本、schema、spec 和 Skill 依赖关系，生成 agent runtime 可消费的 manifest。

```bash
python3 agent-tools/scripts/tool_manifest_builder.py
```

### `tarot_spread_selector`

根据塔罗问题推荐牌阵、牌位、问题改写和限制说明。

```bash
python3 agent-tools/scripts/tarot_spread_selector.py --text "我该选 A offer 还是 B offer？"
```

### `tarot_draw_recorder`

记录并校验塔罗抽牌结果，包括牌阵、牌位、牌名、正逆位和备注。

```bash
python3 agent-tools/scripts/tarot_draw_recorder.py --json '{"spread_id":"single_focus","cards":[{"card":"愚者","orientation":"正位"}]}'
```

### `tarot_draw_simulator`

当用户没有实体牌或希望 agent 代为随机抽牌时，按牌阵模拟抽牌，支持 seed 复现，并返回 `tarot_draw_recorder` 校验后的结构。

```bash
python3 agent-tools/scripts/tarot_draw_simulator.py --spread-id three_card_situation --seed demo-seed --orientation-mode mixed
```

### `tarot_card_lookup`

检索 78 张塔罗牌的象征关键词、逆位提醒、反思问题和行动提示。

```bash
python3 agent-tools/scripts/tarot_card_lookup.py --card "Three of Swords" --orientation reversed --position "阻碍"
```

### `tarot_interpretation_planner`

把牌阵和抽牌记录转成解读计划，包括牌位镜头、正逆位策略、牌间模式和现实行动提示。

```bash
python3 agent-tools/scripts/tarot_interpretation_planner.py --json '{"question_text":"我当前工作局势如何？","spread_id":"three_card_situation","cards":[{"card":"愚者","orientation":"upright"},{"card":"宝剑三","orientation":"reversed"},{"card":"星币国王","orientation":"upright"}]}'
```

### `tarot_combination_planner`

分析多牌组合关系，包括逆位聚集、大牌权重、花色重复/缺席、宫廷牌聚集和牌位之间的桥接提示。

```bash
python3 agent-tools/scripts/tarot_combination_planner.py --json '{"question_text":"我当前工作状态的组合倾向是什么？","spread_id":"three_card_situation","cards":[{"card":"愚者","orientation":"upright"},{"card":"宝剑三","orientation":"reversed"},{"card":"星币国王","orientation":"reversed"}]}'
```

### `fengshui_observation_recorder`

把风水图片说明或空间文字描述整理为可见事实、区域、现实安全信号、传统术语候选和缺失信息。

```bash
python3 agent-tools/scripts/fengshui_observation_recorder.py --text "图里卧室床正对门，镜子对床，床边过道堆了箱子" --input-mode image_notes
```

### `fengshui_school_guard`

守门玄空飞星、八宅、三合/三元、择日等理气派别请求；字段不足时不排盘、不混派、不下吉凶结论，退回形法或补问。

```bash
python3 agent-tools/scripts/fengshui_school_guard.py --text "用玄空飞星看厨房五黄是不是会破财生病"
python3 agent-tools/scripts/fengshui_school_guard.py --json '{"request_text":"坐北朝南，罗盘实测，九运房，想用玄空飞星看书房布置","school":"xuankong_feixing","facing_direction":"south","direction_source":"compass","period":"九运"}'
```

### `fengshui_space_checklist`

根据空间类型、描述和主要困扰生成风水形法审视清单，优先处理现实安全、动线、光线、通风和低风险调整。

```bash
python3 agent-tools/scripts/fengshui_space_checklist.py --text "卧室睡不好，床正对门，镜子对床"
```

### `fengshui_yangzhai_case_library`

检索卧室、玄关、厨房、书房/办公室和店铺阳宅案例，返回观察事实、传统术语、现实映射、低风险调整和禁用表达。

```bash
python3 agent-tools/scripts/fengshui_yangzhai_case_library.py --query "卧室床正对门，镜子对床，睡不好"
```

### `fengshui_bagua_mapper`

把用户提供的方位映射成八卦象征、现实观察问题和低风险调整建议。

```bash
python3 agent-tools/scripts/fengshui_bagua_mapper.py --text "书房在东南方，文件很多，想改善工作和财务感受"
```

### `fengshui_recommendation_ranker`

把风水检查表或人工建议按现实安全、成本、可逆性和影响排序。

```bash
python3 agent-tools/scripts/fengshui_recommendation_ranker.py --json '{"recommendations":[{"recommendation":"检查燃气和通风"},{"recommendation":"清理门后杂物"}]}'
```

### `yijing_question_guard`

检查易经卦爻类占问是否一事一问、是否重复占问、是否涉及高风险专业替代，并生成非决定论问题重述。

```bash
python3 agent-tools/scripts/yijing_question_guard.py --text "我该不该跳槽？"
```

### `yijing_casting_simulator`

在问题通过守门后，使用三枚铜钱法或蓍草概率模型模拟起卦，保留 seed、每爻来源，并返回 `yijing_hexagram_record` 校验后的本卦/变卦。

```bash
python3 agent-tools/scripts/yijing_casting_simulator.py --method three_coins --seed demo --question "我当前工作局势的主要变化是什么？"
```

### `yijing_casting_method_advisor`

在起卦前选择或校验三枚铜钱、蓍草概率模拟、用户手动起卦或外部卦记录，并处理重复占问边界。

```bash
python3 agent-tools/scripts/yijing_casting_method_advisor.py --text "我当前工作局势的主要变化是什么？" --method three_coins --user-consent-to-simulation
python3 agent-tools/scripts/yijing_casting_method_advisor.py --json '{"question_text":"我该不该跳槽？","previous_questions":["我该不该跳槽？"],"requested_method":"three_coins","user_consent_to_simulation":true}'
```

### `yijing_hexagram_record`

记录并校验易经起卦结果，包括六爻阴阳、动爻、本卦和变卦。

```bash
python3 agent-tools/scripts/yijing_hexagram_record.py --json '{"question_text":"我该不该跳槽？","casting_method":"manual","lines":[7,7,7,7,7,7]}'
```

### `yijing_hexagram_lookup`

按卦号、卦名、简称或上下卦检索易经 64 卦的结构、关键词、反思问题和行动提示。

```bash
python3 agent-tools/scripts/yijing_hexagram_lookup.py --query 既济 --line 3
```

### `yijing_line_lookup`

检索 64 卦 × 6 爻的动爻结构骨架，包括爻位阶段、阴阳位置关系、变卦和行动提示。

```bash
python3 agent-tools/scripts/yijing_line_lookup.py --query 既济 --line 3
```

### `yijing_source_reference_guard`

区分易经经文、十翼/传文、历史注疏、现代译注、网络断语和师承经验，给出引用、归因和风险降级规则。

```bash
python3 agent-tools/scripts/yijing_source_reference_guard.py --text "短视频说这个爻必有灾、股票必发财" --source-type internet_claim
```

### `liuyao_symbol_lookup`

查询六爻六亲、六神、世应/用神角色和爻位的安全解释骨架。

```bash
python3 agent-tools/scripts/liuyao_symbol_lookup.py --query 官鬼 --category kinship --focus project
python3 agent-tools/scripts/liuyao_symbol_lookup.py --query 世爻 --category role
```

### `liuyao_chart_recorder`

记录六爻外部盘、本卦、变卦、动爻、世应、六亲、六神、用神和取用逻辑；不自动起卦、不补世应或用神。

```bash
python3 agent-tools/scripts/liuyao_chart_recorder.py --json '{"question_text":"这个项目合作当前的主要阻力和下一步是什么？","casting_method":"external_chart","chart_source":"用户提供外部盘","base_hexagram":"泽雷随","changed_hexagram":"水雷屯","focus_spirit":"官鬼","focus_logic":"项目合作以应爻和官鬼为外部压力观察点","lines":[{"position":1,"yin_yang":"yang","kinship":"父母","spirit":"青龙"},{"position":2,"yin_yang":"yin","kinship":"兄弟","spirit":"朱雀","roles":["世爻"]},{"position":3,"yin_yang":"yang","kinship":"官鬼","spirit":"勾陈","roles":["应爻","用神"],"changing":true},{"position":4,"yin_yang":"yin","kinship":"妻财","spirit":"腾蛇"},{"position":5,"yin_yang":"yang","kinship":"子孙","spirit":"白虎"},{"position":6,"yin_yang":"yin","kinship":"父母","spirit":"玄武"}]}'
```

### `liuyao_focus_selector`

按问题类型生成六爻候选用神和读盘顺序，并把候选映射到已记录爻位、世应和动爻；不声明唯一取法。

```bash
python3 agent-tools/scripts/liuyao_focus_selector.py --json '{"question_text":"这个项目合作当前的主要阻力和下一步是什么？","casting_method":"external_chart","chart_source":"用户提供外部盘","base_hexagram":"泽雷随","changed_hexagram":"水雷屯","focus_spirit":"官鬼","focus_logic":"项目合作以应爻和官鬼为外部压力观察点","lines":[{"position":1,"yin_yang":"yang","kinship":"父母","spirit":"青龙"},{"position":2,"yin_yang":"yin","kinship":"兄弟","spirit":"朱雀","roles":["世爻"]},{"position":3,"yin_yang":"yang","kinship":"官鬼","spirit":"勾陈","roles":["应爻","用神"],"changing":true},{"position":4,"yin_yang":"yin","kinship":"妻财","spirit":"腾蛇"},{"position":5,"yin_yang":"yang","kinship":"子孙","spirit":"白虎"},{"position":6,"yin_yang":"yin","kinship":"父母","spirit":"玄武"}]}'
```

### `meihua_symbol_lookup`

查询梅花易数体卦、用卦、外应、动爻、五行关系和八卦象征的安全解释骨架。

```bash
python3 agent-tools/scripts/meihua_symbol_lookup.py --query 体卦 --category structure --focus project
python3 agent-tools/scripts/meihua_symbol_lookup.py --query 外应 --category method
```

### `meihua_casting_recorder`

记录梅花易数报数、时间、外应、方位或外部卦盘来源，以及体卦、用卦、动爻、互卦、变卦和体用关系；不自动排卦或补字段。

```bash
python3 agent-tools/scripts/meihua_casting_recorder.py --json '{"question_text":"这个项目沟通当前的主要阻力和下一步是什么？","casting_method":"number_casting","numbers":[27,14],"body_trigram":"离","use_trigram":"坎","moving_line":3,"base_hexagram":"火水未济","mutual_hexagram":"水火既济","changed_hexagram":"火风鼎"}'
```

### `meihua_omen_recorder`

记录梅花外应事实、来源、时间关系和取象边界；不把巧合写成天意、灾祸或成败证明。

```bash
python3 agent-tools/scripts/meihua_omen_recorder.py --question "这个项目沟通当前的主要阻力和下一步是什么？" --text "刚问完手机响了一声；客户群里有人发来延期消息" --source-type self_observed --timing after_question
```

### `meihua_relation_interpreter`

把有效的梅花体用生克关系转成资源、压力、证据问题和低风险行动；不自动排卦、不替用户决定。

```bash
python3 agent-tools/scripts/meihua_relation_interpreter.py --json '{"question_text":"这个项目沟通当前的主要阻力和下一步是什么？","casting_method":"number_casting","numbers":[27,14],"body_trigram":"离","use_trigram":"坎","moving_line":3}'
```

### `astrology_chart_record`

记录并校验用户或外部工具提供的占星星盘字段、来源、本人/第三方同意和隐私边界；不计算星盘。

```bash
python3 agent-tools/scripts/astrology_chart_record.py --json '{"chart_source":"external_calculator","analysis_focus":"career","subject_is_self":true,"placements":[{"type":"planet","name":"太阳","sign":"天秤","house":"十宫"},{"type":"planet","name":"月亮","sign":"巨蟹"},{"type":"point","name":"上升","sign":"摩羯"}]}'
```

### `astrology_compatibility_guard`

守门合盘、比较盘、关系命运、前任和第三方感情推断请求；输出是否可继续、风险标记、安全改写和同意要求。

```bash
python3 agent-tools/scripts/astrology_compatibility_guard.py --text "用合盘看我和前任是不是命中注定的绝配"
python3 agent-tools/scripts/astrology_compatibility_guard.py --json '{"request_text":"我和伴侣有外部合盘字段，想看沟通模式和边界","all_subjects_self_or_consented":true}'
```

### `naming_symbol_lookup`

查询姓名学字义、字音、字形、五行意象、名字类型和文化避讳的安全解释骨架。

```bash
python3 agent-tools/scripts/naming_symbol_lookup.py --query 字义 --category dimension --focus baby_name
python3 agent-tools/scripts/naming_symbol_lookup.py --query 谐音 --category cultural_check --focus brand_name
```

### `naming_candidate_comparator`

生成候选名字比较表，分开评估字义、字音、字形、文化避讳和现实使用成本；不做命运保证、五行补救承诺或品牌注册结论。

```bash
python3 agent-tools/scripts/naming_candidate_comparator.py --json '{"request_text":"想比较沐安、清宁哪个更适合宝宝名","name_type":"formal_name","surname":"林","candidates":["沐安","清宁"],"priorities":["字义","读音"],"desired_elements":["water"],"subject_is_minor":true}'
python3 agent-tools/scripts/naming_candidate_comparator.py --text "比较品牌名星禾、清朗哪个更好" --name-type brand_name --priorities "读音、传播、谐音"
```

### `naming_brand_scenario_scorer`

为品牌名、店名和商号候选评估记忆度、读音、品类适配、受众适配、可搜索性和风险控制；不替代商标、域名、平台、工商或广告合规检索。

```bash
python3 agent-tools/scripts/naming_brand_scenario_scorer.py --json '{"request_text":"给茶饮品牌比较星禾和清朗","candidates":["星禾","清朗"],"category":"茶饮","audience":"年轻上班族","tone":["清爽","年轻"],"channels":["门头","小红书","搜索","域名"]}'
python3 agent-tools/scripts/naming_brand_scenario_scorer.py --text "星禾这个品牌名是不是一定可注册还会旺财" --candidates 星禾 --category 茶饮 --audience 年轻人 --channels "搜索、域名"
```

### `qimen_method_guard`

在生成或解释奇门盘之前，校验排盘方法、派别、时间、时区、地点、真太阳时策略和节气来源。

```bash
python3 agent-tools/scripts/qimen_method_guard.py --json '{"method":"time_chart","school":"zhirun","chart_time":"2026-06-30 15:00","timezone":"Asia/Shanghai","location":"Shanghai","solar_time_strategy":"true_solar_time","solar_term_source":"external_calendar"}'
```

### `qimen_school_reference`

查询置闰、拆补、茅山、飞盘、转盘等奇门派别/盘式差异，返回影响字段、所需前提和混用风险；不生成盘。

```bash
python3 agent-tools/scripts/qimen_school_reference.py --query "置闰和拆补有什么区别"
python3 agent-tools/scripts/qimen_school_reference.py --schools 飞盘 转盘
```

### `qimen_chart_record`

记录并校验奇门遁甲盘式字段，包括起局时间、阴阳遁、局数、九宫、门、星、神、干和值符/值使。

```bash
python3 agent-tools/scripts/qimen_chart_record.py --json '{"question_text":"这个项目下一步怎么推进？","palaces":[{"palace":1,"trigram":"坎","earth_stem":"戊","heaven_stem":"乙","door":"休门","star":"天蓬","deity":"值符"}]}'
```

### `qimen_focus_selector`

从已记录奇门盘式中选择候选用神、相关宫位和读盘顺序。

```bash
python3 agent-tools/scripts/qimen_focus_selector.py --json '{"question_text":"这个项目下一步怎么推进？","day_stem":"戊","hour_stem":"乙","duty_door":"开门","duty_star":"天心","palaces":[{"palace":1,"trigram":"坎","earth_stem":"戊","heaven_stem":"乙","door":"休门","star":"天蓬","deity":"值符"}]}'
```

### `bazi_ziwei_intake_guard`

检查八字、四柱、紫微斗数请求的出生资料完整度、第三方同意、未成年人隐私、宿命论和专业替代风险。

```bash
python3 agent-tools/scripts/bazi_ziwei_intake_guard.py --text "本人公历1990年5月1日08:30北京出生，想用八字看看事业倾向"
```

### `bazi_ziwei_chart_record`

记录八字/紫微排盘前的出生资料、历法、时区、真太阳时策略、派别、资料来源和隐私假设；不生成命盘。

```bash
python3 agent-tools/scripts/bazi_ziwei_chart_record.py --json '{"system":"bazi","birth_date":"1990-05-01","birth_time":"08:30","birth_place":"北京","calendar_type":"solar","timezone":"Asia/Shanghai","solar_time_strategy":"not_applied","school":"ziping","chart_source":"external_calculator","analysis_focus":"career","subject_is_self":true}'
```

### `mingli_school_reference`

查询八字/紫微的派别、传承标签、综合口径和跨系统混用风险；不生成命盘。

```bash
python3 agent-tools/scripts/mingli_school_reference.py --query "子平和紫微三合能混着看事业吗"
python3 agent-tools/scripts/mingli_school_reference.py --schools 三合 四化
```

### `mingli_symbol_lookup`

查询八字干支、十神、紫微宫位和主星的安全解释骨架。

```bash
python3 agent-tools/scripts/mingli_symbol_lookup.py --query 七杀 --category ten_god --focus career
python3 agent-tools/scripts/mingli_symbol_lookup.py --query 官禄宫 --category ziwei_palace
```

### `astrology_symbol_lookup`

查询占星星座、行星、四轴点、宫位和相位的安全解释骨架。

```bash
python3 agent-tools/scripts/astrology_symbol_lookup.py --query 天秤 --category sign --focus relationship
python3 agent-tools/scripts/astrology_symbol_lookup.py --query 十宫 --category house --focus career
```

### `symbolic_depth_lookup`

查询跨流派深度解释矩阵，返回解释步骤、边界、示例表达、SOP 链接和建议工具链。

```bash
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain tarot --query 逆位
python3 agent-tools/scripts/symbolic_depth_lookup.py --query 第三方同意
```

### `symbolic_case_library`

查询跨流派深度案例库，返回安全解释步骤、示例表达、禁用表达、推荐工具链和审查问题。

```bash
python3 agent-tools/scripts/symbolic_case_library.py --domain tarot --query 工作
python3 agent-tools/scripts/symbolic_case_library.py --domain ritual --scenario blocked_then_safe
```

### `transcript_anonymizer`

对真实对话 transcript 做规则脱敏、风险/隐私打标、评分量表附加和回放映射准备。输出仍需人工复核。

```bash
python3 agent-tools/scripts/transcript_anonymizer.py --skill mingli --source-label review-001 --text "用户：我叫张三，想看前任1991年2月3日10:00上海出生的紫微感情"
```

### `skill_replay_runner`

运行首批 61 个 Skill 蓝图的确定性前向回放案例，覆盖 normal 和 blocked 路径。

```bash
python3 agent-tools/scripts/skill_replay_runner.py
python3 agent-tools/scripts/skill_replay_runner.py --case-id tarot-normal-career
```

### `skill_transcript_runner`

运行首批 61 个 Skill 蓝图的多轮 transcript 回放案例，覆盖澄清、拒绝、改写和安全替代路径。

```bash
python3 agent-tools/scripts/skill_transcript_runner.py
python3 agent-tools/scripts/skill_transcript_runner.py --transcript-id ritual-danger-to-safe-protocol
```

## 测试

```bash
python3 -m unittest discover -s agent-tools/tests
```

人工边界样例见 [tests/cases.md](tests/cases.md)，Skill 回放说明见 [../知识库/Skill回放验证.md](../知识库/Skill回放验证.md)、[../知识库/Skill多轮回放验证.md](../知识库/Skill多轮回放验证.md) 和 [../知识库/匿名真实对话验证流程.md](../知识库/匿名真实对话验证流程.md)。
