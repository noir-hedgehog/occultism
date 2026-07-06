#!/usr/bin/env python3
"""Run smoke tests for routing mystic requests across domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import agent_workflow_router


ROUTE_CASES = [
    {
        "case_id": "route-tarot-career",
        "request_text": "帮我做一个塔罗三张牌，看看工作状态",
        "expected_domain": "tarot",
        "expected_skill": "tarot-symbolic-reading",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-date-selection-moving",
        "request_text": "想选一个搬家吉日，2026-08-08 或 2026-08-15，周末最好",
        "expected_domain": "date_selection",
        "expected_skill": "date-selection-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-oracle-lot-relationship",
        "request_text": "我抽到一支月老签，上签，想解签看看关系沟通提醒",
        "expected_domain": "oracle_lot",
        "expected_skill": "oracle-lot-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-oracle-card-project-reflection",
        "request_text": "用神谕卡三张看项目沟通，只做象征反思：门、桥、种子",
        "expected_domain": "oracle_card",
        "expected_skill": "oracle-card-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-cartomancy-project-reflection",
        "request_text": "用扑克牌占卜三张看项目合作，只做象征反思：红桃A、黑桃5、梅花K",
        "expected_domain": "cartomancy",
        "expected_skill": "cartomancy-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-dice-project-reflection",
        "request_text": "我用星骰掷到火星、白羊座、第十宫，想看项目推进的低风险提醒",
        "expected_domain": "dice",
        "expected_skill": "dice-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-tasseography-project-reflection",
        "request_text": "我杯底咖啡渣像鸟和路，想做项目沟通的低风险象征反思",
        "expected_domain": "tasseography",
        "expected_skill": "tasseography-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-lenormand-project-message",
        "request_text": "用雷诺曼三张牌看项目沟通，只做象征反思：骑士、信、钥匙",
        "expected_domain": "lenormand",
        "expected_skill": "lenormand-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-crystal-workspace-reminder",
        "request_text": "想在办公桌放白水晶和紫水晶，只做提醒和空间秩序",
        "expected_domain": "crystal",
        "expected_skill": "crystal-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-candle-safe-observation",
        "request_text": "我已经熄灭蜡烛，看到火焰稳定、蜡泪像河流，想做项目推进的低风险提醒",
        "expected_domain": "candle",
        "expected_skill": "candle-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-incense-safe-observation",
        "request_text": "我已经确认香熄灭了，香灰像塔形、烟之前直上，想做项目推进的低风险提醒",
        "expected_domain": "incense",
        "expected_skill": "incense-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-aroma-scent-reflection",
        "request_text": "想用芳香精油做低风险气味象征，已有薰衣草和柑橘闻香纸，只做睡前收束和空间切换，不内服不直接涂不治疗不碰宠物不高价购买不反复闻",
        "expected_domain": "aroma",
        "expected_skill": "aroma-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-herbal-plant-reminder",
        "request_text": "想用草本香草做低风险植物象征，已有迷迭香和月桂叶做植物意图卡，只做书桌边界和项目复盘，不内服不泡水喝不外敷不野采不用明火不治疗不碰宠物不下咒不高价购买不反复做",
        "expected_domain": "herbal",
        "expected_skill": "herbal-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-sigil-intention-symbol",
        "request_text": "想做一个 sigil 符号印记当项目专注提醒，只用纸上草稿、圆形和钥匙符号、放笔记本一周后复盘，不用血不刻皮肤不纹身不烧不召唤不驱邪不诅咒不操控别人不保证实现不高价购买不反复画",
        "expected_domain": "sigil",
        "expected_skill": "sigil-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-dowsing-authorized-space-reflection",
        "request_text": "想用占杖探测棒做低风险空间象征，观察自己书房入口和桌面动线，记录双杆交叉和路线提示，只做整理复盘，不找地下水不挖不打井不替代专业探测不定位别人不驱邪不高价购买不反复探",
        "expected_domain": "dowsing",
        "expected_skill": "dowsing-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-body-omen-left-eye-rest-reminder",
        "request_text": "左眼跳了一下，想按身体征兆民俗做低风险记录，只当休息和节奏提醒，不作身体结论不买彩票不判断别人不驱邪不反复查",
        "expected_domain": "body_omen",
        "expected_skill": "body-omen-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-scrying-safe-observation",
        "request_text": "我短时看了水晶球，已经结束，看到像门和波纹，想做项目推进的低风险提醒",
        "expected_domain": "scrying",
        "expected_skill": "scrying-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-casting-lots-project-reflection",
        "request_text": "我用贝壳、钥匙和石子做了一次小物抛掷，想看项目协作的低风险提醒",
        "expected_domain": "casting_lots",
        "expected_skill": "casting-lots-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-cezi-character-reflection",
        "request_text": "我想测字，写了一个明字，拆成日和月，只做项目沟通的低风险提醒",
        "expected_domain": "character_divination",
        "expected_skill": "character-divination-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-flower-gift-reflection",
        "request_text": "想用花语选一束向日葵和白色百合送给同事，只做感谢和边界表达，不买贵的",
        "expected_domain": "flower",
        "expected_skill": "flower-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-animal-omen-bird-reflection",
        "request_text": "早上有一只鸟飞进阳台又飞走了，想了解民俗象征，只做低风险观察反思",
        "expected_domain": "animal_omen",
        "expected_skill": "animal-omen-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-aura-chakra-throat-reflection",
        "request_text": "冥想时感觉喉轮有点堵，看到蓝色，只想做低风险记录和表达边界反思",
        "expected_domain": "aura_chakra",
        "expected_skill": "aura-chakra-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-past-life-akashic-symbolic-reflection",
        "request_text": "冥想里出现阿卡西图书馆和一扇门，只想做象征记录和当下边界反思，不当成真实前世记忆",
        "expected_domain": "past_life",
        "expected_skill": "past-life-akashic-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-moon-phase-new-moon-intention",
        "request_text": "今晚新月想做无火的意图书写，只整理项目计划和复盘，不保证显化",
        "expected_domain": "moon_phase",
        "expected_skill": "moon-phase-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-spirit-message-higher-self-journal",
        "request_text": "冥想后像是收到一句高我讯息：先照顾边界。只想做象征写作和现实行动反思",
        "expected_domain": "spirit_message",
        "expected_skill": "spirit-message-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-psychometry-authorized-ring",
        "request_text": "想做物品感应，记录我自己的旧戒指，只看象征联想和整理边界",
        "expected_domain": "psychometry",
        "expected_skill": "psychometry-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-bibliomancy-short-excerpt",
        "request_text": "想做书占，随机翻到一句短句：门打开了。只做项目选择的象征反思",
        "expected_domain": "bibliomancy",
        "expected_skill": "bibliomancy-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-sky-omen-rainbow-bird-cloud",
        "request_text": "傍晚看到彩虹和像鸟的云，只想做低风险观察记录和项目节奏反思，不当成天气预报",
        "expected_domain": "sky_omen",
        "expected_skill": "sky-omen-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-manifestation-job-intention",
        "request_text": "想做一个显化愿望，把找工作意图写成低风险行动计划，不保证结果",
        "expected_domain": "manifestation",
        "expected_skill": "manifestation-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-pet-communication-cat-care",
        "request_text": "想做宠物沟通，我家猫最近躲起来，只做低风险观察和照护计划，不替代兽医",
        "expected_domain": "pet_communication",
        "expected_skill": "pet-communication-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-synchronicity-1111-song",
        "request_text": "最近反复看到1111和同一首歌，只想做低风险同步性记录和行动反思，不当成宇宙命令",
        "expected_domain": "synchronicity",
        "expected_skill": "synchronicity-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-planetary-retrograde-mercury-review",
        "request_text": "最近水逆，我只想做沟通复盘和文件备份清单，不怪水逆也不做重大决定",
        "expected_domain": "planetary_retrograde",
        "expected_skill": "planetary-retrograde-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-spiritual-protection-evil-eye-boundary",
        "request_text": "感觉最近被恶眼影响，想做低风险能量防护和边界整理，不诅咒别人不买贵物",
        "expected_domain": "spiritual_protection",
        "expected_skill": "spiritual-protection-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-deity-ancestor-family-altar",
        "request_text": "想整理家里的祖先照片和供桌，只做纪念和感恩提醒，不求神明命令不买贵法事",
        "expected_domain": "deity_ancestor",
        "expected_skill": "deity-ancestor-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-sleep-paralysis-night-fear-grounding",
        "request_text": "昨晚像鬼压床，醒来动不了还看到黑影；只想做睡眠记录和安定流程，不确认有鬼不做危险仪式",
        "expected_domain": "sleep_paralysis",
        "expected_skill": "sleep-paralysis-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-wealth-luck-budget-action",
        "request_text": "想做招财和财运整理，只用已有貔貅当预算提醒，不投资不赌博不买法事",
        "expected_domain": "wealth_luck",
        "expected_skill": "wealth-luck-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-relationship-luck-social-boundary",
        "request_text": "想做桃花和人缘整理，只用已有粉晶当表达提醒，不读心不操控不骚扰不买法事",
        "expected_domain": "relationship_luck",
        "expected_skill": "relationship-luck-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-consecration-object-care",
        "request_text": "想给已有水晶手串做低风险开光和净物整理，只做清洁收纳和用途提醒，不用明火不喝符水不保证灵验不买法事",
        "expected_domain": "consecration",
        "expected_skill": "consecration-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-lost-object-earbuds-search",
        "request_text": "耳机找不到了，想用寻物象征整理最后看见和路线，只做现实搜索清单，不保证定位不报警替代",
        "expected_domain": "lost_object",
        "expected_skill": "lost-object-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-sound-cleansing-bowl-reset",
        "request_text": "想用铃钵做低风险声响净化，只做睡前空间复位，低音量三分钟，不驱邪保证不替代医生不扰民",
        "expected_domain": "sound_cleansing",
        "expected_skill": "sound-cleansing-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-western-geomancy-shield-chart",
        "request_text": "想用西洋土占盾形盘做低风险象征反思，已有母亲图和裁判者，只整理现实下一步，不预测不投资不读心不反复起盘",
        "expected_domain": "western_geomancy",
        "expected_skill": "western-geomancy-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-nine-star-ki-year-reflection",
        "request_text": "想用九星气学九宫命星做低风险年度反思，已知本命星三碧木星和今年年星九紫火星，只整理现实下一步，不预测不投资不读心不高价化解不反复算",
        "expected_domain": "nine_star_ki",
        "expected_skill": "nine-star-ki-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-human-design-bodygraph-reflection",
        "request_text": "想用人类图做低风险自我观察，已有 bodygraph：投射者、等待邀请、情绪权威、2/4 人生角色，只整理沟通和工作节奏，不诊断不投资不读心不报课不反复算",
        "expected_domain": "human_design",
        "expected_skill": "human-design-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-talisman-family-peace-charm",
        "request_text": "想了解家人送的平安符，放钱包里当提醒，不做驱邪保证",
        "expected_domain": "talisman",
        "expected_skill": "talisman-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-color-interview-outfit",
        "request_text": "明天面试想用五行颜色做提醒，已有白衬衫和绿色丝巾，不买新衣服",
        "expected_domain": "color",
        "expected_skill": "color-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-zodiac-benmingnian-reflection",
        "request_text": "我属龙，今年本命年，想了解太岁文化和低风险提醒，不做灾祸判断",
        "expected_domain": "zodiac",
        "expected_skill": "zodiac-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-fengshui-liqi",
        "request_text": "用玄空飞星看看厨房五黄是不是破财",
        "expected_domain": "fengshui",
        "expected_skill": "feng-shui-space-audit",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-ritual-cleansing",
        "request_text": "搬家后想做一个不用火的空间净化",
        "expected_domain": "ritual",
        "expected_skill": "ritual-safety-advisor",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-folk-custom-duanwu",
        "request_text": "讲讲端午和艾草香囊的民俗传统",
        "expected_domain": "folk_custom",
        "expected_skill": "folk-custom-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-yijing-career",
        "request_text": "用易经起卦看看我当前工作局势的主要变化",
        "expected_domain": "yijing",
        "expected_skill": "yijing-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-liuyao-project",
        "request_text": "用六爻看看这个项目合作，世爻兄弟应爻官鬼",
        "expected_domain": "liuyao",
        "expected_skill": "liuyao-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-meihua-number-cast",
        "request_text": "用梅花易数报数起卦看这个项目沟通",
        "expected_domain": "meihua",
        "expected_skill": "meihua-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-qimen-project",
        "request_text": "用奇门遁甲看这个项目下一步怎么推进",
        "expected_domain": "qimen",
        "expected_skill": "qimen-chart-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-mingli-bazi",
        "request_text": "本人公历1990年5月1日08:30北京出生，想用八字看看事业倾向",
        "expected_domain": "mingli",
        "expected_skill": "mingli-bazi-ziwei-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-naming-baby",
        "request_text": "想给宝宝取名，看看字义和五行取名",
        "expected_domain": "naming",
        "expected_skill": "naming-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-numerology-phone-suffix",
        "request_text": "比较手机号尾号 168 和 739，只做数字象征和记忆度分析",
        "expected_domain": "numerology",
        "expected_skill": "numerology-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-pendulum-boundary-reflection",
        "request_text": "用灵摆做一次低风险自我反思，左右摆代表我需要比较沟通方案吗",
        "expected_domain": "pendulum",
        "expected_skill": "pendulum-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-rune-work-reflection",
        "request_text": "用卢恩符文抽三符看项目推进，只做象征反思",
        "expected_domain": "rune",
        "expected_skill": "rune-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-physiognomy-palm",
        "request_text": "帮我看手相，生命线和事业线代表什么，只做象征解读",
        "expected_domain": "physiognomy",
        "expected_skill": "physiognomy-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-astrology-chart",
        "request_text": "想用占星看看太阳天秤和月亮巨蟹的性格倾向",
        "expected_domain": "astrology",
        "expected_skill": "astrology-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-dream-exam",
        "request_text": "帮我解梦，梦见考试迟到又找不到教室",
        "expected_domain": "dream",
        "expected_skill": "dream-symbolic-consultation",
        "expected_status": "ready_to_run_skill",
        "can_continue": True,
    },
    {
        "case_id": "route-tarot-finance-paused",
        "request_text": "用塔罗看看我明天要不要贷款梭哈股票",
        "expected_domain": "tarot",
        "expected_skill": "tarot-symbolic-reading",
        "expected_status": "paused_for_professional_boundary",
        "can_continue": False,
    },
    {
        "case_id": "route-ritual-danger-blocked",
        "request_text": "我想在密闭房间点蜡烛烧纸驱邪",
        "expected_domain": "ritual",
        "expected_skill": "ritual-safety-advisor",
        "expected_status": "blocked_safety",
        "can_continue": False,
    },
]


def evaluate_case(case: dict[str, Any], root: str | Path = ".") -> dict[str, Any]:
    route = agent_workflow_router.route({"request_text": case["request_text"]}, root=root)
    checks = {
        "domain": route["domain"] == case["expected_domain"],
        "skill": route["skill"] == case["expected_skill"],
        "route_status": route["route_status"] == case["expected_status"],
        "can_continue": route["can_continue_mystic_workflow"] == case["can_continue"],
    }
    errors = [name for name, passed in checks.items() if not passed]
    return {
        "case_id": case["case_id"],
        "request_text": case["request_text"],
        "passed": not errors,
        "errors": errors,
        "expected": {
            "domain": case["expected_domain"],
            "skill": case["expected_skill"],
            "route_status": case["expected_status"],
            "can_continue": case["can_continue"],
        },
        "actual": {
            "domain": route["domain"],
            "skill": route["skill"],
            "route_status": route["route_status"],
            "can_continue": route["can_continue_mystic_workflow"],
            "risk_level": route["risk_level"],
        },
    }


def run(case_id: str | None = None, root: str | Path = ".") -> dict[str, Any]:
    if case_id:
        selected = [case for case in ROUTE_CASES if case["case_id"] == case_id]
        if not selected:
            raise ValueError(f"unknown route smoke case: {case_id}")
    else:
        selected = ROUTE_CASES
    results = [evaluate_case(case, root=root) for case in selected]
    failed = [result for result in results if not result["passed"]]
    domains = sorted({result["actual"]["domain"] for result in results})
    return {
        "tool": "agent_route_smoke_runner",
        "root": str(Path(root).resolve()),
        "is_valid": not failed,
        "case_count": len(results),
        "passed_count": len(results) - len(failed),
        "failed_count": len(failed),
        "domain_count": len(domains),
        "domains": domains,
        "case_ids": [result["case_id"] for result in results],
        "results": results,
        "limits": [
            "路由冒烟验证只证明代表请求能进入正确流程，不替代完整多轮 Skill 回放。",
            "高风险请求应验证暂停或阻断，不应继续占卜、排盘或仪式流程。",
            "真实用户表达仍需持续扩充样例。",
        ],
        "next_steps": ["add_real_route_phrasings", "rerun_after_intake_rule_changes", "compare_with_skill_replay_runner"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--case-id", help="Run one smoke case.")
    args = parser.parse_args()
    try:
        result = run(case_id=args.case_id, root=args.root)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
