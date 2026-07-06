#!/usr/bin/env python3
"""Deterministic intake and safety triage for mystic-consultation requests."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class KeywordRule:
    label: str
    keywords: tuple[str, ...]


DOMAIN_RULES = {
    "tarot": ("塔罗", "tarot", "牌阵", "抽牌", "大阿尔卡那", "小阿尔卡那"),
    "oracle_lot": ("求签", "解签", "签文", "签诗", "签号", "观音签", "月老签", "灵签", "寺庙签", "抽签", "模拟抽签"),
    "oracle_card": ("神谕卡", "神谕牌", "oracle card", "oracle cards", "oracle deck", "天使卡", "动物灵性卡", "能量卡"),
    "cartomancy": ("扑克牌占卜", "扑克牌算命", "纸牌占卜", "扑克牌解读", "cartomancy", "playing card reading"),
    "dice": ("星骰", "占星骰", "占卜骰", "骰子占卜", "astrodice", "astro dice", "divination dice"),
    "tasseography": ("茶叶占卜", "茶渣占卜", "咖啡渣占卜", "杯底占卜", "茶占", "咖啡占卜", "咖啡渣", "茶叶形状", "茶渣", "杯底", "杯壁", "tasseography", "tea leaf reading", "coffee grounds"),
    "lenormand": ("雷诺曼", "雷诺曼卡", "lenormand", "36张", "36 张", "骑士牌", "九宫格", "雷诺曼九宫"),
    "crystal": ("水晶", "能量石", "晶石", "crystal", "crystals", "quartz", "amethyst", "rose quartz", "手串", "吊坠", "黑曜石", "粉晶", "紫水晶"),
    "talisman": ("护符", "符箓", "符咒", "灵符", "平安符", "红绳", "香囊", "amulet", "talisman", "charm"),
    "candle": ("蜡烛占卜", "蜡泪占卜", "火焰占卜", "烛火占卜", "蜡烛火焰", "蜡泪", "烛泪", "candle reading", "ceromancy", "candle wax reading"),
    "incense": ("香火占卜", "香灰占卜", "看香", "香谱", "香灰", "香烟形状", "香火", "烟形", "incense reading", "incense ash reading", "smoke reading"),
    "aroma": ("芳香", "香薰", "精油", "香氛", "气味", "嗅觉", "扩香", "闻香纸", "aromatherapy", "essential oil", "scent", "diffuser"),
    "herbal": ("草本", "香草", "草药", "药草", "植物魔法", "绿巫", "草本包", "香草包", "草药袋", "herbal", "herb magic", "green witchcraft", "herbal bundle"),
    "sigil": ("sigil", "sigils", "符号印记", "印记魔法", "魔法印记", "个人印记", "意图符号", "愿望符号", "魔法阵", "符号阵", "seal magic", "magical seal", "magic circle", "symbol circle"),
    "dowsing": ("占杖", "寻水杖", "探测棒", "探测杆", "探矿杖", "地图探测", "dowsing", "dowsing rod", "dowsing rods", "divining rod", "l-rods", "radiesthesia", "map dowsing"),
    "body_omen": ("眼跳", "左眼跳", "右眼跳", "耳鸣", "耳热", "打喷嚏", "喷嚏", "脸热", "手心痒", "身体征兆", "身体预兆", "肉跳", "body omen", "eye twitch", "ear ringing"),
    "scrying": ("水晶球占卜", "镜占", "黑镜占卜", "水占", "凝视占卜", "水晶球", "黑镜", "镜面凝视", "水面凝视", "scrying", "crystal ball reading", "mirror scrying", "water scrying"),
    "casting_lots": ("骨占", "贝壳占卜", "石子占卜", "符物占卜", "小物占卜", "小物抛掷", "符物抛掷", "抛掷占卜", "撒骨", "casting lots", "charm casting", "bone casting", "shell divination"),
    "western_geomancy": ("西洋土占", "盾形占", "盾盘", "土占盘", "western geomancy", "shield chart", "geomantic figure", "geomantic chart"),
    "nine_star_ki": ("九星气学", "九宫命星", "本命星", "月命星", "年命星", "九星命理", "九星流年", "九星方位", "nine star ki", "nine star astrology"),
    "human_design": ("人类图", "human design", "bodygraph", "类型", "人生角色", "内在权威", "策略", "荐骨", "投射者", "显示者", "生产者", "反映者", "manifestor", "generator", "projector", "reflector"),
    "character_divination": ("测字", "拆字", "字占", "字测", "测一个字", "拆一个字", "character divination", "chinese character divination"),
    "flower": ("花语", "花占", "花卜", "花签", "花牌", "植物象征", "送花", "花束", "flower language", "floriography", "flower divination"),
    "animal_omen": ("动物征兆", "动物预兆", "鸟兽虫鱼", "鸟飞进", "飞进阳台", "鸟进屋", "鸟撞窗", "乌鸦叫", "猫头鹰叫", "蛇进屋", "蜘蛛", "蝴蝶", "飞蛾", "animal omen", "bird omen", "insect omen"),
    "aura_chakra": ("气场", "气场颜色", "脉轮", "七轮", "海底轮", "根轮", "脐轮", "太阳轮", "太阳神经丛", "心轮", "喉轮", "眉心轮", "第三眼", "顶轮", "能量场", "能量感受", "灵气", "reiki", "aura", "chakra", "energy field"),
    "past_life": ("前世", "前生", "累世", "宿世", "阿卡西", "阿卡莎", "akashic", "past life", "soul contract", "灵魂契约", "灵魂课题", "灵魂伴侣", "业力关系", "业力", "因果课题"),
    "moon_phase": ("月相", "月亮周期", "新月", "满月", "上弦月", "下弦月", "月食", "蓝月", "超级月亮", "月亮仪式", "新月许愿", "满月释放", "moon phase", "new moon", "full moon", "lunar cycle"),
    "spirit_message": ("通灵", "灵媒", "灵讯", "高我", "高我讯息", "守护灵", "指导灵", "灵性导师", "天使讯息", "祖先讯息", "自动书写", "channeling", "spirit guide", "higher self", "automatic writing", "angel message"),
    "psychometry": ("物品感应", "触物占卜", "物件能量", "旧物能量", "首饰能量", "遗物能量", "读物品", "读这个物品", "psychometry", "object reading", "old object energy", "jewelry reading"),
    "bibliomancy": ("书占", "书籍占卜", "随机翻书", "翻书占卜", "书页占卜", "抽一句书", "页码占卜", "bibliomancy", "book divination", "random book oracle"),
    "sky_omen": ("天象征兆", "云占", "看云", "云形", "彩虹", "彩虹征兆", "日晕", "月晕", "雷电征兆", "风雨预兆", "霞光", "晚霞", "像鸟的云", "鸟形云", "sky omen", "cloud omen", "nephomancy", "weather omen"),
    "manifestation": ("祈愿", "许愿", "愿望仪式", "显化", "心愿", "愿望清单", "意图设定", "manifestation", "manifesting", "manifest", "intention setting", "wish ritual"),
    "pet_communication": ("宠物沟通", "动物沟通", "宠物灵性", "动物灵性", "亡宠", "宠物讯息", "pet communication", "animal communication", "animal communicator", "animal spirit message"),
    "synchronicity": ("同步性", "天使数字", "重复数字", "重复征兆", "宇宙信号", "宇宙讯号", "反复看到", "反复出现", "1111", "11:11", "synchronicity", "angel number", "angel numbers", "repeating number", "repeating signs"),
    "planetary_retrograde": ("水逆", "行星逆行", "星象天气", "星象影响", "逆行周期", "mercury retrograde", "retrograde", "astrology weather"),
    "spiritual_protection": ("恶眼", "evil eye", "能量防护", "灵性防护", "防护罩", "保护罩", "防小人", "负能量", "能量断联", "切断能量", "cord cutting", "energy protection", "energy cord"),
    "deity_ancestor": ("神明", "祖先", "祖灵", "供奉", "供桌", "神台", "祭拜", "祭祖", "拜神", "拜拜", "上供", "供品", "还愿", "酬神", "谢神", "altar", "offering", "ancestor veneration", "deity prayer", "vow return"),
    "sleep_paralysis": ("鬼压床", "压床", "睡眠瘫痪", "睡瘫", "梦魇", "梦魔", "夜惊", "半夜惊醒", "床边有人", "醒来动不了", "sleep paralysis", "night terror", "nightmare spirit"),
    "wealth_luck": ("招财", "财运", "求财", "旺财", "开财库", "补财库", "财库", "财神", "貔貅", "金蟾", "聚宝盆", "prosperity", "wealth luck", "abundance"),
    "relationship_luck": ("桃花", "姻缘", "人缘", "爱情运", "恋爱运", "旺桃花", "招桃花", "红鸾", "天喜", "月老", "红线", "红绳", "粉晶", "peach blossom luck", "romance luck"),
    "consecration": ("开光", "加持", "净物", "净化物件", "净化水晶", "净化手串", "过香火", "祝福物件", "consecration", "blessing", "cleanse object"),
    "lost_object": ("失物", "寻物", "找东西", "丢了", "不见了", "找不到", "遗失", "东西在哪", "可能放哪", "lost object", "missing item"),
    "sound_cleansing": ("声响净化", "声音净化", "铃铛净化", "铃钵", "颂钵", "音叉", "拍手净化", "诵念", "念咒", "sound cleansing", "singing bowl", "mantra", "chanting"),
    "color": ("五行颜色", "开运色", "幸运色", "颜色", "配色", "穿搭", "色彩", "lucky color", "color symbolism"),
    "date_selection": ("择日", "黄历", "老黄历", "吉日", "良辰", "宜忌", "黄道吉日", "黑道日", "冲生肖", "搬家吉日", "开业吉日", "结婚吉日", "领证日", "开工日", "出行日"),
    "zodiac": ("生肖", "属相", "十二生肖", "本命年", "太岁", "犯太岁", "冲太岁", "三合", "六合", "六冲", "相冲", "tai sui"),
    "feng_shui": ("风水", "阳宅", "阴宅", "户型", "卧室", "办公桌", "床位", "明堂", "煞", "玄空", "飞星", "八宅", "罗盘", "坐向", "五黄", "二黑"),
    "liuyao": ("六爻", "六亲", "六神", "世爻", "应爻", "用神", "官鬼", "妻财", "青龙", "白虎"),
    "meihua": ("梅花易数", "梅花占", "报数起卦", "体卦", "用卦", "互卦", "变卦", "外应", "体用"),
    "yijing": ("易经", "周易", "起卦", "卦", "爻"),
    "qimen": ("奇门", "遁甲", "九宫", "值符", "值使", "用神"),
    "mingli": ("八字", "紫微", "斗数", "命理", "四柱", "生辰", "出生时间", "命盘", "大运", "流年"),
    "naming": ("姓名学", "取名", "起名", "改名", "宝宝名", "小名", "艺名", "笔名", "品牌名", "店名", "商号", "品牌比较", "品牌评分", "五行取名", "谐音避讳", "生肖避讳"),
    "numerology": ("数字能量", "数字象征", "数字占卜", "生命灵数", "灵数", "幸运数字", "手机号", "尾号", "车牌号", "门牌号", "号码比较"),
    "pendulum": ("灵摆", "摆锤", "pendulum", "顺时针", "逆时针", "左右摆", "前后摆", "灵摆校准", "摆动"),
    "rune": ("卢恩", "符文", "rune", "runes", "futhark", "Elder Futhark", "单符", "三符", "抽符文"),
    "physiognomy": ("手相", "掌纹", "掌丘", "生命线", "事业线", "感情线", "智慧线", "面相", "相术", "五官", "眉眼", "额头", "鼻相", "痣相"),
    "astrology": ("占星", "星盘", "星座", "太阳星座", "月亮星座", "上升星座", "上升", "相位", "宫位", "合盘", "natal", "birth chart", "zodiac", "astrology"),
    "dream": ("解梦", "梦见", "梦到", "做梦", "噩梦", "梦境", "梦里", "掉牙", "被追", "坠落", "梦见蛇", "梦见水", "梦见死亡"),
    "ritual_safety": ("驱邪", "净化", "下咒", "诅咒", "附身", "鬼", "邪", "护身", "仪式"),
    "folk_custom": ("民俗", "禁忌", "节气", "节令", "祭祀", "习俗", "传统", "春节", "清明", "端午", "中元", "中秋", "冬至", "筷子插饭", "夜里吹口哨", "正月剪发"),
}

INTENT_RULES = {
    "crisis_help": ("自杀", "自残", "伤害自己", "伤害别人", "活不下去", "被威胁", "家暴", "跟踪"),
    "talisman_reflection": ("护符", "符箓", "符咒", "灵符", "平安符", "红绳", "香囊", "amulet", "talisman", "charm"),
    "ritual_help": ("仪式", "驱邪", "净化", "下咒", "诅咒", "护身"),
    "oracle_lot_interpretation": ("求签", "解签", "签文", "签诗", "签号", "观音签", "月老签", "灵签", "抽签"),
    "oracle_card_reflection": ("神谕卡", "神谕牌", "oracle card", "oracle cards", "天使卡", "能量卡"),
    "cartomancy_reflection": ("扑克牌占卜", "扑克牌算命", "纸牌占卜", "扑克牌解读", "cartomancy", "playing card reading"),
    "dice_reflection": ("星骰", "占星骰", "占卜骰", "骰子占卜", "astrodice", "astro dice", "divination dice"),
    "tasseography_reflection": ("茶叶占卜", "茶渣占卜", "咖啡渣占卜", "杯底占卜", "茶占", "咖啡占卜", "咖啡渣", "茶叶形状", "茶渣", "杯底", "杯壁", "tasseography", "tea leaf reading", "coffee grounds"),
    "lenormand_reflection": ("雷诺曼", "雷诺曼卡", "lenormand", "骑士牌", "九宫格"),
    "crystal_reflection": ("水晶", "能量石", "晶石", "crystal", "quartz", "amethyst", "粉晶", "紫水晶", "黑曜石"),
    "candle_reflection": ("蜡烛占卜", "蜡泪占卜", "火焰占卜", "烛火占卜", "蜡烛火焰", "蜡泪", "烛泪", "candle reading", "ceromancy", "candle wax reading"),
    "incense_reflection": ("香火占卜", "香灰占卜", "看香", "香谱", "香灰", "香烟形状", "香火", "烟形", "incense reading", "incense ash reading", "smoke reading"),
    "aroma_reflection": ("芳香", "香薰", "精油", "香氛", "气味", "嗅觉", "扩香", "闻香纸", "aromatherapy", "essential oil", "scent", "diffuser"),
    "herbal_reflection": ("草本", "香草", "草药", "药草", "植物魔法", "绿巫", "草本包", "香草包", "草药袋", "herbal", "herb magic", "green witchcraft", "herbal bundle"),
    "sigil_reflection": ("sigil", "sigils", "符号印记", "印记魔法", "魔法印记", "个人印记", "意图符号", "愿望符号", "魔法阵", "符号阵", "seal magic", "magical seal", "magic circle", "symbol circle"),
    "dowsing_reflection": ("占杖", "寻水杖", "探测棒", "探测杆", "探矿杖", "地图探测", "dowsing", "dowsing rod", "dowsing rods", "divining rod", "l-rods", "radiesthesia", "map dowsing"),
    "body_omen_reflection": ("眼跳", "左眼跳", "右眼跳", "耳鸣", "耳热", "打喷嚏", "喷嚏", "脸热", "手心痒", "身体征兆", "身体预兆", "肉跳", "body omen", "eye twitch", "ear ringing"),
    "scrying_reflection": ("水晶球占卜", "镜占", "黑镜占卜", "水占", "凝视占卜", "水晶球", "黑镜", "镜面凝视", "水面凝视", "scrying", "crystal ball reading", "mirror scrying", "water scrying"),
    "casting_lots_reflection": ("骨占", "贝壳占卜", "石子占卜", "符物占卜", "小物占卜", "小物抛掷", "符物抛掷", "抛掷占卜", "撒骨", "casting lots", "charm casting", "bone casting", "shell divination"),
    "western_geomancy_reflection": ("西洋土占", "盾形占", "盾盘", "土占盘", "western geomancy", "shield chart", "geomantic figure", "geomantic chart"),
    "nine_star_ki_reflection": ("九星气学", "九宫命星", "本命星", "月命星", "年命星", "九星命理", "九星流年", "九星方位", "nine star ki", "nine star astrology"),
    "human_design_reflection": ("人类图", "human design", "bodygraph", "类型", "人生角色", "内在权威", "策略", "荐骨", "投射者", "显示者", "生产者", "反映者", "manifestor", "generator", "projector", "reflector"),
    "character_divination_reflection": ("测字", "拆字", "字占", "字测", "测一个字", "拆一个字", "character divination", "chinese character divination"),
    "flower_reflection": ("花语", "花占", "花卜", "花签", "花牌", "植物象征", "送花", "花束", "flower language", "floriography", "flower divination"),
    "animal_omen_reflection": ("动物征兆", "动物预兆", "鸟兽虫鱼", "鸟飞进", "飞进阳台", "鸟进屋", "鸟撞窗", "乌鸦叫", "猫头鹰叫", "蛇进屋", "蜘蛛", "蝴蝶", "飞蛾", "animal omen", "bird omen", "insect omen"),
    "aura_chakra_reflection": ("气场", "气场颜色", "脉轮", "七轮", "海底轮", "根轮", "脐轮", "太阳轮", "太阳神经丛", "心轮", "喉轮", "眉心轮", "第三眼", "顶轮", "能量场", "能量感受", "灵气", "reiki", "aura", "chakra", "energy field"),
    "past_life_reflection": ("前世", "前生", "累世", "宿世", "阿卡西", "阿卡莎", "akashic", "past life", "soul contract", "灵魂契约", "灵魂课题", "灵魂伴侣", "业力关系", "业力", "因果课题"),
    "moon_phase_reflection": ("月相", "月亮周期", "新月", "满月", "上弦月", "下弦月", "月食", "蓝月", "超级月亮", "月亮仪式", "新月许愿", "满月释放", "moon phase", "new moon", "full moon", "lunar cycle"),
    "spirit_message_reflection": ("通灵", "灵媒", "灵讯", "高我", "高我讯息", "守护灵", "指导灵", "灵性导师", "天使讯息", "祖先讯息", "自动书写", "channeling", "spirit guide", "higher self", "automatic writing", "angel message"),
    "psychometry_reflection": ("物品感应", "触物占卜", "物件能量", "旧物能量", "首饰能量", "遗物能量", "读物品", "psychometry", "object reading", "old object energy", "jewelry reading"),
    "bibliomancy_reflection": ("书占", "书籍占卜", "随机翻书", "翻书占卜", "书页占卜", "抽一句书", "bibliomancy", "book divination", "random book oracle"),
    "sky_omen_reflection": ("天象征兆", "云占", "看云", "云形", "彩虹", "彩虹征兆", "日晕", "月晕", "雷电征兆", "风雨预兆", "霞光", "晚霞", "像鸟的云", "鸟形云", "sky omen", "cloud omen", "nephomancy", "weather omen"),
    "manifestation_reflection": ("祈愿", "许愿", "愿望仪式", "显化", "心愿", "愿望清单", "意图设定", "manifestation", "manifesting", "manifest", "intention setting", "wish ritual"),
    "pet_communication_reflection": ("宠物沟通", "动物沟通", "宠物灵性", "动物灵性", "亡宠", "宠物讯息", "pet communication", "animal communication", "animal communicator", "animal spirit message"),
    "synchronicity_reflection": ("同步性", "天使数字", "重复数字", "重复征兆", "宇宙信号", "宇宙讯号", "反复看到", "反复出现", "1111", "11:11", "synchronicity", "angel number", "angel numbers", "repeating number", "repeating signs"),
    "planetary_retrograde_reflection": ("水逆", "行星逆行", "星象天气", "星象影响", "逆行周期", "mercury retrograde", "retrograde", "astrology weather"),
    "spiritual_protection_reflection": ("恶眼", "evil eye", "能量防护", "灵性防护", "防护罩", "保护罩", "防小人", "负能量", "能量断联", "切断能量", "cord cutting", "energy protection", "energy cord"),
    "deity_ancestor_reflection": ("神明", "祖先", "祖灵", "供奉", "供桌", "神台", "祭拜", "祭祖", "拜神", "拜拜", "上供", "供品", "还愿", "酬神", "谢神", "altar", "offering", "ancestor veneration", "deity prayer", "vow return"),
    "sleep_paralysis_reflection": ("鬼压床", "压床", "睡眠瘫痪", "睡瘫", "梦魇", "梦魔", "夜惊", "半夜惊醒", "床边有人", "醒来动不了", "sleep paralysis", "night terror", "nightmare spirit"),
    "wealth_luck_reflection": ("招财", "财运", "求财", "旺财", "开财库", "补财库", "财库", "财神", "貔貅", "金蟾", "聚宝盆", "prosperity", "wealth luck", "abundance"),
    "relationship_luck_reflection": ("桃花", "姻缘", "人缘", "爱情运", "恋爱运", "旺桃花", "招桃花", "红鸾", "天喜", "月老", "红线", "红绳", "粉晶", "peach blossom luck", "romance luck"),
    "consecration_reflection": ("开光", "加持", "净物", "净化物件", "净化水晶", "净化手串", "过香火", "祝福物件", "consecration", "blessing", "cleanse object"),
    "lost_object_reflection": ("失物", "寻物", "找东西", "丢了", "不见了", "找不到", "遗失", "东西在哪", "可能放哪", "lost object", "missing item"),
    "sound_cleansing_reflection": ("声响净化", "声音净化", "铃铛净化", "铃钵", "颂钵", "音叉", "拍手净化", "诵念", "念咒", "sound cleansing", "singing bowl", "mantra", "chanting"),
    "color_reflection": ("五行颜色", "开运色", "幸运色", "颜色", "配色", "穿搭", "色彩", "lucky color", "color symbolism"),
    "date_selection": ("择日", "黄历", "吉日", "宜忌", "黄道", "搬家吉日", "开业吉日", "结婚吉日", "领证日"),
    "zodiac_reflection": ("生肖", "属相", "十二生肖", "本命年", "太岁", "犯太岁", "冲太岁", "三合", "六合", "六冲", "相冲", "tai sui"),
    "chart_reflection": ("星盘", "星座", "占星", "太阳", "月亮", "上升", "宫位", "相位", "合盘", "natal", "birth chart"),
    "appearance_symbol_reflection": ("手相", "掌纹", "生命线", "事业线", "感情线", "智慧线", "面相", "相术", "鼻相", "痣相"),
    "dream_reflection": ("解梦", "梦见", "梦到", "梦境", "噩梦", "梦里"),
    "space_review": ("房间", "卧室", "办公室", "户型", "床", "桌", "门", "窗", "风水", "玄空", "飞星", "八宅", "罗盘", "坐向", "五黄", "二黑"),
    "name_review": ("取名", "起名", "改名", "名字", "品牌名", "店名", "商号", "品牌比较", "品牌评分"),
    "number_symbol_reflection": ("数字能量", "数字象征", "生命灵数", "幸运数字", "手机号", "尾号", "车牌号", "门牌号", "号码比较"),
    "pendulum_reflection": ("灵摆", "摆锤", "pendulum", "顺时针", "逆时针", "灵摆校准", "摆动"),
    "rune_reflection": ("卢恩", "符文", "rune", "runes", "futhark", "单符", "三符", "抽符文"),
    "cultural_learning": ("是什么", "来源", "历史", "文化", "讲讲", "介绍", "学习"),
    "decision_support": ("选择", "要不要", "适不适合", "方案", "offer", "跳槽", "搬家", "分手"),
    "prediction": ("会不会", "什么时候", "能不能", "是否会", "未来", "预测", "回来", "发财"),
}

RED_RULES = (
    KeywordRule("immediate_self_or_other_harm", ("自杀", "自残", "杀了", "伤害自己", "伤害别人", "活不下去")),
    KeywordRule("violence_or_abuse", ("家暴", "被威胁", "跟踪我", "囚禁", "报警也没用")),
    KeywordRule("dangerous_ritual", ("放血", "割腕", "刀", "血祭", "密闭燃烧", "密闭房间点", "密闭房间烧", "酒精点火", "烧炭")),
)

ORANGE_RULES = (
    KeywordRule("medical_or_pregnancy", ("诊断", "用药", "怀孕", "孕妇", "孕期", "手术", "癌", "病", "药", "医生")),
    KeywordRule("mental_health_crisis", ("幻听", "幻视", "失控", "被附体", "附身", "连续失眠", "睡不着很多天")),
    KeywordRule("legal", ("起诉", "坐牢", "刑事", "律师", "合同", "离婚官司", "移民")),
    KeywordRule("financial", ("股票", "彩票", "赌博", "借贷", "贷款", "投资", "梭哈", "币圈")),
)

YELLOW_RULES = (
    KeywordRule("major_life_decision", ("结婚", "离婚", "分手", "辞职", "跳槽", "搬家", "创业")),
    KeywordRule("relationship_anxiety", ("他会不会回来", "她会不会回来", "复合", "小三", "出轨")),
    KeywordRule("fearful_supernatural_frame", ("是不是有鬼", "是不是被下咒", "是不是中邪", "被诅咒")),
)

SAFE_NEGATED_RISK_PHRASES = (
    "不投资",
    "不赌博",
    "不买彩票",
    "不借贷",
    "不贷款",
    "不做投资",
    "不做赌博",
    "不提供投资",
    "不诊断",
    "不替代医生",
    "不替代医疗",
    "不替代心理咨询",
    "不替代财务",
)


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def remove_safe_negations(text: str) -> str:
    cleaned = text
    for phrase in SAFE_NEGATED_RISK_PHRASES:
        cleaned = cleaned.replace(phrase, "")
    return cleaned


def matching_labels(text: str, rules: Iterable[KeywordRule]) -> list[str]:
    return [rule.label for rule in rules if contains_any(text, rule.keywords)]


def detect_domain(text: str, requested_domain: str | None = None) -> str:
    if requested_domain:
        normalized = requested_domain.strip()
        if normalized in DOMAIN_RULES or normalized == "unknown":
            return normalized
    if contains_any(text, DOMAIN_RULES["consecration"]):
        return "consecration"
    if contains_any(text, DOMAIN_RULES["dream"]):
        return "dream"
    if contains_any(text, DOMAIN_RULES["dowsing"]):
        return "dowsing"
    if contains_any(text, DOMAIN_RULES["body_omen"]):
        return "body_omen"
    if contains_any(text, DOMAIN_RULES["lost_object"]):
        return "lost_object"
    if contains_any(text, DOMAIN_RULES["sound_cleansing"]):
        return "sound_cleansing"
    if contains_any(text, DOMAIN_RULES["relationship_luck"]) and not contains_any(text, DOMAIN_RULES["oracle_lot"]):
        return "relationship_luck"
    if contains_any(text, DOMAIN_RULES["aroma"]):
        return "aroma"
    if contains_any(text, DOMAIN_RULES["herbal"]):
        return "herbal"
    if contains_any(text, DOMAIN_RULES["sigil"]):
        return "sigil"
    if contains_any(text, DOMAIN_RULES["scrying"]):
        return "scrying"
    if contains_any(text, DOMAIN_RULES["psychometry"]):
        return "psychometry"
    if contains_any(text, DOMAIN_RULES["bibliomancy"]):
        return "bibliomancy"
    if contains_any(text, DOMAIN_RULES["sky_omen"]):
        return "sky_omen"
    if contains_any(text, DOMAIN_RULES["casting_lots"]):
        return "casting_lots"
    if contains_any(text, DOMAIN_RULES["western_geomancy"]):
        return "western_geomancy"
    if contains_any(text, DOMAIN_RULES["nine_star_ki"]):
        return "nine_star_ki"
    if contains_any(text, DOMAIN_RULES["human_design"]):
        return "human_design"
    if contains_any(text, DOMAIN_RULES["character_divination"]):
        return "character_divination"
    if contains_any(text, DOMAIN_RULES["flower"]):
        return "flower"
    if contains_any(text, DOMAIN_RULES["animal_omen"]):
        return "animal_omen"
    if contains_any(text, DOMAIN_RULES["aura_chakra"]):
        return "aura_chakra"
    if contains_any(text, DOMAIN_RULES["past_life"]):
        return "past_life"
    if contains_any(text, DOMAIN_RULES["moon_phase"]):
        return "moon_phase"
    if contains_any(text, DOMAIN_RULES["manifestation"]):
        return "manifestation"
    if contains_any(text, DOMAIN_RULES["pet_communication"]):
        return "pet_communication"
    if contains_any(text, DOMAIN_RULES["synchronicity"]):
        return "synchronicity"
    if contains_any(text, DOMAIN_RULES["planetary_retrograde"]):
        return "planetary_retrograde"
    if contains_any(text, DOMAIN_RULES["spiritual_protection"]):
        return "spiritual_protection"
    if contains_any(text, DOMAIN_RULES["deity_ancestor"]):
        return "deity_ancestor"
    if contains_any(text, DOMAIN_RULES["sleep_paralysis"]):
        return "sleep_paralysis"
    if contains_any(text, DOMAIN_RULES["wealth_luck"]):
        return "wealth_luck"
    if contains_any(text, DOMAIN_RULES["spirit_message"]):
        return "spirit_message"
    if contains_any(text, ("民俗", "习俗", "传统", "节气", "节令", "端午", "春节", "清明", "中秋", "冬至")):
        return "folk_custom"
    for domain, keywords in DOMAIN_RULES.items():
        if contains_any(text, keywords):
            return domain
    return "unknown"


def detect_intent(text: str) -> str:
    if contains_any(text, INTENT_RULES["consecration_reflection"]):
        return "consecration_reflection"
    if contains_any(text, INTENT_RULES["dream_reflection"]):
        return "dream_reflection"
    if contains_any(text, INTENT_RULES["dowsing_reflection"]):
        return "dowsing_reflection"
    if contains_any(text, INTENT_RULES["body_omen_reflection"]):
        return "body_omen_reflection"
    if contains_any(text, INTENT_RULES["lost_object_reflection"]):
        return "lost_object_reflection"
    if contains_any(text, INTENT_RULES["sound_cleansing_reflection"]):
        return "sound_cleansing_reflection"
    if contains_any(text, INTENT_RULES["relationship_luck_reflection"]) and not contains_any(text, INTENT_RULES["oracle_lot_interpretation"]):
        return "relationship_luck_reflection"
    if contains_any(text, INTENT_RULES["aroma_reflection"]):
        return "aroma_reflection"
    if contains_any(text, INTENT_RULES["herbal_reflection"]):
        return "herbal_reflection"
    if contains_any(text, INTENT_RULES["sigil_reflection"]):
        return "sigil_reflection"
    if contains_any(text, INTENT_RULES["scrying_reflection"]):
        return "scrying_reflection"
    if contains_any(text, INTENT_RULES["psychometry_reflection"]):
        return "psychometry_reflection"
    if contains_any(text, INTENT_RULES["bibliomancy_reflection"]):
        return "bibliomancy_reflection"
    if contains_any(text, INTENT_RULES["sky_omen_reflection"]):
        return "sky_omen_reflection"
    if contains_any(text, INTENT_RULES["casting_lots_reflection"]):
        return "casting_lots_reflection"
    if contains_any(text, INTENT_RULES["western_geomancy_reflection"]):
        return "western_geomancy_reflection"
    if contains_any(text, INTENT_RULES["nine_star_ki_reflection"]):
        return "nine_star_ki_reflection"
    if contains_any(text, INTENT_RULES["human_design_reflection"]):
        return "human_design_reflection"
    if contains_any(text, INTENT_RULES["character_divination_reflection"]):
        return "character_divination_reflection"
    if contains_any(text, INTENT_RULES["flower_reflection"]):
        return "flower_reflection"
    if contains_any(text, INTENT_RULES["animal_omen_reflection"]):
        return "animal_omen_reflection"
    if contains_any(text, INTENT_RULES["aura_chakra_reflection"]):
        return "aura_chakra_reflection"
    if contains_any(text, INTENT_RULES["past_life_reflection"]):
        return "past_life_reflection"
    if contains_any(text, INTENT_RULES["moon_phase_reflection"]):
        return "moon_phase_reflection"
    if contains_any(text, INTENT_RULES["manifestation_reflection"]):
        return "manifestation_reflection"
    if contains_any(text, INTENT_RULES["pet_communication_reflection"]):
        return "pet_communication_reflection"
    if contains_any(text, INTENT_RULES["synchronicity_reflection"]):
        return "synchronicity_reflection"
    if contains_any(text, INTENT_RULES["planetary_retrograde_reflection"]):
        return "planetary_retrograde_reflection"
    if contains_any(text, INTENT_RULES["spiritual_protection_reflection"]):
        return "spiritual_protection_reflection"
    if contains_any(text, INTENT_RULES["deity_ancestor_reflection"]):
        return "deity_ancestor_reflection"
    if contains_any(text, INTENT_RULES["sleep_paralysis_reflection"]):
        return "sleep_paralysis_reflection"
    if contains_any(text, INTENT_RULES["wealth_luck_reflection"]):
        return "wealth_luck_reflection"
    if contains_any(text, INTENT_RULES["spirit_message_reflection"]):
        return "spirit_message_reflection"
    for intent, keywords in INTENT_RULES.items():
        if contains_any(text, keywords):
            return intent
    return "reflection"


def classify_risk(text: str) -> tuple[str, list[str]]:
    red = matching_labels(text, RED_RULES)
    if red:
        return "red", red
    risk_text = remove_safe_negations(text)
    orange = matching_labels(risk_text, ORANGE_RULES)
    if orange:
        return "orange", orange
    yellow = matching_labels(risk_text, YELLOW_RULES)
    if yellow:
        return "yellow", yellow
    return "green", []


def clarifications_for(domain: str, intent: str, risk_level: str) -> list[str]:
    if risk_level == "red":
        return ["确认用户是否处于即时危险，并优先联系当地紧急服务或可信任的人。"]
    if risk_level == "orange":
        return ["确认是否涉及医疗、法律、财务或精神健康专业问题，并先建议现实世界专业支持。"]

    questions = ["用户希望获得娱乐、反思、文化学习，还是辅助整理决策？"]
    if domain == "tarot":
        questions.append("用户是否已抽牌；若没有，是否希望模拟抽牌？")
    elif domain == "oracle_lot":
        questions.append("签文来源、签号/签等、签文全文、抽签方法和用户的一事一问是什么？")
    elif domain == "oracle_card":
        questions.append("这是神谕卡文化学习、记录已有抽牌，还是低风险象征反思；牌组名称、牌面原文/关键词和图像元素是什么？")
    elif domain == "cartomancy":
        questions.append("这是扑克牌占卜文化学习、记录已有抽牌，还是低风险象征咨询；问题、牌阵、牌面、抽牌来源和次数边界是什么？")
    elif domain == "dice":
        questions.append("这是星骰/占卜骰文化学习、记录已有骰面，还是低风险象征咨询；问题、骰子体系、骰面、掷骰来源和次数边界是什么？")
    elif domain == "tasseography":
        questions.append("这是茶叶/咖啡渣占卜文化学习、记录已有杯底图案，还是低风险象征咨询；问题、媒介、杯底区域、图案来源和观察次数边界是什么？")
    elif domain == "lenormand":
        questions.append("这是雷诺曼文化学习、记录已有抽牌，还是低风险象征反思；问题是否涉及专业替代、第三方隐私、超自然恐惧或反复依赖？")
    elif domain == "crystal":
        questions.append("这是水晶文化学习、记录已有物件，还是低风险象征咨询；水晶名称、使用场景、来源和预算/已有物件说明是什么？")
    elif domain == "candle":
        questions.append("这是蜡烛火焰/蜡泪文化学习、记录已安全结束的观察，还是低风险象征咨询；观察来源、安全状态、火焰/蜡泪/烟雾描述和火源边界是什么？")
    elif domain == "incense":
        questions.append("这是香火/香灰/烟形文化学习、记录已安全结束的观察，还是低风险象征咨询；观察来源、安全状态、香灰/烟形/香头描述和火源/通风边界是什么？")
    elif domain == "aroma":
        questions.append("这是芳香/精油/香薰文化学习、记录已有气味体验，还是低风险气味象征咨询；气味物件、来源、使用方式、空间、时长、通风、安全背景、预算、停止条件和医疗/孕婴宠物过敏/内服涂抹/消防/驱邪恐惧/结果保证/高价购买/反复依赖边界是什么？")
    elif domain == "herbal":
        questions.append("这是草本/香草/植物魔法文化学习、记录已有植物物件，还是低风险草本象征咨询；植物物件、来源、使用方式、容器形式、空间、时长、安全背景、预算、停止条件和医疗/孕婴宠物过敏/内服外敷/野采辨毒/消防烟雾/驱邪恐惧/爱情咒诅咒/结果保证/高价购买/反复依赖边界是什么？")
    elif domain == "sigil":
        questions.append("这是 sigil/符号印记/魔法阵文化学习、记录已有符号，还是低风险个人象征咨询；意图短句、符号元素、来源、媒介、展示位置、时长、安全背景、预算、停止条件和血/身体伤害/纹身永久化/焚烧/召唤驱邪/诅咒操控/结果保证/专业替代/高价购买/反复依赖边界是什么？")
    elif domain == "dowsing":
        questions.append("这是占杖/寻水杖/探测棒文化学习、记录一次授权空间观察，还是低风险路线/空间象征咨询；工具类型、观察目标、空间或地图、动作记录、授权范围、安全背景、现实核查、停止条件和地下管线/开挖打井/水源资源/医疗地气/房产合同/第三方定位/驱邪恐惧/高价购买/反复依赖边界是什么？")
    elif domain == "body_omen":
        questions.append("这是身体征兆民俗文化学习、记录一次本人低风险征兆，还是象征反思；征兆类型、身体位置、时间、持续频率、感受、普通诱因、健康背景、停止条件和医疗红旗/灾祸恐吓/彩票投资/第三方标签/驱邪恐惧/危险试验/反复依赖边界是什么？")
    elif domain == "scrying":
        questions.append("这是水晶球/镜面/水面凝视文化学习、记录短时已结束的观察，还是低风险象征咨询；媒介、观察来源、安全状态、视觉/表面/感受描述和 grounding 边界是什么？")
    elif domain == "casting_lots":
        questions.append("这是骨、贝壳、石子或符物抛掷文化学习、记录已有盘面，还是低风险象征咨询；符物、投掷垫/区域、盘面来源、材料安全和次数边界是什么？")
    elif domain == "western_geomancy":
        questions.append("这是西洋土占/盾形盘文化学习、记录已有盘面，还是低风险象征咨询；起盘来源、生成方式、母亲图、女儿图、侄子图、见证者、裁判者、问题焦点、复盘时间和专业替代/财务赌博/第三方窥探/操控/确定预言/灵异恐惧/反复依赖边界是什么？")
    elif domain == "nine_star_ki":
        questions.append("这是九星气学/九宫命星文化学习、记录已知命星/年星，还是低风险象征咨询；出生年份或已知本命星、月命星、年星、方位焦点、体系来源、节气边界、现实约束、复盘时间和专业替代/财务赌博/关系标签/方位恐吓/高价化解/第三方窥探/操控/确定预言/反复依赖边界是什么？")
    elif domain == "human_design":
        questions.append("这是人类图文化学习、记录已有 bodygraph，还是低风险象征咨询；资料来源、出生资料最小化范围、类型、策略、内在权威、人生角色、中心、通道/闸门、关注主题、复盘时间和出生资料隐私/专业替代/关系标签/职业财务保证/第三方窥探/操控/付费压力/反复依赖边界是什么？")
    elif domain == "character_divination":
        questions.append("这是测字/拆字文化学习、记录已有字例，还是低风险象征咨询；字、来源、部件/结构、用户第一联想和反复测字边界是什么？")
    elif domain == "flower":
        questions.append("这是花语/植物象征文化学习、记录已有花材，还是低风险象征咨询；花材、颜色、场景、对象、预算和过敏/宠物/儿童/香味约束是什么？")
    elif domain == "animal_omen":
        questions.append("这是动物征兆/鸟兽虫鱼文化学习、记录观察，还是低风险象征咨询；动物、行为、地点、时间、频率和咬伤/虫害/野生动物等现实安全背景是什么？")
    elif domain == "aura_chakra":
        questions.append("这是气场/脉轮文化学习、记录身体感受，还是低风险象征咨询；中心、颜色、感受、持续时间、强度、触发场景和身体/心理安全信号是什么？")
    elif domain == "past_life":
        questions.append("这是前世/阿卡西文化学习、梦境/冥想画面记录，还是低风险象征咨询；来源语境、场景、角色、符号、情绪、当下现实锚点和创伤/隐私/付费边界是什么？")
    elif domain == "moon_phase":
        questions.append("这是月相文化学习、周期记录，还是低风险意图/复盘；月相来源、日期备注、主题、意图、现实约束和危险仪式/专业替代/显化保证边界是什么？")
    elif domain == "spirit_message":
        questions.append("这是通灵/高我文化学习、讯息记录，还是低风险象征写作；来源、原句、符号、情绪、现实锚点和命令式声音/幻听幻视/第三方隐私/付费边界是什么？")
    elif domain == "psychometry":
        questions.append("这是物品感应文化学习、获授权物件记录，还是低风险象征反思；物件类型、来源、拥有/同意状态、可见特征、第一联想和失踪犯罪/第三方隐私/真伪归属/付费净化边界是什么？")
    elif domain == "bibliomancy":
        questions.append("这是书占文化学习、一次翻书记录，还是低风险象征反思；书名/来源、抽取方式、页码/位置、用户自提供短句/关键词和专业替代/第三方隐私/经文权威/长段版权文本/反复依赖边界是什么？")
    elif domain == "sky_omen":
        questions.append("这是天象/云形民俗学习、一次天空观察记录，还是低风险象征反思；观察对象、地点时间、天气安全背景、形状颜色、第一联想和灾祸恐吓/天气安全替代/危险暴露/专业替代边界是什么？")
    elif domain == "manifestation":
        questions.append("这是祈愿/显化文化学习、记录一个愿望，还是把意图转成低风险行动计划；愿望主题、意图句、象征物、现实锚点、可控行动、复盘时间、停止条件和结果保证/专业替代/第三方操控/危险仪式边界是什么？")
    elif domain == "pet_communication":
        questions.append("这是宠物行为观察、宠物沟通象征写作，还是亡宠怀念；宠物种类、可见行为、时间背景、健康/兽医边界、照护动作、用户情绪和兽医替代/走失定位/真实讯息/亡宠事实/付费压力边界是什么？")
    elif domain == "synchronicity":
        questions.append("这是同步性/天使数字文化学习、重复征兆记录，还是低风险反思；重复符号、出现频率、场景、情绪、现实锚点、可控行动、停止条件和危险寻找/宇宙命令/专业替代/第三方读心/反复依赖边界是什么？")
    elif domain == "planetary_retrograde":
        questions.append("这是水逆/行星逆行文化学习、星象天气记录，还是低风险复盘计划；逆行主题、关注领域、现实事项、情绪、现实限制、可控行动、复盘时间、停止查询条件和专业替代/宿命归因/读心操控/高价转运/恐慌依赖边界是什么？")
    elif domain == "spiritual_protection":
        questions.append("这是恶眼/能量防护文化学习、边界整理、提醒物使用，还是低风险断联反思；触发场景、身体/情绪感受、现实安全背景、可控边界动作、提醒物、复盘时间、停止条件和指认/诅咒报复/危险仪式/专业替代/关系操控/高价购买/反复依赖边界是什么？")
    elif domain == "deity_ancestor":
        questions.append("这是神明/祖先/供奉文化学习、纪念感恩、供桌整理，还是低风险还愿反思；来源传统、对象、场合、已有物件、家庭同意边界、消防/食品/宠物儿童安全、复盘时间、停止条件和神明命令/灾祸恐吓/危险仪式/专业替代/操控报复/强迫家人/高价法事/反复依赖边界是什么？")
    elif domain == "sleep_paralysis":
        questions.append("这是鬼压床/梦魇文化学习、一次睡眠体验记录，还是睡前安定/醒后复位计划；发生模式、醒来状态、身体感、夜间印象、房间环境、近期压力、睡眠背景、白天影响、安定动作、复盘时间、停止条件和呼吸胸痛/抽搐/连续失眠/幻听幻视/自伤伤人/危险仪式/专业替代/高价法事/反复依赖边界是什么？")
    elif domain == "wealth_luck":
        questions.append("这是招财/财运文化学习、已有物件象征解释，还是预算/收入行动计划；现实目标、收入渠道、预算限制、已有物件、可控行动、复盘时间、停止条件和投资赌博借贷/收益保证/债务压力/违法诈骗/高价法事/神明命令/操控他人/反复依赖边界是什么？")
    elif domain == "relationship_luck":
        questions.append("这是桃花/姻缘文化学习、已有物件象征解释，还是自我呈现/社交沟通行动计划；现实关系状态、本人目标、同意范围、沟通边界、已有物件、可控行动、复盘时间、停止条件和跟踪骚扰/读心/操控复合/家暴威胁/自伤伤人/专业替代/结果保证/高价法事/反复依赖边界是什么？")
    elif domain == "consecration":
        questions.append("这是开光/加持/净物文化学习、已有物件来源整理，还是无火低风险提醒物照料计划；物件来源、材质/当前用途、已有物件、安全边界、可控动作、复盘时间、停止条件和危险仪式/摄入伤身/专业替代/灵验保证/高价开光/神明恐吓/欺骗操控/反复依赖边界是什么？")
    elif domain == "lost_object":
        questions.append("这是失物/寻物象征咨询、最后接触记忆复盘，还是现实搜索计划；物品描述、最后看见时间地点、当天路线、可能区域、已找区域、可联系渠道、现实行动、复盘时间、停止条件和寻人/走失宠物/犯罪证据/专业渠道替代/保证定位/隐私跟踪/反复依赖边界是什么？")
    elif domain == "sound_cleansing":
        questions.append("这是声响净化文化学习、已有铃钵/铃铛/音叉/诵念体验记录，还是低风险空间复位计划；空间、时段、声音工具、音量时长、身体感受、宠物/婴儿/邻里边界、收尾动作、复盘时间、停止条件和医疗心理替代/强制驱灵/声音暴露/扰民/效果保证/高价压力/反复依赖边界是什么？")
    elif domain == "talisman":
        questions.append("这是护符/符箓文化学习、记录已有物件，还是低风险象征咨询；来源、可见符号、使用场景和预算/已有物件说明是什么？")
    elif domain == "color":
        questions.append("这是五行颜色文化学习、穿搭提醒、空间配色，还是低风险象征咨询；场景、候选颜色、已有物件、预算和现实约束是什么？")
    elif domain == "zodiac":
        questions.append("这是生肖/太岁文化学习、本人反思，还是低风险象征咨询；年份/生肖、本人或第三方范围、来源说明和现实关注主题是什么？")
    elif domain == "date_selection":
        questions.append("事件类型、候选日期、不可用日期、现实约束和黄历/民俗来源是什么？")
    elif domain == "feng_shui":
        questions.append("空间类型、主要困扰、门窗/床桌灶位置、光线噪音和杂物情况是什么？")
    elif domain == "yijing":
        questions.append("问题是否已收束为一事一问；用户采用什么起卦方法？")
    elif domain == "liuyao":
        questions.append("问题是否一事一问；是否已有外部六爻盘、起卦方法、世应、六亲、六神和用神取法？")
    elif domain == "meihua":
        questions.append("问题是否一事一问；是否已有报数、时间、外应或外部卦盘来源，以及体卦/用卦/动爻取法？")
    elif domain == "qimen":
        questions.append("问题、起局时间、地点和时区是否明确？")
    elif domain == "mingli":
        questions.append("是否已获得本人同意；出生日期、时间、地点、历法和分析焦点是否明确？")
    elif domain == "naming":
        questions.append("名字用于大名、小名、艺名、笔名还是品牌名；用户更重视字义、读音、字形、五行民俗、谐音还是使用场景？")
    elif domain == "numerology":
        questions.append("是否已脱敏为尾号或非敏感数字；现实优先条件是记忆度、读音、价格、可用性还是个人偏好？")
    elif domain == "pendulum":
        questions.append("这是灵摆文化学习、校准，还是低风险自我反思；问题是否涉及专业替代、第三方隐私、超自然恐惧或反复依赖？")
    elif domain == "rune":
        questions.append("这是卢恩符文文化学习、记录已有抽取，还是低风险象征反思；问题是否涉及专业替代、第三方隐私、超自然恐惧或反复依赖？")
    elif domain == "physiognomy":
        questions.append("是否为本人且愿意以象征/文化学习方式讨论；是否涉及健康、寿命、颜值歧视或第三方外貌评价？")
    elif domain == "astrology":
        questions.append("用户是否提供了外部星盘字段；是否为本人资料，若涉及第三方是否已取得同意？")
    elif domain == "dream":
        questions.append("梦醒后最强烈的感受、最近现实背景、梦是否反复出现或影响睡眠是什么？")
    elif domain == "ritual_safety":
        questions.append("是否包含明火、血液、刀具、摄入、密闭燃烧或伤害他人的意图？")
    elif domain == "folk_custom":
        questions.append("这个民俗说法来自哪里；用户是想文化学习、写文案、安排活动、安抚家人，还是担心犯忌？")
    elif intent == "prediction":
        questions.append("能否把确定性预测改写为可反思、可行动的问题？")
    return questions


def next_steps_for(risk_level: str, domain: str) -> list[str]:
    if risk_level == "red":
        return ["stop_mystic_workflow", "offer_emergency_or_trusted_person_support"]
    if risk_level == "orange":
        return ["pause_divination_or_ritual", "refer_to_qualified_professional", "offer_grounding_support"]

    steps = ["continue_with_safety_notice", "restate_question_non_deterministically"]
    if domain != "unknown":
        steps.append(f"load_{domain}_sop")
    else:
        steps.append("ask_user_to_choose_domain")
    return steps


def triage(payload: dict[str, object]) -> dict[str, object]:
    text = str(payload.get("request_text", "")).strip()
    if not text:
        raise ValueError("request_text is required")
    requested_domain = payload.get("requested_domain")
    domain = detect_domain(text, str(requested_domain) if requested_domain else None)
    intent = detect_intent(text)
    risk_level, risk_signals = classify_risk(text)
    return {
        "request_text": text,
        "domain": domain,
        "intent": intent,
        "risk_level": risk_level,
        "risk_signals": risk_signals,
        "required_clarifications": clarifications_for(domain, intent, risk_level),
        "allowed_next_steps": next_steps_for(risk_level, domain),
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.text:
        return {"request_text": args.text, "requested_domain": args.domain}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw, "requested_domain": args.domain}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="User request text.")
    parser.add_argument("--domain", help="Optional requested domain.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
    args = parser.parse_args()

    try:
        result = triage(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
