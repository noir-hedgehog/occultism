# Agent 运行时交接包

本页把玄学 agent 接入运行时所需的入口、Skill、工具、验证命令和安全不变量整理到一个交接面板。它证明可以做 runtime dry-run，不证明已经完成真实安装或公开发布。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| 状态 | `ready_for_runtime_dry_run` |
| Skill | 61 |
| Tool | 277 |
| 外部开放项 | 3 |

## 运行时入口

| Entrypoint | Tool | Contract |
| --- | --- | --- |
| `request_routing` | `agent_workflow_router` | 输入用户原始请求，输出流派、Skill、SOP、知识卡、初始工具链和风险状态。 |
| `domain_skill_execution` | `codex-skills/*/SKILL.md` | 按路由结果加载对应 Skill；Skill 再调用领域工具和 SOP。 |
| `output_safety_lint` | `mystic_output_lint` | 所有玄学输出交付前必须做安全措辞、专业边界和危险仪式检查。 |

## 准备度检查

| Check | Passed | Summary |
| --- | --- | --- |
| `tool_manifest` | True | 277 tools, 61 skills |
| `tool_wrapper_manifest` | True | 277/277 wrappers ready |
| `tool_definition_export` | True | 277 tool definitions exported |
| `tool_definition_validation` | True | 277/277 definitions valid |
| `tool_registry` | True | 277 tools ready for runtime registration |
| `tool_registry_validation` | True | 277 tools, 0 failed skill checks |
| `route_smoke` | True | 63/63 route cases passed |
| `runtime_dry_run` | True | 63/63 runtime dry-run cases passed |
| `skill_install_readiness` | True | ready_for_install_approval |
| `pilot_readiness` | True | ready_for_internal_dry_run |
| `external_evidence_intake` | True | 3 open external intake items |

## Skill 与工具链

| Skill | Role | Tools |
| --- | --- | --- |
| `tarot-symbolic-reading` | 塔罗牌阵选择与象征解读 | `mystic_intake_triage`, `tarot_spread_selector`, `tarot_draw_simulator`, `tarot_draw_recorder`, `tarot_card_lookup`, `tarot_interpretation_planner`, `tarot_combination_planner`, `symbolic_depth_lookup`, `mystic_output_lint` |
| `oracle-lot-symbolic-consultation` | 求签/签文象征咨询 | `mystic_intake_triage`, `oracle_lot_request_guard`, `oracle_lot_record_builder`, `oracle_lot_symbol_lookup`, `oracle_lot_interpretation_planner`, `mystic_output_lint` |
| `oracle-card-symbolic-consultation` | 神谕卡象征咨询 | `mystic_intake_triage`, `oracle_card_request_guard`, `oracle_card_draw_recorder`, `oracle_card_symbol_lookup`, `oracle_card_interpretation_planner`, `mystic_output_lint` |
| `cartomancy-symbolic-consultation` | 扑克牌占卜象征咨询 | `mystic_intake_triage`, `cartomancy_request_guard`, `cartomancy_draw_recorder`, `cartomancy_card_lookup`, `cartomancy_interpretation_planner`, `mystic_output_lint` |
| `dice-symbolic-consultation` | 星骰/占卜骰象征咨询 | `mystic_intake_triage`, `dice_request_guard`, `dice_roll_recorder`, `dice_symbol_lookup`, `dice_interpretation_planner`, `mystic_output_lint` |
| `tasseography-symbolic-consultation` | 茶叶/咖啡渣占卜象征咨询 | `mystic_intake_triage`, `tasseography_request_guard`, `tasseography_pattern_recorder`, `tasseography_symbol_lookup`, `tasseography_interpretation_planner`, `mystic_output_lint` |
| `lenormand-symbolic-consultation` | 雷诺曼卡象征咨询 | `mystic_intake_triage`, `lenormand_request_guard`, `lenormand_draw_recorder`, `lenormand_card_lookup`, `lenormand_interpretation_planner`, `mystic_output_lint` |
| `crystal-symbolic-consultation` | 水晶/能量石象征咨询 | `mystic_intake_triage`, `crystal_request_guard`, `crystal_item_recorder`, `crystal_symbol_lookup`, `crystal_use_planner`, `mystic_output_lint` |
| `candle-symbolic-consultation` | 蜡烛火焰/蜡泪象征咨询 | `mystic_intake_triage`, `candle_request_guard`, `candle_observation_recorder`, `candle_symbol_lookup`, `candle_interpretation_planner`, `mystic_output_lint` |
| `incense-symbolic-consultation` | 香火/香灰/烟形象征咨询 | `mystic_intake_triage`, `incense_request_guard`, `incense_observation_recorder`, `incense_symbol_lookup`, `incense_interpretation_planner`, `mystic_output_lint` |
| `aroma-symbolic-consultation` | 芳香/精油/气味象征咨询 | `mystic_intake_triage`, `aroma_request_guard`, `aroma_context_recorder`, `aroma_symbol_lookup`, `aroma_practice_planner`, `mystic_output_lint` |
| `herbal-symbolic-consultation` | 草本/香草/植物魔法象征咨询 | `mystic_intake_triage`, `herbal_request_guard`, `herbal_context_recorder`, `herbal_symbol_lookup`, `herbal_practice_planner`, `mystic_output_lint` |
| `sigil-symbolic-consultation` | Sigil/符号印记/魔法阵象征咨询 | `mystic_intake_triage`, `sigil_request_guard`, `sigil_context_recorder`, `sigil_symbol_lookup`, `sigil_practice_planner`, `mystic_output_lint` |
| `dowsing-symbolic-consultation` | 占杖/寻水杖/探测棒象征咨询 | `mystic_intake_triage`, `dowsing_request_guard`, `dowsing_context_recorder`, `dowsing_symbol_lookup`, `dowsing_practice_planner`, `mystic_output_lint` |
| `body-omen-symbolic-consultation` | 身体征兆/眼跳/耳鸣/喷嚏象征咨询 | `mystic_intake_triage`, `body_omen_request_guard`, `body_omen_context_recorder`, `body_omen_symbol_lookup`, `body_omen_reflection_planner`, `mystic_output_lint` |
| `scrying-symbolic-consultation` | 水晶球/镜面/水面凝视象征咨询 | `mystic_intake_triage`, `scrying_request_guard`, `scrying_observation_recorder`, `scrying_symbol_lookup`, `scrying_interpretation_planner`, `mystic_output_lint` |
| `casting-lots-symbolic-consultation` | 骨/贝壳/石子/符物抛掷象征咨询 | `mystic_intake_triage`, `casting_lots_request_guard`, `casting_lots_layout_recorder`, `casting_lots_symbol_lookup`, `casting_lots_interpretation_planner`, `mystic_output_lint` |
| `character-divination-symbolic-consultation` | 测字/拆字象征咨询 | `mystic_intake_triage`, `cezi_request_guard`, `cezi_character_recorder`, `cezi_symbol_lookup`, `cezi_interpretation_planner`, `mystic_output_lint` |
| `flower-symbolic-consultation` | 花语/植物象征咨询 | `mystic_intake_triage`, `flower_request_guard`, `flower_item_recorder`, `flower_symbol_lookup`, `flower_interpretation_planner`, `mystic_output_lint` |
| `animal-omen-symbolic-consultation` | 动物征兆/鸟兽虫鱼象征咨询 | `mystic_intake_triage`, `animal_omen_request_guard`, `animal_omen_observation_recorder`, `animal_omen_symbol_lookup`, `animal_omen_interpretation_planner`, `mystic_output_lint` |
| `aura-chakra-symbolic-consultation` | 气场/脉轮/能量感受象征咨询 | `mystic_intake_triage`, `aura_chakra_request_guard`, `aura_chakra_sensation_recorder`, `aura_chakra_symbol_lookup`, `aura_chakra_reflection_planner`, `mystic_output_lint` |
| `past-life-akashic-symbolic-consultation` | 前世/阿卡西/灵魂课题象征咨询 | `mystic_intake_triage`, `past_life_request_guard`, `past_life_narrative_recorder`, `past_life_symbol_lookup`, `past_life_reflection_planner`, `mystic_output_lint` |
| `moon-phase-symbolic-consultation` | 月相/月亮周期象征咨询 | `mystic_intake_triage`, `moon_phase_request_guard`, `moon_phase_context_recorder`, `moon_phase_symbol_lookup`, `moon_phase_reflection_planner`, `mystic_output_lint` |
| `spirit-message-symbolic-consultation` | 通灵/高我/灵性讯息象征咨询 | `mystic_intake_triage`, `spirit_message_request_guard`, `spirit_message_record_builder`, `spirit_message_symbol_lookup`, `spirit_message_reflection_planner`, `mystic_output_lint` |
| `psychometry-symbolic-consultation` | 物品感应/触物占卜象征咨询 | `mystic_intake_triage`, `psychometry_request_guard`, `psychometry_object_recorder`, `psychometry_symbol_lookup`, `psychometry_reflection_planner`, `mystic_output_lint` |
| `bibliomancy-symbolic-consultation` | 书占/随机翻书象征咨询 | `mystic_intake_triage`, `bibliomancy_request_guard`, `bibliomancy_source_recorder`, `bibliomancy_symbol_lookup`, `bibliomancy_reflection_planner`, `mystic_output_lint` |
| `sky-omen-symbolic-consultation` | 天象/云形征兆象征咨询 | `mystic_intake_triage`, `sky_omen_request_guard`, `sky_omen_observation_recorder`, `sky_omen_symbol_lookup`, `sky_omen_reflection_planner`, `mystic_output_lint` |
| `manifestation-symbolic-consultation` | 祈愿/显化/愿望仪式象征咨询 | `mystic_intake_triage`, `manifestation_request_guard`, `manifestation_intention_recorder`, `manifestation_symbol_lookup`, `manifestation_reflection_planner`, `mystic_output_lint` |
| `pet-communication-symbolic-consultation` | 宠物沟通/动物灵性讯息象征咨询 | `mystic_intake_triage`, `pet_communication_request_guard`, `pet_communication_context_recorder`, `pet_communication_symbol_lookup`, `pet_communication_reflection_planner`, `mystic_output_lint` |
| `synchronicity-symbolic-consultation` | 同步性/天使数字/重复征兆象征咨询 | `mystic_intake_triage`, `synchronicity_request_guard`, `synchronicity_event_recorder`, `synchronicity_symbol_lookup`, `synchronicity_reflection_planner`, `mystic_output_lint` |
| `planetary-retrograde-symbolic-consultation` | 水逆/行星逆行/星象天气象征咨询 | `mystic_intake_triage`, `planetary_retrograde_request_guard`, `planetary_retrograde_context_recorder`, `planetary_retrograde_symbol_lookup`, `planetary_retrograde_reflection_planner`, `mystic_output_lint` |
| `spiritual-protection-symbolic-consultation` | 恶眼/能量防护/断联象征咨询 | `mystic_intake_triage`, `spiritual_protection_request_guard`, `spiritual_protection_context_recorder`, `spiritual_protection_symbol_lookup`, `spiritual_protection_reflection_planner`, `mystic_output_lint` |
| `deity-ancestor-symbolic-consultation` | 神明/祖先/供奉/祭拜象征咨询 | `mystic_intake_triage`, `deity_ancestor_request_guard`, `deity_ancestor_context_recorder`, `deity_ancestor_symbol_lookup`, `deity_ancestor_reflection_planner`, `mystic_output_lint` |
| `sleep-paralysis-symbolic-consultation` | 鬼压床/梦魇/睡前灵异恐惧象征咨询 | `mystic_intake_triage`, `sleep_paralysis_request_guard`, `sleep_paralysis_context_recorder`, `sleep_paralysis_symbol_lookup`, `sleep_paralysis_reflection_planner`, `mystic_output_lint` |
| `wealth-luck-symbolic-consultation` | 招财/财运/财库象征咨询 | `mystic_intake_triage`, `wealth_luck_request_guard`, `wealth_luck_context_recorder`, `wealth_luck_symbol_lookup`, `wealth_luck_action_planner`, `mystic_output_lint` |
| `relationship-luck-symbolic-consultation` | 桃花/姻缘/人缘象征咨询 | `mystic_intake_triage`, `relationship_luck_request_guard`, `relationship_luck_context_recorder`, `relationship_luck_symbol_lookup`, `relationship_luck_action_planner`, `mystic_output_lint` |
| `consecration-symbolic-consultation` | 开光/加持/净物象征咨询 | `mystic_intake_triage`, `consecration_request_guard`, `consecration_context_recorder`, `consecration_symbol_lookup`, `consecration_care_planner`, `mystic_output_lint` |
| `lost-object-symbolic-consultation` | 失物/寻物象征咨询 | `mystic_intake_triage`, `lost_object_request_guard`, `lost_object_context_recorder`, `lost_object_symbol_lookup`, `lost_object_search_planner`, `mystic_output_lint` |
| `sound-cleansing-symbolic-consultation` | 声响净化/铃钵象征咨询 | `mystic_intake_triage`, `sound_cleansing_request_guard`, `sound_cleansing_context_recorder`, `sound_cleansing_symbol_lookup`, `sound_cleansing_practice_planner`, `mystic_output_lint` |
| `western-geomancy-symbolic-consultation` | 西洋土占/盾形盘象征咨询 | `mystic_intake_triage`, `western_geomancy_request_guard`, `western_geomancy_chart_recorder`, `western_geomancy_figure_lookup`, `western_geomancy_interpretation_planner`, `mystic_output_lint` |
| `nine-star-ki-symbolic-consultation` | 九星气学/九宫命星象征咨询 | `mystic_intake_triage`, `nine_star_ki_request_guard`, `nine_star_ki_profile_recorder`, `nine_star_ki_symbol_lookup`, `nine_star_ki_interpretation_planner`, `mystic_output_lint` |
| `human-design-symbolic-consultation` | 人类图/Human Design 象征咨询 | `mystic_intake_triage`, `human_design_request_guard`, `human_design_chart_recorder`, `human_design_symbol_lookup`, `human_design_interpretation_planner`, `mystic_output_lint` |
| `talisman-symbolic-consultation` | 护符/符箓象征咨询 | `mystic_intake_triage`, `talisman_request_guard`, `talisman_record_builder`, `talisman_symbol_lookup`, `talisman_use_planner`, `mystic_output_lint` |
| `color-symbolic-consultation` | 五行颜色/开运色象征咨询 | `mystic_intake_triage`, `color_request_guard`, `color_profile_recorder`, `color_symbol_lookup`, `color_palette_planner`, `mystic_output_lint` |
| `zodiac-symbolic-consultation` | 生肖/太岁象征咨询 | `mystic_intake_triage`, `zodiac_request_guard`, `zodiac_profile_recorder`, `zodiac_symbol_lookup`, `zodiac_interpretation_planner`, `mystic_output_lint` |
| `feng-shui-space-audit` | 居家/办公空间风水审视 | `mystic_intake_triage`, `fengshui_school_guard`, `fengshui_observation_recorder`, `fengshui_space_checklist`, `fengshui_yangzhai_case_library`, `fengshui_bagua_mapper`, `fengshui_recommendation_ranker`, `symbolic_depth_lookup`, `mystic_output_lint` |
| `ritual-safety-advisor` | 驱邪、净化、护身等仪式安全咨询 | `mystic_intake_triage`, `ritual_safety_check`, `ritual_source_example_lookup`, `ritual_source_guard`, `ritual_low_risk_protocol`, `symbolic_depth_lookup`, `mystic_output_lint` |
| `folk-custom-consultation` | 民俗节令、禁忌和象征物的文化解释 | `mystic_intake_triage`, `folk_custom_lookup`, `folk_source_recorder`, `folk_taboo_reframer`, `mystic_output_lint` |
| `yijing-symbolic-consultation` | 易经/周易问题守门与卦爻变化分析 | `mystic_intake_triage`, `yijing_question_guard`, `yijing_casting_method_advisor`, `yijing_casting_simulator`, `yijing_hexagram_record`, `yijing_hexagram_lookup`, `yijing_line_lookup`, `yijing_source_reference_guard`, `symbolic_depth_lookup`, `mystic_output_lint` |
| `liuyao-symbolic-consultation` | 六爻六亲/六神/世应/候选用神解释与一事一问守门 | `mystic_intake_triage`, `yijing_question_guard`, `liuyao_chart_recorder`, `liuyao_focus_selector`, `liuyao_symbol_lookup`, `mystic_output_lint` |
| `meihua-symbolic-consultation` | 梅花易数体用/外应/动爻取象咨询 | `mystic_intake_triage`, `yijing_question_guard`, `meihua_omen_recorder`, `meihua_casting_recorder`, `meihua_relation_interpreter`, `meihua_symbol_lookup`, `mystic_output_lint` |
| `qimen-chart-consultation` | 奇门遁甲盘式记录与局势分析 | `mystic_intake_triage`, `qimen_method_guard`, `qimen_school_reference`, `qimen_chart_record`, `qimen_focus_selector`, `symbolic_depth_lookup`, `mystic_output_lint` |
| `mingli-bazi-ziwei-consultation` | 八字/紫微斗数命理咨询边界与出生资料守门 | `mystic_intake_triage`, `bazi_ziwei_intake_guard`, `mingli_school_reference`, `bazi_ziwei_chart_record`, `mingli_symbol_lookup`, `symbolic_depth_lookup`, `mystic_output_lint` |
| `naming-symbolic-consultation` | 姓名学命名偏好与名字象征咨询 | `mystic_intake_triage`, `naming_symbol_lookup`, `naming_candidate_comparator`, `naming_brand_scenario_scorer`, `mystic_output_lint` |
| `numerology-symbolic-consultation` | 数字象征/号码偏好咨询 | `mystic_intake_triage`, `numerology_request_guard`, `numerology_profile_recorder`, `numerology_symbol_lookup`, `numerology_interpretation_planner`, `mystic_output_lint` |
| `pendulum-symbolic-consultation` | 灵摆/摆锤象征反思咨询 | `mystic_intake_triage`, `pendulum_request_guard`, `pendulum_session_recorder`, `pendulum_symbol_lookup`, `pendulum_interpretation_planner`, `mystic_output_lint` |
| `rune-symbolic-consultation` | 卢恩符文象征咨询 | `mystic_intake_triage`, `rune_request_guard`, `rune_cast_recorder`, `rune_symbol_lookup`, `rune_interpretation_planner`, `mystic_output_lint` |
| `physiognomy-symbolic-consultation` | 手相/面相/相术象征咨询 | `mystic_intake_triage`, `physiognomy_request_guard`, `physiognomy_observation_recorder`, `physiognomy_symbol_lookup`, `physiognomy_interpretation_planner`, `mystic_output_lint` |
| `astrology-symbolic-consultation` | 占星/星盘符号解释与隐私边界咨询 | `mystic_intake_triage`, `astrology_compatibility_guard`, `astrology_chart_record`, `astrology_symbol_lookup`, `mystic_output_lint` |
| `dream-symbolic-consultation` | 解梦与梦境象征反思咨询 | `mystic_intake_triage`, `dream_record_builder`, `dream_symbol_lookup`, `dream_interpretation_planner`, `mystic_output_lint` |
| `date-selection-consultation` | 择日/黄历/吉日选择象征咨询 | `mystic_intake_triage`, `date_selection_guard`, `almanac_symbol_lookup`, `date_constraint_recorder`, `date_option_ranker`, `mystic_output_lint` |

## 安全不变量

- red/orange 风险不得继续占卜、排盘或仪式步骤。
- 不替代医疗、法律、财务、人身安全或精神健康专业支持。
- 不确认鬼神实体伤害、诅咒成立、必然灾祸、必然发财或命运定论。
- 驱邪/净化只能提供低风险、无明火、无危险材料、可撤回的象征性替代。
- 出生资料、第三方信息和真实 transcript 必须按最小化、同意和脱敏规则处理。

## 集成命令

```bash
python3 agent-tools/scripts/agent_workflow_router.py --text '<user request>'
python3 agent-tools/scripts/tool_manifest_builder.py
python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py
python3 agent-tools/scripts/agent_tool_definition_exporter.py --format openai
python3 agent-tools/scripts/agent_tool_definition_validator.py
python3 agent-tools/scripts/agent_tool_registry_builder.py
python3 agent-tools/scripts/agent_tool_registry_validator.py
python3 agent-tools/scripts/skill_install_readiness_report.py --codex-home /Users/uriah/.codex --format markdown
python3 agent-tools/scripts/external_evidence_intake_builder.py --codex-home /Users/uriah/.codex --format markdown
python3 agent-tools/scripts/pilot_readiness_report.py --codex-home /Users/uriah/.codex --format markdown
```

## 验证命令

```bash
python3 agent-tools/scripts/agent_route_smoke_runner.py
python3 agent-tools/scripts/agent_runtime_dry_run_runner.py
python3 agent-tools/scripts/tool_manifest_builder.py
python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py
python3 agent-tools/scripts/agent_tool_definition_exporter.py
python3 agent-tools/scripts/agent_tool_definition_validator.py
python3 agent-tools/scripts/agent_tool_registry_builder.py
python3 agent-tools/scripts/agent_tool_registry_validator.py
python3 agent-tools/scripts/skill_replay_runner.py
python3 agent-tools/scripts/skill_transcript_runner.py
python3 agent-tools/scripts/release_gate_runner.py
```

## 外部开放项

- `actual_skill_install_requires_user_confirmation`
- `real_anonymized_transcripts_needed`
- `content_expert_approval_needed`

## 限制

- ready_for_runtime_dry_run 表示仓库证据足以接入测试 runtime，不表示已经安装到真实 Codex home。
- runtime wrapper 必须保留 agent_workflow_router 的风险暂停语义。
- 外部证据入口仍显示 open 时，不应宣称完整公开发布完成。
