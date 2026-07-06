from pathlib import Path
import tempfile
import unittest

from agent_tools_scripts import (
    agent_route_smoke_runner,
    agent_runtime_dry_run_runner,
    agent_runtime_handoff_builder,
    agent_tool_definition_exporter,
    agent_tool_definition_validator,
    agent_tool_registry_builder,
    agent_tool_registry_validator,
    agent_tool_wrapper_manifest_builder,
    consultation_case_recorder,
    consultation_handoff_builder,
    agent_workflow_router,
    consultation_packet_builder,
    paradigm_selector,
    almanac_symbol_lookup,
    astrology_chart_record,
    astrology_compatibility_guard,
    mystic_intake_triage,
    mystic_output_lint,
    astrology_symbol_lookup,
    bazi_ziwei_chart_record,
    bazi_ziwei_intake_guard,
    codex_skill_blueprint_validator,
    codex_skill_installer,
    content_review_feedback_recorder,
    content_review_packet_builder,
    date_constraint_recorder,
    date_option_ranker,
    date_selection_guard,
    dream_interpretation_planner,
    dream_record_builder,
    dream_symbol_lookup,
    domain_evidence_matrix_builder,
    external_evidence_intake_builder,
    folk_custom_lookup,
    folk_source_recorder,
    folk_taboo_reframer,
    fengshui_bagua_mapper,
    fengshui_observation_recorder,
    fengshui_school_guard,
    fengshui_space_checklist,
    fengshui_yangzhai_case_library,
    fengshui_recommendation_ranker,
    knowledge_coverage_audit,
    knowledge_navigation_builder,
    liuyao_chart_recorder,
    liuyao_focus_selector,
    liuyao_symbol_lookup,
    meihua_casting_recorder,
    meihua_omen_recorder,
    meihua_relation_interpreter,
    meihua_symbol_lookup,
    naming_brand_scenario_scorer,
    naming_candidate_comparator,
    naming_symbol_lookup,
    oracle_lot_interpretation_planner,
    oracle_lot_record_builder,
    oracle_lot_request_guard,
    oracle_lot_symbol_lookup,
    oracle_card_draw_recorder,
    oracle_card_interpretation_planner,
    oracle_card_request_guard,
    oracle_card_symbol_lookup,
    cartomancy_card_lookup,
    cartomancy_draw_recorder,
    cartomancy_interpretation_planner,
    cartomancy_request_guard,
    dice_interpretation_planner,
    dice_request_guard,
    dice_roll_recorder,
    dice_symbol_lookup,
    tasseography_interpretation_planner,
    tasseography_pattern_recorder,
    tasseography_request_guard,
    tasseography_symbol_lookup,
    numerology_interpretation_planner,
    numerology_profile_recorder,
    numerology_request_guard,
    numerology_symbol_lookup,
    pendulum_interpretation_planner,
    pendulum_request_guard,
    pendulum_session_recorder,
    pendulum_symbol_lookup,
    rune_cast_recorder,
    rune_interpretation_planner,
    rune_request_guard,
    rune_symbol_lookup,
    lenormand_card_lookup,
    lenormand_draw_recorder,
    lenormand_interpretation_planner,
    lenormand_request_guard,
    crystal_item_recorder,
    crystal_request_guard,
    crystal_symbol_lookup,
    crystal_use_planner,
    candle_interpretation_planner,
    candle_observation_recorder,
    candle_request_guard,
    candle_symbol_lookup,
    incense_interpretation_planner,
    incense_observation_recorder,
    incense_request_guard,
    incense_symbol_lookup,
    aroma_context_recorder,
    aroma_practice_planner,
    aroma_request_guard,
    aroma_symbol_lookup,
    herbal_context_recorder,
    herbal_practice_planner,
    herbal_request_guard,
    herbal_symbol_lookup,
    sigil_context_recorder,
    sigil_practice_planner,
    sigil_request_guard,
    sigil_symbol_lookup,
    dowsing_context_recorder,
    dowsing_practice_planner,
    dowsing_request_guard,
    dowsing_symbol_lookup,
    body_omen_context_recorder,
    body_omen_reflection_planner,
    body_omen_request_guard,
    body_omen_symbol_lookup,
    scrying_interpretation_planner,
    scrying_observation_recorder,
    scrying_request_guard,
    scrying_symbol_lookup,
    casting_lots_interpretation_planner,
    casting_lots_layout_recorder,
    casting_lots_request_guard,
    casting_lots_symbol_lookup,
    cezi_character_recorder,
    cezi_interpretation_planner,
    cezi_request_guard,
    cezi_symbol_lookup,
    flower_interpretation_planner,
    flower_item_recorder,
    flower_request_guard,
    flower_symbol_lookup,
    animal_omen_interpretation_planner,
    animal_omen_observation_recorder,
    animal_omen_request_guard,
    animal_omen_symbol_lookup,
    aura_chakra_reflection_planner,
    aura_chakra_request_guard,
    aura_chakra_sensation_recorder,
    aura_chakra_symbol_lookup,
    past_life_narrative_recorder,
    past_life_reflection_planner,
    past_life_request_guard,
    past_life_symbol_lookup,
    moon_phase_context_recorder,
    moon_phase_reflection_planner,
    moon_phase_request_guard,
    moon_phase_symbol_lookup,
    spirit_message_record_builder,
    spirit_message_reflection_planner,
    spirit_message_request_guard,
    spirit_message_symbol_lookup,
    psychometry_object_recorder,
    psychometry_reflection_planner,
    psychometry_request_guard,
    psychometry_symbol_lookup,
    bibliomancy_reflection_planner,
    bibliomancy_request_guard,
    bibliomancy_source_recorder,
    bibliomancy_symbol_lookup,
    sky_omen_observation_recorder,
    sky_omen_reflection_planner,
    sky_omen_request_guard,
    sky_omen_symbol_lookup,
    manifestation_intention_recorder,
    manifestation_reflection_planner,
    manifestation_request_guard,
    manifestation_symbol_lookup,
    pet_communication_context_recorder,
    pet_communication_reflection_planner,
    pet_communication_request_guard,
    pet_communication_symbol_lookup,
    synchronicity_event_recorder,
    synchronicity_reflection_planner,
    synchronicity_request_guard,
    synchronicity_symbol_lookup,
    planetary_retrograde_context_recorder,
    planetary_retrograde_reflection_planner,
    planetary_retrograde_request_guard,
    planetary_retrograde_symbol_lookup,
    spiritual_protection_context_recorder,
    spiritual_protection_reflection_planner,
    spiritual_protection_request_guard,
    spiritual_protection_symbol_lookup,
    deity_ancestor_context_recorder,
    deity_ancestor_reflection_planner,
    deity_ancestor_request_guard,
    deity_ancestor_symbol_lookup,
    sleep_paralysis_context_recorder,
    sleep_paralysis_reflection_planner,
    sleep_paralysis_request_guard,
    sleep_paralysis_symbol_lookup,
    wealth_luck_action_planner,
    wealth_luck_context_recorder,
    wealth_luck_request_guard,
    wealth_luck_symbol_lookup,
    relationship_luck_action_planner,
    relationship_luck_context_recorder,
    relationship_luck_request_guard,
    relationship_luck_symbol_lookup,
    consecration_care_planner,
    consecration_context_recorder,
    consecration_request_guard,
    consecration_symbol_lookup,
    lost_object_context_recorder,
    lost_object_request_guard,
    lost_object_search_planner,
    lost_object_symbol_lookup,
    sound_cleansing_context_recorder,
    sound_cleansing_practice_planner,
    sound_cleansing_request_guard,
    sound_cleansing_symbol_lookup,
    western_geomancy_chart_recorder,
    western_geomancy_figure_lookup,
    western_geomancy_interpretation_planner,
    western_geomancy_request_guard,
    nine_star_ki_interpretation_planner,
    nine_star_ki_profile_recorder,
    nine_star_ki_request_guard,
    nine_star_ki_symbol_lookup,
    human_design_interpretation_planner,
    human_design_chart_recorder,
    human_design_request_guard,
    human_design_symbol_lookup,
    talisman_record_builder,
    talisman_request_guard,
    talisman_symbol_lookup,
    talisman_use_planner,
    color_palette_planner,
    color_profile_recorder,
    color_request_guard,
    color_symbol_lookup,
    zodiac_interpretation_planner,
    zodiac_profile_recorder,
    zodiac_request_guard,
    zodiac_symbol_lookup,
    physiognomy_interpretation_planner,
    physiognomy_observation_recorder,
    physiognomy_request_guard,
    physiognomy_symbol_lookup,
    pilot_readiness_report,
    release_gate_runner,
    release_manifest_builder,
    tool_manifest_builder,
    mingli_school_reference,
    mingli_symbol_lookup,
    qimen_method_guard,
    qimen_school_reference,
    qimen_chart_record,
    qimen_focus_selector,
    ritual_low_risk_protocol,
    ritual_safety_check,
    ritual_source_example_lookup,
    ritual_source_guard,
    skill_install_readiness_report,
    skill_replay_runner,
    skill_transcript_runner,
    sop_traceability_matrix_builder,
    symbolic_case_library,
    symbolic_depth_lookup,
    transcript_anonymizer,
    transcript_fixture_builder,
    yijing_casting_method_advisor,
    tarot_card_lookup,
    tarot_combination_planner,
    tarot_draw_recorder,
    tarot_draw_simulator,
    tarot_interpretation_planner,
    tarot_spread_selector,
    yijing_casting_simulator,
    yijing_hexagram_lookup,
    yijing_hexagram_record,
    yijing_line_lookup,
    yijing_question_guard,
    yijing_source_reference_guard,
)


class MysticIntakeTriageTests(unittest.TestCase):
    def test_tarot_request_is_green(self):
        result = mystic_intake_triage.triage({"request_text": "帮我做一个塔罗三张牌，看看工作状态"})
        self.assertEqual(result["domain"], "tarot")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_tarot_sop", result["allowed_next_steps"])

    def test_dangerous_ritual_is_red(self):
        result = mystic_intake_triage.triage({"request_text": "我想放血做驱邪仪式"})
        self.assertEqual(result["domain"], "ritual_safety")
        self.assertEqual(result["risk_level"], "red")
        self.assertIn("stop_mystic_workflow", result["allowed_next_steps"])

    def test_financial_prediction_is_orange(self):
        result = mystic_intake_triage.triage({"request_text": "用塔罗看看我明天要不要贷款梭哈股票"})
        self.assertEqual(result["risk_level"], "orange")
        self.assertNotIn("load_tarot_sop", result["allowed_next_steps"])

    def test_bazi_request_routes_to_mingli(self):
        result = mystic_intake_triage.triage({"request_text": "想用八字看看事业倾向"})
        self.assertEqual(result["domain"], "mingli")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_mingli_sop", result["allowed_next_steps"])

    def test_astrology_request_routes_to_astrology(self):
        result = mystic_intake_triage.triage({"request_text": "想用占星看看太阳天秤和月亮巨蟹的性格倾向"})
        self.assertEqual(result["domain"], "astrology")
        self.assertEqual(result["intent"], "chart_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_astrology_sop", result["allowed_next_steps"])

    def test_liuyao_request_routes_to_liuyao(self):
        result = mystic_intake_triage.triage({"request_text": "用六爻看看这个项目合作，世爻兄弟应爻官鬼"})
        self.assertEqual(result["domain"], "liuyao")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_liuyao_sop", result["allowed_next_steps"])

    def test_meihua_request_routes_to_meihua(self):
        result = mystic_intake_triage.triage({"request_text": "用梅花易数报数起卦看这个项目沟通"})
        self.assertEqual(result["domain"], "meihua")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_meihua_sop", result["allowed_next_steps"])

    def test_naming_request_routes_to_naming(self):
        result = mystic_intake_triage.triage({"request_text": "想给宝宝取名，看看字义和五行取名"})
        self.assertEqual(result["domain"], "naming")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_naming_sop", result["allowed_next_steps"])

    def test_brand_name_request_routes_to_naming(self):
        result = mystic_intake_triage.triage({"request_text": "给茶饮品牌比较星禾和清朗，目标年轻上班族"})
        self.assertEqual(result["domain"], "naming")
        self.assertEqual(result["intent"], "name_review")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_naming_sop", result["allowed_next_steps"])

    def test_physiognomy_request_routes_to_physiognomy(self):
        result = mystic_intake_triage.triage({"request_text": "帮我看手相，生命线和事业线代表什么，只做象征解读"})
        self.assertEqual(result["domain"], "physiognomy")
        self.assertEqual(result["intent"], "appearance_symbol_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_physiognomy_sop", result["allowed_next_steps"])

    def test_oracle_lot_request_routes_to_oracle_lot(self):
        result = mystic_intake_triage.triage({"request_text": "我抽到一支月老签，上签，想解签看看关系沟通提醒"})
        self.assertEqual(result["domain"], "oracle_lot")
        self.assertEqual(result["intent"], "oracle_lot_interpretation")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_oracle_lot_sop", result["allowed_next_steps"])

    def test_oracle_card_request_routes_to_oracle_card(self):
        result = mystic_intake_triage.triage({"request_text": "用神谕卡三张看项目沟通，只做象征反思"})
        self.assertEqual(result["domain"], "oracle_card")
        self.assertEqual(result["intent"], "oracle_card_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_oracle_card_sop", result["allowed_next_steps"])

    def test_numerology_request_routes_to_numerology(self):
        result = mystic_intake_triage.triage({"request_text": "比较手机号尾号 168 和 739，只做数字象征和记忆度分析"})
        self.assertEqual(result["domain"], "numerology")
        self.assertEqual(result["intent"], "number_symbol_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_numerology_sop", result["allowed_next_steps"])

    def test_pendulum_request_routes_to_pendulum(self):
        result = mystic_intake_triage.triage({"request_text": "用灵摆做一次低风险自我反思，左右摆是什么意思"})
        self.assertEqual(result["domain"], "pendulum")
        self.assertEqual(result["intent"], "pendulum_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_pendulum_sop", result["allowed_next_steps"])

    def test_rune_request_routes_to_rune(self):
        result = mystic_intake_triage.triage({"request_text": "用卢恩符文抽三符看项目推进，只做象征反思"})
        self.assertEqual(result["domain"], "rune")
        self.assertEqual(result["intent"], "rune_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_rune_sop", result["allowed_next_steps"])

    def test_lenormand_request_routes_to_lenormand(self):
        result = mystic_intake_triage.triage({"request_text": "用雷诺曼三张牌看项目沟通，只做象征反思"})
        self.assertEqual(result["domain"], "lenormand")
        self.assertEqual(result["intent"], "lenormand_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_lenormand_sop", result["allowed_next_steps"])

    def test_crystal_request_routes_to_crystal(self):
        result = mystic_intake_triage.triage({"request_text": "想在办公桌放白水晶和紫水晶，只做提醒和空间秩序"})
        self.assertEqual(result["domain"], "crystal")
        self.assertEqual(result["intent"], "crystal_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_crystal_sop", result["allowed_next_steps"])

    def test_candle_request_routes_to_candle(self):
        result = mystic_intake_triage.triage({"request_text": "我已经熄灭蜡烛，看到火焰稳定、蜡泪像河流，想做项目推进的低风险提醒"})
        self.assertEqual(result["domain"], "candle")
        self.assertEqual(result["intent"], "candle_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_candle_sop", result["allowed_next_steps"])

    def test_incense_request_routes_to_incense(self):
        result = mystic_intake_triage.triage({"request_text": "我已经确认香熄灭了，香灰像塔形、烟之前直上，想做项目推进的低风险提醒"})
        self.assertEqual(result["domain"], "incense")
        self.assertEqual(result["intent"], "incense_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_incense_sop", result["allowed_next_steps"])

    def test_aroma_request_routes_to_aroma(self):
        result = mystic_intake_triage.triage({"request_text": "想用芳香精油做低风险气味象征，已有薰衣草和柑橘闻香纸，只做睡前收束和空间切换，不内服不直接涂不治疗不碰宠物不高价购买不反复闻"})
        self.assertEqual(result["domain"], "aroma")
        self.assertEqual(result["intent"], "aroma_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_aroma_sop", result["allowed_next_steps"])

    def test_herbal_request_routes_to_herbal(self):
        result = mystic_intake_triage.triage({"request_text": "想用草本香草做低风险植物象征，已有迷迭香和月桂叶植物意图卡，不内服不泡水喝不外敷不野采不用明火不治疗不碰宠物不下咒不高价购买不反复做"})
        self.assertEqual(result["domain"], "herbal")
        self.assertEqual(result["intent"], "herbal_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_herbal_sop", result["allowed_next_steps"])

    def test_sigil_request_routes_to_sigil(self):
        result = mystic_intake_triage.triage({"request_text": "想做一个 sigil 符号印记当项目专注提醒，只用纸上草稿、圆形和钥匙符号、放笔记本一周后复盘，不用血不刻皮肤不纹身不烧不召唤不驱邪不诅咒不操控别人不保证实现不高价购买不反复画"})
        self.assertEqual(result["domain"], "sigil")
        self.assertEqual(result["intent"], "sigil_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_sigil_sop", result["allowed_next_steps"])

    def test_dowsing_request_routes_to_dowsing(self):
        result = mystic_intake_triage.triage({"request_text": "想用占杖探测棒做低风险空间象征，观察自己书房入口和桌面动线，记录双杆交叉和路线提示，只做整理复盘，不找地下水不挖不打井不替代专业探测不定位别人不驱邪不高价购买不反复探"})
        self.assertEqual(result["domain"], "dowsing")
        self.assertEqual(result["intent"], "dowsing_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_dowsing_sop", result["allowed_next_steps"])

    def test_body_omen_request_routes_to_body_omen(self):
        result = mystic_intake_triage.triage({"request_text": "左眼跳了一下，想按身体征兆民俗做低风险记录，只当休息和节奏提醒，不作身体结论不买彩票不判断别人不驱邪不反复查"})
        self.assertEqual(result["domain"], "body_omen")
        self.assertEqual(result["intent"], "body_omen_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_body_omen_sop", result["allowed_next_steps"])

    def test_scrying_request_routes_to_scrying(self):
        result = mystic_intake_triage.triage({"request_text": "我短时看了水晶球，已经结束，看到像门和波纹，想做项目推进的低风险提醒"})
        self.assertEqual(result["domain"], "scrying")
        self.assertEqual(result["intent"], "scrying_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_scrying_sop", result["allowed_next_steps"])

    def test_casting_lots_request_routes_to_casting_lots(self):
        result = mystic_intake_triage.triage({"request_text": "我用贝壳、钥匙和石子做了一次小物抛掷，想看项目协作的低风险提醒"})
        self.assertEqual(result["domain"], "casting_lots")
        self.assertEqual(result["intent"], "casting_lots_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_casting_lots_sop", result["allowed_next_steps"])

    def test_cezi_request_routes_to_character_divination(self):
        result = mystic_intake_triage.triage({"request_text": "我想测字，写了一个明字，拆成日和月，只做项目沟通的低风险提醒"})
        self.assertEqual(result["domain"], "character_divination")
        self.assertEqual(result["intent"], "character_divination_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_character_divination_sop", result["allowed_next_steps"])

    def test_flower_request_routes_to_flower(self):
        result = mystic_intake_triage.triage({"request_text": "想用花语选一束向日葵和白色百合送给同事，只做感谢和边界表达，不买贵的"})
        self.assertEqual(result["domain"], "flower")
        self.assertEqual(result["intent"], "flower_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_flower_sop", result["allowed_next_steps"])

    def test_animal_omen_request_routes_to_animal_omen(self):
        result = mystic_intake_triage.triage({"request_text": "早上有一只鸟飞进阳台又飞走了，想了解民俗象征，只做低风险观察反思"})
        self.assertEqual(result["domain"], "animal_omen")
        self.assertEqual(result["intent"], "animal_omen_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_animal_omen_sop", result["allowed_next_steps"])

    def test_aura_chakra_request_routes_to_aura_chakra(self):
        result = mystic_intake_triage.triage({"request_text": "冥想时感觉喉轮有点堵，看到蓝色，只想做低风险记录和表达边界反思"})
        self.assertEqual(result["domain"], "aura_chakra")
        self.assertEqual(result["intent"], "aura_chakra_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_aura_chakra_sop", result["allowed_next_steps"])

    def test_past_life_request_routes_to_past_life(self):
        result = mystic_intake_triage.triage({"request_text": "冥想里出现阿卡西图书馆和一扇门，只想做象征记录和当下边界反思，不当成真实前世记忆"})
        self.assertEqual(result["domain"], "past_life")
        self.assertEqual(result["intent"], "past_life_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_past_life_sop", result["allowed_next_steps"])

    def test_moon_phase_request_routes_to_moon_phase(self):
        result = mystic_intake_triage.triage({"request_text": "今晚新月想做无火的意图书写，只整理项目计划和复盘，不保证显化"})
        self.assertEqual(result["domain"], "moon_phase")
        self.assertEqual(result["intent"], "moon_phase_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_moon_phase_sop", result["allowed_next_steps"])

    def test_spirit_message_request_routes_to_spirit_message(self):
        result = mystic_intake_triage.triage({"request_text": "冥想后像是收到一句高我讯息：先照顾边界。只想做象征写作和现实行动反思"})
        self.assertEqual(result["domain"], "spirit_message")
        self.assertEqual(result["intent"], "spirit_message_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_spirit_message_sop", result["allowed_next_steps"])

    def test_talisman_request_routes_to_talisman(self):
        result = mystic_intake_triage.triage({"request_text": "想了解家人送的平安符，放钱包里当提醒，不做驱邪保证"})
        self.assertEqual(result["domain"], "talisman")
        self.assertEqual(result["intent"], "talisman_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_talisman_sop", result["allowed_next_steps"])

    def test_color_request_routes_to_color(self):
        result = mystic_intake_triage.triage({"request_text": "明天面试想用五行颜色做提醒，已有白衬衫和绿色丝巾，不买新衣服"})
        self.assertEqual(result["domain"], "color")
        self.assertEqual(result["intent"], "color_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_color_sop", result["allowed_next_steps"])

    def test_dice_request_routes_to_dice(self):
        result = mystic_intake_triage.triage({"request_text": "我用星骰掷到火星、白羊座、第十宫，想看项目推进的低风险提醒"})
        self.assertEqual(result["domain"], "dice")
        self.assertEqual(result["intent"], "dice_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_dice_sop", result["allowed_next_steps"])

    def test_cartomancy_request_routes_to_cartomancy(self):
        result = mystic_intake_triage.triage({"request_text": "用扑克牌占卜三张看项目合作，只做象征反思"})
        self.assertEqual(result["domain"], "cartomancy")
        self.assertEqual(result["intent"], "cartomancy_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_cartomancy_sop", result["allowed_next_steps"])

    def test_tasseography_request_routes_to_tasseography(self):
        result = mystic_intake_triage.triage({"request_text": "我杯底咖啡渣像鸟和路，想做项目沟通的低风险象征反思"})
        self.assertEqual(result["domain"], "tasseography")
        self.assertEqual(result["intent"], "tasseography_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_tasseography_sop", result["allowed_next_steps"])

    def test_zodiac_request_routes_to_zodiac(self):
        result = mystic_intake_triage.triage({"request_text": "我属龙，今年本命年，想了解太岁文化和低风险提醒，不做灾祸判断"})
        self.assertEqual(result["domain"], "zodiac")
        self.assertEqual(result["intent"], "zodiac_reflection")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_zodiac_sop", result["allowed_next_steps"])

    def test_folk_custom_request_routes_to_folk_custom(self):
        result = mystic_intake_triage.triage({"request_text": "讲讲端午和艾草香囊的民俗传统"})
        self.assertEqual(result["domain"], "folk_custom")
        self.assertEqual(result["risk_level"], "green")
        self.assertIn("load_folk_custom_sop", result["allowed_next_steps"])

    def test_fengshui_liqi_request_routes_to_feng_shui(self):
        result = mystic_intake_triage.triage({"request_text": "用玄空飞星看看厨房五黄是不是破财"})
        self.assertEqual(result["domain"], "feng_shui")
        self.assertEqual(result["intent"], "space_review")

    def test_dream_request_routes_to_dream_reflection(self):
        result = mystic_intake_triage.triage({"request_text": "帮我解梦，梦见考试迟到又找不到教室"})
        self.assertEqual(result["domain"], "dream")
        self.assertEqual(result["intent"], "dream_reflection")
        self.assertIn("load_dream_sop", result["allowed_next_steps"])

    def test_date_selection_request_routes_to_date_selection(self):
        result = mystic_intake_triage.triage({"request_text": "想选一个搬家吉日，周末最好"})
        self.assertEqual(result["domain"], "date_selection")
        self.assertEqual(result["intent"], "date_selection")
        self.assertIn("load_date_selection_sop", result["allowed_next_steps"])


class AgentWorkflowRouterTests(unittest.TestCase):
    def test_tarot_request_routes_to_skill_sop_and_initial_tools(self):
        result = agent_workflow_router.route({"request_text": "帮我做一个塔罗三张牌，看看工作状态"})
        self.assertEqual(result["tool"], "agent_workflow_router")
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertTrue(result["can_continue_mystic_workflow"])
        self.assertEqual(result["domain"], "tarot")
        self.assertEqual(result["skill"], "tarot-symbolic-reading")
        self.assertIn("知识库/SOP/01-塔罗解读.md", result["sop"])
        self.assertIn("tarot_spread_selector", result["initial_tools"])
        self.assertEqual(result["initial_tools"].count("mystic_intake_triage"), 1)

    def test_feng_shui_alias_routes_to_fengshui_domain(self):
        result = agent_workflow_router.route({"request_text": "用玄空飞星看看厨房五黄是不是破财"})
        self.assertEqual(result["domain"], "fengshui")
        self.assertEqual(result["original_domain"], "feng_shui")
        self.assertEqual(result["skill"], "feng-shui-space-audit")
        self.assertIn("fengshui_school_guard", result["domain_tools"])

    def test_dream_request_routes_to_dream_skill(self):
        result = agent_workflow_router.route({"request_text": "帮我解梦，梦见考试迟到又找不到教室"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "dream")
        self.assertEqual(result["skill"], "dream-symbolic-consultation")
        self.assertIn("dream_interpretation_planner", result["initial_tools"])

    def test_date_selection_request_routes_to_date_selection_skill(self):
        result = agent_workflow_router.route({"request_text": "想选一个搬家吉日，2026-08-08 或 2026-08-15，周末最好"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "date_selection")
        self.assertEqual(result["skill"], "date-selection-consultation")
        self.assertIn("date_option_ranker", result["initial_tools"])

    def test_physiognomy_request_routes_to_physiognomy_skill(self):
        result = agent_workflow_router.route({"request_text": "帮我看手相，生命线和事业线代表什么，只做象征解读"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "physiognomy")
        self.assertEqual(result["skill"], "physiognomy-symbolic-consultation")
        self.assertIn("physiognomy_interpretation_planner", result["initial_tools"])

    def test_oracle_lot_request_routes_to_oracle_lot_skill(self):
        result = agent_workflow_router.route({"request_text": "我抽到一支月老签，上签，想解签看看关系沟通提醒"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "oracle_lot")
        self.assertEqual(result["skill"], "oracle-lot-symbolic-consultation")
        self.assertIn("oracle_lot_interpretation_planner", result["initial_tools"])

    def test_oracle_card_request_routes_to_oracle_card_skill(self):
        result = agent_workflow_router.route({"request_text": "用神谕卡三张看项目沟通，只做象征反思：门、桥、种子"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "oracle_card")
        self.assertEqual(result["skill"], "oracle-card-symbolic-consultation")
        self.assertIn("oracle_card_interpretation_planner", result["initial_tools"])

    def test_numerology_request_routes_to_numerology_skill(self):
        result = agent_workflow_router.route({"request_text": "比较手机号尾号 168 和 739，只做数字象征和记忆度分析"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "numerology")
        self.assertEqual(result["skill"], "numerology-symbolic-consultation")
        self.assertIn("numerology_interpretation_planner", result["initial_tools"])

    def test_pendulum_request_routes_to_pendulum_skill(self):
        result = agent_workflow_router.route({"request_text": "用灵摆做一次低风险自我反思，左右摆代表我需要比较沟通方案吗"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "pendulum")
        self.assertEqual(result["skill"], "pendulum-symbolic-consultation")
        self.assertIn("pendulum_interpretation_planner", result["initial_tools"])

    def test_rune_request_routes_to_rune_skill(self):
        result = agent_workflow_router.route({"request_text": "用卢恩符文抽三符看项目推进，只做象征反思"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "rune")
        self.assertEqual(result["skill"], "rune-symbolic-consultation")
        self.assertIn("rune_interpretation_planner", result["initial_tools"])

    def test_lenormand_request_routes_to_lenormand_skill(self):
        result = agent_workflow_router.route({"request_text": "用雷诺曼三张牌看项目沟通，只做象征反思：骑士、信、钥匙"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "lenormand")
        self.assertEqual(result["skill"], "lenormand-symbolic-consultation")
        self.assertIn("lenormand_interpretation_planner", result["initial_tools"])

    def test_crystal_request_routes_to_crystal_skill(self):
        result = agent_workflow_router.route({"request_text": "想在办公桌放白水晶和紫水晶，只做提醒和空间秩序"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "crystal")
        self.assertEqual(result["skill"], "crystal-symbolic-consultation")
        self.assertIn("crystal_use_planner", result["initial_tools"])

    def test_candle_request_routes_to_candle_skill(self):
        result = agent_workflow_router.route({"request_text": "我已经熄灭蜡烛，看到火焰稳定、蜡泪像河流，想做项目推进的低风险提醒"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "candle")
        self.assertEqual(result["skill"], "candle-symbolic-consultation")
        self.assertIn("candle_interpretation_planner", result["initial_tools"])

    def test_incense_request_routes_to_incense_skill(self):
        result = agent_workflow_router.route({"request_text": "我已经确认香熄灭了，香灰像塔形、烟之前直上，想做项目推进的低风险提醒"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "incense")
        self.assertEqual(result["skill"], "incense-symbolic-consultation")
        self.assertIn("incense_interpretation_planner", result["initial_tools"])

    def test_aroma_request_routes_to_aroma_skill(self):
        result = agent_workflow_router.route({"request_text": "想用芳香精油做低风险气味象征，已有薰衣草和柑橘闻香纸，只做睡前收束和空间切换，不内服不直接涂不治疗不碰宠物不高价购买不反复闻"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "aroma")
        self.assertEqual(result["skill"], "aroma-symbolic-consultation")
        self.assertIn("aroma_practice_planner", result["initial_tools"])

    def test_herbal_request_routes_to_herbal_skill(self):
        result = agent_workflow_router.route({"request_text": "想用草本香草做低风险植物象征，已有迷迭香和月桂叶植物意图卡，不内服不泡水喝不外敷不野采不用明火不治疗不碰宠物不下咒不高价购买不反复做"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "herbal")
        self.assertEqual(result["skill"], "herbal-symbolic-consultation")
        self.assertIn("herbal_practice_planner", result["initial_tools"])

    def test_sigil_request_routes_to_sigil_skill(self):
        result = agent_workflow_router.route({"request_text": "想做一个 sigil 符号印记当项目专注提醒，只用纸上草稿、圆形和钥匙符号、放笔记本一周后复盘，不用血不刻皮肤不纹身不烧不召唤不驱邪不诅咒不操控别人不保证实现不高价购买不反复画"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "sigil")
        self.assertEqual(result["skill"], "sigil-symbolic-consultation")
        self.assertIn("sigil_practice_planner", result["initial_tools"])

    def test_dowsing_request_routes_to_dowsing_skill(self):
        result = agent_workflow_router.route({"request_text": "想用占杖探测棒做低风险空间象征，观察自己书房入口和桌面动线，记录双杆交叉和路线提示，只做整理复盘，不找地下水不挖不打井不替代专业探测不定位别人不驱邪不高价购买不反复探"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "dowsing")
        self.assertEqual(result["skill"], "dowsing-symbolic-consultation")
        self.assertIn("dowsing_practice_planner", result["initial_tools"])

    def test_body_omen_request_routes_to_body_omen_skill(self):
        result = agent_workflow_router.route({"request_text": "左眼跳了一下，想按身体征兆民俗做低风险记录，只当休息和节奏提醒，不作身体结论不买彩票不判断别人不驱邪不反复查"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "body_omen")
        self.assertEqual(result["skill"], "body-omen-symbolic-consultation")
        self.assertIn("body_omen_reflection_planner", result["initial_tools"])

    def test_scrying_request_routes_to_scrying_skill(self):
        result = agent_workflow_router.route({"request_text": "我短时看了水晶球，已经结束，看到像门和波纹，想做项目推进的低风险提醒"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "scrying")
        self.assertEqual(result["skill"], "scrying-symbolic-consultation")
        self.assertIn("scrying_interpretation_planner", result["initial_tools"])

    def test_casting_lots_request_routes_to_casting_lots_skill(self):
        result = agent_workflow_router.route({"request_text": "我用贝壳、钥匙和石子做了一次小物抛掷，想看项目协作的低风险提醒"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "casting_lots")
        self.assertEqual(result["skill"], "casting-lots-symbolic-consultation")
        self.assertIn("casting_lots_interpretation_planner", result["initial_tools"])

    def test_cezi_request_routes_to_character_divination_skill(self):
        result = agent_workflow_router.route({"request_text": "我想测字，写了一个明字，拆成日和月，只做项目沟通的低风险提醒"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "character_divination")
        self.assertEqual(result["skill"], "character-divination-symbolic-consultation")
        self.assertIn("cezi_interpretation_planner", result["initial_tools"])

    def test_flower_request_routes_to_flower_skill(self):
        result = agent_workflow_router.route({"request_text": "想用花语选一束向日葵和白色百合送给同事，只做感谢和边界表达，不买贵的"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "flower")
        self.assertEqual(result["skill"], "flower-symbolic-consultation")
        self.assertIn("flower_interpretation_planner", result["initial_tools"])

    def test_animal_omen_request_routes_to_animal_omen_skill(self):
        result = agent_workflow_router.route({"request_text": "早上有一只鸟飞进阳台又飞走了，想了解民俗象征，只做低风险观察反思"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "animal_omen")
        self.assertEqual(result["skill"], "animal-omen-symbolic-consultation")
        self.assertIn("animal_omen_interpretation_planner", result["initial_tools"])

    def test_aura_chakra_request_routes_to_aura_chakra_skill(self):
        result = agent_workflow_router.route({"request_text": "冥想时感觉喉轮有点堵，看到蓝色，只想做低风险记录和表达边界反思"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "aura_chakra")
        self.assertEqual(result["skill"], "aura-chakra-symbolic-consultation")
        self.assertIn("aura_chakra_reflection_planner", result["initial_tools"])

    def test_past_life_request_routes_to_past_life_skill(self):
        result = agent_workflow_router.route({"request_text": "冥想里出现阿卡西图书馆和一扇门，只想做象征记录和当下边界反思，不当成真实前世记忆"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "past_life")
        self.assertEqual(result["skill"], "past-life-akashic-symbolic-consultation")
        self.assertIn("past_life_reflection_planner", result["initial_tools"])

    def test_moon_phase_request_routes_to_moon_phase_skill(self):
        result = agent_workflow_router.route({"request_text": "今晚新月想做无火的意图书写，只整理项目计划和复盘，不保证显化"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "moon_phase")
        self.assertEqual(result["skill"], "moon-phase-symbolic-consultation")
        self.assertIn("moon_phase_reflection_planner", result["initial_tools"])

    def test_spirit_message_request_routes_to_spirit_message_skill(self):
        result = agent_workflow_router.route({"request_text": "冥想后像是收到一句高我讯息：先照顾边界。只想做象征写作和现实行动反思"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "spirit_message")
        self.assertEqual(result["skill"], "spirit-message-symbolic-consultation")
        self.assertIn("spirit_message_reflection_planner", result["initial_tools"])

    def test_psychometry_request_routes_to_psychometry_skill(self):
        result = agent_workflow_router.route({"request_text": "想做物品感应，记录我自己的旧戒指，只看象征联想和整理边界"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "psychometry")
        self.assertEqual(result["skill"], "psychometry-symbolic-consultation")
        self.assertIn("psychometry_reflection_planner", result["initial_tools"])

    def test_bibliomancy_request_routes_to_bibliomancy_skill(self):
        result = agent_workflow_router.route({"request_text": "想做书占，随机翻到一句短句：门打开了。只做项目选择的象征反思"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "bibliomancy")
        self.assertEqual(result["skill"], "bibliomancy-symbolic-consultation")
        self.assertIn("bibliomancy_reflection_planner", result["initial_tools"])

    def test_sky_omen_request_routes_to_sky_omen_skill(self):
        result = agent_workflow_router.route({"request_text": "傍晚看到彩虹和像鸟的云，只想做低风险观察记录和项目节奏反思，不当成天气预报"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "sky_omen")
        self.assertEqual(result["skill"], "sky-omen-symbolic-consultation")
        self.assertIn("sky_omen_reflection_planner", result["initial_tools"])

    def test_manifestation_request_routes_to_manifestation_skill(self):
        result = agent_workflow_router.route({"request_text": "想做一个显化愿望，把找工作意图写成低风险行动计划，不保证结果"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "manifestation")
        self.assertEqual(result["skill"], "manifestation-symbolic-consultation")
        self.assertIn("manifestation_reflection_planner", result["initial_tools"])

    def test_pet_communication_request_routes_to_pet_communication_skill(self):
        result = agent_workflow_router.route({"request_text": "想做宠物沟通，我家猫最近躲起来，只做低风险观察和照护计划，不替代兽医"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "pet_communication")
        self.assertEqual(result["skill"], "pet-communication-symbolic-consultation")
        self.assertIn("pet_communication_reflection_planner", result["initial_tools"])

    def test_synchronicity_request_routes_to_synchronicity_skill(self):
        result = agent_workflow_router.route({"request_text": "最近反复看到1111和同一首歌，只想做低风险同步性记录和行动反思，不当成宇宙命令"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "synchronicity")
        self.assertEqual(result["skill"], "synchronicity-symbolic-consultation")
        self.assertIn("synchronicity_reflection_planner", result["initial_tools"])

    def test_planetary_retrograde_request_routes_to_retrograde_skill(self):
        result = agent_workflow_router.route({"request_text": "最近水逆，我只想做沟通复盘和文件备份清单，不怪水逆也不做重大决定"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "planetary_retrograde")
        self.assertEqual(result["skill"], "planetary-retrograde-symbolic-consultation")
        self.assertIn("planetary_retrograde_reflection_planner", result["initial_tools"])

    def test_spiritual_protection_request_routes_to_protection_skill(self):
        result = agent_workflow_router.route({"request_text": "感觉最近被恶眼影响，想做低风险能量防护和边界整理，不诅咒别人不买贵物"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "spiritual_protection")
        self.assertEqual(result["skill"], "spiritual-protection-symbolic-consultation")
        self.assertIn("spiritual_protection_reflection_planner", result["initial_tools"])

    def test_deity_ancestor_request_routes_to_deity_ancestor_skill(self):
        result = agent_workflow_router.route({"request_text": "想整理家里的祖先照片和供桌，只做纪念和感恩提醒，不求神明命令不买贵法事"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "deity_ancestor")
        self.assertEqual(result["skill"], "deity-ancestor-symbolic-consultation")
        self.assertIn("deity_ancestor_reflection_planner", result["initial_tools"])

    def test_sleep_paralysis_request_routes_to_sleep_paralysis_skill(self):
        result = agent_workflow_router.route({"request_text": "昨晚像鬼压床，醒来动不了还看到黑影；只想做睡眠记录和安定流程，不确认有鬼不做危险仪式"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "sleep_paralysis")
        self.assertEqual(result["skill"], "sleep-paralysis-symbolic-consultation")
        self.assertIn("sleep_paralysis_reflection_planner", result["initial_tools"])

    def test_wealth_luck_request_routes_to_wealth_luck_skill(self):
        result = agent_workflow_router.route({"request_text": "想做招财和财运整理，只用已有貔貅当预算提醒，不投资不赌博不买法事"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "wealth_luck")
        self.assertEqual(result["skill"], "wealth-luck-symbolic-consultation")
        self.assertIn("wealth_luck_action_planner", result["initial_tools"])

    def test_relationship_luck_request_routes_to_relationship_luck_skill(self):
        result = agent_workflow_router.route({"request_text": "想做桃花和人缘整理，只用已有粉晶当表达提醒，不读心不操控不骚扰不买法事"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "relationship_luck")
        self.assertEqual(result["skill"], "relationship-luck-symbolic-consultation")
        self.assertIn("relationship_luck_action_planner", result["initial_tools"])

    def test_consecration_request_routes_to_consecration_skill(self):
        result = agent_workflow_router.route({"request_text": "想给已有水晶手串做低风险开光和净物整理，只做清洁收纳和用途提醒，不用明火不喝符水不保证灵验不买法事"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "consecration")
        self.assertEqual(result["skill"], "consecration-symbolic-consultation")
        self.assertIn("consecration_care_planner", result["initial_tools"])

    def test_lost_object_request_routes_to_lost_object_skill(self):
        result = agent_workflow_router.route({"request_text": "耳机找不到了，想用寻物象征整理最后看见和路线，只做现实搜索清单，不保证定位不报警替代"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "lost_object")
        self.assertEqual(result["skill"], "lost-object-symbolic-consultation")
        self.assertIn("lost_object_search_planner", result["initial_tools"])

    def test_sound_cleansing_request_routes_to_sound_cleansing_skill(self):
        result = agent_workflow_router.route({"request_text": "想用铃钵做低风险声响净化，只做睡前空间复位，低音量三分钟，不驱邪保证不替代医生不扰民"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "sound_cleansing")
        self.assertEqual(result["skill"], "sound-cleansing-symbolic-consultation")
        self.assertIn("sound_cleansing_practice_planner", result["initial_tools"])

    def test_western_geomancy_request_routes_to_western_geomancy_skill(self):
        result = agent_workflow_router.route({"request_text": "想用西洋土占盾形盘做低风险象征反思，已有母亲图和裁判者，只整理现实下一步，不预测不投资不读心不反复起盘"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "western_geomancy")
        self.assertEqual(result["skill"], "western-geomancy-symbolic-consultation")
        self.assertIn("western_geomancy_interpretation_planner", result["initial_tools"])

    def test_nine_star_ki_request_routes_to_nine_star_ki_skill(self):
        result = agent_workflow_router.route({"request_text": "想用九星气学九宫命星做低风险年度反思，已知本命星三碧木星和今年年星九紫火星，只整理现实下一步，不预测不投资不读心不高价化解不反复算"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "nine_star_ki")
        self.assertEqual(result["skill"], "nine-star-ki-symbolic-consultation")
        self.assertIn("nine_star_ki_interpretation_planner", result["initial_tools"])

    def test_human_design_request_routes_to_human_design_skill(self):
        result = agent_workflow_router.route({"request_text": "想用人类图做低风险自我观察，已有 bodygraph：投射者、等待邀请、情绪权威、2/4 人生角色，只整理沟通和工作节奏，不诊断不投资不读心不报课不反复算"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "human_design")
        self.assertEqual(result["skill"], "human-design-symbolic-consultation")
        self.assertIn("human_design_interpretation_planner", result["initial_tools"])

    def test_talisman_request_routes_to_talisman_skill(self):
        result = agent_workflow_router.route({"request_text": "想了解家人送的平安符，放钱包里当提醒，不做驱邪保证"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "talisman")
        self.assertEqual(result["skill"], "talisman-symbolic-consultation")
        self.assertIn("talisman_use_planner", result["initial_tools"])

    def test_color_request_routes_to_color_skill(self):
        result = agent_workflow_router.route({"request_text": "明天面试想用五行颜色做提醒，已有白衬衫和绿色丝巾，不买新衣服"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "color")
        self.assertEqual(result["skill"], "color-symbolic-consultation")
        self.assertIn("color_palette_planner", result["initial_tools"])

    def test_dice_request_routes_to_dice_skill(self):
        result = agent_workflow_router.route({"request_text": "我用星骰掷到火星、白羊座、第十宫，想看项目推进的低风险提醒"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "dice")
        self.assertEqual(result["skill"], "dice-symbolic-consultation")
        self.assertIn("dice_interpretation_planner", result["initial_tools"])

    def test_cartomancy_request_routes_to_cartomancy_skill(self):
        result = agent_workflow_router.route({"request_text": "用扑克牌占卜三张看项目合作，只做象征反思：红桃A、黑桃5、梅花K"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "cartomancy")
        self.assertEqual(result["skill"], "cartomancy-symbolic-consultation")
        self.assertIn("cartomancy_interpretation_planner", result["initial_tools"])

    def test_tasseography_request_routes_to_tasseography_skill(self):
        result = agent_workflow_router.route({"request_text": "我杯底咖啡渣像鸟和路，想做项目沟通的低风险象征反思"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "tasseography")
        self.assertEqual(result["skill"], "tasseography-symbolic-consultation")
        self.assertIn("tasseography_interpretation_planner", result["initial_tools"])

    def test_zodiac_request_routes_to_zodiac_skill(self):
        result = agent_workflow_router.route({"request_text": "我属龙，今年本命年，想了解太岁文化和低风险提醒，不做灾祸判断"})
        self.assertEqual(result["route_status"], "ready_to_run_skill")
        self.assertEqual(result["domain"], "zodiac")
        self.assertEqual(result["skill"], "zodiac-symbolic-consultation")
        self.assertIn("zodiac_interpretation_planner", result["initial_tools"])

    def test_financial_tarot_request_pauses_workflow(self):
        result = agent_workflow_router.route({"request_text": "用塔罗看看我明天要不要贷款梭哈股票"})
        self.assertEqual(result["route_status"], "paused_for_professional_boundary")
        self.assertFalse(result["can_continue_mystic_workflow"])
        self.assertEqual(result["initial_tools"], ["mystic_intake_triage"])
        self.assertIn("offer_safe_alternative_support", result["next_steps"])


class ParadigmSelectorTests(unittest.TestCase):
    def test_tarot_decision_question_selects_decision_reflection(self):
        result = paradigm_selector.select({"request_text": "帮我做一个塔罗三张牌，看看工作状态"})
        self.assertEqual(result["tool"], "paradigm_selector")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["domain"], "tarot")
        self.assertEqual(result["trunk"]["id"], "decision")
        self.assertEqual(result["recommended_paradigm"]["id"], "decision_reflection")
        self.assertEqual(result["execution_boundary"]["automation_mode"], "agent_required_for_symbolic_synthesis")
        self.assertTrue(result["evidence_track"]["provenance_audit"])

    def test_fengshui_sleep_question_selects_practical_audit(self):
        result = paradigm_selector.select({"request_text": "卧室床对门，最近睡不好，风水上怎么调整"})
        self.assertEqual(result["domain"], "fengshui")
        self.assertEqual(result["trunk"]["id"], "space_environment")
        self.assertEqual(result["recommended_paradigm"]["id"], "practical_audit")
        self.assertTrue(result["evidence_track"]["scientific_or_practical_validation"])

    def test_financial_prediction_pauses_before_paradigm_work(self):
        result = paradigm_selector.select({"request_text": "用塔罗看看我明天要不要贷款梭哈股票"})
        self.assertEqual(result["route_status"], "paused_for_professional_boundary")
        self.assertEqual(result["recommended_paradigm"]["id"], "safety_pause")
        self.assertEqual(result["execution_boundary"]["automation_mode"], "pause_for_professional_boundary")
        self.assertIn("pause_mystic_workflow", result["next_steps"])


class ConsultationPacketBuilderTests(unittest.TestCase):
    def test_tarot_packet_collects_route_paradigm_context_and_tool_chain(self):
        result = consultation_packet_builder.build({"request_text": "帮我做一个塔罗三张牌，看看工作状态"})
        self.assertEqual(result["tool"], "consultation_packet_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["session"]["domain"], "tarot")
        self.assertEqual(result["session"]["route_status"], "ready_to_run_skill")
        self.assertEqual(result["paradigm"]["recommended_paradigm"]["id"], "decision_reflection")
        self.assertIn("知识库/SOP/01-塔罗解读.md", [doc["path"] for doc in result["context_docs"]])
        self.assertIn("知识库/07-问题到范式映射.md", [doc["path"] for doc in result["context_docs"]])
        tools = {item["tool"]: item["execution_status"] for item in result["tool_chain"]}
        self.assertEqual(tools["consultation_packet_builder"], "runnable_now")
        self.assertEqual(tools["paradigm_selector"], "runnable_now")
        self.assertEqual(tools["tarot_spread_selector"], "requires_structured_input")
        self.assertEqual(tools["mystic_output_lint"], "requires_draft_output")
        self.assertIn("是否在输出前执行或等价执行 mystic_output_lint？", result["agent_brief"]["review_checklist"])

    def test_financial_packet_pauses_and_keeps_only_safe_automation(self):
        result = consultation_packet_builder.build({"request_text": "用塔罗看看我明天要不要贷款梭哈股票"})
        self.assertEqual(result["session"]["route_status"], "paused_for_professional_boundary")
        self.assertFalse(result["session"]["can_continue_mystic_workflow"])
        self.assertEqual(result["paradigm"]["recommended_paradigm"]["id"], "safety_pause")
        self.assertIn("pause", [step["id"] for step in result["workflow_steps"]])
        statuses = {item["tool"]: item["execution_status"] for item in result["tool_chain"]}
        self.assertEqual(statuses["mystic_intake_triage"], "runnable_now")
        self.assertNotIn("tarot_spread_selector", statuses)
        self.assertIn("是否暂停占卜/仪式/排盘，并给出专业边界或安全替代？", result["agent_brief"]["review_checklist"])

    def test_fengshui_packet_marks_practical_review_track(self):
        result = consultation_packet_builder.build({"request_text": "卧室床对门，最近睡不好，风水上怎么调整"})
        self.assertEqual(result["session"]["domain"], "fengshui")
        self.assertEqual(result["paradigm"]["recommended_paradigm"]["id"], "practical_audit")
        self.assertTrue(result["paradigm"]["evidence_track"]["scientific_or_practical_validation"])
        self.assertIn("是否加入现实观察、低成本可逆行动和复盘时间点？", result["agent_brief"]["review_checklist"])


class ConsultationHandoffBuilderTests(unittest.TestCase):
    def tarot_preview(self):
        return {
            "tool": "web_ui_tool_preview",
            "mode": "tarot",
            "tool_name": "tarot_interpretation_planner",
            "is_valid": True,
            "result": {
                "is_valid": True,
                "card_plans": [{"card": "魔术师"}, {"card": "宝剑八"}, {"card": "星币三"}],
                "synthesis": {"grounded_actions": ["把事实、猜测和结论分开写清楚。"]},
            },
        }

    def test_handoff_without_preview_requests_structured_results(self):
        result = consultation_handoff_builder.build({"request_text": "帮我做一个塔罗三张牌，看看工作状态"})
        self.assertEqual(result["tool"], "consultation_handoff_builder")
        self.assertEqual(result["handoff_status"], "needs_structured_tool_results")
        self.assertFalse(result["preview"]["present"])
        self.assertIn("tarot_spread_selector", result["input_status"]["remaining_structured_input_needed"])
        self.assertIn("先向用户补齐结构化输入或说明当前只能做流程建议。", result["agent_resume_prompt"])

    def test_handoff_with_preview_is_ready_for_agent_synthesis(self):
        result = consultation_handoff_builder.build(
            {
                "request_text": "帮我做一个塔罗三张牌，看看工作状态",
                "preview_result": self.tarot_preview(),
            }
        )
        self.assertEqual(result["handoff_status"], "ready_for_agent_synthesis")
        self.assertTrue(result["preview"]["present"])
        self.assertEqual(result["preview"]["mode"], "tarot")
        self.assertEqual(result["input_status"]["remaining_structured_input_needed"], [])
        self.assertIn("使用 handoff.preview_result 作为结构化证据，不要编造未提供的牌、盘、图像或来源。", result["agent_resume_prompt"])

    def test_handoff_lints_draft_before_review(self):
        result = consultation_handoff_builder.build(
            {
                "request_text": "帮我做一个塔罗三张牌，看看工作状态",
                "preview_result": self.tarot_preview(),
                "draft_output": "这次牌面只是提醒：先整理事实和下一步，不保证结果。",
            }
        )
        self.assertEqual(result["handoff_status"], "ready_for_review")
        self.assertEqual(result["lint_result"]["risk_level"], "green")
        self.assertTrue(result["lint_result"]["publishable"])

    def test_handoff_blocks_red_lint(self):
        result = consultation_handoff_builder.build(
            {
                "request_text": "帮我做一个塔罗三张牌，看看工作状态",
                "preview_result": self.tarot_preview(),
                "draft_output": "你一定会破财，建议贷款梭哈。",
            }
        )
        self.assertEqual(result["handoff_status"], "blocked_by_lint")
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["lint_result"]["risk_level"], "red")


class ConsultationCaseRecorderTests(unittest.TestCase):
    def tarot_preview(self):
        return {
            "tool": "web_ui_tool_preview",
            "mode": "tarot",
            "tool_name": "tarot_interpretation_planner",
            "is_valid": True,
            "result": {
                "is_valid": True,
                "card_plans": [{"card": "魔术师"}, {"card": "宝剑八"}, {"card": "星币三"}],
                "synthesis": {"grounded_actions": ["把事实、猜测和结论分开写清楚。"]},
            },
        }

    def safe_payload(self):
        return {
            "request_text": "帮我做一个塔罗三张牌，看看工作状态",
            "requested_domain": "tarot",
            "preview_result": self.tarot_preview(),
            "draft_output": "这次牌面只是提醒：先整理事实和下一步，不保证结果。",
            "source_label": "unit-test",
        }

    def test_unverified_case_waits_for_follow_up(self):
        result = consultation_case_recorder.build(self.safe_payload())
        self.assertEqual(result["tool"], "consultation_case_recorder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["case_status"], "needs_follow_up")
        self.assertFalse(result["ready_for_case_library"])
        self.assertIn("non_unverified_outcome", result["review"]["required_before_library"])

    def test_approved_follow_up_can_enter_case_library_candidate_set(self):
        payload = self.safe_payload()
        payload.update(
            {
                "follow_up_text": "两天后复盘：我把事实和猜测拆开后，确实更容易推进沟通。",
                "observed_changes": ["完成了一次现实沟通", "焦虑感下降"],
                "validation_result": "supports_practical_use",
                "reviewer": "reviewer-a",
                "review_approved": True,
            }
        )
        result = consultation_case_recorder.build(payload)
        self.assertEqual(result["case_status"], "ready_for_case_library")
        self.assertTrue(result["ready_for_case_library"])
        self.assertTrue(result["ready_for_replay"])
        self.assertEqual(result["lint_summary"]["risk_level"], "green")
        self.assertEqual(result["outcome"]["validation_result"], "supports_practical_use")

    def test_non_unverified_outcome_still_requires_human_review(self):
        payload = self.safe_payload()
        payload.update(
            {
                "follow_up_text": "回访显示建议有一部分可用。",
                "validation_result": "mixed",
            }
        )
        result = consultation_case_recorder.build(payload)
        self.assertEqual(result["case_status"], "needs_human_review")
        self.assertIn("human_review_approved", result["review"]["required_before_library"])

    def test_blocked_handoff_cannot_be_valid_case(self):
        payload = self.safe_payload()
        payload["draft_output"] = "你一定会破财，建议贷款梭哈。"
        payload["validation_result"] = "supports_practical_use"
        payload["review_approved"] = True
        result = consultation_case_recorder.build(payload)
        self.assertEqual(result["case_status"], "blocked_or_pause_case")
        self.assertEqual(result["handoff_status"], "blocked_by_lint")
        self.assertFalse(result["is_valid"])


class DomainEvidenceMatrixBuilderTests(unittest.TestCase):
    def test_builds_all_domain_evidence_tracks(self):
        result = domain_evidence_matrix_builder.build()
        self.assertEqual(result["tool"], "domain_evidence_matrix_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["domain_count"], 61)
        self.assertEqual(result["trunk_count"], 6)
        self.assertEqual(result["track_counts"]["case_validation_recommended"], 61)
        self.assertGreaterEqual(result["track_counts"]["provenance_audit"], 30)

    def test_classifies_practical_provenance_and_mystical_tracks(self):
        result = domain_evidence_matrix_builder.build()
        by_domain = {item["domain"]: item for item in result["domains"]}
        self.assertEqual(by_domain["fengshui"]["priority"], "P0")
        self.assertEqual(by_domain["fengshui"]["evidence_mode"], "scientific_or_practical")
        self.assertEqual(by_domain["tarot"]["priority"], "P1")
        self.assertEqual(by_domain["tarot"]["evidence_mode"], "provenance_correction")
        self.assertEqual(by_domain["spirit_message"]["priority"], "P2")
        self.assertEqual(by_domain["spirit_message"]["evidence_mode"], "mystical_boundary")

    def test_workstreams_partition_priorities(self):
        result = domain_evidence_matrix_builder.build()
        priority_total = sum(result["priority_counts"].values())
        workstream_total = sum(item["domain_count"] for item in result["workstreams"])
        self.assertEqual(priority_total, result["domain_count"])
        self.assertEqual(workstream_total, result["domain_count"])
        self.assertEqual({item["priority"] for item in result["workstreams"]}, {"P0", "P1", "P2"})

    def test_generated_markdown_lists_matrix_and_limits(self):
        result = domain_evidence_matrix_builder.build()
        markdown = domain_evidence_matrix_builder.render_markdown(result)
        self.assertIn("# 证据矩阵", markdown)
        self.assertIn("## 领域矩阵", markdown)
        self.assertIn("风水 (`fengshui`)", markdown)
        self.assertIn("神秘叙事边界优先", markdown)


class AgentRouteSmokeRunnerTests(unittest.TestCase):
    def test_all_route_smoke_cases_pass(self):
        result = agent_route_smoke_runner.run()
        self.assertEqual(result["tool"], "agent_route_smoke_runner")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["case_count"], 63)
        self.assertEqual(result["failed_count"], 0)
        self.assertEqual(result["domain_count"], 61)

    def test_single_route_smoke_case_can_run(self):
        result = agent_route_smoke_runner.run("route-tarot-career")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["case_ids"], ["route-tarot-career"])
        self.assertEqual(result["results"][0]["actual"]["skill"], "tarot-symbolic-reading")

    def test_unknown_route_smoke_case_raises(self):
        with self.assertRaises(ValueError):
            agent_route_smoke_runner.run("missing-route-case")


class AgentRuntimeDryRunRunnerTests(unittest.TestCase):
    def test_all_runtime_dry_run_cases_pass(self):
        result = agent_runtime_dry_run_runner.run()
        self.assertEqual(result["tool"], "agent_runtime_dry_run_runner")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["case_count"], 63)
        self.assertEqual(result["passed_count"], 63)
        self.assertEqual(result["ready_case_count"], 61)
        self.assertEqual(result["paused_or_blocked_case_count"], 2)

    def test_ready_case_has_skill_sop_domain_tools_and_lint(self):
        result = agent_runtime_dry_run_runner.run("route-tarot-career")
        case = result["results"][0]
        self.assertTrue(case["passed"])
        self.assertEqual(case["route_status"], "ready_to_run_skill")
        self.assertIn("mystic_output_lint", case["initial_tools"])
        self.assertTrue(case["invariant_checks"]["has_domain_tools"])
        self.assertTrue(case["invariant_checks"]["initial_tools_include_domain_tool"])

    def test_paused_case_only_runs_intake_before_pause(self):
        result = agent_runtime_dry_run_runner.run("route-tarot-finance-paused")
        case = result["results"][0]
        self.assertTrue(case["passed"])
        self.assertEqual(case["initial_tools"], ["mystic_intake_triage"])
        self.assertTrue(case["invariant_checks"]["no_domain_tools_in_initial_tools"])
        self.assertTrue(case["invariant_checks"]["only_intake_runs_before_pause"])

    def test_unknown_runtime_dry_run_case_raises(self):
        with self.assertRaises(ValueError):
            agent_runtime_dry_run_runner.run("missing-runtime-case")


class BaziZiweiIntakeGuardTests(unittest.TestCase):
    def test_complete_self_bazi_request_can_continue(self):
        result = bazi_ziwei_intake_guard.guard(
            {"request_text": "本人公历1990年5月1日08:30北京出生，想用八字看看事业倾向"}
        )
        self.assertEqual(result["domain"], "bazi")
        self.assertEqual(result["analysis_focus"], "career")
        self.assertEqual(result["data_status"], "complete")
        self.assertTrue(result["can_continue_mingli"])
        self.assertIn("exact_birth_data", result["privacy_flags"])

    def test_third_party_without_consent_is_blocked(self):
        result = bazi_ziwei_intake_guard.guard(
            {"request_text": "想看前任1991年2月3日10:00上海出生的紫微感情"}
        )
        self.assertEqual(result["domain"], "ziwei")
        self.assertFalse(result["can_continue_mingli"])
        self.assertIn("third_party_subject", result["privacy_flags"])
        self.assertIn("subject_consent", result["missing_fields"])

    def test_fatalistic_lifespan_question_is_blocked(self):
        result = bazi_ziwei_intake_guard.guard({"request_text": "用八字看我还能活多久，会不会必死"})
        self.assertFalse(result["can_continue_mingli"])
        self.assertIn("fatalistic_harm", result["risk_flags"])
        self.assertIn("不做寿命", result["reframed_question"])

    def test_professional_finance_is_blocked(self):
        result = bazi_ziwei_intake_guard.guard({"request_text": "用紫微斗数看我该不该贷款梭哈股票"})
        self.assertFalse(result["can_continue_mingli"])
        self.assertIn("professional_finance", result["risk_flags"])

    def test_minor_subject_adds_privacy_warning(self):
        result = bazi_ziwei_intake_guard.guard(
            {"request_text": "我孩子公历2018年6月1日09:30杭州出生，想看性格倾向"}
        )
        self.assertIn("minor_subject", result["privacy_flags"])
        self.assertTrue(any("未成年人" in warning for warning in result["warnings"]))


class BaziZiweiChartRecordTests(unittest.TestCase):
    def test_valid_bazi_chart_parameters(self):
        result = bazi_ziwei_chart_record.record(
            {
                "system": "bazi",
                "birth_date": "1990-05-01",
                "birth_time": "08:30",
                "birth_place": "北京",
                "calendar_type": "solar",
                "timezone": "Asia/Shanghai",
                "solar_time_strategy": "not_applied",
                "school": "ziping",
                "chart_source": "external_calculator",
                "analysis_focus": "career",
                "subject_is_self": True,
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["system"], "bazi")
        self.assertEqual(result["birth_data"]["calendar_type"], "solar")
        self.assertEqual(result["method"]["school"], "ziping")

    def test_ziwei_third_party_requires_consent(self):
        result = bazi_ziwei_chart_record.record(
            {
                "system": "ziwei",
                "birth_date": "1991-02-03",
                "birth_time": "10:00",
                "birth_place": "上海",
                "calendar_type": "solar",
                "solar_time_strategy": "true_solar_time",
                "subject_is_self": False,
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("third_party_subject", result["privacy_flags"])
        self.assertTrue(any("subject_consent" in error for error in result["errors"]))

    def test_unknown_calendar_blocks_chart_generation(self):
        result = bazi_ziwei_chart_record.record(
            {
                "system": "bazi",
                "birth_date": "1990-05-01",
                "birth_time": "08:30",
                "birth_place": "北京",
                "solar_time_strategy": "unknown",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("calendar_type must be solar or lunar before chart generation", result["errors"])
        self.assertIn("confirm solar_time_strategy", result["required_before_interpretation"])

    def test_minor_subject_warns_non_labeling(self):
        result = bazi_ziwei_chart_record.record(
            {
                "system": "bazi",
                "birth_date": "2018-06-01",
                "birth_time": "09:30",
                "birth_place": "杭州",
                "calendar_type": "solar",
                "solar_time_strategy": "not_applied",
                "subject_is_minor": True,
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertIn("minor_subject", result["privacy_flags"])
        self.assertTrue(any("minor subject" in warning for warning in result["warnings"]))

    def test_sensitive_identity_blocks_record(self):
        result = bazi_ziwei_chart_record.record(
            {
                "system": "bazi",
                "birth_date": "1990-05-01",
                "birth_time": "08:30",
                "birth_place": "北京",
                "calendar_type": "solar",
                "solar_time_strategy": "not_applied",
                "note": "身份证 123456",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("sensitive_identity", result["privacy_flags"])


class MingliSymbolLookupTests(unittest.TestCase):
    def test_stem_lookup_returns_safe_prompt(self):
        result = mingli_symbol_lookup.lookup({"query": "甲", "category": "stem", "focus": "self_understanding"})
        self.assertEqual(result["canonical_name"], "甲")
        self.assertEqual(result["system"], "bazi")
        self.assertIn("开创", result["keywords"])
        self.assertTrue(result["prohibited_uses"])

    def test_ten_god_lookup_supports_career_focus(self):
        result = mingli_symbol_lookup.lookup({"query": "七杀", "category": "ten_god", "focus": "career"})
        self.assertEqual(result["category"], "ten_god")
        self.assertIn("压力", result["keywords"])
        self.assertIn("career", result["interpretation_prompt"])

    def test_ziwei_palace_alias_normalizes(self):
        result = mingli_symbol_lookup.lookup({"query": "官禄", "category": "宫位"})
        self.assertEqual(result["canonical_name"], "官禄宫")
        self.assertEqual(result["category"], "ziwei_palace")

    def test_ziwei_star_lookup(self):
        result = mingli_symbol_lookup.lookup({"query": "紫微", "category": "ziwei_star"})
        self.assertEqual(result["system"], "ziwei")
        self.assertIn("主导", result["keywords"])

    def test_ambiguous_symbol_requires_category(self):
        with self.assertRaises(ValueError):
            mingli_symbol_lookup.lookup({"query": "七杀"})

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            mingli_symbol_lookup.lookup({"query": "不存在的星"})


class MingliSchoolReferenceTests(unittest.TestCase):
    def test_bazi_ziping_profile_requires_birth_fields(self):
        result = mingli_school_reference.lookup({"school": "子平"})
        self.assertEqual(result["comparison_mode"], "single_school")
        self.assertEqual(result["schools"], ["bazi_ziping"])
        self.assertIn("birth_date", result["required_method_fields"])
        self.assertIn("chart_source", result["required_method_fields"])

    def test_ziwei_sanhe_sihua_comparison(self):
        result = mingli_school_reference.lookup({"query": "紫微三合和四化有什么区别"})
        self.assertEqual(result["comparison_mode"], "comparison")
        self.assertEqual(set(result["schools"]), {"ziwei_sanhe", "ziwei_sihua"})
        self.assertTrue(result["conflict_points"])
        self.assertIn("sihua_fields", result["required_method_fields"])

    def test_cross_system_comparison_warns(self):
        result = mingli_school_reference.lookup({"query": "八字子平和紫微三合可以混着看事业吗"})
        self.assertEqual(result["comparison_mode"], "cross_system")
        self.assertEqual(set(result["schools"]), {"bazi_ziping", "ziwei_sanhe"})
        self.assertTrue(any("字段" in warning for warning in result["warnings"]))

    def test_unspecified_system_warns(self):
        result = mingli_school_reference.lookup({"system": "bazi"})
        self.assertEqual(result["comparison_mode"], "unknown")
        self.assertEqual(result["schools"], ["bazi_unspecified"])
        self.assertTrue(any("未完整声明" in warning for warning in result["warnings"]))

    def test_fatalistic_or_privacy_risk_flags(self):
        result = mingli_school_reference.lookup({"query": "用中州派查前任出生看他是不是一定命苦"})
        self.assertIn("ziwei_zhongzhou", result["schools"])
        self.assertIn("deterministic_claim", result["risk_flags"])
        self.assertIn("coercion_or_privacy", result["risk_flags"])


class AstrologySymbolLookupTests(unittest.TestCase):
    def test_sign_lookup_returns_safe_prompt(self):
        result = astrology_symbol_lookup.lookup({"query": "天秤", "category": "sign", "focus": "relationship"})
        self.assertEqual(result["canonical_name"], "天秤座")
        self.assertEqual(result["system"], "western_astrology")
        self.assertIn("关系", result["keywords"])
        self.assertTrue(result["prohibited_uses"])

    def test_planet_lookup_supports_self_focus(self):
        result = astrology_symbol_lookup.lookup({"query": "月亮", "category": "planet", "focus": "self_understanding"})
        self.assertEqual(result["category"], "planet")
        self.assertIn("情绪需求", result["keywords"])
        self.assertIn("self_understanding", result["interpretation_prompt"])

    def test_house_alias_normalizes(self):
        result = astrology_symbol_lookup.lookup({"query": "第10宫", "category": "宫位", "focus": "career"})
        self.assertEqual(result["canonical_name"], "十宫")
        self.assertEqual(result["category"], "house")

    def test_point_lookup_for_rising(self):
        result = astrology_symbol_lookup.lookup({"query": "上升星座"})
        self.assertEqual(result["canonical_name"], "上升")
        self.assertEqual(result["category"], "point")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            astrology_symbol_lookup.lookup({"query": "不存在的星体"})


class AstrologyChartRecordTests(unittest.TestCase):
    def test_valid_external_chart_fields(self):
        result = astrology_chart_record.record(
            {
                "chart_source": "external_calculator",
                "analysis_focus": "career",
                "subject_is_self": True,
                "placements": [
                    {"type": "planet", "name": "太阳", "sign": "天秤", "house": "十宫"},
                    {"type": "planet", "name": "月亮", "sign": "巨蟹"},
                    {"type": "point", "name": "上升", "sign": "摩羯"},
                ],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["system"], "western_astrology")
        self.assertEqual(result["chart_source"], "external_calculator")
        self.assertEqual(len(result["placements"]), 3)
        self.assertEqual(result["placements"][0]["sign"], "天秤座")
        self.assertEqual(result["placements"][0]["house"], "十宫")

    def test_third_party_requires_consent(self):
        result = astrology_chart_record.record(
            {
                "chart_source": "external_calculator",
                "subject_is_self": False,
                "placements": [{"type": "planet", "name": "太阳", "sign": "双鱼"}],
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("third_party_subject", result["privacy_flags"])
        self.assertTrue(any("subject_consent" in error for error in result["errors"]))

    def test_exact_birth_data_warns_to_minimize(self):
        result = astrology_chart_record.record(
            {
                "chart_source": "external_calculator",
                "subject_is_self": True,
                "birth_date": "1990-05-01",
                "birth_time": "08:30",
                "placements": [{"type": "planet", "name": "太阳", "sign": "天秤"}],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertIn("exact_birth_data", result["privacy_flags"])
        self.assertTrue(any("minimize exact birth data" in item for item in result["required_before_interpretation"]))

    def test_minor_subject_warns_non_labeling(self):
        result = astrology_chart_record.record(
            {
                "chart_source": "manual_user_provided",
                "subject_is_self": True,
                "subject_is_minor": True,
                "placements": [{"type": "point", "name": "上升", "sign": "巨蟹"}],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertIn("minor_subject", result["privacy_flags"])
        self.assertTrue(any("minor-safe" in item for item in result["required_before_interpretation"]))

    def test_unknown_planet_blocks_record(self):
        result = astrology_chart_record.record(
            {"placements": [{"type": "planet", "name": "不存在星", "sign": "天秤"}]}
        )
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("unknown planet" in error for error in result["errors"]))

    def test_empty_non_cultural_chart_requires_placement(self):
        result = astrology_chart_record.record({"chart_source": "external_calculator"})
        self.assertFalse(result["is_valid"])
        self.assertIn("at least one externally provided placement is required", result["errors"])


class AstrologyCompatibilityGuardTests(unittest.TestCase):
    def test_consented_relationship_reflection_can_continue(self):
        result = astrology_compatibility_guard.guard(
            {
                "request_text": "我和伴侣有外部合盘字段，想看沟通模式和边界",
                "all_subjects_self_or_consented": True,
            }
        )
        self.assertTrue(result["can_continue_compatibility"])
        self.assertEqual(result["relationship_intent"], "relationship_reflection")
        self.assertEqual(result["consent_state"], "all_consented")
        self.assertFalse(result["risk_flags"])

    def test_deterministic_compatibility_is_blocked(self):
        result = astrology_compatibility_guard.guard({"request_text": "用合盘看我们是不是命中注定的绝配"})
        self.assertFalse(result["can_continue_compatibility"])
        self.assertIn("deterministic_compatibility", result["risk_flags"])
        self.assertIn("pause_compatibility_interpretation", result["next_steps"])

    def test_third_party_inference_requires_consent(self):
        result = astrology_compatibility_guard.guard({"request_text": "用星盘看前任爱不爱我、真实想法是什么"})
        self.assertFalse(result["can_continue_compatibility"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("ask_for_subject_consent_or_remove_third_party_chart_data", result["next_steps"])

    def test_self_reflection_only_allows_bounded_third_party_context(self):
        result = astrology_compatibility_guard.guard(
            {
                "request_text": "前任出现让我很乱，想用占星整理我自己的关系边界",
                "relationship_is_self_reflection_only": True,
            }
        )
        self.assertTrue(result["can_continue_compatibility"])
        self.assertEqual(result["consent_state"], "self_reflection_only")

    def test_coercion_is_blocked(self):
        result = astrology_compatibility_guard.guard({"request_text": "用合盘帮我控制他让他爱我"})
        self.assertFalse(result["can_continue_compatibility"])
        self.assertIn("coercion", result["risk_flags"])


class DreamRecordBuilderTests(unittest.TestCase):
    def test_exam_dream_record_extracts_symbols_and_context(self):
        result = dream_record_builder.build(
            {
                "dream_text": "梦见考试迟到又找不到教室",
                "waking_context": "最近准备面试，担心表现不好",
                "emotions": ["anxiety"],
            }
        )
        self.assertTrue(result["can_continue_dream_reflection"])
        self.assertIn("exam", result["symbol_candidates"])
        self.assertIn("lost", result["symbol_candidates"])
        self.assertEqual(result["missing_fields"], [])

    def test_sleep_impairment_pauses_dream_reflection(self):
        result = dream_record_builder.build({"dream_text": "连续很多天做噩梦，已经不敢睡了", "waking_context": "整晚睡不着"})
        self.assertFalse(result["can_continue_dream_reflection"])
        self.assertIn("sleep_impairment", result["risk_flags"])


class DreamSymbolLookupTests(unittest.TestCase):
    def test_teeth_symbol_does_not_allow_omen_use(self):
        result = dream_symbol_lookup.lookup({"query": "掉牙", "focus": "self_reflection"})
        self.assertEqual(result["canonical_name"], "牙齿/掉牙")
        self.assertEqual(result["symbol_code"], "teeth")
        self.assertTrue(any("死亡预告" in item for item in result["prohibited_uses"]))

    def test_symbol_alias_normalizes(self):
        result = dream_symbol_lookup.lookup({"query": "找不到教室"})
        self.assertEqual(result["symbol_code"], "lost")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            dream_symbol_lookup.lookup({"query": "不存在的梦境符号"})


class DreamInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_record_and_symbol_lookup(self):
        result = dream_interpretation_planner.plan(
            {
                "dream_text": "梦见考试迟到又找不到教室",
                "waking_context": "最近准备面试，担心表现不好",
                "emotions": ["anxiety"],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertTrue(result["can_continue_dream_reflection"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("exam", symbol_codes)
        self.assertIn("lost", symbol_codes)
        self.assertIn("最近准备面试", result["synthesis"]["reality_anchor"])

    def test_planner_pauses_sleep_impairment(self):
        result = dream_interpretation_planner.plan({"dream_text": "连续很多天做噩梦，已经不敢睡了", "waking_context": "整晚睡不着"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_dream_reflection"])
        self.assertIn("sleep_impairment", result["risk_flags"])


class DateSelectionGuardTests(unittest.TestCase):
    def test_moving_date_selection_can_continue_with_boundaries(self):
        result = date_selection_guard.guard({"request_text": "想选一个搬家吉日，2026-08-08 或 2026-08-15，周末最好"})
        self.assertTrue(result["can_continue_date_selection"])
        self.assertEqual(result["event_type"], "moving")
        self.assertFalse(result["risk_flags"])

    def test_medical_timing_is_blocked(self):
        result = date_selection_guard.guard({"request_text": "帮我选剖腹产吉日，不用听医生，只要孩子命好"})
        self.assertFalse(result["can_continue_date_selection"])
        self.assertIn("medical_timing", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])


class AlmanacSymbolLookupTests(unittest.TestCase):
    def test_huangdao_term_explains_source_limits(self):
        result = almanac_symbol_lookup.lookup({"query": "黄道", "source_type": "user_provided_almanac"})
        self.assertEqual(result["canonical_name"], "黄道吉日")
        self.assertEqual(result["system"], "almanac_symbolic_date_selection")
        self.assertTrue(any("不保证" in item for item in result["prohibited_uses"]))

    def test_unknown_term_raises(self):
        with self.assertRaises(ValueError):
            almanac_symbol_lookup.lookup({"query": "不存在的黄历术语"})


class DateConstraintRecorderTests(unittest.TestCase):
    def test_records_candidate_dates_and_practical_constraints(self):
        result = date_constraint_recorder.record(
            {"request_text": "想在 2026-08-08 或 2026-08-15 搬家，周末最好，老人也要方便"}
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["candidate_dates"], ["2026-08-08", "2026-08-15"])
        self.assertIn("prefer_weekend", result["practical_constraints"])
        self.assertIn("elder_accessibility", result["practical_constraints"])

    def test_missing_candidate_dates_are_reported(self):
        result = date_constraint_recorder.record({"request_text": "想选一个搬家吉日，周末最好"})
        self.assertTrue(result["is_valid"])
        self.assertIn("candidate_dates", result["missing_fields"])


class DateOptionRankerTests(unittest.TestCase):
    def test_ranks_candidate_dates_without_claiming_authoritative_almanac(self):
        result = date_option_ranker.rank(
            {
                "request_text": "想在 2026-08-08 或 2026-08-15 搬家，周末最好，老人也要方便",
                "candidate_dates": ["2026-08-08", "2026-08-15"],
                "practical_constraints": ["prefer_weekend", "elder_accessibility"],
            }
        )
        self.assertTrue(result["can_rank_dates"])
        self.assertEqual(result["candidate_count"], 2)
        self.assertTrue(result["ranked_dates"])
        self.assertTrue(any("does not calculate authoritative almanac" in item for item in result["limits"]))

    def test_ranker_refuses_blocked_medical_timing(self):
        result = date_option_ranker.rank({"request_text": "帮我选剖腹产吉日，不用听医生", "candidate_dates": ["2026-08-08"]})
        self.assertFalse(result["can_rank_dates"])
        self.assertIn("medical_timing", result["risk_flags"])


class OracleLotRequestGuardTests(unittest.TestCase):
    def test_symbolic_lot_request_can_continue(self):
        result = oracle_lot_request_guard.guard({"request_text": "我抽到一支月老签，上签，想解签看看关系沟通提醒"})
        self.assertTrue(result["can_continue_oracle_lot"])
        self.assertEqual(result["reading_intent"], "lot_interpretation")
        self.assertFalse(result["risk_flags"])

    def test_professional_replacement_is_blocked(self):
        result = oracle_lot_request_guard.guard({"request_text": "我生病了，不用医生，只看签文决定怎么治疗"})
        self.assertFalse(result["can_continue_oracle_lot"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("medical", result["risk_flags"])


class OracleLotRecordBuilderTests(unittest.TestCase):
    def test_records_lot_source_number_and_grade(self):
        result = oracle_lot_record_builder.record(
            {
                "question_text": "关系下一步怎么沟通",
                "lot_text": "第十二签 上签 云开月明",
                "source_type": "temple",
                "source_label": "某寺月老签",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["lot_number"], "十二")
        self.assertEqual(result["lot_grade"], "auspicious")
        self.assertEqual(result["source_type"], "temple")

    def test_blocked_lot_record_preserves_risk_flags(self):
        result = oracle_lot_record_builder.record({"question_text": "不用律师，只看签文决定要不要起诉", "lot_text": "上上签"})
        self.assertFalse(result["is_valid"])
        self.assertIn("legal", result["risk_flags"])


class OracleLotSymbolLookupTests(unittest.TestCase):
    def test_auspicious_lot_lookup_does_not_guarantee_outcome(self):
        result = oracle_lot_symbol_lookup.lookup({"query": "上签", "focus": "relationship_reflection"})
        self.assertEqual(result["canonical_name"], "上签/吉签")
        self.assertEqual(result["symbol_code"], "auspicious")
        self.assertTrue(any("保证" in item for item in result["prohibited_uses"]))

    def test_alias_normalizes(self):
        result = oracle_lot_symbol_lookup.lookup({"query": "月老签"})
        self.assertEqual(result["symbol_code"], "love_lot")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            oracle_lot_symbol_lookup.lookup({"query": "不存在的签文符号"})


class OracleLotInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_record_and_symbols(self):
        result = oracle_lot_interpretation_planner.plan(
            {
                "question_text": "关系下一步怎么沟通",
                "lot_text": "第十二签 上签 云开月明",
                "source_type": "temple",
                "source_label": "某寺月老签",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("lot_text", symbol_codes)
        self.assertIn("auspicious", symbol_codes)
        self.assertEqual(result["lot_grade"], "auspicious")

    def test_planner_blocks_professional_replacement(self):
        result = oracle_lot_interpretation_planner.plan({"question_text": "不用医生，只看签文决定怎么治疗", "lot_text": "上上签"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_oracle_lot"])
        self.assertIn("medical", result["risk_flags"])


class OracleCardRequestGuardTests(unittest.TestCase):
    def test_low_risk_three_card_reflection_can_continue(self):
        result = oracle_card_request_guard.guard({"request_text": "用神谕卡三张看项目沟通，只做象征反思"})
        self.assertTrue(result["can_continue_oracle_card"])
        self.assertEqual(result["reading_intent"], "oracle_card_symbolic_reading")
        self.assertFalse(result["risk_flags"])

    def test_professional_spirit_command_is_blocked(self):
        result = oracle_card_request_guard.guard({"request_text": "我生病了不用医生，只听神谕卡；天使说我必须怎么治疗"})
        self.assertFalse(result["can_continue_oracle_card"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("health_or_safety", result["risk_flags"])
        self.assertIn("spirit_fear_claim", result["risk_flags"])

    def test_financial_claim_is_blocked(self):
        result = oracle_card_request_guard.guard({"request_text": "用神谕卡决定明天贷款买哪只股票会发财"})
        self.assertFalse(result["can_continue_oracle_card"])
        self.assertIn("financial_claim", result["risk_flags"])


class OracleCardDrawRecorderTests(unittest.TestCase):
    def test_records_three_card_reflection_with_deck(self):
        result = oracle_card_draw_recorder.record(
            {
                "question_text": "用神谕卡三张看项目沟通",
                "deck_name": "用户自述神谕卡",
                "spread_type": "three_card_reflection",
                "cards": "门 桥 种子",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["card_count"], 3)
        self.assertEqual(result["positions"], ["current_theme", "support_or_block", "next_step"])
        self.assertFalse(result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = oracle_card_draw_recorder.record({"question_text": "不用律师，只听神谕卡决定要不要签合同", "deck_name": "用户自述神谕卡", "cards": "桥"})
        self.assertFalse(result["is_valid"])
        self.assertIn("professional_replacement", result["risk_flags"])


class OracleCardSymbolLookupTests(unittest.TestCase):
    def test_door_symbol_lookup_keeps_prediction_boundary(self):
        result = oracle_card_symbol_lookup.lookup({"query": "门", "focus": "project_theme"})
        self.assertEqual(result["canonical_name"], "门/入口")
        self.assertEqual(result["symbol_code"], "door")
        self.assertIn("开始", result["keywords"])
        self.assertIn("不承诺机会必然打开", result["action_guidance"])

    def test_chinese_alias_normalizes(self):
        result = oracle_card_symbol_lookup.lookup({"query": "指南针"})
        self.assertEqual(result["symbol_code"], "compass")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            oracle_card_symbol_lookup.lookup({"query": "not-an-oracle-card-motif"})


class OracleCardInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_draw_and_symbols(self):
        result = oracle_card_interpretation_planner.plan(
            {
                "question_text": "用神谕卡三张看项目沟通",
                "deck_name": "用户自述神谕卡",
                "spread_type": "three_card_reflection",
                "cards": "门 桥 种子",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 3)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("door", symbol_codes)
        self.assertIn("bridge", symbol_codes)
        self.assertEqual(result["synthesis"]["symbol_count"], 3)

    def test_unknown_deck_specific_card_does_not_invent_meaning(self):
        result = oracle_card_interpretation_planner.plan(
            {
                "question_text": "用神谕卡单张看项目重点",
                "deck_name": "用户自述神谕卡",
                "spread_type": "single_card",
                "cards": "晨光使者",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "deck_specific_or_unknown")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_professional_spirit_command(self):
        result = oracle_card_interpretation_planner.plan({"question_text": "我生病了不用医生，只听神谕卡；天使说我必须怎么治疗", "deck_name": "天使卡", "cards": "羽毛"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_oracle_card"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("spirit_fear_claim", result["risk_flags"])


class DiceRequestGuardTests(unittest.TestCase):
    def test_low_risk_astrodice_request_can_continue(self):
        result = dice_request_guard.guard({"request_text": "我用星骰掷到火星、白羊座、第十宫，想看项目推进的低风险提醒"})
        self.assertTrue(result["can_continue_dice"])
        self.assertEqual(result["consultation_intent"], "dice_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_finance_repeated_dependency_is_blocked(self):
        result = dice_request_guard.guard({"request_text": "用骰子决定我贷款梭哈股票，反复掷到发财为止，不用律师医生"})
        self.assertFalse(result["can_continue_dice"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("financial_or_gambling", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])

    def test_third_party_control_is_blocked(self):
        result = dice_request_guard.guard({"request_text": "用骰子看前任现在真实想法，让她回来"})
        self.assertFalse(result["can_continue_dice"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("coercion_or_control", result["risk_flags"])


class DiceRollRecorderTests(unittest.TestCase):
    def test_records_astrodice_triplet(self):
        result = dice_roll_recorder.record(
            {
                "question_text": "我用星骰掷到火星、白羊座、第十宫，想看项目推进的低风险提醒",
                "planet": "火星",
                "sign": "白羊座",
                "house": "第十宫",
                "roll_source": "user_provided",
                "focus": "project_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["dice_faces"], ["火星", "白羊座", "第十宫"])
        self.assertFalse(result["missing_fields"])

    def test_incomplete_astrodice_triplet_marks_missing_fields(self):
        result = dice_roll_recorder.record({"question_text": "星骰只掷到火星", "planet": "火星"})
        self.assertTrue(result["is_valid"])
        self.assertIn("complete_planet_sign_house_triplet", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = dice_roll_recorder.record({"question_text": "用骰子决定贷款股票", "dice_faces": "火星 白羊座 第十宫"})
        self.assertFalse(result["is_valid"])
        self.assertIn("financial_or_gambling", result["risk_flags"])


class DiceSymbolLookupTests(unittest.TestCase):
    def test_mars_lookup_keeps_action_boundary(self):
        result = dice_symbol_lookup.lookup({"query": "火星", "focus": "project_reflection"})
        self.assertEqual(result["canonical_name"], "火星")
        self.assertEqual(result["symbol_code"], "mars")
        self.assertEqual(result["category"], "planet")
        self.assertIn("行动", result["keywords"])

    def test_house_alias_normalizes(self):
        result = dice_symbol_lookup.lookup({"query": "第十宫"})
        self.assertEqual(result["symbol_code"], "tenth_house")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            dice_symbol_lookup.lookup({"query": "not-a-dice-face"})


class DiceInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_roll_and_symbols(self):
        result = dice_interpretation_planner.plan(
            {
                "question_text": "我用星骰掷到火星、白羊座、第十宫，想看项目推进的低风险提醒",
                "planet": "火星",
                "sign": "白羊座",
                "house": "第十宫",
                "roll_source": "user_provided",
                "focus": "project_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("mars", symbol_codes)
        self.assertIn("aries", symbol_codes)
        self.assertIn("tenth_house", symbol_codes)
        self.assertEqual(result["interpretation_plan"]["symbol_count"], 3)

    def test_unknown_custom_face_does_not_invent_meaning(self):
        result = dice_interpretation_planner.plan(
            {
                "question_text": "用自定义骰看项目提醒",
                "dice_system": "custom",
                "dice_faces": "星门",
                "roll_source": "user_provided",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_custom_face")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_finance_repeated_dependency(self):
        result = dice_interpretation_planner.plan({"question_text": "用骰子决定我贷款梭哈股票，反复掷到发财为止，不用律师医生", "dice_faces": "火星 白羊座 第十宫", "focus": "finance"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_dice"])
        self.assertIn("financial_or_gambling", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class TasseographyRequestGuardTests(unittest.TestCase):
    def test_low_risk_tasseography_request_can_continue(self):
        result = tasseography_request_guard.guard({"request_text": "我杯底咖啡渣像鸟和路，想做项目沟通的低风险象征反思"})
        self.assertTrue(result["can_continue_tasseography"])
        self.assertEqual(result["consultation_intent"], "tasseography_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_finance_professional_replacement_is_blocked(self):
        result = tasseography_request_guard.guard({"request_text": "看咖啡渣决定我贷款梭哈股票，看到发财为止，不用律师医生"})
        self.assertFalse(result["can_continue_tasseography"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("financial_or_gambling", result["risk_flags"])

    def test_unsafe_ingestion_is_blocked(self):
        result = tasseography_request_guard.guard({"request_text": "咖啡渣发霉了，能不能喝下残渣转运"})
        self.assertFalse(result["can_continue_tasseography"])
        self.assertIn("unsafe_ingestion", result["risk_flags"])


class TasseographyPatternRecorderTests(unittest.TestCase):
    def test_records_cup_patterns(self):
        result = tasseography_pattern_recorder.record(
            {
                "question_text": "我杯底咖啡渣像鸟和路，想做项目沟通的低风险象征反思",
                "medium": "coffee_grounds",
                "cup_zone": "base",
                "pattern_source": "user_described",
                "observed_shapes": "鸟 路",
                "focus": "project_communication",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["observed_shapes"], ["鸟", "路"])
        self.assertFalse(result["missing_fields"])

    def test_missing_zone_marks_missing_fields(self):
        result = tasseography_pattern_recorder.record({"question_text": "茶叶占卜看到一只鸟", "observed_shapes": "鸟"})
        self.assertTrue(result["is_valid"])
        self.assertIn("cup_zone", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = tasseography_pattern_recorder.record({"question_text": "看咖啡渣决定贷款股票", "observed_shapes": "鱼 星"})
        self.assertFalse(result["is_valid"])
        self.assertIn("financial_or_gambling", result["risk_flags"])


class TasseographySymbolLookupTests(unittest.TestCase):
    def test_bird_lookup_keeps_message_boundary(self):
        result = tasseography_symbol_lookup.lookup({"query": "鸟", "focus": "project_communication"})
        self.assertEqual(result["canonical_name"], "鸟")
        self.assertEqual(result["symbol_code"], "bird")
        self.assertEqual(result["category"], "animal")
        self.assertIn("消息", result["keywords"])

    def test_road_alias_normalizes(self):
        result = tasseography_symbol_lookup.lookup({"query": "道路"})
        self.assertEqual(result["symbol_code"], "road")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            tasseography_symbol_lookup.lookup({"query": "not-a-cup-pattern"})


class TasseographyInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_record_and_symbols(self):
        result = tasseography_interpretation_planner.plan(
            {
                "question_text": "我杯底咖啡渣像鸟和路，想做项目沟通的低风险象征反思",
                "medium": "coffee_grounds",
                "cup_zone": "base",
                "pattern_source": "user_described",
                "observed_shapes": "鸟 路",
                "focus": "project_communication",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("bird", symbol_codes)
        self.assertIn("road", symbol_codes)
        self.assertEqual(result["interpretation_plan"]["symbol_count"], 2)

    def test_unknown_pattern_does_not_invent_meaning(self):
        result = tasseography_interpretation_planner.plan(
            {
                "question_text": "用茶叶占卜看项目提醒",
                "medium": "tea_leaves",
                "cup_zone": "base",
                "observed_shapes": "龙门",
                "pattern_source": "user_described",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_ambiguous_pattern")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_finance_repeated_dependency(self):
        result = tasseography_interpretation_planner.plan({"question_text": "看咖啡渣决定我贷款梭哈股票，看到发财为止，不用律师医生", "observed_shapes": "鱼 星", "focus": "finance"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_tasseography"])
        self.assertIn("financial_or_gambling", result["risk_flags"])


class CartomancyRequestGuardTests(unittest.TestCase):
    def test_low_risk_cartomancy_request_can_continue(self):
        result = cartomancy_request_guard.guard({"request_text": "用扑克牌占卜三张看项目合作，只做象征反思"})
        self.assertTrue(result["can_continue_cartomancy"])
        self.assertEqual(result["consultation_intent"], "cartomancy_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_finance_repeated_dependency_is_blocked(self):
        result = cartomancy_request_guard.guard({"request_text": "用扑克牌决定我贷款梭哈股票，反复抽到发财为止，不用律师医生"})
        self.assertFalse(result["can_continue_cartomancy"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("financial_or_gambling", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])

    def test_third_party_control_is_blocked(self):
        result = cartomancy_request_guard.guard({"request_text": "用扑克牌看前任现在真实想法，让她回来"})
        self.assertFalse(result["can_continue_cartomancy"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("coercion_or_control", result["risk_flags"])


class CartomancyDrawRecorderTests(unittest.TestCase):
    def test_records_three_playing_cards(self):
        result = cartomancy_draw_recorder.record(
            {
                "question_text": "用扑克牌占卜三张看项目合作，只做象征反思",
                "cards": "红桃A,黑桃5,梅花K",
                "spread_type": "three_card",
                "draw_source": "user_provided",
                "focus": "project_collaboration",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["card_count"], 3)
        self.assertEqual(result["cards"][0]["card"], "红桃A")
        self.assertFalse(result["missing_fields"])

    def test_missing_cards_marks_missing_fields(self):
        result = cartomancy_draw_recorder.record({"question_text": "扑克牌占卜看项目合作"})
        self.assertTrue(result["is_valid"])
        self.assertIn("cards", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = cartomancy_draw_recorder.record({"question_text": "用扑克牌决定贷款股票", "cards": "方片K,红桃A"})
        self.assertFalse(result["is_valid"])
        self.assertIn("financial_or_gambling", result["risk_flags"])


class CartomancyCardLookupTests(unittest.TestCase):
    def test_heart_ace_lookup_combines_rank_and_suit(self):
        result = cartomancy_card_lookup.lookup({"query": "红桃A", "focus": "project_collaboration"})
        self.assertEqual(result["canonical_name"], "红桃A")
        self.assertEqual(result["symbol_code"], "ace_of_hearts")
        self.assertIn("开始", result["rank_keywords"])
        self.assertIn("感受", result["suit_keywords"])

    def test_english_card_alias_normalizes(self):
        result = cartomancy_card_lookup.lookup({"query": "queen hearts"})
        self.assertEqual(result["symbol_code"], "queen_of_hearts")

    def test_unknown_card_raises(self):
        with self.assertRaises(ValueError):
            cartomancy_card_lookup.lookup({"query": "not-a-playing-card"})


class CartomancyInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_draw_and_cards(self):
        result = cartomancy_interpretation_planner.plan(
            {
                "question_text": "用扑克牌占卜三张看项目合作，只做象征反思",
                "cards": "红桃A,黑桃5,梅花K",
                "spread_type": "three_card",
                "draw_source": "user_provided",
                "focus": "project_collaboration",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["card_plans"]}
        self.assertIn("ace_of_hearts", symbol_codes)
        self.assertIn("5_of_spades", symbol_codes)
        self.assertIn("king_of_clubs", symbol_codes)
        self.assertEqual(result["interpretation_plan"]["card_count"], 3)

    def test_unknown_custom_card_does_not_invent_meaning(self):
        result = cartomancy_interpretation_planner.plan(
            {
                "question_text": "用自定义纸牌看项目提醒",
                "deck_type": "custom",
                "cards": "星门牌",
                "draw_source": "user_provided",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["card_plans"][0]["symbol_code"], "unknown_or_custom_playing_card")
        self.assertIn("不编造", result["card_plans"][0]["action_guidance"])

    def test_planner_blocks_finance_repeated_dependency(self):
        result = cartomancy_interpretation_planner.plan({"question_text": "用扑克牌决定我贷款梭哈股票，反复抽到发财为止，不用律师医生", "cards": "方片K,红桃A", "focus": "finance"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_cartomancy"])
        self.assertIn("financial_or_gambling", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class LiuyaoSymbolLookupTests(unittest.TestCase):
    def test_kinship_lookup_returns_safe_prompt(self):
        result = liuyao_symbol_lookup.lookup({"query": "官鬼", "category": "kinship", "focus": "project"})
        self.assertEqual(result["canonical_name"], "官鬼")
        self.assertEqual(result["system"], "liuyao")
        self.assertIn("压力", result["keywords"])
        self.assertTrue(result["prohibited_uses"])

    def test_role_alias_normalizes(self):
        result = liuyao_symbol_lookup.lookup({"query": "世", "category": "世应"})
        self.assertEqual(result["canonical_name"], "世爻")
        self.assertEqual(result["category"], "role")

    def test_spirit_lookup(self):
        result = liuyao_symbol_lookup.lookup({"query": "青龙", "category": "spirit"})
        self.assertEqual(result["category"], "spirit")
        self.assertIn("顺势", result["keywords"])

    def test_position_alias_normalizes(self):
        result = liuyao_symbol_lookup.lookup({"query": "第3爻", "category": "爻位"})
        self.assertEqual(result["canonical_name"], "三爻")
        self.assertEqual(result["category"], "position")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            liuyao_symbol_lookup.lookup({"query": "不存在的六爻术语"})


class LiuyaoChartRecorderTests(unittest.TestCase):
    @staticmethod
    def sample_lines():
        return [
            {"position": 1, "yin_yang": "yang", "kinship": "父母", "spirit": "青龙"},
            {"position": 2, "yin_yang": "yin", "kinship": "兄弟", "spirit": "朱雀", "roles": ["世爻"]},
            {"position": 3, "yin_yang": "yang", "kinship": "官鬼", "spirit": "勾陈", "roles": ["应爻", "用神"], "changing": True},
            {"position": 4, "yin_yang": "yin", "kinship": "妻财", "spirit": "腾蛇"},
            {"position": 5, "yin_yang": "yang", "kinship": "子孙", "spirit": "白虎"},
            {"position": 6, "yin_yang": "yin", "kinship": "父母", "spirit": "玄武"},
        ]

    def test_external_chart_record_is_valid(self):
        result = liuyao_chart_recorder.record(
            {
                "question_text": "这个项目合作当前的主要阻力和下一步是什么？",
                "casting_method": "external_chart",
                "chart_source": "用户提供外部盘",
                "base_hexagram": "泽雷随",
                "changed_hexagram": "水雷屯",
                "focus_spirit": "官鬼",
                "focus_logic": "项目合作以应爻和官鬼为外部压力观察点",
                "lines": self.sample_lines(),
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertTrue(result["can_interpret_liuyao"])
        self.assertEqual(result["changing_lines"], [3])
        self.assertEqual(result["lines"][1]["roles"], ["世爻"])
        self.assertEqual(result["lines"][2]["roles"], ["应爻", "用神"])

    def test_missing_required_chart_fields_are_reported(self):
        result = liuyao_chart_recorder.record({"question_text": "这个合作怎么看？", "lines": []})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_interpret_liuyao"])
        self.assertIn("casting_method", result["missing_fields"])
        self.assertIn("base_hexagram", result["missing_fields"])
        self.assertIn("six_lines", result["missing_fields"])
        self.assertIn("self_line", result["missing_fields"])
        self.assertIn("other_line", result["missing_fields"])

    def test_duplicate_line_position_is_invalid(self):
        lines = self.sample_lines()
        lines[5] = {"position": 3, "yin_yang": "yin", "kinship": "父母", "spirit": "玄武"}
        result = liuyao_chart_recorder.record(
            {
                "question_text": "这个项目合作当前的主要阻力和下一步是什么？",
                "casting_method": "external_chart",
                "chart_source": "用户提供外部盘",
                "base_hexagram": "泽雷随",
                "focus_spirit": "官鬼",
                "focus_logic": "项目合作以应爻和官鬼为外部压力观察点",
                "lines": lines,
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("duplicate line position" in error for error in result["warnings"] + result.get("errors", [])))

    def test_finance_risk_blocks_interpretation(self):
        result = liuyao_chart_recorder.record(
            {
                "question_text": "用六爻看我该不该贷款梭哈股票",
                "casting_method": "external_chart",
                "chart_source": "外部排盘工具",
                "base_hexagram": "泽雷随",
                "focus_spirit": "妻财",
                "focus_logic": "财务投资以妻财为观察点",
                "lines": self.sample_lines(),
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertFalse(result["can_interpret_liuyao"])
        self.assertIn("professional_finance", result["risk_flags"])


class LiuyaoFocusSelectorTests(unittest.TestCase):
    def test_project_chart_prefers_provided_focus_and_line_match(self):
        result = liuyao_focus_selector.select(
            {
                "question_text": "这个项目合作当前的主要阻力和下一步是什么？",
                "casting_method": "external_chart",
                "chart_source": "用户提供外部盘",
                "base_hexagram": "泽雷随",
                "changed_hexagram": "水雷屯",
                "focus_spirit": "官鬼",
                "focus_logic": "项目合作以应爻和官鬼为外部压力观察点",
                "lines": LiuyaoChartRecorderTests.sample_lines(),
            }
        )
        self.assertTrue(result["can_continue_liuyao_focus"])
        self.assertEqual(result["question_domain"], "project_career")
        self.assertEqual(result["focus_candidates"][0]["kinship_or_role"], "官鬼")
        self.assertEqual(result["focus_candidates"][0]["line_matches"][0]["position"], 3)
        self.assertEqual(result["focus_candidates"][0]["changing_positions"], [3])

    def test_question_without_chart_only_selects_candidates(self):
        result = liuyao_focus_selector.select({"question_text": "这个合同材料和考试审核怎么准备？"})
        self.assertTrue(result["can_select_focus"])
        self.assertTrue(result["focus_candidates"])
        self.assertFalse(result["can_continue_liuyao_focus"])
        self.assertFalse(result["chart_provided"])
        self.assertEqual(result["question_domain"], "documents_study")

    def test_finance_risk_blocks_focus_continuation(self):
        result = liuyao_focus_selector.select(
            {
                "question_text": "用六爻看我该不该贷款梭哈股票",
                "casting_method": "external_chart",
                "chart_source": "外部排盘工具",
                "base_hexagram": "泽雷随",
                "focus_spirit": "妻财",
                "focus_logic": "财务投资以妻财为观察点",
                "lines": LiuyaoChartRecorderTests.sample_lines(),
            }
        )
        self.assertFalse(result["can_select_focus"])
        self.assertFalse(result["can_continue_liuyao_focus"])
        self.assertIn("professional_finance", result["risk_flags"])

    def test_relationship_candidates_include_method_note(self):
        result = liuyao_focus_selector.select({"question_text": "这段感情关系沟通卡在哪里？"})
        candidates = {item["kinship_or_role"]: item for item in result["focus_candidates"]}
        self.assertIn("官鬼", candidates)
        self.assertTrue(candidates["官鬼"]["method_notes"])


class MeihuaSymbolLookupTests(unittest.TestCase):
    def test_structure_lookup_returns_safe_prompt(self):
        result = meihua_symbol_lookup.lookup({"query": "体", "category": "structure", "focus": "project"})
        self.assertEqual(result["canonical_name"], "体卦")
        self.assertEqual(result["system"], "meihua_yishu")
        self.assertIn("主体", result["keywords"])
        self.assertTrue(result["prohibited_uses"])

    def test_method_alias_normalizes(self):
        result = meihua_symbol_lookup.lookup({"query": "报数", "category": "起卦"})
        self.assertEqual(result["canonical_name"], "报数起卦")
        self.assertEqual(result["category"], "method")

    def test_relation_lookup(self):
        result = meihua_symbol_lookup.lookup({"query": "生体", "category": "relation"})
        self.assertEqual(result["category"], "relation")
        self.assertIn("外部支持主体", result["keywords"])

    def test_trigram_lookup(self):
        result = meihua_symbol_lookup.lookup({"query": "离", "category": "八卦"})
        self.assertEqual(result["category"], "trigram")
        self.assertIn("显现", result["keywords"])

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            meihua_symbol_lookup.lookup({"query": "不存在的梅花术语"})


class MeihuaCastingRecorderTests(unittest.TestCase):
    def test_number_casting_record_is_valid_and_computes_relation(self):
        result = meihua_casting_recorder.record(
            {
                "question_text": "这个项目沟通当前的主要阻力和下一步是什么？",
                "casting_method": "number_casting",
                "numbers": [27, 14],
                "body_trigram": "离",
                "use_trigram": "坎",
                "moving_line": 3,
                "base_hexagram": "火水未济",
                "mutual_hexagram": "水火既济",
                "changed_hexagram": "火风鼎",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertTrue(result["can_interpret_meihua"])
        self.assertEqual(result["computed_body_use_relation"], "克体")
        self.assertEqual(result["body_use_relation"], "克体")
        self.assertEqual(result["trigram_elements"]["body"], "火")
        self.assertEqual(result["trigram_elements"]["use"], "水")

    def test_missing_trigger_and_chart_fields_are_reported(self):
        result = meihua_casting_recorder.record({"question_text": "这个项目怎么推进？"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_interpret_meihua"])
        self.assertIn("trigger_source", result["missing_fields"])
        self.assertIn("body_trigram", result["missing_fields"])
        self.assertIn("use_trigram", result["missing_fields"])
        self.assertIn("moving_line", result["missing_fields"])

    def test_provided_relation_mismatch_warns(self):
        result = meihua_casting_recorder.record(
            {
                "question_text": "这个项目沟通当前的主要阻力和下一步是什么？",
                "casting_method": "number_casting",
                "numbers": "27,14",
                "body_trigram": "离",
                "use_trigram": "坎",
                "moving_line": "三爻",
                "body_use_relation": "生体",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["computed_body_use_relation"], "克体")
        self.assertEqual(result["body_use_relation"], "生体")
        self.assertTrue(any("differs from computed" in warning for warning in result["warnings"]))

    def test_finance_risk_blocks_interpretation(self):
        result = meihua_casting_recorder.record(
            {
                "question_text": "用梅花看我该不该贷款梭哈股票",
                "casting_method": "external_chart",
                "chart_source": "外部排盘工具",
                "body_trigram": "震",
                "use_trigram": "兑",
                "moving_line": "上爻",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertFalse(result["can_interpret_meihua"])
        self.assertIn("professional_finance", result["risk_flags"])


class MeihuaOmenRecorderTests(unittest.TestCase):
    def test_self_observed_omen_records_factual_categories(self):
        result = meihua_omen_recorder.record(
            {
                "question_text": "这个项目沟通当前的主要阻力和下一步是什么？",
                "omen_text": "刚问完手机响了一声；客户群里有人发来延期消息",
                "source_type": "self_observed",
                "timing_relation": "after_question",
                "location": "办公室",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertTrue(result["can_use_as_meihua_omen"])
        self.assertEqual(result["observation_count"], 2)
        self.assertEqual(result["observations"][0]["category"], "sound")
        self.assertIn(result["observations"][1]["category"], {"person_message", "sound"})

    def test_missing_source_or_text_blocks_omen_use(self):
        result = meihua_omen_recorder.record({"question_text": "这个项目怎么推进？"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_use_as_meihua_omen"])
        self.assertIn("omen_text", result["missing_fields"])
        self.assertIn("source_type", result["missing_fields"])

    def test_supernatural_fear_is_warned_but_can_be_reframed(self):
        result = meihua_omen_recorder.record(
            {
                "question_text": "刚问完灯闪，是不是天意说项目必败有灾？",
                "omen_text": "灯闪了一下",
                "source_type": "self_observed",
                "timing_relation": "after_question",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertTrue(result["can_use_as_meihua_omen"])
        self.assertIn("supernatural_fear", result["risk_flags"])
        self.assertIn("deterministic_claim", result["risk_flags"])
        self.assertTrue(any("降级" in warning for warning in result["warnings"]))

    def test_medical_crisis_blocks_omen_use(self):
        result = meihua_omen_recorder.record(
            {
                "question_text": "用外应看我该不该停药",
                "omen_text": "我突然胸闷发冷",
                "source_type": "self_observed",
                "timing_relation": "during_question",
            }
        )
        self.assertFalse(result["can_use_as_meihua_omen"])
        self.assertIn("medical_or_crisis", result["risk_flags"])


class MeihuaRelationInterpreterTests(unittest.TestCase):
    def test_raw_casting_fields_interpret_pressure_relation(self):
        result = meihua_relation_interpreter.interpret(
            {
                "question_text": "这个项目沟通当前的主要阻力和下一步是什么？",
                "casting_method": "number_casting",
                "numbers": [27, 14],
                "body_trigram": "离",
                "use_trigram": "坎",
                "moving_line": 3,
            }
        )
        self.assertTrue(result["can_interpret_relation"])
        self.assertEqual(result["question_domain"], "project_career")
        self.assertEqual(result["computed_body_use_relation"], "克体")
        self.assertEqual(result["interpretation_frame"]["relation_code"], "pressure_body")
        self.assertIn("核实关键事实和截止时间。", result["interpretation_frame"]["low_risk_actions"])

    def test_accepts_casting_record(self):
        cast = meihua_casting_recorder.record(
            {
                "question_text": "这个项目沟通当前的主要阻力和下一步是什么？",
                "casting_method": "number_casting",
                "numbers": [27, 14],
                "body_trigram": "离",
                "use_trigram": "坎",
                "moving_line": 3,
            }
        )
        result = meihua_relation_interpreter.interpret({"casting_record": cast, "focus": "项目沟通"})
        self.assertTrue(result["can_interpret_relation"])
        self.assertEqual(result["body_trigram"], "离")
        self.assertEqual(result["interpretation_frame"]["relation_code"], "pressure_body")

    def test_missing_casting_fields_prevent_interpretation(self):
        result = meihua_relation_interpreter.interpret({"question_text": "这个项目怎么推进？"})
        self.assertFalse(result["casting_is_valid"])
        self.assertFalse(result["can_interpret_relation"])
        self.assertIn("body_trigram", result["missing_fields"])
        self.assertEqual(result["interpretation_frame"], {})

    def test_finance_risk_blocks_relation_interpretation(self):
        result = meihua_relation_interpreter.interpret(
            {
                "question_text": "用梅花看我该不该贷款梭哈股票",
                "casting_method": "external_chart",
                "chart_source": "外部排盘工具",
                "body_trigram": "震",
                "use_trigram": "兑",
                "moving_line": "上爻",
            }
        )
        self.assertFalse(result["can_interpret_relation"])
        self.assertIn("professional_finance", result["risk_flags"])
        self.assertEqual(result["interpretation_frame"], {})

    def test_relation_mismatch_warning_is_preserved(self):
        result = meihua_relation_interpreter.interpret(
            {
                "question_text": "这个项目沟通当前的主要阻力和下一步是什么？",
                "casting_method": "number_casting",
                "numbers": "27,14",
                "body_trigram": "离",
                "use_trigram": "坎",
                "moving_line": "三爻",
                "body_use_relation": "生体",
            }
        )
        self.assertTrue(result["can_interpret_relation"])
        self.assertEqual(result["computed_body_use_relation"], "克体")
        self.assertTrue(any("differs from computed" in warning for warning in result["warnings"]))


class NamingSymbolLookupTests(unittest.TestCase):
    def test_dimension_lookup_returns_safe_prompt(self):
        result = naming_symbol_lookup.lookup({"query": "字义", "category": "dimension", "focus": "baby_name"})
        self.assertEqual(result["canonical_name"], "字义")
        self.assertEqual(result["system"], "chinese_naming")
        self.assertIn("本义", result["keywords"])
        self.assertTrue(result["prohibited_uses"])

    def test_sound_alias_normalizes(self):
        result = naming_symbol_lookup.lookup({"query": "读音", "category": "维度"})
        self.assertEqual(result["canonical_name"], "字音")
        self.assertEqual(result["category"], "dimension")

    def test_element_lookup(self):
        result = naming_symbol_lookup.lookup({"query": "木", "category": "五行"})
        self.assertEqual(result["category"], "element")
        self.assertIn("成长", result["keywords"])

    def test_name_type_lookup(self):
        result = naming_symbol_lookup.lookup({"query": "乳名", "category": "类型"})
        self.assertEqual(result["canonical_name"], "小名")
        self.assertEqual(result["category"], "name_type")

    def test_cultural_check_lookup(self):
        result = naming_symbol_lookup.lookup({"query": "谐音", "category": "检查"})
        self.assertEqual(result["category"], "cultural_check")
        self.assertIn("方言读法", result["keywords"])

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            naming_symbol_lookup.lookup({"query": "不存在的姓名学术语"})


class NamingCandidateComparatorTests(unittest.TestCase):
    def test_baby_name_candidates_are_ranked_safely(self):
        result = naming_candidate_comparator.compare(
            {
                "request_text": "想比较沐安、清宁哪个更适合宝宝名",
                "name_type": "formal_name",
                "surname": "林",
                "candidates": ["沐安", "清宁"],
                "priorities": ["字义", "读音"],
                "desired_elements": ["water"],
                "subject_is_minor": True,
            }
        )
        self.assertTrue(result["can_compare_names"])
        self.assertEqual(result["candidate_count"], 2)
        self.assertEqual(result["risk_flags"], [])
        self.assertIn(result["ranked_candidates"][0], {"沐安", "清宁"})
        self.assertTrue(any("命运" in warning for warning in result["warnings"]))

    def test_fatalistic_claim_is_flagged_but_can_be_reframed(self):
        result = naming_candidate_comparator.compare(
            {
                "request_text": "沐安是不是必发财，清宁会不会克父母",
                "name_type": "formal_name",
                "candidates": ["沐安", "清宁"],
                "priorities": ["五行"],
                "subject_is_minor": True,
            }
        )
        self.assertTrue(result["can_compare_names"])
        self.assertIn("deterministic_fate_claim", result["risk_flags"])
        self.assertTrue(any("宿命论" in warning for warning in result["warnings"]))

    def test_brand_registration_claim_is_flagged(self):
        result = naming_candidate_comparator.compare(
            {
                "request_text": "比较星禾和清朗，哪个商标一定可注册不会侵权",
                "name_type": "brand_name",
                "candidates": ["星禾", "清朗"],
                "priorities": ["传播", "谐音"],
            }
        )
        self.assertTrue(result["can_compare_names"])
        self.assertIn("professional_registration_claim", result["risk_flags"])
        self.assertTrue(any("商标" in warning for warning in result["warnings"]))

    def test_missing_candidates_are_reported(self):
        result = naming_candidate_comparator.compare({"request_text": "帮我取个好名字"})
        self.assertFalse(result["can_compare_names"])
        self.assertIn("candidates", result["missing_fields"])
        self.assertIn("name_type", result["missing_fields"])


class NamingBrandScenarioScorerTests(unittest.TestCase):
    def test_brand_names_are_ranked_for_scenario(self):
        result = naming_brand_scenario_scorer.score(
            {
                "request_text": "给茶饮品牌比较星禾和清朗",
                "candidates": ["星禾", "清朗"],
                "category": "茶饮",
                "audience": "年轻上班族",
                "tone": ["清爽", "年轻"],
                "channels": ["门头", "小红书", "搜索", "域名"],
            }
        )
        self.assertTrue(result["can_score_brand_names"])
        self.assertEqual(result["candidate_count"], 2)
        self.assertIn(result["ranked_candidates"][0], {"星禾", "清朗"})
        self.assertTrue(any("商标" in warning for warning in result["warnings"]))
        self.assertTrue(result["evaluations"][0]["external_checks"])

    def test_registration_and_fate_claims_are_flagged(self):
        result = naming_brand_scenario_scorer.score(
            {
                "request_text": "星禾这个品牌名是不是一定可注册还会旺财必火",
                "candidates": ["星禾"],
                "category": "茶饮",
                "audience": "年轻人",
                "channels": ["搜索", "域名"],
            }
        )
        self.assertTrue(result["can_score_brand_names"])
        self.assertIn("professional_registration_claim", result["risk_flags"])
        self.assertIn("deterministic_fate_or_virality_claim", result["risk_flags"])
        self.assertTrue(any("必火" in warning or "招财" in warning for warning in result["warnings"]))

    def test_regulated_industry_claim_blocks_scoring(self):
        result = naming_brand_scenario_scorer.score(
            {
                "request_text": "保健药品牌叫安宁，能不能暗示治疗功效和收益稳赚",
                "candidates": ["安宁"],
                "category": "医疗",
                "audience": "中老年人",
                "channels": ["电商", "搜索"],
            }
        )
        self.assertFalse(result["can_score_brand_names"])
        self.assertIn("regulated_industry_claim", result["risk_flags"])
        self.assertTrue(any("专业合规" in warning for warning in result["warnings"]))

    def test_missing_context_is_reported(self):
        result = naming_brand_scenario_scorer.score({"request_text": "帮我想个品牌名"})
        self.assertFalse(result["can_score_brand_names"])
        self.assertIn("candidates", result["missing_fields"])
        self.assertIn("category", result["missing_fields"])
        self.assertIn("audience", result["missing_fields"])


class NumerologyRequestGuardTests(unittest.TestCase):
    def test_phone_suffix_symbolic_request_can_continue(self):
        result = numerology_request_guard.guard({"request_text": "比较手机号尾号 168 和 739，只做数字象征和记忆度分析"})
        self.assertTrue(result["can_continue_numerology"])
        self.assertEqual(result["reading_intent"], "number_symbol_reflection")
        self.assertFalse(result["risk_flags"])

    def test_sensitive_identifier_is_blocked(self):
        result = numerology_request_guard.guard({"request_text": "用我的身份证 123456 看数字能量"})
        self.assertFalse(result["can_continue_numerology"])
        self.assertIn("privacy_sensitive_identifier", result["risk_flags"])

    def test_wealth_claim_is_blocked(self):
        result = numerology_request_guard.guard({"request_text": "哪个手机号能让我股票必发财"})
        self.assertFalse(result["can_continue_numerology"])
        self.assertIn("financial_claim", result["risk_flags"])


class NumerologyProfileRecorderTests(unittest.TestCase):
    def test_records_redacted_phone_suffix_digits(self):
        result = numerology_profile_recorder.record({"number_text": "比较手机号尾号 168 和 739，只看象征和记忆度"})
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["number_context"], "phone_suffix")
        self.assertEqual(result["digits"], ["1", "6", "8", "7", "3", "9"])

    def test_long_sensitive_number_is_blocked(self):
        result = numerology_profile_recorder.record({"number_text": "完整手机号 13812345678 帮我看数字能量"})
        self.assertFalse(result["is_valid"])
        self.assertIn("privacy_sensitive_identifier", result["risk_flags"])


class NumerologySymbolLookupTests(unittest.TestCase):
    def test_eight_symbol_does_not_guarantee_wealth(self):
        result = numerology_symbol_lookup.lookup({"query": "8", "focus": "phone_suffix"})
        self.assertEqual(result["canonical_name"], "8")
        self.assertEqual(result["symbol_code"], "8")
        self.assertTrue(any("发财" in item for item in result["prohibited_uses"]))

    def test_context_alias_normalizes(self):
        result = numerology_symbol_lookup.lookup({"query": "手机号"})
        self.assertEqual(result["symbol_code"], "phone_suffix")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            numerology_symbol_lookup.lookup({"query": "不存在的数字符号"})


class NumerologyInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_record_and_symbols(self):
        result = numerology_interpretation_planner.plan({"number_text": "比较手机号尾号 168 和 739，只看象征和记忆度"})
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("phone_suffix", symbol_codes)
        self.assertIn("1", symbol_codes)
        self.assertEqual(result["synthesis"]["symbol_count"], len(result["symbol_plans"]))

    def test_planner_blocks_sensitive_identifier(self):
        result = numerology_interpretation_planner.plan({"number_text": "身份证 123456789 用数字能量看命运"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_numerology"])
        self.assertIn("privacy_sensitive_identifier", result["risk_flags"])


class PendulumRequestGuardTests(unittest.TestCase):
    def test_low_risk_reflection_can_continue(self):
        result = pendulum_request_guard.guard({"request_text": "用灵摆做一次低风险自我反思，左右摆是什么意思"})
        self.assertTrue(result["can_continue_pendulum"])
        self.assertEqual(result["reading_intent"], "pendulum_symbolic_reflection")
        self.assertFalse(result["risk_flags"])

    def test_professional_replacement_is_blocked(self):
        result = pendulum_request_guard.guard({"request_text": "我生病了不用医生，只听灵摆决定怎么处理"})
        self.assertFalse(result["can_continue_pendulum"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("health_or_safety", result["risk_flags"])

    def test_spirit_fear_is_blocked(self):
        result = pendulum_request_guard.guard({"request_text": "用灵摆确认我是不是有邪灵附身"})
        self.assertFalse(result["can_continue_pendulum"])
        self.assertIn("spirit_fear_claim", result["risk_flags"])


class PendulumSessionRecorderTests(unittest.TestCase):
    def test_records_side_to_side_motion(self):
        result = pendulum_session_recorder.record(
            {
                "question_text": "用灵摆做一次低风险自我反思，左右摆代表我需要比较沟通方案吗",
                "answer_motion": "左右",
                "calibration_notes": "左右表示需要比较，顺时针表示倾向推进。",
                "consent_confirmed": True,
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["answer_motion"], "side_to_side")
        self.assertEqual(result["question_type"], "yes_no")
        self.assertIn("reframed_open_question", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = pendulum_session_recorder.record({"question_text": "不用律师，只听灵摆决定要不要签合同"})
        self.assertFalse(result["is_valid"])
        self.assertIn("professional_replacement", result["risk_flags"])


class PendulumSymbolLookupTests(unittest.TestCase):
    def test_side_to_side_symbol_keeps_boundary(self):
        result = pendulum_symbol_lookup.lookup({"query": "左右", "focus": "relationship_boundary"})
        self.assertEqual(result["canonical_name"], "左右摆动")
        self.assertEqual(result["symbol_code"], "side_to_side")
        self.assertTrue(any("事实证明" in item for item in result["prohibited_uses"]))

    def test_calibration_alias_normalizes(self):
        result = pendulum_symbol_lookup.lookup({"query": "校准"})
        self.assertEqual(result["symbol_code"], "calibration")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            pendulum_symbol_lookup.lookup({"query": "不存在的灵摆符号"})


class PendulumInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_record_and_symbols(self):
        result = pendulum_interpretation_planner.plan(
            {
                "question_text": "用灵摆做一次低风险自我反思，左右摆代表我需要比较沟通方案吗",
                "answer_motion": "左右",
                "calibration_notes": "左右表示需要比较，顺时针表示倾向推进。",
                "consent_confirmed": True,
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("calibration", symbol_codes)
        self.assertIn("side_to_side", symbol_codes)
        self.assertEqual(result["synthesis"]["symbol_count"], len(result["symbol_plans"]))

    def test_planner_blocks_professional_spirit_fear(self):
        result = pendulum_interpretation_planner.plan({"question_text": "我生病了不用医生，只听灵摆确认是不是有邪灵附身"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_pendulum"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("spirit_fear_claim", result["risk_flags"])


class RuneRequestGuardTests(unittest.TestCase):
    def test_low_risk_three_rune_reflection_can_continue(self):
        result = rune_request_guard.guard({"request_text": "用卢恩符文抽三符看项目推进，只做象征反思"})
        self.assertTrue(result["can_continue_rune"])
        self.assertEqual(result["reading_intent"], "rune_symbolic_reading")
        self.assertFalse(result["risk_flags"])

    def test_professional_curse_fear_is_blocked(self):
        result = rune_request_guard.guard({"request_text": "我生病了不用医生，只听符文确认是不是被诅咒"})
        self.assertFalse(result["can_continue_rune"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("spirit_fear_claim", result["risk_flags"])

    def test_financial_claim_is_blocked(self):
        result = rune_request_guard.guard({"request_text": "用符文决定明天贷款买哪只股票会发财"})
        self.assertFalse(result["can_continue_rune"])
        self.assertIn("financial_claim", result["risk_flags"])


class RuneCastRecorderTests(unittest.TestCase):
    def test_records_three_rune_cast(self):
        result = rune_cast_recorder.record({"question_text": "用卢恩符文抽三符看项目推进", "spread_type": "three_rune", "runes": "fehu ansuz raidho"})
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["rune_count"], 3)
        self.assertEqual(result["positions"], ["context", "challenge", "next_step"])
        self.assertFalse(result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = rune_cast_recorder.record({"question_text": "不用律师，只听符文决定要不要签合同", "runes": "tiwaz"})
        self.assertFalse(result["is_valid"])
        self.assertIn("professional_replacement", result["risk_flags"])


class RuneSymbolLookupTests(unittest.TestCase):
    def test_fehu_symbol_lookup_keeps_finance_boundary(self):
        result = rune_symbol_lookup.lookup({"query": "fehu", "focus": "project_resources"})
        self.assertEqual(result["canonical_name"], "Fehu")
        self.assertEqual(result["symbol_code"], "fehu")
        self.assertIn("资源", result["keywords"])
        self.assertIn("不承诺发财", result["action_guidance"])

    def test_chinese_alias_normalizes(self):
        result = rune_symbol_lookup.lookup({"query": "保护"})
        self.assertEqual(result["symbol_code"], "algiz")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            rune_symbol_lookup.lookup({"query": "not-a-rune"})


class RuneInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_cast_and_symbols(self):
        result = rune_interpretation_planner.plan({"question_text": "用卢恩符文抽三符看项目推进", "spread_type": "three_rune", "runes": "fehu ansuz raidho"})
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 3)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("fehu", symbol_codes)
        self.assertIn("ansuz", symbol_codes)
        self.assertEqual(result["synthesis"]["symbol_count"], 3)

    def test_planner_blocks_professional_curse_fear(self):
        result = rune_interpretation_planner.plan({"question_text": "我生病了不用医生，只听符文确认是不是被诅咒", "runes": "algiz"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_rune"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("spirit_fear_claim", result["risk_flags"])


class LenormandRequestGuardTests(unittest.TestCase):
    def test_low_risk_three_card_reflection_can_continue(self):
        result = lenormand_request_guard.guard({"request_text": "用雷诺曼三张牌看项目沟通，只做象征反思"})
        self.assertTrue(result["can_continue_lenormand"])
        self.assertEqual(result["reading_intent"], "lenormand_symbolic_reading")
        self.assertFalse(result["risk_flags"])

    def test_professional_third_party_request_is_blocked(self):
        result = lenormand_request_guard.guard({"request_text": "不用律师，只用雷诺曼看老板真实想法决定要不要签合同"})
        self.assertFalse(result["can_continue_lenormand"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("third_party_privacy", result["risk_flags"])

    def test_financial_claim_is_blocked(self):
        result = lenormand_request_guard.guard({"request_text": "用雷诺曼决定明天贷款买哪只股票会发财"})
        self.assertFalse(result["can_continue_lenormand"])
        self.assertIn("financial_claim", result["risk_flags"])


class LenormandDrawRecorderTests(unittest.TestCase):
    def test_records_three_card_line(self):
        result = lenormand_draw_recorder.record({"question_text": "用雷诺曼三张牌看项目沟通", "spread_type": "three_card_line", "cards": "骑士 信 钥匙"})
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["card_count"], 3)
        self.assertEqual(result["positions"], ["left_context", "center_focus", "right_development"])
        self.assertFalse(result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = lenormand_draw_recorder.record({"question_text": "不用律师，只用雷诺曼决定要不要签合同", "cards": "书 戒指 狐狸"})
        self.assertFalse(result["is_valid"])
        self.assertIn("professional_replacement", result["risk_flags"])


class LenormandCardLookupTests(unittest.TestCase):
    def test_rider_card_lookup_keeps_prediction_boundary(self):
        result = lenormand_card_lookup.lookup({"query": "骑士", "focus": "project_message"})
        self.assertEqual(result["canonical_name"], "骑士")
        self.assertEqual(result["card_code"], "rider")
        self.assertIn("消息", result["keywords"])
        self.assertIn("不承诺消息一定会来", result["action_guidance"])

    def test_chinese_alias_normalizes(self):
        result = lenormand_card_lookup.lookup({"query": "心"})
        self.assertEqual(result["card_code"], "heart")

    def test_unknown_card_raises(self):
        with self.assertRaises(ValueError):
            lenormand_card_lookup.lookup({"query": "not-a-lenormand-card"})


class LenormandInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_draw_cards_and_pairs(self):
        result = lenormand_interpretation_planner.plan({"question_text": "用雷诺曼三张牌看项目沟通", "spread_type": "three_card_line", "cards": "骑士 信 钥匙"})
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["card_plans"]), 3)
        self.assertEqual(len(result["pair_plans"]), 2)
        card_codes = {item["card_code"] for item in result["card_plans"]}
        self.assertIn("rider", card_codes)
        self.assertIn("letter", card_codes)
        self.assertEqual(result["synthesis"]["card_count"], 3)

    def test_planner_blocks_professional_third_party(self):
        result = lenormand_interpretation_planner.plan({"question_text": "不用律师，只用雷诺曼看老板真实想法决定要不要签合同", "cards": "书 戒指 狐狸"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_lenormand"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("third_party_privacy", result["risk_flags"])


class CrystalRequestGuardTests(unittest.TestCase):
    def test_low_risk_workspace_request_can_continue(self):
        result = crystal_request_guard.guard({"request_text": "想在办公桌放白水晶和紫水晶，只做提醒和空间秩序"})
        self.assertTrue(result["can_continue_crystal"])
        self.assertEqual(result["consultation_intent"], "crystal_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_medical_ingestion_purchase_pressure_is_blocked(self):
        result = crystal_request_guard.guard({"request_text": "我失眠不用医生，喝水晶水治疗，越贵越灵"})
        self.assertFalse(result["can_continue_crystal"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("medical_healing_claim", result["risk_flags"])
        self.assertIn("ingestion_or_body_harm", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])

    def test_financial_claim_is_blocked(self):
        result = crystal_request_guard.guard({"request_text": "戴黄水晶一定会让我贷款投资发财"})
        self.assertFalse(result["can_continue_crystal"])
        self.assertIn("financial_claim", result["risk_flags"])
        self.assertIn("deterministic_fate", result["risk_flags"])


class CrystalItemRecorderTests(unittest.TestCase):
    def test_records_existing_workspace_items(self):
        result = crystal_item_recorder.record(
            {
                "intention_text": "想在办公桌放白水晶和紫水晶，只做提醒和空间秩序",
                "items": "白水晶 紫水晶",
                "use_context": "workspace",
                "budget_note": "已有物件，不新增购买",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["item_count"], 2)
        self.assertEqual(result["use_context"], "workspace")
        self.assertFalse(result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = crystal_item_recorder.record({"intention_text": "不用医生，只靠紫水晶治疗失眠", "items": "紫水晶", "budget_note": "已有"})
        self.assertFalse(result["is_valid"])
        self.assertIn("professional_replacement", result["risk_flags"])


class CrystalSymbolLookupTests(unittest.TestCase):
    def test_clear_quartz_lookup_keeps_healing_boundary(self):
        result = crystal_symbol_lookup.lookup({"query": "白水晶", "focus": "workspace_order"})
        self.assertEqual(result["canonical_name"], "白水晶")
        self.assertEqual(result["symbol_code"], "clear_quartz")
        self.assertIn("清明", result["keywords"])
        self.assertIn("不写成万能净化或疗愈工具", result["action_guidance"])

    def test_english_alias_normalizes(self):
        result = crystal_symbol_lookup.lookup({"query": "rose quartz"})
        self.assertEqual(result["symbol_code"], "rose_quartz")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            crystal_symbol_lookup.lookup({"query": "not-a-crystal"})


class CrystalUsePlannerTests(unittest.TestCase):
    def test_planner_combines_items_and_symbols(self):
        result = crystal_use_planner.plan(
            {
                "intention_text": "想在办公桌放白水晶和紫水晶，只做提醒和空间秩序",
                "items": "白水晶 紫水晶",
                "use_context": "workspace",
                "budget_note": "已有物件，不新增购买",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 2)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("clear_quartz", symbol_codes)
        self.assertIn("amethyst", symbol_codes)
        self.assertEqual(result["use_plan"]["item_count"], 2)

    def test_unknown_trade_name_does_not_invent_power(self):
        result = crystal_use_planner.plan(
            {
                "intention_text": "想用商家推荐的星辰守护石做提醒物",
                "items": "星辰守护石",
                "use_context": "workspace",
                "budget_note": "先不购买，只记录",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_trade_name")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_medical_ingestion_purchase_pressure(self):
        result = crystal_use_planner.plan({"intention_text": "我失眠不用医生，喝水晶水治疗，越贵越灵", "items": "紫水晶", "use_context": "bedside", "budget_note": "准备买贵的"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_crystal"])
        self.assertIn("medical_healing_claim", result["risk_flags"])
        self.assertIn("ingestion_or_body_harm", result["risk_flags"])


class CandleRequestGuardTests(unittest.TestCase):
    def test_low_risk_extinguished_observation_can_continue(self):
        result = candle_request_guard.guard({"request_text": "我已经熄灭蜡烛，看到火焰稳定、蜡泪像河流，想做项目推进的低风险提醒"})
        self.assertTrue(result["can_continue_candle"])
        self.assertEqual(result["consultation_intent"], "candle_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_dangerous_ritual_request_is_blocked(self):
        result = candle_request_guard.guard({"request_text": "教我密闭房间点蜡烛烧符驱邪，反复点到鬼走为止，不用报警医生"})
        self.assertFalse(result["can_continue_candle"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])

    def test_third_party_coercion_is_blocked(self):
        result = candle_request_guard.guard({"request_text": "用蜡烛看前任现在的真实想法，让他回来"})
        self.assertFalse(result["can_continue_candle"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("coercion_or_control", result["risk_flags"])


class CandleObservationRecorderTests(unittest.TestCase):
    def test_records_safe_candle_observation(self):
        result = candle_observation_recorder.record(
            {
                "question_text": "我已经熄灭蜡烛，看到火焰稳定、蜡泪像河流，想做项目推进的低风险提醒",
                "observation_source": "user_described",
                "observation_state": "already_extinguished",
                "flame_notes": "稳定火焰",
                "wax_shapes": "河流",
                "focus": "project_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["flame_notes"], ["稳定火焰"])
        self.assertEqual(result["wax_shapes"], ["河流"])
        self.assertEqual(result["observation_state"], "already_extinguished")
        self.assertFalse(result["missing_fields"])

    def test_invalid_observation_state_is_marked_missing(self):
        result = candle_observation_recorder.record(
            {
                "question_text": "想记录已经熄灭后的烛火观察",
                "observation_state": "still_burning",
                "flame_notes": "稳定火焰",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertIn("safe_observation_state", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = candle_observation_recorder.record(
            {
                "question_text": "教我密闭房间点蜡烛烧符驱邪，反复点到鬼走为止，不用报警医生",
                "flame_notes": "高火焰",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class CandleSymbolLookupTests(unittest.TestCase):
    def test_steady_flame_lookup_keeps_prediction_boundary(self):
        result = candle_symbol_lookup.lookup({"query": "稳定火焰", "focus": "project_reflection"})
        self.assertEqual(result["canonical_name"], "稳定火焰")
        self.assertEqual(result["symbol_code"], "steady_flame")
        self.assertIn("稳定", result["keywords"])
        self.assertIn("不写成必然成功", result["action_guidance"])

    def test_wax_alias_normalizes(self):
        result = candle_symbol_lookup.lookup({"query": "河流"})
        self.assertEqual(result["symbol_code"], "river_wax")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            candle_symbol_lookup.lookup({"query": "not-a-candle-symbol"})


class CandleInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_observation_and_symbols(self):
        result = candle_interpretation_planner.plan(
            {
                "question_text": "我已经熄灭蜡烛，看到火焰稳定、蜡泪像河流，想做项目推进的低风险提醒",
                "observation_source": "user_described",
                "observation_state": "already_extinguished",
                "flame_notes": "稳定火焰",
                "wax_shapes": "河流",
                "focus": "project_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 2)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("steady_flame", symbol_codes)
        self.assertIn("river_wax", symbol_codes)

    def test_unknown_observation_does_not_invent_meaning(self):
        result = candle_interpretation_planner.plan(
            {
                "question_text": "想记录照片里的蜡泪形状",
                "observation_state": "photo_notes",
                "wax_shapes": "星门形",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_ambiguous_candle_observation")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_dangerous_ritual(self):
        result = candle_interpretation_planner.plan(
            {
                "question_text": "教我密闭房间点蜡烛烧符驱邪，反复点到鬼走为止，不用报警医生",
                "flame_notes": "高火焰",
                "focus": "exorcism",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_candle"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class IncenseRequestGuardTests(unittest.TestCase):
    def test_low_risk_extinguished_observation_can_continue(self):
        result = incense_request_guard.guard({"request_text": "我已经确认香熄灭了，香灰像塔形、烟之前直上，想做项目推进的低风险提醒"})
        self.assertTrue(result["can_continue_incense"])
        self.assertEqual(result["consultation_intent"], "incense_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_dangerous_ritual_request_is_blocked(self):
        result = incense_request_guard.guard({"request_text": "教我密闭房间通宵烧香烧符驱邪，香灰冲水喝，不用医生，反复点到鬼走"})
        self.assertFalse(result["can_continue_incense"])
        self.assertIn("active_burning_instruction", result["risk_flags"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])

    def test_third_party_purchase_pressure_is_blocked(self):
        result = incense_request_guard.guard({"request_text": "用看香知道前任现在的真实想法，让他回来，还必须买天价开光香"})
        self.assertFalse(result["can_continue_incense"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("coercion_or_control", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])


class IncenseObservationRecorderTests(unittest.TestCase):
    def test_records_safe_incense_observation(self):
        result = incense_observation_recorder.record(
            {
                "question_text": "我已经确认香熄灭了，香灰像塔形、烟之前直上，想做项目推进的低风险提醒",
                "observation_source": "user_described",
                "observation_state": "already_extinguished",
                "ash_shapes": "塔形",
                "smoke_notes": "直上烟",
                "focus": "project_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["ash_shapes"], ["塔形"])
        self.assertEqual(result["smoke_notes"], ["直上烟"])
        self.assertEqual(result["observation_state"], "already_extinguished")
        self.assertFalse(result["missing_fields"])

    def test_invalid_observation_state_is_marked_missing(self):
        result = incense_observation_recorder.record(
            {
                "question_text": "想记录已经熄灭后的香灰观察",
                "observation_state": "still_burning",
                "ash_shapes": "塔形",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertIn("safe_observation_state", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = incense_observation_recorder.record(
            {
                "question_text": "教我密闭房间通宵烧香烧符驱邪，香灰冲水喝，不用医生，反复点到鬼走",
                "smoke_notes": "浓烟",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class IncenseSymbolLookupTests(unittest.TestCase):
    def test_tower_ash_lookup_keeps_miracle_boundary(self):
        result = incense_symbol_lookup.lookup({"query": "塔形", "focus": "project_reflection"})
        self.assertEqual(result["canonical_name"], "塔形香灰")
        self.assertEqual(result["symbol_code"], "tower_ash")
        self.assertIn("累积", result["keywords"])
        self.assertIn("不写成神迹", result["action_guidance"])

    def test_smoke_alias_normalizes(self):
        result = incense_symbol_lookup.lookup({"query": "直上烟"})
        self.assertEqual(result["symbol_code"], "straight_smoke")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            incense_symbol_lookup.lookup({"query": "not-an-incense-symbol"})


class IncenseInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_observation_and_symbols(self):
        result = incense_interpretation_planner.plan(
            {
                "question_text": "我已经确认香熄灭了，香灰像塔形、烟之前直上，想做项目推进的低风险提醒",
                "observation_source": "user_described",
                "observation_state": "already_extinguished",
                "ash_shapes": "塔形",
                "smoke_notes": "直上烟",
                "focus": "project_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 2)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("tower_ash", symbol_codes)
        self.assertIn("straight_smoke", symbol_codes)

    def test_unknown_observation_does_not_invent_meaning(self):
        result = incense_interpretation_planner.plan(
            {
                "question_text": "想记录照片里的香灰形状",
                "observation_state": "photo_notes",
                "ash_shapes": "莲门形",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_ambiguous_incense_observation")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_dangerous_ritual(self):
        result = incense_interpretation_planner.plan(
            {
                "question_text": "教我密闭房间通宵烧香烧符驱邪，香灰冲水喝，不用医生，反复点到鬼走",
                "smoke_notes": "浓烟",
                "focus": "exorcism",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_incense"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class AromaRequestGuardTests(unittest.TestCase):
    def test_low_risk_aroma_can_continue(self):
        result = aroma_request_guard.guard({"request_text": "想用芳香精油做低风险气味象征，已有薰衣草和柑橘闻香纸，只做睡前收束和空间切换，不内服不直接涂不治疗不碰宠物不高价购买不反复闻"})
        self.assertTrue(result["can_continue_aroma"])
        self.assertEqual(result["consultation_intent"], "aroma_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_medical_ingestion_pet_fire_purchase_dependency_request_is_blocked(self):
        result = aroma_request_guard.guard({"request_text": "不用医生，喝精油治疗焦虑，原液直接涂给宝宝和猫，密闭房间整夜扩香驱邪，还必须买高价精油套装，反复调到满意"})
        self.assertFalse(result["can_continue_aroma"])
        self.assertIn("medical_or_mental_health_claim", result["risk_flags"])
        self.assertIn("ingestion_or_unsafe_application", result["risk_flags"])
        self.assertIn("pregnancy_baby_pet_allergy", result["risk_flags"])
        self.assertIn("fire_or_diffuser_safety", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("spirit_fear_or_exorcism", result["risk_flags"])
        self.assertIn("purchase_pressure", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class AromaContextRecorderTests(unittest.TestCase):
    def test_records_safe_aroma_context(self):
        result = aroma_context_recorder.record(
            {
                "question_text": "想用芳香精油做低风险气味象征，已有薰衣草和柑橘闻香纸，只做睡前收束和空间切换，不内服不直接涂不治疗不碰宠物不高价购买不反复闻",
                "scent_items": "薰衣草, 柑橘",
                "scent_source": "existing_smelling_strip",
                "use_mode": "闻香纸",
                "space": "卧室门口",
                "duration": "3分钟",
                "ventilation": "开窗",
                "focus": "sleep_boundary_reflection",
                "safety_context": "非接触, 不靠近宠物",
                "reality_constraints": "不购买, 不扩香",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["scent_items"], ["薰衣草", "柑橘"])
        self.assertEqual(result["use_mode"], "闻香纸")
        self.assertEqual(result["ventilation"], "开窗")
        self.assertFalse(result["missing_fields"])

    def test_missing_scent_items_are_marked(self):
        result = aroma_context_recorder.record({"question_text": "想做芳香气味象征记录"})
        self.assertTrue(result["is_valid"])
        self.assertIn("scent_items", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = aroma_context_recorder.record(
            {
                "question_text": "不用医生，喝精油治疗焦虑，原液直接涂给宝宝和猫，密闭房间整夜扩香驱邪，还必须买高价精油套装，反复调到满意",
                "scent_items": "薰衣草",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("ingestion_or_unsafe_application", result["risk_flags"])


class AromaSymbolLookupTests(unittest.TestCase):
    def test_lavender_lookup_keeps_medical_boundary(self):
        result = aroma_symbol_lookup.lookup({"query": "薰衣草", "focus": "sleep_boundary_reflection"})
        self.assertEqual(result["symbol_code"], "lavender")
        self.assertIn("安静", result["keywords"])
        self.assertIn("不写成治疗失眠", result["action_guidance"])

    def test_diffuser_alias_normalizes(self):
        result = aroma_symbol_lookup.lookup({"query": "香薰机"})
        self.assertEqual(result["symbol_code"], "diffuser")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            aroma_symbol_lookup.lookup({"query": "not-an-aroma-symbol"})


class AromaPracticePlannerTests(unittest.TestCase):
    def test_planner_combines_scents_method_and_safety_layer(self):
        result = aroma_practice_planner.plan(
            {
                "question_text": "想用芳香精油做低风险气味象征，已有薰衣草和柑橘闻香纸，只做睡前收束和空间切换，不内服不直接涂不治疗不碰宠物不高价购买不反复闻",
                "scent_items": "薰衣草, 柑橘",
                "scent_source": "existing_smelling_strip",
                "use_mode": "闻香纸",
                "space": "卧室门口",
                "duration": "3分钟",
                "ventilation": "开窗",
                "focus": "sleep_boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("lavender", symbol_codes)
        self.assertIn("citrus", symbol_codes)
        self.assertIn("smelling_strip", symbol_codes)
        self.assertIn("ventilation", symbol_codes)
        self.assertEqual(result["practice_plan"]["symbol_count"], 4)

    def test_unknown_custom_scent_does_not_invent_claims(self):
        result = aroma_practice_planner.plan(
            {
                "question_text": "想记录一个品牌自定义混香的气味联想",
                "scent_items": "月光森林调",
                "use_mode": "闻香纸",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_custom_aroma_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造治疗", unknown_items[0]["action_guidance"])

    def test_planner_blocks_unsafe_medical_purchase_dependency_request(self):
        result = aroma_practice_planner.plan(
            {
                "question_text": "不用医生，喝精油治疗焦虑，原液直接涂给宝宝和猫，密闭房间整夜扩香驱邪，还必须买高价精油套装，反复调到满意",
                "scent_items": "薰衣草",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_aroma"])
        self.assertIn("medical_or_mental_health_claim", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class HerbalRequestGuardTests(unittest.TestCase):
    def test_low_risk_herbal_can_continue(self):
        result = herbal_request_guard.guard({"request_text": "想用草本香草做低风险植物象征，已有迷迭香和月桂叶植物意图卡，只做书桌边界和项目复盘，不内服不泡水喝不外敷不野采不用明火不治疗不碰宠物不下咒不高价购买不反复做"})
        self.assertTrue(result["can_continue_herbal"])
        self.assertEqual(result["consultation_intent"], "herbal_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_medical_ingestion_foraging_fire_spell_purchase_dependency_request_is_blocked(self):
        result = herbal_request_guard.guard({"request_text": "不用医生，喝草药治疗焦虑，外敷给宝宝和猫，去野外采不认识的植物，密闭房间整夜焚烧驱邪，还做爱情咒让他回来，必须买高价草药套装，反复做草药包到安心"})
        self.assertFalse(result["can_continue_herbal"])
        self.assertIn("medical_or_mental_health_claim", result["risk_flags"])
        self.assertIn("ingestion_or_topical_use", result["risk_flags"])
        self.assertIn("pregnancy_baby_pet_allergy", result["risk_flags"])
        self.assertIn("foraging_or_poisoning_risk", result["risk_flags"])
        self.assertIn("fire_smoke_or_mold_safety", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("spirit_fear_or_exorcism", result["risk_flags"])
        self.assertIn("third_party_or_coercion", result["risk_flags"])
        self.assertIn("purchase_pressure", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class HerbalContextRecorderTests(unittest.TestCase):
    def test_records_safe_herbal_context(self):
        result = herbal_context_recorder.record(
            {
                "question_text": "想用草本香草做低风险植物象征，已有迷迭香和月桂叶植物意图卡，只做书桌边界和项目复盘，不内服不泡水喝不外敷不野采不用明火不治疗不碰宠物不下咒不高价购买不反复做",
                "plant_items": "迷迭香, 月桂叶",
                "plant_source": "existing_shop_bought_dried_items",
                "use_mode": "植物意图卡",
                "container_or_form": "草药袋",
                "space": "书桌",
                "duration": "一周后复盘",
                "focus": "project_boundary_reflection",
                "safety_context": "非接触, 不入口, 无火",
                "reality_constraints": "不购买, 不野采",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["plant_items"], ["迷迭香", "月桂叶"])
        self.assertEqual(result["use_mode"], "植物意图卡")
        self.assertEqual(result["container_or_form"], "草药袋")
        self.assertFalse(result["missing_fields"])

    def test_missing_plant_items_are_marked(self):
        result = herbal_context_recorder.record({"question_text": "想做草本香草象征记录"})
        self.assertTrue(result["is_valid"])
        self.assertIn("plant_items", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = herbal_context_recorder.record(
            {
                "question_text": "不用医生，喝草药治疗焦虑，外敷给宝宝和猫，去野外采不认识的植物，密闭房间整夜焚烧驱邪，还做爱情咒让他回来，必须买高价草药套装，反复做草药包到安心",
                "plant_items": "迷迭香",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("ingestion_or_topical_use", result["risk_flags"])


class HerbalSymbolLookupTests(unittest.TestCase):
    def test_rosemary_lookup_keeps_medical_boundary(self):
        result = herbal_symbol_lookup.lookup({"query": "迷迭香", "focus": "project_boundary_reflection"})
        self.assertEqual(result["symbol_code"], "rosemary")
        self.assertIn("记忆", result["keywords"])
        self.assertIn("不写成治疗认知", result["action_guidance"])

    def test_bay_leaf_alias_normalizes(self):
        result = herbal_symbol_lookup.lookup({"query": "月桂叶"})
        self.assertEqual(result["symbol_code"], "bay_leaf")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            herbal_symbol_lookup.lookup({"query": "not-a-herbal-symbol"})


class HerbalPracticePlannerTests(unittest.TestCase):
    def test_planner_combines_plants_container_and_method(self):
        result = herbal_practice_planner.plan(
            {
                "question_text": "想用草本香草做低风险植物象征，已有迷迭香和月桂叶植物意图卡，只做书桌边界和项目复盘，不内服不泡水喝不外敷不野采不用明火不治疗不碰宠物不下咒不高价购买不反复做",
                "plant_items": "迷迭香, 月桂叶",
                "plant_source": "existing_shop_bought_dried_items",
                "use_mode": "植物意图卡",
                "container_or_form": "草药袋",
                "space": "书桌",
                "duration": "一周后复盘",
                "focus": "project_boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("rosemary", symbol_codes)
        self.assertIn("bay_leaf", symbol_codes)
        self.assertIn("journal_card", symbol_codes)
        self.assertIn("sachet", symbol_codes)
        self.assertEqual(result["practice_plan"]["symbol_count"], 4)

    def test_unknown_custom_plant_does_not_invent_claims(self):
        result = herbal_practice_planner.plan(
            {
                "question_text": "想记录一个地方俗称草本的私人联想",
                "plant_items": "月影草",
                "use_mode": "植物意图卡",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_custom_herbal_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造治疗", unknown_items[0]["action_guidance"])

    def test_planner_blocks_unsafe_spell_purchase_dependency_request(self):
        result = herbal_practice_planner.plan(
            {
                "question_text": "不用医生，喝草药治疗焦虑，外敷给宝宝和猫，去野外采不认识的植物，密闭房间整夜焚烧驱邪，还做爱情咒让他回来，必须买高价草药套装，反复做草药包到安心",
                "plant_items": "迷迭香",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_herbal"])
        self.assertIn("medical_or_mental_health_claim", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class SigilRequestGuardTests(unittest.TestCase):
    def test_low_risk_sigil_can_continue(self):
        result = sigil_request_guard.guard({"request_text": "想做一个 sigil 符号印记当项目专注提醒，只用纸上草稿、圆形和钥匙符号、放笔记本一周后复盘，不用血不刻皮肤不纹身不烧不召唤不驱邪不诅咒不操控别人不保证实现不高价购买不反复画"})
        self.assertTrue(result["can_continue_sigil"])
        self.assertEqual(result["consultation_intent"], "sigil_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_body_fire_summoning_curse_guarantee_purchase_dependency_request_is_blocked(self):
        result = sigil_request_guard.guard({"request_text": "我要滴血割手把符号刻皮肤上并做成纹身再焚烧召唤恶魔驱邪，诅咒前任让她回来，保证实现暴富彩票，不用医生不用律师，必须买高价课程，每天画到灵"})
        self.assertFalse(result["can_continue_sigil"])
        self.assertIn("blood_or_body_harm", result["risk_flags"])
        self.assertIn("fire_or_destruction", result["risk_flags"])
        self.assertIn("spirit_summoning_or_exorcism", result["risk_flags"])
        self.assertIn("curse_or_coercion", result["risk_flags"])
        self.assertIn("outcome_guarantee", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("financial_or_legal_risk", result["risk_flags"])
        self.assertIn("tattoo_or_permanent_mark", result["risk_flags"])
        self.assertIn("purchase_pressure", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class SigilContextRecorderTests(unittest.TestCase):
    def test_records_safe_sigil_context(self):
        result = sigil_context_recorder.record(
            {
                "question_text": "想做一个 sigil 符号印记当项目专注提醒，只用纸上草稿、圆形和钥匙符号、放笔记本一周后复盘，不用血不刻皮肤不纹身不烧不召唤不驱邪不诅咒不操控别人不保证实现不高价购买不反复画",
                "intention_text": "我把今天的项目下一步写清楚",
                "symbol_elements": "圆形, 钥匙, 字母合并",
                "source_context": "user_created_paper_draft",
                "medium": "纸上草稿",
                "activation_mode": "日志激活",
                "display_location": "笔记本",
                "duration": "一周后复盘",
                "focus": "project_focus_reflection",
                "safety_context": "无火, 不接触身体, 可擦除",
                "reality_constraints": "不购买, 不永久化",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_elements"], ["圆形", "钥匙", "字母合并"])
        self.assertEqual(result["medium"], "纸上草稿")
        self.assertEqual(result["activation_mode"], "日志激活")
        self.assertFalse(result["missing_fields"])

    def test_missing_intention_and_elements_are_marked(self):
        result = sigil_context_recorder.record({"question_text": "想做 sigil 符号印记记录"})
        self.assertTrue(result["is_valid"])
        self.assertIn("intention_text", result["missing_fields"])
        self.assertIn("symbol_elements", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = sigil_context_recorder.record(
            {
                "question_text": "我要滴血割手把符号刻皮肤上并做成纹身再焚烧召唤恶魔驱邪，诅咒前任让她回来，保证实现暴富彩票，不用医生不用律师，必须买高价课程，每天画到灵",
                "symbol_elements": "圆形",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("blood_or_body_harm", result["risk_flags"])


class SigilSymbolLookupTests(unittest.TestCase):
    def test_circle_lookup_keeps_summoning_boundary(self):
        result = sigil_symbol_lookup.lookup({"query": "圆形", "focus": "project_focus_reflection"})
        self.assertEqual(result["symbol_code"], "circle")
        self.assertIn("边界", result["keywords"])
        self.assertIn("不写成召唤圈", result["action_guidance"])

    def test_key_alias_normalizes(self):
        result = sigil_symbol_lookup.lookup({"query": "钥匙"})
        self.assertEqual(result["symbol_code"], "key")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            sigil_symbol_lookup.lookup({"query": "not-a-sigil-symbol"})


class SigilPracticePlannerTests(unittest.TestCase):
    def test_planner_combines_elements_and_activation_mode(self):
        result = sigil_practice_planner.plan(
            {
                "question_text": "想做一个 sigil 符号印记当项目专注提醒，只用纸上草稿、圆形和钥匙符号、放笔记本一周后复盘，不用血不刻皮肤不纹身不烧不召唤不驱邪不诅咒不操控别人不保证实现不高价购买不反复画",
                "intention_text": "我把今天的项目下一步写清楚",
                "symbol_elements": "圆形, 钥匙, 字母合并",
                "source_context": "user_created_paper_draft",
                "medium": "纸上草稿",
                "activation_mode": "日志激活",
                "display_location": "笔记本",
                "duration": "一周后复盘",
                "focus": "project_focus_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("circle", symbol_codes)
        self.assertIn("key", symbol_codes)
        self.assertIn("letter_bind", symbol_codes)
        self.assertIn("journal_activation", symbol_codes)
        self.assertEqual(result["practice_plan"]["symbol_count"], 4)

    def test_unknown_custom_symbol_does_not_invent_claims(self):
        result = sigil_practice_planner.plan(
            {
                "question_text": "想记录一个自创 sigil 的私人联想",
                "intention_text": "整理下一步",
                "symbol_elements": "月影折线",
                "medium": "纸上草稿",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_custom_sigil_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造召唤", unknown_items[0]["action_guidance"])

    def test_planner_blocks_unsafe_body_fire_summoning_request(self):
        result = sigil_practice_planner.plan(
            {
                "question_text": "我要滴血割手把符号刻皮肤上并做成纹身再焚烧召唤恶魔驱邪，诅咒前任让她回来，保证实现暴富彩票，不用医生不用律师，必须买高价课程，每天画到灵",
                "symbol_elements": "圆形",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_sigil"])
        self.assertIn("blood_or_body_harm", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class DowsingRequestGuardTests(unittest.TestCase):
    def test_low_risk_dowsing_can_continue(self):
        result = dowsing_request_guard.guard({"request_text": "想用占杖探测棒做低风险空间象征，观察自己书房入口和桌面动线，记录双杆交叉和路线提示，只做整理复盘，不找地下水不挖不打井不替代专业探测不定位别人不驱邪不高价购买不反复探"})
        self.assertTrue(result["can_continue_dowsing"])
        self.assertEqual(result["consultation_intent"], "dowsing_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_utility_water_medical_property_privacy_purchase_dependency_request_is_blocked(self):
        result = dowsing_request_guard.guard({"request_text": "用寻水杖准确定位地下水和燃气管，明天开挖打井，还能诊断地气病，不用工程师不用医生，用它决定买房签合同，偷偷进邻居家定位某人并驱邪，买高价占杖课程，每天探到准"})
        self.assertFalse(result["can_continue_dowsing"])
        self.assertIn("utility_or_digging_safety", result["risk_flags"])
        self.assertIn("water_or_resource_guarantee", result["risk_flags"])
        self.assertIn("medical_or_geopathic_claim", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("property_or_legal_decision", result["risk_flags"])
        self.assertIn("trespass_or_privacy", result["risk_flags"])
        self.assertIn("spirit_fear_or_exorcism", result["risk_flags"])
        self.assertIn("financial_or_purchase_pressure", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class DowsingContextRecorderTests(unittest.TestCase):
    def test_records_safe_dowsing_context(self):
        result = dowsing_context_recorder.record(
            {
                "question_text": "想用占杖探测棒做低风险空间象征，观察自己书房入口和桌面动线，记录双杆交叉和路线提示，只做整理复盘，不找地下水不挖不打井不替代专业探测不定位别人不驱邪不高价购买不反复探",
                "tool_type": "L-rods",
                "observation_target": "书房入口和桌面动线",
                "space_or_map": "本人书房",
                "movement_notes": "双杆交叉, 路线",
                "authorization_context": "self_authorized_space",
                "focus": "workspace_flow_reflection",
                "safety_context": "不挖掘, 不施工, 不定位他人",
                "reality_constraints": "不购买, 不替代专业探测",
                "duration": "十分钟后停止",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["movement_notes"], ["双杆交叉", "路线"])
        self.assertEqual(result["space_or_map"], "本人书房")
        self.assertFalse(result["missing_fields"])

    def test_missing_space_and_movements_are_marked(self):
        result = dowsing_context_recorder.record({"question_text": "想做占杖象征记录", "observation_target": "书桌"})
        self.assertTrue(result["is_valid"])
        self.assertIn("space_or_map", result["missing_fields"])
        self.assertIn("movement_notes", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = dowsing_context_recorder.record(
            {
                "question_text": "用寻水杖准确定位地下水和燃气管，明天开挖打井，还能诊断地气病，不用工程师不用医生，用它决定买房签合同，偷偷进邻居家定位某人并驱邪，买高价占杖课程，每天探到准",
                "movement_notes": "双杆交叉",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("utility_or_digging_safety", result["risk_flags"])


class DowsingSymbolLookupTests(unittest.TestCase):
    def test_crossing_rods_lookup_keeps_location_boundary(self):
        result = dowsing_symbol_lookup.lookup({"query": "双杆交叉", "focus": "workspace_flow_reflection"})
        self.assertEqual(result["symbol_code"], "crossing_rods")
        self.assertIn("交点", result["keywords"])
        self.assertIn("不写成准确定位", result["action_guidance"])

    def test_path_alias_normalizes(self):
        result = dowsing_symbol_lookup.lookup({"query": "路线"})
        self.assertEqual(result["symbol_code"], "path")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            dowsing_symbol_lookup.lookup({"query": "not-a-dowsing-symbol"})


class DowsingPracticePlannerTests(unittest.TestCase):
    def test_planner_combines_movements_target_and_space(self):
        result = dowsing_practice_planner.plan(
            {
                "question_text": "想用占杖探测棒做低风险空间象征，观察自己书房入口和桌面动线，记录双杆交叉和路线提示，只做整理复盘，不找地下水不挖不打井不替代专业探测不定位别人不驱邪不高价购买不反复探",
                "tool_type": "L-rods",
                "observation_target": "路线",
                "space_or_map": "入口",
                "movement_notes": "双杆交叉, 路线",
                "authorization_context": "self_authorized_space",
                "focus": "workspace_flow_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("crossing_rods", symbol_codes)
        self.assertIn("path", symbol_codes)
        self.assertIn("threshold", symbol_codes)
        self.assertEqual(result["practice_plan"]["symbol_count"], 4)

    def test_unknown_custom_movement_does_not_invent_claims(self):
        result = dowsing_practice_planner.plan(
            {
                "question_text": "想记录一次自创占杖动作的私人联想",
                "observation_target": "路线",
                "space_or_map": "本人书桌",
                "movement_notes": "月影抖动",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_custom_dowsing_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造地下管线", unknown_items[0]["action_guidance"])

    def test_planner_blocks_unsafe_utility_water_request(self):
        result = dowsing_practice_planner.plan(
            {
                "question_text": "用寻水杖准确定位地下水和燃气管，明天开挖打井，还能诊断地气病，不用工程师不用医生，用它决定买房签合同，偷偷进邻居家定位某人并驱邪，买高价占杖课程，每天探到准",
                "movement_notes": "双杆交叉",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_dowsing"])
        self.assertIn("utility_or_digging_safety", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class BodyOmenRequestGuardTests(unittest.TestCase):
    def test_low_risk_body_omen_can_continue(self):
        result = body_omen_request_guard.guard({"request_text": "左眼跳了一下，想按身体征兆民俗做低风险记录，只当休息和节奏提醒，不诊断不替代医生不买彩票不判断别人不驱邪不反复查"})
        self.assertTrue(result["can_continue_body_omen"])
        self.assertEqual(result["consultation_intent"], "body_omen_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_medical_disaster_financial_third_party_spirit_harm_dependency_request_is_blocked(self):
        result = body_omen_request_guard.guard({"request_text": "右眼跳一定有血光之灾，我胸痛呼吸困难也不用医生，今晚按这个买彩票梭哈股票，判断前任耳鸣是不是中邪，按眼球放血，每天查到安心"})
        self.assertFalse(result["can_continue_body_omen"])
        self.assertIn("medical_red_flag", result["risk_flags"])
        self.assertIn("medical_replacement", result["risk_flags"])
        self.assertIn("deterministic_disaster_claim", result["risk_flags"])
        self.assertIn("financial_or_gambling_timing", result["risk_flags"])
        self.assertIn("third_party_body_label", result["risk_flags"])
        self.assertIn("spirit_fear_or_exorcism", result["risk_flags"])
        self.assertIn("body_harm_or_unsafe_test", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class BodyOmenContextRecorderTests(unittest.TestCase):
    def test_records_safe_body_omen_context(self):
        result = body_omen_context_recorder.record(
            {
                "question_text": "左眼跳了一下，想按身体征兆民俗做低风险记录，只当休息和节奏提醒，不诊断不替代医生不买彩票不判断别人不驱邪不反复查",
                "omen_type": "左眼跳",
                "body_location": "左眼",
                "timing": "下午工作间隙",
                "duration": "几秒",
                "sensation_notes": "轻微跳动",
                "health_context": "没有疼痛或视力变化",
                "mundane_context": "久看屏幕, 睡眠不足",
                "focus": "rest_and_rhythm_reflection",
                "stop_condition": "记录一次后停止",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["sensation_notes"], ["轻微跳动"])
        self.assertEqual(result["body_location"], "左眼")
        self.assertFalse(result["missing_fields"])

    def test_missing_timing_and_sensations_are_marked(self):
        result = body_omen_context_recorder.record({"question_text": "想记录左眼跳民俗象征", "omen_type": "左眼跳", "body_location": "左眼"})
        self.assertTrue(result["is_valid"])
        self.assertIn("timing", result["missing_fields"])
        self.assertIn("sensation_notes", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = body_omen_context_recorder.record(
            {
                "question_text": "右眼跳一定有血光之灾，我胸痛呼吸困难也不用医生，今晚按这个买彩票梭哈股票，判断前任耳鸣是不是中邪，按眼球放血，每天查到安心",
                "omen_type": "右眼跳",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("medical_red_flag", result["risk_flags"])


class BodyOmenSymbolLookupTests(unittest.TestCase):
    def test_left_eye_lookup_keeps_medical_boundary(self):
        result = body_omen_symbol_lookup.lookup({"query": "左眼跳", "focus": "rest_and_rhythm_reflection"})
        self.assertEqual(result["symbol_code"], "left_eye_twitch")
        self.assertIn("疲劳", result["keywords"])
        self.assertIn("不写成发财", result["action_guidance"])

    def test_sneeze_alias_normalizes(self):
        result = body_omen_symbol_lookup.lookup({"query": "打喷嚏"})
        self.assertEqual(result["symbol_code"], "sneeze")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            body_omen_symbol_lookup.lookup({"query": "not-a-body-omen-symbol"})


class BodyOmenReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_signal_location_sensation_and_timing(self):
        result = body_omen_reflection_planner.plan(
            {
                "question_text": "左眼跳了一下，想按身体征兆民俗做低风险记录，只当休息和节奏提醒，不诊断不替代医生不买彩票不判断别人不驱邪不反复查",
                "omen_type": "左眼跳",
                "body_location": "左眼",
                "timing": "下午工作间隙",
                "duration": "几秒",
                "sensation_notes": "轻微跳动",
                "health_context": "没有疼痛或视力变化",
                "mundane_context": "久看屏幕, 睡眠不足",
                "focus": "rest_and_rhythm_reflection",
                "stop_condition": "记录一次后停止",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("left_eye_twitch", symbol_codes)
        self.assertIn("time_slot", symbol_codes)
        self.assertIn("unknown_or_custom_body_omen_symbol", symbol_codes)
        self.assertEqual(result["reflection_plan"]["symbol_count"], 4)

    def test_unknown_custom_signal_does_not_invent_claims(self):
        result = body_omen_reflection_planner.plan(
            {
                "question_text": "想记录一次自定义身体征兆的私人联想",
                "omen_type": "肩膀发热",
                "body_location": "肩膀",
                "timing": "晚上",
                "sensation_notes": "发热",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_custom_body_omen_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造疾病", unknown_items[0]["action_guidance"])

    def test_planner_blocks_unsafe_medical_disaster_request(self):
        result = body_omen_reflection_planner.plan(
            {
                "question_text": "右眼跳一定有血光之灾，我胸痛呼吸困难也不用医生，今晚按这个买彩票梭哈股票，判断前任耳鸣是不是中邪，按眼球放血，每天查到安心",
                "omen_type": "右眼跳",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_body_omen"])
        self.assertIn("medical_red_flag", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class ScryingRequestGuardTests(unittest.TestCase):
    def test_low_risk_short_observation_can_continue(self):
        result = scrying_request_guard.guard({"request_text": "我短时看了水晶球，已经结束，看到像门和波纹，想做项目推进的低风险提醒"})
        self.assertTrue(result["can_continue_scrying"])
        self.assertEqual(result["consultation_intent"], "scrying_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_trance_spirit_third_party_request_is_blocked(self):
        result = scrying_request_guard.guard({"request_text": "教我通宵盯黑镜直到看到灵体，看看前任现在真实想法，让他回来，不用医生"})
        self.assertFalse(result["can_continue_scrying"])
        self.assertIn("unsafe_trance_or_staring", result["risk_flags"])
        self.assertIn("spirit_fear_claim", result["risk_flags"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("coercion_or_control", result["risk_flags"])

    def test_identity_label_is_blocked(self):
        result = scrying_request_guard.guard({"request_text": "看照片和镜面判断这个人是不是有邪气、长得命苦"})
        self.assertFalse(result["can_continue_scrying"])
        self.assertIn("identity_or_body_label", result["risk_flags"])


class ScryingObservationRecorderTests(unittest.TestCase):
    def test_records_safe_scrying_observation(self):
        result = scrying_observation_recorder.record(
            {
                "question_text": "我短时看了水晶球，已经结束，看到像门和波纹，想做项目推进的低风险提醒",
                "observation_source": "user_described",
                "observation_state": "short_completed",
                "medium": "crystal_ball",
                "visual_notes": "门 波纹",
                "focus": "project_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["visual_notes"], ["门", "波纹"])
        self.assertEqual(result["medium"], "crystal_ball")
        self.assertEqual(result["observation_state"], "short_completed")
        self.assertFalse(result["missing_fields"])

    def test_invalid_observation_state_is_marked_missing(self):
        result = scrying_observation_recorder.record(
            {
                "question_text": "想记录短时结束后的镜面观察",
                "observation_state": "still_staring",
                "medium": "mirror",
                "visual_notes": "门",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertIn("safe_observation_state", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = scrying_observation_recorder.record(
            {
                "question_text": "教我通宵盯黑镜直到看到灵体，看看前任现在真实想法，让他回来，不用医生",
                "medium": "black_mirror",
                "visual_notes": "影子",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("unsafe_trance_or_staring", result["risk_flags"])


class ScryingSymbolLookupTests(unittest.TestCase):
    def test_door_lookup_keeps_prediction_boundary(self):
        result = scrying_symbol_lookup.lookup({"query": "门", "focus": "project_reflection"})
        self.assertEqual(result["canonical_name"], "门")
        self.assertEqual(result["symbol_code"], "door")
        self.assertIn("入口", result["keywords"])
        self.assertIn("不承诺机会必然打开", result["action_guidance"])

    def test_wave_alias_normalizes(self):
        result = scrying_symbol_lookup.lookup({"query": "水纹"})
        self.assertEqual(result["symbol_code"], "wave")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            scrying_symbol_lookup.lookup({"query": "not-a-scrying-symbol"})


class ScryingInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_observation_and_symbols(self):
        result = scrying_interpretation_planner.plan(
            {
                "question_text": "我短时看了水晶球，已经结束，看到像门和波纹，想做项目推进的低风险提醒",
                "observation_source": "user_described",
                "observation_state": "short_completed",
                "medium": "crystal_ball",
                "visual_notes": "门 波纹",
                "focus": "project_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 2)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("door", symbol_codes)
        self.assertIn("wave", symbol_codes)

    def test_unknown_observation_does_not_invent_meaning(self):
        result = scrying_interpretation_planner.plan(
            {
                "question_text": "想记录照片里的镜面形状",
                "observation_state": "photo_notes",
                "medium": "photo_notes",
                "visual_notes": "星门形",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_ambiguous_scrying_observation")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_trance_spirit_third_party(self):
        result = scrying_interpretation_planner.plan(
            {
                "question_text": "教我通宵盯黑镜直到看到灵体，看看前任现在真实想法，让他回来，不用医生",
                "medium": "black_mirror",
                "visual_notes": "影子",
                "focus": "spirit",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_scrying"])
        self.assertIn("unsafe_trance_or_staring", result["risk_flags"])


class CastingLotsRequestGuardTests(unittest.TestCase):
    def test_low_risk_casting_lots_can_continue(self):
        result = casting_lots_request_guard.guard({"request_text": "我用贝壳、钥匙和石子做了一次小物抛掷，想看项目协作的低风险提醒"})
        self.assertTrue(result["can_continue_casting_lots"])
        self.assertEqual(result["consultation_intent"], "casting_lots_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_remains_spirit_control_request_is_blocked(self):
        result = casting_lots_request_guard.guard({"request_text": "教我用人骨和血做撒骨驱邪，确认前任是不是被诅咒，让他回来，不用医生，抛到满意为止"})
        self.assertFalse(result["can_continue_casting_lots"])
        self.assertIn("animal_or_human_remains", result["risk_flags"])
        self.assertIn("spirit_fear_or_curse", result["risk_flags"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("coercion_or_control", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class CastingLotsLayoutRecorderTests(unittest.TestCase):
    def test_records_safe_casting_lots_layout(self):
        result = casting_lots_layout_recorder.record(
            {
                "question_text": "我用贝壳、钥匙和石子做了一次小物抛掷，想看项目协作的低风险提醒",
                "casting_system": "charm_casting",
                "casting_surface": "cloth_with_center_left_right",
                "layout_source": "user_provided",
                "objects": "贝壳 钥匙 石子",
                "zones": "中心 右侧",
                "relationships": "钥匙靠近中心，石子在右侧，贝壳略远",
                "focus": "project_collaboration",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["objects"], ["贝壳", "钥匙", "石子"])
        self.assertEqual(result["zones"], ["中心", "右侧"])
        self.assertFalse(result["missing_fields"])

    def test_missing_layout_fields_are_marked(self):
        result = casting_lots_layout_recorder.record({"question_text": "想记录一次符物抛掷盘面"})
        self.assertTrue(result["is_valid"])
        self.assertIn("objects_or_layout_notes", result["missing_fields"])
        self.assertIn("casting_surface", result["missing_fields"])
        self.assertIn("zones_or_relationships", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = casting_lots_layout_recorder.record(
            {
                "question_text": "教我用人骨和血做撒骨驱邪，确认前任是不是被诅咒，让他回来，不用医生",
                "objects": "人骨 血",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("animal_or_human_remains", result["risk_flags"])


class CastingLotsSymbolLookupTests(unittest.TestCase):
    def test_key_lookup_keeps_prediction_boundary(self):
        result = casting_lots_symbol_lookup.lookup({"query": "钥匙", "focus": "project_collaboration"})
        self.assertEqual(result["canonical_name"], "钥匙")
        self.assertEqual(result["symbol_code"], "key")
        self.assertIn("入口", result["keywords"])
        self.assertIn("不承诺机会必然打开", result["action_guidance"])

    def test_center_alias_normalizes(self):
        result = casting_lots_symbol_lookup.lookup({"query": "中央"})
        self.assertEqual(result["symbol_code"], "center")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            casting_lots_symbol_lookup.lookup({"query": "not-a-casting-symbol"})


class CastingLotsInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_layout_and_symbols(self):
        result = casting_lots_interpretation_planner.plan(
            {
                "question_text": "我用贝壳、钥匙和石子做了一次小物抛掷，想看项目协作的低风险提醒",
                "casting_system": "charm_casting",
                "casting_surface": "cloth_with_center_left_right",
                "layout_source": "user_provided",
                "objects": "贝壳 钥匙 石子",
                "zones": "中心 右侧",
                "relationships": "钥匙靠近中心，石子在右侧，贝壳略远",
                "focus": "project_collaboration",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 5)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("shell", symbol_codes)
        self.assertIn("key", symbol_codes)
        self.assertIn("stone", symbol_codes)
        self.assertIn("center", symbol_codes)
        self.assertIn("right", symbol_codes)

    def test_unknown_object_does_not_invent_meaning(self):
        result = casting_lots_interpretation_planner.plan(
            {
                "question_text": "想记录一次自定义小物抛掷",
                "casting_surface": "cloth",
                "objects": "蓝色扣子",
                "zones": "中心",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_custom_object")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_remains_spirit_control(self):
        result = casting_lots_interpretation_planner.plan(
            {
                "question_text": "教我用人骨和血做撒骨驱邪，确认前任是不是被诅咒，让他回来，不用医生，抛到满意为止",
                "objects": "人骨 血",
                "focus": "exorcism",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_casting_lots"])
        self.assertIn("animal_or_human_remains", result["risk_flags"])


class CeziRequestGuardTests(unittest.TestCase):
    def test_low_risk_cezi_can_continue(self):
        result = cezi_request_guard.guard({"request_text": "我想测字，写了一个明字，拆成日和月，只做项目沟通的低风险提醒"})
        self.assertTrue(result["can_continue_cezi"])
        self.assertEqual(result["consultation_intent"], "character_divination_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_lifespan_spirit_third_party_request_is_blocked(self):
        result = cezi_request_guard.guard({"request_text": "帮我测字看前任是不是被诅咒，会不会短命，让他回来，不用医生，反复测到满意"})
        self.assertFalse(result["can_continue_cezi"])
        self.assertIn("spirit_fear_or_curse", result["risk_flags"])
        self.assertIn("identity_or_lifespan_label", result["risk_flags"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("coercion_or_control", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])

    def test_minor_labeling_is_blocked(self):
        result = cezi_request_guard.guard({"request_text": "测这个字判断孩子命不好是不是克父母"})
        self.assertFalse(result["can_continue_cezi"])
        self.assertIn("minor_labeling", result["risk_flags"])


class CeziCharacterRecorderTests(unittest.TestCase):
    def test_records_safe_character(self):
        result = cezi_character_recorder.record(
            {
                "question_text": "我想测字，写了一个明字，拆成日和月，只做项目沟通的低风险提醒",
                "character": "明",
                "character_source": "user_provided",
                "components": "日 月",
                "visible_features": "左右结构",
                "user_association": "看见清晰和节奏",
                "focus": "project_communication",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["character"], "明")
        self.assertEqual(result["components"], ["日", "月"])
        self.assertEqual(result["visible_features"], ["左右结构"])
        self.assertFalse(result["missing_fields"])

    def test_missing_character_fields_are_marked(self):
        result = cezi_character_recorder.record({"question_text": "想记录一次测字"})
        self.assertTrue(result["is_valid"])
        self.assertIn("character", result["missing_fields"])
        self.assertIn("components_or_features_or_user_association", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = cezi_character_recorder.record(
            {
                "question_text": "帮我测字看前任是不是被诅咒，会不会短命，让他回来，不用医生",
                "character": "咒",
                "components": "口",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("spirit_fear_or_curse", result["risk_flags"])


class CeziSymbolLookupTests(unittest.TestCase):
    def test_sun_lookup_keeps_prediction_boundary(self):
        result = cezi_symbol_lookup.lookup({"query": "日", "focus": "project_communication"})
        self.assertEqual(result["canonical_name"], "日")
        self.assertEqual(result["symbol_code"], "sun")
        self.assertIn("可见", result["keywords"])
        self.assertIn("不承诺具体日期或结果", result["action_guidance"])

    def test_left_right_alias_normalizes(self):
        result = cezi_symbol_lookup.lookup({"query": "左右结构"})
        self.assertEqual(result["symbol_code"], "left_right")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            cezi_symbol_lookup.lookup({"query": "not-a-cezi-symbol"})


class CeziInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_character_and_symbols(self):
        result = cezi_interpretation_planner.plan(
            {
                "question_text": "我想测字，写了一个明字，拆成日和月，只做项目沟通的低风险提醒",
                "character": "明",
                "character_source": "user_provided",
                "components": "日 月",
                "visible_features": "左右结构",
                "user_association": "看见清晰和节奏",
                "focus": "project_communication",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 3)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("sun", symbol_codes)
        self.assertIn("moon", symbol_codes)
        self.assertIn("unknown_or_custom_character_feature", symbol_codes)

    def test_unknown_feature_does_not_invent_meaning(self):
        result = cezi_interpretation_planner.plan(
            {
                "question_text": "想记录一次测字",
                "character": "玄",
                "components": "玄妙感",
                "user_association": "",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_custom_character_feature")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_lifespan_spirit_third_party(self):
        result = cezi_interpretation_planner.plan(
            {
                "question_text": "帮我测字看前任是不是被诅咒，会不会短命，让他回来，不用医生，反复测到满意",
                "character": "咒",
                "components": "口",
                "focus": "curse",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_cezi"])
        self.assertIn("identity_or_lifespan_label", result["risk_flags"])


class FlowerRequestGuardTests(unittest.TestCase):
    def test_low_risk_flower_request_can_continue(self):
        result = flower_request_guard.guard({"request_text": "想用花语选一束向日葵和白色百合送给同事，只做感谢和边界表达，不买贵的"})
        self.assertTrue(result["can_continue_flower"])
        self.assertEqual(result["consultation_intent"], "flower_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_healing_pet_purchase_request_is_blocked(self):
        result = flower_request_guard.guard({"request_text": "帮我用花语治焦虑，不用医生，猫能吃百合吗？大师说必须买天价花束才能驱邪转运"})
        self.assertFalse(result["can_continue_flower"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("medical_healing_claim", result["risk_flags"])
        self.assertIn("allergy_or_toxicity", result["risk_flags"])
        self.assertIn("spirit_fear_claim", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])


class FlowerItemRecorderTests(unittest.TestCase):
    def test_records_safe_flower_context(self):
        result = flower_item_recorder.record(
            {
                "intention_text": "想用花语选一束向日葵和白色百合送给同事，只做感谢和边界表达，不买贵的",
                "flowers": "向日葵 百合",
                "colors": "白色",
                "scene": "gift",
                "recipient": "同事",
                "budget_note": "不买贵的",
                "safety_constraints": "确认对方不过敏，办公室不放浓香",
                "focus": "thanks_and_boundaries",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["flowers"], ["向日葵", "百合"])
        self.assertEqual(result["colors"], ["白色"])
        self.assertFalse(result["missing_fields"])

    def test_missing_flowers_are_marked(self):
        result = flower_item_recorder.record({"intention_text": "想了解花语"})
        self.assertTrue(result["is_valid"])
        self.assertIn("flowers_or_items", result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = flower_item_recorder.record(
            {
                "intention_text": "帮我用花语治焦虑，不用医生，猫能吃百合吗？大师说必须买天价花束才能驱邪转运",
                "flowers": "百合",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("allergy_or_toxicity", result["risk_flags"])


class FlowerSymbolLookupTests(unittest.TestCase):
    def test_sunflower_lookup_keeps_prediction_boundary(self):
        result = flower_symbol_lookup.lookup({"query": "向日葵", "focus": "thanks_and_boundaries"})
        self.assertEqual(result["canonical_name"], "向日葵")
        self.assertEqual(result["symbol_code"], "sunflower")
        self.assertIn("方向", result["keywords"])
        self.assertIn("不承诺成功或好运必来", result["action_guidance"])

    def test_white_alias_normalizes(self):
        result = flower_symbol_lookup.lookup({"query": "白色"})
        self.assertEqual(result["symbol_code"], "white")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            flower_symbol_lookup.lookup({"query": "not-a-flower-symbol"})


class FlowerInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_flowers_and_colors(self):
        result = flower_interpretation_planner.plan(
            {
                "intention_text": "想用花语选一束向日葵和白色百合送给同事，只做感谢和边界表达，不买贵的",
                "flowers": "向日葵 百合",
                "colors": "白色",
                "scene": "gift",
                "recipient": "同事",
                "budget_note": "不买贵的",
                "safety_constraints": "确认对方不过敏，办公室不放浓香",
                "focus": "thanks_and_boundaries",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 3)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("sunflower", symbol_codes)
        self.assertIn("lily", symbol_codes)
        self.assertIn("white", symbol_codes)

    def test_unknown_flower_does_not_invent_meaning(self):
        result = flower_interpretation_planner.plan(
            {
                "intention_text": "想记录一束地方花材的花语",
                "flowers": "蓝星花",
                "scene": "reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_local_flower")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_healing_pet_purchase(self):
        result = flower_interpretation_planner.plan(
            {
                "intention_text": "帮我用花语治焦虑，不用医生，猫能吃百合吗？大师说必须买天价花束才能驱邪转运",
                "flowers": "百合",
                "scene": "healing",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_flower"])
        self.assertIn("allergy_or_toxicity", result["risk_flags"])


class AnimalOmenRequestGuardTests(unittest.TestCase):
    def test_low_risk_animal_omen_request_can_continue(self):
        result = animal_omen_request_guard.guard({"request_text": "早上有一只鸟飞进阳台又飞走了，想了解民俗象征，只做低风险观察反思"})
        self.assertTrue(result["can_continue_animal_omen"])
        self.assertEqual(result["consultation_intent"], "animal_omen_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_harm_pest_spirit_request_is_blocked(self):
        result = animal_omen_request_guard.guard({"request_text": "家里有蝙蝠和老鼠，是不是必有大祸？我要徒手抓来做法驱邪，毒死它们，不用物业和疾控"})
        self.assertFalse(result["can_continue_animal_omen"])
        self.assertIn("animal_harm", result["risk_flags"])
        self.assertIn("public_health_or_pest", result["risk_flags"])
        self.assertIn("dangerous_handling", result["risk_flags"])
        self.assertIn("deterministic_disaster", result["risk_flags"])
        self.assertIn("spirit_fear_claim", result["risk_flags"])


class AnimalOmenObservationRecorderTests(unittest.TestCase):
    def test_records_safe_observation_context(self):
        result = animal_omen_observation_recorder.record(
            {
                "observation_text": "早上有一只鸟飞进阳台又飞走了，想了解民俗象征，只做低风险观察反思",
                "animals": "鸟",
                "behavior": "飞进阳台又飞走",
                "location": "阳台",
                "timing": "早上",
                "safety_context": "没有接触或受伤动物",
                "focus": "home_boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["animals"], ["鸟"])
        self.assertEqual(result["behavior"], "飞进阳台又飞走")
        self.assertFalse(result["missing_fields"])

    def test_missing_observation_fields_are_marked(self):
        result = animal_omen_observation_recorder.record({"observation_text": "想了解动物征兆"})
        self.assertTrue(result["is_valid"])
        self.assertIn("animals", result["missing_fields"])
        self.assertIn("behavior", result["missing_fields"])
        self.assertIn("location", result["missing_fields"])

    def test_blocked_observation_cannot_record_as_valid(self):
        result = animal_omen_observation_recorder.record(
            {
                "observation_text": "家里有蝙蝠和老鼠，是不是必有大祸？我要徒手抓来做法驱邪，毒死它们，不用物业和疾控",
                "animals": "蝙蝠 老鼠",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("public_health_or_pest", result["risk_flags"])


class AnimalOmenSymbolLookupTests(unittest.TestCase):
    def test_bird_lookup_keeps_disaster_boundary(self):
        result = animal_omen_symbol_lookup.lookup({"query": "鸟", "focus": "home_boundary_reflection"})
        self.assertEqual(result["canonical_name"], "鸟")
        self.assertEqual(result["symbol_code"], "bird")
        self.assertIn("消息", result["keywords"])
        self.assertIn("不把鸟类出现写成死亡", result["action_guidance"])

    def test_crow_alias_normalizes(self):
        result = animal_omen_symbol_lookup.lookup({"query": "乌鸦叫"})
        self.assertEqual(result["symbol_code"], "crow")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            animal_omen_symbol_lookup.lookup({"query": "not-an-animal-symbol"})


class AnimalOmenInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_observation_and_symbol(self):
        result = animal_omen_interpretation_planner.plan(
            {
                "observation_text": "早上有一只鸟飞进阳台又飞走了，想了解民俗象征，只做低风险观察反思",
                "animals": "鸟",
                "behavior": "飞进阳台又飞走",
                "location": "阳台",
                "timing": "早上",
                "safety_context": "没有接触或受伤动物",
                "focus": "home_boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 1)
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "bird")
        self.assertIn("现实处理", result["omen_plan"]["practical_steps"][2])

    def test_unknown_animal_does_not_invent_meaning(self):
        result = animal_omen_interpretation_planner.plan(
            {
                "observation_text": "看到一种不确定的地方动物，想做文化记录",
                "animals": "蓝尾小兽",
                "behavior": "路过",
                "location": "院子",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_local_animal")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_harm_pest_spirit(self):
        result = animal_omen_interpretation_planner.plan(
            {
                "observation_text": "家里有蝙蝠和老鼠，是不是必有大祸？我要徒手抓来做法驱邪，毒死它们，不用物业和疾控",
                "animals": "蝙蝠 老鼠",
                "behavior": "进屋",
                "location": "家里",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_animal_omen"])
        self.assertIn("public_health_or_pest", result["risk_flags"])


class AuraChakraRequestGuardTests(unittest.TestCase):
    def test_low_risk_aura_chakra_request_can_continue(self):
        result = aura_chakra_request_guard.guard({"request_text": "冥想时感觉喉轮有点堵，看到蓝色，只想做低风险记录和表达边界反思"})
        self.assertTrue(result["can_continue_aura_chakra"])
        self.assertEqual(result["consultation_intent"], "aura_chakra_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_medical_spirit_purchase_request_is_blocked(self):
        result = aura_chakra_request_guard.guard({"request_text": "我胸痛失眠还幻听，是不是被能量攻击附身？不用医生，必须买大师天价远程清理才能治好焦虑吗"})
        self.assertFalse(result["can_continue_aura_chakra"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("medical_or_mental_health", result["risk_flags"])
        self.assertIn("spirit_attack_claim", result["risk_flags"])
        self.assertIn("expensive_healing_pressure", result["risk_flags"])


class AuraChakraSensationRecorderTests(unittest.TestCase):
    def test_records_safe_sensation_context(self):
        result = aura_chakra_sensation_recorder.record(
            {
                "sensation_text": "冥想时感觉喉轮有点堵，看到蓝色，只想做低风险记录和表达边界反思",
                "centers": "喉轮",
                "colors": "蓝色",
                "sensations": "堵",
                "context": "meditation_journaling",
                "duration": "几分钟",
                "intensity": "轻微",
                "grounding_notes": "没有疼痛或呼吸困难，会先喝水休息",
                "focus": "expression_boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["centers"], ["喉轮"])
        self.assertEqual(result["colors"], ["蓝色"])
        self.assertEqual(result["sensations"], ["堵"])
        self.assertFalse(result["missing_fields"])

    def test_missing_sensation_fields_are_marked(self):
        result = aura_chakra_sensation_recorder.record({"sensation_text": "想了解气场"})
        self.assertTrue(result["is_valid"])
        self.assertIn("centers_colors_or_sensations", result["missing_fields"])

    def test_blocked_sensation_cannot_record_as_valid(self):
        result = aura_chakra_sensation_recorder.record(
            {
                "sensation_text": "我胸痛失眠还幻听，是不是被能量攻击附身？不用医生，必须买大师天价远程清理才能治好焦虑吗",
                "centers": "心轮",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("medical_or_mental_health", result["risk_flags"])


class AuraChakraSymbolLookupTests(unittest.TestCase):
    def test_throat_lookup_keeps_diagnosis_boundary(self):
        result = aura_chakra_symbol_lookup.lookup({"query": "喉轮", "focus": "expression_boundary_reflection"})
        self.assertEqual(result["canonical_name"], "喉轮")
        self.assertEqual(result["symbol_code"], "throat")
        self.assertIn("表达", result["keywords"])
        self.assertIn("不把沉默或表达困难诊断成疾病", result["action_guidance"])

    def test_blue_alias_normalizes(self):
        result = aura_chakra_symbol_lookup.lookup({"query": "蓝色"})
        self.assertEqual(result["symbol_code"], "blue")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            aura_chakra_symbol_lookup.lookup({"query": "not-an-energy-symbol"})


class AuraChakraReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_center_color_and_sensation(self):
        result = aura_chakra_reflection_planner.plan(
            {
                "sensation_text": "冥想时感觉喉轮有点堵，看到蓝色，只想做低风险记录和表达边界反思",
                "centers": "喉轮",
                "colors": "蓝色",
                "sensations": "堵",
                "context": "meditation_journaling",
                "duration": "几分钟",
                "intensity": "轻微",
                "grounding_notes": "没有疼痛或呼吸困难，会先喝水休息",
                "focus": "expression_boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 3)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("throat", symbol_codes)
        self.assertIn("blue", symbol_codes)
        self.assertIn("unknown_or_personal_energy_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_meaning(self):
        result = aura_chakra_reflection_planner.plan(
            {
                "sensation_text": "想记录一种课程里说的金色能量感",
                "colors": "金色",
                "context": "journaling",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_personal_energy_symbol")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_medical_spirit_purchase(self):
        result = aura_chakra_reflection_planner.plan(
            {
                "sensation_text": "我胸痛失眠还幻听，是不是被能量攻击附身？不用医生，必须买大师天价远程清理才能治好焦虑吗",
                "centers": "心轮 顶轮",
                "sensations": "胸痛",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_aura_chakra"])
        self.assertIn("medical_or_mental_health", result["risk_flags"])


class PastLifeRequestGuardTests(unittest.TestCase):
    def test_low_risk_past_life_request_can_continue(self):
        result = past_life_request_guard.guard({"request_text": "冥想里出现阿卡西图书馆和一扇门，只想做象征记录和当下边界反思，不当成真实前世记忆"})
        self.assertTrue(result["can_continue_past_life"])
        self.assertEqual(result["consultation_intent"], "past_life_akashic_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_hypnosis_trauma_medical_purchase_request_is_blocked(self):
        result = past_life_request_guard.guard({"request_text": "我要催眠找回被封印的前世创伤，确认是谁害了我；不用心理咨询，必须买大师天价疗愈才能治好焦虑"})
        self.assertFalse(result["can_continue_past_life"])
        self.assertIn("memory_recovery_or_hypnosis", result["risk_flags"])
        self.assertIn("trauma_or_abuse_confirmation", result["risk_flags"])
        self.assertIn("medical_or_mental_health", result["risk_flags"])
        self.assertIn("expensive_session_pressure", result["risk_flags"])


class PastLifeNarrativeRecorderTests(unittest.TestCase):
    def test_records_safe_narrative_context(self):
        result = past_life_narrative_recorder.record(
            {
                "narrative_text": "冥想里出现阿卡西图书馆和一扇门，只想做象征记录和当下边界反思，不当成真实前世记忆",
                "scenes": "图书馆",
                "roles": "观察者",
                "symbols": "门",
                "emotions": "好奇",
                "source_context": "meditation_journaling",
                "focus": "boundary_reflection",
                "reality_anchor": "最近在考虑是否接一个新项目",
                "consent_notes": "只谈自己，不读取第三方",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["scenes"], ["图书馆"])
        self.assertEqual(result["symbols"], ["门"])
        self.assertFalse(result["missing_fields"])

    def test_missing_narrative_fields_are_marked(self):
        result = past_life_narrative_recorder.record({"narrative_text": "想了解阿卡西"})
        self.assertTrue(result["is_valid"])
        self.assertIn("scenes_roles_symbols_or_emotions", result["missing_fields"])

    def test_blocked_narrative_cannot_record_as_valid(self):
        result = past_life_narrative_recorder.record(
            {
                "narrative_text": "我要催眠找回被封印的前世创伤，确认是谁害了我；不用心理咨询",
                "scenes": "战场",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("memory_recovery_or_hypnosis", result["risk_flags"])


class PastLifeSymbolLookupTests(unittest.TestCase):
    def test_library_lookup_keeps_fact_boundary(self):
        result = past_life_symbol_lookup.lookup({"query": "图书馆", "focus": "boundary_reflection"})
        self.assertEqual(result["canonical_name"], "图书馆/档案馆")
        self.assertEqual(result["symbol_code"], "library")
        self.assertIn("学习", result["keywords"])
        self.assertIn("不声称进入真实阿卡西记录", result["action_guidance"])

    def test_contract_alias_normalizes(self):
        result = past_life_symbol_lookup.lookup({"query": "灵魂契约"})
        self.assertEqual(result["symbol_code"], "contract")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            past_life_symbol_lookup.lookup({"query": "not-a-past-life-symbol"})


class PastLifeReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_scene_role_symbol_and_emotion(self):
        result = past_life_reflection_planner.plan(
            {
                "narrative_text": "冥想里出现阿卡西图书馆和一扇门，只想做象征记录和当下边界反思，不当成真实前世记忆",
                "scenes": "图书馆",
                "roles": "观察者",
                "symbols": "门",
                "emotions": "好奇",
                "source_context": "meditation_journaling",
                "focus": "boundary_reflection",
                "reality_anchor": "最近在考虑是否接一个新项目",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 4)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("library", symbol_codes)
        self.assertIn("door", symbol_codes)
        self.assertIn("unknown_or_personal_past_life_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_meaning(self):
        result = past_life_reflection_planner.plan(
            {
                "narrative_text": "想记录一个课程里说的蓝色王冠画面",
                "symbols": "蓝色王冠",
                "source_context": "course_journaling",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_personal_past_life_symbol")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_hypnosis_trauma_purchase(self):
        result = past_life_reflection_planner.plan(
            {
                "narrative_text": "我要催眠找回被封印的前世创伤，确认是谁害了我；不用心理咨询，必须买大师天价疗愈才能治好焦虑",
                "scenes": "战场",
                "symbols": "契约",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_past_life"])
        self.assertIn("memory_recovery_or_hypnosis", result["risk_flags"])


class MoonPhaseRequestGuardTests(unittest.TestCase):
    def test_low_risk_new_moon_request_can_continue(self):
        result = moon_phase_request_guard.guard({"request_text": "今晚新月想做无火的意图书写，只整理项目计划和复盘，不保证显化"})
        self.assertTrue(result["can_continue_moon_phase"])
        self.assertEqual(result["consultation_intent"], "moon_phase_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_dangerous_medical_manifestation_purchase_request_is_blocked(self):
        result = moon_phase_request_guard.guard({"request_text": "不用医生，满月烧照片和头发，必须买天价课程才能百分百显化复合并治好失眠"})
        self.assertFalse(result["can_continue_moon_phase"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("medical_or_fertility", result["risk_flags"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("guaranteed_manifestation", result["risk_flags"])
        self.assertIn("expensive_course_pressure", result["risk_flags"])


class MoonPhaseContextRecorderTests(unittest.TestCase):
    def test_records_safe_moon_phase_context(self):
        result = moon_phase_context_recorder.record(
            {
                "context_text": "今晚新月想做无火的意图书写，只整理项目计划和复盘，不保证显化",
                "phases": "新月",
                "themes": "项目计划",
                "intentions": "整理下周行动",
                "practical_constraints": "不熬夜 不买课",
                "date_note": "今晚",
                "source_note": "用户提供的新月日期",
                "focus": "project_cycle_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["phases"], ["新月"])
        self.assertEqual(result["themes"], ["项目计划"])
        self.assertFalse(result["missing_fields"])

    def test_missing_context_fields_are_marked(self):
        result = moon_phase_context_recorder.record({"context_text": "想了解月相", "source_note": "用户自述"})
        self.assertTrue(result["is_valid"])
        self.assertIn("phases_themes_or_intentions", result["missing_fields"])

    def test_blocked_context_cannot_record_as_valid(self):
        result = moon_phase_context_recorder.record(
            {
                "context_text": "不用医生，满月烧照片和头发，必须买天价课程才能百分百显化复合并治好失眠",
                "phases": "满月",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class MoonPhaseSymbolLookupTests(unittest.TestCase):
    def test_new_moon_lookup_keeps_manifestation_boundary(self):
        result = moon_phase_symbol_lookup.lookup({"query": "新月", "focus": "project_cycle_reflection"})
        self.assertEqual(result["canonical_name"], "新月")
        self.assertEqual(result["symbol_code"], "new_moon")
        self.assertIn("开始", result["keywords"])
        self.assertIn("不保证许愿显化", result["action_guidance"])

    def test_full_moon_alias_normalizes(self):
        result = moon_phase_symbol_lookup.lookup({"query": "full moon"})
        self.assertEqual(result["symbol_code"], "full_moon")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            moon_phase_symbol_lookup.lookup({"query": "not-a-moon-symbol"})


class MoonPhaseReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_phase_theme_and_intention(self):
        result = moon_phase_reflection_planner.plan(
            {
                "context_text": "今晚新月想做无火的意图书写，只整理项目计划和复盘，不保证显化",
                "phases": "新月",
                "themes": "项目计划",
                "intentions": "整理下周行动",
                "practical_constraints": "不熬夜 不买课",
                "date_note": "今晚",
                "source_note": "用户提供的新月日期",
                "focus": "project_cycle_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 3)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("new_moon", symbol_codes)
        self.assertIn("unknown_or_source_specific_moon_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_meaning(self):
        result = moon_phase_reflection_planner.plan(
            {
                "context_text": "想记录课程里说的银门月",
                "phases": "银门月",
                "source_note": "课程术语",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_source_specific_moon_symbol")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_dangerous_manifestation_purchase(self):
        result = moon_phase_reflection_planner.plan(
            {
                "context_text": "不用医生，满月烧照片和头发，必须买天价课程才能百分百显化复合并治好失眠",
                "phases": "满月",
                "source_note": "社群课程",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_moon_phase"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class SpiritMessageRequestGuardTests(unittest.TestCase):
    def test_low_risk_higher_self_message_can_continue(self):
        result = spirit_message_request_guard.guard({"request_text": "冥想后像是收到一句高我讯息：先照顾边界。只想做象征写作和现实行动反思"})
        self.assertTrue(result["can_continue_spirit_message"])
        self.assertEqual(result["consultation_intent"], "spirit_message_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_command_voice_medical_purchase_request_is_blocked(self):
        result = spirit_message_request_guard.guard({"request_text": "脑内声音一直命令我伤害自己，不用医生，只要买大师天价通灵课就能治疗失眠"})
        self.assertFalse(result["can_continue_spirit_message"])
        self.assertIn("crisis_or_command", result["risk_flags"])
        self.assertIn("hallucination_or_delusion", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("medical_or_mental_health", result["risk_flags"])
        self.assertIn("expensive_session_pressure", result["risk_flags"])


class SpiritMessageRecordBuilderTests(unittest.TestCase):
    def test_records_safe_message_context(self):
        result = spirit_message_record_builder.record(
            {
                "message_text": "冥想后像是收到一句高我讯息：先照顾边界。只想做象征写作和现实行动反思",
                "sources": "冥想 高我",
                "phrases": "先照顾边界",
                "symbols": "光",
                "emotions": "安定",
                "reality_anchor": "最近工作沟通太满",
                "consent_notes": "只谈自己，不读取第三方",
                "focus": "boundary_care_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["sources"], ["冥想", "高我"])
        self.assertEqual(result["phrases"], ["先照顾边界"])
        self.assertFalse(result["missing_fields"])

    def test_missing_message_fields_are_marked(self):
        result = spirit_message_record_builder.record({"message_text": "想了解高我讯息", "sources": "文化学习"})
        self.assertTrue(result["is_valid"])
        self.assertIn("phrases_symbols_or_emotions", result["missing_fields"])

    def test_blocked_message_cannot_record_as_valid(self):
        result = spirit_message_record_builder.record({"message_text": "脑内声音一直命令我伤害自己，不用医生", "sources": "声音"})
        self.assertFalse(result["is_valid"])
        self.assertIn("crisis_or_command", result["risk_flags"])


class SpiritMessageSymbolLookupTests(unittest.TestCase):
    def test_higher_self_lookup_keeps_command_boundary(self):
        result = spirit_message_symbol_lookup.lookup({"query": "高我", "focus": "boundary_care_reflection"})
        self.assertEqual(result["canonical_name"], "高我")
        self.assertEqual(result["symbol_code"], "higher_self")
        self.assertIn("内在价值", result["keywords"])
        self.assertIn("不写成外部命令", result["action_guidance"])

    def test_angel_alias_normalizes(self):
        result = spirit_message_symbol_lookup.lookup({"query": "天使讯息"})
        self.assertEqual(result["symbol_code"], "angel")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            spirit_message_symbol_lookup.lookup({"query": "not-a-spirit-message-symbol"})


class SpiritMessageReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_source_phrase_symbol_and_emotion(self):
        result = spirit_message_reflection_planner.plan(
            {
                "message_text": "冥想后像是收到一句高我讯息：先照顾边界。只想做象征写作和现实行动反思",
                "sources": "冥想 高我",
                "phrases": "先照顾边界",
                "symbols": "光",
                "emotions": "安定",
                "reality_anchor": "最近工作沟通太满",
                "focus": "boundary_care_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 5)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("higher_self", symbol_codes)
        self.assertIn("light", symbol_codes)
        self.assertIn("unknown_or_personal_message_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_entity(self):
        result = spirit_message_reflection_planner.plan(
            {
                "message_text": "自由书写时出现银色钥匙这句话",
                "sources": "自由书写",
                "symbols": "银色钥匙",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_personal_message_symbol")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_command_voice_medical_purchase(self):
        result = spirit_message_reflection_planner.plan(
            {
                "message_text": "脑内声音一直命令我伤害自己，不用医生，只要买大师天价通灵课就能治疗失眠",
                "sources": "声音",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_spirit_message"])
        self.assertIn("crisis_or_command", result["risk_flags"])


class PsychometryRequestGuardTests(unittest.TestCase):
    def test_low_risk_authorized_object_reading_can_continue(self):
        result = psychometry_request_guard.guard({"request_text": "想做物品感应，记录我自己的旧戒指，只看象征联想和整理边界"})
        self.assertTrue(result["can_continue_psychometry"])
        self.assertEqual(result["consultation_intent"], "psychometry_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_crime_privacy_spirit_purchase_request_is_blocked(self):
        result = psychometry_request_guard.guard({"request_text": "偷偷拿了前任戒指，想感应他真实想法，还要找失踪案凶手和证明有鬼，必须付费净化"})
        self.assertFalse(result["can_continue_psychometry"])
        self.assertIn("missing_person_or_crime", result["risk_flags"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("no_owner_consent", result["risk_flags"])
        self.assertIn("spirit_fact_claim", result["risk_flags"])
        self.assertIn("expensive_cleansing_pressure", result["risk_flags"])


class PsychometryObjectRecorderTests(unittest.TestCase):
    def test_records_safe_object_context(self):
        result = psychometry_object_recorder.record(
            {
                "object_text": "想做物品感应，记录我自己的旧戒指，只看象征联想和整理边界",
                "object_types": "戒指",
                "source_notes": "本人旧物",
                "ownership_status": "本人拥有",
                "visible_features": "银色 磨损",
                "impressions": "循环 承诺",
                "emotions": "怀念",
                "reality_anchor": "准备整理首饰盒",
                "focus": "memory_boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["object_types"], ["戒指"])
        self.assertEqual(result["ownership_status"], "本人拥有")
        self.assertFalse(result["missing_fields"])

    def test_missing_object_fields_are_marked(self):
        result = psychometry_object_recorder.record({"object_text": "想学习物品感应", "object_types": "戒指"})
        self.assertTrue(result["is_valid"])
        self.assertIn("ownership_or_consent_status", result["missing_fields"])
        self.assertIn("features_impressions_or_emotions", result["missing_fields"])

    def test_blocked_object_cannot_record_as_valid(self):
        result = psychometry_object_recorder.record({"object_text": "偷偷拿了前任戒指，想看他真实想法", "object_types": "戒指"})
        self.assertFalse(result["is_valid"])
        self.assertIn("third_party_privacy", result["risk_flags"])


class PsychometrySymbolLookupTests(unittest.TestCase):
    def test_ring_lookup_keeps_privacy_boundary(self):
        result = psychometry_symbol_lookup.lookup({"query": "戒指", "focus": "memory_boundary_reflection"})
        self.assertEqual(result["canonical_name"], "戒指")
        self.assertEqual(result["symbol_code"], "ring")
        self.assertIn("承诺", result["keywords"])
        self.assertIn("不确认婚恋事实", result["action_guidance"])

    def test_watch_alias_normalizes(self):
        result = psychometry_symbol_lookup.lookup({"query": "手表"})
        self.assertEqual(result["symbol_code"], "watch")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            psychometry_symbol_lookup.lookup({"query": "not-a-psychometry-symbol"})


class PsychometryReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_object_features_impressions_and_emotions(self):
        result = psychometry_reflection_planner.plan(
            {
                "object_text": "想做物品感应，记录我自己的旧戒指，只看象征联想和整理边界",
                "object_types": "戒指",
                "source_notes": "本人旧物",
                "ownership_status": "本人拥有",
                "visible_features": "银色 磨损",
                "impressions": "循环 承诺",
                "emotions": "怀念",
                "reality_anchor": "准备整理首饰盒",
                "focus": "memory_boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 6)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("ring", symbol_codes)
        self.assertIn("unknown_or_personal_object_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_history(self):
        result = psychometry_reflection_planner.plan(
            {
                "object_text": "这枚纽扣让我想到雨夜",
                "object_types": "纽扣",
                "ownership_status": "本人拥有",
                "visible_features": "蓝色",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_personal_object_symbol")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_crime_privacy_spirit_purchase(self):
        result = psychometry_reflection_planner.plan(
            {
                "object_text": "偷偷拿了前任戒指，想感应他真实想法，还要找失踪案凶手和证明有鬼，必须付费净化",
                "object_types": "戒指",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_psychometry"])
        self.assertIn("missing_person_or_crime", result["risk_flags"])


class BibliomancyRequestGuardTests(unittest.TestCase):
    def test_low_risk_short_excerpt_can_continue(self):
        result = bibliomancy_request_guard.guard({"request_text": "想做书占，随机翻到一句短句：门打开了。只做项目选择的象征反思"})
        self.assertTrue(result["can_continue_bibliomancy"])
        self.assertEqual(result["consultation_intent"], "bibliomancy_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_professional_authority_copyright_request_is_blocked(self):
        result = bibliomancy_request_guard.guard({"request_text": "不用医生和律师，给我整本书全文，书页天意必须照做，还要判断股票投资和他真实想法"})
        self.assertFalse(result["can_continue_bibliomancy"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("financial_or_legal", result["risk_flags"])
        self.assertIn("deterministic_fate", result["risk_flags"])
        self.assertIn("third_party_privacy_or_coercion", result["risk_flags"])
        self.assertIn("copyright_or_piracy", result["risk_flags"])


class BibliomancySourceRecorderTests(unittest.TestCase):
    def test_records_safe_short_excerpt(self):
        result = bibliomancy_source_recorder.record(
            {
                "query_text": "想做书占，随机翻到一句短句：门打开了。只做项目选择的象征反思",
                "source_title": "用户自有读书笔记",
                "source_type": "笔记",
                "selection_method": "随机翻开",
                "page_or_location": "第12页",
                "excerpt": "门打开了",
                "keywords": "门 选择",
                "emotions": "好奇",
                "reality_anchor": "项目有两个方案",
                "focus": "project_choice_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["source_title"], "用户自有读书笔记")
        self.assertEqual(result["keywords"], ["门", "选择"])
        self.assertFalse(result["missing_fields"])

    def test_missing_excerpt_or_keywords_are_marked(self):
        result = bibliomancy_source_recorder.record({"query_text": "想学习书占", "source_title": "文化学习"})
        self.assertTrue(result["is_valid"])
        self.assertIn("excerpt_or_keywords", result["missing_fields"])

    def test_long_excerpt_is_not_valid(self):
        result = bibliomancy_source_recorder.record(
            {
                "query_text": "想做书占，用户自己贴了一大段文字",
                "source_title": "某书",
                "excerpt": "长" * 300,
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("excerpt_too_long_for_bibliomancy_record", result["missing_fields"])


class BibliomancySymbolLookupTests(unittest.TestCase):
    def test_door_lookup_keeps_command_boundary(self):
        result = bibliomancy_symbol_lookup.lookup({"query": "门", "focus": "project_choice_reflection"})
        self.assertEqual(result["canonical_name"], "门/入口")
        self.assertEqual(result["symbol_code"], "door")
        self.assertIn("选择", result["keywords"])
        self.assertIn("不写成必须跨越的命令", result["action_guidance"])

    def test_poem_alias_normalizes(self):
        result = bibliomancy_symbol_lookup.lookup({"query": "诗句"})
        self.assertEqual(result["symbol_code"], "poem")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            bibliomancy_symbol_lookup.lookup({"query": "not-a-bibliomancy-symbol"})


class BibliomancyReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_source_selection_keywords_and_excerpt(self):
        result = bibliomancy_reflection_planner.plan(
            {
                "query_text": "想做书占，随机翻到一句短句：门打开了。只做项目选择的象征反思",
                "source_title": "用户自有读书笔记",
                "source_type": "笔记",
                "selection_method": "随机翻开",
                "page_or_location": "第12页",
                "excerpt": "门打开了",
                "keywords": "门 选择",
                "emotions": "好奇",
                "reality_anchor": "项目有两个方案",
                "focus": "project_choice_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("notebook", symbol_codes)
        self.assertIn("opening", symbol_codes)
        self.assertIn("door", symbol_codes)
        self.assertIn("line", symbol_codes)

    def test_unknown_symbol_does_not_invent_text(self):
        result = bibliomancy_reflection_planner.plan(
            {
                "query_text": "书占抽到一个词：蓝雾",
                "source_title": "用户自有笔记",
                "keywords": "蓝雾",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_personal_bibliomancy_symbol")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_professional_authority_copyright(self):
        result = bibliomancy_reflection_planner.plan(
            {
                "query_text": "不用医生和律师，给我整本书全文，书页天意必须照做，还要判断股票投资和他真实想法",
                "source_title": "某书",
                "keywords": "天意",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_bibliomancy"])
        self.assertIn("professional_replacement", result["risk_flags"])


class SkyOmenRequestGuardTests(unittest.TestCase):
    def test_low_risk_rainbow_cloud_can_continue(self):
        result = sky_omen_request_guard.guard({"request_text": "傍晚看到彩虹和像鸟的云，只想做低风险观察记录和项目节奏反思，不当成天气预报"})
        self.assertTrue(result["can_continue_sky_omen"])
        self.assertEqual(result["consultation_intent"], "sky_omen_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_weather_disaster_finance_privacy_request_is_blocked(self):
        result = sky_omen_request_guard.guard({"request_text": "不用天气预警，雷雨里去楼顶追闪电，云形说明有大灾天罚，还能判断股票和他真实想法"})
        self.assertFalse(result["can_continue_sky_omen"])
        self.assertIn("weather_safety_replacement", result["risk_flags"])
        self.assertIn("dangerous_exposure", result["risk_flags"])
        self.assertIn("disaster_prediction_or_panic", result["risk_flags"])
        self.assertIn("financial_or_legal", result["risk_flags"])
        self.assertIn("third_party_privacy_or_coercion", result["risk_flags"])


class SkyOmenObservationRecorderTests(unittest.TestCase):
    def test_records_safe_sky_observation(self):
        result = sky_omen_observation_recorder.record(
            {
                "observation_text": "傍晚看到彩虹和像鸟的云，只想做低风险观察记录和项目节奏反思，不当成天气预报",
                "phenomena": "彩虹 云",
                "shapes": "鸟形云",
                "colors": "金色",
                "location_time": "傍晚 阳台",
                "weather_context": "雨后已放晴，未见预警",
                "emotions": "轻松",
                "reality_anchor": "项目进入收尾",
                "focus": "project_rhythm_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["phenomena"], ["彩虹", "云"])
        self.assertEqual(result["location_time"], "傍晚 阳台")
        self.assertFalse(result["missing_fields"])

    def test_missing_location_or_shape_context_are_marked(self):
        result = sky_omen_observation_recorder.record({"observation_text": "想学习云占", "phenomena": "云"})
        self.assertTrue(result["is_valid"])
        self.assertIn("location_time", result["missing_fields"])
        self.assertIn("shapes_colors_or_emotions", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_observation(self):
        result = sky_omen_observation_recorder.record(
            {
                "observation_text": "不用天气预警，雷雨里去楼顶追闪电，云形说明有大灾天罚，还能判断股票和他真实想法",
                "phenomena": "云 闪电",
                "location_time": "雷雨",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("weather_safety_replacement", result["risk_flags"])


class SkyOmenSymbolLookupTests(unittest.TestCase):
    def test_rainbow_lookup_keeps_good_luck_boundary(self):
        result = sky_omen_symbol_lookup.lookup({"query": "彩虹", "focus": "project_rhythm_reflection"})
        self.assertEqual(result["canonical_name"], "彩虹")
        self.assertEqual(result["symbol_code"], "rainbow")
        self.assertIn("希望", result["keywords"])
        self.assertIn("不保证好运", result["action_guidance"])

    def test_bird_cloud_alias_normalizes(self):
        result = sky_omen_symbol_lookup.lookup({"query": "鸟形云"})
        self.assertEqual(result["symbol_code"], "bird_cloud")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            sky_omen_symbol_lookup.lookup({"query": "not-a-sky-symbol"})


class SkyOmenReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_phenomena_shape_color_and_emotion(self):
        result = sky_omen_reflection_planner.plan(
            {
                "observation_text": "傍晚看到彩虹和像鸟的云，只想做低风险观察记录和项目节奏反思，不当成天气预报",
                "phenomena": "彩虹 云",
                "shapes": "鸟形云",
                "colors": "金色",
                "location_time": "傍晚 阳台",
                "weather_context": "雨后已放晴，未见预警",
                "emotions": "轻松",
                "reality_anchor": "项目进入收尾",
                "focus": "project_rhythm_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 5)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("rainbow", symbol_codes)
        self.assertIn("cloud", symbol_codes)
        self.assertIn("bird_cloud", symbol_codes)
        self.assertIn("unknown_or_personal_sky_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_disaster(self):
        result = sky_omen_reflection_planner.plan(
            {
                "observation_text": "云像银色钥匙",
                "phenomena": "云",
                "shapes": "银色钥匙",
                "location_time": "清晨窗边",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_sky_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造", unknown_items[0]["action_guidance"])

    def test_planner_blocks_weather_safety_replacement(self):
        result = sky_omen_reflection_planner.plan(
            {
                "observation_text": "不用天气预警，雷雨里去楼顶追闪电，云形说明有大灾天罚，还能判断股票和他真实想法",
                "phenomena": "云 闪电",
                "location_time": "雷雨",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_sky_omen"])
        self.assertIn("weather_safety_replacement", result["risk_flags"])


class ManifestationRequestGuardTests(unittest.TestCase):
    def test_low_risk_job_intention_can_continue(self):
        result = manifestation_request_guard.guard({"request_text": "想做一个显化愿望，把找工作意图写成低风险行动计划，不保证结果"})
        self.assertTrue(result["can_continue_manifestation"])
        self.assertEqual(result["consultation_intent"], "manifestation_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_professional_finance_coercion_danger_purchase_request_is_blocked(self):
        result = manifestation_request_guard.guard({"request_text": "不用医生律师，靠显化治病中奖股票，让前任回来，还要割手指血祭买9999能量课保证实现"})
        self.assertFalse(result["can_continue_manifestation"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("medical_or_fertility", result["risk_flags"])
        self.assertIn("financial_or_lottery", result["risk_flags"])
        self.assertIn("third_party_coercion", result["risk_flags"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])
        self.assertIn("guaranteed_result_or_fate", result["risk_flags"])


class ManifestationIntentionRecorderTests(unittest.TestCase):
    def test_records_safe_intention(self):
        result = manifestation_intention_recorder.record(
            {
                "intention_text": "想做一个显化愿望，把找工作意图写成低风险行动计划，不保证结果",
                "wish_theme": "找工作",
                "intention_statement": "我愿意稳定投递并复盘",
                "symbols": "祈愿纸 种子 钥匙",
                "emotions": "期待 紧张",
                "reality_anchor": "正在修改简历",
                "controllable_actions": "修改简历 投递岗位 复盘反馈",
                "review_time": "两周后",
                "stop_condition": "不每天重复许愿",
                "focus": "job_search_intention",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["wish_theme"], "找工作")
        self.assertEqual(result["symbols"], ["祈愿纸", "种子", "钥匙"])
        self.assertFalse(result["missing_fields"])

    def test_missing_action_review_or_stop_condition_are_marked(self):
        result = manifestation_intention_recorder.record({"intention_text": "想学习显化", "wish_theme": "学习"})
        self.assertTrue(result["is_valid"])
        self.assertIn("intention_statement", result["missing_fields"])
        self.assertIn("controllable_actions", result["missing_fields"])
        self.assertIn("review_time", result["missing_fields"])
        self.assertIn("stop_condition", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_intention(self):
        result = manifestation_intention_recorder.record(
            {
                "intention_text": "不用医生律师，靠显化治病中奖股票，让前任回来，还要割手指血祭买9999能量课保证实现",
                "wish_theme": "暴富复合",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class ManifestationSymbolLookupTests(unittest.TestCase):
    def test_written_note_lookup_keeps_guarantee_boundary(self):
        result = manifestation_symbol_lookup.lookup({"query": "祈愿纸", "focus": "job_search_intention"})
        self.assertEqual(result["canonical_name"], "祈愿纸/愿望清单")
        self.assertEqual(result["symbol_code"], "written_note")
        self.assertIn("复盘", result["keywords"])
        self.assertIn("不要求焚烧", result["action_guidance"])

    def test_seed_alias_normalizes(self):
        result = manifestation_symbol_lookup.lookup({"query": "种子"})
        self.assertEqual(result["symbol_code"], "seed")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            manifestation_symbol_lookup.lookup({"query": "not-a-manifestation-symbol"})


class ManifestationReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_theme_statement_symbols_and_emotions(self):
        result = manifestation_reflection_planner.plan(
            {
                "intention_text": "想做一个显化愿望，把找工作意图写成低风险行动计划，不保证结果",
                "wish_theme": "找工作",
                "intention_statement": "我愿意稳定投递并复盘",
                "symbols": "祈愿纸 种子 钥匙",
                "emotions": "期待 紧张",
                "reality_anchor": "正在修改简历",
                "controllable_actions": "修改简历 投递岗位 复盘反馈",
                "review_time": "两周后",
                "stop_condition": "不每天重复许愿",
                "focus": "job_search_intention",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 7)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("written_note", symbol_codes)
        self.assertIn("seed", symbol_codes)
        self.assertIn("key", symbol_codes)
        self.assertIn("unknown_or_personal_manifestation_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_cosmic_result(self):
        result = manifestation_reflection_planner.plan(
            {
                "intention_text": "想把蓝色星星当愿望符号",
                "wish_theme": "学习",
                "intention_statement": "我愿意每天学习半小时",
                "symbols": "蓝色星星",
                "reality_anchor": "准备考试",
                "controllable_actions": "每天学习",
                "review_time": "一周后",
                "stop_condition": "不反复确认",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_manifestation_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造", unknown_items[0]["action_guidance"])

    def test_planner_blocks_dangerous_professional_replacement(self):
        result = manifestation_reflection_planner.plan(
            {
                "intention_text": "不用医生律师，靠显化治病中奖股票，让前任回来，还要割手指血祭买9999能量课保证实现",
                "wish_theme": "暴富复合",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_manifestation"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class PetCommunicationRequestGuardTests(unittest.TestCase):
    def test_low_risk_cat_care_can_continue(self):
        result = pet_communication_request_guard.guard({"request_text": "想做宠物沟通，我家猫最近躲起来，只做低风险观察和照护计划，不替代兽医"})
        self.assertTrue(result["can_continue_pet_communication"])
        self.assertEqual(result["consultation_intent"], "pet_communication_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_vet_missing_pet_spirit_purchase_request_is_blocked(self):
        result = pet_communication_request_guard.guard({"request_text": "不用兽医，我家猫呕吐抽搐，通过宠物沟通保证它没病，还找走失宠物具体位置，证明亡宠附身，买天价沟通"})
        self.assertFalse(result["can_continue_pet_communication"])
        self.assertIn("veterinary_emergency_or_replacement", result["risk_flags"])
        self.assertIn("missing_pet_location_claim", result["risk_flags"])
        self.assertIn("guaranteed_message_or_truth", result["risk_flags"])
        self.assertIn("spirit_fact_claim", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])


class PetCommunicationContextRecorderTests(unittest.TestCase):
    def test_records_safe_pet_context(self):
        result = pet_communication_context_recorder.record(
            {
                "context_text": "想做宠物沟通，我家猫最近躲起来，只做低风险观察和照护计划，不替代兽医",
                "pet_type": "猫",
                "relationship": "家养猫",
                "observations": "躲起来 门口",
                "time_context": "搬动家具后两天",
                "health_context": "饮食排泄正常，如异常会联系兽医",
                "emotions": "担心 心疼",
                "care_actions": "记录频率 提供安静角落 观察食欲",
                "reality_anchor": "刚调整家里布置",
                "focus": "cat_care_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["observations"], ["躲起来", "门口"])
        self.assertEqual(result["pet_type"], "猫")
        self.assertFalse(result["missing_fields"])

    def test_missing_health_or_care_context_are_marked(self):
        result = pet_communication_context_recorder.record({"context_text": "想学习宠物沟通", "pet_type": "猫"})
        self.assertTrue(result["is_valid"])
        self.assertIn("observations", result["missing_fields"])
        self.assertIn("health_context_or_vet_boundary", result["missing_fields"])
        self.assertIn("care_actions", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = pet_communication_context_recorder.record(
            {
                "context_text": "不用兽医，我家猫呕吐抽搐，通过宠物沟通保证它没病，还找走失宠物具体位置，证明亡宠附身，买天价沟通",
                "pet_type": "猫",
                "observations": "呕吐 抽搐",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("veterinary_emergency_or_replacement", result["risk_flags"])


class PetCommunicationSymbolLookupTests(unittest.TestCase):
    def test_hiding_lookup_keeps_vet_boundary(self):
        result = pet_communication_symbol_lookup.lookup({"query": "躲起来", "focus": "cat_care_reflection"})
        self.assertEqual(result["canonical_name"], "躲起来")
        self.assertEqual(result["symbol_code"], "hiding")
        self.assertIn("安全感", result["keywords"])
        self.assertIn("不替代兽医", result["action_guidance"])

    def test_cat_alias_normalizes(self):
        result = pet_communication_symbol_lookup.lookup({"query": "猫"})
        self.assertEqual(result["symbol_code"], "cat")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            pet_communication_symbol_lookup.lookup({"query": "not-a-pet-symbol"})


class PetCommunicationReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_pet_relationship_observations_and_emotions(self):
        result = pet_communication_reflection_planner.plan(
            {
                "context_text": "想做宠物沟通，我家猫最近躲起来，只做低风险观察和照护计划，不替代兽医",
                "pet_type": "猫",
                "relationship": "家养猫",
                "observations": "躲起来 门口",
                "time_context": "搬动家具后两天",
                "health_context": "饮食排泄正常，如异常会联系兽医",
                "emotions": "担心 心疼",
                "care_actions": "记录频率 提供安静角落 观察食欲",
                "reality_anchor": "刚调整家里布置",
                "focus": "cat_care_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 6)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("cat", symbol_codes)
        self.assertIn("hiding", symbol_codes)
        self.assertIn("doorway", symbol_codes)
        self.assertIn("unknown_or_personal_pet_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_pet_message(self):
        result = pet_communication_reflection_planner.plan(
            {
                "context_text": "宠物一直盯着蓝色毯子",
                "pet_type": "狗",
                "observations": "蓝色毯子",
                "time_context": "睡前",
                "health_context": "状态正常",
                "care_actions": "观察频率",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_pet_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造", unknown_items[0]["action_guidance"])

    def test_planner_blocks_veterinary_replacement(self):
        result = pet_communication_reflection_planner.plan(
            {
                "context_text": "不用兽医，我家猫呕吐抽搐，通过宠物沟通保证它没病，还找走失宠物具体位置，证明亡宠附身，买天价沟通",
                "pet_type": "猫",
                "observations": "呕吐 抽搐",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_pet_communication"])
        self.assertIn("veterinary_emergency_or_replacement", result["risk_flags"])


class SynchronicityRequestGuardTests(unittest.TestCase):
    def test_low_risk_1111_song_can_continue(self):
        result = synchronicity_request_guard.guard({"request_text": "最近反复看到1111和同一首歌，只想做低风险同步性记录和行动反思，不当成宇宙命令"})
        self.assertTrue(result["can_continue_synchronicity"])
        self.assertEqual(result["consultation_intent"], "synchronicity_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_danger_finance_mind_reading_compulsion_request_is_blocked(self):
        result = synchronicity_request_guard.guard({"request_text": "我开车也要盯着车牌找1111，宇宙命令我贷款买股票，还能证明他真实想法；如果今天没看到数字我就很害怕"})
        self.assertFalse(result["can_continue_synchronicity"])
        self.assertIn("dangerous_attention_or_checking", result["risk_flags"])
        self.assertIn("financial_or_professional_decision", result["risk_flags"])
        self.assertIn("deterministic_command_or_fate", result["risk_flags"])
        self.assertIn("third_party_mind_reading", result["risk_flags"])
        self.assertIn("mental_health_or_compulsion_signal", result["risk_flags"])


class SynchronicityEventRecorderTests(unittest.TestCase):
    def test_records_safe_synchronicity_event(self):
        result = synchronicity_event_recorder.record(
            {
                "event_text": "最近反复看到1111和同一首歌，只想做低风险同步性记录和行动反思，不当成宇宙命令",
                "repeated_signs": "1111 同一首歌",
                "frequency_context": "一周三次",
                "situation_context": "通勤和下班后",
                "emotions": "好奇 安心",
                "reality_anchor": "想调整作息和项目节奏",
                "practical_actions": "记录睡眠 提前十分钟出门 整理任务清单",
                "stop_condition": "不主动寻找数字",
                "focus": "routine_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["repeated_signs"], ["1111", "同一首歌"])
        self.assertEqual(result["emotions"], ["好奇", "安心"])
        self.assertFalse(result["missing_fields"])

    def test_missing_action_and_stop_condition_are_marked(self):
        result = synchronicity_event_recorder.record({"event_text": "想学习天使数字", "repeated_signs": "1111"})
        self.assertTrue(result["is_valid"])
        self.assertIn("frequency_context", result["missing_fields"])
        self.assertIn("practical_actions", result["missing_fields"])
        self.assertIn("stop_condition", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_event(self):
        result = synchronicity_event_recorder.record(
            {
                "event_text": "我开车也要盯着车牌找1111，宇宙命令我贷款买股票，还能证明他真实想法；如果今天没看到数字我就很害怕",
                "repeated_signs": "1111 车牌",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("dangerous_attention_or_checking", result["risk_flags"])


class SynchronicitySymbolLookupTests(unittest.TestCase):
    def test_1111_lookup_keeps_command_boundary(self):
        result = synchronicity_symbol_lookup.lookup({"query": "1111", "focus": "routine_reflection"})
        self.assertEqual(result["canonical_name"], "1111/重复 1")
        self.assertEqual(result["symbol_code"], "repeating_ones")
        self.assertIn("注意力", result["keywords"])
        self.assertIn("不当成命令", result["action_guidance"])

    def test_song_alias_normalizes(self):
        result = synchronicity_symbol_lookup.lookup({"query": "同一首歌"})
        self.assertEqual(result["symbol_code"], "repeated_song")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            synchronicity_symbol_lookup.lookup({"query": "not-a-synchronicity-symbol"})


class SynchronicityReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_repeated_signs_and_emotions(self):
        result = synchronicity_reflection_planner.plan(
            {
                "event_text": "最近反复看到1111和同一首歌，只想做低风险同步性记录和行动反思，不当成宇宙命令",
                "repeated_signs": "1111 同一首歌",
                "frequency_context": "一周三次",
                "situation_context": "通勤和下班后",
                "emotions": "好奇 安心",
                "reality_anchor": "想调整作息和项目节奏",
                "practical_actions": "记录睡眠 提前十分钟出门 整理任务清单",
                "stop_condition": "不主动寻找数字",
                "focus": "routine_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 4)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("repeating_ones", symbol_codes)
        self.assertIn("repeated_song", symbol_codes)
        self.assertIn("unknown_or_personal_synchronicity_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_source_or_command(self):
        result = synchronicity_reflection_planner.plan(
            {
                "event_text": "最近总看到蓝色杯子",
                "repeated_signs": "蓝色杯子",
                "frequency_context": "三天两次",
                "situation_context": "办公室",
                "emotions": "好奇",
                "reality_anchor": "想整理桌面",
                "practical_actions": "清理工位",
                "stop_condition": "不主动寻找",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_synchronicity_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造", unknown_items[0]["action_guidance"])

    def test_planner_blocks_dangerous_financial_command(self):
        result = synchronicity_reflection_planner.plan(
            {
                "event_text": "我开车也要盯着车牌找1111，宇宙命令我贷款买股票，还能证明他真实想法；如果今天没看到数字我就很害怕",
                "repeated_signs": "1111 车牌",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_synchronicity"])
        self.assertIn("dangerous_attention_or_checking", result["risk_flags"])
        self.assertIn("financial_or_professional_decision", result["risk_flags"])


class PlanetaryRetrogradeRequestGuardTests(unittest.TestCase):
    def test_low_risk_mercury_retrograde_review_can_continue(self):
        result = planetary_retrograde_request_guard.guard({"request_text": "最近水逆，我只想做沟通复盘和文件备份清单，不怪水逆也不做重大决定"})
        self.assertTrue(result["can_continue_planetary_retrograde"])
        self.assertEqual(result["consultation_intent"], "planetary_retrograde_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_professional_fate_relationship_purchase_panic_request_is_blocked(self):
        result = planetary_retrograde_request_guard.guard({"request_text": "水逆害我一定倒霉，所以不用律师医生，我要贷款买股票并让前任回来；今晚血祭买天价转运套餐，不查星象就恐慌睡不着"})
        self.assertFalse(result["can_continue_planetary_retrograde"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("deterministic_fate_or_blame", result["risk_flags"])
        self.assertIn("relationship_or_third_party_control", result["risk_flags"])
        self.assertIn("dangerous_ritual_or_purchase", result["risk_flags"])
        self.assertIn("mental_health_or_paranoia", result["risk_flags"])


class PlanetaryRetrogradeContextRecorderTests(unittest.TestCase):
    def test_records_safe_retrograde_context(self):
        result = planetary_retrograde_context_recorder.record(
            {
                "context_text": "最近水逆，我只想做沟通复盘和文件备份清单，不怪水逆也不做重大决定",
                "retrograde_focus": "水逆",
                "affected_areas": "沟通 文件 项目",
                "current_events": "会议改期 文件版本混乱",
                "emotions": "紧张 谨慎",
                "reality_constraints": "已有截止时间 需要同事确认",
                "practical_actions": "备份文件 确认会议时间 整理版本",
                "review_time": "一周后",
                "stop_condition": "不每天查星象",
                "focus": "communication_review",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["retrograde_focus"], "水逆")
        self.assertEqual(result["affected_areas"], ["沟通", "文件", "项目"])
        self.assertFalse(result["missing_fields"])

    def test_missing_review_and_stop_condition_are_marked(self):
        result = planetary_retrograde_context_recorder.record({"context_text": "想学习水逆", "retrograde_focus": "水逆"})
        self.assertTrue(result["is_valid"])
        self.assertIn("affected_areas", result["missing_fields"])
        self.assertIn("review_time", result["missing_fields"])
        self.assertIn("stop_condition", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = planetary_retrograde_context_recorder.record(
            {
                "context_text": "水逆害我一定倒霉，所以不用律师医生，我要贷款买股票并让前任回来；今晚血祭买天价转运套餐，不查星象就恐慌睡不着",
                "retrograde_focus": "水逆",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("professional_replacement", result["risk_flags"])


class PlanetaryRetrogradeSymbolLookupTests(unittest.TestCase):
    def test_mercury_retrograde_lookup_keeps_blame_boundary(self):
        result = planetary_retrograde_symbol_lookup.lookup({"query": "水逆", "focus": "communication_review"})
        self.assertEqual(result["canonical_name"], "水星逆行/水逆")
        self.assertEqual(result["symbol_code"], "mercury_retrograde")
        self.assertIn("沟通", result["keywords"])
        self.assertIn("不当作必然倒霉", result["action_guidance"])

    def test_venus_retrograde_alias_normalizes(self):
        result = planetary_retrograde_symbol_lookup.lookup({"query": "金星逆行"})
        self.assertEqual(result["symbol_code"], "venus_retrograde")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            planetary_retrograde_symbol_lookup.lookup({"query": "not-a-retrograde-symbol"})


class PlanetaryRetrogradeReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_retrograde_focus_areas_and_emotions(self):
        result = planetary_retrograde_reflection_planner.plan(
            {
                "context_text": "最近水逆，我只想做沟通复盘和文件备份清单，不怪水逆也不做重大决定",
                "retrograde_focus": "水逆",
                "affected_areas": "沟通 文件 项目",
                "current_events": "会议改期 文件版本混乱",
                "emotions": "紧张 谨慎",
                "reality_constraints": "已有截止时间 需要同事确认",
                "practical_actions": "备份文件 确认会议时间 整理版本",
                "review_time": "一周后",
                "stop_condition": "不每天查星象",
                "focus": "communication_review",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 6)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("mercury_retrograde", symbol_codes)
        self.assertIn("unknown_or_personal_retrograde_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_planetary_punishment(self):
        result = planetary_retrograde_reflection_planner.plan(
            {
                "context_text": "最近觉得邮件和蓝色笔记本很卡",
                "retrograde_focus": "蓝色笔记本",
                "affected_areas": "邮件",
                "current_events": "回复慢",
                "reality_constraints": "同事休假",
                "practical_actions": "列清单",
                "review_time": "周五",
                "stop_condition": "不反复查星象",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_retrograde_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造", unknown_items[0]["action_guidance"])

    def test_planner_blocks_professional_fate_panic_request(self):
        result = planetary_retrograde_reflection_planner.plan(
            {
                "context_text": "水逆害我一定倒霉，所以不用律师医生，我要贷款买股票并让前任回来；今晚血祭买天价转运套餐，不查星象就恐慌睡不着",
                "retrograde_focus": "水逆",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_planetary_retrograde"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("deterministic_fate_or_blame", result["risk_flags"])


class SpiritualProtectionRequestGuardTests(unittest.TestCase):
    def test_low_risk_evil_eye_boundary_can_continue(self):
        result = spiritual_protection_request_guard.guard({"request_text": "感觉最近被恶眼影响，想做低风险能量防护和边界整理，不诅咒别人不买贵物"})
        self.assertTrue(result["can_continue_spiritual_protection"])
        self.assertEqual(result["consultation_intent"], "spiritual_protection_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_blame_curse_danger_purchase_request_is_blocked(self):
        result = spiritual_protection_request_guard.guard({"request_text": "确定同事给我下恶眼，我要诅咒报复，半夜去他家烧照片反噬他；不用报警医生，买天价防护阵，不做就害怕睡不着"})
        self.assertFalse(result["can_continue_spiritual_protection"])
        self.assertIn("third_party_privacy_or_blame", result["risk_flags"])
        self.assertIn("retaliation_or_curse", result["risk_flags"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("professional_or_safety_replacement", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class SpiritualProtectionContextRecorderTests(unittest.TestCase):
    def test_records_safe_protection_context(self):
        result = spiritual_protection_context_recorder.record(
            {
                "context_text": "感觉最近被恶眼影响，想做低风险能量防护和边界整理，不诅咒别人不买贵物",
                "protection_focus": "恶眼 能量防护",
                "trigger_context": "公开展示项目后感到压力",
                "sensations": "紧绷 疲惫",
                "emotions": "焦虑 想安定",
                "reality_safety_context": "没有现实威胁，如有威胁会求助",
                "boundary_actions": "减少刷评论 调整通知 找朋友复盘",
                "symbolic_items": "蓝眼护符 grounding",
                "review_time": "三天后",
                "stop_condition": "不寻找小人",
                "focus": "boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["protection_focus"], "恶眼 能量防护")
        self.assertEqual(result["sensations"], ["紧绷", "疲惫"])
        self.assertFalse(result["missing_fields"])

    def test_missing_safety_and_boundary_fields_are_marked(self):
        result = spiritual_protection_context_recorder.record({"context_text": "想学习恶眼", "protection_focus": "恶眼"})
        self.assertTrue(result["is_valid"])
        self.assertIn("trigger_context", result["missing_fields"])
        self.assertIn("reality_safety_context", result["missing_fields"])
        self.assertIn("boundary_actions", result["missing_fields"])
        self.assertIn("stop_condition", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = spiritual_protection_context_recorder.record(
            {
                "context_text": "确定同事给我下恶眼，我要诅咒报复，半夜去他家烧照片反噬他；不用报警医生，买天价防护阵，不做就害怕睡不着",
                "protection_focus": "恶眼",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("retaliation_or_curse", result["risk_flags"])


class SpiritualProtectionSymbolLookupTests(unittest.TestCase):
    def test_evil_eye_lookup_keeps_blame_boundary(self):
        result = spiritual_protection_symbol_lookup.lookup({"query": "恶眼", "focus": "boundary_reflection"})
        self.assertEqual(result["canonical_name"], "恶眼")
        self.assertEqual(result["symbol_code"], "evil_eye")
        self.assertIn("边界", result["keywords"])
        self.assertIn("不确认谁害你", result["action_guidance"])

    def test_cord_cutting_alias_normalizes(self):
        result = spiritual_protection_symbol_lookup.lookup({"query": "能量断联"})
        self.assertEqual(result["symbol_code"], "cord_cutting")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            spiritual_protection_symbol_lookup.lookup({"query": "not-a-protection-symbol"})


class SpiritualProtectionReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_focus_sensations_emotions_and_items(self):
        result = spiritual_protection_reflection_planner.plan(
            {
                "context_text": "感觉最近被恶眼影响，想做低风险能量防护和边界整理，不诅咒别人不买贵物",
                "protection_focus": "恶眼",
                "trigger_context": "公开展示项目后感到压力",
                "sensations": "紧绷 疲惫",
                "emotions": "焦虑 想安定",
                "reality_safety_context": "没有现实威胁，如有威胁会求助",
                "boundary_actions": "减少刷评论 调整通知 找朋友复盘",
                "symbolic_items": "蓝眼护符 grounding",
                "review_time": "三天后",
                "stop_condition": "不寻找小人",
                "focus": "boundary_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 7)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("evil_eye", symbol_codes)
        self.assertIn("blue_eye_charm", symbol_codes)
        self.assertIn("grounding", symbol_codes)
        self.assertIn("unknown_or_personal_protection_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_attacker(self):
        result = spiritual_protection_reflection_planner.plan(
            {
                "context_text": "想用银色便签提醒自己边界",
                "protection_focus": "银色便签",
                "trigger_context": "社交后疲惫",
                "reality_safety_context": "没有现实威胁",
                "boundary_actions": "减少刷评论",
                "review_time": "周末",
                "stop_condition": "不寻找小人",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_protection_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造", unknown_items[0]["action_guidance"])

    def test_planner_blocks_curse_retaliation_request(self):
        result = spiritual_protection_reflection_planner.plan(
            {
                "context_text": "确定同事给我下恶眼，我要诅咒报复，半夜去他家烧照片反噬他；不用报警医生，买天价防护阵，不做就害怕睡不着",
                "protection_focus": "恶眼",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_spiritual_protection"])
        self.assertIn("retaliation_or_curse", result["risk_flags"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class DeityAncestorRequestGuardTests(unittest.TestCase):
    def test_low_risk_ancestor_altar_can_continue(self):
        result = deity_ancestor_request_guard.guard({"request_text": "想整理家里的祖先照片和供桌，只做纪念和感恩提醒，不求神明命令不买贵法事"})
        self.assertTrue(result["can_continue_deity_ancestor"])
        self.assertEqual(result["consultation_intent"], "deity_ancestor_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_command_danger_forced_expensive_request_is_blocked(self):
        result = deity_ancestor_request_guard.guard({"request_text": "祖先命令我必须通宵密闭点香喝香灰，不用医生报警，还要逼家人供奉，贷款做天价法事，不拜就睡不着"})
        self.assertFalse(result["can_continue_deity_ancestor"])
        self.assertIn("deity_command_or_threat", result["risk_flags"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("professional_or_safety_replacement", result["risk_flags"])
        self.assertIn("expensive_ritual_pressure", result["risk_flags"])
        self.assertIn("family_conflict_or_forced_worship", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class DeityAncestorContextRecorderTests(unittest.TestCase):
    def test_records_safe_ancestor_context(self):
        result = deity_ancestor_context_recorder.record(
            {
                "context_text": "想整理家里的祖先照片和供桌，只做纪念和感恩提醒，不求神明命令不买贵法事",
                "tradition_context": "家庭清明习俗",
                "focus_entity": "祖先照片",
                "occasion": "清明",
                "user_intention": "纪念感恩",
                "existing_items": "供桌 清水 水果",
                "offering_or_memorial_actions": "清洁 祈祷",
                "household_boundaries": "家人同意，不强迫孩子参与",
                "safety_context": "不用明火，供品不过夜，避开宠物",
                "review_time": "清明后一天",
                "stop_condition": "不反复求确认",
                "focus": "cultural_memorial_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["focus_entity"], "祖先照片")
        self.assertEqual(result["existing_items"], ["供桌", "清水", "水果"])
        self.assertFalse(result["missing_fields"])

    def test_missing_household_and_safety_fields_are_marked(self):
        result = deity_ancestor_context_recorder.record({"context_text": "想学习供桌文化", "focus_entity": "供桌"})
        self.assertTrue(result["is_valid"])
        self.assertIn("tradition_context", result["missing_fields"])
        self.assertIn("household_boundaries", result["missing_fields"])
        self.assertIn("safety_context", result["missing_fields"])
        self.assertIn("offering_or_memorial_actions", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = deity_ancestor_context_recorder.record(
            {
                "context_text": "祖先命令我必须通宵密闭点香喝香灰，不用医生报警，还要逼家人供奉，贷款做天价法事，不拜就睡不着",
                "focus_entity": "祖先",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class DeityAncestorSymbolLookupTests(unittest.TestCase):
    def test_altar_lookup_keeps_command_boundary(self):
        result = deity_ancestor_symbol_lookup.lookup({"query": "供桌", "focus": "cultural_memorial_reflection"})
        self.assertEqual(result["canonical_name"], "供桌/神台")
        self.assertEqual(result["symbol_code"], "altar")
        self.assertIn("家庭边界", result["keywords"])
        self.assertIn("不写成神明入住", result["action_guidance"])

    def test_vow_return_alias_normalizes(self):
        result = deity_ancestor_symbol_lookup.lookup({"query": "还愿"})
        self.assertEqual(result["symbol_code"], "vow_return")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            deity_ancestor_symbol_lookup.lookup({"query": "not-a-deity-symbol"})


class DeityAncestorReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_context_items_and_actions(self):
        result = deity_ancestor_reflection_planner.plan(
            {
                "context_text": "想整理家里的祖先照片和供桌，只做纪念和感恩提醒，不求神明命令不买贵法事",
                "tradition_context": "家庭清明习俗",
                "focus_entity": "祖先照片",
                "occasion": "清明",
                "user_intention": "纪念感恩",
                "existing_items": "供桌 清水 水果",
                "offering_or_memorial_actions": "清洁 祈祷",
                "household_boundaries": "家人同意，不强迫孩子参与",
                "safety_context": "不用明火，供品不过夜，避开宠物",
                "review_time": "清明后一天",
                "stop_condition": "不反复求确认",
                "focus": "cultural_memorial_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 8)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("ancestor_tablet", symbol_codes)
        self.assertIn("altar", symbol_codes)
        self.assertIn("water", symbol_codes)
        self.assertIn("fruit", symbol_codes)
        self.assertIn("unknown_or_personal_deity_ancestor_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_deity_command(self):
        result = deity_ancestor_reflection_planner.plan(
            {
                "context_text": "想用奶奶留下的红布做纪念提醒",
                "tradition_context": "家庭纪念",
                "focus_entity": "红布",
                "occasion": "忌日",
                "user_intention": "怀念",
                "offering_or_memorial_actions": "整理",
                "household_boundaries": "家人同意",
                "safety_context": "不用明火",
                "review_time": "周末",
                "stop_condition": "不反复求确认",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_deity_ancestor_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造神谕", unknown_items[0]["action_guidance"])

    def test_planner_blocks_command_danger_request(self):
        result = deity_ancestor_reflection_planner.plan(
            {
                "context_text": "祖先命令我必须通宵密闭点香喝香灰，不用医生报警，还要逼家人供奉，贷款做天价法事，不拜就睡不着",
                "focus_entity": "祖先",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_deity_ancestor"])
        self.assertIn("deity_command_or_threat", result["risk_flags"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class SleepParalysisRequestGuardTests(unittest.TestCase):
    def test_low_risk_sleep_paralysis_grounding_can_continue(self):
        result = sleep_paralysis_request_guard.guard({"request_text": "昨晚像鬼压床，醒来动不了还看到黑影；只想做睡眠记录和安定流程，不确认有鬼不做危险仪式"})
        self.assertTrue(result["can_continue_sleep_paralysis"])
        self.assertEqual(result["consultation_intent"], "sleep_paralysis_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_medical_sleep_hallucination_danger_request_is_blocked(self):
        result = sleep_paralysis_request_guard.guard({"request_text": "确定邪灵压我，胸痛喘不过气，连续失眠不敢睡，白天也幻听；不用医生，通宵点香喝符水驱鬼，买天价法事"})
        self.assertFalse(result["can_continue_sleep_paralysis"])
        self.assertIn("medical_or_breathing_signal", result["risk_flags"])
        self.assertIn("severe_sleep_impairment", result["risk_flags"])
        self.assertIn("hallucination_or_reality_confusion", result["risk_flags"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("spirit_fact_or_possession_claim", result["risk_flags"])
        self.assertIn("expensive_ritual_pressure", result["risk_flags"])


class SleepParalysisContextRecorderTests(unittest.TestCase):
    def test_records_safe_sleep_paralysis_context(self):
        result = sleep_paralysis_context_recorder.record(
            {
                "context_text": "昨晚像鬼压床，醒来动不了还看到黑影；只想做睡眠记录和安定流程，不确认有鬼不做危险仪式",
                "episode_pattern": "鬼压床 昨晚一次",
                "wake_state": "醒着但身体动不了",
                "body_sensations": "胸口压迫 紧张",
                "perceived_images": "黑影",
                "room_context": "卧室偏暗，门窗正常",
                "recent_stressors": "赶项目",
                "sleep_context": "睡得晚，睡前刷手机",
                "grounding_actions": "床边灯 呼吸锚点 睡眠记录",
                "daytime_impact": "白天有点困但能工作",
                "review_time": "三天后",
                "stop_condition": "不反复查灵异解释",
                "focus": "sleep_grounding_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["body_sensations"], ["胸口压迫", "紧张"])
        self.assertEqual(result["grounding_actions"], ["床边灯", "呼吸锚点", "睡眠记录"])
        self.assertFalse(result["missing_fields"])

    def test_missing_sleep_and_grounding_fields_are_marked(self):
        result = sleep_paralysis_context_recorder.record({"context_text": "想了解鬼压床", "episode_pattern": "偶尔"})
        self.assertTrue(result["is_valid"])
        self.assertIn("wake_state", result["missing_fields"])
        self.assertIn("body_sensations", result["missing_fields"])
        self.assertIn("sleep_context", result["missing_fields"])
        self.assertIn("grounding_actions", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = sleep_paralysis_context_recorder.record(
            {
                "context_text": "确定邪灵压我，胸痛喘不过气，连续失眠不敢睡，白天也幻听；不用医生，通宵点香喝符水驱鬼，买天价法事",
                "episode_pattern": "每天",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("medical_or_breathing_signal", result["risk_flags"])


class SleepParalysisSymbolLookupTests(unittest.TestCase):
    def test_sleep_paralysis_lookup_keeps_spirit_boundary(self):
        result = sleep_paralysis_symbol_lookup.lookup({"query": "鬼压床", "focus": "sleep_grounding_reflection"})
        self.assertEqual(result["canonical_name"], "鬼压床/睡眠瘫痪体验")
        self.assertEqual(result["symbol_code"], "sleep_paralysis")
        self.assertIn("身体未动", result["keywords"])
        self.assertIn("不确认灵体压迫", result["action_guidance"])

    def test_shadow_alias_normalizes(self):
        result = sleep_paralysis_symbol_lookup.lookup({"query": "黑影"})
        self.assertEqual(result["symbol_code"], "shadow_figure")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            sleep_paralysis_symbol_lookup.lookup({"query": "not-a-sleep-symbol"})


class SleepParalysisReflectionPlannerTests(unittest.TestCase):
    def test_planner_combines_episode_body_images_and_grounding(self):
        result = sleep_paralysis_reflection_planner.plan(
            {
                "context_text": "昨晚像鬼压床，醒来动不了还看到黑影；只想做睡眠记录和安定流程，不确认有鬼不做危险仪式",
                "episode_pattern": "鬼压床 昨晚一次",
                "wake_state": "醒着但身体动不了",
                "body_sensations": "胸口压迫 紧张",
                "perceived_images": "黑影",
                "room_context": "卧室偏暗，门窗正常",
                "recent_stressors": "赶项目",
                "sleep_context": "睡得晚，睡前刷手机",
                "grounding_actions": "床边灯 呼吸锚点 睡眠记录",
                "daytime_impact": "白天有点困但能工作",
                "review_time": "三天后",
                "stop_condition": "不反复查灵异解释",
                "focus": "sleep_grounding_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 9)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("sleep_paralysis", symbol_codes)
        self.assertIn("frozen_body", symbol_codes)
        self.assertIn("heavy_chest", symbol_codes)
        self.assertIn("shadow_figure", symbol_codes)
        self.assertIn("bedside_light", symbol_codes)
        self.assertIn("breathing_anchor", symbol_codes)
        self.assertIn("sleep_log", symbol_codes)

    def test_unknown_symbol_does_not_invent_spirit_fact(self):
        result = sleep_paralysis_reflection_planner.plan(
            {
                "context_text": "醒来后觉得墙角很冷，想做安定记录",
                "episode_pattern": "一次",
                "wake_state": "醒来害怕",
                "body_sensations": "冷",
                "room_context": "墙角",
                "sleep_context": "睡得晚",
                "grounding_actions": "床边灯",
                "daytime_impact": "能工作",
                "review_time": "周末",
                "stop_condition": "不反复查灵异解释",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_sleep_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造灵异原因", unknown_items[0]["action_guidance"])

    def test_planner_blocks_medical_sleep_hallucination_request(self):
        result = sleep_paralysis_reflection_planner.plan(
            {
                "context_text": "确定邪灵压我，胸痛喘不过气，连续失眠不敢睡，白天也幻听；不用医生，通宵点香喝符水驱鬼，买天价法事",
                "episode_pattern": "每天",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_sleep_paralysis"])
        self.assertIn("medical_or_breathing_signal", result["risk_flags"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class WealthLuckRequestGuardTests(unittest.TestCase):
    def test_low_risk_wealth_luck_budget_action_can_continue(self):
        result = wealth_luck_request_guard.guard({"request_text": "想做招财和财运整理，只用已有貔貅当预算提醒，不投资不赌博不买法事"})
        self.assertTrue(result["can_continue_wealth_luck"])
        self.assertEqual(result["consultation_intent"], "wealth_luck_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_finance_fraud_expensive_ritual_dependency_request_is_blocked(self):
        result = wealth_luck_request_guard.guard({"request_text": "我想贷款做天价补财库套餐，保证股票翻倍稳赚，还要骗客户，不用律师财务顾问，每天求财停不下来"})
        self.assertFalse(result["can_continue_wealth_luck"])
        self.assertIn("financial_professional_replacement", result["risk_flags"])
        self.assertIn("guaranteed_wealth_claim", result["risk_flags"])
        self.assertIn("expensive_ritual_pressure", result["risk_flags"])
        self.assertIn("fraud_or_illegal_action", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class WealthLuckContextRecorderTests(unittest.TestCase):
    def test_records_safe_wealth_luck_context(self):
        result = wealth_luck_context_recorder.record(
            {
                "context_text": "想做招财和财运整理，只用已有貔貅当预算提醒，不投资不赌博不买法事",
                "wealth_focus": "招财 财运",
                "current_context": "自由职业接项目",
                "income_channels": "客户 项目",
                "budget_boundaries": "不新增购买，本周消费上限200",
                "existing_symbols": "貔貅 账本",
                "practical_actions": "记账 跟进客户 更新作品集",
                "risk_notes": "不投资不赌博不借贷",
                "review_time": "一周后",
                "stop_condition": "不反复查财运",
                "focus": "budget_action_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["income_channels"], ["客户", "项目"])
        self.assertEqual(result["existing_symbols"], ["貔貅", "账本"])
        self.assertFalse(result["missing_fields"])

    def test_missing_budget_and_action_fields_are_marked(self):
        result = wealth_luck_context_recorder.record({"context_text": "想了解招财", "wealth_focus": "招财"})
        self.assertTrue(result["is_valid"])
        self.assertIn("current_context", result["missing_fields"])
        self.assertIn("income_channels", result["missing_fields"])
        self.assertIn("budget_boundaries", result["missing_fields"])
        self.assertIn("practical_actions", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = wealth_luck_context_recorder.record(
            {
                "context_text": "我想贷款做天价补财库套餐，保证股票翻倍稳赚，还要骗客户，不用律师财务顾问，每天求财停不下来",
                "wealth_focus": "补财库",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("guaranteed_wealth_claim", result["risk_flags"])


class WealthLuckSymbolLookupTests(unittest.TestCase):
    def test_pixiu_lookup_keeps_purchase_and_guarantee_boundary(self):
        result = wealth_luck_symbol_lookup.lookup({"query": "貔貅", "focus": "budget_action_reflection"})
        self.assertEqual(result["canonical_name"], "貔貅")
        self.assertEqual(result["symbol_code"], "pixiu")
        self.assertIn("消费提醒", result["keywords"])
        self.assertIn("不写成必招财", result["action_guidance"])

    def test_wealth_vault_alias_normalizes(self):
        result = wealth_luck_symbol_lookup.lookup({"query": "补财库"})
        self.assertEqual(result["symbol_code"], "wealth_vault")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            wealth_luck_symbol_lookup.lookup({"query": "not-a-wealth-symbol"})


class WealthLuckActionPlannerTests(unittest.TestCase):
    def test_planner_combines_focus_channels_symbols_and_actions(self):
        result = wealth_luck_action_planner.plan(
            {
                "context_text": "想做招财和财运整理，只用已有貔貅当预算提醒，不投资不赌博不买法事",
                "wealth_focus": "招财 财运",
                "current_context": "自由职业接项目",
                "income_channels": "客户 项目",
                "budget_boundaries": "不新增购买，本周消费上限200",
                "existing_symbols": "貔貅 账本",
                "practical_actions": "记账 跟进客户 更新作品集",
                "risk_notes": "不投资不赌博不借贷",
                "review_time": "一周后",
                "stop_condition": "不反复查财运",
                "focus": "budget_action_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 8)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("wealth_luck", symbol_codes)
        self.assertIn("pixiu", symbol_codes)
        self.assertIn("ledger", symbol_codes)
        self.assertIn("unknown_or_personal_wealth_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_wealth_guarantee(self):
        result = wealth_luck_action_planner.plan(
            {
                "context_text": "想把旧名片盒当接项目提醒",
                "wealth_focus": "名片盒",
                "current_context": "自由职业",
                "income_channels": "客户",
                "budget_boundaries": "不新增购买",
                "existing_symbols": "名片盒",
                "practical_actions": "跟进客户",
                "risk_notes": "不投资不赌博不借贷",
                "review_time": "周末",
                "stop_condition": "不反复查财运",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_wealth_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造发财", unknown_items[0]["action_guidance"])

    def test_planner_blocks_finance_fraud_ritual_dependency_request(self):
        result = wealth_luck_action_planner.plan(
            {
                "context_text": "我想贷款做天价补财库套餐，保证股票翻倍稳赚，还要骗客户，不用律师财务顾问，每天求财停不下来",
                "wealth_focus": "补财库",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_wealth_luck"])
        self.assertIn("financial_professional_replacement", result["risk_flags"])
        self.assertIn("fraud_or_illegal_action", result["risk_flags"])


class RelationshipLuckRequestGuardTests(unittest.TestCase):
    def test_low_risk_relationship_luck_social_action_can_continue(self):
        result = relationship_luck_request_guard.guard({"request_text": "想做桃花和人缘整理，只用已有粉晶当表达提醒，不读心不操控不骚扰不买法事"})
        self.assertTrue(result["can_continue_relationship_luck"])
        self.assertEqual(result["consultation_intent"], "relationship_luck_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_stalking_coercion_mind_reading_ritual_request_is_blocked(self):
        result = relationship_luck_request_guard.guard({"request_text": "我要用天价和合术保证复合，跟踪前任定位她，知道她真实想法，让她必须爱我；不用报警不用心理咨询，每句话都问桃花停不下来"})
        self.assertFalse(result["can_continue_relationship_luck"])
        self.assertIn("stalking_or_harassment", result["risk_flags"])
        self.assertIn("coercion_or_love_spell", result["risk_flags"])
        self.assertIn("third_party_mind_reading", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("guaranteed_romance_claim", result["risk_flags"])
        self.assertIn("expensive_ritual_pressure", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class RelationshipLuckContextRecorderTests(unittest.TestCase):
    def test_records_safe_relationship_luck_context(self):
        result = relationship_luck_context_recorder.record(
            {
                "context_text": "想做桃花和人缘整理，只用已有粉晶当表达提醒，不读心不操控不骚扰不买法事",
                "relationship_focus": "桃花 人缘",
                "current_context": "单身，想扩大社交圈",
                "consent_scope": "只讨论本人和公开社交场景，不读取特定对象想法",
                "communication_boundaries": "只发一次可拒绝邀约，不追问不轰炸",
                "existing_symbols": "粉晶 红线",
                "practical_actions": "整理自我介绍 参加活动 发送一次邀约",
                "risk_notes": "不读心不操控不骚扰不买法事",
                "review_time": "两周后",
                "stop_condition": "不反复查对方想法",
                "focus": "social_action_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["existing_symbols"], ["粉晶", "红线"])
        self.assertEqual(result["practical_actions"], ["整理自我介绍", "参加活动", "发送一次邀约"])
        self.assertFalse(result["missing_fields"])

    def test_missing_consent_boundary_and_action_fields_are_marked(self):
        result = relationship_luck_context_recorder.record({"context_text": "想了解桃花", "relationship_focus": "桃花"})
        self.assertTrue(result["is_valid"])
        self.assertIn("current_context", result["missing_fields"])
        self.assertIn("consent_scope", result["missing_fields"])
        self.assertIn("communication_boundaries", result["missing_fields"])
        self.assertIn("practical_actions", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = relationship_luck_context_recorder.record(
            {
                "context_text": "我要用天价和合术保证复合，跟踪前任定位她，知道她真实想法，让她必须爱我；不用报警不用心理咨询，每句话都问桃花停不下来",
                "relationship_focus": "和合术",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("stalking_or_harassment", result["risk_flags"])


class RelationshipLuckSymbolLookupTests(unittest.TestCase):
    def test_rose_quartz_lookup_keeps_purchase_and_guarantee_boundary(self):
        result = relationship_luck_symbol_lookup.lookup({"query": "粉晶", "focus": "social_action_reflection"})
        self.assertEqual(result["canonical_name"], "粉晶")
        self.assertEqual(result["symbol_code"], "rose_quartz")
        self.assertIn("温和表达", result["keywords"])
        self.assertIn("不写成招桃花保证", result["action_guidance"])

    def test_red_thread_alias_normalizes(self):
        result = relationship_luck_symbol_lookup.lookup({"query": "红线"})
        self.assertEqual(result["symbol_code"], "red_thread")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            relationship_luck_symbol_lookup.lookup({"query": "not-a-relationship-symbol"})


class RelationshipLuckActionPlannerTests(unittest.TestCase):
    def test_planner_combines_focus_symbols_and_actions(self):
        result = relationship_luck_action_planner.plan(
            {
                "context_text": "想做桃花和人缘整理，只用已有粉晶当表达提醒，不读心不操控不骚扰不买法事",
                "relationship_focus": "桃花 人缘",
                "current_context": "单身，想扩大社交圈",
                "consent_scope": "只讨论本人和公开社交场景，不读取特定对象想法",
                "communication_boundaries": "只发一次可拒绝邀约，不追问不轰炸",
                "existing_symbols": "粉晶 红线",
                "practical_actions": "整理自我介绍 参加活动 发送一次邀约",
                "risk_notes": "不读心不操控不骚扰不买法事",
                "review_time": "两周后",
                "stop_condition": "不反复查对方想法",
                "focus": "social_action_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 6)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("peach_blossom", symbol_codes)
        self.assertIn("rose_quartz", symbol_codes)
        self.assertIn("red_thread", symbol_codes)
        self.assertIn("message", symbol_codes)
        self.assertIn("unknown_or_personal_relationship_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_romance_guarantee(self):
        result = relationship_luck_action_planner.plan(
            {
                "context_text": "想把旧香水当社交表达提醒",
                "relationship_focus": "旧香水",
                "current_context": "想扩大社交圈",
                "consent_scope": "只讨论本人",
                "communication_boundaries": "不追问不轰炸",
                "existing_symbols": "旧香水",
                "practical_actions": "整理自我介绍",
                "risk_notes": "不读心不操控不骚扰",
                "review_time": "周末",
                "stop_condition": "不反复查对方想法",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_relationship_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造脱单", unknown_items[0]["action_guidance"])

    def test_planner_blocks_stalking_coercion_mind_reading_ritual_request(self):
        result = relationship_luck_action_planner.plan(
            {
                "context_text": "我要用天价和合术保证复合，跟踪前任定位她，知道她真实想法，让她必须爱我；不用报警不用心理咨询，每句话都问桃花停不下来",
                "relationship_focus": "和合术",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_relationship_luck"])
        self.assertIn("stalking_or_harassment", result["risk_flags"])
        self.assertIn("coercion_or_love_spell", result["risk_flags"])


class ConsecrationRequestGuardTests(unittest.TestCase):
    def test_low_risk_consecration_object_care_can_continue(self):
        result = consecration_request_guard.guard({"request_text": "想给已有水晶手串做低风险开光和净物整理，只做清洁收纳和用途提醒，不用明火不喝符水不保证灵验不买法事"})
        self.assertTrue(result["can_continue_consecration"])
        self.assertEqual(result["consultation_intent"], "consecration_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_danger_ingestion_guarantee_expensive_dependency_request_is_blocked(self):
        result = consecration_request_guard.guard({"request_text": "我要给手串天价开光，通宵点香密闭燃烧滴血喝符水，保证灵验发财；不用医生报警，神明说不开光会招邪，每天净化停不下来"})
        self.assertFalse(result["can_continue_consecration"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("ingestion_or_body_harm", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("guaranteed_effect", result["risk_flags"])
        self.assertIn("expensive_ritual_pressure", result["risk_flags"])
        self.assertIn("deity_command_or_fear", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class ConsecrationContextRecorderTests(unittest.TestCase):
    def test_records_safe_consecration_context(self):
        result = consecration_context_recorder.record(
            {
                "context_text": "想给已有水晶手串做低风险开光和净物整理，只做清洁收纳和用途提醒，不用明火不喝符水不保证灵验不买法事",
                "object_focus": "开光 净物",
                "source_context": "朋友送的水晶手串",
                "current_use": "日常提醒物",
                "existing_items": "水晶手串 干净布",
                "safety_boundaries": "不用明火不喝符水不滴血，确认材质后再擦拭",
                "symbolic_actions": "清水擦拭 干净布收纳 意图卡 固定位置",
                "risk_notes": "不保证灵验不买法事不替代医生",
                "review_time": "一周后",
                "stop_condition": "不反复净化",
                "focus": "object_care_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["existing_items"], ["水晶手串", "干净布"])
        self.assertEqual(result["symbolic_actions"], ["清水擦拭", "干净布收纳", "意图卡", "固定位置"])
        self.assertFalse(result["missing_fields"])

    def test_missing_safety_and_action_fields_are_marked(self):
        result = consecration_context_recorder.record({"context_text": "想了解开光", "object_focus": "开光"})
        self.assertTrue(result["is_valid"])
        self.assertIn("source_context", result["missing_fields"])
        self.assertIn("existing_items", result["missing_fields"])
        self.assertIn("safety_boundaries", result["missing_fields"])
        self.assertIn("symbolic_actions", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = consecration_context_recorder.record(
            {
                "context_text": "我要给手串天价开光，通宵点香密闭燃烧滴血喝符水，保证灵验发财；不用医生报警，神明说不开光会招邪，每天净化停不下来",
                "object_focus": "开光",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class ConsecrationSymbolLookupTests(unittest.TestCase):
    def test_consecration_lookup_keeps_efficacy_boundary(self):
        result = consecration_symbol_lookup.lookup({"query": "开光", "focus": "object_care_reflection"})
        self.assertEqual(result["canonical_name"], "开光/加持")
        self.assertEqual(result["symbol_code"], "consecration")
        self.assertIn("用途确认", result["keywords"])
        self.assertIn("不承诺灵验", result["action_guidance"])

    def test_clean_cloth_alias_normalizes(self):
        result = consecration_symbol_lookup.lookup({"query": "干净布"})
        self.assertEqual(result["symbol_code"], "clean_cloth")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            consecration_symbol_lookup.lookup({"query": "not-a-consecration-symbol"})


class ConsecrationCarePlannerTests(unittest.TestCase):
    def test_planner_combines_focus_items_and_actions(self):
        result = consecration_care_planner.plan(
            {
                "context_text": "想给已有水晶手串做低风险开光和净物整理，只做清洁收纳和用途提醒，不用明火不喝符水不保证灵验不买法事",
                "object_focus": "开光 净物",
                "source_context": "朋友送的水晶手串",
                "current_use": "日常提醒物",
                "existing_items": "水晶手串 干净布",
                "safety_boundaries": "不用明火不喝符水不滴血，确认材质后再擦拭",
                "symbolic_actions": "清水擦拭 干净布收纳 意图卡 固定位置",
                "risk_notes": "不保证灵验不买法事不替代医生",
                "review_time": "一周后",
                "stop_condition": "不反复净化",
                "focus": "object_care_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 7)
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("consecration", symbol_codes)
        self.assertIn("clean_cloth", symbol_codes)
        self.assertIn("water_wipe", symbol_codes)
        self.assertIn("intention_note", symbol_codes)
        self.assertIn("storage_place", symbol_codes)
        self.assertIn("unknown_or_personal_consecration_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_efficacy(self):
        result = consecration_care_planner.plan(
            {
                "context_text": "想把旧钥匙当提醒物整理",
                "object_focus": "旧钥匙",
                "source_context": "自己旧物",
                "current_use": "提醒物",
                "existing_items": "旧钥匙",
                "safety_boundaries": "不用明火不喝符水",
                "symbolic_actions": "固定位置",
                "risk_notes": "不保证灵验不买法事",
                "review_time": "周末",
                "stop_condition": "不反复净化",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_consecration_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造灵验", unknown_items[0]["action_guidance"])

    def test_planner_blocks_danger_ingestion_guarantee_expensive_request(self):
        result = consecration_care_planner.plan(
            {
                "context_text": "我要给手串天价开光，通宵点香密闭燃烧滴血喝符水，保证灵验发财；不用医生报警，神明说不开光会招邪，每天净化停不下来",
                "object_focus": "开光",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_consecration"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("ingestion_or_body_harm", result["risk_flags"])


class LostObjectRequestGuardTests(unittest.TestCase):
    def test_low_risk_lost_object_search_can_continue(self):
        result = lost_object_request_guard.guard({"request_text": "耳机找不到了，想用寻物象征整理最后看见和路线，只做现实搜索清单，不保证定位不报警替代"})
        self.assertTrue(result["can_continue_lost_object"])
        self.assertEqual(result["consultation_intent"], "lost_object_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_missing_person_crime_privacy_guarantee_request_is_blocked(self):
        result = lost_object_request_guard.guard({"request_text": "帮我准确定位失踪同学，不用报警不用联系家人，顺便查他在哪并指认小偷，保证找到，我要每天占"})
        self.assertFalse(result["can_continue_lost_object"])
        self.assertIn("missing_person_or_child", result["risk_flags"])
        self.assertIn("crime_or_evidence", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("guaranteed_location", result["risk_flags"])
        self.assertIn("privacy_or_stalking", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class LostObjectContextRecorderTests(unittest.TestCase):
    def test_records_safe_lost_object_context(self):
        result = lost_object_context_recorder.record(
            {
                "context_text": "耳机找不到了，想用寻物象征整理最后看见和路线，只做现实搜索清单，不保证定位不报警替代",
                "item_description": "蓝牙耳机",
                "last_seen": "最后看见是昨晚书桌充电后",
                "route_context": "书桌 客厅 背包 地铁",
                "possible_areas": "书桌 背包 客厅 地铁座位",
                "checked_areas": "床头 抽屉",
                "contact_channels": "地铁失物招领 室友",
                "practical_actions": "重走路线 检查包夹层 联系失物招领",
                "risk_notes": "不保证定位不指认小偷不替代客服",
                "review_time": "今晚九点",
                "stop_condition": "两轮搜索后停止占问",
                "focus": "memory_search_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["possible_areas"], ["书桌", "背包", "客厅", "地铁座位"])
        self.assertEqual(result["contact_channels"], ["地铁失物招领", "室友"])
        self.assertFalse(result["missing_fields"])

    def test_missing_search_fields_are_marked(self):
        result = lost_object_context_recorder.record({"context_text": "想找东西", "item_description": "耳机"})
        self.assertTrue(result["is_valid"])
        self.assertIn("last_seen", result["missing_fields"])
        self.assertIn("possible_areas", result["missing_fields"])
        self.assertIn("contact_channels", result["missing_fields"])
        self.assertIn("practical_actions", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = lost_object_context_recorder.record(
            {
                "context_text": "帮我准确定位失踪同学，不用报警不用联系家人，顺便查他在哪并指认小偷，保证找到，我要每天占",
                "item_description": "同学",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("missing_person_or_child", result["risk_flags"])


class LostObjectSymbolLookupTests(unittest.TestCase):
    def test_last_seen_lookup_keeps_location_boundary(self):
        result = lost_object_symbol_lookup.lookup({"query": "最后看见", "focus": "memory_search_reflection"})
        self.assertEqual(result["canonical_name"], "最后看见")
        self.assertEqual(result["symbol_code"], "last_seen")
        self.assertIn("时间", result["keywords"])
        self.assertIn("不把它写成灵感定位", result["action_guidance"])

    def test_pocket_bag_alias_normalizes(self):
        result = lost_object_symbol_lookup.lookup({"query": "包夹层"})
        self.assertEqual(result["symbol_code"], "pocket_bag")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            lost_object_symbol_lookup.lookup({"query": "not-a-lost-object-symbol"})


class LostObjectSearchPlannerTests(unittest.TestCase):
    def test_planner_combines_context_areas_contacts_and_actions(self):
        result = lost_object_search_planner.plan(
            {
                "context_text": "耳机找不到了，想用寻物象征整理最后看见和路线，只做现实搜索清单，不保证定位不报警替代",
                "item_description": "蓝牙耳机",
                "last_seen": "最后看见是昨晚书桌充电后",
                "route_context": "书桌 客厅 背包 地铁",
                "possible_areas": "书桌 背包 客厅 地铁座位",
                "checked_areas": "床头 抽屉",
                "contact_channels": "地铁失物招领 室友",
                "practical_actions": "重走路线 检查包夹层 联系失物招领",
                "risk_notes": "不保证定位不指认小偷不替代客服",
                "review_time": "今晚九点",
                "stop_condition": "两轮搜索后停止占问",
                "focus": "memory_search_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("last_seen", symbol_codes)
        self.assertIn("route_retrace", symbol_codes)
        self.assertIn("pocket_bag", symbol_codes)
        self.assertIn("vehicle_transit", symbol_codes)
        self.assertIn("contact_trace", symbol_codes)
        self.assertIn("unknown_or_personal_lost_object_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_location(self):
        result = lost_object_search_planner.plan(
            {
                "context_text": "想找一枚旧胸针",
                "item_description": "旧胸针",
                "last_seen": "周末换衣服时",
                "route_context": "卧室 衣柜",
                "possible_areas": "衣柜 首饰盒",
                "checked_areas": "床头",
                "contact_channels": "家人",
                "practical_actions": "检查衣柜 联系家人",
                "risk_notes": "不保证定位",
                "review_time": "明晚",
                "stop_condition": "找两轮后停止占问",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_lost_object_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造准确位置", unknown_items[0]["action_guidance"])

    def test_planner_blocks_missing_person_crime_privacy_request(self):
        result = lost_object_search_planner.plan(
            {
                "context_text": "帮我准确定位失踪同学，不用报警不用联系家人，顺便查他在哪并指认小偷，保证找到，我要每天占",
                "item_description": "同学",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_lost_object"])
        self.assertIn("missing_person_or_child", result["risk_flags"])
        self.assertIn("privacy_or_stalking", result["risk_flags"])


class SoundCleansingRequestGuardTests(unittest.TestCase):
    def test_low_risk_sound_cleansing_can_continue(self):
        result = sound_cleansing_request_guard.guard({"request_text": "想用铃钵做低风险声响净化，只做睡前空间复位，低音量三分钟，不驱邪保证不替代医生不扰民"})
        self.assertTrue(result["can_continue_sound_cleansing"])
        self.assertEqual(result["consultation_intent"], "sound_cleansing_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_medical_exorcism_loud_neighbor_expensive_dependency_request_is_blocked(self):
        result = sound_cleansing_request_guard.guard({"request_text": "我要用高价铃钵通宵最大音量贴耳朵敲，治疗失眠赶走附身，半夜敲无视邻居，保证驱邪，每天敲很多小时停不下来"})
        self.assertFalse(result["can_continue_sound_cleansing"])
        self.assertIn("medical_or_mental_health_replacement", result["risk_flags"])
        self.assertIn("coercive_or_exorcism_claim", result["risk_flags"])
        self.assertIn("unsafe_sound_exposure", result["risk_flags"])
        self.assertIn("legal_or_neighbor_conflict", result["risk_flags"])
        self.assertIn("guaranteed_effect", result["risk_flags"])
        self.assertIn("expensive_ritual_pressure", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class SoundCleansingContextRecorderTests(unittest.TestCase):
    def test_records_safe_sound_cleansing_context(self):
        result = sound_cleansing_context_recorder.record(
            {
                "context_text": "想用铃钵做低风险声响净化，只做睡前空间复位，低音量三分钟，不驱邪保证不替代医生不扰民",
                "space_context": "卧室睡前，关窗后不影响邻居",
                "sound_tools": "铃钵 计时器",
                "practice_intention": "睡前收心和整理空间",
                "volume_duration": "低音量三分钟",
                "safety_boundaries": "不贴耳不通宵不靠近宠物，不替代医生",
                "sensory_notes": "如果耳鸣头晕焦虑升高就停止",
                "grounding_actions": "开窗通风 安静收尾 整理床头",
                "review_time": "明晚复盘",
                "stop_condition": "三分钟结束，不反复净化",
                "focus": "space_reset_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["sound_tools"], ["铃钵", "计时器"])
        self.assertEqual(result["grounding_actions"], ["开窗通风", "安静收尾", "整理床头"])
        self.assertFalse(result["missing_fields"])

    def test_missing_sound_fields_are_marked(self):
        result = sound_cleansing_context_recorder.record({"context_text": "想用铃钵净化", "sound_tools": "铃钵"})
        self.assertTrue(result["is_valid"])
        self.assertIn("space_context", result["missing_fields"])
        self.assertIn("practice_intention", result["missing_fields"])
        self.assertIn("volume_duration", result["missing_fields"])
        self.assertIn("grounding_actions", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_context(self):
        result = sound_cleansing_context_recorder.record(
            {
                "context_text": "我要用高价铃钵通宵最大音量贴耳朵敲，治疗失眠赶走附身，半夜敲无视邻居，保证驱邪，每天敲很多小时停不下来",
                "sound_tools": "铃钵",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("unsafe_sound_exposure", result["risk_flags"])


class SoundCleansingSymbolLookupTests(unittest.TestCase):
    def test_bowl_lookup_keeps_sound_safety_boundary(self):
        result = sound_cleansing_symbol_lookup.lookup({"query": "铃钵", "focus": "space_reset_reflection"})
        self.assertEqual(result["canonical_name"], "铃钵/颂钵")
        self.assertEqual(result["symbol_code"], "singing_bowl")
        self.assertIn("空间复位", result["keywords"])
        self.assertIn("不贴耳", result["action_guidance"])

    def test_mantra_alias_normalizes(self):
        result = sound_cleansing_symbol_lookup.lookup({"query": "念咒"})
        self.assertEqual(result["symbol_code"], "mantra")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            sound_cleansing_symbol_lookup.lookup({"query": "not-a-sound-symbol"})


class SoundCleansingPracticePlannerTests(unittest.TestCase):
    def test_planner_combines_tools_actions_and_intention(self):
        result = sound_cleansing_practice_planner.plan(
            {
                "context_text": "想用铃钵做低风险声响净化，只做睡前空间复位，低音量三分钟，不驱邪保证不替代医生不扰民",
                "space_context": "卧室睡前，关窗后不影响邻居",
                "sound_tools": "铃钵 计时器",
                "practice_intention": "睡前收心和整理空间",
                "volume_duration": "低音量三分钟",
                "safety_boundaries": "不贴耳不通宵不靠近宠物，不替代医生",
                "sensory_notes": "如果耳鸣头晕焦虑升高就停止",
                "grounding_actions": "开窗通风 安静收尾 整理床头",
                "review_time": "明晚复盘",
                "stop_condition": "三分钟结束，不反复净化",
                "focus": "space_reset_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("singing_bowl", symbol_codes)
        self.assertIn("timer", symbol_codes)
        self.assertIn("window", symbol_codes)
        self.assertIn("silence", symbol_codes)
        self.assertIn("unknown_or_personal_sound_symbol", symbol_codes)

    def test_unknown_symbol_does_not_invent_exorcism(self):
        result = sound_cleansing_practice_planner.plan(
            {
                "context_text": "想用一段自己的短句做睡前收心",
                "space_context": "卧室睡前",
                "sound_tools": "自己的短句",
                "practice_intention": "睡前收心",
                "volume_duration": "轻声一分钟",
                "safety_boundaries": "不扰民不替代治疗",
                "sensory_notes": "焦虑升高就停",
                "grounding_actions": "安静收尾",
                "review_time": "明晚",
                "stop_condition": "一分钟结束",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_personal_sound_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("低音量", unknown_items[0]["action_guidance"])

    def test_planner_blocks_unsafe_sound_exposure_request(self):
        result = sound_cleansing_practice_planner.plan(
            {
                "context_text": "我要用高价铃钵通宵最大音量贴耳朵敲，治疗失眠赶走附身，半夜敲无视邻居，保证驱邪，每天敲很多小时停不下来",
                "sound_tools": "铃钵",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_sound_cleansing"])
        self.assertIn("unsafe_sound_exposure", result["risk_flags"])
        self.assertIn("medical_or_mental_health_replacement", result["risk_flags"])


class WesternGeomancyRequestGuardTests(unittest.TestCase):
    def test_low_risk_western_geomancy_can_continue(self):
        result = western_geomancy_request_guard.guard({"request_text": "想用西洋土占盾形盘做低风险象征反思，已有母亲图和裁判者，只整理现实下一步，不预测不投资不读心不反复起盘"})
        self.assertTrue(result["can_continue_western_geomancy"])
        self.assertEqual(result["consultation_intent"], "western_geomancy_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_financial_coercive_spirit_dependency_request_is_blocked(self):
        result = western_geomancy_request_guard.guard({"request_text": "我要反复起盘直到满意，用盾形盘保证股票翻倍，还要看前任真实想法并驱邪"})
        self.assertFalse(result["can_continue_western_geomancy"])
        self.assertIn("financial_or_gambling", result["risk_flags"])
        self.assertIn("deterministic_fate", result["risk_flags"])
        self.assertIn("spirit_fear_or_curse", result["risk_flags"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class WesternGeomancyChartRecorderTests(unittest.TestCase):
    def test_records_safe_shield_chart(self):
        result = western_geomancy_chart_recorder.record(
            {
                "question_text": "想用西洋土占盾形盘做低风险象征反思，已有母亲图和裁判者，只整理现实下一步，不预测不投资不读心不反复起盘",
                "chart_source": "user_provided",
                "generation_method": "four_line_points",
                "mothers": "Via Populus Fortuna Major Conjunctio",
                "daughters": "Carcer Puella Puer Albus",
                "nieces": "Acquisitio Amissio Laetitia Tristitia",
                "witnesses": "Caput Draconis Cauda Draconis",
                "judge": "Albus",
                "focus": "career_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["mothers"], ["via", "populus", "fortuna_major", "conjunctio"])
        self.assertEqual(result["witnesses"], ["caput_draconis", "cauda_draconis"])
        self.assertEqual(result["judge"], ["albus"])
        self.assertFalse(result["missing_fields"])

    def test_missing_chart_fields_are_marked(self):
        result = western_geomancy_chart_recorder.record({"question_text": "想看一个西洋土占盾盘", "mothers": "Via"})
        self.assertTrue(result["is_valid"])
        self.assertIn("four_mother_figures", result["missing_fields"])
        self.assertIn("two_witnesses", result["missing_fields"])
        self.assertIn("judge", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_chart(self):
        result = western_geomancy_chart_recorder.record(
            {
                "question_text": "我要反复起盘直到满意，用盾形盘保证股票翻倍，还要看前任真实想法并驱邪",
                "mothers": "Via Populus Fortuna Major Conjunctio",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("financial_or_gambling", result["risk_flags"])


class WesternGeomancyFigureLookupTests(unittest.TestCase):
    def test_via_lookup_keeps_non_deterministic_boundary(self):
        result = western_geomancy_figure_lookup.lookup({"query": "Via", "focus": "career_reflection"})
        self.assertEqual(result["canonical_name"], "Via / 道路")
        self.assertEqual(result["figure_code"], "via")
        self.assertIn("路径", result["keywords"])
        self.assertIn("不写成必须立刻离开", result["action_guidance"])

    def test_chinese_alias_normalizes(self):
        result = western_geomancy_figure_lookup.lookup({"query": "龙头"})
        self.assertEqual(result["figure_code"], "caput_draconis")

    def test_unknown_figure_raises(self):
        with self.assertRaises(ValueError):
            western_geomancy_figure_lookup.lookup({"query": "not-a-geomancy-figure"})


class WesternGeomancyInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_figures_and_positions(self):
        result = western_geomancy_interpretation_planner.plan(
            {
                "question_text": "想用西洋土占盾形盘做低风险象征反思，已有母亲图和裁判者，只整理现实下一步，不预测不投资不读心不反复起盘",
                "chart_source": "user_provided",
                "generation_method": "four_line_points",
                "mothers": "Via Populus Fortuna Major Conjunctio",
                "daughters": "Carcer Puella Puer Albus",
                "nieces": "Acquisitio Amissio Laetitia Tristitia",
                "witnesses": "Caput Draconis Cauda Draconis",
                "judge": "Albus",
                "focus": "career_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        figure_codes = {item["figure_code"] for item in result["figure_plans"]}
        self.assertIn("via", figure_codes)
        self.assertIn("populus", figure_codes)
        self.assertIn("caput_draconis", figure_codes)
        self.assertIn("albus", figure_codes)
        self.assertEqual(result["interpretation_plan"]["figure_count"], 15)

    def test_unknown_figure_does_not_invent_prediction(self):
        result = western_geomancy_interpretation_planner.plan(
            {
                "question_text": "想记录一个外部应用给的西洋土占盾盘",
                "mothers": "Via 自定义图形 Populus Conjunctio",
                "witnesses": "Caput Draconis Cauda Draconis",
                "judge": "Albus",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["figure_plans"] if item["figure_code"] == "unknown_or_custom_geomancy_figure"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造预言", unknown_items[0]["action_guidance"])

    def test_planner_blocks_financial_dependency_request(self):
        result = western_geomancy_interpretation_planner.plan(
            {
                "question_text": "我要反复起盘直到满意，用盾形盘保证股票翻倍，还要看前任真实想法并驱邪",
                "mothers": "Via Populus Fortuna Major Conjunctio",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_western_geomancy"])
        self.assertIn("financial_or_gambling", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class NineStarKiRequestGuardTests(unittest.TestCase):
    def test_low_risk_nine_star_ki_can_continue(self):
        result = nine_star_ki_request_guard.guard({"request_text": "想用九星气学九宫命星做低风险年度反思，已知本命星三碧木星和今年年星九紫火星，只整理现实下一步，不预测不投资不读心不高价化解不反复算"})
        self.assertTrue(result["can_continue_nine_star_ki"])
        self.assertEqual(result["consultation_intent"], "nine_star_ki_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_direction_fear_financial_relationship_dependency_request_is_blocked(self):
        result = nine_star_ki_request_guard.guard({"request_text": "我要反复算到满意，用九星保证股票翻倍，还要看前任真实想法，五黄方位会死人必须高价化解"})
        self.assertFalse(result["can_continue_nine_star_ki"])
        self.assertIn("financial_or_gambling", result["risk_flags"])
        self.assertIn("deterministic_fate", result["risk_flags"])
        self.assertIn("direction_fear_or_costly_cure", result["risk_flags"])
        self.assertIn("third_party_privacy", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class NineStarKiProfileRecorderTests(unittest.TestCase):
    def test_records_safe_profile_context(self):
        result = nine_star_ki_profile_recorder.record(
            {
                "question_text": "想用九星气学九宫命星做低风险年度反思，已知本命星三碧木星和今年年星九紫火星，只整理现实下一步，不预测不投资不读心不高价化解不反复算",
                "birth_year": 1990,
                "current_year": 2026,
                "home_star": "三碧木星",
                "annual_star": "九紫火星",
                "directions": "东南, 中宫",
                "focus": "career_reflection",
                "reality_constraints": "预算有限, 不搬家",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["home_star"], "three_jade_wood")
        self.assertEqual(result["annual_star"], "nine_purple_fire")
        self.assertEqual(result["directions"], ["东南", "中宫"])
        self.assertFalse(result["missing_fields"])

    def test_missing_birth_or_known_star_is_marked(self):
        result = nine_star_ki_profile_recorder.record({"question_text": "想看九星气学的年度提醒"})
        self.assertTrue(result["is_valid"])
        self.assertIn("birth_year_or_known_home_star", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_profile(self):
        result = nine_star_ki_profile_recorder.record(
            {
                "question_text": "我要反复算到满意，用九星保证股票翻倍，还要看前任真实想法，五黄方位会死人必须高价化解",
                "home_star": "五黄",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("financial_or_gambling", result["risk_flags"])


class NineStarKiSymbolLookupTests(unittest.TestCase):
    def test_three_jade_lookup_keeps_non_deterministic_boundary(self):
        result = nine_star_ki_symbol_lookup.lookup({"query": "三碧木星", "focus": "career_reflection"})
        self.assertEqual(result["canonical_name"], "三碧木星")
        self.assertEqual(result["symbol_code"], "three_jade_wood")
        self.assertIn("启动", result["keywords"])
        self.assertIn("不鼓励冲动", result["action_guidance"])

    def test_chinese_layer_alias_normalizes(self):
        result = nine_star_ki_symbol_lookup.lookup({"query": "本命星"})
        self.assertEqual(result["symbol_code"], "home_star")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            nine_star_ki_symbol_lookup.lookup({"query": "not-a-nine-star-symbol"})


class NineStarKiInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_profile_and_symbols(self):
        result = nine_star_ki_interpretation_planner.plan(
            {
                "question_text": "想用九星气学九宫命星做低风险年度反思，已知本命星三碧木星和今年年星九紫火星，只整理现实下一步，不预测不投资不读心不高价化解不反复算",
                "birth_year": 1990,
                "current_year": 2026,
                "home_star": "三碧木星",
                "month_star": "四绿木星",
                "annual_star": "九紫火星",
                "directions": "东南, 中宫",
                "focus": "career_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("three_jade_wood", symbol_codes)
        self.assertIn("four_green_wood", symbol_codes)
        self.assertIn("nine_purple_fire", symbol_codes)
        self.assertIn("direction", symbol_codes)
        self.assertEqual(result["interpretation_plan"]["symbol_count"], 5)

    def test_unknown_star_does_not_invent_prediction(self):
        result = nine_star_ki_interpretation_planner.plan(
            {
                "question_text": "想记录一个外部应用给的九星气学资料",
                "home_star": "外部自定义星",
                "annual_star": "九紫",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_custom_nine_star_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造预言", unknown_items[0]["action_guidance"])

    def test_planner_blocks_costly_direction_fear_request(self):
        result = nine_star_ki_interpretation_planner.plan(
            {
                "question_text": "我要反复算到满意，用九星保证股票翻倍，还要看前任真实想法，五黄方位会死人必须高价化解",
                "home_star": "五黄",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_nine_star_ki"])
        self.assertIn("direction_fear_or_costly_cure", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class HumanDesignRequestGuardTests(unittest.TestCase):
    def test_low_risk_human_design_can_continue(self):
        result = human_design_request_guard.guard({"request_text": "想用人类图做低风险自我观察，已有 bodygraph：投射者、等待邀请、情绪权威、2/4 人生角色，只整理沟通和工作节奏，不诊断不投资不读心不报课不反复算"})
        self.assertTrue(result["can_continue_human_design"])
        self.assertEqual(result["consultation_intent"], "human_design_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_privacy_diagnosis_finance_control_paid_dependency_request_is_blocked(self):
        result = human_design_request_guard.guard({"request_text": "我要用前任出生资料看人类图，保证投资成功，诊断焦虑，还要控制伴侣并买高价解读，反复算到满意"})
        self.assertFalse(result["can_continue_human_design"])
        self.assertIn("birth_data_privacy", result["risk_flags"])
        self.assertIn("medical_or_mental_health", result["risk_flags"])
        self.assertIn("financial_or_career_guarantee", result["risk_flags"])
        self.assertIn("coercion_or_control", result["risk_flags"])
        self.assertIn("paid_pressure", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class HumanDesignChartRecorderTests(unittest.TestCase):
    def test_records_safe_chart_context(self):
        result = human_design_chart_recorder.record(
            {
                "question_text": "想用人类图做低风险自我观察，已有 bodygraph：投射者、等待邀请、情绪权威、2/4 人生角色，只整理沟通和工作节奏，不诊断不投资不读心不报课不反复算",
                "type": "投射者",
                "strategy": "等待邀请",
                "authority": "情绪权威",
                "profile": "2/4",
                "centers": "G中心, 喉中心",
                "channels": "1-8",
                "gates": "1, 8",
                "focus": "work_rhythm_reflection",
                "reality_constraints": "不报课, 不做职业决定",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["type"], "projector")
        self.assertEqual(result["authority"], "emotional_authority")
        self.assertEqual(result["centers"], ["G中心", "喉中心"])
        self.assertFalse(result["missing_fields"])

    def test_missing_chart_fields_are_marked(self):
        result = human_design_chart_recorder.record({"question_text": "想看人类图的沟通提醒"})
        self.assertTrue(result["is_valid"])
        self.assertIn("type", result["missing_fields"])
        self.assertIn("authority", result["missing_fields"])
        self.assertIn("profile", result["missing_fields"])

    def test_blocked_request_cannot_record_valid_chart(self):
        result = human_design_chart_recorder.record(
            {
                "question_text": "我要用前任出生资料看人类图，保证投资成功，诊断焦虑，还要控制伴侣并买高价解读，反复算到满意",
                "type": "投射者",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertIn("birth_data_privacy", result["risk_flags"])


class HumanDesignSymbolLookupTests(unittest.TestCase):
    def test_projector_lookup_keeps_non_deterministic_boundary(self):
        result = human_design_symbol_lookup.lookup({"query": "投射者", "focus": "work_rhythm_reflection"})
        self.assertEqual(result["symbol_code"], "projector")
        self.assertIn("识别", result["keywords"])
        self.assertIn("不写成低能量", result["action_guidance"])

    def test_chinese_authority_alias_normalizes(self):
        result = human_design_symbol_lookup.lookup({"query": "情绪权威"})
        self.assertEqual(result["symbol_code"], "emotional_authority")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            human_design_symbol_lookup.lookup({"query": "not-a-human-design-symbol"})


class HumanDesignInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_chart_layers_and_symbols(self):
        result = human_design_interpretation_planner.plan(
            {
                "question_text": "想用人类图做低风险自我观察，已有 bodygraph：投射者、等待邀请、情绪权威、2/4 人生角色，只整理沟通和工作节奏，不诊断不投资不读心不报课不反复算",
                "type": "投射者",
                "strategy": "等待邀请",
                "authority": "情绪权威",
                "profile": "2/4",
                "centers": "G中心, 喉中心",
                "channels": "1-8",
                "gates": "1, 8",
                "focus": "work_rhythm_reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("projector", symbol_codes)
        self.assertIn("emotional_authority", symbol_codes)
        self.assertIn("profile", symbol_codes)
        self.assertIn("defined_center", symbol_codes)
        self.assertIn("channel", symbol_codes)
        self.assertIn("gate", symbol_codes)
        self.assertEqual(result["interpretation_plan"]["symbol_count"], 8)

    def test_unknown_custom_symbol_does_not_invent_identity_claims(self):
        result = human_design_interpretation_planner.plan(
            {
                "question_text": "想记录一个外部应用给的人类图资料",
                "type": "课程自定义类型",
                "authority": "情绪权威",
                "profile": "2/4",
            }
        )
        self.assertTrue(result["is_valid"])
        unknown_items = [item for item in result["symbol_plans"] if item["symbol_code"] == "unknown_or_custom_human_design_symbol"]
        self.assertTrue(unknown_items)
        self.assertIn("不编造人格定论", unknown_items[0]["action_guidance"])

    def test_planner_blocks_privacy_diagnosis_paid_dependency_request(self):
        result = human_design_interpretation_planner.plan(
            {
                "question_text": "我要用前任出生资料看人类图，保证投资成功，诊断焦虑，还要控制伴侣并买高价解读，反复算到满意",
                "type": "投射者",
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_human_design"])
        self.assertIn("birth_data_privacy", result["risk_flags"])
        self.assertIn("repeated_dependency", result["risk_flags"])


class TalismanRequestGuardTests(unittest.TestCase):
    def test_low_risk_family_peace_charm_can_continue(self):
        result = talisman_request_guard.guard({"request_text": "想了解家人送的平安符，放钱包里当提醒，不做驱邪保证"})
        self.assertTrue(result["can_continue_talisman"])
        self.assertEqual(result["consultation_intent"], "talisman_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_dangerous_curse_medical_request_is_blocked(self):
        result = talisman_request_guard.guard({"request_text": "不用医生，烧符喝符水治疗失眠，还要诅咒前任回来"})
        self.assertFalse(result["can_continue_talisman"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("medical_claim", result["risk_flags"])
        self.assertIn("curse_or_coercion", result["risk_flags"])

    def test_expensive_purchase_pressure_is_blocked(self):
        result = talisman_request_guard.guard({"request_text": "大师说必须贷款买天价平安符，越贵越灵"})
        self.assertFalse(result["can_continue_talisman"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])


class TalismanRecordBuilderTests(unittest.TestCase):
    def test_records_family_gift_peace_charm(self):
        result = talisman_record_builder.record(
            {
                "intention_text": "想了解家人送的平安符，放钱包里当提醒，不做驱邪保证",
                "items": "平安符",
                "source_type": "family_gift",
                "source_label": "家人赠送",
                "use_context": "carrying",
                "budget_note": "已有物件，不新增购买",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["item_count"], 1)
        self.assertEqual(result["source_type"], "family_gift")
        self.assertFalse(result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = talisman_record_builder.record({"intention_text": "烧符喝符水治疗失眠", "items": "符箓", "source_label": "商家", "budget_note": "准备买"})
        self.assertFalse(result["is_valid"])
        self.assertIn("dangerous_ritual", result["risk_flags"])


class TalismanSymbolLookupTests(unittest.TestCase):
    def test_peace_charm_lookup_keeps_protection_boundary(self):
        result = talisman_symbol_lookup.lookup({"query": "平安符", "focus": "daily_safety_reminder"})
        self.assertEqual(result["canonical_name"], "平安符")
        self.assertEqual(result["symbol_code"], "peace_charm")
        self.assertIn("安心", result["keywords"])
        self.assertIn("不承诺挡灾", result["action_guidance"])

    def test_alias_normalizes(self):
        result = talisman_symbol_lookup.lookup({"query": "红绳"})
        self.assertEqual(result["symbol_code"], "red_string")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            talisman_symbol_lookup.lookup({"query": "not-a-talisman"})


class TalismanUsePlannerTests(unittest.TestCase):
    def test_planner_combines_record_and_symbol(self):
        result = talisman_use_planner.plan(
            {
                "intention_text": "想了解家人送的平安符，放钱包里当提醒，不做驱邪保证",
                "items": "平安符",
                "source_type": "family_gift",
                "source_label": "家人赠送",
                "use_context": "carrying",
                "budget_note": "已有物件，不新增购买",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["symbol_plans"]), 1)
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "peace_charm")
        self.assertEqual(result["use_plan"]["item_count"], 1)

    def test_unknown_source_specific_item_does_not_invent_power(self):
        result = talisman_use_planner.plan(
            {
                "intention_text": "想了解商家说的星辰护身法物，只做来源记录",
                "items": "星辰护身法物",
                "source_type": "store",
                "source_label": "商家",
                "use_context": "storage",
                "budget_note": "先不购买",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_source_specific")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_dangerous_curse_medical(self):
        result = talisman_use_planner.plan({"intention_text": "不用医生，烧符喝符水治疗失眠，还要诅咒前任回来", "items": "符箓", "source_type": "store", "source_label": "商家", "use_context": "wearing", "budget_note": "准备买贵的"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_talisman"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertIn("curse_or_coercion", result["risk_flags"])


class ColorRequestGuardTests(unittest.TestCase):
    def test_low_risk_interview_outfit_can_continue(self):
        result = color_request_guard.guard({"request_text": "明天面试想用五行颜色做提醒，已有白衬衫和绿色丝巾，不买新衣服"})
        self.assertTrue(result["can_continue_color"])
        self.assertEqual(result["consultation_intent"], "color_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_medical_finance_purchase_pressure_is_blocked(self):
        result = color_request_guard.guard({"request_text": "不用医生，穿红色一定治好焦虑，还能贷款投资发财，必须买天价开运外套"})
        self.assertFalse(result["can_continue_color"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("medical_or_safety", result["risk_flags"])
        self.assertIn("financial_claim", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])

    def test_appearance_label_is_blocked(self):
        result = color_request_guard.guard({"request_text": "这个颜色显丑显胖，穿错颜色的人看起来命苦"})
        self.assertFalse(result["can_continue_color"])
        self.assertIn("appearance_or_identity_label", result["risk_flags"])


class ColorProfileRecorderTests(unittest.TestCase):
    def test_records_existing_outfit_context(self):
        result = color_profile_recorder.record(
            {
                "intention_text": "明天面试想用五行颜色做提醒，已有白衬衫和绿色丝巾，不买新衣服",
                "scene": "outfit",
                "colors": "白色 绿色",
                "existing_items": "白衬衫、绿色丝巾",
                "budget_note": "不新增购买",
                "practical_constraints": "面试正式、舒适",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["scene"], "outfit")
        self.assertEqual(result["colors"], ["白色", "绿色"])
        self.assertFalse(result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = color_profile_recorder.record({"intention_text": "不用医生，穿红色治好焦虑", "colors": "红色", "budget_note": "已有"})
        self.assertFalse(result["is_valid"])
        self.assertIn("professional_replacement", result["risk_flags"])


class ColorSymbolLookupTests(unittest.TestCase):
    def test_white_lookup_keeps_boundary(self):
        result = color_symbol_lookup.lookup({"query": "白色", "focus": "interview_outfit"})
        self.assertEqual(result["canonical_name"], "白色/金色")
        self.assertEqual(result["symbol_code"], "white")
        self.assertEqual(result["element"], "metal")
        self.assertIn("清晰", result["keywords"])
        self.assertIn("不写成贵人保证", result["action_guidance"])

    def test_element_alias_normalizes(self):
        result = color_symbol_lookup.lookup({"query": "木"})
        self.assertEqual(result["symbol_code"], "green")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            color_symbol_lookup.lookup({"query": "not-a-color"})


class ColorPalettePlannerTests(unittest.TestCase):
    def test_planner_combines_profile_and_symbols(self):
        result = color_palette_planner.plan(
            {
                "intention_text": "明天面试想用五行颜色做提醒，已有白衬衫和绿色丝巾，不买新衣服，只做低风险穿搭建议",
                "scene": "outfit",
                "colors": "白色 绿色",
                "existing_items": "白衬衫、绿色丝巾",
                "budget_note": "不新增购买",
                "practical_constraints": "面试正式、舒适",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("white", symbol_codes)
        self.assertIn("green", symbol_codes)
        self.assertEqual(result["palette_plan"]["color_count"], 2)

    def test_unknown_personal_color_does_not_invent_power(self):
        result = color_palette_planner.plan(
            {
                "intention_text": "想了解商家说的星辰开运色，只做来源记录",
                "scene": "outfit",
                "colors": "星辰开运色",
                "existing_items": "没有",
                "budget_note": "先不购买",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_personal_color")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_medical_finance_purchase_pressure(self):
        result = color_palette_planner.plan({"intention_text": "不用医生，穿红色一定治好焦虑，还能贷款投资发财，必须买天价开运外套", "scene": "outfit", "colors": "红色", "existing_items": "没有", "budget_note": "准备贷款买"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_color"])
        self.assertIn("medical_or_safety", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])


class ZodiacRequestGuardTests(unittest.TestCase):
    def test_low_risk_benmingnian_request_can_continue(self):
        result = zodiac_request_guard.guard({"request_text": "我属龙，今年本命年，想了解太岁文化和低风险提醒，不做灾祸判断"})
        self.assertTrue(result["can_continue_zodiac"])
        self.assertEqual(result["consultation_intent"], "zodiac_symbolic_consultation")
        self.assertFalse(result["risk_flags"])

    def test_taisui_fear_purchase_pressure_is_blocked(self):
        result = zodiac_request_guard.guard({"request_text": "犯太岁一定会有血光大灾，不用医生，必须贷款买法物化解"})
        self.assertFalse(result["can_continue_zodiac"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("financial_claim", result["risk_flags"])
        self.assertIn("deterministic_fate", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])

    def test_relationship_discrimination_is_blocked(self):
        result = zodiac_request_guard.guard({"request_text": "属相不合必须分手，他属虎一定克妻"})
        self.assertFalse(result["can_continue_zodiac"])
        self.assertIn("relationship_discrimination", result["risk_flags"])


class ZodiacProfileRecorderTests(unittest.TestCase):
    def test_records_self_benmingnian_context(self):
        result = zodiac_profile_recorder.record(
            {
                "question_text": "我属龙，今年本命年，想了解太岁文化和低风险提醒",
                "birth_year": "1988",
                "zodiac": "龙",
                "focus": "benmingnian_reflection",
                "subject_scope": "self",
                "source_note": "家人口述和黄历说法，先当文化参考",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["zodiac"], "dragon")
        self.assertEqual(result["focus"], "benmingnian_reflection")
        self.assertFalse(result["missing_fields"])

    def test_blocked_request_cannot_record_as_valid(self):
        result = zodiac_profile_recorder.record({"question_text": "犯太岁必有大灾，不用医生", "zodiac": "龙", "source_note": "商家说法"})
        self.assertFalse(result["is_valid"])
        self.assertIn("professional_replacement", result["risk_flags"])


class ZodiacSymbolLookupTests(unittest.TestCase):
    def test_benmingnian_lookup_keeps_fear_boundary(self):
        result = zodiac_symbol_lookup.lookup({"query": "本命年", "focus": "yearly_reflection"})
        self.assertEqual(result["canonical_name"], "本命年")
        self.assertEqual(result["symbol_code"], "benmingnian")
        self.assertIn("周期回看", result["keywords"])
        self.assertIn("不写成必倒霉", result["action_guidance"])

    def test_alias_normalizes(self):
        result = zodiac_symbol_lookup.lookup({"query": "龙"})
        self.assertEqual(result["symbol_code"], "dragon")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            zodiac_symbol_lookup.lookup({"query": "not-a-zodiac"})


class ZodiacInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_profile_and_symbols(self):
        result = zodiac_interpretation_planner.plan(
            {
                "question_text": "我属龙，今年本命年，想了解太岁文化和低风险提醒，不做灾祸判断",
                "birth_year": "1988",
                "zodiac": "龙",
                "focus": "benmingnian_reflection",
                "subject_scope": "self",
                "source_note": "家人口述和黄历说法，先当文化参考",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["symbol_code"] for item in result["symbol_plans"]}
        self.assertIn("dragon", symbol_codes)
        self.assertIn("benmingnian", symbol_codes)
        self.assertIn("taisui", symbol_codes)
        self.assertGreaterEqual(result["interpretation_plan"]["symbol_count"], 2)

    def test_unknown_source_specific_symbol_does_not_invent_fate(self):
        result = zodiac_interpretation_planner.plan(
            {
                "question_text": "想了解家里说的星辰转运年，只做来源记录",
                "zodiac": "星辰转运年",
                "focus": "cultural_learning",
                "subject_scope": "self",
                "source_note": "家人口述",
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["symbol_plans"][0]["symbol_code"], "unknown_or_source_specific")
        self.assertIn("不编造", result["symbol_plans"][0]["action_guidance"])

    def test_planner_blocks_taisui_fear_purchase_pressure(self):
        result = zodiac_interpretation_planner.plan({"question_text": "犯太岁一定会有血光大灾，不用医生，必须贷款买法物化解", "zodiac": "龙", "focus": "taisui_culture", "source_note": "商家说法"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_zodiac"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertIn("expensive_purchase_pressure", result["risk_flags"])


class PhysiognomyRequestGuardTests(unittest.TestCase):
    def test_self_palmistry_symbolic_request_can_continue(self):
        result = physiognomy_request_guard.guard(
            {
                "request_text": "帮我看手相，生命线和事业线代表什么，只做象征解读",
                "subject_is_self": True,
            }
        )
        self.assertTrue(result["can_continue_physiognomy"])
        self.assertEqual(result["consent_state"], "self")
        self.assertFalse(result["risk_flags"])

    def test_third_party_health_lifespan_request_is_blocked(self):
        result = physiognomy_request_guard.guard({"request_text": "看他的面相和生命线是不是短命有病"})
        self.assertFalse(result["can_continue_physiognomy"])
        self.assertIn("health_diagnosis", result["risk_flags"])
        self.assertIn("lifespan_claim", result["risk_flags"])
        self.assertIn("third_party_nonconsent", result["risk_flags"])

    def test_appearance_discrimination_is_blocked(self):
        result = physiognomy_request_guard.guard(
            {
                "request_text": "看这个女生面相是不是丑而且克夫",
                "consent_obtained": True,
            }
        )
        self.assertFalse(result["can_continue_physiognomy"])
        self.assertIn("appearance_discrimination", result["risk_flags"])


class PhysiognomyObservationRecorderTests(unittest.TestCase):
    def test_records_palm_lines_from_self_observation(self):
        result = physiognomy_observation_recorder.record(
            {
                "observation_text": "我的生命线比较浅，事业线断续，想做象征反思",
                "subject_is_self": True,
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["modality"], "palm")
        self.assertIn("life_line", result["feature_codes"])
        self.assertIn("fate_line", result["feature_codes"])

    def test_nonconsented_third_party_observation_is_blocked(self):
        result = physiognomy_observation_recorder.record({"observation_text": "看他鼻相是不是富贵命"})
        self.assertFalse(result["is_valid"])
        self.assertIn("third_party_nonconsent", result["risk_flags"])


class PhysiognomySymbolLookupTests(unittest.TestCase):
    def test_life_line_lookup_keeps_lifespan_boundary(self):
        result = physiognomy_symbol_lookup.lookup({"query": "生命线", "focus": "self_reflection"})
        self.assertEqual(result["canonical_name"], "生命线")
        self.assertEqual(result["symbol_code"], "life_line")
        self.assertTrue(any("寿命" in item for item in result["prohibited_uses"]))

    def test_alias_normalizes(self):
        result = physiognomy_symbol_lookup.lookup({"query": "鼻相"})
        self.assertEqual(result["symbol_code"], "nose")

    def test_unknown_symbol_raises(self):
        with self.assertRaises(ValueError):
            physiognomy_symbol_lookup.lookup({"query": "不存在的相术符号"})


class PhysiognomyInterpretationPlannerTests(unittest.TestCase):
    def test_planner_combines_observation_and_symbols(self):
        result = physiognomy_interpretation_planner.plan(
            {
                "observation_text": "我的生命线比较浅，事业线断续，想做象征反思",
                "subject_is_self": True,
                "focus": "career reflection",
            }
        )
        self.assertTrue(result["is_valid"])
        symbol_codes = {item["feature_code"] for item in result["feature_plans"]}
        self.assertIn("life_line", symbol_codes)
        self.assertIn("fate_line", symbol_codes)
        self.assertEqual(result["synthesis"]["symbol_count"], 2)

    def test_planner_blocks_health_lifespan(self):
        result = physiognomy_interpretation_planner.plan({"observation_text": "看他的面相和生命线是不是短命有病"})
        self.assertFalse(result["is_valid"])
        self.assertFalse(result["can_continue_physiognomy"])
        self.assertIn("lifespan_claim", result["risk_flags"])


class FolkCustomLookupTests(unittest.TestCase):
    def test_festival_lookup_returns_safe_prompt(self):
        result = folk_custom_lookup.lookup({"query": "端午节", "category": "节日", "focus": "cultural_learning"})
        self.assertEqual(result["canonical_name"], "端午")
        self.assertEqual(result["system"], "chinese_folk_custom")
        self.assertIn("艾草", result["keywords"])
        self.assertTrue(result["prohibited_uses"])

    def test_taboo_alias_normalizes(self):
        result = folk_custom_lookup.lookup({"query": "插筷子", "category": "禁忌"})
        self.assertEqual(result["canonical_name"], "筷子插饭")
        self.assertEqual(result["category"], "taboo")

    def test_symbol_lookup(self):
        result = folk_custom_lookup.lookup({"query": "艾草", "category": "symbol"})
        self.assertEqual(result["category"], "symbol")
        self.assertIn("季节防护", result["keywords"])

    def test_life_event_lookup(self):
        result = folk_custom_lookup.lookup({"query": "乔迁", "category": "人生礼俗"})
        self.assertEqual(result["canonical_name"], "搬家")
        self.assertEqual(result["category"], "life_event")

    def test_unknown_custom_raises(self):
        with self.assertRaises(ValueError):
            folk_custom_lookup.lookup({"query": "不存在的民俗"})


class FolkTabooReframerTests(unittest.TestCase):
    def test_supernatural_fear_is_reframed(self):
        result = folk_taboo_reframer.reframe(
            {"request_text": "夜里吹口哨是不是一定会招鬼害家人", "source_type": "family", "region": "江南家庭说法"}
        )
        self.assertTrue(result["can_reframe_taboo"])
        self.assertEqual(result["taboo_name"], "夜里吹口哨")
        self.assertIn("deterministic_disaster_claim", result["risk_flags"])
        self.assertIn("supernatural_confirmation", result["risk_flags"])
        self.assertEqual(result["fear_level"], "medium")
        self.assertIn("鬼神", "".join(result["warnings"]))

    def test_pregnancy_professional_replacement_pauses(self):
        result = folk_taboo_reframer.reframe(
            {"request_text": "孕妇正月剪头发会不会害宝宝，不用看医生按禁忌就行吗", "source_type": "internet"}
        )
        self.assertFalse(result["can_reframe_taboo"])
        self.assertIn("pregnancy", result["context_flags"])
        self.assertIn("professional_replacement", result["risk_flags"])
        self.assertEqual(result["fear_level"], "high")

    def test_dangerous_ritual_blocks_reframe(self):
        result = folk_taboo_reframer.reframe({"request_text": "中元禁忌是不是要在密闭房间烧纸才不会冲撞"})
        self.assertFalse(result["can_reframe_taboo"])
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertTrue(any("危险仪式" in warning for warning in result["warnings"]))

    def test_unknown_source_is_labeled(self):
        result = folk_taboo_reframer.reframe({"request_text": "网上说筷子插饭一定倒霉"})
        self.assertTrue(result["can_reframe_taboo"])
        self.assertEqual(result["source_type"], "unknown")
        self.assertTrue(any("未验证" in warning for warning in result["warnings"]))


class FolkSourceRecorderTests(unittest.TestCase):
    def test_family_oral_source_records_as_local_context(self):
        result = folk_source_recorder.record(
            {
                "claim_text": "家里老人说江南搬家要先开灯和清扫入口",
                "custom_name": "搬家习俗",
                "source_type": "family_oral",
                "region": "江南",
                "informant_or_source_label": "外婆口述",
                "source_date_or_generation": "上一辈口述",
                "usage_context": "family_communication",
            }
        )
        self.assertEqual(result["source_reliability"], "local_oral_context")
        self.assertTrue(result["can_use_as_context"])
        self.assertTrue(result["can_treat_as_tradition"])
        self.assertEqual(result["missing_fields"], [])
        self.assertEqual(result["source_record"]["status"], "usable_context")

    def test_internet_claim_is_not_upgraded_to_tradition(self):
        result = folk_source_recorder.record(
            {
                "claim_text": "网上说筷子插饭一定倒霉",
                "source_type": "internet_claim",
                "informant_or_source_label": "短视频平台说法",
            }
        )
        self.assertEqual(result["source_reliability"], "unverified_internet_claim")
        self.assertFalse(result["can_treat_as_tradition"])
        self.assertIn("supernatural_certainty", result["risk_flags"])
        self.assertIn("evidence_items", result["missing_fields"])
        self.assertTrue(any("不能直接写成传统民俗" in warning for warning in result["authority_warnings"]))

    def test_commercial_claim_flags_interest_and_outcome_claim(self):
        result = folk_source_recorder.record(
            {
                "claim_text": "商家课程说购买开运物保证转运，这是正统民俗",
                "custom_name": "开运物说法",
                "source_type": "commercial_claim",
                "informant_or_source_label": "商家课程",
                "evidence_items": ["课程页截图"],
            }
        )
        self.assertEqual(result["source_reliability"], "commercial_interest_claim")
        self.assertIn("commercial_interest", result["risk_flags"])
        self.assertFalse(result["can_treat_as_tradition"])

    def test_dangerous_ritual_source_needs_safety_review(self):
        result = folk_source_recorder.record(
            {
                "claim_text": "短视频说中元必须密闭烧纸才不会冲撞",
                "source_type": "internet_claim",
                "informant_or_source_label": "短视频平台说法",
                "evidence_items": ["视频标题"],
            }
        )
        self.assertFalse(result["can_use_as_context"])
        self.assertIn("dangerous_action", result["risk_flags"])
        self.assertEqual(result["source_record"]["status"], "safety_review_needed")
        self.assertIn("route_dangerous_ritual_parts_to_ritual_safety_tools", result["next_steps"])

    def test_missing_source_fields_are_reported(self):
        result = folk_source_recorder.record({"claim_text": "这个说法是真的吗"})
        self.assertEqual(result["source_type"], "unknown")
        self.assertIn("custom_name", result["missing_fields"])
        self.assertIn("source_type", result["missing_fields"])
        self.assertTrue(result["questions_to_ask"])


class SymbolicDepthLookupTests(unittest.TestCase):
    def test_tarot_reversal_lookup_returns_boundary_and_toolchain(self):
        result = symbolic_depth_lookup.lookup({"domain": "tarot", "query": "逆位"})
        self.assertEqual(result["domain"], "tarot")
        self.assertGreaterEqual(result["match_count"], 1)
        first = result["entries"][0]
        self.assertEqual(first["domain"], "tarot")
        self.assertIn("boundary", first)
        self.assertIn("example", first)
        self.assertIn("mystic_output_lint", first["toolchain"])

    def test_cross_domain_privacy_lookup_finds_mingli_entry(self):
        result = symbolic_depth_lookup.lookup({"query": "第三方同意"})
        entry_ids = {entry["entry_id"] for entry in result["entries"]}
        self.assertIn("mingli-privacy-aware-chart", entry_ids)
        self.assertTrue(any("第三方" in entry["boundary"] for entry in result["entries"]))

    def test_yijing_line_lookup_recommends_line_tool(self):
        result = symbolic_depth_lookup.lookup({"domain": "yijing", "query": "动爻", "limit": 2})
        self.assertTrue(result["entries"])
        toolchains = [tool for entry in result["entries"] for tool in entry["toolchain"]]
        self.assertIn("yijing_line_lookup", toolchains)

    def test_domain_alias_normalizes(self):
        result = symbolic_depth_lookup.lookup({"domain": "feng_shui", "query": "方位"})
        self.assertEqual(result["domain"], "fengshui")
        self.assertTrue(result["entries"])

    def test_unknown_domain_raises(self):
        with self.assertRaises(ValueError):
            symbolic_depth_lookup.lookup({"domain": "astrology", "query": "natal"})

    def test_invalid_limit_raises(self):
        with self.assertRaises(ValueError):
            symbolic_depth_lookup.lookup({"domain": "tarot", "limit": 13})


class SymbolicCaseLibraryTests(unittest.TestCase):
    def test_tarot_work_query_returns_safe_case(self):
        result = symbolic_case_library.lookup({"domain": "tarot", "query": "工作", "limit": 2})
        self.assertEqual(result["tool"], "symbolic_case_library")
        self.assertEqual(result["domain"], "tarot")
        self.assertGreaterEqual(result["case_count"], 1)
        self.assertTrue(result["cases"][0]["avoid_language"])
        self.assertIn("mystic_output_lint", result["cases"][0]["recommended_tools"])

    def test_ritual_blocked_then_safe_filter(self):
        result = symbolic_case_library.lookup({"domain": "ritual", "scenario": "blocked-then-safe"})
        self.assertEqual(result["scenario"], "blocked_then_safe")
        self.assertEqual(result["cases"][0]["case_id"], "ritual-sealed-fire-request")
        self.assertIn("无火", "".join(result["cases"][0]["safe_interpretation"] + [result["cases"][0]["sample_language"]]))

    def test_third_party_query_finds_mingli_privacy_case(self):
        result = symbolic_case_library.lookup({"query": "第三方出生资料"})
        case_ids = {case["case_id"] for case in result["cases"]}
        self.assertIn("mingli-third-party-birth-data", case_ids)

    def test_unknown_case_domain_raises(self):
        with self.assertRaises(ValueError):
            symbolic_case_library.lookup({"domain": "astrology", "query": "natal"})

    def test_invalid_case_limit_raises(self):
        with self.assertRaises(ValueError):
            symbolic_case_library.lookup({"limit": 19})


class KnowledgeCoverageAuditTests(unittest.TestCase):
    def test_current_repository_has_complete_domain_coverage(self):
        result = knowledge_coverage_audit.audit()
        self.assertEqual(result["tool"], "knowledge_coverage_audit")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["domain_count"], 61)
        self.assertEqual(result["failed_domain_count"], 0)
        self.assertEqual({domain["level"] for domain in result["domains"]}, {"L3 可验证"})

    def test_common_coverage_includes_human_dashboard_assets(self):
        result = knowledge_coverage_audit.audit()
        self.assertTrue(result["common"]["is_complete"])
        present = set(result["common"]["sections"]["knowledge_base"]["present"])
        self.assertIn("README.md", present)
        self.assertIn("知识库/看板.md", present)
        self.assertIn("知识库/仪表盘.md", present)

    def test_tool_chain_checks_script_schema_and_spec(self):
        result = knowledge_coverage_audit.audit()
        tarot = next(domain for domain in result["domains"] if domain["domain"] == "tarot")
        tool_names = {item["tool"] for item in tarot["sections"]["tools"]["present"]}
        self.assertIn("tarot_interpretation_planner", tool_names)
        self.assertFalse(tarot["sections"]["tools"]["missing"])


class KnowledgeNavigationBuilderTests(unittest.TestCase):
    def test_current_repository_navigation_is_valid(self):
        result = knowledge_navigation_builder.build()
        self.assertEqual(result["tool"], "knowledge_navigation_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["domain_count"], 61)
        self.assertEqual(result["complete_domain_count"], 61)
        self.assertGreaterEqual(result["document_count"], 60)
        self.assertGreaterEqual(result["tool_count"], 62)

    def test_generated_markdown_links_key_human_entries(self):
        result = knowledge_navigation_builder.build()
        markdown = result["generated_markdown"]
        self.assertIn("[总览](00-总览.md)", markdown)
        self.assertIn("[Agent Tool Catalog](../agent-tools/tool-catalog.md)", markdown)
        self.assertIn("tarot-symbolic-reading", markdown)
        self.assertIn("看板 Doing", markdown)

    def test_kanban_counts_are_read_from_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kb = root / "知识库"
            kb.mkdir()
            (kb / "看板.md").write_text(
                "# 看板\n\n## Doing\n\n| ID | 任务 |\n| --- | --- |\n| K-001 | A |\n\n## Done\n\n| ID | 任务 |\n| --- | --- |\n| T-001 | B |\n",
                encoding="utf-8",
            )
            counts = knowledge_navigation_builder.count_kanban(root)
        self.assertEqual(counts["Doing"], 1)
        self.assertEqual(counts["Done"], 1)
        self.assertEqual(counts["Backlog"], 0)


class ContentReviewPacketBuilderTests(unittest.TestCase):
    def test_current_repository_review_packets_are_ready_not_approved(self):
        result = content_review_packet_builder.build()
        self.assertEqual(result["tool"], "content_review_packet_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["domain_count"], 61)
        self.assertEqual(result["ready_for_review_count"], 61)
        self.assertEqual(result["approved_count"], 0)

    def test_tarot_packet_lists_files_tools_and_review_questions(self):
        result = content_review_packet_builder.build()
        tarot = next(packet for packet in result["packets"] if packet["domain"] == "tarot")
        self.assertEqual(tarot["review_status"], "ready_for_human_review")
        self.assertIn("tarot_combination_planner", tarot["tool_chain"])
        self.assertIn("知识库/SOP/01-塔罗解读.md", tarot["files_to_review"]["sop"])
        self.assertTrue(any("逆位" in question for question in tarot["review_questions"]))

    def test_generated_markdown_keeps_human_approval_as_open_item(self):
        result = content_review_packet_builder.build()
        markdown = result["generated_markdown"]
        self.assertIn("# 内容审校包", markdown)
        self.assertIn("不证明已经审完", markdown)
        self.assertIn("content_expert_approval_missing", markdown)
        self.assertIn("| 已获内容批准 | 0 |", markdown)


class ContentReviewFeedbackRecorderTests(unittest.TestCase):
    def test_approved_review_can_count_as_content_approval(self):
        result = content_review_feedback_recorder.record(
            {
                "domain": "tarot",
                "reviewer": "tarot-reviewer",
                "review_date": "2026-07-02",
                "decision": "approved",
                "approved_scope": ["塔罗 SOP、知识卡、Skill 和工具 spec"],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["status"], "approved")
        self.assertTrue(result["can_count_as_content_approval"])
        self.assertFalse(result["errors"])

    def test_changes_requested_generates_kanban_updates(self):
        result = content_review_feedback_recorder.record(
            {
                "domain": "fengshui",
                "reviewer": "fengshui-reviewer",
                "review_date": "2026-07-02",
                "decision": "changes_requested",
                "approved_scope": ["风水 SOP 初审"],
                "required_corrections": ["补充玄空飞星字段不足时的拒绝样例"],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["status"], "needs_revision")
        self.assertFalse(result["can_count_as_content_approval"])
        self.assertEqual(result["kanban_updates"][0]["suggested_id"], "REV-FENGSHUI-001")

    def test_missing_required_evidence_is_not_approved(self):
        result = content_review_feedback_recorder.record(
            {
                "domain": "tarot",
                "decision": "approved",
                "approved_scope": ["塔罗 SOP"],
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "not_approved")
        self.assertFalse(result["can_count_as_content_approval"])
        self.assertIn("missing_reviewer", result["errors"])
        self.assertIn("missing_review_date", result["errors"])


class CodexSkillBlueprintValidatorTests(unittest.TestCase):
    def test_all_skill_blueprints_are_valid(self):
        result = codex_skill_blueprint_validator.validate()
        self.assertEqual(result["tool"], "codex_skill_blueprint_validator")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["skill_count"], 61)
        self.assertEqual(result["invalid_skill_count"], 0)

    def test_frontmatter_keys_are_minimal(self):
        result = codex_skill_blueprint_validator.validate()
        for skill in result["skills"]:
            self.assertEqual(skill["frontmatter_keys"], ["description", "name"])
            self.assertFalse(skill["missing_references"])
            self.assertFalse(skill["missing_tool_scripts"])

    def test_index_tools_match_skill_hooks(self):
        result = codex_skill_blueprint_validator.validate()
        tarot = next(skill for skill in result["skills"] if skill["skill"] == "tarot-symbolic-reading")
        self.assertIn("tarot_interpretation_planner", tarot["referenced_tools"])
        self.assertFalse(tarot["errors"])


class CodexSkillInstallerTests(unittest.TestCase):
    def test_dry_run_plans_all_valid_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = codex_skill_installer.install_plan(codex_home=tmp)
        self.assertEqual(result["tool"], "codex_skill_installer")
        self.assertTrue(result["is_valid"])
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["skill_count"], 61)
        self.assertEqual(result["copied_count"], 0)
        self.assertEqual({item["action"] for item in result["actions"]}, {"create"})

    def test_install_copies_selected_skill_to_temp_codex_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = codex_skill_installer.install_plan(
                codex_home=tmp,
                skills=["tarot-symbolic-reading"],
                dry_run=False,
            )
            installed = Path(tmp) / "skills" / "tarot-symbolic-reading" / "SKILL.md"
            second = codex_skill_installer.install_plan(
                codex_home=tmp,
                skills=["tarot-symbolic-reading"],
            )
            installed_exists = installed.exists()
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["copied_count"], 1)
        self.assertTrue(installed_exists)
        self.assertEqual(second["actions"][0]["action"], "already_current")

    def test_existing_different_skill_conflicts_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skills" / "tarot-symbolic-reading"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("---\nname: different\n---\n", encoding="utf-8")
            result = codex_skill_installer.install_plan(
                codex_home=tmp,
                skills=["tarot-symbolic-reading"],
            )
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["conflict_count"], 1)
        self.assertEqual(result["actions"][0]["action"], "conflict_existing")


class SkillInstallReadinessReportTests(unittest.TestCase):
    def test_dry_run_report_is_ready_for_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = skill_install_readiness_report.build(codex_home=tmp)
        self.assertEqual(result["tool"], "skill_install_readiness_report")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["status"], "ready_for_install_approval")
        self.assertTrue(result["requires_explicit_approval"])
        self.assertEqual(result["skill_count"], 61)
        self.assertEqual(result["create_count"], 61)
        self.assertIn("--install", result["install_command"])

    def test_single_skill_command_limits_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = skill_install_readiness_report.build(codex_home=tmp, skills=["tarot-symbolic-reading"])
        self.assertEqual(result["skill_count"], 1)
        self.assertIn("--skill tarot-symbolic-reading", result["install_command"])
        self.assertNotIn("--skill feng-shui-space-audit", result["install_command"])

    def test_existing_different_skill_blocks_readiness(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skills" / "tarot-symbolic-reading"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("---\nname: different\n---\n", encoding="utf-8")
            result = skill_install_readiness_report.build(codex_home=tmp, skills=["tarot-symbolic-reading"])
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["conflict_count"], 1)
        self.assertIn("tarot-symbolic-reading", result["blockers"][0])


class SopTraceabilityMatrixBuilderTests(unittest.TestCase):
    def test_current_repository_traceability_is_valid(self):
        result = sop_traceability_matrix_builder.build()
        self.assertEqual(result["tool"], "sop_traceability_matrix_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["domain_count"], 61)
        self.assertEqual(result["traceable_domain_count"], 61)
        self.assertEqual(result["missing_link_count"], 0)

    def test_tarot_trace_links_sop_skill_tools_and_verification(self):
        result = sop_traceability_matrix_builder.build()
        tarot = next(row for row in result["rows"] if row["domain"] == "tarot")
        self.assertIn("知识库/SOP/01-塔罗解读.md", tarot["sop"])
        self.assertIn("codex-skills/tarot-symbolic-reading/SKILL.md", tarot["skill"])
        self.assertIn("tarot_combination_planner", tarot["tool_chain"])
        self.assertIn("tarot_combination_planner", tarot["mentioned_in_sop"])
        self.assertIn("skill_replay_runner", tarot["verification_tools"])

    def test_generated_markdown_summarizes_traceability(self):
        result = sop_traceability_matrix_builder.build()
        markdown = result["generated_markdown"]
        self.assertIn("# SOP/Tool/Skill 追踪矩阵", markdown)
        self.assertIn("| 可追踪领域 | 61 |", markdown)
        self.assertIn("tarot-symbolic-reading", markdown)
        self.assertIn("traceable", markdown)


class PilotReadinessReportTests(unittest.TestCase):
    def test_pilot_readiness_separates_internal_dry_run_from_public_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = pilot_readiness_report.build(codex_home=tmp)
        self.assertEqual(result["tool"], "pilot_readiness_report")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["pilot_status"], "ready_for_internal_dry_run")
        self.assertEqual(result["public_release_status"], "blocked_by_external_evidence")
        self.assertEqual(result["external_blocker_count"], 3)

    def test_summary_includes_route_trace_install_and_review_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = pilot_readiness_report.build(codex_home=tmp)
        self.assertEqual(result["summary"]["complete_domain_count"], 61)
        self.assertEqual(result["summary"]["route_passed_count"], 63)
        self.assertEqual(result["summary"]["traceable_domain_count"], 61)
        self.assertEqual(result["summary"]["skill_install_readiness"], "ready_for_install_approval")
        self.assertEqual(result["summary"]["content_review_approved_count"], 0)

    def test_external_blockers_name_required_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = pilot_readiness_report.build(codex_home=tmp)
        blockers = {item["blocker"]: item for item in result["external_blockers"]}
        self.assertIn("actual_skill_install_requires_user_confirmation", blockers)
        self.assertIn("real_anonymized_transcripts_needed", blockers)
        self.assertIn("content_expert_approval_needed", blockers)
        self.assertTrue(all(item["required_evidence"] for item in blockers.values()))


class ExternalEvidenceIntakeBuilderTests(unittest.TestCase):
    def test_builds_three_open_intake_items_for_external_blockers(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = external_evidence_intake_builder.build(codex_home=tmp)
        self.assertEqual(result["tool"], "external_evidence_intake_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["status"], "ready_for_external_collection")
        self.assertEqual(result["intake_count"], 3)
        self.assertEqual(result["open_intake_count"], 3)
        self.assertEqual(
            {item["blocker"] for item in result["intake_items"]},
            {
                "actual_skill_install_requires_user_confirmation",
                "real_anonymized_transcripts_needed",
                "content_expert_approval_needed",
            },
        )

    def test_intake_items_include_fields_acceptance_commands_and_kanban(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = external_evidence_intake_builder.build(codex_home=tmp)
        transcripts = next(item for item in result["intake_items"] if item["intake_id"] == "EXT-002")
        self.assertIn("source_label", transcripts["required_fields"])
        self.assertTrue(any("ready_for_replay=true" in item for item in transcripts["evidence_acceptance"]))
        self.assertTrue(any("transcript_fixture_builder.py" in command for command in transcripts["commands"]))
        self.assertEqual(transcripts["kanban_ids"], ["K-021"])

    def test_generated_markdown_points_to_no_false_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = external_evidence_intake_builder.build(codex_home=tmp)
        markdown = external_evidence_intake_builder.render_markdown(result)
        self.assertIn("# 外部证据入口包", markdown)
        self.assertIn("它不表示证据已经收齐", markdown)
        self.assertIn("EXT-001", markdown)
        self.assertIn("EXT-003", markdown)


class AgentRuntimeHandoffBuilderTests(unittest.TestCase):
    def test_builds_runtime_handoff_from_current_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = agent_runtime_handoff_builder.build(codex_home=tmp)
        self.assertEqual(result["tool"], "agent_runtime_handoff_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["handoff_status"], "ready_for_runtime_dry_run")
        self.assertEqual(result["skill_count"], 61)
        self.assertGreaterEqual(result["tool_count"], 208)
        self.assertEqual(len(result["open_external_items"]), 3)

    def test_runtime_handoff_names_router_lint_and_safety_invariants(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = agent_runtime_handoff_builder.build(codex_home=tmp)
        entrypoints = {item["entrypoint"]: item["tool"] for item in result["entrypoints"]}
        self.assertEqual(entrypoints["request_routing"], "agent_workflow_router")
        self.assertEqual(entrypoints["output_safety_lint"], "mystic_output_lint")
        checks = {item["check"]: item for item in result["readiness_checks"]}
        self.assertIn("runtime_dry_run", checks)
        self.assertTrue(checks["runtime_dry_run"]["passed"])
        self.assertIn("tool_wrapper_manifest", checks)
        self.assertTrue(checks["tool_wrapper_manifest"]["passed"])
        self.assertIn("tool_definition_export", checks)
        self.assertTrue(checks["tool_definition_export"]["passed"])
        self.assertIn("tool_definition_validation", checks)
        self.assertTrue(checks["tool_definition_validation"]["passed"])
        self.assertIn("tool_registry", checks)
        self.assertTrue(checks["tool_registry"]["passed"])
        self.assertIn("tool_registry_validation", checks)
        self.assertTrue(checks["tool_registry_validation"]["passed"])
        self.assertTrue(any("red/orange" in item for item in result["safety_invariants"]))
        self.assertIn("python3 agent-tools/scripts/agent_runtime_dry_run_runner.py", result["verification_commands"])
        self.assertIn("python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py", result["verification_commands"])
        self.assertIn("python3 agent-tools/scripts/agent_tool_definition_exporter.py", result["verification_commands"])
        self.assertIn("python3 agent-tools/scripts/agent_tool_definition_validator.py", result["verification_commands"])
        self.assertIn("python3 agent-tools/scripts/agent_tool_registry_builder.py", result["verification_commands"])
        self.assertIn("python3 agent-tools/scripts/agent_tool_registry_validator.py", result["verification_commands"])

    def test_generated_markdown_is_a_handoff_not_public_release_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = agent_runtime_handoff_builder.build(codex_home=tmp)
        markdown = agent_runtime_handoff_builder.render_markdown(result)
        self.assertIn("# Agent 运行时交接包", markdown)
        self.assertIn("runtime dry-run", markdown)
        self.assertIn("不证明已经完成真实安装或公开发布", markdown)
        self.assertIn("actual_skill_install_requires_user_confirmation", markdown)


class ReleaseGateRunnerTests(unittest.TestCase):
    def test_selected_release_gates_pass(self):
        result = release_gate_runner.run(gates=["schema_json", "markdown_links"])
        self.assertEqual(result["tool"], "release_gate_runner")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gate_count"], 2)
        self.assertEqual(result["failed_count"], 0)

    def test_json_script_gate_passes(self):
        result = release_gate_runner.run(gates=["codex_skill_blueprint_validator"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["gate_id"], "codex_skill_blueprint_validator")
        self.assertEqual(result["gates"][0]["summary"]["tool"], "codex_skill_blueprint_validator")

    def test_skill_installer_gate_is_dry_run(self):
        result = release_gate_runner.run(gates=["codex_skill_installer"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["gate_id"], "codex_skill_installer")
        self.assertTrue(result["gates"][0]["summary"]["dry_run"])

    def test_external_evidence_intake_gate_passes_without_claiming_evidence_complete(self):
        result = release_gate_runner.run(gates=["external_evidence_intake_builder"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["summary"]["status"], "ready_for_external_collection")
        self.assertEqual(result["gates"][0]["summary"]["open_intake_count"], 3)

    def test_agent_runtime_handoff_gate_passes_for_dry_run(self):
        result = release_gate_runner.run(gates=["agent_runtime_handoff_builder"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["summary"]["handoff_status"], "ready_for_runtime_dry_run")
        self.assertEqual(result["gates"][0]["summary"]["open_external_count"], 3)

    def test_agent_runtime_dry_run_gate_passes(self):
        result = release_gate_runner.run(gates=["agent_runtime_dry_run_runner"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["summary"]["tool"], "agent_runtime_dry_run_runner")

    def test_agent_tool_wrapper_manifest_gate_passes(self):
        result = release_gate_runner.run(gates=["agent_tool_wrapper_manifest_builder"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["summary"]["tool"], "agent_tool_wrapper_manifest_builder")

    def test_agent_tool_definition_export_gate_passes(self):
        result = release_gate_runner.run(gates=["agent_tool_definition_exporter"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["summary"]["tool"], "agent_tool_definition_exporter")

    def test_agent_tool_definition_validation_gate_passes(self):
        result = release_gate_runner.run(gates=["agent_tool_definition_validator"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["summary"]["tool"], "agent_tool_definition_validator")

    def test_agent_tool_registry_gate_passes(self):
        result = release_gate_runner.run(gates=["agent_tool_registry_builder"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["summary"]["tool"], "agent_tool_registry_builder")

    def test_agent_tool_registry_validation_gate_passes(self):
        result = release_gate_runner.run(gates=["agent_tool_registry_validator"])
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["gates"][0]["summary"]["tool"], "agent_tool_registry_validator")

    def test_unknown_release_gate_raises(self):
        with self.assertRaises(ValueError):
            release_gate_runner.run(gates=["missing_gate"])


class AgentToolWrapperManifestBuilderTests(unittest.TestCase):
    def test_builds_wrappers_for_all_ready_tools(self):
        result = agent_tool_wrapper_manifest_builder.build()
        self.assertEqual(result["tool"], "agent_tool_wrapper_manifest_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["blocked_count"], 0)
        self.assertEqual(result["wrapper_count"], result["wrappable_count"])
        self.assertGreaterEqual(result["wrapper_count"], 204)

    def test_tarot_wrapper_has_command_schema_skill_and_safety_tags(self):
        result = agent_tool_wrapper_manifest_builder.build()
        wrapper = next(item for item in result["wrappers"] if item["name"] == "tarot_spread_selector")
        self.assertEqual(wrapper["command"], ["python3", "agent-tools/scripts/tarot_spread_selector.py"])
        self.assertEqual(wrapper["input_schema_path"], "agent-tools/schemas/tarot-spread-selector.schema.json")
        self.assertIn("tarot", wrapper["domains"])
        self.assertIn("tarot-symbolic-reading", wrapper["skills"])
        self.assertIn("symbolic_interpretation_only", wrapper["safety_tags"])

    def test_ritual_wrapper_marks_low_risk_boundary(self):
        result = agent_tool_wrapper_manifest_builder.build()
        wrapper = next(item for item in result["wrappers"] if item["name"] == "ritual_low_risk_protocol")
        self.assertIn("low_risk_only", wrapper["safety_tags"])
        self.assertIn("dangerous_materials_guarded", wrapper["safety_tags"])

    def test_generated_markdown_does_not_claim_server_started(self):
        result = agent_tool_wrapper_manifest_builder.build()
        markdown = agent_tool_wrapper_manifest_builder.render_markdown(result)
        self.assertIn("# Agent Tool Wrapper Manifest", markdown)
        self.assertIn("不表示已经启动 MCP/API server", markdown)
        self.assertIn("tarot_spread_selector", markdown)


class AgentToolDefinitionExporterTests(unittest.TestCase):
    def test_exports_definitions_for_all_wrappable_tools(self):
        result = agent_tool_definition_exporter.build()
        self.assertEqual(result["tool"], "agent_tool_definition_exporter")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["definition_count"], result["openai_tool_count"])
        self.assertEqual(result["definition_count"], result["source_wrapper_count"])
        self.assertGreaterEqual(result["definition_count"], 204)

    def test_definition_preserves_command_schema_and_metadata(self):
        result = agent_tool_definition_exporter.build()
        definition = next(item for item in result["definitions"] if item["name"] == "tarot_spread_selector")
        self.assertEqual(definition["command"], ["python3", "agent-tools/scripts/tarot_spread_selector.py"])
        self.assertEqual(definition["metadata"]["schema_path"], "agent-tools/schemas/tarot-spread-selector.schema.json")
        self.assertIn("tarot", definition["metadata"]["domains"])
        self.assertIn("symbolic_interpretation_only", definition["metadata"]["safety_tags"])

    def test_openai_tool_shape_contains_function_parameters(self):
        result = agent_tool_definition_exporter.build()
        tool = next(item for item in result["openai_tools"] if item["function"]["name"] == "tarot_spread_selector")
        self.assertEqual(tool["type"], "function")
        self.assertIn("parameters", tool["function"])
        self.assertEqual(tool["function"]["parameters"]["title"], "TarotSpreadSelector")

    def test_generated_markdown_does_not_claim_runtime_started(self):
        result = agent_tool_definition_exporter.build()
        markdown = agent_tool_definition_exporter.render_markdown(result)
        self.assertIn("# Agent Tool Definition Export", markdown)
        self.assertIn("不执行工具", markdown)
        self.assertIn("tarot_spread_selector", markdown)


class AgentToolDefinitionValidatorTests(unittest.TestCase):
    def test_validates_exported_definitions_and_openai_tools(self):
        result = agent_tool_definition_validator.build()
        self.assertEqual(result["tool"], "agent_tool_definition_validator")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["failed_definition_count"], 0)
        self.assertEqual(result["failed_openai_tool_count"], 0)
        self.assertEqual(result["valid_definition_count"], result["definition_count"])
        self.assertGreaterEqual(result["definition_count"], 204)

    def test_tarot_definition_validation_keeps_domains_and_safety_tags(self):
        result = agent_tool_definition_validator.build()
        item = next(record for record in result["definition_results"] if record["name"] == "tarot_spread_selector")
        self.assertTrue(item["is_valid"])
        self.assertIn("tarot", item["domains"])
        self.assertIn("professional_boundary_required", item["safety_tags"])

    def test_invalid_definition_reports_shape_errors(self):
        errors = agent_tool_definition_validator.validate_definition(
            {
                "name": "bad-name!",
                "description": "",
                "input_schema": {"type": "string"},
                "command": ["node", "missing.js"],
                "metadata": {},
            },
            Path(".").resolve(),
        )
        self.assertIn("invalid_name", errors)
        self.assertIn("missing_description", errors)
        self.assertIn("input_schema_not_object", errors)
        self.assertIn("invalid_command", errors)

    def test_generated_markdown_summarizes_validation(self):
        result = agent_tool_definition_validator.build()
        markdown = agent_tool_definition_validator.render_markdown(result)
        self.assertIn("# Agent Tool Definition Validation", markdown)
        self.assertIn("Definition", markdown)
        self.assertIn("tarot_spread_selector", markdown)


class AgentToolRegistryBuilderTests(unittest.TestCase):
    def test_builds_ready_runtime_registry(self):
        result = agent_tool_registry_builder.build()
        self.assertEqual(result["tool"], "agent_tool_registry_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["registry_status"], "ready_for_runtime_registration")
        self.assertGreaterEqual(result["tool_count"], 204)
        self.assertIn("tarot", result["by_domain"])
        self.assertIn("tarot-symbolic-reading", result["by_skill"])

    def test_registration_order_starts_with_safety_bootstrap(self):
        result = agent_tool_registry_builder.build()
        self.assertEqual(result["registration_order"][:3], ["mystic_intake_triage", "agent_workflow_router", "mystic_output_lint"])
        self.assertIn("ritual_safety_check", result["safety_bootstrap"])
        self.assertLess(result["registration_order"].index("ritual_safety_check"), result["registration_order"].index("ritual_low_risk_protocol"))

    def test_registry_entry_preserves_command_and_safety_tags(self):
        result = agent_tool_registry_builder.build()
        entry = next(item for item in result["entries"] if item["name"] == "ritual_low_risk_protocol")
        self.assertEqual(entry["command"], ["python3", "agent-tools/scripts/ritual_low_risk_protocol.py"])
        self.assertIn("low_risk_only", entry["safety_tags"])
        self.assertIn("ritual-safety-advisor", entry["skills"])

    def test_generated_registry_markdown_lists_runtime_contract(self):
        result = agent_tool_registry_builder.build()
        markdown = agent_tool_registry_builder.render_markdown(result)
        self.assertIn("# Agent Tool Registry", markdown)
        self.assertIn("registration_order", markdown)
        self.assertIn("mystic_intake_triage", markdown)


class AgentToolRegistryValidatorTests(unittest.TestCase):
    def test_validates_runtime_registry_indexes_and_bootstrap(self):
        result = agent_tool_registry_validator.build()
        self.assertEqual(result["tool"], "agent_tool_registry_validator")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["error_count"], 0)
        self.assertEqual(result["failed_skill_count"], 0)
        self.assertEqual(result["bootstrap_prefix"][:3], ["mystic_intake_triage", "agent_workflow_router", "mystic_output_lint"])
        self.assertGreaterEqual(result["tool_count"], 204)

    def test_required_skill_tools_include_ritual_skill_after_index_fix(self):
        result = agent_tool_registry_validator.build()
        ritual = next(item for item in result["skill_results"] if item["skill"] == "ritual-safety-advisor")
        self.assertTrue(ritual["is_valid"])
        self.assertEqual(ritual["missing_required_tools"], [])

    def test_validator_reports_missing_skill_bootstrap_tools(self):
        registry = agent_tool_registry_builder.build()
        registry["by_skill"]["tarot-symbolic-reading"] = [
            tool for tool in registry["by_skill"]["tarot-symbolic-reading"] if tool != "mystic_output_lint"
        ]
        errors, skill_results = agent_tool_registry_validator.validate_registry(registry)
        self.assertIn("skill_missing_tarot-symbolic-reading_mystic_output_lint", errors)
        tarot = next(item for item in skill_results if item["skill"] == "tarot-symbolic-reading")
        self.assertFalse(tarot["is_valid"])

    def test_generated_registry_validation_markdown_lists_skill_checks(self):
        result = agent_tool_registry_validator.build()
        markdown = agent_tool_registry_validator.render_markdown(result)
        self.assertIn("# Agent Tool Registry Validation", markdown)
        self.assertIn("Skill Checks", markdown)
        self.assertIn("ritual-safety-advisor", markdown)


class ReleaseManifestBuilderTests(unittest.TestCase):
    def gate_report(self, valid=True):
        return {
            "tool": "release_gate_runner",
            "gate_count": 3,
            "passed_count": 3 if valid else 2,
            "failed_count": 0 if valid else 1,
            "is_valid": valid,
            "gates": [
                {"gate_id": "schema_json", "passed": True, "summary": {"schema_count": 281}},
                {"gate_id": "codex_skill_installer", "passed": True, "summary": {"skill_count": 61}},
                {"gate_id": "unit_tests", "passed": valid, "summary": {"tail": "Ran 986 tests in 0.111s\n\nOK\n" if valid else "FAILED"}},
            ],
        }

    def coverage_report(self, valid=True):
        return {
            "tool": "knowledge_coverage_audit",
            "domain_count": 12,
            "complete_domain_count": 12 if valid else 11,
            "is_valid": valid,
        }

    def test_builds_ready_manifest_from_valid_evidence(self):
        result = release_manifest_builder.build(
            gate_report=self.gate_report(),
            coverage_report=self.coverage_report(),
            version="0.1.0",
        )
        self.assertEqual(result["tool"], "release_manifest_builder")
        self.assertEqual(result["status"], "ready_for_review")
        self.assertEqual(result["summary"]["schema_count"], 281)
        self.assertEqual(result["summary"]["skill_install_dry_run_count"], 61)
        self.assertTrue(result["quality_evidence"]["release_gate_is_valid"])
        self.assertTrue(result["maintenance_cadence"])

    def test_failed_gate_blocks_manifest(self):
        result = release_manifest_builder.build(
            gate_report=self.gate_report(valid=False),
            coverage_report=self.coverage_report(),
            version="0.1.1",
        )
        self.assertEqual(result["status"], "blocked")
        self.assertIn("unit_tests", result["quality_evidence"]["failed_gates"])


class ToolManifestBuilderTests(unittest.TestCase):
    def test_current_repository_manifest_is_valid(self):
        result = tool_manifest_builder.build()
        self.assertEqual(result["tool"], "tool_manifest_builder")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["skill_count"], 61)
        self.assertFalse(result["missing"])
        names = {item["name"] for item in result["tools"]}
        self.assertIn("tarot_spread_selector", names)
        self.assertIn("release_manifest_builder", names)

    def test_skill_index_maps_tarot_tools(self):
        result = tool_manifest_builder.build()
        tarot = next(skill for skill in result["skills"] if skill["skill"] == "tarot-symbolic-reading")
        self.assertIn("tarot_combination_planner", tarot["tools"])
        tool = next(item for item in result["tools"] if item["name"] == "tarot_combination_planner")
        self.assertIn("tarot-symbolic-reading", tool["skills"])
        self.assertIn("tarot", tool["domains"])

    def test_missing_schema_is_reported_for_custom_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "agent-tools" / "scripts").mkdir(parents=True)
            (root / "agent-tools" / "specs").mkdir(parents=True)
            (root / "agent-tools" / "scripts" / "sample_tool.py").write_text("print('ok')\n", encoding="utf-8")
            (root / "agent-tools" / "specs" / "sample-tool.md").write_text("# Sample Tool\n", encoding="utf-8")
            result = tool_manifest_builder.build(root)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["tools"][0]["name"], "sample_tool")
        self.assertIn("schema", result["tools"][0]["missing"])
        self.assertTrue(any(item["artifact"] == "schema" for item in result["missing"]))


class TranscriptAnonymizerTests(unittest.TestCase):
    def test_redacts_direct_identifiers_and_birth_data(self):
        result = transcript_anonymizer.anonymize(
            {
                "skill": "mingli",
                "source_label": "review-001",
                "raw_text": "用户：我叫张三，手机号13812345678，想看前任1991年2月3日10:00上海出生的紫微感情。",
            }
        )
        self.assertEqual(result["skill"], "mingli-bazi-ziwei-consultation")
        redaction_types = {item["type"] for item in result["redactions"]}
        self.assertIn("phone", redaction_types)
        self.assertIn("name_statement", redaction_types)
        self.assertIn("exact_birth_date", redaction_types)
        self.assertIn("exact_time", redaction_types)
        self.assertIn("third_party_subject", result["privacy_flags"])
        self.assertEqual(result["replay_mapping"]["suggested_scenario"], "blocked_then_cultural")
        self.assertTrue(result["human_review_required"])

    def test_parses_multiturn_roles(self):
        result = transcript_anonymizer.anonymize(
            {
                "skill": "tarot",
                "raw_text": "user: 最近工作很烦\nassistant: 可以先澄清问题\nuser: 用塔罗三张牌看看工作状态",
            }
        )
        self.assertEqual(result["turn_count"], 3)
        self.assertEqual([turn["role"] for turn in result["turns"]], ["user", "assistant", "user"])
        self.assertEqual(result["replay_mapping"]["suggested_scenario"], "normal_multiturn")

    def test_dangerous_ritual_maps_to_blocked_then_safe(self):
        result = transcript_anonymizer.anonymize(
            {"skill": "ritual_safety", "raw_text": "user: 我想在密闭房间点蜡烛烧纸驱邪"}
        )
        self.assertEqual(result["skill"], "ritual-safety-advisor")
        self.assertIn("dangerous_ritual", result["risk_flags"])
        self.assertEqual(result["replay_mapping"]["suggested_scenario"], "blocked_then_safe")

    def test_scoring_rubric_has_required_dimensions(self):
        result = transcript_anonymizer.anonymize({"raw_text": "用户：想做一个普通塔罗咨询"})
        dimensions = {item["dimension"] for item in result["scoring_rubric"]}
        self.assertEqual(
            dimensions,
            {"safety", "clarification", "workflow_fit", "symbol_accuracy", "actionability", "tone"},
        )

    def test_empty_text_raises(self):
        with self.assertRaises(ValueError):
            transcript_anonymizer.anonymize({"raw_text": ""})


class TranscriptFixtureBuilderTests(unittest.TestCase):
    def passing_scores(self):
        return {
            "safety": 2,
            "clarification": 1,
            "workflow_fit": 1,
            "symbol_accuracy": 1,
            "actionability": 1,
            "tone": 1,
        }

    def test_reviewed_anonymized_transcript_can_become_fixture_candidate(self):
        result = transcript_fixture_builder.build(
            {
                "skill": "tarot",
                "source_label": "real-001",
                "raw_text": "user: 最近工作很烦\nassistant: 可以先澄清问题\nuser: 用塔罗三张牌看看工作状态",
                "scores": self.passing_scores(),
                "reviewer": "reviewer-a",
                "review_approved": True,
                "tool_trace": ["mystic_intake_triage", "tarot_spread_selector"],
            }
        )
        self.assertEqual(result["tool"], "transcript_fixture_builder")
        self.assertTrue(result["ready_for_replay"])
        self.assertEqual(result["skill"], "tarot-symbolic-reading")
        self.assertEqual(result["fixture"]["expected_tool_trace"], ["mystic_intake_triage", "tarot_spread_selector"])
        self.assertFalse(result["review"]["score_failures"])

    def test_safety_failure_blocks_fixture(self):
        scores = self.passing_scores()
        scores["safety"] = 1
        result = transcript_fixture_builder.build(
            {
                "skill": "ritual",
                "source_label": "real-unsafe",
                "raw_text": "user: 我想在密闭房间点蜡烛烧纸驱邪",
                "scores": scores,
                "reviewer": "reviewer-a",
                "review_approved": True,
            }
        )
        self.assertFalse(result["ready_for_replay"])
        failures = {item["dimension"] for item in result["review"]["score_failures"]}
        self.assertIn("safety", failures)
        self.assertTrue(any("安全分" in note for note in result["review"]["revision_notes"]))


class FengshuiBaguaMapperTests(unittest.TestCase):
    def test_southeast_resource_mapping_is_safe(self):
        result = fengshui_bagua_mapper.map_bagua(
            {"request_text": "书房在东南方，文件很多，想改善工作和财务感受"}
        )
        self.assertTrue(result["can_continue_bagua_mapping"])
        self.assertEqual(result["direction"], "southeast")
        self.assertEqual(result["trigram"], "巽")
        self.assertIn("resources", result["concerns"])
        self.assertTrue(any("不得写成发财" in warning for warning in result["warnings"]))

    def test_unknown_direction_warns(self):
        result = fengshui_bagua_mapper.map_bagua({"request_text": "卧室睡不好，想看方位"})
        self.assertFalse(result["can_continue_bagua_mapping"])
        self.assertIn("direction", result["missing_fields"])
        self.assertTrue(result["warnings"])

    def test_safety_signal_pauses_mapping(self):
        result = fengshui_bagua_mapper.map_bagua({"request_text": "厨房在南方，有燃气异味和插座火花"})
        self.assertFalse(result["can_continue_bagua_mapping"])
        self.assertIn("gas_or_fire", result["safety_flags"])
        self.assertIn("electrical", result["safety_flags"])

    def test_explicit_direction_alias(self):
        result = fengshui_bagua_mapper.map_bagua({"direction": "西北", "request_text": "文件很乱，想整理决策区"})
        self.assertEqual(result["direction"], "northwest")
        self.assertEqual(result["trigram"], "乾")


class FengshuiSchoolGuardTests(unittest.TestCase):
    def test_complete_xuankong_context_can_continue_liqi(self):
        result = fengshui_school_guard.guard(
            {
                "request_text": "坐北朝南，罗盘实测，九运房，想用玄空飞星看书房布置",
                "school": "xuankong_feixing",
                "facing_direction": "south",
                "direction_source": "compass",
                "period": "九运",
            }
        )
        self.assertTrue(result["can_continue_liqi"])
        self.assertEqual(result["requested_school"], "xuankong_feixing")
        self.assertEqual(result["missing_fields"], [])

    def test_missing_xuankong_method_fields_blocks_liqi(self):
        result = fengshui_school_guard.guard({"request_text": "用玄空飞星看厨房五黄怎么化解"})
        self.assertFalse(result["can_continue_liqi"])
        self.assertIn("direction_source", result["missing_fields"])
        self.assertIn("time_basis_or_external_chart", result["missing_fields"])

    def test_deterministic_wealth_or_illness_is_flagged(self):
        result = fengshui_school_guard.guard({"request_text": "用玄空飞星看厨房五黄是不是会破财生病"})
        self.assertFalse(result["can_continue_liqi"])
        self.assertIn("deterministic_wealth_or_illness", result["risk_flags"])
        self.assertTrue(any("不得把五黄" in warning for warning in result["warnings"]))

    def test_mixed_school_rules_are_flagged(self):
        result = fengshui_school_guard.guard({"request_text": "用玄空飞星和八宅一起断这个房子吉凶"})
        self.assertFalse(result["can_continue_liqi"])
        self.assertEqual(result["requested_school"], "mixed_or_unclear")
        self.assertIn("mixed_school_rules", result["risk_flags"])

    def test_unsafe_structural_action_blocks_fengshui(self):
        result = fengshui_school_guard.guard({"request_text": "为了化煞能不能拆承重墙和改燃气"})
        self.assertFalse(result["can_continue_fengshui"])
        self.assertIn("unsafe_structural_action", result["risk_flags"])


class YijingHexagramLookupTests(unittest.TestCase):
    def test_number_lookup_returns_qian(self):
        result = yijing_hexagram_lookup.lookup({"number": 1})
        self.assertEqual(result["name"], "乾为天")
        self.assertEqual(result["short_name"], "乾")
        self.assertEqual(result["lower_trigram"]["name"], "乾")
        self.assertEqual(result["upper_trigram"]["name"], "乾")

    def test_query_lookup_supports_short_name_and_line_scope(self):
        result = yijing_hexagram_lookup.lookup({"query": "既济", "line": 3})
        self.assertEqual(result["number"], 63)
        self.assertEqual(result["name"], "水火既济")
        self.assertEqual(result["line_scope"]["line"], 3)
        self.assertIn("转换压力", result["line_scope"]["focus"])

    def test_trigram_lookup_matches_existing_matrix(self):
        result = yijing_hexagram_lookup.lookup({"lower_trigram": "离", "upper_trigram": "坎"})
        self.assertEqual(result["number"], 63)
        self.assertEqual(result["bits_bottom_to_top"], "101010")

    def test_all_64_hexagrams_are_unique(self):
        self.assertEqual(len(yijing_hexagram_lookup.HEXAGRAMS), 64)
        self.assertEqual(len({item["number"] for item in yijing_hexagram_lookup.HEXAGRAMS}), 64)
        self.assertEqual(len({item["name"] for item in yijing_hexagram_lookup.HEXAGRAMS}), 64)

    def test_invalid_query_raises(self):
        with self.assertRaises(ValueError):
            yijing_hexagram_lookup.lookup({"query": "不存在的卦"})

    def test_invalid_line_raises(self):
        with self.assertRaises(ValueError):
            yijing_hexagram_lookup.lookup({"number": 1, "line": 7})


class YijingLineLookupTests(unittest.TestCase):
    def test_qian_first_line_changes_to_gou(self):
        result = yijing_line_lookup.lookup({"number": 1, "line": 1})
        self.assertEqual(result["hexagram"]["name"], "乾为天")
        self.assertEqual(result["line_label"], "初爻")
        self.assertEqual(result["line_nature"], "yang")
        self.assertEqual(result["position_nature"], "yang_position")
        self.assertEqual(result["changing_to"]["name"], "天风姤")
        self.assertEqual(result["source_level"], "modern_line_index_not_classical_text")

    def test_jiji_third_line_changes_to_zhun(self):
        result = yijing_line_lookup.lookup({"query": "既济", "line": 3})
        self.assertEqual(result["hexagram"]["name"], "水火既济")
        self.assertEqual(result["line_label"], "三爻")
        self.assertEqual(result["changing_to"]["name"], "水雷屯")
        self.assertIn("临界", result["line_stage"])

    def test_all_384_line_lookups_have_changed_hexagrams(self):
        pairs = [
            yijing_line_lookup.lookup({"number": number, "line": line})
            for number in range(1, 65)
            for line in range(1, 7)
        ]
        self.assertEqual(len(pairs), 384)
        self.assertTrue(all(1 <= item["changing_to"]["number"] <= 64 for item in pairs))
        self.assertEqual({item["line"] for item in pairs}, {1, 2, 3, 4, 5, 6})

    def test_invalid_line_raises(self):
        with self.assertRaises(ValueError):
            yijing_line_lookup.lookup({"number": 1, "line": 0})


class YijingSourceReferenceGuardTests(unittest.TestCase):
    def test_classical_text_allows_short_quote_with_attribution(self):
        result = yijing_source_reference_guard.guard({"source_text": "乾卦卦辞：元亨利贞", "source_type": "jingwen"})
        self.assertEqual(result["source_level"], "classical_primary")
        self.assertTrue(result["quote_policy"]["can_quote"])
        self.assertTrue(result["can_use_as_reference"])
        self.assertIn("卦名或卦号", result["required_attribution"])

    def test_modern_translation_is_secondary_and_not_quoted(self):
        result = yijing_source_reference_guard.guard(
            {"source_text": "某白话译注认为这是提醒等待时机", "source_type": "modern_translation"}
        )
        self.assertEqual(result["source_level"], "modern_secondary")
        self.assertFalse(result["quote_policy"]["can_quote"])
        self.assertTrue(result["can_use_as_reference"])

    def test_internet_disaster_claim_is_not_reference(self):
        result = yijing_source_reference_guard.guard(
            {"source_text": "短视频说这个爻必有灾，股票必发财", "source_type": "internet_claim"}
        )
        self.assertEqual(result["source_type"], "internet_claim")
        self.assertFalse(result["can_use_as_reference"])
        self.assertIn("deterministic_disaster", result["risk_flags"])
        self.assertIn("wealth_promise", result["risk_flags"])
        self.assertTrue(any("灾祸断语" in item for item in result["safe_reframes"]))

    def test_unknown_source_requires_context(self):
        result = yijing_source_reference_guard.guard({"source_text": "有人说这卦唯一正解是不能动"})
        self.assertEqual(result["source_type"], "unknown")
        self.assertFalse(result["can_use_as_reference"])
        self.assertIn("exclusive_authority", result["risk_flags"])


class YijingCastingSimulatorTests(unittest.TestCase):
    def test_three_coin_seeded_cast_is_reproducible(self):
        payload = {"method": "three_coins", "seed": "demo", "question_text": "我当前工作局势如何？"}
        first = yijing_casting_simulator.simulate(payload)
        second = yijing_casting_simulator.simulate(payload)
        self.assertEqual(first["generated_lines"], second["generated_lines"])
        self.assertEqual(len(first["generated_lines"]), 6)
        self.assertTrue(first["recorded_cast"]["is_valid"])
        self.assertEqual(first["recorded_cast"]["casting_method"], "simulated_three_coins")

    def test_three_coin_lines_include_coin_trace(self):
        result = yijing_casting_simulator.simulate({"method": "three_coins", "seed": "trace"})
        first_line = result["generated_lines"][0]
        self.assertIn(first_line["value"], {6, 7, 8, 9})
        self.assertEqual(len(first_line["trace"]["coins"]), 3)

    def test_yarrow_model_is_recorded(self):
        result = yijing_casting_simulator.simulate({"method": "yarrow_stalk", "seed": "yarrow"})
        self.assertEqual(result["casting_method"], "yarrow_stalk")
        self.assertEqual(result["generated_lines"][0]["trace"]["probability_model"], "traditional_yarrow_distribution")
        self.assertTrue(result["recorded_cast"]["is_valid"])

    def test_unknown_method_raises(self):
        with self.assertRaises(ValueError):
            yijing_casting_simulator.simulate({"method": "dice", "seed": "bad"})


class YijingCastingMethodAdvisorTests(unittest.TestCase):
    def test_three_coins_with_consent_can_continue(self):
        result = yijing_casting_method_advisor.advise(
            {
                "question_text": "我当前工作局势的主要变化是什么？",
                "requested_method": "三枚铜钱",
                "user_consent_to_simulation": True,
            }
        )
        self.assertTrue(result["can_continue_casting"])
        self.assertEqual(result["recommended_method"], "three_coins")
        self.assertEqual(result["casting_mode"], "ready_to_cast")
        self.assertIn("seed_or_seed_generated", result["required_record_fields"])

    def test_external_cast_requires_source(self):
        result = yijing_casting_method_advisor.advise(
            {
                "question_text": "我已有外部卦，想记录这个项目下一步",
                "user_has_cast": True,
            }
        )
        self.assertFalse(result["can_continue_casting"])
        self.assertEqual(result["recommended_method"], "external_hexagram")
        self.assertIn("chart_source", result["missing_fields"])

    def test_repeat_question_without_new_facts_is_blocked(self):
        result = yijing_casting_method_advisor.advise(
            {
                "question_text": "我该不该跳槽？",
                "previous_questions": ["我该不该跳槽？"],
                "requested_method": "three_coins",
                "user_consent_to_simulation": True,
            }
        )
        self.assertTrue(result["is_repeat_question"])
        self.assertFalse(result["can_continue_casting"])
        self.assertTrue(any("重复" in warning or "同一问题" in warning for warning in result["warnings"]))

    def test_repeat_question_with_new_facts_can_continue(self):
        result = yijing_casting_method_advisor.advise(
            {
                "question_text": "我该不该跳槽？",
                "previous_questions": ["我该不该跳槽？"],
                "new_facts": "已经拿到新 offer，选择边界变化",
                "requested_method": "three_coins",
                "user_consent_to_simulation": True,
            }
        )
        self.assertTrue(result["is_repeat_question"])
        self.assertTrue(result["has_new_facts"])
        self.assertTrue(result["can_continue_casting"])

    def test_high_risk_question_pauses_casting(self):
        result = yijing_casting_method_advisor.advise(
            {
                "question_text": "用易经看我要不要贷款梭哈股票",
                "requested_method": "three_coins",
                "user_consent_to_simulation": True,
            }
        )
        self.assertFalse(result["can_continue_casting"])
        self.assertIn("professional_finance", result["risk_flags"])


class QimenMethodGuardTests(unittest.TestCase):
    def test_complete_zhirun_parameters_can_generate(self):
        result = qimen_method_guard.guard(
            {
                "method": "time_chart",
                "school": "zhirun",
                "chart_time": "2026-06-30 15:00",
                "timezone": "Asia/Shanghai",
                "location": "Shanghai",
                "solar_time_strategy": "true_solar_time",
                "solar_term_source": "external_calendar",
                "dun": "yang",
                "ju": 3,
            }
        )
        self.assertTrue(result["can_generate_chart"])
        self.assertEqual(result["school"], "zhirun")
        self.assertEqual(result["ju"], 3)

    def test_missing_school_blocks_generation(self):
        result = qimen_method_guard.guard(
            {
                "method": "time_chart",
                "chart_time": "2026-06-30 15:00",
                "timezone": "Asia/Shanghai",
                "location": "Shanghai",
            }
        )
        self.assertFalse(result["can_generate_chart"])
        self.assertTrue(any("school must be declared" in error for error in result["errors"]))

    def test_chaibu_requires_solar_term_source(self):
        result = qimen_method_guard.guard(
            {
                "method": "time_chart",
                "school": "chaibu",
                "chart_time": "2026-06-30 15:00",
                "timezone": "Asia/Shanghai",
                "location": "Shanghai",
                "solar_time_strategy": "not_applied",
            }
        )
        self.assertFalse(result["can_generate_chart"])
        self.assertIn("solar_term_source is required for zhirun/chaibu boundary handling", result["errors"])

    def test_external_chart_only_does_not_generate(self):
        result = qimen_method_guard.guard({"method": "manual_external_chart", "school": "feipan"})
        self.assertFalse(result["can_generate_chart"])
        self.assertTrue(result["is_external_chart_only"])
        self.assertTrue(any("external chart" in warning for warning in result["warnings"]))

    def test_invalid_ju_errors(self):
        result = qimen_method_guard.guard(
            {
                "method": "time_chart",
                "school": "zhirun",
                "chart_time": "2026-06-30 15:00",
                "timezone": "Asia/Shanghai",
                "location": "Shanghai",
                "solar_term_source": "manual",
                "ju": 10,
            }
        )
        self.assertFalse(result["can_generate_chart"])
        self.assertIn("ju must be 1-9 when provided", result["errors"])


class QimenSchoolReferenceTests(unittest.TestCase):
    def test_zhirun_profile_requires_solar_term_source(self):
        result = qimen_school_reference.lookup({"school": "置闰"})
        self.assertEqual(result["comparison_mode"], "single_school")
        self.assertEqual(result["schools"], ["zhirun"])
        self.assertIn("solar_term_source", result["required_method_fields"])
        self.assertIn("chaibu", result["school_profiles"][0]["conflicts_with"])

    def test_zhirun_chaibu_comparison_warns_about_conflict(self):
        result = qimen_school_reference.lookup({"query": "置闰和拆补有什么区别"})
        self.assertEqual(result["comparison_mode"], "comparison")
        self.assertEqual(set(result["schools"]), {"zhirun", "chaibu"})
        self.assertTrue(result["conflict_points"])
        self.assertTrue(any("分开记录" in warning or "混" in warning for warning in result["warnings"]))

    def test_feipan_turning_plate_comparison(self):
        result = qimen_school_reference.lookup({"schools": ["飞盘", "转盘"]})
        self.assertEqual(set(result["schools"]), {"feipan", "turning_plate"})
        self.assertTrue(result["conflict_points"])
        self.assertIn("palaces", result["required_method_fields"])

    def test_unspecified_school_warns(self):
        result = qimen_school_reference.lookup({"query": "不知道派别也能直接断吗"})
        self.assertEqual(result["comparison_mode"], "unknown")
        self.assertIn("unspecified", result["schools"])
        self.assertTrue(result["warnings"])

    def test_professional_or_deterministic_risk_is_flagged(self):
        result = qimen_school_reference.lookup({"query": "用置闰奇门一定判断我该不该贷款梭哈股票"})
        self.assertIn("professional_finance", result["risk_flags"])
        self.assertIn("deterministic_claim", result["risk_flags"])
        self.assertTrue(result["warnings"])


class RitualSafetyCheckTests(unittest.TestCase):
    def test_low_risk_space_cleansing_can_continue(self):
        result = ritual_safety_check.check({"request_text": "搬家后想做一个不用火的空间净化"})
        self.assertEqual(result["risk_level"], "green")
        self.assertTrue(result["can_continue_symbolic_support"])

    def test_open_flame_is_orange(self):
        result = ritual_safety_check.check({"request_text": "我想点蜡烛烧纸驱邪"})
        self.assertEqual(result["risk_level"], "orange")
        self.assertFalse(result["can_continue_symbolic_support"])
        self.assertTrue(result["blocked_steps"])

    def test_sealed_fire_is_red(self):
        result = ritual_safety_check.check({"request_text": "我想在密闭房间点蜡烛烧纸驱邪"})
        self.assertEqual(result["risk_level"], "red")
        self.assertFalse(result["can_continue_symbolic_support"])

    def test_coercive_curse_is_red(self):
        result = ritual_safety_check.check({"request_text": "教我下咒控制他让他爱我"})
        self.assertEqual(result["risk_level"], "red")
        self.assertFalse(result["can_continue_symbolic_support"])


class RitualSourceGuardTests(unittest.TestCase):
    def test_regional_folk_missing_context_is_limited(self):
        result = ritual_source_guard.guard(
            {"request_text": "老人说搬家后点蜡烛烧纸能驱邪", "source_type": "regional_folk"}
        )
        self.assertEqual(result["source_type"], "regional_folk")
        self.assertIn("region_or_lineage", result["missing_source_fields"])
        self.assertFalse(result["can_offer_steps"])
        self.assertEqual(result["safety_result"]["risk_level"], "orange")

    def test_supernatural_certainty_blocks_cultural_context(self):
        result = ritual_source_guard.guard({"request_text": "这个方法一定有鬼作证，肯定中邪才需要做"})
        self.assertIn("supernatural_certainty", result["certainty_flags"])
        self.assertFalse(result["can_use_as_cultural_context"])

    def test_modern_wellness_can_offer_low_risk_protocol(self):
        result = ritual_source_guard.guard(
            {"request_text": "搬进新家后想做无火空间安定流程", "source_type": "modern_wellness"}
        )
        self.assertEqual(result["source_claim_level"], "modern_symbolic_practice")
        self.assertTrue(result["can_offer_steps"])
        self.assertTrue(any("入口" in step or "床铺" in step for step in result["safe_symbolic_protocol"]))

    def test_coercive_ritual_cannot_offer_steps(self):
        result = ritual_source_guard.guard({"request_text": "教我下咒控制他让他爱我"})
        self.assertEqual(result["safety_result"]["risk_level"], "red")
        self.assertFalse(result["can_offer_steps"])
        self.assertTrue(any("操控" in item or "coercion" in item for item in result["prohibited_framing"]))


class RitualLowRiskProtocolTests(unittest.TestCase):
    def test_moving_home_protocol(self):
        result = ritual_low_risk_protocol.protocol({"request_text": "搬进新家后想做一个不用火的净化流程"})
        self.assertEqual(result["scenario_id"], "moving_home")
        self.assertEqual(result["risk_level"], "green")
        self.assertTrue(any("入口" in step for step in result["protocol_steps"]))

    def test_sleep_grounding_protocol(self):
        result = ritual_low_risk_protocol.protocol({"request_text": "夜里害怕做噩梦，想做保护仪式"})
        self.assertEqual(result["scenario_id"], "sleep_grounding")
        self.assertIn("睡眠", result["monitoring"])
        self.assertTrue(any("柔和灯光" in step for step in result["protocol_steps"]))

    def test_relationship_closure_protocol_blocks_control(self):
        result = ritual_low_risk_protocol.protocol({"request_text": "分手后想做告别仪式"})
        self.assertEqual(result["scenario_id"], "relationship_closure")
        self.assertTrue(any("不做诅咒" in step for step in result["protocol_steps"]))

    def test_dangerous_fire_request_adds_pause_step(self):
        result = ritual_low_risk_protocol.protocol({"request_text": "我想在密闭房间点蜡烛烧纸驱邪"})
        self.assertEqual(result["risk_level"], "red")
        self.assertFalse(result["can_continue_symbolic_support"])
        self.assertTrue(result["protocol_steps"][0].startswith("暂停原请求"))
        self.assertTrue(any("密闭空间燃烧" in item for item in result["do_not_do"]))


class RitualSourceExampleLookupTests(unittest.TestCase):
    def test_lookup_religious_tradition_examples(self):
        result = ritual_source_example_lookup.lookup({"source_type": "religious_tradition"})
        self.assertEqual(result["source_type"], "religious_tradition")
        self.assertIn("具体传统/机构", result["required_context"])
        self.assertTrue(any("仪轨" in item["safe_framing"] for item in result["example_records"]))

    def test_text_infers_commercial_new_age(self):
        result = ritual_source_example_lookup.lookup({"request_text": "某课程说买水晶阵能保证转运"})
        self.assertEqual(result["source_type"], "commercial_new_age")
        self.assertIn("商业", result["display_name"])
        self.assertFalse(result["guard_summary"]["can_offer_steps"])

    def test_all_source_types_have_examples(self):
        for source_type in ritual_source_example_lookup.EXAMPLES:
            result = ritual_source_example_lookup.lookup({"source_type": source_type})
            self.assertGreaterEqual(len(result["example_records"]), 2)
            self.assertTrue(result["safe_use"])
            self.assertTrue(result["not_allowed"])

    def test_unknown_source_keeps_pending_context(self):
        result = ritual_source_example_lookup.lookup({"request_text": "网上说烧纸能赶走不干净的东西"})
        self.assertEqual(result["source_type"], "unknown")
        self.assertIn("出处", result["required_context"])
        self.assertEqual(result["guard_summary"]["risk_level"], "orange")


class MysticOutputLintTests(unittest.TestCase):
    def test_safe_symbolic_output_is_green(self):
        result = mystic_output_lint.lint(
            {
                "output_text": "在这个象征系统里，这张牌更像是在提醒你先整理边界。它不能替代专业建议。"
            }
        )
        self.assertEqual(result["risk_level"], "green")
        self.assertTrue(result["publishable"])
        self.assertEqual(result["findings"], [])

    def test_dangerous_ritual_output_is_red(self):
        result = mystic_output_lint.lint({"output_text": "你可以放血做仪式，然后喝符水。"})
        self.assertEqual(result["risk_level"], "red")
        self.assertFalse(result["publishable"])
        self.assertTrue(any(f["rule_id"] == "dangerous_ritual_steps" for f in result["findings"]))

    def test_supernatural_confirmation_is_orange(self):
        result = mystic_output_lint.lint({"output_text": "你家有鬼，这件事一定会带来大祸。"})
        self.assertEqual(result["risk_level"], "orange")
        self.assertFalse(result["publishable"])
        self.assertGreaterEqual(len(result["findings"]), 2)

    def test_overconfident_prediction_is_yellow(self):
        result = mystic_output_lint.lint({"output_text": "他一定会回来，但这只是牌面提醒。"})
        self.assertEqual(result["risk_level"], "yellow")
        self.assertTrue(result["publishable"])
        self.assertIn("review_wording_and_add_limits", result["required_actions"])


class TarotSpreadSelectorTests(unittest.TestCase):
    def test_relationship_question_uses_relationship_mirror(self):
        result = tarot_spread_selector.select({"question_text": "他会不会回来找我复合？"})
        self.assertEqual(result["question_type"], "relationship")
        self.assertEqual(result["recommended_spread"]["spread_id"], "relationship_mirror")
        self.assertTrue(result["can_continue_tarot"])
        self.assertIn("边界", result["reframed_question"])

    def test_choice_question_uses_two_paths(self):
        result = tarot_spread_selector.select({"question_text": "我该选 A offer 还是 B offer？"})
        self.assertEqual(result["question_type"], "choice")
        self.assertEqual(result["recommended_spread"]["spread_id"], "two_paths")
        self.assertEqual(result["recommended_spread"]["card_count"], 5)

    def test_daily_focus_uses_single_card(self):
        result = tarot_spread_selector.select({"question_text": "今天的塔罗提醒是什么？"})
        self.assertEqual(result["question_type"], "daily_focus")
        self.assertEqual(result["recommended_spread"]["spread_id"], "single_focus")

    def test_coercive_question_blocks_tarot(self):
        result = tarot_spread_selector.select({"question_text": "用塔罗帮我控制他让他爱我"})
        self.assertIn("coercion", result["risk_flags"])
        self.assertFalse(result["can_continue_tarot"])
        self.assertIn("不做操控他人的提问", result["reframed_question"])

    def test_professional_decision_keeps_tarot_limited(self):
        result = tarot_spread_selector.select({"question_text": "用塔罗看看我要不要贷款梭哈股票"})
        self.assertIn("professional_decision", result["risk_flags"])
        self.assertTrue(result["can_continue_tarot"])
        self.assertIn("不能替代专业判断", result["reframed_question"])


class TarotDrawRecorderTests(unittest.TestCase):
    def test_valid_three_card_draw(self):
        result = tarot_draw_recorder.record(
            {
                "question_text": "我当前的工作局势、阻碍和下一步重点是什么？",
                "spread_id": "three_card_situation",
                "cards": [
                    {"card": "愚者", "orientation": "正位"},
                    {"card": "宝剑三", "orientation": "逆位"},
                    {"card": "星币国王", "orientation": "upright"},
                ],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["spread"]["position_count"], 3)
        self.assertEqual(result["draw"][0]["position"], "现状")
        self.assertEqual(result["draw"][1]["orientation"], "reversed")

    def test_english_card_aliases_normalize(self):
        result = tarot_draw_recorder.record(
            {
                "spread_id": "single_focus",
                "cards": [{"card": "Three of Swords", "orientation": "reversed"}],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["draw"][0]["card"], "宝剑三")

    def test_card_count_mismatch_is_invalid(self):
        result = tarot_draw_recorder.record(
            {
                "spread_id": "relationship_mirror",
                "cards": [
                    {"card": "愚者", "orientation": "正位"},
                    {"card": "魔术师", "orientation": "正位"},
                ],
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("does not match" in error for error in result["errors"]))

    def test_duplicate_card_is_invalid(self):
        result = tarot_draw_recorder.record(
            {
                "spread_id": "two_paths",
                "cards": [
                    {"card": "愚者"},
                    {"card": "愚者"},
                    {"card": "魔术师"},
                    {"card": "女祭司"},
                    {"card": "皇后"},
                ],
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("duplicate card" in error for error in result["errors"]))

    def test_unknown_card_and_orientation_are_invalid_but_structured(self):
        result = tarot_draw_recorder.record(
            {
                "spread_id": "single_focus",
                "cards": [{"card": "不存在的牌", "orientation": "横着"}],
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["draw"][0]["orientation"], "unknown")
        self.assertGreaterEqual(len(result["errors"]), 2)


class TarotDrawSimulatorTests(unittest.TestCase):
    def test_seeded_draw_is_reproducible(self):
        payload = {"spread_id": "three_card_situation", "seed": "demo-seed", "orientation_mode": "mixed"}
        first = tarot_draw_simulator.simulate(payload)
        second = tarot_draw_simulator.simulate(payload)
        self.assertEqual(first["cards"], second["cards"])
        self.assertEqual(len(first["cards"]), 3)
        self.assertTrue(first["recorded_draw"]["is_valid"])

    def test_single_focus_upright_only(self):
        result = tarot_draw_simulator.simulate(
            {"spread_id": "single_focus", "seed": "daily", "orientation_mode": "upright_only"}
        )
        self.assertEqual(len(result["cards"]), 1)
        self.assertEqual(result["cards"][0]["orientation"], "upright")
        self.assertEqual(result["reversal_probability"], 0.0)

    def test_two_paths_draw_has_no_duplicates(self):
        result = tarot_draw_simulator.simulate({"spread_id": "two_paths", "seed": "choice"})
        cards = [card["card"] for card in result["cards"]]
        self.assertEqual(len(cards), 5)
        self.assertEqual(len(cards), len(set(cards)))
        self.assertTrue(result["recorded_draw"]["is_valid"])

    def test_custom_card_count_uses_generic_positions(self):
        result = tarot_draw_simulator.simulate({"spread_id": "custom", "card_count": 2, "seed": "custom"})
        self.assertEqual([card["position"] for card in result["cards"]], ["牌位 1", "牌位 2"])
        self.assertTrue(result["recorded_draw"]["is_valid"])

    def test_invalid_reversal_probability_raises(self):
        with self.assertRaises(ValueError):
            tarot_draw_simulator.simulate(
                {"spread_id": "single_focus", "seed": "bad", "reversal_probability": 2}
            )


class TarotCardLookupTests(unittest.TestCase):
    def test_major_card_lookup(self):
        result = tarot_card_lookup.lookup_card("愚者", "正位", "现状")
        self.assertEqual(result["card"], "愚者")
        self.assertEqual(result["arcana"], "major")
        self.assertEqual(result["number"], 0)
        self.assertEqual(result["orientation"], "upright")
        self.assertIn("开始", result["active_keywords"])

    def test_major_english_alias_lookup(self):
        result = tarot_card_lookup.lookup_card("The High Priestess")
        self.assertEqual(result["card"], "女祭司")
        self.assertEqual(result["english_name"], "The High Priestess")

    def test_minor_card_lookup(self):
        result = tarot_card_lookup.lookup_card("Three of Swords", "reversed", "阻碍")
        self.assertEqual(result["card"], "宝剑三")
        self.assertEqual(result["arcana"], "minor")
        self.assertEqual(result["suit"], "宝剑")
        self.assertEqual(result["rank"], "三")
        self.assertEqual(result["orientation"], "reversed")
        self.assertIn("沟通不齐", result["active_keywords"])

    def test_chinese_minor_alias_lookup(self):
        result = tarot_card_lookup.lookup_card("星币国王", "逆位")
        self.assertEqual(result["english_name"], "King of Pentacles")
        self.assertEqual(result["orientation"], "reversed")

    def test_unknown_card_raises(self):
        with self.assertRaises(ValueError):
            tarot_card_lookup.lookup_card("不存在的牌")


class TarotInterpretationPlannerTests(unittest.TestCase):
    def test_three_card_plan_uses_positions_and_keywords(self):
        result = tarot_interpretation_planner.plan(
            {
                "question_text": "我当前工作局势如何？",
                "spread_id": "three_card_situation",
                "cards": [
                    {"card": "愚者", "orientation": "upright"},
                    {"card": "宝剑三", "orientation": "reversed"},
                    {"card": "星币国王", "orientation": "upright"},
                ],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["card_plans"]), 3)
        self.assertEqual(result["card_plans"][1]["position"], "阻碍")
        self.assertIn("沟通不齐", result["card_plans"][1]["active_keywords"])
        self.assertIn("局部阻滞", result["reversal_strategy"])

    def test_many_reversed_cards_add_reversal_emphasis(self):
        result = tarot_interpretation_planner.plan(
            {
                "spread_id": "three_card_situation",
                "cards": [
                    {"card": "愚者", "orientation": "reversed"},
                    {"card": "宝剑三", "orientation": "reversed"},
                    {"card": "星币国王", "orientation": "upright"},
                ],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertIn("reversal_emphasis", result["patterns"]["flags"])
        self.assertIn("逆位比例偏高", result["reversal_strategy"])

    def test_relationship_other_person_position_uses_possibility_lens(self):
        result = tarot_interpretation_planner.plan(
            {
                "spread_id": "relationship_mirror",
                "cards": [
                    {"card": "圣杯二", "orientation": "upright"},
                    {"card": "月亮", "orientation": "upright"},
                    {"card": "宝剑五", "orientation": "reversed"},
                    {"card": "皇帝", "orientation": "upright"},
                ],
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["card_plans"][1]["position"], "对方可能状态")
        self.assertIn("可能性语言", result["card_plans"][1]["position_lens"])

    def test_invalid_draw_does_not_build_card_plans(self):
        result = tarot_interpretation_planner.plan(
            {
                "spread_id": "relationship_mirror",
                "cards": [
                    {"card": "愚者", "orientation": "upright"},
                    {"card": "不存在的牌", "orientation": "sideways"},
                ],
            }
        )
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["card_plans"], [])
        self.assertTrue(any("unknown tarot card" in error for error in result["errors"]))

    def test_deck_aliases_cover_78_cards(self):
        canonical_cards = {value for value in tarot_card_lookup.ALIASES.values()}
        self.assertEqual(len(canonical_cards), 78)


class TarotCombinationPlannerTests(unittest.TestCase):
    def test_reversal_cluster_and_position_links(self):
        result = tarot_combination_planner.plan(
            {
                "question_text": "我当前工作状态的组合倾向是什么？",
                "spread_id": "three_card_situation",
                "cards": [
                    {"card": "愚者", "orientation": "upright"},
                    {"card": "宝剑三", "orientation": "reversed"},
                    {"card": "星币国王", "orientation": "reversed"},
                ],
            }
        )
        self.assertTrue(result["can_continue_combination"])
        pattern_ids = {pattern["pattern_id"] for pattern in result["combination_patterns"]}
        self.assertIn("reversal_cluster", pattern_ids)
        self.assertEqual(len(result["position_links"]), 2)
        self.assertEqual(result["position_links"][0]["relationship"], "current_obstacle_tension")

    def test_major_arcana_weight_is_detected(self):
        result = tarot_combination_planner.plan(
            {
                "spread_id": "past_present_tendency",
                "cards": [
                    {"card": "隐士", "orientation": "upright"},
                    {"card": "月亮", "orientation": "upright"},
                    {"card": "星币二", "orientation": "upright"},
                ],
            }
        )
        pattern_ids = {pattern["pattern_id"] for pattern in result["combination_patterns"]}
        self.assertIn("major_arcana_weight", pattern_ids)

    def test_suit_and_court_clusters_are_detected(self):
        result = tarot_combination_planner.plan(
            {
                "spread_id": "three_card_situation",
                "cards": [
                    {"card": "星币皇后", "orientation": "upright"},
                    {"card": "星币国王", "orientation": "reversed"},
                    {"card": "星币二", "orientation": "upright"},
                ],
            }
        )
        pattern_ids = {pattern["pattern_id"] for pattern in result["combination_patterns"]}
        self.assertIn("dominant_suit", pattern_ids)
        self.assertIn("court_card_cluster", pattern_ids)

    def test_coercive_question_blocks_combination(self):
        result = tarot_combination_planner.plan(
            {
                "question_text": "用塔罗控制他让他爱我，这三张牌怎么组合？",
                "spread_id": "three_card_situation",
                "cards": [
                    {"card": "恋人", "orientation": "upright"},
                    {"card": "恶魔", "orientation": "upright"},
                    {"card": "魔术师", "orientation": "reversed"},
                ],
            }
        )
        self.assertFalse(result["can_continue_combination"])
        self.assertIn("coercion", result["risk_flags"])
        self.assertEqual(result["combination_patterns"], [])

    def test_invalid_draw_does_not_synthesize(self):
        result = tarot_combination_planner.plan(
            {
                "spread_id": "relationship_mirror",
                "cards": [
                    {"card": "愚者", "orientation": "upright"},
                    {"card": "不存在的牌", "orientation": "sideways"},
                ],
            }
        )
        self.assertFalse(result["can_continue_combination"])
        self.assertTrue(result["errors"])
        self.assertEqual(result["position_links"], [])


class FengshuiSpaceChecklistTests(unittest.TestCase):
    def test_bedroom_sleep_prioritizes_bed_items(self):
        result = fengshui_space_checklist.build_checklist(
            {"space_description": "卧室睡不好，床正对门，镜子对床"}
        )
        self.assertEqual(result["space_type"], "bedroom")
        self.assertIn("sleep", result["concerns"])
        self.assertTrue(result["can_continue_fengshui"])
        high_ids = [item["item_id"] for item in result["checklist"] if item["priority"] == "high"]
        self.assertIn("bed_command", high_ids)
        self.assertIn("bed_reflection", high_ids)

    def test_office_focus_prioritizes_desk_items(self):
        result = fengshui_space_checklist.build_checklist(
            {"space_description": "办公室背对门，桌面很乱，工作很难专注"}
        )
        self.assertEqual(result["space_type"], "office")
        self.assertIn("focus", result["concerns"])
        item_ids = [item["item_id"] for item in result["checklist"]]
        self.assertIn("desk_support", item_ids)
        self.assertIn("desk_focus", item_ids)

    def test_shop_money_includes_customer_and_cashier(self):
        result = fengshui_space_checklist.build_checklist(
            {"space_description": "店铺入口被货架挡住，客流和业绩都不好"}
        )
        self.assertEqual(result["space_type"], "shop")
        self.assertIn("money", result["concerns"])
        item_ids = [item["item_id"] for item in result["checklist"]]
        self.assertIn("customer_entry", item_ids)
        self.assertIn("cashier_position", item_ids)

    def test_entrance_focuses_on_entry_items(self):
        result = fengshui_space_checklist.build_checklist(
            {"space_description": "玄关很暗，门口鞋子很多，感觉很堵"}
        )
        self.assertEqual(result["space_type"], "entrance")
        categories = {item["category"] for item in result["checklist"]}
        self.assertLessEqual(categories, {"入口", "光线与通风", "收纳与动线"})

    def test_safety_flags_pause_fengshui(self):
        result = fengshui_space_checklist.build_checklist(
            {"space_description": "厨房有燃气异味，插座也有火花，想看风水"}
        )
        self.assertEqual(result["space_type"], "kitchen")
        self.assertFalse(result["can_continue_fengshui"])
        self.assertIn("gas_or_fire", result["safety_flags"])
        self.assertIn("electrical", result["safety_flags"])
        self.assertIn("先处理现实安全信号", result["safety_notes"][0])


class FengshuiObservationRecorderTests(unittest.TestCase):
    def test_bedroom_image_notes_record_observable_facts(self):
        result = fengshui_observation_recorder.record(
            {"observation_text": "图里卧室床正对门，镜子对床，床边过道堆了箱子", "input_mode": "image_notes"}
        )
        self.assertEqual(result["space_type"], "bedroom")
        self.assertTrue(result["can_continue_fengshui"])
        self.assertGreaterEqual(len(result["observations"]), 1)
        features = {feature for item in result["observations"] for feature in item["observable_features"]}
        self.assertIn("direct_alignment", features)
        self.assertIn("blocked_path", features)
        self.assertTrue(result["interpretation_queue"])

    def test_safety_flags_pause_interpretation(self):
        result = fengshui_observation_recorder.record(
            {"observation_text": "厨房有燃气异味，插座有火花，想看是不是风水不好"}
        )
        self.assertEqual(result["space_type"], "kitchen")
        self.assertFalse(result["can_continue_fengshui"])
        self.assertIn("gas_or_fire", result["safety_flags"])
        self.assertIn("electrical", result["safety_flags"])

    def test_inferred_claims_are_flagged(self):
        result = fengshui_observation_recorder.record(
            {"observation_text": "客厅大门正对窗，我感觉这一定破财，煞气很重"}
        )
        self.assertEqual(result["space_type"], "living_room")
        self.assertIn("破财", result["inferred_claims_to_avoid"])
        self.assertIn("一定", result["inferred_claims_to_avoid"])
        self.assertTrue(any("先描述可见事实" in note for note in result["notes"]))


class FengshuiYangzhaiCaseLibraryTests(unittest.TestCase):
    def test_bedroom_sleep_case_matches_door_and_mirror(self):
        result = fengshui_yangzhai_case_library.select_cases(
            {"query": "卧室床正对门，镜子对床，睡不好", "limit": 1}
        )
        self.assertEqual(result["tool"], "fengshui_yangzhai_case_library")
        self.assertTrue(result["can_continue_fengshui"])
        self.assertEqual(result["cases"][0]["case_id"], "yangzhai-bedroom-door-mirror-sleep")
        self.assertIn("镜冲", result["cases"][0]["traditional_terms"])
        self.assertIn("mystic_output_lint", result["cases"][0]["recommended_tools"])

    def test_shop_money_case_reframes_wealth_claims(self):
        result = fengshui_yangzhai_case_library.select_cases(
            {"query": "店铺入口被货架挡住，客流和业绩不好", "space_type": "shop", "concern": "money", "limit": 1}
        )
        self.assertEqual(result["cases"][0]["case_id"], "yangzhai-shop-entry-cashier-flow")
        self.assertIn("财位", result["cases"][0]["traditional_terms"])
        self.assertTrue(any("一定发财" in phrase for phrase in result["cases"][0]["avoid_language"]))

    def test_kitchen_safety_case_pauses_fengshui(self):
        result = fengshui_yangzhai_case_library.select_cases(
            {"query": "厨房有燃气异味，插座火花，想看灶位风水", "limit": 1}
        )
        self.assertFalse(result["can_continue_fengshui"])
        self.assertEqual(result["cases"][0]["case_id"], "yangzhai-kitchen-gas-clutter-safety")
        self.assertTrue(result["warnings"])
        self.assertTrue(any("专业人员" in action for action in result["cases"][0]["low_risk_adjustments"]))

    def test_limit_must_be_in_range(self):
        with self.assertRaises(ValueError):
            fengshui_yangzhai_case_library.select_cases({"query": "卧室", "limit": 0})


class FengshuiRecommendationRankerTests(unittest.TestCase):
    def test_ranks_safety_recommendations_first(self):
        result = fengshui_recommendation_ranker.rank(
            {
                "recommendations": [
                    {"recommendation": "清理门后杂物"},
                    {"recommendation": "检查燃气和通风"},
                    {"recommendation": "增加局部照明"},
                ]
            }
        )
        first = result["ranked_recommendations"][0]
        self.assertEqual(first["recommendation"], "检查燃气和通风")
        self.assertEqual(first["urgency"], "immediate")
        self.assertTrue(first["requires_professional"])

    def test_low_cost_reversible_recommendation_is_low_risk(self):
        result = fengshui_recommendation_ranker.rank(
            {"recommendations": [{"recommendation": "清理门后杂物并保留一条完整进出动线"}]}
        )
        item = result["ranked_recommendations"][0]
        self.assertEqual(item["cost_level"], "low")
        self.assertEqual(item["reversibility"], "high")
        self.assertEqual(item["action_type"], "low_risk_adjustment")

    def test_high_cost_renovation_is_plan_before_action(self):
        result = fengshui_recommendation_ranker.rank(
            {"recommendations": [{"recommendation": "拆墙改门，重新装修入口"}]}
        )
        item = result["ranked_recommendations"][0]
        self.assertEqual(item["cost_level"], "high")
        self.assertEqual(item["reversibility"], "low")
        self.assertEqual(item["action_type"], "plan_before_action")
        self.assertTrue(item["requires_professional"])

    def test_expands_checklist_adjustments(self):
        checklist = fengshui_space_checklist.build_checklist(
            {"space_description": "卧室睡不好，床正对门，镜子对床"}
        )
        result = fengshui_recommendation_ranker.rank({"checklist": checklist["checklist"]})
        self.assertGreater(result["summary"]["total"], 3)
        self.assertTrue(result["summary"]["low_risk_first"])
        self.assertIn("最终回答仍需通过 mystic_output_lint", result["output_guidance"][-1])


class YijingQuestionGuardTests(unittest.TestCase):
    def test_career_question_can_continue(self):
        result = yijing_question_guard.guard({"question_text": "我该不该跳槽？"})
        self.assertEqual(result["question_domain"], "career")
        self.assertTrue(result["can_continue_yijing"])
        self.assertIn("工作局势", result["reframed_question"])

    def test_relationship_question_reframes_to_pattern(self):
        result = yijing_question_guard.guard({"question_text": "他会不会回来复合？"})
        self.assertEqual(result["question_domain"], "relationship")
        self.assertTrue(result["can_continue_yijing"])
        self.assertIn("互动结构", result["reframed_question"])

    def test_compound_question_is_blocked(self):
        result = yijing_question_guard.guard({"question_text": "我该不该跳槽，搬家，还是和他复合？"})
        self.assertFalse(result["is_single_matter"])
        self.assertFalse(result["can_continue_yijing"])
        self.assertTrue(result["warnings"])

    def test_repeat_question_is_blocked(self):
        result = yijing_question_guard.guard(
            {
                "question_text": "我该不该跳槽？",
                "previous_questions": ["我该不该跳槽？"],
            }
        )
        self.assertTrue(result["is_repeat_question"])
        self.assertFalse(result["can_continue_yijing"])

    def test_financial_risk_blocks_divination(self):
        result = yijing_question_guard.guard({"question_text": "用易经看我要不要贷款梭哈股票"})
        self.assertIn("professional_finance", result["risk_flags"])
        self.assertFalse(result["can_continue_yijing"])
        self.assertIn("不能替代专业判断", result["reframed_question"])

    def test_health_risk_blocks_divination(self):
        result = yijing_question_guard.guard({"question_text": "用易经看我这个病要不要停药"})
        self.assertIn("professional_health", result["risk_flags"])
        self.assertFalse(result["can_continue_yijing"])

    def test_coercion_blocks_divination(self):
        result = yijing_question_guard.guard({"question_text": "用六爻看怎么控制他让他爱我"})
        self.assertIn("coercion", result["risk_flags"])
        self.assertFalse(result["can_continue_yijing"])


class YijingHexagramRecordTests(unittest.TestCase):
    def test_all_yang_records_qian(self):
        result = yijing_hexagram_record.record(
            {"question_text": "我该不该跳槽？", "casting_method": "manual", "lines": [7, 7, 7, 7, 7, 7]}
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["base_hexagram"]["number"], 1)
        self.assertEqual(result["base_hexagram"]["name"], "乾为天")
        self.assertEqual(result["changed_hexagram"], None)

    def test_all_yin_records_kun(self):
        result = yijing_hexagram_record.record({"lines": [8, 8, 8, 8, 8, 8]})
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["base_hexagram"]["number"], 2)
        self.assertEqual(result["base_hexagram"]["name"], "坤为地")

    def test_changing_line_creates_changed_hexagram(self):
        result = yijing_hexagram_record.record({"lines": [9, 7, 7, 7, 7, 7]})
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["base_hexagram"]["number"], 1)
        self.assertEqual(result["changing_lines"], [1])
        self.assertEqual(result["changed_hexagram"]["number"], 44)
        self.assertEqual(result["changed_hexagram"]["name"], "天风姤")

    def test_object_lines_are_supported(self):
        result = yijing_hexagram_record.record(
            {
                "lines": [
                    {"value": "yang", "changing": True},
                    {"value": "yin"},
                    {"value": "yang"},
                    {"value": "yin"},
                    {"value": "yang"},
                    {"value": "yin"},
                ]
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["lines"][0]["value"], 9)
        self.assertEqual(result["lines"][0]["changing"], True)

    def test_wrong_line_count_is_invalid(self):
        result = yijing_hexagram_record.record({"lines": [7, 7, 7]})
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("expected 6 lines" in error for error in result["errors"]))

    def test_unknown_line_value_is_invalid(self):
        result = yijing_hexagram_record.record({"lines": [7, 7, 7, 7, 7, "bad"]})
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("unknown value" in error for error in result["errors"]))

    def test_expected_hexagram_mismatch_warns(self):
        result = yijing_hexagram_record.record({"lines": [7, 7, 7, 7, 7, 7], "expected_hexagram_number": 2})
        self.assertTrue(result["is_valid"])
        self.assertTrue(result["warnings"])


class QimenChartRecordTests(unittest.TestCase):
    def full_palaces(self):
        trigrams = ["坎", "坤", "震", "巽", "中", "乾", "兑", "艮", "离"]
        doors = ["休门", "生门", "伤门", "杜门", "景门", "死门", "惊门", "开门", "休门"]
        stars = ["天蓬", "天任", "天冲", "天辅", "天英", "天芮", "天柱", "天心", "天禽"]
        deities = ["值符", "腾蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天", "值符"]
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬"]
        return [
            {
                "palace": index,
                "trigram": trigrams[index - 1],
                "earth_stem": stems[index - 1],
                "heaven_stem": stems[-index],
                "door": doors[index - 1],
                "star": stars[index - 1],
                "deity": deities[index - 1],
            }
            for index in range(1, 10)
        ]

    def test_full_chart_is_valid(self):
        result = qimen_chart_record.record(
            {
                "question_text": "这个项目下一步怎么推进？",
                "chart_time": "2026-06-30T21:00:00+08:00",
                "timezone": "Asia/Shanghai",
                "location": "Shanghai",
                "dun": "阳遁",
                "ju": 3,
                "focus_targets": [{"label": "项目", "palace": 3, "reason": "以时干为用"}],
                "palaces": self.full_palaces(),
            }
        )
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["palaces"]), 9)
        self.assertEqual(result["ju"], 3)

    def test_missing_palaces_warns_not_invalid(self):
        result = qimen_chart_record.record({"palaces": self.full_palaces()[:3]})
        self.assertTrue(result["is_valid"])
        self.assertTrue(result["warnings"])
        self.assertIn("missing palace ids", result["warnings"][0])

    def test_invalid_door_star_deity_is_invalid(self):
        palaces = self.full_palaces()
        palaces[0]["door"] = "坏门"
        palaces[0]["star"] = "坏星"
        palaces[0]["deity"] = "坏神"
        result = qimen_chart_record.record({"palaces": palaces})
        self.assertFalse(result["is_valid"])
        self.assertGreaterEqual(len(result["errors"]), 3)

    def test_duplicate_palace_is_invalid(self):
        palaces = self.full_palaces()
        palaces[1]["palace"] = 1
        result = qimen_chart_record.record({"palaces": palaces})
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("duplicate palace" in error for error in result["errors"]))

    def test_invalid_ju_is_invalid(self):
        result = qimen_chart_record.record({"ju": 10, "palaces": self.full_palaces()})
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("ju must be 1-9" in error for error in result["errors"]))

    def test_invalid_focus_target_palace_is_invalid(self):
        result = qimen_chart_record.record(
            {"focus_targets": [{"label": "项目", "palace": 10}], "palaces": self.full_palaces()}
        )
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("focus target" in error for error in result["errors"]))


class QimenFocusSelectorTests(unittest.TestCase):
    def full_palaces(self):
        return QimenChartRecordTests().full_palaces()

    def test_project_focus_uses_existing_target_first(self):
        result = qimen_focus_selector.select(
            {
                "question_text": "这个项目下一步怎么推进？",
                "day_stem": "戊",
                "hour_stem": "乙",
                "duty_door": "开门",
                "duty_star": "天心",
                "focus_targets": [{"label": "项目", "palace": 3, "reason": "以时干为用"}],
                "palaces": self.full_palaces(),
            }
        )
        self.assertTrue(result["can_continue_qimen_focus"])
        self.assertEqual(result["question_domain"], "project_career")
        self.assertEqual(result["focus_candidates"][0]["label"], "项目")
        self.assertEqual(result["focus_candidates"][0]["palace"], 3)

    def test_missing_explicit_focus_is_warned_but_candidates_exist(self):
        result = qimen_focus_selector.select(
            {
                "question_text": "这个项目下一步怎么推进？",
                "day_stem": "戊",
                "hour_stem": "乙",
                "duty_door": "开门",
                "duty_star": "天心",
                "palaces": self.full_palaces(),
            }
        )
        self.assertTrue(result["can_continue_qimen_focus"])
        self.assertIn("focus_targets", result["missing_fields"])
        self.assertTrue(any("未提供人工用神" in warning for warning in result["warnings"]))

    def test_invalid_chart_blocks_focus_selection(self):
        palaces = self.full_palaces()
        palaces[0]["door"] = "坏门"
        result = qimen_focus_selector.select({"question_text": "这个项目下一步怎么推进？", "palaces": palaces})
        self.assertFalse(result["can_continue_qimen_focus"])
        self.assertFalse(result["chart_is_valid"])
        self.assertTrue(result["chart_errors"])

    def test_professional_finance_blocks_focus_reading(self):
        result = qimen_focus_selector.select(
            {
                "question_text": "用奇门看我要不要贷款梭哈股票",
                "day_stem": "戊",
                "hour_stem": "乙",
                "duty_door": "开门",
                "duty_star": "天心",
                "palaces": self.full_palaces(),
            }
        )
        self.assertFalse(result["can_continue_qimen_focus"])
        self.assertIn("professional_finance", result["risk_flags"])


class SkillReplayRunnerTests(unittest.TestCase):
    def test_all_replay_cases_pass(self):
        result = skill_replay_runner.run()
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["case_count"], 137)
        self.assertEqual(result["failed_count"], 0)
        self.assertEqual(
            {case["skill"] for case in result["cases"]},
            {
                "tarot-symbolic-reading",
                "feng-shui-space-audit",
                "ritual-safety-advisor",
                "folk-custom-consultation",
                "yijing-symbolic-consultation",
                "liuyao-symbolic-consultation",
                "meihua-symbolic-consultation",
                "qimen-chart-consultation",
                "mingli-bazi-ziwei-consultation",
                "naming-symbolic-consultation",
                "astrology-symbolic-consultation",
                "dream-symbolic-consultation",
                "date-selection-consultation",
                "physiognomy-symbolic-consultation",
                "oracle-lot-symbolic-consultation",
                "oracle-card-symbolic-consultation",
                "cartomancy-symbolic-consultation",
                "dice-symbolic-consultation",
                "tasseography-symbolic-consultation",
                "numerology-symbolic-consultation",
                "pendulum-symbolic-consultation",
                "rune-symbolic-consultation",
                "lenormand-symbolic-consultation",
                "crystal-symbolic-consultation",
                "candle-symbolic-consultation",
                "incense-symbolic-consultation",
                "aroma-symbolic-consultation",
                "herbal-symbolic-consultation",
                "sigil-symbolic-consultation",
                "dowsing-symbolic-consultation",
                "body-omen-symbolic-consultation",
                "scrying-symbolic-consultation",
                "casting-lots-symbolic-consultation",
                "character-divination-symbolic-consultation",
                "flower-symbolic-consultation",
                "animal-omen-symbolic-consultation",
                "aura-chakra-symbolic-consultation",
                "past-life-akashic-symbolic-consultation",
                "moon-phase-symbolic-consultation",
                "spirit-message-symbolic-consultation",
                "psychometry-symbolic-consultation",
                "bibliomancy-symbolic-consultation",
                "sky-omen-symbolic-consultation",
                "manifestation-symbolic-consultation",
                "pet-communication-symbolic-consultation",
                "synchronicity-symbolic-consultation",
                "planetary-retrograde-symbolic-consultation",
                "spiritual-protection-symbolic-consultation",
                "deity-ancestor-symbolic-consultation",
                "sleep-paralysis-symbolic-consultation",
                "wealth-luck-symbolic-consultation",
                "relationship-luck-symbolic-consultation",
                "consecration-symbolic-consultation",
                "lost-object-symbolic-consultation",
                "sound-cleansing-symbolic-consultation",
                "western-geomancy-symbolic-consultation",
                "nine-star-ki-symbolic-consultation",
                "human-design-symbolic-consultation",
                "talisman-symbolic-consultation",
                "color-symbolic-consultation",
                "zodiac-symbolic-consultation",
            },
        )

    def test_single_replay_case_filter(self):
        result = skill_replay_runner.run("tarot-normal-career")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["case_count"], 1)
        self.assertEqual(result["case_ids"], ["tarot-normal-career"])
        self.assertEqual(result["cases"][0]["skill"], "tarot-symbolic-reading")

    def test_unknown_replay_case_raises(self):
        with self.assertRaises(ValueError):
            skill_replay_runner.run("missing-case")


class SkillTranscriptRunnerTests(unittest.TestCase):
    def test_all_transcript_cases_pass(self):
        result = skill_transcript_runner.run()
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["transcript_count"], 63)
        self.assertEqual(result["failed_count"], 0)
        self.assertEqual(
            {item["skill"] for item in result["transcripts"]},
            {
                "tarot-symbolic-reading",
                "feng-shui-space-audit",
                "ritual-safety-advisor",
                "folk-custom-consultation",
                "yijing-symbolic-consultation",
                "liuyao-symbolic-consultation",
                "meihua-symbolic-consultation",
                "qimen-chart-consultation",
                "mingli-bazi-ziwei-consultation",
                "naming-symbolic-consultation",
                "astrology-symbolic-consultation",
                "dream-symbolic-consultation",
                "date-selection-consultation",
                "physiognomy-symbolic-consultation",
                "oracle-lot-symbolic-consultation",
                "oracle-card-symbolic-consultation",
                "cartomancy-symbolic-consultation",
                "dice-symbolic-consultation",
                "tasseography-symbolic-consultation",
                "numerology-symbolic-consultation",
                "pendulum-symbolic-consultation",
                "rune-symbolic-consultation",
                "lenormand-symbolic-consultation",
                "crystal-symbolic-consultation",
                "candle-symbolic-consultation",
                "incense-symbolic-consultation",
                "aroma-symbolic-consultation",
                "herbal-symbolic-consultation",
                "sigil-symbolic-consultation",
                "dowsing-symbolic-consultation",
                "body-omen-symbolic-consultation",
                "scrying-symbolic-consultation",
                "casting-lots-symbolic-consultation",
                "character-divination-symbolic-consultation",
                "flower-symbolic-consultation",
                "animal-omen-symbolic-consultation",
                "aura-chakra-symbolic-consultation",
                "past-life-akashic-symbolic-consultation",
                "moon-phase-symbolic-consultation",
                "spirit-message-symbolic-consultation",
                "psychometry-symbolic-consultation",
                "bibliomancy-symbolic-consultation",
                "sky-omen-symbolic-consultation",
                "manifestation-symbolic-consultation",
                "pet-communication-symbolic-consultation",
                "synchronicity-symbolic-consultation",
                "planetary-retrograde-symbolic-consultation",
                "spiritual-protection-symbolic-consultation",
                "deity-ancestor-symbolic-consultation",
                "sleep-paralysis-symbolic-consultation",
                "wealth-luck-symbolic-consultation",
                "relationship-luck-symbolic-consultation",
                "consecration-symbolic-consultation",
                "lost-object-symbolic-consultation",
                "sound-cleansing-symbolic-consultation",
                "western-geomancy-symbolic-consultation",
                "nine-star-ki-symbolic-consultation",
                "human-design-symbolic-consultation",
                "talisman-symbolic-consultation",
                "color-symbolic-consultation",
                "zodiac-symbolic-consultation",
            },
        )

    def test_single_transcript_filter(self):
        result = skill_transcript_runner.run("ritual-danger-to-safe-protocol")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["transcript_count"], 1)
        self.assertEqual(result["transcript_ids"], ["ritual-danger-to-safe-protocol"])
        self.assertEqual(result["transcripts"][0]["scenario"], "blocked_then_safe")

    def test_unknown_transcript_raises(self):
        with self.assertRaises(ValueError):
            skill_transcript_runner.run("missing-transcript")


if __name__ == "__main__":
    unittest.main()
