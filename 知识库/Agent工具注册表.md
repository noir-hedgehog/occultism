# Agent Tool Registry

本页把已验证的 agent tool definitions 组织成 runtime 注册表，包括注册顺序、按流派索引、按 Skill 索引和安全启动工具。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| 状态 | `ready_for_runtime_registration` |
| Tool | 281 |
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
25. `domain_evidence_matrix_builder`
26. `external_evidence_intake_builder`
27. `knowledge_coverage_audit`
28. `knowledge_navigation_builder`
29. `paradigm_selector`
30. `pilot_readiness_report`
31. `release_gate_runner`
32. `release_manifest_builder`
33. `skill_install_readiness_report`
34. `sop_traceability_matrix_builder`
35. `symbolic_case_library`
36. `symbolic_depth_lookup`
37. `tool_manifest_builder`
38. `transcript_anonymizer`
39. `transcript_fixture_builder`
40. `animal_omen_request_guard`
41. `aroma_request_guard`
42. `aura_chakra_request_guard`
43. `bibliomancy_request_guard`
44. `body_omen_request_guard`
45. `candle_request_guard`
46. `cartomancy_request_guard`
47. `casting_lots_request_guard`
48. `cezi_request_guard`
49. `color_request_guard`
50. `consecration_request_guard`
51. `crystal_request_guard`
52. `date_selection_guard`
53. `deity_ancestor_request_guard`
54. `dice_request_guard`
55. `dowsing_request_guard`
56. `flower_request_guard`
57. `herbal_request_guard`
58. `human_design_request_guard`
59. `incense_request_guard`
60. `lenormand_request_guard`
61. `lost_object_request_guard`
62. `manifestation_request_guard`
63. `moon_phase_request_guard`
64. `nine_star_ki_request_guard`
65. `numerology_request_guard`
66. `oracle_card_request_guard`
67. `oracle_lot_request_guard`
68. `past_life_request_guard`
69. `pendulum_request_guard`
70. `pet_communication_request_guard`
71. `physiognomy_request_guard`
72. `planetary_retrograde_request_guard`
73. `psychometry_request_guard`
74. `relationship_luck_request_guard`
75. `ritual_source_guard`
76. `rune_request_guard`
77. `scrying_request_guard`
78. `sigil_request_guard`
79. `sky_omen_request_guard`
80. `sleep_paralysis_request_guard`
81. `sound_cleansing_request_guard`
82. `spirit_message_request_guard`
83. `spiritual_protection_request_guard`
84. `synchronicity_request_guard`
85. `talisman_request_guard`
86. `tasseography_request_guard`
87. `wealth_luck_request_guard`
88. `western_geomancy_request_guard`
89. `yijing_source_reference_guard`
90. `zodiac_request_guard`
91. `almanac_symbol_lookup`
92. `animal_omen_interpretation_planner`
93. `animal_omen_observation_recorder`
94. `animal_omen_symbol_lookup`
95. `aroma_context_recorder`
96. `aroma_practice_planner`
97. `aroma_symbol_lookup`
98. `astrology_chart_record`
99. `astrology_symbol_lookup`
100. `aura_chakra_reflection_planner`
101. `aura_chakra_sensation_recorder`
102. `aura_chakra_symbol_lookup`
103. `bazi_ziwei_chart_record`
104. `bibliomancy_reflection_planner`
105. `bibliomancy_source_recorder`
106. `bibliomancy_symbol_lookup`
107. `body_omen_context_recorder`
108. `body_omen_reflection_planner`
109. `body_omen_symbol_lookup`
110. `candle_interpretation_planner`
111. `candle_observation_recorder`
112. `candle_symbol_lookup`
113. `cartomancy_card_lookup`
114. `cartomancy_draw_recorder`
115. `cartomancy_interpretation_planner`
116. `casting_lots_interpretation_planner`
117. `casting_lots_layout_recorder`
118. `casting_lots_symbol_lookup`
119. `cezi_character_recorder`
120. `cezi_interpretation_planner`
121. `cezi_symbol_lookup`
122. `color_palette_planner`
123. `color_profile_recorder`
124. `color_symbol_lookup`
125. `consecration_care_planner`
126. `consecration_context_recorder`
127. `consecration_symbol_lookup`
128. `crystal_item_recorder`
129. `crystal_symbol_lookup`
130. `crystal_use_planner`
131. `date_constraint_recorder`
132. `date_option_ranker`
133. `deity_ancestor_context_recorder`
134. `deity_ancestor_reflection_planner`
135. `deity_ancestor_symbol_lookup`
136. `dice_interpretation_planner`
137. `dice_roll_recorder`
138. `dice_symbol_lookup`
139. `dowsing_context_recorder`
140. `dowsing_practice_planner`
141. `dowsing_symbol_lookup`
142. `dream_interpretation_planner`
143. `dream_record_builder`
144. `dream_symbol_lookup`
145. `fengshui_bagua_mapper`
146. `fengshui_observation_recorder`
147. `fengshui_recommendation_ranker`
148. `fengshui_space_checklist`
149. `fengshui_yangzhai_case_library`
150. `flower_interpretation_planner`
151. `flower_item_recorder`
152. `flower_symbol_lookup`
153. `folk_custom_lookup`
154. `folk_source_recorder`
155. `folk_taboo_reframer`
156. `herbal_context_recorder`
157. `herbal_practice_planner`
158. `herbal_symbol_lookup`
159. `human_design_chart_recorder`
160. `human_design_interpretation_planner`
161. `human_design_symbol_lookup`
162. `incense_interpretation_planner`
163. `incense_observation_recorder`
164. `incense_symbol_lookup`
165. `lenormand_card_lookup`
166. `lenormand_draw_recorder`
167. `lenormand_interpretation_planner`
168. `liuyao_chart_recorder`
169. `liuyao_focus_selector`
170. `liuyao_symbol_lookup`
171. `lost_object_context_recorder`
172. `lost_object_search_planner`
173. `lost_object_symbol_lookup`
174. `manifestation_intention_recorder`
175. `manifestation_reflection_planner`
176. `manifestation_symbol_lookup`
177. `meihua_casting_recorder`
178. `meihua_omen_recorder`
179. `meihua_relation_interpreter`
180. `meihua_symbol_lookup`
181. `mingli_school_reference`
182. `mingli_symbol_lookup`
183. `moon_phase_context_recorder`
184. `moon_phase_reflection_planner`
185. `moon_phase_symbol_lookup`
186. `naming_brand_scenario_scorer`
187. `naming_candidate_comparator`
188. `naming_symbol_lookup`
189. `nine_star_ki_interpretation_planner`
190. `nine_star_ki_profile_recorder`
191. `nine_star_ki_symbol_lookup`
192. `numerology_interpretation_planner`
193. `numerology_profile_recorder`
194. `numerology_symbol_lookup`
195. `oracle_card_draw_recorder`
196. `oracle_card_interpretation_planner`
197. `oracle_card_symbol_lookup`
198. `oracle_lot_interpretation_planner`
199. `oracle_lot_record_builder`
200. `oracle_lot_symbol_lookup`
201. `past_life_narrative_recorder`
202. `past_life_reflection_planner`
203. `past_life_symbol_lookup`
204. `pendulum_interpretation_planner`
205. `pendulum_session_recorder`
206. `pendulum_symbol_lookup`
207. `pet_communication_context_recorder`
208. `pet_communication_reflection_planner`
209. `pet_communication_symbol_lookup`
210. `physiognomy_interpretation_planner`
211. `physiognomy_observation_recorder`
212. `physiognomy_symbol_lookup`
213. `planetary_retrograde_context_recorder`
214. `planetary_retrograde_reflection_planner`
215. `planetary_retrograde_symbol_lookup`
216. `psychometry_object_recorder`
217. `psychometry_reflection_planner`
218. `psychometry_symbol_lookup`
219. `qimen_chart_record`
220. `qimen_focus_selector`
221. `qimen_school_reference`
222. `relationship_luck_action_planner`
223. `relationship_luck_context_recorder`
224. `relationship_luck_symbol_lookup`
225. `ritual_low_risk_protocol`
226. `ritual_source_example_lookup`
227. `rune_cast_recorder`
228. `rune_interpretation_planner`
229. `rune_symbol_lookup`
230. `scrying_interpretation_planner`
231. `scrying_observation_recorder`
232. `scrying_symbol_lookup`
233. `sigil_context_recorder`
234. `sigil_practice_planner`
235. `sigil_symbol_lookup`
236. `sky_omen_observation_recorder`
237. `sky_omen_reflection_planner`
238. `sky_omen_symbol_lookup`
239. `sleep_paralysis_context_recorder`
240. `sleep_paralysis_reflection_planner`
241. `sleep_paralysis_symbol_lookup`
242. `sound_cleansing_context_recorder`
243. `sound_cleansing_practice_planner`
244. `sound_cleansing_symbol_lookup`
245. `spirit_message_record_builder`
246. `spirit_message_reflection_planner`
247. `spirit_message_symbol_lookup`
248. `spiritual_protection_context_recorder`
249. `spiritual_protection_reflection_planner`
250. `spiritual_protection_symbol_lookup`
251. `synchronicity_event_recorder`
252. `synchronicity_reflection_planner`
253. `synchronicity_symbol_lookup`
254. `talisman_record_builder`
255. `talisman_symbol_lookup`
256. `talisman_use_planner`
257. `tarot_card_lookup`
258. `tarot_combination_planner`
259. `tarot_draw_recorder`
260. `tarot_draw_simulator`
261. `tarot_interpretation_planner`
262. `tarot_spread_selector`
263. `tasseography_interpretation_planner`
264. `tasseography_pattern_recorder`
265. `tasseography_symbol_lookup`
266. `wealth_luck_action_planner`
267. `wealth_luck_context_recorder`
268. `wealth_luck_symbol_lookup`
269. `western_geomancy_chart_recorder`
270. `western_geomancy_figure_lookup`
271. `western_geomancy_interpretation_planner`
272. `yijing_casting_method_advisor`
273. `yijing_casting_simulator`
274. `yijing_hexagram_lookup`
275. `yijing_hexagram_record`
276. `yijing_line_lookup`
277. `zodiac_interpretation_planner`
278. `zodiac_profile_recorder`
279. `zodiac_symbol_lookup`
280. `skill_replay_runner`
281. `skill_transcript_runner`

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
