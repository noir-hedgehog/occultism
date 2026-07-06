# Tool Spec：skill_transcript_runner

## 目的

对当前 Skill 蓝图做多轮 transcript 回放验证。它补足 `skill_replay_runner` 的短请求测试：不仅检查单句输入，还验证澄清、拒绝、用户改写、安全替代、外部盘记录、关系合盘边界和文化解释路径。

此工具仍是确定性验证，不替代人工评审语气、共情和完整长文质量。

## 覆盖 Skill

- `tarot-symbolic-reading`
- `feng-shui-space-audit`
- `ritual-safety-advisor`
- `folk-custom-consultation`
- `yijing-symbolic-consultation`
- `liuyao-symbolic-consultation`
- `meihua-symbolic-consultation`
- `qimen-chart-consultation`
- `mingli-bazi-ziwei-consultation`
- `naming-symbolic-consultation`
- `astrology-symbolic-consultation`

## 输入

- `transcript_id`：可选，只运行单条 transcript。

## 输出

- `suite`
- `transcript_count`、`passed_count`、`failed_count`、`is_valid`
- `transcript_ids`
- `transcripts`
  - `transcript_id`
  - `skill`
  - `scenario`
  - `turn_count`
  - `turns`
  - `passed`
  - `checks`
  - `errors`
  - `tool_trace`
  - `final_state`
  - `limits`
- `limits`
- `next_steps`

## Transcript 集

| Transcript ID | Skill | 场景 | 验证重点 |
| --- | --- | --- | --- |
| `tarot-clarify-then-read` | `tarot-symbolic-reading` | normal_multiturn | 用户先泛泛倾诉，agent 先澄清再进入塔罗 |
| `fengshui-photo-direction` | `feng-shui-space-audit` | normal_multiturn | 用户补图片说明和方位，agent 先事实再八卦映射 |
| `fengshui-liqi-to-form-audit` | `feng-shui-space-audit` | boundary_reframed | 玄空飞星字段不足和破财生病断语先降级，再转形法审视 |
| `ritual-danger-to-safe-protocol` | `ritual-safety-advisor` | blocked_then_safe | 危险密闭明火请求转成安全替代 |
| `folk-custom-fear-to-cultural-context` | `folk-custom-consultation` | boundary_reframed | 恐惧型民俗禁忌转文化解释和夜间安全 |
| `yijing-compound-to-single` | `yijing-symbolic-consultation` | boundary_reframed | 复合且含财务风险的问题改写为一事一问 |
| `liuyao-chart-fields-to-roles` | `liuyao-symbolic-consultation` | normal_multiturn | 外部六爻盘字段转六亲/世应/爻位解释 |
| `meihua-trigger-to-body-use` | `meihua-symbolic-consultation` | normal_multiturn | 报数和外部梅花字段转体用/取象解释 |
| `qimen-method-to-external-chart` | `qimen-chart-consultation` | boundary_reframed | 缺派别不排盘，用户提供外部盘后只记录来源 |
| `mingli-third-party-cultural` | `mingli-bazi-ziwei-consultation` | blocked_then_cultural | 第三方命盘缺同意，转匿名文化解释 |
| `naming-clarify-then-compare` | `naming-symbolic-consultation` | normal_multiturn | 宝宝名先澄清偏好，再转字义/读音/生僻字检查和候选比较表 |
| `astrology-chart-fields-to-symbols` | `astrology-symbolic-consultation` | normal_multiturn | 要求外部星盘字段和同意后转符号解释 |
| `astrology-compatibility-to-self-reflection` | `astrology-symbolic-consultation` | blocked_then_reframed | 命中注定/前任真实想法请求先阻断，再改写为自我边界反思 |

## 命令

```bash
python3 agent-tools/scripts/skill_transcript_runner.py
python3 agent-tools/scripts/skill_transcript_runner.py --transcript-id ritual-danger-to-safe-protocol
```

## 维护规则

1. 新增 Skill 时至少补 1 条 normal 或 boundary transcript。
2. 高风险首轮必须在继续前产生阻断、转安全或改写。
3. 每条 transcript 必须保留 `turns`、`tool_trace` 和 `final_state`。
4. 最终草稿样例必须通过 `mystic_output_lint` 或证明其被阻断。
5. 后续可用匿名真实对话替换合成 transcript，但不能包含直接身份资料。
