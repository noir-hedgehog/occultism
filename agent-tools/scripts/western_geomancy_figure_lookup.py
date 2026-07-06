#!/usr/bin/env python3
"""Lookup safe symbolic prompts for Western geomancy figures."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


FIGURES = {
    "populus": ("Populus / 人群", "stable", "群体、流动、承载、环境回声", "不把多数氛围写成客观事实或群体意见证明。"),
    "via": ("Via / 道路", "mobile", "路径、转场、变化、重新排序", "不写成必须立刻离开或做重大决定。"),
    "fortuna_major": ("Fortuna Major / 大吉", "supportive", "长期支持、稳定资源、可持续优势", "不承诺成功、升职、收益或命运眷顾。"),
    "fortuna_minor": ("Fortuna Minor / 小吉", "supportive", "短期机会、窗口、外部助力、轻量推进", "不把短期机会写成保证结果。"),
    "conjunctio": ("Conjunctio / 结合", "relational", "连接、会合、协商、信息交汇", "不用于窥探第三方真实想法或强制关系。"),
    "carcer": ("Carcer / 牢笼", "restrictive", "限制、边界、暂停、结构", "不写成厄运、诅咒或永久困住。"),
    "puella": ("Puella / 少女", "relational", "柔和、审美、调停、关系氛围", "不做性别标签或关系保证。"),
    "puer": ("Puer / 少年", "active", "行动、冲动、启动、竞争", "不鼓励冲动、攻击或高风险行动。"),
    "rubeus": ("Rubeus / 红色", "volatile", "强烈情绪、警讯、过热、需要降温", "不写成灾祸预言；优先暂停和降风险。"),
    "albus": ("Albus / 白色", "reflective", "澄清、冷静、观察、理性整理", "不替代医疗、法律或事实调查。"),
    "acquisitio": ("Acquisitio / 获得", "growth", "收集、增加、资源进账、学习获得", "不承诺赚钱、中奖或投资收益。"),
    "amissio": ("Amissio / 失去", "release", "放下、减少、交换成本、清理", "不写成必然损失或关系结束。"),
    "laetitia": ("Laetitia / 喜悦", "uplift", "上升、轻松、开放、恢复弹性", "不保证好消息或结果一定改善。"),
    "tristitia": ("Tristitia / 忧伤", "weight", "重量、低落、延迟、需要承托", "不做心理诊断或宿命化悲观。"),
    "caput_draconis": ("Caput Draconis / 龙头", "threshold", "入口、开始、门槛、开启条件", "不写成神谕命令或必须开始。"),
    "cauda_draconis": ("Cauda Draconis / 龙尾", "threshold", "出口、结束、余波、释放条件", "不写成必然终结或灾祸。"),
    "left_witness": ("左见证者", "chart_position", "过去侧、内在侧、既有资源或牵制", "位置含义依体系而变，需记录使用规则。"),
    "right_witness": ("右见证者", "chart_position", "未来侧、外在侧、互动条件或行动面", "不把位置写成确定预言。"),
    "judge": ("裁判者", "chart_position", "综合句、收束点、复盘问题", "裁判者不是命令，只是本轮盘面的总结提示。"),
}

ALIASES = {
    "人群": "populus",
    "大众": "populus",
    "populus": "populus",
    "道路": "via",
    "路": "via",
    "via": "via",
    "大吉": "fortuna_major",
    "fortuna_major": "fortuna_major",
    "fortuna major": "fortuna_major",
    "小吉": "fortuna_minor",
    "fortuna_minor": "fortuna_minor",
    "fortuna minor": "fortuna_minor",
    "结合": "conjunctio",
    "连接": "conjunctio",
    "conjunctio": "conjunctio",
    "牢笼": "carcer",
    "拘束": "carcer",
    "carcer": "carcer",
    "少女": "puella",
    "puella": "puella",
    "少年": "puer",
    "puer": "puer",
    "红色": "rubeus",
    "rubeus": "rubeus",
    "白色": "albus",
    "albus": "albus",
    "获得": "acquisitio",
    "acquisitio": "acquisitio",
    "失去": "amissio",
    "amissio": "amissio",
    "喜悦": "laetitia",
    "laetitia": "laetitia",
    "忧伤": "tristitia",
    "tristitia": "tristitia",
    "龙头": "caput_draconis",
    "caput_draconis": "caput_draconis",
    "caput draconis": "caput_draconis",
    "龙尾": "cauda_draconis",
    "cauda_draconis": "cauda_draconis",
    "cauda draconis": "cauda_draconis",
    "左见证": "left_witness",
    "左见证者": "left_witness",
    "right_witness": "right_witness",
    "右见证": "right_witness",
    "右见证者": "right_witness",
    "judge": "judge",
    "裁判者": "judge",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace("-", "_")
    if lowered in FIGURES:
        return lowered
    return ALIASES.get(text, ALIASES.get(text.lower(), lowered.replace(" ", "_")))


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("figure", payload.get("symbol", ""))))
    if not code:
        raise ValueError("query, figure, or symbol is required")
    if code not in FIGURES:
        raise ValueError(f"unknown western geomancy figure: {code}")
    canonical, category, keywords_raw, action = FIGURES[code]
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    return {
        "tool": "western_geomancy_figure_lookup",
        "query": str(payload.get("query", payload.get("figure", payload.get("symbol", code)))).strip(),
        "canonical_name": canonical,
        "system": "western_geomancy_symbolic_reflection",
        "figure_code": code,
        "category": category,
        "symbol_set": "sixteen_common_geomantic_figures_plus_chart_positions",
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为西洋土占象征，围绕{focus}整理趋势语言、现实证据、边界和低风险下一步。",
        "reflection_questions": [
            "这个图形处在母亲、女儿、侄子、见证者还是裁判者位置？",
            "它更像资源、阻力、门槛、连接、释放、暂停还是行动提醒？",
            "哪些结论必须回到现实证据、专业支持、当事人沟通或安全约束？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把图形写成确定预言、事实证明、诊断、财富结果、赌博建议或专业意见。",
            "不使用盾形盘窥探第三方真实想法、控制他人或决定重大风险事项。",
            "不反复起盘直到满意。",
        ],
        "next_steps": ["combine_with_western_geomancy_chart_record", "prefer_reality_check_and_low_risk_action", "run_mystic_output_lint"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.query:
        return {"query": args.query, "focus": args.focus}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Western geomancy figure, e.g. Via, Populus, 龙头.")
    parser.add_argument("--focus", help="Optional consultation focus.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = lookup(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
