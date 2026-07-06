# Tool Spec：fengshui_observation_recorder

## 目的

在风水解释前记录可见事实，尤其适用于用户提供照片说明、户型描述或空间观察文本时。该工具不做最终风水判断，只把“看见/听见/用户报告的事实”整理成可审计记录，并标记哪些传统术语可以在事实之后谨慎解释。

## 输入

- `observation_text` / `space_description` / `request_text`：文字观察或图片说明
- `space_type`：可选，卧室、办公室、客厅、厨房、入口、店铺等
- `input_mode`：`text_description`、`image_notes` 或 `mixed`

## 输出

- `space_type`
- `observations`：每条可见事实、区域、特征、传统术语候选、现实体验映射
- `safety_flags`：燃气、电路、霉菌/空气、安保、严重睡眠/精神状态
- `inferred_claims_to_avoid`：用户或模型不应直接采纳的推断词
- `missing_details`
- `interpretation_queue`：允许进入传统术语解释的观察项
- `notes`、`next_steps`

## 安全规则

1. 先描述可见事实，再解释传统术语。
2. 不从照片或描述直接断言灾祸、财富、婚姻、疾病或超自然原因。
3. 现实安全信号必须先处理，不能包装成风水建议。
4. 对图片内容不确定时标记为 `reported` 或补问，不伪装成已观察事实。

## 命令

```bash
python3 agent-tools/scripts/fengshui_observation_recorder.py --text "图里卧室床正对门，镜子对床，床边过道堆了箱子"
```
