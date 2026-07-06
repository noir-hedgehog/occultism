# Agent Tool Registry

本页把已验证的 agent tool definitions 组织成 runtime 注册表，包括注册顺序、按流派索引、按 Skill 索引和安全启动工具。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| 状态 | `ready_for_runtime_registration` |
| Tool | 280 |
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
20. `consultation_case_recorder`
21. `consultation_handoff_builder`
22. `consultation_packet_builder`
23. `content_review_feedback_recorder`
24. `content_review_packet_builder`
25. `external_evidence_intake_builder`
26. `knowledge_coverage_audit`
27. `knowledge_navigation_builder`
28. `paradigm_selector`
29. `pilot_readiness_report`
30. `release_gate_runner`
31. `release_manifest_builder`
32. `skill_install_readiness_report`
33. `sop_traceability_matrix_builder`
34. `symbolic_case_library`
35. `symbolic_depth_lookup`
36. `tool_manifest_builder`
37. `transcript_anonymizer`
38. `transcript_fixture_builder`
39. `animal_omen_request_guard`
40. `aroma_request_guard`
41. `aura_chakra_request_guard`
42. `bibliomancy_request_guard`
43. `body_omen_request_guard`
44. `candle_request_guard`
45. `cartomancy_request_guard`
46. `casting_lots_request_guard`
47. `cezi_request_guard`
48. `color_request_guard`
49. `consecration_request_guard`
50. `crystal_request_guard`
51. `date_selection_guard`
52. `deity_ancestor_request_guard`
53. `dice_request_guard`
54. `dowsing_request_guard`
55. `flower_request_guard`
56. `herbal_request_guard`
57. `human_design_request_guard`
58. `incense_request_guard`
59. `lenormand_request_guard`
60. `lost_object_request_guard`
61. `manifestation_request_guard`
62. `moon_phase_request_guard`
63. `nine_star_ki_request_guard`
64. `numerology_request_guard`
65. `oracle_card_request_guard`
66. `oracle_lot_request_guard`
67. `past_life_request_guard`
68. `pendulum_request_guard`
69. `pet_communication_request_guard`
70. `physiognomy_request_guard`
71. `planetary_retrograde_request_guard`
72. `psychometry_request_guard`
73. `relationship_luck_request_guard`
74. `ritual_source_guard`
75. `rune_request_guard`
76. `scrying_request_guard`
77. `sigil_request_guard`
78. `sky_omen_request_guard`
79. `sleep_paralysis_request_guard`
80. `sound_cleansing_request_guard`
81. `spirit_message_request_guard`
82. `spiritual_protection_request_guard`
83. `synchronicity_request_guard`
84. `talisman_request_guard`
85. `tasseography_request_guard`
86. `wealth_luck_request_guard`
87. `western_geomancy_request_guard`
88. `yijing_source_reference_guard`
89. `zodiac_request_guard`
90. `almanac_symbol_lookup`
91. `animal_omen_interpretation_planner`
92. `animal_omen_observation_recorder`
93. `animal_omen_symbol_lookup`
94. `aroma_context_recorder`
95. `aroma_practice_planner`
96. `aroma_symbol_lookup`
97. `astrology_chart_record`
98. `astrology_symbol_lookup`
99. `aura_chakra_reflection_planner`
100. `aura_chakra_sensation_recorder`
101. `aura_chakra_symbol_lookup`
102. `bazi_ziwei_chart_record`
103. `bibliomancy_reflection_planner`
104. `bibliomancy_source_recorder`
105. `bibliomancy_symbol_lookup`
106. `body_omen_context_recorder`
107. `body_omen_reflection_planner`
108. `body_omen_symbol_lookup`
109. `candle_interpretation_planner`
110. `candle_observation_recorder`
111. `candle_symbol_lookup`
112. `cartomancy_card_lookup`
113. `cartomancy_draw_recorder`
114. `cartomancy_interpretation_planner`
115. `casting_lots_interpretation_planner`
116. `casting_lots_layout_recorder`
117. `casting_lots_symbol_lookup`
118. `cezi_character_recorder`
119. `cezi_interpretation_planner`
120. `cezi_symbol_lookup`
121. `color_palette_planner`
122. `color_profile_recorder`
123. `color_symbol_lookup`
124. `consecration_care_planner`
125. `consecration_context_recorder`
126. `consecration_symbol_lookup`
127. `crystal_item_recorder`
128. `crystal_symbol_lookup`
129. `crystal_use_planner`
130. `date_constraint_recorder`
131. `date_option_ranker`
132. `deity_ancestor_context_recorder`
133. `deity_ancestor_reflection_planner`
134. `deity_ancestor_symbol_lookup`
135. `dice_interpretation_planner`
136. `dice_roll_recorder`
137. `dice_symbol_lookup`
138. `dowsing_context_recorder`
139. `dowsing_practice_planner`
140. `dowsing_symbol_lookup`
141. `dream_interpretation_planner`
142. `dream_record_builder`
143. `dream_symbol_lookup`
144. `fengshui_bagua_mapper`
145. `fengshui_observation_recorder`
146. `fengshui_recommendation_ranker`
147. `fengshui_space_checklist`
148. `fengshui_yangzhai_case_library`
149. `flower_interpretation_planner`
150. `flower_item_recorder`
151. `flower_symbol_lookup`
152. `folk_custom_lookup`
153. `folk_source_recorder`
154. `folk_taboo_reframer`
155. `herbal_context_recorder`
156. `herbal_practice_planner`
157. `herbal_symbol_lookup`
158. `human_design_chart_recorder`
159. `human_design_interpretation_planner`
160. `human_design_symbol_lookup`
161. `incense_interpretation_planner`
162. `incense_observation_recorder`
163. `incense_symbol_lookup`
164. `lenormand_card_lookup`
165. `lenormand_draw_recorder`
166. `lenormand_interpretation_planner`
167. `liuyao_chart_recorder`
168. `liuyao_focus_selector`
169. `liuyao_symbol_lookup`
170. `lost_object_context_recorder`
171. `lost_object_search_planner`
172. `lost_object_symbol_lookup`
173. `manifestation_intention_recorder`
174. `manifestation_reflection_planner`
175. `manifestation_symbol_lookup`
176. `meihua_casting_recorder`
177. `meihua_omen_recorder`
178. `meihua_relation_interpreter`
179. `meihua_symbol_lookup`
180. `mingli_school_reference`
181. `mingli_symbol_lookup`
182. `moon_phase_context_recorder`
183. `moon_phase_reflection_planner`
184. `moon_phase_symbol_lookup`
185. `naming_brand_scenario_scorer`
186. `naming_candidate_comparator`
187. `naming_symbol_lookup`
188. `nine_star_ki_interpretation_planner`
189. `nine_star_ki_profile_recorder`
190. `nine_star_ki_symbol_lookup`
191. `numerology_interpretation_planner`
192. `numerology_profile_recorder`
193. `numerology_symbol_lookup`
194. `oracle_card_draw_recorder`
195. `oracle_card_interpretation_planner`
196. `oracle_card_symbol_lookup`
197. `oracle_lot_interpretation_planner`
198. `oracle_lot_record_builder`
199. `oracle_lot_symbol_lookup`
200. `past_life_narrative_recorder`
201. `past_life_reflection_planner`
202. `past_life_symbol_lookup`
203. `pendulum_interpretation_planner`
204. `pendulum_session_recorder`
205. `pendulum_symbol_lookup`
206. `pet_communication_context_recorder`
207. `pet_communication_reflection_planner`
208. `pet_communication_symbol_lookup`
209. `physiognomy_interpretation_planner`
210. `physiognomy_observation_recorder`
211. `physiognomy_symbol_lookup`
212. `planetary_retrograde_context_recorder`
213. `planetary_retrograde_reflection_planner`
214. `planetary_retrograde_symbol_lookup`
215. `psychometry_object_recorder`
216. `psychometry_reflection_planner`
217. `psychometry_symbol_lookup`
218. `qimen_chart_record`
219. `qimen_focus_selector`
220. `qimen_school_reference`
221. `relationship_luck_action_planner`
222. `relationship_luck_context_recorder`
223. `relationship_luck_symbol_lookup`
224. `ritual_low_risk_protocol`
225. `ritual_source_example_lookup`
226. `rune_cast_recorder`
227. `rune_interpretation_planner`
228. `rune_symbol_lookup`
229. `scrying_interpretation_planner`
230. `scrying_observation_recorder`
231. `scrying_symbol_lookup`
232. `sigil_context_recorder`
233. `sigil_practice_planner`
234. `sigil_symbol_lookup`
235. `sky_omen_observation_recorder`
236. `sky_omen_reflection_planner`
237. `sky_omen_symbol_lookup`
238. `sleep_paralysis_context_recorder`
239. `sleep_paralysis_reflection_planner`
240. `sleep_paralysis_symbol_lookup`
241. `sound_cleansing_context_recorder`
242. `sound_cleansing_practice_planner`
243. `sound_cleansing_symbol_lookup`
244. `spirit_message_record_builder`
245. `spirit_message_reflection_planner`
246. `spirit_message_symbol_lookup`
247. `spiritual_protection_context_recorder`
248. `spiritual_protection_reflection_planner`
249. `spiritual_protection_symbol_lookup`
250. `synchronicity_event_recorder`
251. `synchronicity_reflection_planner`
252. `synchronicity_symbol_lookup`
253. `talisman_record_builder`
254. `talisman_symbol_lookup`
255. `talisman_use_planner`
256. `tarot_card_lookup`
257. `tarot_combination_planner`
258. `tarot_draw_recorder`
259. `tarot_draw_simulator`
260. `tarot_interpretation_planner`
261. `tarot_spread_selector`
262. `tasseography_interpretation_planner`
263. `tasseography_pattern_recorder`
264. `tasseography_symbol_lookup`
265. `wealth_luck_action_planner`
266. `wealth_luck_context_recorder`
267. `wealth_luck_symbol_lookup`
268. `western_geomancy_chart_recorder`
269. `western_geomancy_figure_lookup`
270. `western_geomancy_interpretation_planner`
271. `yijing_casting_method_advisor`
272. `yijing_casting_simulator`
273. `yijing_hexagram_lookup`
274. `yijing_hexagram_record`
275. `yijing_line_lookup`
276. `zodiac_interpretation_planner`
277. `zodiac_profile_recorder`
278. `zodiac_symbol_lookup`
279. `skill_replay_runner`
280. `skill_transcript_runner`

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
- `consultation_case_recorder`
- `consultation_handoff_builder`
- `consultation_packet_builder`
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
