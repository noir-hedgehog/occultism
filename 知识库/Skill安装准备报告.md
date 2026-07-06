# Skill 安装准备报告

本页汇总 Codex Skill 安装前的 dry-run 证据、目标路径、冲突状态和审批清单。它不表示已经安装。

## 当前状态

| 指标 | 当前值 |
| --- | --- |
| 状态 | `ready_for_install_approval` |
| 目标 Codex home | `/private/tmp/mystic-codex-home-preview` |
| 目标 skills 目录 | `/private/tmp/mystic-codex-home-preview/skills` |
| Skill 数 | 61 |
| 将创建 | 61 |
| 已是最新 | 0 |
| 冲突 | 0 |
| 内容审校批准 | 0 |
| 可进入内容审校 | 61 |

## 审批清单

- 确认目标 Codex home 正确。
- 确认将安装或覆盖的 Skill 名称正确。
- 确认当前仓库路径会在 Skill 引用知识库和工具时保持可访问。
- 确认真实匿名 transcript、内容审校和安装时机的开放事项是否可接受。
- 确认如需覆盖已有 Skill，已人工检查差异并显式加入 --overwrite。

## 安装命令

仅在用户明确确认后运行：

```bash
python3 agent-tools/scripts/codex_skill_installer.py --codex-home /private/tmp/mystic-codex-home-preview --install --skill animal-omen-symbolic-consultation --skill aroma-symbolic-consultation --skill astrology-symbolic-consultation --skill aura-chakra-symbolic-consultation --skill bibliomancy-symbolic-consultation --skill body-omen-symbolic-consultation --skill candle-symbolic-consultation --skill cartomancy-symbolic-consultation --skill casting-lots-symbolic-consultation --skill character-divination-symbolic-consultation --skill color-symbolic-consultation --skill consecration-symbolic-consultation --skill crystal-symbolic-consultation --skill date-selection-consultation --skill deity-ancestor-symbolic-consultation --skill dice-symbolic-consultation --skill dowsing-symbolic-consultation --skill dream-symbolic-consultation --skill feng-shui-space-audit --skill flower-symbolic-consultation --skill folk-custom-consultation --skill herbal-symbolic-consultation --skill human-design-symbolic-consultation --skill incense-symbolic-consultation --skill lenormand-symbolic-consultation --skill liuyao-symbolic-consultation --skill lost-object-symbolic-consultation --skill manifestation-symbolic-consultation --skill meihua-symbolic-consultation --skill mingli-bazi-ziwei-consultation --skill moon-phase-symbolic-consultation --skill naming-symbolic-consultation --skill nine-star-ki-symbolic-consultation --skill numerology-symbolic-consultation --skill oracle-card-symbolic-consultation --skill oracle-lot-symbolic-consultation --skill past-life-akashic-symbolic-consultation --skill pendulum-symbolic-consultation --skill pet-communication-symbolic-consultation --skill physiognomy-symbolic-consultation --skill planetary-retrograde-symbolic-consultation --skill psychometry-symbolic-consultation --skill qimen-chart-consultation --skill relationship-luck-symbolic-consultation --skill ritual-safety-advisor --skill rune-symbolic-consultation --skill scrying-symbolic-consultation --skill sigil-symbolic-consultation --skill sky-omen-symbolic-consultation --skill sleep-paralysis-symbolic-consultation --skill sound-cleansing-symbolic-consultation --skill spirit-message-symbolic-consultation --skill spiritual-protection-symbolic-consultation --skill synchronicity-symbolic-consultation --skill talisman-symbolic-consultation --skill tarot-symbolic-reading --skill tasseography-symbolic-consultation --skill wealth-luck-symbolic-consultation --skill western-geomancy-symbolic-consultation --skill yijing-symbolic-consultation --skill zodiac-symbolic-consultation
```

## Dry-run 行动

| Skill | Action | Reason |
| --- | --- | --- |
| `animal-omen-symbolic-consultation` | `create` | target skill is not installed |
| `aroma-symbolic-consultation` | `create` | target skill is not installed |
| `astrology-symbolic-consultation` | `create` | target skill is not installed |
| `aura-chakra-symbolic-consultation` | `create` | target skill is not installed |
| `bibliomancy-symbolic-consultation` | `create` | target skill is not installed |
| `body-omen-symbolic-consultation` | `create` | target skill is not installed |
| `candle-symbolic-consultation` | `create` | target skill is not installed |
| `cartomancy-symbolic-consultation` | `create` | target skill is not installed |
| `casting-lots-symbolic-consultation` | `create` | target skill is not installed |
| `character-divination-symbolic-consultation` | `create` | target skill is not installed |
| `color-symbolic-consultation` | `create` | target skill is not installed |
| `consecration-symbolic-consultation` | `create` | target skill is not installed |
| `crystal-symbolic-consultation` | `create` | target skill is not installed |
| `date-selection-consultation` | `create` | target skill is not installed |
| `deity-ancestor-symbolic-consultation` | `create` | target skill is not installed |
| `dice-symbolic-consultation` | `create` | target skill is not installed |
| `dowsing-symbolic-consultation` | `create` | target skill is not installed |
| `dream-symbolic-consultation` | `create` | target skill is not installed |
| `feng-shui-space-audit` | `create` | target skill is not installed |
| `flower-symbolic-consultation` | `create` | target skill is not installed |
| `folk-custom-consultation` | `create` | target skill is not installed |
| `herbal-symbolic-consultation` | `create` | target skill is not installed |
| `human-design-symbolic-consultation` | `create` | target skill is not installed |
| `incense-symbolic-consultation` | `create` | target skill is not installed |
| `lenormand-symbolic-consultation` | `create` | target skill is not installed |
| `liuyao-symbolic-consultation` | `create` | target skill is not installed |
| `lost-object-symbolic-consultation` | `create` | target skill is not installed |
| `manifestation-symbolic-consultation` | `create` | target skill is not installed |
| `meihua-symbolic-consultation` | `create` | target skill is not installed |
| `mingli-bazi-ziwei-consultation` | `create` | target skill is not installed |
| `moon-phase-symbolic-consultation` | `create` | target skill is not installed |
| `naming-symbolic-consultation` | `create` | target skill is not installed |
| `nine-star-ki-symbolic-consultation` | `create` | target skill is not installed |
| `numerology-symbolic-consultation` | `create` | target skill is not installed |
| `oracle-card-symbolic-consultation` | `create` | target skill is not installed |
| `oracle-lot-symbolic-consultation` | `create` | target skill is not installed |
| `past-life-akashic-symbolic-consultation` | `create` | target skill is not installed |
| `pendulum-symbolic-consultation` | `create` | target skill is not installed |
| `pet-communication-symbolic-consultation` | `create` | target skill is not installed |
| `physiognomy-symbolic-consultation` | `create` | target skill is not installed |
| `planetary-retrograde-symbolic-consultation` | `create` | target skill is not installed |
| `psychometry-symbolic-consultation` | `create` | target skill is not installed |
| `qimen-chart-consultation` | `create` | target skill is not installed |
| `relationship-luck-symbolic-consultation` | `create` | target skill is not installed |
| `ritual-safety-advisor` | `create` | target skill is not installed |
| `rune-symbolic-consultation` | `create` | target skill is not installed |
| `scrying-symbolic-consultation` | `create` | target skill is not installed |
| `sigil-symbolic-consultation` | `create` | target skill is not installed |
| `sky-omen-symbolic-consultation` | `create` | target skill is not installed |
| `sleep-paralysis-symbolic-consultation` | `create` | target skill is not installed |
| `sound-cleansing-symbolic-consultation` | `create` | target skill is not installed |
| `spirit-message-symbolic-consultation` | `create` | target skill is not installed |
| `spiritual-protection-symbolic-consultation` | `create` | target skill is not installed |
| `synchronicity-symbolic-consultation` | `create` | target skill is not installed |
| `talisman-symbolic-consultation` | `create` | target skill is not installed |
| `tarot-symbolic-reading` | `create` | target skill is not installed |
| `tasseography-symbolic-consultation` | `create` | target skill is not installed |
| `wealth-luck-symbolic-consultation` | `create` | target skill is not installed |
| `western-geomancy-symbolic-consultation` | `create` | target skill is not installed |
| `yijing-symbolic-consultation` | `create` | target skill is not installed |
| `zodiac-symbolic-consultation` | `create` | target skill is not installed |

## 限制

- 此报告只做 dry-run 准备，不安装或覆盖任何 Skill。
- ready_for_install_approval 表示可请求人工确认，不表示已经安装。
- 内容审校批准数来自审校包当前记录；没有真实审校反馈时不应视为内容已批准。
