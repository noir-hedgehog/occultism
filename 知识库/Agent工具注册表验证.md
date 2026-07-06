# Agent Tool Registry Validation

本页验证 runtime 工具注册表是否适合注册：注册顺序、索引、bootstrap 和 Skill 必备工具必须一致。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| Valid | True |
| Tool | 280 |
| Domain group | 62 |
| Skill group | 61 |
| Error | 0 |

## Bootstrap Prefix

- `mystic_intake_triage`
- `agent_workflow_router`
- `mystic_output_lint`

## Skill Checks

| Skill | Valid | Missing Required Tools | Invalid Tools |
| --- | --- | --- | --- |
| `animal-omen-symbolic-consultation` | True | - | - |
| `aroma-symbolic-consultation` | True | - | - |
| `astrology-symbolic-consultation` | True | - | - |
| `aura-chakra-symbolic-consultation` | True | - | - |
| `bibliomancy-symbolic-consultation` | True | - | - |
| `body-omen-symbolic-consultation` | True | - | - |
| `candle-symbolic-consultation` | True | - | - |
| `cartomancy-symbolic-consultation` | True | - | - |
| `casting-lots-symbolic-consultation` | True | - | - |
| `character-divination-symbolic-consultation` | True | - | - |
| `color-symbolic-consultation` | True | - | - |
| `consecration-symbolic-consultation` | True | - | - |
| `crystal-symbolic-consultation` | True | - | - |
| `date-selection-consultation` | True | - | - |
| `deity-ancestor-symbolic-consultation` | True | - | - |
| `dice-symbolic-consultation` | True | - | - |
| `dowsing-symbolic-consultation` | True | - | - |
| `dream-symbolic-consultation` | True | - | - |
| `feng-shui-space-audit` | True | - | - |
| `flower-symbolic-consultation` | True | - | - |
| `folk-custom-consultation` | True | - | - |
| `herbal-symbolic-consultation` | True | - | - |
| `human-design-symbolic-consultation` | True | - | - |
| `incense-symbolic-consultation` | True | - | - |
| `lenormand-symbolic-consultation` | True | - | - |
| `liuyao-symbolic-consultation` | True | - | - |
| `lost-object-symbolic-consultation` | True | - | - |
| `manifestation-symbolic-consultation` | True | - | - |
| `meihua-symbolic-consultation` | True | - | - |
| `mingli-bazi-ziwei-consultation` | True | - | - |
| `moon-phase-symbolic-consultation` | True | - | - |
| `naming-symbolic-consultation` | True | - | - |
| `nine-star-ki-symbolic-consultation` | True | - | - |
| `numerology-symbolic-consultation` | True | - | - |
| `oracle-card-symbolic-consultation` | True | - | - |
| `oracle-lot-symbolic-consultation` | True | - | - |
| `past-life-akashic-symbolic-consultation` | True | - | - |
| `pendulum-symbolic-consultation` | True | - | - |
| `pet-communication-symbolic-consultation` | True | - | - |
| `physiognomy-symbolic-consultation` | True | - | - |
| `planetary-retrograde-symbolic-consultation` | True | - | - |
| `psychometry-symbolic-consultation` | True | - | - |
| `qimen-chart-consultation` | True | - | - |
| `relationship-luck-symbolic-consultation` | True | - | - |
| `ritual-safety-advisor` | True | - | - |
| `rune-symbolic-consultation` | True | - | - |
| `scrying-symbolic-consultation` | True | - | - |
| `sigil-symbolic-consultation` | True | - | - |
| `sky-omen-symbolic-consultation` | True | - | - |
| `sleep-paralysis-symbolic-consultation` | True | - | - |
| `sound-cleansing-symbolic-consultation` | True | - | - |
| `spirit-message-symbolic-consultation` | True | - | - |
| `spiritual-protection-symbolic-consultation` | True | - | - |
| `synchronicity-symbolic-consultation` | True | - | - |
| `talisman-symbolic-consultation` | True | - | - |
| `tarot-symbolic-reading` | True | - | - |
| `tasseography-symbolic-consultation` | True | - | - |
| `wealth-luck-symbolic-consultation` | True | - | - |
| `western-geomancy-symbolic-consultation` | True | - | - |
| `yijing-symbolic-consultation` | True | - | - |
| `zodiac-symbolic-consultation` | True | - | - |

## 限制

- 此验证只检查注册表结构，不注册或执行工具。
- 通过验证不代表 runtime 命令执行器已完成权限隔离。
- Skill 仍需通过回放和真实匿名 transcript 流程继续验证。
