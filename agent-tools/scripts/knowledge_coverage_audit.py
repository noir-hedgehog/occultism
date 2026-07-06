#!/usr/bin/env python3
"""Audit mystic-agent knowledge base coverage across domains."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DOMAIN_REQUIREMENTS: dict[str, dict[str, Any]] = {
    "tarot": {
        "display_name": "塔罗",
        "sop": ["知识库/SOP/01-塔罗解读.md"],
        "knowledge": ["知识库/流派/塔罗.md", "知识库/流派/塔罗牌义速查.md", "知识库/流派/塔罗牌阵案例与逆位策略.md"],
        "skill": ["codex-skills/tarot-symbolic-reading/SKILL.md"],
        "tools": ["tarot_spread_selector", "tarot_draw_recorder", "tarot_draw_simulator", "tarot_card_lookup", "tarot_interpretation_planner", "tarot_combination_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "date_selection": {
        "display_name": "择日/黄历",
        "sop": ["知识库/SOP/15-择日与黄历象征咨询.md"],
        "knowledge": ["知识库/流派/择日与黄历.md"],
        "skill": ["codex-skills/date-selection-consultation/SKILL.md"],
        "tools": ["date_selection_guard", "almanac_symbol_lookup", "date_constraint_recorder", "date_option_ranker"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "oracle_lot": {
        "display_name": "求签/签文",
        "sop": ["知识库/SOP/17-求签与签文象征咨询.md"],
        "knowledge": ["知识库/流派/求签与签文.md"],
        "skill": ["codex-skills/oracle-lot-symbolic-consultation/SKILL.md"],
        "tools": ["oracle_lot_request_guard", "oracle_lot_record_builder", "oracle_lot_symbol_lookup", "oracle_lot_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "oracle_card": {
        "display_name": "神谕卡",
        "sop": ["知识库/SOP/22-神谕卡象征咨询.md"],
        "knowledge": ["知识库/流派/神谕卡.md"],
        "skill": ["codex-skills/oracle-card-symbolic-consultation/SKILL.md"],
        "tools": ["oracle_card_request_guard", "oracle_card_draw_recorder", "oracle_card_symbol_lookup", "oracle_card_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "cartomancy": {
        "display_name": "扑克牌占卜",
        "sop": ["知识库/SOP/29-扑克牌占卜象征咨询.md"],
        "knowledge": ["知识库/流派/扑克牌占卜.md"],
        "skill": ["codex-skills/cartomancy-symbolic-consultation/SKILL.md"],
        "tools": ["cartomancy_request_guard", "cartomancy_draw_recorder", "cartomancy_card_lookup", "cartomancy_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "dice": {
        "display_name": "星骰/占卜骰",
        "sop": ["知识库/SOP/27-星骰占卜骰象征咨询.md"],
        "knowledge": ["知识库/流派/星骰与占卜骰.md"],
        "skill": ["codex-skills/dice-symbolic-consultation/SKILL.md"],
        "tools": ["dice_request_guard", "dice_roll_recorder", "dice_symbol_lookup", "dice_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "tasseography": {
        "display_name": "茶叶/咖啡渣占卜",
        "sop": ["知识库/SOP/28-茶叶咖啡渣占卜象征咨询.md"],
        "knowledge": ["知识库/流派/茶叶与咖啡渣占卜.md"],
        "skill": ["codex-skills/tasseography-symbolic-consultation/SKILL.md"],
        "tools": ["tasseography_request_guard", "tasseography_pattern_recorder", "tasseography_symbol_lookup", "tasseography_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "lenormand": {
        "display_name": "雷诺曼卡",
        "sop": ["知识库/SOP/21-雷诺曼卡象征咨询.md"],
        "knowledge": ["知识库/流派/雷诺曼卡.md"],
        "skill": ["codex-skills/lenormand-symbolic-consultation/SKILL.md"],
        "tools": ["lenormand_request_guard", "lenormand_draw_recorder", "lenormand_card_lookup", "lenormand_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "crystal": {
        "display_name": "水晶/能量石",
        "sop": ["知识库/SOP/23-水晶与能量石象征咨询.md"],
        "knowledge": ["知识库/流派/水晶与能量石.md"],
        "skill": ["codex-skills/crystal-symbolic-consultation/SKILL.md"],
        "tools": ["crystal_request_guard", "crystal_item_recorder", "crystal_symbol_lookup", "crystal_use_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "candle": {
        "display_name": "蜡烛火焰/蜡泪",
        "sop": ["知识库/SOP/30-蜡烛火焰蜡泪象征咨询.md"],
        "knowledge": ["知识库/流派/蜡烛火焰与蜡泪.md"],
        "skill": ["codex-skills/candle-symbolic-consultation/SKILL.md"],
        "tools": ["candle_request_guard", "candle_observation_recorder", "candle_symbol_lookup", "candle_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "incense": {
        "display_name": "香火/香灰/烟形",
        "sop": ["知识库/SOP/31-香火香灰烟形象征咨询.md"],
        "knowledge": ["知识库/流派/香火香灰与烟形.md"],
        "skill": ["codex-skills/incense-symbolic-consultation/SKILL.md"],
        "tools": ["incense_request_guard", "incense_observation_recorder", "incense_symbol_lookup", "incense_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "aroma": {
        "display_name": "芳香/精油/气味象征",
        "sop": ["知识库/SOP/59-芳香精油气味象征咨询.md"],
        "knowledge": ["知识库/流派/芳香精油与气味象征.md"],
        "skill": ["codex-skills/aroma-symbolic-consultation/SKILL.md"],
        "tools": ["aroma_request_guard", "aroma_context_recorder", "aroma_symbol_lookup", "aroma_practice_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "herbal": {
        "display_name": "草本/香草/植物魔法象征",
        "sop": ["知识库/SOP/60-草本香草植物魔法象征咨询.md"],
        "knowledge": ["知识库/流派/草本香草与植物魔法象征.md"],
        "skill": ["codex-skills/herbal-symbolic-consultation/SKILL.md"],
        "tools": ["herbal_request_guard", "herbal_context_recorder", "herbal_symbol_lookup", "herbal_practice_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "sigil": {
        "display_name": "Sigil/符号印记/魔法阵象征",
        "sop": ["知识库/SOP/61-Sigil符号印记魔法阵象征咨询.md"],
        "knowledge": ["知识库/流派/Sigil符号印记与魔法阵象征.md"],
        "skill": ["codex-skills/sigil-symbolic-consultation/SKILL.md"],
        "tools": ["sigil_request_guard", "sigil_context_recorder", "sigil_symbol_lookup", "sigil_practice_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "dowsing": {
        "display_name": "占杖/寻水杖/探测棒象征",
        "sop": ["知识库/SOP/62-占杖寻水杖探测棒象征咨询.md"],
        "knowledge": ["知识库/流派/占杖寻水杖与探测棒象征.md"],
        "skill": ["codex-skills/dowsing-symbolic-consultation/SKILL.md"],
        "tools": ["dowsing_request_guard", "dowsing_context_recorder", "dowsing_symbol_lookup", "dowsing_practice_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "body_omen": {
        "display_name": "身体征兆/眼跳/耳鸣/喷嚏象征",
        "sop": ["知识库/SOP/63-身体征兆眼跳耳鸣喷嚏象征咨询.md"],
        "knowledge": ["知识库/流派/身体征兆眼跳耳鸣喷嚏象征.md"],
        "skill": ["codex-skills/body-omen-symbolic-consultation/SKILL.md"],
        "tools": ["body_omen_request_guard", "body_omen_context_recorder", "body_omen_symbol_lookup", "body_omen_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "scrying": {
        "display_name": "水晶球/镜面/水面凝视",
        "sop": ["知识库/SOP/32-水晶球镜面水面凝视象征咨询.md"],
        "knowledge": ["知识库/流派/水晶球镜面与水面凝视.md"],
        "skill": ["codex-skills/scrying-symbolic-consultation/SKILL.md"],
        "tools": ["scrying_request_guard", "scrying_observation_recorder", "scrying_symbol_lookup", "scrying_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "casting_lots": {
        "display_name": "骨/贝壳/石子/符物抛掷",
        "sop": ["知识库/SOP/33-骨贝石子符物抛掷象征咨询.md"],
        "knowledge": ["知识库/流派/骨贝石子与符物抛掷.md"],
        "skill": ["codex-skills/casting-lots-symbolic-consultation/SKILL.md"],
        "tools": ["casting_lots_request_guard", "casting_lots_layout_recorder", "casting_lots_symbol_lookup", "casting_lots_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "character_divination": {
        "display_name": "测字/拆字",
        "sop": ["知识库/SOP/34-测字拆字象征咨询.md"],
        "knowledge": ["知识库/流派/测字与拆字.md"],
        "skill": ["codex-skills/character-divination-symbolic-consultation/SKILL.md"],
        "tools": ["cezi_request_guard", "cezi_character_recorder", "cezi_symbol_lookup", "cezi_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "flower": {
        "display_name": "花语/植物象征",
        "sop": ["知识库/SOP/35-花语植物象征咨询.md"],
        "knowledge": ["知识库/流派/花语与植物象征.md"],
        "skill": ["codex-skills/flower-symbolic-consultation/SKILL.md"],
        "tools": ["flower_request_guard", "flower_item_recorder", "flower_symbol_lookup", "flower_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "animal_omen": {
        "display_name": "动物征兆/鸟兽虫鱼",
        "sop": ["知识库/SOP/36-动物征兆鸟兽虫鱼象征咨询.md"],
        "knowledge": ["知识库/流派/动物征兆与鸟兽虫鱼.md"],
        "skill": ["codex-skills/animal-omen-symbolic-consultation/SKILL.md"],
        "tools": ["animal_omen_request_guard", "animal_omen_observation_recorder", "animal_omen_symbol_lookup", "animal_omen_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "aura_chakra": {
        "display_name": "气场/脉轮/能量感受",
        "sop": ["知识库/SOP/37-气场脉轮能量感受象征咨询.md"],
        "knowledge": ["知识库/流派/气场脉轮与能量感受.md"],
        "skill": ["codex-skills/aura-chakra-symbolic-consultation/SKILL.md"],
        "tools": ["aura_chakra_request_guard", "aura_chakra_sensation_recorder", "aura_chakra_symbol_lookup", "aura_chakra_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "past_life": {
        "display_name": "前世/阿卡西/灵魂课题",
        "sop": ["知识库/SOP/38-前世阿卡西灵魂课题象征咨询.md"],
        "knowledge": ["知识库/流派/前世阿卡西与灵魂课题.md"],
        "skill": ["codex-skills/past-life-akashic-symbolic-consultation/SKILL.md"],
        "tools": ["past_life_request_guard", "past_life_narrative_recorder", "past_life_symbol_lookup", "past_life_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "moon_phase": {
        "display_name": "月相/月亮周期",
        "sop": ["知识库/SOP/39-月相月亮周期象征咨询.md"],
        "knowledge": ["知识库/流派/月相与月亮周期.md"],
        "skill": ["codex-skills/moon-phase-symbolic-consultation/SKILL.md"],
        "tools": ["moon_phase_request_guard", "moon_phase_context_recorder", "moon_phase_symbol_lookup", "moon_phase_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "spirit_message": {
        "display_name": "通灵/高我/灵性讯息",
        "sop": ["知识库/SOP/40-通灵高我讯息象征咨询.md"],
        "knowledge": ["知识库/流派/通灵高我与灵性讯息.md"],
        "skill": ["codex-skills/spirit-message-symbolic-consultation/SKILL.md"],
        "tools": ["spirit_message_request_guard", "spirit_message_record_builder", "spirit_message_symbol_lookup", "spirit_message_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "psychometry": {
        "display_name": "物品感应/触物占卜",
        "sop": ["知识库/SOP/41-物品感应触物占卜象征咨询.md"],
        "knowledge": ["知识库/流派/物品感应与触物占卜.md"],
        "skill": ["codex-skills/psychometry-symbolic-consultation/SKILL.md"],
        "tools": ["psychometry_request_guard", "psychometry_object_recorder", "psychometry_symbol_lookup", "psychometry_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "bibliomancy": {
        "display_name": "书占/随机翻书",
        "sop": ["知识库/SOP/42-书占随机翻书象征咨询.md"],
        "knowledge": ["知识库/流派/书占与随机翻书.md"],
        "skill": ["codex-skills/bibliomancy-symbolic-consultation/SKILL.md"],
        "tools": ["bibliomancy_request_guard", "bibliomancy_source_recorder", "bibliomancy_symbol_lookup", "bibliomancy_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "sky_omen": {
        "display_name": "天象/云形征兆",
        "sop": ["知识库/SOP/43-天象云形征兆象征咨询.md"],
        "knowledge": ["知识库/流派/天象云形与天气征兆.md"],
        "skill": ["codex-skills/sky-omen-symbolic-consultation/SKILL.md"],
        "tools": ["sky_omen_request_guard", "sky_omen_observation_recorder", "sky_omen_symbol_lookup", "sky_omen_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "manifestation": {
        "display_name": "祈愿/显化/愿望仪式",
        "sop": ["知识库/SOP/44-祈愿显化愿望仪式象征咨询.md"],
        "knowledge": ["知识库/流派/祈愿显化与愿望仪式.md"],
        "skill": ["codex-skills/manifestation-symbolic-consultation/SKILL.md"],
        "tools": ["manifestation_request_guard", "manifestation_intention_recorder", "manifestation_symbol_lookup", "manifestation_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "pet_communication": {
        "display_name": "宠物沟通/动物灵性讯息",
        "sop": ["知识库/SOP/45-宠物沟通动物灵性讯息象征咨询.md"],
        "knowledge": ["知识库/流派/宠物沟通与动物灵性讯息.md"],
        "skill": ["codex-skills/pet-communication-symbolic-consultation/SKILL.md"],
        "tools": ["pet_communication_request_guard", "pet_communication_context_recorder", "pet_communication_symbol_lookup", "pet_communication_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "synchronicity": {
        "display_name": "同步性/天使数字/重复征兆",
        "sop": ["知识库/SOP/46-同步性天使数字重复征兆象征咨询.md"],
        "knowledge": ["知识库/流派/同步性天使数字与重复征兆.md"],
        "skill": ["codex-skills/synchronicity-symbolic-consultation/SKILL.md"],
        "tools": ["synchronicity_request_guard", "synchronicity_event_recorder", "synchronicity_symbol_lookup", "synchronicity_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "planetary_retrograde": {
        "display_name": "水逆/行星逆行/星象天气",
        "sop": ["知识库/SOP/47-水逆行星逆行星象天气象征咨询.md"],
        "knowledge": ["知识库/流派/水逆行星逆行与星象天气.md"],
        "skill": ["codex-skills/planetary-retrograde-symbolic-consultation/SKILL.md"],
        "tools": ["planetary_retrograde_request_guard", "planetary_retrograde_context_recorder", "planetary_retrograde_symbol_lookup", "planetary_retrograde_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "spiritual_protection": {
        "display_name": "恶眼/能量防护/断联",
        "sop": ["知识库/SOP/48-恶眼能量防护断联象征咨询.md"],
        "knowledge": ["知识库/流派/恶眼能量防护与断联.md"],
        "skill": ["codex-skills/spiritual-protection-symbolic-consultation/SKILL.md"],
        "tools": ["spiritual_protection_request_guard", "spiritual_protection_context_recorder", "spiritual_protection_symbol_lookup", "spiritual_protection_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "deity_ancestor": {
        "display_name": "神明/祖先/供奉/祭拜",
        "sop": ["知识库/SOP/49-神明祖先供奉祭拜象征咨询.md"],
        "knowledge": ["知识库/流派/神明祖先供奉与祭拜.md"],
        "skill": ["codex-skills/deity-ancestor-symbolic-consultation/SKILL.md"],
        "tools": ["deity_ancestor_request_guard", "deity_ancestor_context_recorder", "deity_ancestor_symbol_lookup", "deity_ancestor_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "sleep_paralysis": {
        "display_name": "鬼压床/梦魇/睡前灵异恐惧",
        "sop": ["知识库/SOP/50-鬼压床梦魇睡前灵异恐惧象征咨询.md"],
        "knowledge": ["知识库/流派/鬼压床梦魇与睡前灵异恐惧.md"],
        "skill": ["codex-skills/sleep-paralysis-symbolic-consultation/SKILL.md"],
        "tools": ["sleep_paralysis_request_guard", "sleep_paralysis_context_recorder", "sleep_paralysis_symbol_lookup", "sleep_paralysis_reflection_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "wealth_luck": {
        "display_name": "招财/财运/财库",
        "sop": ["知识库/SOP/51-招财财运财库象征咨询.md"],
        "knowledge": ["知识库/流派/招财财运与财库象征.md"],
        "skill": ["codex-skills/wealth-luck-symbolic-consultation/SKILL.md"],
        "tools": ["wealth_luck_request_guard", "wealth_luck_context_recorder", "wealth_luck_symbol_lookup", "wealth_luck_action_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "relationship_luck": {
        "display_name": "桃花/姻缘/人缘",
        "sop": ["知识库/SOP/52-桃花姻缘人缘象征咨询.md"],
        "knowledge": ["知识库/流派/桃花姻缘与人缘象征.md"],
        "skill": ["codex-skills/relationship-luck-symbolic-consultation/SKILL.md"],
        "tools": ["relationship_luck_request_guard", "relationship_luck_context_recorder", "relationship_luck_symbol_lookup", "relationship_luck_action_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "consecration": {
        "display_name": "开光/加持/净物",
        "sop": ["知识库/SOP/53-开光加持净物象征咨询.md"],
        "knowledge": ["知识库/流派/开光加持与净物象征.md"],
        "skill": ["codex-skills/consecration-symbolic-consultation/SKILL.md"],
        "tools": ["consecration_request_guard", "consecration_context_recorder", "consecration_symbol_lookup", "consecration_care_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "lost_object": {
        "display_name": "失物/寻物",
        "sop": ["知识库/SOP/54-失物寻物象征咨询.md"],
        "knowledge": ["知识库/流派/失物寻物象征.md"],
        "skill": ["codex-skills/lost-object-symbolic-consultation/SKILL.md"],
        "tools": ["lost_object_request_guard", "lost_object_context_recorder", "lost_object_symbol_lookup", "lost_object_search_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "sound_cleansing": {
        "display_name": "声响净化/铃钵",
        "sop": ["知识库/SOP/55-声响净化象征咨询.md"],
        "knowledge": ["知识库/流派/声响净化与铃钵象征.md"],
        "skill": ["codex-skills/sound-cleansing-symbolic-consultation/SKILL.md"],
        "tools": ["sound_cleansing_request_guard", "sound_cleansing_context_recorder", "sound_cleansing_symbol_lookup", "sound_cleansing_practice_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "western_geomancy": {
        "display_name": "西洋土占/盾形盘",
        "sop": ["知识库/SOP/56-西洋土占盾形盘象征咨询.md"],
        "knowledge": ["知识库/流派/西洋土占与盾形盘.md"],
        "skill": ["codex-skills/western-geomancy-symbolic-consultation/SKILL.md"],
        "tools": ["western_geomancy_request_guard", "western_geomancy_chart_recorder", "western_geomancy_figure_lookup", "western_geomancy_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "nine_star_ki": {
        "display_name": "九星气学/九宫命星",
        "sop": ["知识库/SOP/57-九星气学九宫命星象征咨询.md"],
        "knowledge": ["知识库/流派/九星气学与九宫命星.md"],
        "skill": ["codex-skills/nine-star-ki-symbolic-consultation/SKILL.md"],
        "tools": ["nine_star_ki_request_guard", "nine_star_ki_profile_recorder", "nine_star_ki_symbol_lookup", "nine_star_ki_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "human_design": {
        "display_name": "人类图/Human Design",
        "sop": ["知识库/SOP/58-人类图象征咨询.md"],
        "knowledge": ["知识库/流派/人类图.md"],
        "skill": ["codex-skills/human-design-symbolic-consultation/SKILL.md"],
        "tools": ["human_design_request_guard", "human_design_chart_recorder", "human_design_symbol_lookup", "human_design_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "talisman": {
        "display_name": "护符/符箓",
        "sop": ["知识库/SOP/24-护符符箓象征咨询.md"],
        "knowledge": ["知识库/流派/护符符箓.md"],
        "skill": ["codex-skills/talisman-symbolic-consultation/SKILL.md"],
        "tools": ["talisman_request_guard", "talisman_record_builder", "talisman_symbol_lookup", "talisman_use_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "color": {
        "display_name": "五行颜色/开运色",
        "sop": ["知识库/SOP/26-五行颜色开运色象征咨询.md"],
        "knowledge": ["知识库/流派/五行颜色与开运色.md"],
        "skill": ["codex-skills/color-symbolic-consultation/SKILL.md"],
        "tools": ["color_request_guard", "color_profile_recorder", "color_symbol_lookup", "color_palette_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "zodiac": {
        "display_name": "生肖/太岁",
        "sop": ["知识库/SOP/25-生肖太岁象征咨询.md"],
        "knowledge": ["知识库/流派/生肖太岁.md"],
        "skill": ["codex-skills/zodiac-symbolic-consultation/SKILL.md"],
        "tools": ["zodiac_request_guard", "zodiac_profile_recorder", "zodiac_symbol_lookup", "zodiac_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "fengshui": {
        "display_name": "风水",
        "sop": ["知识库/SOP/02-风水空间审视.md", "知识库/SOP/07-风水观察记录规范.md"],
        "knowledge": ["知识库/流派/风水.md", "知识库/流派/风水八卦方位映射.md", "知识库/流派/风水理气派别边界.md", "知识库/流派/风水阳宅案例库.md"],
        "skill": ["codex-skills/feng-shui-space-audit/SKILL.md"],
        "tools": ["fengshui_school_guard", "fengshui_observation_recorder", "fengshui_space_checklist", "fengshui_yangzhai_case_library", "fengshui_bagua_mapper", "fengshui_recommendation_ranker"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "ritual": {
        "display_name": "空间净化/驱邪",
        "sop": ["知识库/SOP/03-空间净化与驱邪安全咨询.md"],
        "knowledge": [
            "知识库/流派/空间净化与驱邪.md",
            "知识库/流派/民俗仪式资料来源规范.md",
            "知识库/流派/地区宗教来源样例.md",
            "知识库/流派/仪式低风险真实案例集.md",
        ],
        "skill": ["codex-skills/ritual-safety-advisor/SKILL.md"],
        "tools": ["ritual_safety_check", "ritual_source_example_lookup", "ritual_source_guard", "ritual_low_risk_protocol"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "folk_custom": {
        "display_name": "民俗节令/禁忌",
        "sop": ["知识库/SOP/13-民俗节令与禁忌咨询.md"],
        "knowledge": ["知识库/流派/民俗节令与禁忌.md"],
        "skill": ["codex-skills/folk-custom-consultation/SKILL.md"],
        "tools": ["folk_custom_lookup", "folk_source_recorder", "folk_taboo_reframer"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "yijing": {
        "display_name": "易经/周易",
        "sop": ["知识库/SOP/04-易经占问.md"],
        "knowledge": ["知识库/流派/易经.md", "知识库/流派/易经64卦速查.md", "知识库/流派/易经384爻索引.md", "知识库/流派/易经原典注疏来源规范.md"],
        "skill": ["codex-skills/yijing-symbolic-consultation/SKILL.md"],
        "tools": ["yijing_question_guard", "yijing_casting_method_advisor", "yijing_casting_simulator", "yijing_hexagram_record", "yijing_hexagram_lookup", "yijing_line_lookup", "yijing_source_reference_guard"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "liuyao": {
        "display_name": "六爻",
        "sop": ["知识库/SOP/10-六爻占问.md"],
        "knowledge": ["知识库/流派/六爻.md"],
        "skill": ["codex-skills/liuyao-symbolic-consultation/SKILL.md"],
        "tools": ["liuyao_symbol_lookup", "liuyao_chart_recorder", "liuyao_focus_selector"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "meihua": {
        "display_name": "梅花易数",
        "sop": ["知识库/SOP/11-梅花易数占问.md"],
        "knowledge": ["知识库/流派/梅花易数.md"],
        "skill": ["codex-skills/meihua-symbolic-consultation/SKILL.md"],
        "tools": ["meihua_symbol_lookup", "meihua_casting_recorder", "meihua_omen_recorder", "meihua_relation_interpreter"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "qimen": {
        "display_name": "奇门遁甲",
        "sop": ["知识库/SOP/05-奇门遁甲局势分析.md"],
        "knowledge": ["知识库/流派/奇门遁甲.md", "知识库/流派/奇门用神与盘式解读骨架.md"],
        "skill": ["codex-skills/qimen-chart-consultation/SKILL.md"],
        "tools": ["qimen_method_guard", "qimen_school_reference", "qimen_chart_record", "qimen_focus_selector"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "mingli": {
        "display_name": "八字/紫微斗数",
        "sop": ["知识库/SOP/06-命理咨询边界.md", "知识库/SOP/08-命理排盘参数记录.md"],
        "knowledge": ["知识库/流派/八字与紫微斗数.md", "知识库/流派/命理象征索引.md"],
        "skill": ["codex-skills/mingli-bazi-ziwei-consultation/SKILL.md"],
        "tools": ["bazi_ziwei_intake_guard", "bazi_ziwei_chart_record", "mingli_school_reference", "mingli_symbol_lookup"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "naming": {
        "display_name": "姓名学",
        "sop": ["知识库/SOP/12-姓名学命名咨询.md"],
        "knowledge": ["知识库/流派/姓名学.md"],
        "skill": ["codex-skills/naming-symbolic-consultation/SKILL.md"],
        "tools": ["naming_symbol_lookup", "naming_candidate_comparator", "naming_brand_scenario_scorer"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "numerology": {
        "display_name": "数字象征/号码",
        "sop": ["知识库/SOP/18-数字象征与号码咨询.md"],
        "knowledge": ["知识库/流派/数字象征与号码.md"],
        "skill": ["codex-skills/numerology-symbolic-consultation/SKILL.md"],
        "tools": ["numerology_request_guard", "numerology_profile_recorder", "numerology_symbol_lookup", "numerology_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "pendulum": {
        "display_name": "灵摆/摆锤",
        "sop": ["知识库/SOP/19-灵摆占卜象征咨询.md"],
        "knowledge": ["知识库/流派/灵摆占卜.md"],
        "skill": ["codex-skills/pendulum-symbolic-consultation/SKILL.md"],
        "tools": ["pendulum_request_guard", "pendulum_session_recorder", "pendulum_symbol_lookup", "pendulum_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "rune": {
        "display_name": "卢恩符文",
        "sop": ["知识库/SOP/20-卢恩符文象征咨询.md"],
        "knowledge": ["知识库/流派/卢恩符文.md"],
        "skill": ["codex-skills/rune-symbolic-consultation/SKILL.md"],
        "tools": ["rune_request_guard", "rune_cast_recorder", "rune_symbol_lookup", "rune_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "physiognomy": {
        "display_name": "手相/面相",
        "sop": ["知识库/SOP/16-手相面相象征咨询.md"],
        "knowledge": ["知识库/流派/手相与面相.md"],
        "skill": ["codex-skills/physiognomy-symbolic-consultation/SKILL.md"],
        "tools": ["physiognomy_request_guard", "physiognomy_observation_recorder", "physiognomy_symbol_lookup", "physiognomy_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "astrology": {
        "display_name": "占星/星盘",
        "sop": ["知识库/SOP/09-占星星盘象征咨询.md"],
        "knowledge": ["知识库/流派/占星.md"],
        "skill": ["codex-skills/astrology-symbolic-consultation/SKILL.md"],
        "tools": ["astrology_compatibility_guard", "astrology_chart_record", "astrology_symbol_lookup"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
    "dream": {
        "display_name": "解梦/梦境象征",
        "sop": ["知识库/SOP/14-解梦与梦境象征咨询.md"],
        "knowledge": ["知识库/流派/解梦.md"],
        "skill": ["codex-skills/dream-symbolic-consultation/SKILL.md"],
        "tools": ["dream_record_builder", "dream_symbol_lookup", "dream_interpretation_planner"],
        "verification": ["skill_replay_runner", "skill_transcript_runner"],
    },
}

COMMON_REQUIREMENTS = {
    "knowledge_base": [
        "README.md",
        "知识库/00-总览.md",
        "知识库/01-安全边界.md",
        "知识库/02-流派地图.md",
        "知识库/04-质量检查清单.md",
        "知识库/05-路线图.md",
        "知识库/版本记录.md",
        "知识库/维护节奏.md",
        "知识库/真实对话Fixture规范.md",
        "知识库/Agent运行时DryRun验证.md",
        "知识库/Agent工具WrapperManifest.md",
        "知识库/Agent工具定义导出.md",
        "知识库/Agent工具定义验证.md",
        "知识库/Agent工具注册表.md",
        "知识库/Agent工具注册表验证.md",
        "知识库/工具与Skill Manifest规范.md",
        "知识库/导航索引.md",
        "知识库/内容审校包.md",
        "知识库/内容审校反馈记录规范.md",
        "知识库/Skill安装准备报告.md",
        "知识库/SOP-Tool-Skill追踪矩阵.md",
        "知识库/试运行准备度报告.md",
        "知识库/外部证据入口包.md",
        "知识库/Agent运行时交接包.md",
        "知识库/看板.md",
        "知识库/仪表盘.md",
    ],
    "templates": [
        "知识库/模板/Tool规格模板.md",
        "知识库/模板/SOP模板.md",
        "知识库/模板/流派知识卡模板.md",
        "知识库/模板/Codex-Skill模板.md",
    ],
    "shared_tools": [
        "agent_route_smoke_runner",
        "agent_runtime_dry_run_runner",
        "agent_runtime_handoff_builder",
        "agent_tool_definition_exporter",
        "agent_tool_definition_validator",
        "agent_tool_registry_builder",
        "agent_tool_registry_validator",
        "agent_tool_wrapper_manifest_builder",
        "agent_workflow_router",
        "codex_skill_blueprint_validator",
        "codex_skill_installer",
        "content_review_feedback_recorder",
        "content_review_packet_builder",
        "external_evidence_intake_builder",
        "mystic_intake_triage",
        "mystic_output_lint",
        "knowledge_coverage_audit",
        "knowledge_navigation_builder",
        "pilot_readiness_report",
        "release_gate_runner",
        "release_manifest_builder",
        "skill_install_readiness_report",
        "sop_traceability_matrix_builder",
        "tool_manifest_builder",
        "symbolic_depth_lookup",
        "symbolic_case_library",
        "transcript_anonymizer",
        "transcript_fixture_builder",
    ],
    "shared_verification": [
        "agent-tools/tests/test_tools.py",
        "agent-tools/tests/cases.md",
        "知识库/Skill回放验证.md",
        "知识库/Skill多轮回放验证.md",
        "知识库/匿名真实对话验证流程.md",
        "知识库/真实对话Fixture规范.md",
        "知识库/Agent路由冒烟验证.md",
    ],
}


def tool_files(tool: str) -> dict[str, str]:
    script = f"agent-tools/scripts/{tool}.py"
    schema = f"agent-tools/schemas/{tool.replace('_', '-')}.schema.json"
    spec = f"agent-tools/specs/{tool.replace('_', '-')}.md"
    if tool == "mystic_intake_triage":
        schema = "agent-tools/schemas/mystic-intake.schema.json"
        spec = "agent-tools/specs/mystic-intake-triage.md"
    if tool == "ritual_safety_check":
        schema = "agent-tools/schemas/ritual-safety.schema.json"
        spec = "agent-tools/specs/ritual-safety-check.md"
    return {"script": script, "schema": schema, "spec": spec}


def path_status(root: Path, paths: list[str]) -> dict[str, Any]:
    present = [path for path in paths if (root / path).exists()]
    missing = [path for path in paths if not (root / path).exists()]
    return {"present": present, "missing": missing, "is_complete": not missing}


def tool_status(root: Path, tools: list[str]) -> dict[str, Any]:
    present: list[dict[str, str]] = []
    missing: list[str] = []
    for tool in tools:
        files = tool_files(tool)
        absent = [path for path in files.values() if not (root / path).exists()]
        if absent:
            missing.extend(absent)
        else:
            present.append({"tool": tool, **files})
    return {"present": present, "missing": missing, "is_complete": not missing}


def level_for_sections(sections: dict[str, Any]) -> str:
    if all(section["is_complete"] for section in sections.values()):
        return "L3 可验证"
    if sections["sop"]["is_complete"] and sections["knowledge"]["is_complete"] and sections["tools"]["present"]:
        return "L2 可执行"
    if sections["knowledge"]["present"]:
        return "L1 可读"
    return "L0 草稿"


def audit(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    domains: list[dict[str, Any]] = []
    for domain, requirements in DOMAIN_REQUIREMENTS.items():
        sections = {
            "sop": path_status(root_path, requirements["sop"]),
            "knowledge": path_status(root_path, requirements["knowledge"]),
            "skill": path_status(root_path, requirements["skill"]),
            "tools": tool_status(root_path, requirements["tools"]),
            "verification": tool_status(root_path, requirements["verification"]),
        }
        missing = [item for section in sections.values() for item in section["missing"]]
        domains.append(
            {
                "domain": domain,
                "display_name": requirements["display_name"],
                "level": level_for_sections(sections),
                "is_complete": not missing,
                "sections": sections,
                "missing": missing,
                "next_steps": ["maintain_examples", "expand_real_anonymized_transcripts"] if not missing else ["fill_missing_artifacts"],
            }
        )

    common_sections = {
        "knowledge_base": path_status(root_path, COMMON_REQUIREMENTS["knowledge_base"]),
        "templates": path_status(root_path, COMMON_REQUIREMENTS["templates"]),
        "shared_tools": tool_status(root_path, COMMON_REQUIREMENTS["shared_tools"]),
        "shared_verification": path_status(root_path, COMMON_REQUIREMENTS["shared_verification"]),
    }
    common_missing = [item for section in common_sections.values() for item in section["missing"]]
    failed_domains = [item["domain"] for item in domains if not item["is_complete"]]
    return {
        "tool": "knowledge_coverage_audit",
        "root": str(root_path),
        "domain_count": len(domains),
        "complete_domain_count": len(domains) - len(failed_domains),
        "failed_domain_count": len(failed_domains),
        "is_valid": not failed_domains and not common_missing,
        "domains": domains,
        "common": {
            "is_complete": not common_missing,
            "sections": common_sections,
            "missing": common_missing,
        },
        "quality_gates": [
            "python3 -m unittest discover -s agent-tools/tests",
            "for f in agent-tools/schemas/*.json; do python3 -m json.tool \"$f\" >/dev/null || exit 1; done",
            "python3 agent-tools/scripts/agent_workflow_router.py --text '帮我做一个塔罗三张牌，看看工作状态'",
            "python3 agent-tools/scripts/agent_route_smoke_runner.py",
            "python3 agent-tools/scripts/agent_runtime_dry_run_runner.py",
            "python3 agent-tools/scripts/agent_runtime_handoff_builder.py --codex-home /tmp/mystic-codex-home-preview",
            "python3 agent-tools/scripts/agent_tool_definition_exporter.py",
            "python3 agent-tools/scripts/agent_tool_definition_validator.py",
            "python3 agent-tools/scripts/agent_tool_registry_builder.py",
            "python3 agent-tools/scripts/agent_tool_registry_validator.py",
            "python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py",
            "python3 agent-tools/scripts/codex_skill_installer.py --codex-home /tmp/mystic-codex-home-preview",
            "python3 agent-tools/scripts/content_review_packet_builder.py",
            "python3 agent-tools/scripts/content_review_feedback_recorder.py --domain tarot --reviewer reviewer --review-date 2026-07-02 --decision approved --approved-scope baseline",
            "python3 agent-tools/scripts/external_evidence_intake_builder.py --codex-home /tmp/mystic-codex-home-preview",
            "python3 agent-tools/scripts/pilot_readiness_report.py --codex-home /tmp/mystic-codex-home-preview",
            "python3 agent-tools/scripts/release_manifest_builder.py --version 0.1.0",
            "python3 agent-tools/scripts/skill_install_readiness_report.py --codex-home /tmp/mystic-codex-home-preview",
            "python3 agent-tools/scripts/sop_traceability_matrix_builder.py",
            "python3 agent-tools/scripts/tool_manifest_builder.py",
            "python3 agent-tools/scripts/skill_replay_runner.py",
            "python3 agent-tools/scripts/skill_transcript_runner.py",
            "README 本地链接检查",
        ],
        "limits": [
            "覆盖度审计只检查关键文件存在，不证明内容质量已经充分。",
            "真实匿名 transcript 仍需要人工复核和评分。",
            "L3 可验证表示首批工具化与回放证据齐全，不等于所有派别和案例已穷尽。",
        ],
        "next_steps": [
            "run_quality_gates",
            "review_dashboard_against_audit",
            "expand_real_anonymized_transcripts",
            "add_domain_specific_variant_cases",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to audit.")
    args = parser.parse_args()
    print(json.dumps(audit(args.root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
