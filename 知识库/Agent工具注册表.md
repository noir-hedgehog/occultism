# Agent Tool Registry

本页把已验证的 agent tool definitions 组织成 runtime 注册表，包括注册顺序、按流派索引、按 Skill 索引和安全启动工具。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| 状态 | `ready_for_runtime_registration` |
| Tool | 284 |
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
30. `knowledge_coverage_audit`
31. `knowledge_navigation_builder`
32. `paradigm_selector`
33. `pilot_readiness_report`
34. `release_gate_runner`
35. `release_manifest_builder`
36. `skill_install_readiness_report`
37. `sop_traceability_matrix_builder`
38. `symbolic_case_library`
39. `symbolic_depth_lookup`
40. `tool_manifest_builder`
41. `transcript_anonymizer`
42. `transcript_fixture_builder`
43. `animal_omen_request_guard`
44. `aroma_request_guard`
45. `aura_chakra_request_guard`
46. `bibliomancy_request_guard`
47. `body_omen_request_guard`
48. `candle_request_guard`
49. `cartomancy_request_guard`
50. `casting_lots_request_guard`
51. `cezi_request_guard`
52. `color_request_guard`
53. `consecration_request_guard`
54. `crystal_request_guard`
55. `date_selection_guard`
56. `deity_ancestor_request_guard`
57. `dice_request_guard`
58. `dowsing_request_guard`
59. `flower_request_guard`
60. `herbal_request_guard`
61. `human_design_request_guard`
62. `incense_request_guard`
63. `lenormand_request_guard`
64. `lost_object_request_guard`
65. `manifestation_request_guard`
66. `moon_phase_request_guard`
67. `nine_star_ki_request_guard`
68. `numerology_request_guard`
69. `oracle_card_request_guard`
70. `oracle_lot_request_guard`
71. `past_life_request_guard`
72. `pendulum_request_guard`
73. `pet_communication_request_guard`
74. `physiognomy_request_guard`
75. `planetary_retrograde_request_guard`
76. `psychometry_request_guard`
77. `relationship_luck_request_guard`
78. `ritual_source_guard`
79. `rune_request_guard`
80. `scrying_request_guard`
81. `sigil_request_guard`
82. `sky_omen_request_guard`
83. `sleep_paralysis_request_guard`
84. `sound_cleansing_request_guard`
85. `spirit_message_request_guard`
86. `spiritual_protection_request_guard`
87. `synchronicity_request_guard`
88. `talisman_request_guard`
89. `tasseography_request_guard`
90. `wealth_luck_request_guard`
91. `western_geomancy_request_guard`
92. `yijing_source_reference_guard`
93. `zodiac_request_guard`
94. `almanac_symbol_lookup`
95. `animal_omen_interpretation_planner`
96. `animal_omen_observation_recorder`
97. `animal_omen_symbol_lookup`
98. `aroma_context_recorder`
99. `aroma_practice_planner`
100. `aroma_symbol_lookup`
101. `astrology_chart_record`
102. `astrology_symbol_lookup`
103. `aura_chakra_reflection_planner`
104. `aura_chakra_sensation_recorder`
105. `aura_chakra_symbol_lookup`
106. `bazi_ziwei_chart_record`
107. `bibliomancy_reflection_planner`
108. `bibliomancy_source_recorder`
109. `bibliomancy_symbol_lookup`
110. `body_omen_context_recorder`
111. `body_omen_reflection_planner`
112. `body_omen_symbol_lookup`
113. `candle_interpretation_planner`
114. `candle_observation_recorder`
115. `candle_symbol_lookup`
116. `cartomancy_card_lookup`
117. `cartomancy_draw_recorder`
118. `cartomancy_interpretation_planner`
119. `casting_lots_interpretation_planner`
120. `casting_lots_layout_recorder`
121. `casting_lots_symbol_lookup`
122. `cezi_character_recorder`
123. `cezi_interpretation_planner`
124. `cezi_symbol_lookup`
125. `color_palette_planner`
126. `color_profile_recorder`
127. `color_symbol_lookup`
128. `consecration_care_planner`
129. `consecration_context_recorder`
130. `consecration_symbol_lookup`
131. `crystal_item_recorder`
132. `crystal_symbol_lookup`
133. `crystal_use_planner`
134. `date_constraint_recorder`
135. `date_option_ranker`
136. `deity_ancestor_context_recorder`
137. `deity_ancestor_reflection_planner`
138. `deity_ancestor_symbol_lookup`
139. `dice_interpretation_planner`
140. `dice_roll_recorder`
141. `dice_symbol_lookup`
142. `dowsing_context_recorder`
143. `dowsing_practice_planner`
144. `dowsing_symbol_lookup`
145. `dream_interpretation_planner`
146. `dream_record_builder`
147. `dream_symbol_lookup`
148. `fengshui_bagua_mapper`
149. `fengshui_observation_recorder`
150. `fengshui_recommendation_ranker`
151. `fengshui_space_checklist`
152. `fengshui_yangzhai_case_library`
153. `flower_interpretation_planner`
154. `flower_item_recorder`
155. `flower_symbol_lookup`
156. `folk_custom_lookup`
157. `folk_source_recorder`
158. `folk_taboo_reframer`
159. `herbal_context_recorder`
160. `herbal_practice_planner`
161. `herbal_symbol_lookup`
162. `human_design_chart_recorder`
163. `human_design_interpretation_planner`
164. `human_design_symbol_lookup`
165. `incense_interpretation_planner`
166. `incense_observation_recorder`
167. `incense_symbol_lookup`
168. `lenormand_card_lookup`
169. `lenormand_draw_recorder`
170. `lenormand_interpretation_planner`
171. `liuyao_chart_recorder`
172. `liuyao_focus_selector`
173. `liuyao_symbol_lookup`
174. `lost_object_context_recorder`
175. `lost_object_search_planner`
176. `lost_object_symbol_lookup`
177. `manifestation_intention_recorder`
178. `manifestation_reflection_planner`
179. `manifestation_symbol_lookup`
180. `meihua_casting_recorder`
181. `meihua_omen_recorder`
182. `meihua_relation_interpreter`
183. `meihua_symbol_lookup`
184. `mingli_school_reference`
185. `mingli_symbol_lookup`
186. `moon_phase_context_recorder`
187. `moon_phase_reflection_planner`
188. `moon_phase_symbol_lookup`
189. `naming_brand_scenario_scorer`
190. `naming_candidate_comparator`
191. `naming_symbol_lookup`
192. `nine_star_ki_interpretation_planner`
193. `nine_star_ki_profile_recorder`
194. `nine_star_ki_symbol_lookup`
195. `numerology_interpretation_planner`
196. `numerology_profile_recorder`
197. `numerology_symbol_lookup`
198. `oracle_card_draw_recorder`
199. `oracle_card_interpretation_planner`
200. `oracle_card_symbol_lookup`
201. `oracle_lot_interpretation_planner`
202. `oracle_lot_record_builder`
203. `oracle_lot_symbol_lookup`
204. `past_life_narrative_recorder`
205. `past_life_reflection_planner`
206. `past_life_symbol_lookup`
207. `pendulum_interpretation_planner`
208. `pendulum_session_recorder`
209. `pendulum_symbol_lookup`
210. `pet_communication_context_recorder`
211. `pet_communication_reflection_planner`
212. `pet_communication_symbol_lookup`
213. `physiognomy_interpretation_planner`
214. `physiognomy_observation_recorder`
215. `physiognomy_symbol_lookup`
216. `planetary_retrograde_context_recorder`
217. `planetary_retrograde_reflection_planner`
218. `planetary_retrograde_symbol_lookup`
219. `psychometry_object_recorder`
220. `psychometry_reflection_planner`
221. `psychometry_symbol_lookup`
222. `qimen_chart_record`
223. `qimen_focus_selector`
224. `qimen_school_reference`
225. `relationship_luck_action_planner`
226. `relationship_luck_context_recorder`
227. `relationship_luck_symbol_lookup`
228. `ritual_low_risk_protocol`
229. `ritual_source_example_lookup`
230. `rune_cast_recorder`
231. `rune_interpretation_planner`
232. `rune_symbol_lookup`
233. `scrying_interpretation_planner`
234. `scrying_observation_recorder`
235. `scrying_symbol_lookup`
236. `sigil_context_recorder`
237. `sigil_practice_planner`
238. `sigil_symbol_lookup`
239. `sky_omen_observation_recorder`
240. `sky_omen_reflection_planner`
241. `sky_omen_symbol_lookup`
242. `sleep_paralysis_context_recorder`
243. `sleep_paralysis_reflection_planner`
244. `sleep_paralysis_symbol_lookup`
245. `sound_cleansing_context_recorder`
246. `sound_cleansing_practice_planner`
247. `sound_cleansing_symbol_lookup`
248. `spirit_message_record_builder`
249. `spirit_message_reflection_planner`
250. `spirit_message_symbol_lookup`
251. `spiritual_protection_context_recorder`
252. `spiritual_protection_reflection_planner`
253. `spiritual_protection_symbol_lookup`
254. `synchronicity_event_recorder`
255. `synchronicity_reflection_planner`
256. `synchronicity_symbol_lookup`
257. `talisman_record_builder`
258. `talisman_symbol_lookup`
259. `talisman_use_planner`
260. `tarot_card_lookup`
261. `tarot_combination_planner`
262. `tarot_draw_recorder`
263. `tarot_draw_simulator`
264. `tarot_interpretation_planner`
265. `tarot_spread_selector`
266. `tasseography_interpretation_planner`
267. `tasseography_pattern_recorder`
268. `tasseography_symbol_lookup`
269. `wealth_luck_action_planner`
270. `wealth_luck_context_recorder`
271. `wealth_luck_symbol_lookup`
272. `western_geomancy_chart_recorder`
273. `western_geomancy_figure_lookup`
274. `western_geomancy_interpretation_planner`
275. `yijing_casting_method_advisor`
276. `yijing_casting_simulator`
277. `yijing_hexagram_lookup`
278. `yijing_hexagram_record`
279. `yijing_line_lookup`
280. `zodiac_interpretation_planner`
281. `zodiac_profile_recorder`
282. `zodiac_symbol_lookup`
283. `skill_replay_runner`
284. `skill_transcript_runner`

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
