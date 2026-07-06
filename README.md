# 玄学大典 / Occultism Agent Toolkit

Safety-first occultism knowledge base, toolchain, Codex Skill blueprint set, and local Web UI for symbolic consultation agents.

这个仓库用于沉淀玄学类 agent 的知识、SOP、工具规格、Codex Skill 蓝图和本地交互工作台。目标不是宣称玄学结论客观为真，而是把占卜、风水、仪式、象征解释等请求整理成可审计、可复用、可安全分流、可程序化接入的咨询流程。

## 当前推进目标

- 以 6 条主干收束 61 个领域，避免继续碎片化扩张。
- 对已建内容做科学化、溯源勘误和神秘强度分层。
- 建立给人使用的本地 Web UI，并开放轻量 API 给 agent/runtime 接入。
- 将知识库、工具、Skill 蓝图、验证证据和 UI 发布到 `noir-hedgehog/occultism.git`。

建议 GitHub description：

```text
Safety-first occultism agent toolkit: knowledge base, SOPs, Python tools, Codex Skill blueprints, and a local Web UI for symbolic consultation workflows.
```

## 当前结构

- [知识库/00-总览.md](知识库/00-总览.md)：项目范围、产物类型、成熟度定义
- [知识库/01-安全边界.md](知识库/01-安全边界.md)：高风险请求、用户状态筛查、升级处理
- [知识库/02-流派地图.md](知识库/02-流派地图.md)：首批流派与知识拆分方式
- [知识库/项目目标.md](知识库/项目目标.md)：当前推进目标、阶段和近期完成标准
- [知识库/03-主干生成发展史.md](知识库/03-主干生成发展史.md)：6 条主干从安全骨架、代表流派到范式层的生成过程
- [知识库/SOP/09-占星星盘象征咨询.md](知识库/SOP/09-占星星盘象征咨询.md)：占星/星盘象征咨询流程
- [知识库/SOP/10-六爻占问.md](知识库/SOP/10-六爻占问.md)：六爻占问流程
- [知识库/SOP/11-梅花易数占问.md](知识库/SOP/11-梅花易数占问.md)：梅花易数占问流程
- [知识库/SOP/12-姓名学命名咨询.md](知识库/SOP/12-姓名学命名咨询.md)：姓名学命名咨询流程
- [知识库/SOP/13-民俗节令与禁忌咨询.md](知识库/SOP/13-民俗节令与禁忌咨询.md)：民俗节令与禁忌咨询流程
- [知识库/SOP/14-解梦与梦境象征咨询.md](知识库/SOP/14-解梦与梦境象征咨询.md)：解梦与梦境象征咨询流程
- [知识库/SOP/15-择日与黄历象征咨询.md](知识库/SOP/15-择日与黄历象征咨询.md)：择日、黄历和吉日选择咨询流程
- [知识库/SOP/16-手相面相象征咨询.md](知识库/SOP/16-手相面相象征咨询.md)：手相、面相和相术象征咨询流程
- [知识库/SOP/17-求签与签文象征咨询.md](知识库/SOP/17-求签与签文象征咨询.md)：求签、解签和签文象征咨询流程
- [知识库/SOP/18-数字象征与号码咨询.md](知识库/SOP/18-数字象征与号码咨询.md)：数字象征、生命灵数和号码偏好咨询流程
- [知识库/SOP/19-灵摆占卜象征咨询.md](知识库/SOP/19-灵摆占卜象征咨询.md)：灵摆、摆锤和 yes/no 摆动象征咨询流程
- [知识库/SOP/20-卢恩符文象征咨询.md](知识库/SOP/20-卢恩符文象征咨询.md)：卢恩符文、单符/三符和 Elder Futhark 象征咨询流程
- [知识库/SOP/21-雷诺曼卡象征咨询.md](知识库/SOP/21-雷诺曼卡象征咨询.md)：雷诺曼卡、三张线、五张线和九宫格象征咨询流程
- [知识库/SOP/22-神谕卡象征咨询.md](知识库/SOP/22-神谕卡象征咨询.md)：神谕卡、牌组差异、图像母题和低风险象征反思流程
- [知识库/SOP/23-水晶与能量石象征咨询.md](知识库/SOP/23-水晶与能量石象征咨询.md)：水晶、能量石、佩戴/摆放和低风险提醒物咨询流程
- [知识库/SOP/24-护符符箓象征咨询.md](知识库/SOP/24-护符符箓象征咨询.md)：护符、符箓、平安符和低风险象征物咨询流程
- [知识库/SOP/25-生肖太岁象征咨询.md](知识库/SOP/25-生肖太岁象征咨询.md)：生肖、属相、本命年、太岁和低风险时间象征咨询流程
- [知识库/SOP/26-五行颜色开运色象征咨询.md](知识库/SOP/26-五行颜色开运色象征咨询.md)：五行颜色、开运色、穿搭/空间配色和低风险提醒流程
- [知识库/SOP/27-星骰占卜骰象征咨询.md](知识库/SOP/27-星骰占卜骰象征咨询.md)：星骰、占卜骰、骰面记录和低风险象征反思流程
- [知识库/SOP/28-茶叶咖啡渣占卜象征咨询.md](知识库/SOP/28-茶叶咖啡渣占卜象征咨询.md)：茶叶、咖啡渣、杯底图案和低风险象征反思流程
- [知识库/SOP/29-扑克牌占卜象征咨询.md](知识库/SOP/29-扑克牌占卜象征咨询.md)：扑克牌、纸牌占卜、牌面记录和低风险象征反思流程
- [知识库/SOP/30-蜡烛火焰蜡泪象征咨询.md](知识库/SOP/30-蜡烛火焰蜡泪象征咨询.md)：蜡烛火焰、蜡泪、观察来源和明火安全边界下的低风险象征反思流程
- [知识库/SOP/31-香火香灰烟形象征咨询.md](知识库/SOP/31-香火香灰烟形象征咨询.md)：香火、香灰、烟形、观察来源和火源/通风安全边界下的低风险象征反思流程
- [知识库/SOP/32-水晶球镜面水面凝视象征咨询.md](知识库/SOP/32-水晶球镜面水面凝视象征咨询.md)：水晶球、镜面、水面凝视、短时观察和 grounding 边界下的低风险象征反思流程
- [知识库/SOP/33-骨贝石子符物抛掷象征咨询.md](知识库/SOP/33-骨贝石子符物抛掷象征咨询.md)：骨、贝壳、石子、符物/小物抛掷、盘面关系和材料安全边界下的低风险象征反思流程
- [知识库/SOP/34-测字拆字象征咨询.md](知识库/SOP/34-测字拆字象征咨询.md)：测字、拆字、字形部件、用户联想和反标签边界下的低风险象征反思流程
- [知识库/SOP/35-花语植物象征咨询.md](知识库/SOP/35-花语植物象征咨询.md)：花语、花占、送花、植物象征和过敏/宠物安全边界下的低风险象征反思流程
- [知识库/SOP/36-动物征兆鸟兽虫鱼象征咨询.md](知识库/SOP/36-动物征兆鸟兽虫鱼象征咨询.md)：动物征兆、鸟兽虫鱼、民俗预兆和动物/公共卫生安全边界下的低风险象征反思流程
- [知识库/SOP/37-气场脉轮能量感受象征咨询.md](知识库/SOP/37-气场脉轮能量感受象征咨询.md)：气场、脉轮、能量感受、身体记录和医疗/心理健康边界下的低风险象征反思流程
- [知识库/SOP/38-前世阿卡西灵魂课题象征咨询.md](知识库/SOP/38-前世阿卡西灵魂课题象征咨询.md)：前世、阿卡西记录、灵魂课题、象征叙事和创伤/记忆恢复/宿命论边界下的低风险反思流程
- [知识库/SOP/39-月相月亮周期象征咨询.md](知识库/SOP/39-月相月亮周期象征咨询.md)：月相、月亮周期、新月许愿、满月释放和无火低风险意图/复盘流程
- [知识库/SOP/40-通灵高我讯息象征咨询.md](知识库/SOP/40-通灵高我讯息象征咨询.md)：通灵、高我、守护灵、天使讯息、自动书写和命令/幻听/第三方隐私边界下的象征写作流程
- [知识库/SOP/41-物品感应触物占卜象征咨询.md](知识库/SOP/41-物品感应触物占卜象征咨询.md)：物品感应、触物占卜、旧物/首饰/遗物象征联想和授权/隐私/事实边界下的低风险反思流程
- [知识库/SOP/42-书占随机翻书象征咨询.md](知识库/SOP/42-书占随机翻书象征咨询.md)：书占、随机翻书、短句/关键词象征反思和版权/经文权威/专业替代边界流程
- [知识库/SOP/43-天象云形征兆象征咨询.md](知识库/SOP/43-天象云形征兆象征咨询.md)：天象、云形、彩虹、日月晕和雷电天气征兆的观察记录、象征反思和天气安全边界流程
- [知识库/SOP/44-祈愿显化愿望仪式象征咨询.md](知识库/SOP/44-祈愿显化愿望仪式象征咨询.md)：祈愿、显化、愿望仪式和意图设定的低风险行动计划与结果保证/专业替代/危险仪式边界流程
- [知识库/SOP/45-宠物沟通动物灵性讯息象征咨询.md](知识库/SOP/45-宠物沟通动物灵性讯息象征咨询.md)：宠物沟通、动物灵性讯息、行为观察和亡宠怀念的兽医/走失/事实确认边界流程
- [知识库/SOP/46-同步性天使数字重复征兆象征咨询.md](知识库/SOP/46-同步性天使数字重复征兆象征咨询.md)：同步性、天使数字、重复征兆和宇宙讯号的低风险记录/行动反思与危险寻找/命令化/专业替代/读心边界流程
- [知识库/SOP/47-水逆行星逆行星象天气象征咨询.md](知识库/SOP/47-水逆行星逆行星象天气象征咨询.md)：水逆、行星逆行和星象天气的复盘/沟通/备份计划与宿命归因/专业替代/高价转运边界流程
- [知识库/SOP/48-恶眼能量防护断联象征咨询.md](知识库/SOP/48-恶眼能量防护断联象征咨询.md)：恶眼、能量防护、灵性防护和能量断联的边界整理/提醒物使用与指认/诅咒/危险仪式边界流程
- [知识库/SOP/49-神明祖先供奉祭拜象征咨询.md](知识库/SOP/49-神明祖先供奉祭拜象征咨询.md)：神明、祖先、供奉、祭拜和还愿的文化/纪念/感恩整理与神谕命令/危险仪式/高价法事边界流程
- [知识库/SOP/50-鬼压床梦魇睡前灵异恐惧象征咨询.md](知识库/SOP/50-鬼压床梦魇睡前灵异恐惧象征咨询.md)：鬼压床、梦魇、夜惊和睡前灵异恐惧的睡眠记录/醒后安定与灵体确认/危险仪式/专业替代边界流程
- [知识库/SOP/51-招财财运财库象征咨询.md](知识库/SOP/51-招财财运财库象征咨询.md)：招财、财运、财库和财神/貔貅等象征的预算/收入行动计划与投资赌博/收益保证/高价法事边界流程
- [知识库/SOP/52-桃花姻缘人缘象征咨询.md](知识库/SOP/52-桃花姻缘人缘象征咨询.md)：桃花、姻缘、人缘、月老、红线和粉晶的自我呈现/沟通边界/社交行动与读心操控/骚扰/高价和合边界流程
- [知识库/SOP/53-开光加持净物象征咨询.md](知识库/SOP/53-开光加持净物象征咨询.md)：开光、加持、净物、已有物件照料和低风险用途提醒的无火/非摄入/非灵验保证边界流程
- [知识库/SOP/54-失物寻物象征咨询.md](知识库/SOP/54-失物寻物象征咨询.md)：失物、寻物、找东西和方位占问的最后接触记录/路线复盘/区域搜索与寻人/犯罪/隐私定位边界流程
- [知识库/SOP/55-声响净化象征咨询.md](知识库/SOP/55-声响净化象征咨询.md)：声响净化、铃钵、铃铛、音叉、拍手和诵念的短时低音量空间复位与医疗/驱灵/扰民/高价器具边界流程
- [知识库/SOP/56-西洋土占盾形盘象征咨询.md](知识库/SOP/56-西洋土占盾形盘象征咨询.md)：西洋土占、盾形占、盾盘和 geomantic figures 的盘面记录、图形查询、现实复盘与专业替代/投资赌博/读心操控/反复起盘边界流程
- [知识库/SOP/57-九星气学九宫命星象征咨询.md](知识库/SOP/57-九星气学九宫命星象征咨询.md)：九星气学、九宫命星、本命星、年星和方位焦点的资料记录、象征查询、现实复盘与专业替代/投资赌博/关系标签/方位恐吓/高价化解/反复依赖边界流程
- [知识库/SOP/58-人类图象征咨询.md](知识库/SOP/58-人类图象征咨询.md)：人类图、Human Design、bodygraph、类型、策略、内在权威、人生角色、中心、通道和闸门的低风险象征咨询与出生资料隐私/诊断/职业财务保证/关系筛选/付费压力/反复依赖边界流程
- [知识库/SOP/59-芳香精油气味象征咨询.md](知识库/SOP/59-芳香精油气味象征咨询.md)：芳香、香薰、精油、香氛、气味、嗅觉、闻香纸和短时扩香的低风险气味象征与医疗/内服涂抹/孕婴宠物过敏/消防/驱邪/高价购买/反复依赖边界流程
- [知识库/SOP/60-草本香草植物魔法象征咨询.md](知识库/SOP/60-草本香草植物魔法象征咨询.md)：草本、香草、草药、药草、植物魔法、绿巫、草本包、香草包、草药袋和植物意图卡的低风险植物象征与医疗/内服外敷/孕婴宠物过敏/野采辨毒/消防烟雾/驱邪/爱情咒诅咒/高价购买/反复依赖边界流程
- [知识库/SOP/61-Sigil符号印记魔法阵象征咨询.md](知识库/SOP/61-Sigil符号印记魔法阵象征咨询.md)：sigil、符号印记、印记魔法、魔法印记、意图符号、愿望符号、seal magic、魔法阵和符号阵的低风险符号象征与血/身体伤害/纹身永久化/焚烧/召唤驱邪/诅咒操控/结果保证/专业替代/高价购买/反复依赖边界流程
- [知识库/SOP/62-占杖寻水杖探测棒象征咨询.md](知识库/SOP/62-占杖寻水杖探测棒象征咨询.md)：占杖、寻水杖、探测棒、探测杆、探矿杖、dowsing rods、divining rods、L-rods、map dowsing 和 radiesthesia 的低风险路线/空间象征与地下管线/开挖打井/水源资源/医疗地气/房产合同/第三方定位/驱邪/高价购买/反复依赖边界流程
- [知识库/SOP/63-身体征兆眼跳耳鸣喷嚏象征咨询.md](知识库/SOP/63-身体征兆眼跳耳鸣喷嚏象征咨询.md)：身体征兆、眼跳、左眼跳、右眼跳、耳鸣、耳热、喷嚏、脸热、手心痒和肉跳的低风险民俗象征与医疗红旗/灾祸恐吓/彩票投资/第三方标签/驱邪恐惧/危险试验/反复依赖边界流程
- [知识库/流派/占星.md](知识库/流派/占星.md)：占星流派知识卡
- [知识库/流派/解梦.md](知识库/流派/解梦.md)：解梦与梦境象征知识卡
- [知识库/流派/择日与黄历.md](知识库/流派/择日与黄历.md)：择日与黄历知识卡
- [知识库/流派/手相与面相.md](知识库/流派/手相与面相.md)：手相、面相和相术知识卡
- [知识库/流派/求签与签文.md](知识库/流派/求签与签文.md)：求签、解签和签文知识卡
- [知识库/流派/数字象征与号码.md](知识库/流派/数字象征与号码.md)：数字象征、生命灵数和号码知识卡
- [知识库/流派/灵摆占卜.md](知识库/流派/灵摆占卜.md)：灵摆、摆锤和摆动象征知识卡
- [知识库/流派/卢恩符文.md](知识库/流派/卢恩符文.md)：卢恩符文和 Elder Futhark 象征知识卡
- [知识库/流派/雷诺曼卡.md](知识库/流派/雷诺曼卡.md)：雷诺曼卡 36 张牌、线性牌阵和相邻组合知识卡
- [知识库/流派/神谕卡.md](知识库/流派/神谕卡.md)：神谕卡牌组来源、常见图像母题、牌义边界和咨询流程知识卡
- [知识库/流派/水晶与能量石.md](知识库/流派/水晶与能量石.md)：水晶与能量石的象征、使用场景、消费边界和危险用法禁区
- [知识库/流派/护符符箓.md](知识库/流派/护符符箓.md)：护符、符箓、平安符、红绳和香囊的象征、来源边界和危险用法禁区
- [知识库/流派/生肖太岁.md](知识库/流派/生肖太岁.md)：生肖、属相、本命年、太岁、合冲和化解话术的文化边界
- [知识库/流派/五行颜色与开运色.md](知识库/流派/五行颜色与开运色.md)：五行颜色、开运色、穿搭配色、空间配色和消费边界
- [知识库/流派/星骰与占卜骰.md](知识库/流派/星骰与占卜骰.md)：星骰、占星骰、占卜骰的骰面组合、记录边界和反复依赖风险
- [知识库/流派/茶叶与咖啡渣占卜.md](知识库/流派/茶叶与咖啡渣占卜.md)：茶叶、咖啡渣、杯底图案、观察来源和食品安全边界
- [知识库/流派/扑克牌占卜.md](知识库/流派/扑克牌占卜.md)：标准 52 张扑克牌、花色点数、抽牌来源和反复依赖边界
- [知识库/流派/蜡烛火焰与蜡泪.md](知识库/流派/蜡烛火焰与蜡泪.md)：蜡烛火焰、蜡泪形态、观察记录和明火/驱邪/专业替代边界
- [知识库/流派/香火香灰与烟形.md](知识库/流派/香火香灰与烟形.md)：香火、香灰、烟形、香头余光、观察记录和火源/通风/驱邪/高价购买边界
- [知识库/流派/水晶球镜面与水面凝视.md](知识库/流派/水晶球镜面与水面凝视.md)：水晶球、镜面、黑镜、水面凝视、视觉联想和身心安全/灵体恐惧/反复依赖边界
- [知识库/流派/骨贝石子与符物抛掷.md](知识库/流派/骨贝石子与符物抛掷.md)：骨、贝壳、石子、钥匙、硬币等符物抛掷的物件、区域、关系和材料安全边界
- [知识库/流派/测字与拆字.md](知识库/流派/测字与拆字.md)：测字、拆字、汉字部件、结构、用户联想和寿命/人格/儿童标签禁区
- [知识库/流派/花语与植物象征.md](知识库/流派/花语与植物象征.md)：花语、植物象征、送花语境、民俗来源和疗愈/过敏/宠物安全边界
- [知识库/流派/动物征兆与鸟兽虫鱼.md](知识库/流派/动物征兆与鸟兽虫鱼.md)：动物征兆、鸟兽虫鱼、现实观察、民俗象征和动物伤害/虫害/公共卫生边界
- [知识库/流派/气场脉轮与能量感受.md](知识库/流派/气场脉轮与能量感受.md)：气场、脉轮、能量感受、身体觉察、grounding 和医疗/灵异/付费疗愈边界
- [知识库/流派/前世阿卡西与灵魂课题.md](知识库/流派/前世阿卡西与灵魂课题.md)：前世、阿卡西、灵魂契约、业力关系和象征叙事的记忆/创伤/宿命论边界
- [知识库/流派/月相与月亮周期.md](知识库/流派/月相与月亮周期.md)：新月、满月、月食、蓝月等月相周期的意图整理、复盘和危险仪式/显化保证边界
- [知识库/流派/通灵高我与灵性讯息.md](知识库/流派/通灵高我与灵性讯息.md)：通灵、高我、守护灵、天使讯息、自动书写和灵性讯息的象征写作/专业边界
- [知识库/流派/物品感应与触物占卜.md](知识库/流派/物品感应与触物占卜.md)：物品感应、触物占卜、旧物/首饰/遗物联想和失踪犯罪/第三方隐私/真伪归属边界
- [知识库/流派/书占与随机翻书.md](知识库/流派/书占与随机翻书.md)：书占、随机翻书、短摘录/关键词、经典/经文和版权合规边界
- [知识库/流派/天象云形与天气征兆.md](知识库/流派/天象云形与天气征兆.md)：天象、云形、彩虹、日月晕、雷电和天气征兆的民俗象征、安全预警边界和低风险观察反思
- [知识库/流派/祈愿显化与愿望仪式.md](知识库/流派/祈愿显化与愿望仪式.md)：祈愿、显化、愿望清单、意图设定和象征提醒物的现实行动/复盘边界
- [知识库/流派/宠物沟通与动物灵性讯息.md](知识库/流派/宠物沟通与动物灵性讯息.md)：宠物沟通、动物沟通、行为观察、照护动作和亡宠怀念的低风险象征写作边界
- [知识库/流派/同步性天使数字与重复征兆.md](知识库/流派/同步性天使数字与重复征兆.md)：同步性、天使数字、重复数字、歌曲/名字/羽毛等重复征兆的非命令化低风险反思边界
- [知识库/流派/水逆行星逆行与星象天气.md](知识库/流派/水逆行星逆行与星象天气.md)：水逆、行星逆行、逆行阴影期和星象天气的非宿命化复盘/沟通检查边界
- [知识库/流派/恶眼能量防护与断联.md](知识库/流派/恶眼能量防护与断联.md)：恶眼、能量防护、保护罩、能量断联和提醒物的非指认、非报复低风险边界整理
- [知识库/流派/神明祖先供奉与祭拜.md](知识库/流派/神明祖先供奉与祭拜.md)：神明、祖先、供桌、供品、祭拜、许愿还愿和家庭纪念的非命令、非恐吓低风险整理
- [知识库/流派/鬼压床梦魇与睡前灵异恐惧.md](知识库/流派/鬼压床梦魇与睡前灵异恐惧.md)：鬼压床、睡眠瘫痪、梦魇、夜惊和床边人影体验的非灵体确认睡眠安定流程
- [知识库/流派/招财财运与财库象征.md](知识库/流派/招财财运与财库象征.md)：招财、财运、财库、财神、貔貅、金蟾和聚宝盆的非收益保证预算/行动整理流程
- [知识库/流派/桃花姻缘与人缘象征.md](知识库/流派/桃花姻缘与人缘象征.md)：桃花、姻缘、人缘、月老、红线、粉晶和社交行动的非读心、非操控、尊重同意整理流程
- [知识库/流派/开光加持与净物象征.md](知识库/流派/开光加持与净物象征.md)：开光、加持、净物、圣化和物件照料的非灵验保证、非危险仪式、非高价法事整理流程
- [知识库/流派/失物寻物象征.md](知识库/流派/失物寻物象征.md)：失物、寻物、找东西、方位线索和现实搜索清单的非定位保证、非寻人、非犯罪指认整理流程
- [知识库/流派/声响净化与铃钵象征.md](知识库/流派/声响净化与铃钵象征.md)：声响净化、铃钵、铃铛、音叉、拍手和诵念的空间复位、注意力提示、低音量时长和停止条件整理流程
- [知识库/流派/西洋土占与盾形盘.md](知识库/流派/西洋土占与盾形盘.md)：西洋土占、盾形盘、16 个常见 geomantic figures、见证者和裁判者的低风险象征反思整理流程
- [知识库/流派/九星气学与九宫命星.md](知识库/流派/九星气学与九宫命星.md)：九星气学、九宫命星、一白到九紫、本命星、年星和方位焦点的低风险象征反思整理流程
- [知识库/流派/人类图.md](知识库/流派/人类图.md)：人类图、Human Design、bodygraph、类型、策略、内在权威、人生角色、中心、通道和闸门的低风险象征反思整理流程
- [知识库/流派/芳香精油与气味象征.md](知识库/流派/芳香精油与气味象征.md)：芳香、香薰、精油、香氛、气味、闻香纸、香包和短时空间气味的低风险象征反思整理流程
- [知识库/流派/草本香草与植物魔法象征.md](知识库/流派/草本香草与植物魔法象征.md)：草本、香草、草药、药草、植物魔法、绿巫、草药袋、植物意图卡和非接触植物提醒物的低风险象征反思整理流程
- [知识库/流派/Sigil符号印记与魔法阵象征.md](知识库/流派/Sigil符号印记与魔法阵象征.md)：sigil、符号印记、魔法阵、意图符号、形状母题、字母合并和纸面/数字草稿的低风险象征反思整理流程
- [知识库/流派/占杖寻水杖与探测棒象征.md](知识库/流派/占杖寻水杖与探测棒象征.md)：占杖、寻水杖、探测棒、L-rods、地图探测、杆体动作、授权空间和现实核查清单的低风险象征反思整理流程
- [知识库/流派/身体征兆眼跳耳鸣喷嚏象征.md](知识库/流派/身体征兆眼跳耳鸣喷嚏象征.md)：眼跳、耳鸣、喷嚏、耳热、脸热、手心痒、肉跳、时辰记录和身体照料清单的低风险民俗象征反思整理流程
- [知识库/流派/六爻.md](知识库/流派/六爻.md)：六爻流派知识卡
- [知识库/流派/梅花易数.md](知识库/流派/梅花易数.md)：梅花易数流派知识卡
- [知识库/流派/姓名学.md](知识库/流派/姓名学.md)：姓名学流派知识卡
- [知识库/流派/民俗节令与禁忌.md](知识库/流派/民俗节令与禁忌.md)：民俗节令与禁忌知识卡
- [知识库/流派/跨流派深度解读矩阵.md](知识库/流派/跨流派深度解读矩阵.md)：牌义、卦义、盘式、方位、命理和仪式的深度解释边界与案例
- [知识库/流派/跨流派深度案例集.md](知识库/流派/跨流派深度案例集.md)：跨流派安全示例、禁用表达和审查问题
- [知识库/流派/风水理气派别边界.md](知识库/流派/风水理气派别边界.md)：玄空飞星、八宅、三合/三元和择日等理气派别守门
- [知识库/流派/风水阳宅案例库.md](知识库/流派/风水阳宅案例库.md)：卧室、玄关、厨房、书房/办公室和店铺阳宅案例
- [知识库/04-质量检查清单.md](知识库/04-质量检查清单.md)：知识卡、SOP、Tool、Skill 的验收标准
- [知识库/05-路线图.md](知识库/05-路线图.md)：分阶段建设计划
- [知识库/06-体系盘点与主干路线.md](知识库/06-体系盘点与主干路线.md)：当前主干/分支盘点、科学化/溯源/神秘强度和案例验证优先级
- [知识库/07-问题到范式映射.md](知识库/07-问题到范式映射.md)：从具体用户问题推导适用范式、自动化边界和 agent 分工
- [知识库/Skill回放验证.md](知识库/Skill回放验证.md)：首批 Skill 前向回放案例
- [知识库/Skill多轮回放验证.md](知识库/Skill多轮回放验证.md)：多轮 transcript 验证案例
- [知识库/Agent路由冒烟验证.md](知识库/Agent路由冒烟验证.md)：跨流派运行时路由冒烟验证
- [知识库/Agent运行时DryRun验证.md](知识库/Agent运行时DryRun验证.md)：代表请求的 runtime 契约 dry-run 验证
- [知识库/Agent工具WrapperManifest.md](知识库/Agent工具WrapperManifest.md)：agent runtime/MCP/API wrapper 元数据清单
- [知识库/Agent工具定义导出.md](知识库/Agent工具定义导出.md)：agent tool definition 和 OpenAI-style function tool 导出
- [知识库/Agent工具定义验证.md](知识库/Agent工具定义验证.md)：注册前验证工具定义、OpenAI-style function tool 和本地引用
- [知识库/Agent工具注册表.md](知识库/Agent工具注册表.md)：runtime 注册顺序、流派/Skill 索引和安全启动工具
- [知识库/Agent工具注册表验证.md](知识库/Agent工具注册表验证.md)：注册前验证注册顺序、Skill 索引和安全 bootstrap 一致性
- [知识库/Skill蓝图验证.md](知识库/Skill蓝图验证.md)：Skill frontmatter、引用和工具钩子静态验证
- [知识库/匿名真实对话验证流程.md](知识库/匿名真实对话验证流程.md)：真实对话脱敏、评分和回放接入流程
- [知识库/真实对话Fixture规范.md](知识库/真实对话Fixture规范.md)：脱敏 transcript 进入回放前的 fixture 评分与批准规则
- [知识库/工具与Skill Manifest规范.md](知识库/工具与Skill Manifest规范.md)：工具三件套与 Skill 依赖 manifest 规范
- [知识库/维护审计.md](知识库/维护审计.md)：覆盖度审计和维护质量门
- [知识库/发布验收.md](知识库/发布验收.md)：发布前一键质量门
- [知识库/版本记录.md](知识库/版本记录.md)：版本状态、自动证据和开放事项
- [知识库/维护节奏.md](知识库/维护节奏.md)：每次变更、每批素材、每月和发布前维护节奏
- [知识库/内容审校包.md](知识库/内容审校包.md)：各流派人工内容审校入口
- [知识库/内容审校反馈记录规范.md](知识库/内容审校反馈记录规范.md)：内容专家反馈记录与批准计数规则
- [知识库/Skill安装准备报告.md](知识库/Skill安装准备报告.md)：Codex Skill 安装 dry-run 和审批清单
- [知识库/SOP-Tool-Skill追踪矩阵.md](知识库/SOP-Tool-Skill追踪矩阵.md)：SOP、工具、Skill 和验证证据追踪矩阵
- [知识库/试运行准备度报告.md](知识库/试运行准备度报告.md)：内部试运行准备度和外部阻塞项汇总
- [知识库/外部证据入口包.md](知识库/外部证据入口包.md)：安装确认、真实 transcript 和专家审校的收集入口
- [知识库/Agent运行时交接包.md](知识库/Agent运行时交接包.md)：agent runtime 接入所需入口、工具链和验证命令
- [知识库/导航索引.md](知识库/导航索引.md)：给维护者和使用者看的知识库入口
- [知识库/看板.md](知识库/看板.md)：人类可读的任务看板
- [知识库/仪表盘.md](知识库/仪表盘.md)：成熟度、工具、Skill 状态
- [知识库/SOP](知识库/SOP)：可执行流程
- [知识库/流派](知识库/流派)：各流派知识卡
- [知识库/模板](知识库/模板)：新增流派、SOP、Tool、Skill 时使用的模板
- [agent-tools](agent-tools)：工具规格、输入输出 schema、tool catalog
- [codex-skills](codex-skills/index.md)：可迁移到 Codex skills 目录的 skill 蓝图
- [web-ui](web-ui/README.md)：本地 Web UI 和轻量 API

## 建设原则

1. 安全优先：遇到医疗、法律、财务、人身安全、精神危机等请求，必须先分流到现实世界支持。
2. 过程可见：每次解读都记录输入、方法、限制、输出结构和后续建议。
3. 流派分离：不同体系的概念、步骤和证据等级分别维护，避免混搭成不可验证的黑箱。
4. 人机双读：知识库给人看，Skill 给 agent 执行，Tool 负责结构化、可重复的子任务。
5. 逐步深化：先建立模板和低风险 SOP，再为每个流派补充术语、牌义/卦义/盘式、案例和验证集。

## 当前可运行命令

```bash
python3 agent-tools/scripts/mystic_intake_triage.py --text "帮我做一个塔罗三张牌，看看工作状态"
python3 agent-tools/scripts/agent_workflow_router.py --text "帮我做一个塔罗三张牌，看看工作状态"
python3 agent-tools/scripts/paradigm_selector.py --text "帮我做一个塔罗三张牌，看看工作状态"
python3 agent-tools/scripts/consultation_packet_builder.py --text "帮我做一个塔罗三张牌，看看工作状态"
python3 agent-tools/scripts/agent_route_smoke_runner.py
python3 agent-tools/scripts/agent_runtime_dry_run_runner.py
python3 agent-tools/scripts/agent_tool_wrapper_manifest_builder.py --format markdown
python3 agent-tools/scripts/agent_tool_definition_exporter.py --format openai
python3 agent-tools/scripts/agent_tool_definition_validator.py --format markdown
python3 agent-tools/scripts/agent_tool_registry_builder.py --format markdown
python3 agent-tools/scripts/agent_tool_registry_validator.py --format markdown
python3 agent-tools/scripts/release_gate_runner.py
python3 agent-tools/scripts/ritual_safety_check.py --text "搬家后想做一个不用火的空间净化"
python3 agent-tools/scripts/mystic_output_lint.py --text "你家有鬼，这件事一定会带来大祸。"
python3 agent-tools/scripts/codex_skill_blueprint_validator.py
python3 agent-tools/scripts/codex_skill_installer.py --codex-home /tmp/mystic-codex-home-preview
python3 agent-tools/scripts/release_manifest_builder.py --version 0.1.0
python3 agent-tools/scripts/tool_manifest_builder.py
python3 agent-tools/scripts/knowledge_navigation_builder.py --format markdown
python3 agent-tools/scripts/content_review_packet_builder.py --format markdown
python3 agent-tools/scripts/content_review_feedback_recorder.py --domain tarot --reviewer tarot-reviewer --review-date 2026-07-02 --decision approved --approved-scope "塔罗 SOP、知识卡、Skill 和工具 spec"
python3 agent-tools/scripts/skill_install_readiness_report.py --codex-home /tmp/mystic-codex-home-preview --format markdown
python3 agent-tools/scripts/sop_traceability_matrix_builder.py --format markdown
python3 agent-tools/scripts/pilot_readiness_report.py --codex-home /tmp/mystic-codex-home-preview --format markdown
python3 agent-tools/scripts/external_evidence_intake_builder.py --codex-home /tmp/mystic-codex-home-preview --format markdown
python3 agent-tools/scripts/agent_runtime_handoff_builder.py --codex-home /tmp/mystic-codex-home-preview --format markdown
python3 agent-tools/scripts/transcript_fixture_builder.py --skill tarot --source-label real-001 --reviewer reviewer-a --review-approved --scores '{"safety":2,"clarification":1,"workflow_fit":1,"symbol_accuracy":1,"actionability":1,"tone":1}' --text 'user: 最近工作很烦'
python3 web-ui/server.py --port 8765
python3 agent-tools/scripts/tarot_spread_selector.py --text "我该选 A offer 还是 B offer？"
python3 agent-tools/scripts/tarot_draw_recorder.py --json '{"spread_id":"single_focus","cards":[{"card":"愚者","orientation":"正位"}]}'
python3 agent-tools/scripts/tarot_draw_simulator.py --spread-id three_card_situation --seed demo-seed --orientation-mode mixed
python3 agent-tools/scripts/tarot_card_lookup.py --card "Three of Swords" --orientation reversed --position "阻碍"
python3 agent-tools/scripts/tarot_interpretation_planner.py --json '{"question_text":"我当前工作局势如何？","spread_id":"three_card_situation","cards":[{"card":"愚者","orientation":"upright"},{"card":"宝剑三","orientation":"reversed"},{"card":"星币国王","orientation":"upright"}]}'
python3 agent-tools/scripts/tarot_combination_planner.py --json '{"question_text":"我当前工作状态的组合倾向是什么？","spread_id":"three_card_situation","cards":[{"card":"愚者","orientation":"upright"},{"card":"宝剑三","orientation":"reversed"},{"card":"星币国王","orientation":"reversed"}]}'
python3 agent-tools/scripts/fengshui_observation_recorder.py --text "图里卧室床正对门，镜子对床，床边过道堆了箱子" --input-mode image_notes
python3 agent-tools/scripts/fengshui_space_checklist.py --text "卧室睡不好，床正对门，镜子对床"
python3 agent-tools/scripts/fengshui_school_guard.py --text "用玄空飞星看厨房五黄是不是会破财生病"
python3 agent-tools/scripts/fengshui_yangzhai_case_library.py --query "卧室床正对门，镜子对床，睡不好"
python3 agent-tools/scripts/fengshui_bagua_mapper.py --text "书房在东南方，文件很多，想改善工作和财务感受"
python3 agent-tools/scripts/fengshui_recommendation_ranker.py --json '{"recommendations":[{"recommendation":"检查燃气和通风"},{"recommendation":"清理门后杂物"}]}'
python3 agent-tools/scripts/yijing_question_guard.py --text "我该不该跳槽？"
python3 agent-tools/scripts/yijing_casting_method_advisor.py --text "我当前工作局势的主要变化是什么？" --method three_coins --user-consent-to-simulation
python3 agent-tools/scripts/yijing_casting_simulator.py --method three_coins --seed demo --question "我当前工作局势的主要变化是什么？"
python3 agent-tools/scripts/yijing_hexagram_record.py --json '{"question_text":"我该不该跳槽？","casting_method":"manual","lines":[7,7,7,7,7,7]}'
python3 agent-tools/scripts/yijing_hexagram_lookup.py --query "既济" --line 3
python3 agent-tools/scripts/yijing_line_lookup.py --query "既济" --line 3
python3 agent-tools/scripts/yijing_source_reference_guard.py --text "短视频说这个爻必有灾、股票必发财" --source-type internet_claim
python3 agent-tools/scripts/liuyao_symbol_lookup.py --query 官鬼 --category kinship --focus project
python3 agent-tools/scripts/liuyao_chart_recorder.py --json '{"question_text":"这个项目合作当前的主要阻力和下一步是什么？","casting_method":"external_chart","chart_source":"用户提供外部盘","base_hexagram":"泽雷随","changed_hexagram":"水雷屯","focus_spirit":"官鬼","focus_logic":"项目合作以应爻和官鬼为外部压力观察点","lines":[{"position":1,"yin_yang":"yang","kinship":"父母","spirit":"青龙"},{"position":2,"yin_yang":"yin","kinship":"兄弟","spirit":"朱雀","roles":["世爻"]},{"position":3,"yin_yang":"yang","kinship":"官鬼","spirit":"勾陈","roles":["应爻","用神"],"changing":true},{"position":4,"yin_yang":"yin","kinship":"妻财","spirit":"腾蛇"},{"position":5,"yin_yang":"yang","kinship":"子孙","spirit":"白虎"},{"position":6,"yin_yang":"yin","kinship":"父母","spirit":"玄武"}]}'
python3 agent-tools/scripts/liuyao_focus_selector.py --json '{"question_text":"这个项目合作当前的主要阻力和下一步是什么？","casting_method":"external_chart","chart_source":"用户提供外部盘","base_hexagram":"泽雷随","changed_hexagram":"水雷屯","focus_spirit":"官鬼","focus_logic":"项目合作以应爻和官鬼为外部压力观察点","lines":[{"position":1,"yin_yang":"yang","kinship":"父母","spirit":"青龙"},{"position":2,"yin_yang":"yin","kinship":"兄弟","spirit":"朱雀","roles":["世爻"]},{"position":3,"yin_yang":"yang","kinship":"官鬼","spirit":"勾陈","roles":["应爻","用神"],"changing":true},{"position":4,"yin_yang":"yin","kinship":"妻财","spirit":"腾蛇"},{"position":5,"yin_yang":"yang","kinship":"子孙","spirit":"白虎"},{"position":6,"yin_yang":"yin","kinship":"父母","spirit":"玄武"}]}'
python3 agent-tools/scripts/meihua_symbol_lookup.py --query 体卦 --category structure --focus project
python3 agent-tools/scripts/meihua_casting_recorder.py --json '{"question_text":"这个项目沟通当前的主要阻力和下一步是什么？","casting_method":"number_casting","numbers":[27,14],"body_trigram":"离","use_trigram":"坎","moving_line":3,"base_hexagram":"火水未济","mutual_hexagram":"水火既济","changed_hexagram":"火风鼎"}'
python3 agent-tools/scripts/meihua_omen_recorder.py --question "这个项目沟通当前的主要阻力和下一步是什么？" --text "刚问完手机响了一声；客户群里有人发来延期消息" --source-type self_observed --timing after_question
python3 agent-tools/scripts/meihua_relation_interpreter.py --json '{"question_text":"这个项目沟通当前的主要阻力和下一步是什么？","casting_method":"number_casting","numbers":[27,14],"body_trigram":"离","use_trigram":"坎","moving_line":3}'
python3 agent-tools/scripts/naming_symbol_lookup.py --query 字义 --category dimension --focus baby_name
python3 agent-tools/scripts/naming_candidate_comparator.py --json '{"request_text":"想比较沐安、清宁哪个更适合宝宝名","name_type":"formal_name","surname":"林","candidates":["沐安","清宁"],"priorities":["字义","读音"],"desired_elements":["water"],"subject_is_minor":true}'
python3 agent-tools/scripts/naming_brand_scenario_scorer.py --json '{"request_text":"给茶饮品牌比较星禾和清朗","candidates":["星禾","清朗"],"category":"茶饮","audience":"年轻上班族","tone":["清爽","年轻"],"channels":["门头","小红书","搜索","域名"]}'
python3 agent-tools/scripts/qimen_method_guard.py --json '{"method":"time_chart","school":"zhirun","chart_time":"2026-06-30 15:00","timezone":"Asia/Shanghai","location":"Shanghai","solar_time_strategy":"true_solar_time","solar_term_source":"external_calendar"}'
python3 agent-tools/scripts/qimen_school_reference.py --query "置闰和拆补有什么区别"
python3 agent-tools/scripts/qimen_chart_record.py --json '{"question_text":"这个项目下一步怎么推进？","palaces":[{"palace":1,"trigram":"坎","earth_stem":"戊","heaven_stem":"乙","door":"休门","star":"天蓬","deity":"值符"}]}'
python3 agent-tools/scripts/qimen_focus_selector.py --json '{"question_text":"这个项目下一步怎么推进？","day_stem":"戊","hour_stem":"乙","duty_door":"开门","duty_star":"天心","palaces":[{"palace":1,"trigram":"坎","earth_stem":"戊","heaven_stem":"乙","door":"休门","star":"天蓬","deity":"值符"}]}'
python3 agent-tools/scripts/ritual_source_guard.py --text "老人说搬家后点蜡烛烧纸能驱邪" --source-type regional_folk
python3 agent-tools/scripts/ritual_low_risk_protocol.py --text "搬进新家后想做一个不用火的净化流程"
python3 agent-tools/scripts/ritual_source_example_lookup.py --text "某课程说买水晶阵能保证转运"
python3 agent-tools/scripts/folk_custom_lookup.py --query 端午 --category festival --focus cultural_learning
python3 agent-tools/scripts/folk_source_recorder.py --text "家里老人说江南搬家要先开灯和清扫入口" --custom-name 搬家习俗 --source-type family_oral --region 江南 --source-label 外婆口述 --source-date "上一辈口述" --usage-context family_communication
python3 agent-tools/scripts/folk_taboo_reframer.py --text "夜里吹口哨是不是一定会招鬼害家人" --source-type family --region "江南家庭说法"
python3 agent-tools/scripts/knowledge_coverage_audit.py
python3 agent-tools/scripts/bazi_ziwei_intake_guard.py --text "本人公历1990年5月1日08:30北京出生，想用八字看看事业倾向"
python3 agent-tools/scripts/bazi_ziwei_chart_record.py --json '{"system":"bazi","birth_date":"1990-05-01","birth_time":"08:30","birth_place":"北京","calendar_type":"solar","timezone":"Asia/Shanghai","solar_time_strategy":"not_applied","school":"ziping","chart_source":"external_calculator","analysis_focus":"career","subject_is_self":true}'
python3 agent-tools/scripts/mingli_school_reference.py --query "子平和紫微三合能混着看事业吗"
python3 agent-tools/scripts/mingli_symbol_lookup.py --query 七杀 --category ten_god --focus career
python3 agent-tools/scripts/astrology_chart_record.py --json '{"chart_source":"external_calculator","analysis_focus":"career","subject_is_self":true,"placements":[{"type":"planet","name":"太阳","sign":"天秤","house":"十宫"},{"type":"planet","name":"月亮","sign":"巨蟹"},{"type":"point","name":"上升","sign":"摩羯"}]}'
python3 agent-tools/scripts/astrology_compatibility_guard.py --text "用合盘看我和前任是不是命中注定的绝配"
python3 agent-tools/scripts/astrology_symbol_lookup.py --query 天秤 --category sign --focus relationship
python3 agent-tools/scripts/symbolic_case_library.py --domain tarot --query 工作
python3 agent-tools/scripts/symbolic_depth_lookup.py --domain tarot --query 逆位
python3 agent-tools/scripts/transcript_anonymizer.py --skill mingli --source-label review-001 --text "用户：我叫张三，想看前任1991年2月3日10:00上海出生的紫微感情"
python3 agent-tools/scripts/skill_replay_runner.py
python3 agent-tools/scripts/skill_transcript_runner.py
python3 -m unittest discover -s agent-tools/tests
```
