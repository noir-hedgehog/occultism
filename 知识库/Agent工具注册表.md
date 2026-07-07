# Agent Tool Registry

本页把已验证的 agent tool definitions 组织成 runtime 注册表，包括注册顺序、按流派索引、按 Skill 索引和安全启动工具。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| 状态 | `ready_for_runtime_registration` |
| Tool | 286 |
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
18. `case_validation_backlog_builder`
19. `case_validation_template_builder`
20. `codex_skill_blueprint_validator`
21. `codex_skill_installer`
22. `consultation_case_recorder`
23. `consultation_execution_runner`
24. `consultation_handoff_builder`
25. `consultation_packet_builder`
26. `content_review_feedback_recorder`
27. `content_review_packet_builder`
28. `domain_evidence_matrix_builder`
29. `external_evidence_intake_builder`
30. `interaction_surface_matrix_builder`
31. `knowledge_coverage_audit`
32. `knowledge_navigation_builder`
33. `paradigm_selector`
34. `pilot_readiness_report`
35. `release_gate_runner`
36. `release_manifest_builder`
37. `skill_install_readiness_report`
38. `sop_traceability_matrix_builder`
39. `symbolic_case_library`
40. `symbolic_depth_lookup`
41. `tool_manifest_builder`
42. `transcript_anonymizer`
43. `transcript_fixture_builder`
44. `web_ui_surface_smoke_runner`
45. `animal_omen_request_guard`
46. `aroma_request_guard`
47. `aura_chakra_request_guard`
48. `bibliomancy_request_guard`
49. `body_omen_request_guard`
50. `candle_request_guard`
51. `cartomancy_request_guard`
52. `casting_lots_request_guard`
53. `cezi_request_guard`
54. `color_request_guard`
55. `consecration_request_guard`
56. `crystal_request_guard`
57. `date_selection_guard`
58. `deity_ancestor_request_guard`
59. `dice_request_guard`
60. `dowsing_request_guard`
61. `flower_request_guard`
62. `herbal_request_guard`
63. `human_design_request_guard`
64. `incense_request_guard`
65. `lenormand_request_guard`
66. `lost_object_request_guard`
67. `manifestation_request_guard`
68. `moon_phase_request_guard`
69. `nine_star_ki_request_guard`
70. `numerology_request_guard`
71. `oracle_card_request_guard`
72. `oracle_lot_request_guard`
73. `past_life_request_guard`
74. `pendulum_request_guard`
75. `pet_communication_request_guard`
76. `physiognomy_request_guard`
77. `planetary_retrograde_request_guard`
78. `psychometry_request_guard`
79. `relationship_luck_request_guard`
80. `ritual_source_guard`
81. `rune_request_guard`
82. `scrying_request_guard`
83. `sigil_request_guard`
84. `sky_omen_request_guard`
85. `sleep_paralysis_request_guard`
86. `sound_cleansing_request_guard`
87. `spirit_message_request_guard`
88. `spiritual_protection_request_guard`
89. `synchronicity_request_guard`
90. `talisman_request_guard`
91. `tasseography_request_guard`
92. `wealth_luck_request_guard`
93. `western_geomancy_request_guard`
94. `yijing_source_reference_guard`
95. `zodiac_request_guard`
96. `almanac_symbol_lookup`
97. `animal_omen_interpretation_planner`
98. `animal_omen_observation_recorder`
99. `animal_omen_symbol_lookup`
100. `aroma_context_recorder`
101. `aroma_practice_planner`
102. `aroma_symbol_lookup`
103. `astrology_chart_record`
104. `astrology_symbol_lookup`
105. `aura_chakra_reflection_planner`
106. `aura_chakra_sensation_recorder`
107. `aura_chakra_symbol_lookup`
108. `bazi_ziwei_chart_record`
109. `bibliomancy_reflection_planner`
110. `bibliomancy_source_recorder`
111. `bibliomancy_symbol_lookup`
112. `body_omen_context_recorder`
113. `body_omen_reflection_planner`
114. `body_omen_symbol_lookup`
115. `candle_interpretation_planner`
116. `candle_observation_recorder`
117. `candle_symbol_lookup`
118. `cartomancy_card_lookup`
119. `cartomancy_draw_recorder`
120. `cartomancy_interpretation_planner`
121. `casting_lots_interpretation_planner`
122. `casting_lots_layout_recorder`
123. `casting_lots_symbol_lookup`
124. `cezi_character_recorder`
125. `cezi_interpretation_planner`
126. `cezi_symbol_lookup`
127. `color_palette_planner`
128. `color_profile_recorder`
129. `color_symbol_lookup`
130. `consecration_care_planner`
131. `consecration_context_recorder`
132. `consecration_symbol_lookup`
133. `crystal_item_recorder`
134. `crystal_symbol_lookup`
135. `crystal_use_planner`
136. `date_constraint_recorder`
137. `date_option_ranker`
138. `deity_ancestor_context_recorder`
139. `deity_ancestor_reflection_planner`
140. `deity_ancestor_symbol_lookup`
141. `dice_interpretation_planner`
142. `dice_roll_recorder`
143. `dice_symbol_lookup`
144. `dowsing_context_recorder`
145. `dowsing_practice_planner`
146. `dowsing_symbol_lookup`
147. `dream_interpretation_planner`
148. `dream_record_builder`
149. `dream_symbol_lookup`
150. `fengshui_bagua_mapper`
151. `fengshui_observation_recorder`
152. `fengshui_recommendation_ranker`
153. `fengshui_space_checklist`
154. `fengshui_yangzhai_case_library`
155. `flower_interpretation_planner`
156. `flower_item_recorder`
157. `flower_symbol_lookup`
158. `folk_custom_lookup`
159. `folk_source_recorder`
160. `folk_taboo_reframer`
161. `herbal_context_recorder`
162. `herbal_practice_planner`
163. `herbal_symbol_lookup`
164. `human_design_chart_recorder`
165. `human_design_interpretation_planner`
166. `human_design_symbol_lookup`
167. `incense_interpretation_planner`
168. `incense_observation_recorder`
169. `incense_symbol_lookup`
170. `lenormand_card_lookup`
171. `lenormand_draw_recorder`
172. `lenormand_interpretation_planner`
173. `liuyao_chart_recorder`
174. `liuyao_focus_selector`
175. `liuyao_symbol_lookup`
176. `lost_object_context_recorder`
177. `lost_object_search_planner`
178. `lost_object_symbol_lookup`
179. `manifestation_intention_recorder`
180. `manifestation_reflection_planner`
181. `manifestation_symbol_lookup`
182. `meihua_casting_recorder`
183. `meihua_omen_recorder`
184. `meihua_relation_interpreter`
185. `meihua_symbol_lookup`
186. `mingli_school_reference`
187. `mingli_symbol_lookup`
188. `moon_phase_context_recorder`
189. `moon_phase_reflection_planner`
190. `moon_phase_symbol_lookup`
191. `naming_brand_scenario_scorer`
192. `naming_candidate_comparator`
193. `naming_symbol_lookup`
194. `nine_star_ki_interpretation_planner`
195. `nine_star_ki_profile_recorder`
196. `nine_star_ki_symbol_lookup`
197. `numerology_interpretation_planner`
198. `numerology_profile_recorder`
199. `numerology_symbol_lookup`
200. `oracle_card_draw_recorder`
201. `oracle_card_interpretation_planner`
202. `oracle_card_symbol_lookup`
203. `oracle_lot_interpretation_planner`
204. `oracle_lot_record_builder`
205. `oracle_lot_symbol_lookup`
206. `past_life_narrative_recorder`
207. `past_life_reflection_planner`
208. `past_life_symbol_lookup`
209. `pendulum_interpretation_planner`
210. `pendulum_session_recorder`
211. `pendulum_symbol_lookup`
212. `pet_communication_context_recorder`
213. `pet_communication_reflection_planner`
214. `pet_communication_symbol_lookup`
215. `physiognomy_interpretation_planner`
216. `physiognomy_observation_recorder`
217. `physiognomy_symbol_lookup`
218. `planetary_retrograde_context_recorder`
219. `planetary_retrograde_reflection_planner`
220. `planetary_retrograde_symbol_lookup`
221. `psychometry_object_recorder`
222. `psychometry_reflection_planner`
223. `psychometry_symbol_lookup`
224. `qimen_chart_record`
225. `qimen_focus_selector`
226. `qimen_school_reference`
227. `relationship_luck_action_planner`
228. `relationship_luck_context_recorder`
229. `relationship_luck_symbol_lookup`
230. `ritual_low_risk_protocol`
231. `ritual_source_example_lookup`
232. `rune_cast_recorder`
233. `rune_interpretation_planner`
234. `rune_symbol_lookup`
235. `scrying_interpretation_planner`
236. `scrying_observation_recorder`
237. `scrying_symbol_lookup`
238. `sigil_context_recorder`
239. `sigil_practice_planner`
240. `sigil_symbol_lookup`
241. `sky_omen_observation_recorder`
242. `sky_omen_reflection_planner`
243. `sky_omen_symbol_lookup`
244. `sleep_paralysis_context_recorder`
245. `sleep_paralysis_reflection_planner`
246. `sleep_paralysis_symbol_lookup`
247. `sound_cleansing_context_recorder`
248. `sound_cleansing_practice_planner`
249. `sound_cleansing_symbol_lookup`
250. `spirit_message_record_builder`
251. `spirit_message_reflection_planner`
252. `spirit_message_symbol_lookup`
253. `spiritual_protection_context_recorder`
254. `spiritual_protection_reflection_planner`
255. `spiritual_protection_symbol_lookup`
256. `synchronicity_event_recorder`
257. `synchronicity_reflection_planner`
258. `synchronicity_symbol_lookup`
259. `talisman_record_builder`
260. `talisman_symbol_lookup`
261. `talisman_use_planner`
262. `tarot_card_lookup`
263. `tarot_combination_planner`
264. `tarot_draw_recorder`
265. `tarot_draw_simulator`
266. `tarot_interpretation_planner`
267. `tarot_spread_selector`
268. `tasseography_interpretation_planner`
269. `tasseography_pattern_recorder`
270. `tasseography_symbol_lookup`
271. `wealth_luck_action_planner`
272. `wealth_luck_context_recorder`
273. `wealth_luck_symbol_lookup`
274. `western_geomancy_chart_recorder`
275. `western_geomancy_figure_lookup`
276. `western_geomancy_interpretation_planner`
277. `yijing_casting_method_advisor`
278. `yijing_casting_simulator`
279. `yijing_hexagram_lookup`
280. `yijing_hexagram_record`
281. `yijing_line_lookup`
282. `zodiac_interpretation_planner`
283. `zodiac_profile_recorder`
284. `zodiac_symbol_lookup`
285. `skill_replay_runner`
286. `skill_transcript_runner`

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
- `case_validation_backlog_builder`
- `case_validation_template_builder`
- `codex_skill_blueprint_validator`
- `codex_skill_installer`
- `consultation_case_recorder`
- `consultation_execution_runner`
- `consultation_handoff_builder`
- `consultation_packet_builder`
- `content_review_feedback_recorder`
- `content_review_packet_builder`
- `domain_evidence_matrix_builder`
- `external_evidence_intake_builder`
- `interaction_surface_matrix_builder`
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
- `web_ui_surface_smoke_runner`

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
