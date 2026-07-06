# Agent Tool Registry

本页把已验证的 agent tool definitions 组织成 runtime 注册表，包括注册顺序、按流派索引、按 Skill 索引和安全启动工具。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| 状态 | `ready_for_runtime_registration` |
| Tool | 277 |
| Domain group | 62 |
| Skill group | 61 |

## Runtime Contract

- `register`：Register entries in registration_order.
- `execute`：Invoke command with schema-validated input and preserve JSON stdout.
- `guard`：Do not call domain tools when agent_workflow_router returns paused or blocked status.
- `lint`：Run mystic_output_lint or equivalent before user-visible mystic output.

## Safety Bootstrap

- `mystic_intake_triage`
- `agent_workflow_router`
- `mystic_output_lint`
- `ritual_safety_check`
- `bazi_ziwei_intake_guard`
- `astrology_compatibility_guard`
- `fengshui_school_guard`
- `yijing_question_guard`
- `qimen_method_guard`

## Registration Order

1. `mystic_intake_triage`
2. `agent_workflow_router`
3. `mystic_output_lint`
4. `ritual_safety_check`
5. `bazi_ziwei_intake_guard`
6. `astrology_compatibility_guard`
7. `fengshui_school_guard`
8. `yijing_question_guard`
9. `qimen_method_guard`
10. `agent_route_smoke_runner`
11. `agent_runtime_dry_run_runner`
12. `agent_runtime_handoff_builder`
13. `agent_tool_definition_exporter`
14. `agent_tool_definition_validator`
15. `agent_tool_registry_builder`
16. `agent_tool_registry_validator`
17. `agent_tool_wrapper_manifest_builder`
18. `codex_skill_blueprint_validator`
19. `codex_skill_installer`
20. `content_review_feedback_recorder`
21. `content_review_packet_builder`
22. `external_evidence_intake_builder`
23. `knowledge_coverage_audit`
24. `knowledge_navigation_builder`
25. `paradigm_selector`
26. `pilot_readiness_report`
27. `release_gate_runner`
28. `release_manifest_builder`
29. `skill_install_readiness_report`
30. `sop_traceability_matrix_builder`
31. `symbolic_case_library`
32. `symbolic_depth_lookup`
33. `tool_manifest_builder`
34. `transcript_anonymizer`
35. `transcript_fixture_builder`
36. `animal_omen_request_guard`
37. `aroma_request_guard`
38. `aura_chakra_request_guard`
39. `bibliomancy_request_guard`
40. `body_omen_request_guard`
41. `candle_request_guard`
42. `cartomancy_request_guard`
43. `casting_lots_request_guard`
44. `cezi_request_guard`
45. `color_request_guard`
46. `consecration_request_guard`
47. `crystal_request_guard`
48. `date_selection_guard`
49. `deity_ancestor_request_guard`
50. `dice_request_guard`
51. `dowsing_request_guard`
52. `flower_request_guard`
53. `herbal_request_guard`
54. `human_design_request_guard`
55. `incense_request_guard`
56. `lenormand_request_guard`
57. `lost_object_request_guard`
58. `manifestation_request_guard`
59. `moon_phase_request_guard`
60. `nine_star_ki_request_guard`
61. `numerology_request_guard`
62. `oracle_card_request_guard`
63. `oracle_lot_request_guard`
64. `past_life_request_guard`
65. `pendulum_request_guard`
66. `pet_communication_request_guard`
67. `physiognomy_request_guard`
68. `planetary_retrograde_request_guard`
69. `psychometry_request_guard`
70. `relationship_luck_request_guard`
71. `ritual_source_guard`
72. `rune_request_guard`
73. `scrying_request_guard`
74. `sigil_request_guard`
75. `sky_omen_request_guard`
76. `sleep_paralysis_request_guard`
77. `sound_cleansing_request_guard`
78. `spirit_message_request_guard`
79. `spiritual_protection_request_guard`
80. `synchronicity_request_guard`
81. `talisman_request_guard`
82. `tasseography_request_guard`
83. `wealth_luck_request_guard`
84. `western_geomancy_request_guard`
85. `yijing_source_reference_guard`
86. `zodiac_request_guard`
87. `almanac_symbol_lookup`
88. `animal_omen_interpretation_planner`
89. `animal_omen_observation_recorder`
90. `animal_omen_symbol_lookup`
91. `aroma_context_recorder`
92. `aroma_practice_planner`
93. `aroma_symbol_lookup`
94. `astrology_chart_record`
95. `astrology_symbol_lookup`
96. `aura_chakra_reflection_planner`
97. `aura_chakra_sensation_recorder`
98. `aura_chakra_symbol_lookup`
99. `bazi_ziwei_chart_record`
100. `bibliomancy_reflection_planner`
101. `bibliomancy_source_recorder`
102. `bibliomancy_symbol_lookup`
103. `body_omen_context_recorder`
104. `body_omen_reflection_planner`
105. `body_omen_symbol_lookup`
106. `candle_interpretation_planner`
107. `candle_observation_recorder`
108. `candle_symbol_lookup`
109. `cartomancy_card_lookup`
110. `cartomancy_draw_recorder`
111. `cartomancy_interpretation_planner`
112. `casting_lots_interpretation_planner`
113. `casting_lots_layout_recorder`
114. `casting_lots_symbol_lookup`
115. `cezi_character_recorder`
116. `cezi_interpretation_planner`
117. `cezi_symbol_lookup`
118. `color_palette_planner`
119. `color_profile_recorder`
120. `color_symbol_lookup`
121. `consecration_care_planner`
122. `consecration_context_recorder`
123. `consecration_symbol_lookup`
124. `crystal_item_recorder`
125. `crystal_symbol_lookup`
126. `crystal_use_planner`
127. `date_constraint_recorder`
128. `date_option_ranker`
129. `deity_ancestor_context_recorder`
130. `deity_ancestor_reflection_planner`
131. `deity_ancestor_symbol_lookup`
132. `dice_interpretation_planner`
133. `dice_roll_recorder`
134. `dice_symbol_lookup`
135. `dowsing_context_recorder`
136. `dowsing_practice_planner`
137. `dowsing_symbol_lookup`
138. `dream_interpretation_planner`
139. `dream_record_builder`
140. `dream_symbol_lookup`
141. `fengshui_bagua_mapper`
142. `fengshui_observation_recorder`
143. `fengshui_recommendation_ranker`
144. `fengshui_space_checklist`
145. `fengshui_yangzhai_case_library`
146. `flower_interpretation_planner`
147. `flower_item_recorder`
148. `flower_symbol_lookup`
149. `folk_custom_lookup`
150. `folk_source_recorder`
151. `folk_taboo_reframer`
152. `herbal_context_recorder`
153. `herbal_practice_planner`
154. `herbal_symbol_lookup`
155. `human_design_chart_recorder`
156. `human_design_interpretation_planner`
157. `human_design_symbol_lookup`
158. `incense_interpretation_planner`
159. `incense_observation_recorder`
160. `incense_symbol_lookup`
161. `lenormand_card_lookup`
162. `lenormand_draw_recorder`
163. `lenormand_interpretation_planner`
164. `liuyao_chart_recorder`
165. `liuyao_focus_selector`
166. `liuyao_symbol_lookup`
167. `lost_object_context_recorder`
168. `lost_object_search_planner`
169. `lost_object_symbol_lookup`
170. `manifestation_intention_recorder`
171. `manifestation_reflection_planner`
172. `manifestation_symbol_lookup`
173. `meihua_casting_recorder`
174. `meihua_omen_recorder`
175. `meihua_relation_interpreter`
176. `meihua_symbol_lookup`
177. `mingli_school_reference`
178. `mingli_symbol_lookup`
179. `moon_phase_context_recorder`
180. `moon_phase_reflection_planner`
181. `moon_phase_symbol_lookup`
182. `naming_brand_scenario_scorer`
183. `naming_candidate_comparator`
184. `naming_symbol_lookup`
185. `nine_star_ki_interpretation_planner`
186. `nine_star_ki_profile_recorder`
187. `nine_star_ki_symbol_lookup`
188. `numerology_interpretation_planner`
189. `numerology_profile_recorder`
190. `numerology_symbol_lookup`
191. `oracle_card_draw_recorder`
192. `oracle_card_interpretation_planner`
193. `oracle_card_symbol_lookup`
194. `oracle_lot_interpretation_planner`
195. `oracle_lot_record_builder`
196. `oracle_lot_symbol_lookup`
197. `past_life_narrative_recorder`
198. `past_life_reflection_planner`
199. `past_life_symbol_lookup`
200. `pendulum_interpretation_planner`
201. `pendulum_session_recorder`
202. `pendulum_symbol_lookup`
203. `pet_communication_context_recorder`
204. `pet_communication_reflection_planner`
205. `pet_communication_symbol_lookup`
206. `physiognomy_interpretation_planner`
207. `physiognomy_observation_recorder`
208. `physiognomy_symbol_lookup`
209. `planetary_retrograde_context_recorder`
210. `planetary_retrograde_reflection_planner`
211. `planetary_retrograde_symbol_lookup`
212. `psychometry_object_recorder`
213. `psychometry_reflection_planner`
214. `psychometry_symbol_lookup`
215. `qimen_chart_record`
216. `qimen_focus_selector`
217. `qimen_school_reference`
218. `relationship_luck_action_planner`
219. `relationship_luck_context_recorder`
220. `relationship_luck_symbol_lookup`
221. `ritual_low_risk_protocol`
222. `ritual_source_example_lookup`
223. `rune_cast_recorder`
224. `rune_interpretation_planner`
225. `rune_symbol_lookup`
226. `scrying_interpretation_planner`
227. `scrying_observation_recorder`
228. `scrying_symbol_lookup`
229. `sigil_context_recorder`
230. `sigil_practice_planner`
231. `sigil_symbol_lookup`
232. `sky_omen_observation_recorder`
233. `sky_omen_reflection_planner`
234. `sky_omen_symbol_lookup`
235. `sleep_paralysis_context_recorder`
236. `sleep_paralysis_reflection_planner`
237. `sleep_paralysis_symbol_lookup`
238. `sound_cleansing_context_recorder`
239. `sound_cleansing_practice_planner`
240. `sound_cleansing_symbol_lookup`
241. `spirit_message_record_builder`
242. `spirit_message_reflection_planner`
243. `spirit_message_symbol_lookup`
244. `spiritual_protection_context_recorder`
245. `spiritual_protection_reflection_planner`
246. `spiritual_protection_symbol_lookup`
247. `synchronicity_event_recorder`
248. `synchronicity_reflection_planner`
249. `synchronicity_symbol_lookup`
250. `talisman_record_builder`
251. `talisman_symbol_lookup`
252. `talisman_use_planner`
253. `tarot_card_lookup`
254. `tarot_combination_planner`
255. `tarot_draw_recorder`
256. `tarot_draw_simulator`
257. `tarot_interpretation_planner`
258. `tarot_spread_selector`
259. `tasseography_interpretation_planner`
260. `tasseography_pattern_recorder`
261. `tasseography_symbol_lookup`
262. `wealth_luck_action_planner`
263. `wealth_luck_context_recorder`
264. `wealth_luck_symbol_lookup`
265. `western_geomancy_chart_recorder`
266. `western_geomancy_figure_lookup`
267. `western_geomancy_interpretation_planner`
268. `yijing_casting_method_advisor`
269. `yijing_casting_simulator`
270. `yijing_hexagram_lookup`
271. `yijing_hexagram_record`
272. `yijing_line_lookup`
273. `zodiac_interpretation_planner`
274. `zodiac_profile_recorder`
275. `zodiac_symbol_lookup`
276. `skill_replay_runner`
277. `skill_transcript_runner`

## Domain Index

### animal_omen
- `animal_omen_interpretation_planner`
- `animal_omen_observation_recorder`
- `animal_omen_request_guard`
- `animal_omen_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### aroma
- `aroma_context_recorder`
- `aroma_practice_planner`
- `aroma_request_guard`
- `aroma_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### astrology
- `astrology_chart_record`
- `astrology_compatibility_guard`
- `astrology_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### aura_chakra
- `aura_chakra_reflection_planner`
- `aura_chakra_request_guard`
- `aura_chakra_sensation_recorder`
- `aura_chakra_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### bibliomancy
- `bibliomancy_reflection_planner`
- `bibliomancy_request_guard`
- `bibliomancy_source_recorder`
- `bibliomancy_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### body_omen
- `body_omen_context_recorder`
- `body_omen_reflection_planner`
- `body_omen_request_guard`
- `body_omen_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### candle
- `candle_interpretation_planner`
- `candle_observation_recorder`
- `candle_request_guard`
- `candle_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### cartomancy
- `cartomancy_card_lookup`
- `cartomancy_draw_recorder`
- `cartomancy_interpretation_planner`
- `cartomancy_request_guard`
- `skill_replay_runner`
- `skill_transcript_runner`

### casting_lots
- `casting_lots_interpretation_planner`
- `casting_lots_layout_recorder`
- `casting_lots_request_guard`
- `casting_lots_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### character_divination
- `cezi_character_recorder`
- `cezi_interpretation_planner`
- `cezi_request_guard`
- `cezi_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### color
- `color_palette_planner`
- `color_profile_recorder`
- `color_request_guard`
- `color_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### consecration
- `consecration_care_planner`
- `consecration_context_recorder`
- `consecration_request_guard`
- `consecration_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### crystal
- `crystal_item_recorder`
- `crystal_request_guard`
- `crystal_symbol_lookup`
- `crystal_use_planner`
- `skill_replay_runner`
- `skill_transcript_runner`

### date_selection
- `almanac_symbol_lookup`
- `date_constraint_recorder`
- `date_option_ranker`
- `date_selection_guard`
- `skill_replay_runner`
- `skill_transcript_runner`

### deity_ancestor
- `deity_ancestor_context_recorder`
- `deity_ancestor_reflection_planner`
- `deity_ancestor_request_guard`
- `deity_ancestor_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### dice
- `dice_interpretation_planner`
- `dice_request_guard`
- `dice_roll_recorder`
- `dice_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### dowsing
- `dowsing_context_recorder`
- `dowsing_practice_planner`
- `dowsing_request_guard`
- `dowsing_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### dream
- `dream_interpretation_planner`
- `dream_record_builder`
- `dream_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### fengshui
- `fengshui_bagua_mapper`
- `fengshui_observation_recorder`
- `fengshui_recommendation_ranker`
- `fengshui_school_guard`
- `fengshui_space_checklist`
- `fengshui_yangzhai_case_library`
- `skill_replay_runner`
- `skill_transcript_runner`

### flower
- `flower_interpretation_planner`
- `flower_item_recorder`
- `flower_request_guard`
- `flower_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### folk_custom
- `folk_custom_lookup`
- `folk_source_recorder`
- `folk_taboo_reframer`
- `skill_replay_runner`
- `skill_transcript_runner`

### herbal
- `herbal_context_recorder`
- `herbal_practice_planner`
- `herbal_request_guard`
- `herbal_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### human_design
- `human_design_chart_recorder`
- `human_design_interpretation_planner`
- `human_design_request_guard`
- `human_design_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### incense
- `incense_interpretation_planner`
- `incense_observation_recorder`
- `incense_request_guard`
- `incense_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### lenormand
- `lenormand_card_lookup`
- `lenormand_draw_recorder`
- `lenormand_interpretation_planner`
- `lenormand_request_guard`
- `skill_replay_runner`
- `skill_transcript_runner`

### liuyao
- `liuyao_chart_recorder`
- `liuyao_focus_selector`
- `liuyao_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### lost_object
- `lost_object_context_recorder`
- `lost_object_request_guard`
- `lost_object_search_planner`
- `lost_object_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### manifestation
- `manifestation_intention_recorder`
- `manifestation_reflection_planner`
- `manifestation_request_guard`
- `manifestation_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### meihua
- `meihua_casting_recorder`
- `meihua_omen_recorder`
- `meihua_relation_interpreter`
- `meihua_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### mingli
- `bazi_ziwei_chart_record`
- `bazi_ziwei_intake_guard`
- `mingli_school_reference`
- `mingli_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### moon_phase
- `moon_phase_context_recorder`
- `moon_phase_reflection_planner`
- `moon_phase_request_guard`
- `moon_phase_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### naming
- `naming_brand_scenario_scorer`
- `naming_candidate_comparator`
- `naming_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### nine_star_ki
- `nine_star_ki_interpretation_planner`
- `nine_star_ki_profile_recorder`
- `nine_star_ki_request_guard`
- `nine_star_ki_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### numerology
- `numerology_interpretation_planner`
- `numerology_profile_recorder`
- `numerology_request_guard`
- `numerology_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### oracle_card
- `oracle_card_draw_recorder`
- `oracle_card_interpretation_planner`
- `oracle_card_request_guard`
- `oracle_card_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### oracle_lot
- `oracle_lot_interpretation_planner`
- `oracle_lot_record_builder`
- `oracle_lot_request_guard`
- `oracle_lot_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### past_life
- `past_life_narrative_recorder`
- `past_life_reflection_planner`
- `past_life_request_guard`
- `past_life_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### pendulum
- `pendulum_interpretation_planner`
- `pendulum_request_guard`
- `pendulum_session_recorder`
- `pendulum_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### pet_communication
- `pet_communication_context_recorder`
- `pet_communication_reflection_planner`
- `pet_communication_request_guard`
- `pet_communication_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### physiognomy
- `physiognomy_interpretation_planner`
- `physiognomy_observation_recorder`
- `physiognomy_request_guard`
- `physiognomy_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### planetary_retrograde
- `planetary_retrograde_context_recorder`
- `planetary_retrograde_reflection_planner`
- `planetary_retrograde_request_guard`
- `planetary_retrograde_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### psychometry
- `psychometry_object_recorder`
- `psychometry_reflection_planner`
- `psychometry_request_guard`
- `psychometry_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### qimen
- `qimen_chart_record`
- `qimen_focus_selector`
- `qimen_method_guard`
- `qimen_school_reference`
- `skill_replay_runner`
- `skill_transcript_runner`

### relationship_luck
- `relationship_luck_action_planner`
- `relationship_luck_context_recorder`
- `relationship_luck_request_guard`
- `relationship_luck_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### ritual
- `ritual_low_risk_protocol`
- `ritual_safety_check`
- `ritual_source_example_lookup`
- `ritual_source_guard`
- `skill_replay_runner`
- `skill_transcript_runner`

### rune
- `rune_cast_recorder`
- `rune_interpretation_planner`
- `rune_request_guard`
- `rune_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### scrying
- `scrying_interpretation_planner`
- `scrying_observation_recorder`
- `scrying_request_guard`
- `scrying_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### shared
- `agent_route_smoke_runner`
- `agent_runtime_dry_run_runner`
- `agent_runtime_handoff_builder`
- `agent_tool_definition_exporter`
- `agent_tool_definition_validator`
- `agent_tool_registry_builder`
- `agent_tool_registry_validator`
- `agent_tool_wrapper_manifest_builder`
- `agent_workflow_router`
- `codex_skill_blueprint_validator`
- `codex_skill_installer`
- `content_review_feedback_recorder`
- `content_review_packet_builder`
- `external_evidence_intake_builder`
- `knowledge_coverage_audit`
- `knowledge_navigation_builder`
- `mystic_intake_triage`
- `mystic_output_lint`
- `paradigm_selector`
- `pilot_readiness_report`
- `release_gate_runner`
- `release_manifest_builder`
- `skill_install_readiness_report`
- `sop_traceability_matrix_builder`
- `symbolic_case_library`
- `symbolic_depth_lookup`
- `tool_manifest_builder`
- `transcript_anonymizer`
- `transcript_fixture_builder`

### sigil
- `sigil_context_recorder`
- `sigil_practice_planner`
- `sigil_request_guard`
- `sigil_symbol_lookup`
- `skill_replay_runner`
- `skill_transcript_runner`

### sky_omen
- `skill_replay_runner`
- `skill_transcript_runner`
- `sky_omen_observation_recorder`
- `sky_omen_reflection_planner`
- `sky_omen_request_guard`
- `sky_omen_symbol_lookup`

### sleep_paralysis
- `skill_replay_runner`
- `skill_transcript_runner`
- `sleep_paralysis_context_recorder`
- `sleep_paralysis_reflection_planner`
- `sleep_paralysis_request_guard`
- `sleep_paralysis_symbol_lookup`

### sound_cleansing
- `skill_replay_runner`
- `skill_transcript_runner`
- `sound_cleansing_context_recorder`
- `sound_cleansing_practice_planner`
- `sound_cleansing_request_guard`
- `sound_cleansing_symbol_lookup`

### spirit_message
- `skill_replay_runner`
- `skill_transcript_runner`
- `spirit_message_record_builder`
- `spirit_message_reflection_planner`
- `spirit_message_request_guard`
- `spirit_message_symbol_lookup`

### spiritual_protection
- `skill_replay_runner`
- `skill_transcript_runner`
- `spiritual_protection_context_recorder`
- `spiritual_protection_reflection_planner`
- `spiritual_protection_request_guard`
- `spiritual_protection_symbol_lookup`

### synchronicity
- `skill_replay_runner`
- `skill_transcript_runner`
- `synchronicity_event_recorder`
- `synchronicity_reflection_planner`
- `synchronicity_request_guard`
- `synchronicity_symbol_lookup`

### talisman
- `skill_replay_runner`
- `skill_transcript_runner`
- `talisman_record_builder`
- `talisman_request_guard`
- `talisman_symbol_lookup`
- `talisman_use_planner`

### tarot
- `skill_replay_runner`
- `skill_transcript_runner`
- `tarot_card_lookup`
- `tarot_combination_planner`
- `tarot_draw_recorder`
- `tarot_draw_simulator`
- `tarot_interpretation_planner`
- `tarot_spread_selector`

### tasseography
- `skill_replay_runner`
- `skill_transcript_runner`
- `tasseography_interpretation_planner`
- `tasseography_pattern_recorder`
- `tasseography_request_guard`
- `tasseography_symbol_lookup`

### wealth_luck
- `skill_replay_runner`
- `skill_transcript_runner`
- `wealth_luck_action_planner`
- `wealth_luck_context_recorder`
- `wealth_luck_request_guard`
- `wealth_luck_symbol_lookup`

### western_geomancy
- `skill_replay_runner`
- `skill_transcript_runner`
- `western_geomancy_chart_recorder`
- `western_geomancy_figure_lookup`
- `western_geomancy_interpretation_planner`
- `western_geomancy_request_guard`

### yijing
- `skill_replay_runner`
- `skill_transcript_runner`
- `yijing_casting_method_advisor`
- `yijing_casting_simulator`
- `yijing_hexagram_lookup`
- `yijing_hexagram_record`
- `yijing_line_lookup`
- `yijing_question_guard`
- `yijing_source_reference_guard`

### zodiac
- `skill_replay_runner`
- `skill_transcript_runner`
- `zodiac_interpretation_planner`
- `zodiac_profile_recorder`
- `zodiac_request_guard`
- `zodiac_symbol_lookup`

## 限制

- 此 registry 不启动工具服务，只提供注册表。
- 注册顺序不能替代 runtime 权限隔离和命令执行沙箱。
- 外部证据未完成前，只能用于 dry-run 或内部试运行。
