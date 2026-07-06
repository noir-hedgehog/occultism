# Agent Tool Definition Validation

本页验证导出的 agent tool definitions 是否适合进入 runtime 注册层。它只检查注册形状和本地引用，不执行工具。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| Definition | 278/278 |
| OpenAI-style tool | 278/278 |
| 失败 definition | 0 |
| 失败 OpenAI tool | 0 |

## Definition 检查

| Tool | Valid | Domains | Safety Tags | Errors |
| --- | --- | --- | --- | --- |
| `agent_route_smoke_runner` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `agent_runtime_dry_run_runner` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `agent_runtime_handoff_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `agent_tool_definition_exporter` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `agent_tool_definition_validator` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `agent_tool_registry_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `agent_tool_registry_validator` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `agent_tool_wrapper_manifest_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `agent_workflow_router` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `almanac_symbol_lookup` | True | `date_selection` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `animal_omen_interpretation_planner` | True | `animal_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `animal_omen_observation_recorder` | True | `animal_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `animal_omen_request_guard` | True | `animal_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `animal_omen_symbol_lookup` | True | `animal_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `aroma_context_recorder` | True | `aroma` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `aroma_practice_planner` | True | `aroma` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `aroma_request_guard` | True | `aroma` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `aroma_symbol_lookup` | True | `aroma` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `astrology_chart_record` | True | `astrology` | `birth_data_minimization`, `professional_boundary_required`, `symbolic_interpretation_only`, `third_party_privacy` | - |
| `astrology_compatibility_guard` | True | `astrology` | `birth_data_minimization`, `professional_boundary_required`, `symbolic_interpretation_only`, `third_party_privacy` | - |
| `astrology_symbol_lookup` | True | `astrology` | `birth_data_minimization`, `professional_boundary_required`, `symbolic_interpretation_only`, `third_party_privacy` | - |
| `aura_chakra_reflection_planner` | True | `aura_chakra` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `aura_chakra_request_guard` | True | `aura_chakra` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `aura_chakra_sensation_recorder` | True | `aura_chakra` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `aura_chakra_symbol_lookup` | True | `aura_chakra` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `bazi_ziwei_chart_record` | True | `mingli` | `birth_data_minimization`, `no_fatalism`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `bazi_ziwei_intake_guard` | True | `mingli` | `birth_data_minimization`, `no_fatalism`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `bibliomancy_reflection_planner` | True | `bibliomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `bibliomancy_request_guard` | True | `bibliomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `bibliomancy_source_recorder` | True | `bibliomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `bibliomancy_symbol_lookup` | True | `bibliomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `body_omen_context_recorder` | True | `body_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `body_omen_reflection_planner` | True | `body_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `body_omen_request_guard` | True | `body_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `body_omen_symbol_lookup` | True | `body_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `candle_interpretation_planner` | True | `candle` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `candle_observation_recorder` | True | `candle` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `candle_request_guard` | True | `candle` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `candle_symbol_lookup` | True | `candle` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `cartomancy_card_lookup` | True | `cartomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `cartomancy_draw_recorder` | True | `cartomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `cartomancy_interpretation_planner` | True | `cartomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `cartomancy_request_guard` | True | `cartomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `casting_lots_interpretation_planner` | True | `casting_lots` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `casting_lots_layout_recorder` | True | `casting_lots` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `casting_lots_request_guard` | True | `casting_lots` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `casting_lots_symbol_lookup` | True | `casting_lots` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `cezi_character_recorder` | True | `character_divination` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `cezi_interpretation_planner` | True | `character_divination` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `cezi_request_guard` | True | `character_divination` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `cezi_symbol_lookup` | True | `character_divination` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `codex_skill_blueprint_validator` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `codex_skill_installer` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `color_palette_planner` | True | `color` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `color_profile_recorder` | True | `color` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `color_request_guard` | True | `color` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `color_symbol_lookup` | True | `color` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `consecration_care_planner` | True | `consecration` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `consecration_context_recorder` | True | `consecration` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `consecration_request_guard` | True | `consecration` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `consecration_symbol_lookup` | True | `consecration` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `consultation_packet_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `content_review_feedback_recorder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `content_review_packet_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `crystal_item_recorder` | True | `crystal` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `crystal_request_guard` | True | `crystal` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `crystal_symbol_lookup` | True | `crystal` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `crystal_use_planner` | True | `crystal` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `date_constraint_recorder` | True | `date_selection` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `date_option_ranker` | True | `date_selection` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `date_selection_guard` | True | `date_selection` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `deity_ancestor_context_recorder` | True | `deity_ancestor` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `deity_ancestor_reflection_planner` | True | `deity_ancestor` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `deity_ancestor_request_guard` | True | `deity_ancestor` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `deity_ancestor_symbol_lookup` | True | `deity_ancestor` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dice_interpretation_planner` | True | `dice` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dice_request_guard` | True | `dice` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dice_roll_recorder` | True | `dice` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dice_symbol_lookup` | True | `dice` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dowsing_context_recorder` | True | `dowsing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dowsing_practice_planner` | True | `dowsing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dowsing_request_guard` | True | `dowsing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dowsing_symbol_lookup` | True | `dowsing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dream_interpretation_planner` | True | `dream` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dream_record_builder` | True | `dream` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `dream_symbol_lookup` | True | `dream` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `external_evidence_intake_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `fengshui_bagua_mapper` | True | `fengshui` | `no_deterministic_disaster_claims`, `professional_boundary_required`, `real_world_safety_first`, `symbolic_interpretation_only` | - |
| `fengshui_observation_recorder` | True | `fengshui` | `no_deterministic_disaster_claims`, `professional_boundary_required`, `real_world_safety_first`, `symbolic_interpretation_only` | - |
| `fengshui_recommendation_ranker` | True | `fengshui` | `no_deterministic_disaster_claims`, `professional_boundary_required`, `real_world_safety_first`, `symbolic_interpretation_only` | - |
| `fengshui_school_guard` | True | `fengshui` | `no_deterministic_disaster_claims`, `professional_boundary_required`, `real_world_safety_first`, `symbolic_interpretation_only` | - |
| `fengshui_space_checklist` | True | `fengshui` | `no_deterministic_disaster_claims`, `professional_boundary_required`, `real_world_safety_first`, `symbolic_interpretation_only` | - |
| `fengshui_yangzhai_case_library` | True | `fengshui` | `no_deterministic_disaster_claims`, `professional_boundary_required`, `real_world_safety_first`, `symbolic_interpretation_only` | - |
| `flower_interpretation_planner` | True | `flower` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `flower_item_recorder` | True | `flower` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `flower_request_guard` | True | `flower` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `flower_symbol_lookup` | True | `flower` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `folk_custom_lookup` | True | `folk_custom` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `folk_source_recorder` | True | `folk_custom` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `folk_taboo_reframer` | True | `folk_custom` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `herbal_context_recorder` | True | `herbal` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `herbal_practice_planner` | True | `herbal` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `herbal_request_guard` | True | `herbal` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `herbal_symbol_lookup` | True | `herbal` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `human_design_chart_recorder` | True | `human_design` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `human_design_interpretation_planner` | True | `human_design` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `human_design_request_guard` | True | `human_design` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `human_design_symbol_lookup` | True | `human_design` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `incense_interpretation_planner` | True | `incense` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `incense_observation_recorder` | True | `incense` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `incense_request_guard` | True | `incense` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `incense_symbol_lookup` | True | `incense` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `knowledge_coverage_audit` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `knowledge_navigation_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `lenormand_card_lookup` | True | `lenormand` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `lenormand_draw_recorder` | True | `lenormand` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `lenormand_interpretation_planner` | True | `lenormand` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `lenormand_request_guard` | True | `lenormand` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `liuyao_chart_recorder` | True | `liuyao` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `liuyao_focus_selector` | True | `liuyao` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `liuyao_symbol_lookup` | True | `liuyao` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `lost_object_context_recorder` | True | `lost_object` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `lost_object_request_guard` | True | `lost_object` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `lost_object_search_planner` | True | `lost_object` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `lost_object_symbol_lookup` | True | `lost_object` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `manifestation_intention_recorder` | True | `manifestation` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `manifestation_reflection_planner` | True | `manifestation` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `manifestation_request_guard` | True | `manifestation` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `manifestation_symbol_lookup` | True | `manifestation` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `meihua_casting_recorder` | True | `meihua` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `meihua_omen_recorder` | True | `meihua` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `meihua_relation_interpreter` | True | `meihua` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `meihua_symbol_lookup` | True | `meihua` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `mingli_school_reference` | True | `mingli` | `birth_data_minimization`, `no_fatalism`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `mingli_symbol_lookup` | True | `mingli` | `birth_data_minimization`, `no_fatalism`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `moon_phase_context_recorder` | True | `moon_phase` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `moon_phase_reflection_planner` | True | `moon_phase` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `moon_phase_request_guard` | True | `moon_phase` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `moon_phase_symbol_lookup` | True | `moon_phase` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `mystic_intake_triage` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `mystic_output_lint` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `naming_brand_scenario_scorer` | True | `naming` | `no_fate_or_compliance_guarantee`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `naming_candidate_comparator` | True | `naming` | `no_fate_or_compliance_guarantee`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `naming_symbol_lookup` | True | `naming` | `no_fate_or_compliance_guarantee`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `nine_star_ki_interpretation_planner` | True | `nine_star_ki` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `nine_star_ki_profile_recorder` | True | `nine_star_ki` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `nine_star_ki_request_guard` | True | `nine_star_ki` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `nine_star_ki_symbol_lookup` | True | `nine_star_ki` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `numerology_interpretation_planner` | True | `numerology` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `numerology_profile_recorder` | True | `numerology` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `numerology_request_guard` | True | `numerology` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `numerology_symbol_lookup` | True | `numerology` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `oracle_card_draw_recorder` | True | `oracle_card` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `oracle_card_interpretation_planner` | True | `oracle_card` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `oracle_card_request_guard` | True | `oracle_card` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `oracle_card_symbol_lookup` | True | `oracle_card` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `oracle_lot_interpretation_planner` | True | `oracle_lot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `oracle_lot_record_builder` | True | `oracle_lot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `oracle_lot_request_guard` | True | `oracle_lot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `oracle_lot_symbol_lookup` | True | `oracle_lot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `paradigm_selector` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `past_life_narrative_recorder` | True | `past_life` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `past_life_reflection_planner` | True | `past_life` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `past_life_request_guard` | True | `past_life` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `past_life_symbol_lookup` | True | `past_life` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `pendulum_interpretation_planner` | True | `pendulum` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `pendulum_request_guard` | True | `pendulum` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `pendulum_session_recorder` | True | `pendulum` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `pendulum_symbol_lookup` | True | `pendulum` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `pet_communication_context_recorder` | True | `pet_communication` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `pet_communication_reflection_planner` | True | `pet_communication` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `pet_communication_request_guard` | True | `pet_communication` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `pet_communication_symbol_lookup` | True | `pet_communication` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `physiognomy_interpretation_planner` | True | `physiognomy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `physiognomy_observation_recorder` | True | `physiognomy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `physiognomy_request_guard` | True | `physiognomy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `physiognomy_symbol_lookup` | True | `physiognomy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `pilot_readiness_report` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `planetary_retrograde_context_recorder` | True | `planetary_retrograde` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `planetary_retrograde_reflection_planner` | True | `planetary_retrograde` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `planetary_retrograde_request_guard` | True | `planetary_retrograde` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `planetary_retrograde_symbol_lookup` | True | `planetary_retrograde` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `psychometry_object_recorder` | True | `psychometry` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `psychometry_reflection_planner` | True | `psychometry` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `psychometry_request_guard` | True | `psychometry` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `psychometry_symbol_lookup` | True | `psychometry` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `qimen_chart_record` | True | `qimen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `qimen_focus_selector` | True | `qimen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `qimen_method_guard` | True | `qimen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `qimen_school_reference` | True | `qimen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `relationship_luck_action_planner` | True | `relationship_luck` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `relationship_luck_context_recorder` | True | `relationship_luck` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `relationship_luck_request_guard` | True | `relationship_luck` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `relationship_luck_symbol_lookup` | True | `relationship_luck` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `release_gate_runner` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `release_manifest_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `ritual_low_risk_protocol` | True | `ritual` | `dangerous_materials_guarded`, `low_risk_only`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `ritual_safety_check` | True | `ritual` | `dangerous_materials_guarded`, `low_risk_only`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `ritual_source_example_lookup` | True | `ritual` | `dangerous_materials_guarded`, `low_risk_only`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `ritual_source_guard` | True | `ritual` | `dangerous_materials_guarded`, `low_risk_only`, `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `rune_cast_recorder` | True | `rune` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `rune_interpretation_planner` | True | `rune` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `rune_request_guard` | True | `rune` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `rune_symbol_lookup` | True | `rune` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `scrying_interpretation_planner` | True | `scrying` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `scrying_observation_recorder` | True | `scrying` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `scrying_request_guard` | True | `scrying` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `scrying_symbol_lookup` | True | `scrying` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sigil_context_recorder` | True | `sigil` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sigil_practice_planner` | True | `sigil` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sigil_request_guard` | True | `sigil` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sigil_symbol_lookup` | True | `sigil` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `skill_install_readiness_report` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `skill_replay_runner` | True | `animal_omen`, `aroma`, `astrology`, `aura_chakra`, `bibliomancy`, `body_omen`, `candle`, `cartomancy`, `casting_lots`, `character_divination`, `color`, `consecration`, `crystal`, `date_selection`, `deity_ancestor`, `dice`, `dowsing`, `dream`, `fengshui`, `flower`, `folk_custom`, `herbal`, `human_design`, `incense`, `lenormand`, `liuyao`, `lost_object`, `manifestation`, `meihua`, `mingli`, `moon_phase`, `naming`, `nine_star_ki`, `numerology`, `oracle_card`, `oracle_lot`, `past_life`, `pendulum`, `pet_communication`, `physiognomy`, `planetary_retrograde`, `psychometry`, `qimen`, `relationship_luck`, `ritual`, `rune`, `scrying`, `sigil`, `sky_omen`, `sleep_paralysis`, `sound_cleansing`, `spirit_message`, `spiritual_protection`, `synchronicity`, `talisman`, `tarot`, `tasseography`, `wealth_luck`, `western_geomancy`, `yijing`, `zodiac` | `birth_data_minimization`, `dangerous_materials_guarded`, `low_risk_only`, `no_deterministic_disaster_claims`, `no_fatalism`, `no_fate_or_compliance_guarantee`, `professional_boundary_required`, `real_world_safety_first`, `symbolic_interpretation_only`, `third_party_privacy` | - |
| `skill_transcript_runner` | True | `animal_omen`, `aroma`, `astrology`, `aura_chakra`, `bibliomancy`, `body_omen`, `candle`, `cartomancy`, `casting_lots`, `character_divination`, `color`, `consecration`, `crystal`, `date_selection`, `deity_ancestor`, `dice`, `dowsing`, `dream`, `fengshui`, `flower`, `folk_custom`, `herbal`, `human_design`, `incense`, `lenormand`, `liuyao`, `lost_object`, `manifestation`, `meihua`, `mingli`, `moon_phase`, `naming`, `nine_star_ki`, `numerology`, `oracle_card`, `oracle_lot`, `past_life`, `pendulum`, `pet_communication`, `physiognomy`, `planetary_retrograde`, `psychometry`, `qimen`, `relationship_luck`, `ritual`, `rune`, `scrying`, `sigil`, `sky_omen`, `sleep_paralysis`, `sound_cleansing`, `spirit_message`, `spiritual_protection`, `synchronicity`, `talisman`, `tarot`, `tasseography`, `wealth_luck`, `western_geomancy`, `yijing`, `zodiac` | `birth_data_minimization`, `dangerous_materials_guarded`, `low_risk_only`, `no_deterministic_disaster_claims`, `no_fatalism`, `no_fate_or_compliance_guarantee`, `professional_boundary_required`, `real_world_safety_first`, `symbolic_interpretation_only`, `third_party_privacy` | - |
| `sky_omen_observation_recorder` | True | `sky_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sky_omen_reflection_planner` | True | `sky_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sky_omen_request_guard` | True | `sky_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sky_omen_symbol_lookup` | True | `sky_omen` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sleep_paralysis_context_recorder` | True | `sleep_paralysis` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sleep_paralysis_reflection_planner` | True | `sleep_paralysis` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sleep_paralysis_request_guard` | True | `sleep_paralysis` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sleep_paralysis_symbol_lookup` | True | `sleep_paralysis` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sop_traceability_matrix_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `sound_cleansing_context_recorder` | True | `sound_cleansing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sound_cleansing_practice_planner` | True | `sound_cleansing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sound_cleansing_request_guard` | True | `sound_cleansing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `sound_cleansing_symbol_lookup` | True | `sound_cleansing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `spirit_message_record_builder` | True | `spirit_message` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `spirit_message_reflection_planner` | True | `spirit_message` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `spirit_message_request_guard` | True | `spirit_message` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `spirit_message_symbol_lookup` | True | `spirit_message` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `spiritual_protection_context_recorder` | True | `spiritual_protection` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `spiritual_protection_reflection_planner` | True | `spiritual_protection` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `spiritual_protection_request_guard` | True | `spiritual_protection` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `spiritual_protection_symbol_lookup` | True | `spiritual_protection` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `symbolic_case_library` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `symbolic_depth_lookup` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `synchronicity_event_recorder` | True | `synchronicity` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `synchronicity_reflection_planner` | True | `synchronicity` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `synchronicity_request_guard` | True | `synchronicity` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `synchronicity_symbol_lookup` | True | `synchronicity` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `talisman_record_builder` | True | `talisman` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `talisman_request_guard` | True | `talisman` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `talisman_symbol_lookup` | True | `talisman` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `talisman_use_planner` | True | `talisman` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tarot_card_lookup` | True | `tarot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tarot_combination_planner` | True | `tarot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tarot_draw_recorder` | True | `tarot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tarot_draw_simulator` | True | `tarot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tarot_interpretation_planner` | True | `tarot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tarot_spread_selector` | True | `tarot` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tasseography_interpretation_planner` | True | `tasseography` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tasseography_pattern_recorder` | True | `tasseography` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tasseography_request_guard` | True | `tasseography` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tasseography_symbol_lookup` | True | `tasseography` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `tool_manifest_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `transcript_anonymizer` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `transcript_fixture_builder` | True | `shared` | `professional_boundary_required`, `runtime_infrastructure`, `symbolic_interpretation_only` | - |
| `wealth_luck_action_planner` | True | `wealth_luck` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `wealth_luck_context_recorder` | True | `wealth_luck` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `wealth_luck_request_guard` | True | `wealth_luck` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `wealth_luck_symbol_lookup` | True | `wealth_luck` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `western_geomancy_chart_recorder` | True | `western_geomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `western_geomancy_figure_lookup` | True | `western_geomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `western_geomancy_interpretation_planner` | True | `western_geomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `western_geomancy_request_guard` | True | `western_geomancy` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `yijing_casting_method_advisor` | True | `yijing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `yijing_casting_simulator` | True | `yijing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `yijing_hexagram_lookup` | True | `yijing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `yijing_hexagram_record` | True | `yijing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `yijing_line_lookup` | True | `yijing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `yijing_question_guard` | True | `yijing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `yijing_source_reference_guard` | True | `yijing` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `zodiac_interpretation_planner` | True | `zodiac` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `zodiac_profile_recorder` | True | `zodiac` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `zodiac_request_guard` | True | `zodiac` | `professional_boundary_required`, `symbolic_interpretation_only` | - |
| `zodiac_symbol_lookup` | True | `zodiac` | `professional_boundary_required`, `symbolic_interpretation_only` | - |

## 限制

- 此验证只检查注册形状和本地文件引用，不执行工具。
- schema 为 object 不代表业务语义充分，仍需工具内部验证和 runtime dry-run。
- OpenAI-style 形状有效不表示已绑定真实命令执行器。
