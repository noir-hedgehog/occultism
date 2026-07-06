#!/usr/bin/env python3
"""Guard birth-data intake for Bazi and Ziwei Dou Shu consultations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    label: str
    keywords: tuple[str, ...]


DOMAIN_RULES = {
    "bazi": ("八字", "四柱", "生辰八字", "天干", "地支", "大运", "流年"),
    "ziwei": ("紫微", "斗数", "命宫", "身宫", "十四主星", "紫微斗数"),
}

FOCUS_RULES = {
    "career": ("事业", "工作", "跳槽", "职业", "项目", "升职", "offer"),
    "relationship": ("感情", "婚姻", "复合", "恋爱", "伴侣", "桃花"),
    "self_understanding": ("性格", "优势", "天赋", "自我", "状态", "倾向"),
    "timing": ("大运", "流年", "什么时候", "何时", "年份", "阶段"),
    "family": ("家庭", "父母", "孩子", "子女", "亲人"),
    "health": ("健康", "病", "手术", "怀孕", "医生", "用药"),
    "finance": ("股票", "投资", "彩票", "赌博", "贷款", "借贷", "发财"),
    "legal": ("官司", "起诉", "律师", "刑事", "合同", "移民"),
}

RISK_RULES = (
    Rule("crisis", ("自杀", "自残", "活不下去", "伤害自己", "伤害别人", "家暴", "被威胁")),
    Rule("professional_health", ("诊断", "用药", "手术", "怀孕", "癌", "病", "医生")),
    Rule("professional_finance", ("股票", "彩票", "赌博", "贷款", "借贷", "梭哈", "币圈", "投资")),
    Rule("professional_legal", ("起诉", "官司", "刑事", "律师", "合同", "移民")),
    Rule("fatalistic_harm", ("死期", "活多久", "克死", "必死", "注定没救", "命里没救", "一定离婚")),
    Rule("coercion", ("控制他", "控制她", "让他爱我", "让她爱我", "拆散", "报复")),
)

THIRD_PARTY_MARKERS = ("他", "她", "前任", "对象", "朋友", "同事", "老板", "老公", "老婆", "男友", "女友")
MINOR_MARKERS = ("孩子", "宝宝", "儿子", "女儿", "未成年", "小孩")
CALENDAR_MARKERS = ("公历", "阳历", "农历", "阴历", "真太阳时", "北京时间")
TIME_MARKERS = ("子时", "丑时", "寅时", "卯时", "辰时", "巳时", "午时", "未时", "申时", "酉时", "戌时", "亥时")


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_domain(text: str, requested_domain: object = None) -> str:
    if isinstance(requested_domain, str) and requested_domain in ("bazi", "ziwei", "mingli"):
        return requested_domain
    for domain, keywords in DOMAIN_RULES.items():
        if contains_any(text, keywords):
            return domain
    return "mingli"


def detect_focus(text: str) -> str:
    for focus, keywords in FOCUS_RULES.items():
        if contains_any(text, keywords):
            return focus
    return "general"


def detect_risks(text: str) -> list[str]:
    return [rule.label for rule in RISK_RULES if contains_any(text, rule.keywords)]


def has_birth_date(payload: dict[str, object], text: str) -> bool:
    if payload.get("birth_date") or payload.get("birth_datetime"):
        return True
    return bool(re.search(r"(?:19|20)\d{2}[-/.年]\d{1,2}(?:[-/.月]\d{1,2})?", text))


def has_birth_time(payload: dict[str, object], text: str) -> bool:
    if payload.get("birth_time") or payload.get("birth_datetime"):
        return True
    return bool(re.search(r"(?:^|[^\d])\d{1,2}:\d{2}(?:[^\d]|$)", text) or contains_any(text, TIME_MARKERS))


def has_birth_place(payload: dict[str, object], text: str) -> bool:
    if payload.get("birth_place"):
        return True
    return contains_any(text, ("北京", "上海", "广州", "深圳", "杭州", "成都", "重庆", "南京", "武汉", "西安", "台北", "香港"))


def has_calendar_type(payload: dict[str, object], text: str) -> bool:
    if payload.get("calendar_type"):
        return True
    return contains_any(text, CALENDAR_MARKERS)


def has_subject_consent(payload: dict[str, object], text: str) -> bool:
    if payload.get("subject_consent") is True:
        return True
    return contains_any(text, ("本人", "我自己的", "已同意", "经过同意", "同意分析"))


def detect_privacy_flags(payload: dict[str, object], text: str) -> list[str]:
    flags: list[str] = []
    if has_birth_date(payload, text) or has_birth_time(payload, text):
        flags.append("exact_birth_data")
    if contains_any(text, THIRD_PARTY_MARKERS) or payload.get("subject_is_self") is False:
        flags.append("third_party_subject")
    if contains_any(text, MINOR_MARKERS) or payload.get("subject_is_minor") is True:
        flags.append("minor_subject")
    if contains_any(text, ("身份证", "手机号", "住址", "姓名全名", "真实姓名")):
        flags.append("sensitive_identity")
    return flags


def missing_fields(payload: dict[str, object], text: str, focus: str, privacy_flags: list[str]) -> list[str]:
    missing: list[str] = []
    if not has_birth_date(payload, text):
        missing.append("birth_date")
    if not has_birth_time(payload, text):
        missing.append("birth_time")
    if not has_birth_place(payload, text):
        missing.append("birth_place")
    if not has_calendar_type(payload, text):
        missing.append("calendar_type")
    if focus == "general":
        missing.append("analysis_focus")
    if "third_party_subject" in privacy_flags and not has_subject_consent(payload, text):
        missing.append("subject_consent")
    return missing


def data_status(missing: list[str]) -> str:
    core_missing = [field for field in missing if field in ("birth_date", "birth_time", "birth_place", "calendar_type")]
    if not missing:
        return "complete"
    if len(core_missing) <= 2:
        return "partial"
    return "minimal"


def reframe(focus: str, risks: list[str], privacy_flags: list[str], missing: list[str]) -> str:
    if "crisis" in risks:
        return "先暂停命理分析，把问题改为：我现在如何获得即时安全和可信任支持？"
    if any(risk.startswith("professional_") for risk in risks):
        return "命理不能替代专业判断；可改为：面对这个现实问题，我需要确认哪些事实、风险和支持？"
    if "fatalistic_harm" in risks:
        return "不做寿命、灾祸或不可改变命运的断言；可改为：我如何理解当前压力，并找到可行动的调整方向？"
    if "coercion" in risks:
        return "不做操控他人的命理判断；可改为：我如何尊重边界并处理自己的选择？"
    if "subject_consent" in missing:
        return "请先获得当事人同意，或改为匿名、概括性的文化学习问题。"
    if "minor_subject" in privacy_flags:
        return "涉及未成年人时，只能做非标签化的支持性观察，不做终身定性或高风险预测。"
    if focus == "career":
        return "从命理象征角度整理职业倾向、阶段压力和可验证的行动选择。"
    if focus == "relationship":
        return "从命理象征角度整理关系互动倾向、边界和可沟通事项。"
    if focus == "timing":
        return "从命理象征角度观察阶段主题，不把年份或运势当成确定结果。"
    if focus == "self_understanding":
        return "从命理象征角度整理性格资源、惯性模式和可练习的调整方向。"
    return "把命理分析限定为自我理解、阶段复盘和行动提示，不做宿命断言。"


def next_steps(can_continue: bool, status: str) -> list[str]:
    if not can_continue:
        return ["pause_mingli_reading", "resolve_privacy_safety_or_professional_issue_first"]
    steps = ["confirm_consent_and_scope", "collect_or_confirm_birth_data"]
    if status == "complete":
        steps.append("record_chart_method_or_generate_chart_when_available")
    else:
        steps.append("ask_missing_birth_data_or_offer_general_symbolic_reading")
    steps.append("lint_final_output_with_mystic_output_lint")
    return steps


def guard(payload: dict[str, object]) -> dict[str, object]:
    text = str(payload.get("request_text", payload.get("question_text", ""))).strip()
    if not text:
        raise ValueError("request_text or question_text is required")

    domain = detect_domain(text, payload.get("requested_domain"))
    focus = detect_focus(text)
    risks = detect_risks(text)
    privacy = detect_privacy_flags(payload, text)
    missing = missing_fields(payload, text, focus, privacy)
    status = data_status(missing)

    blocking_risks = {
        "crisis",
        "professional_health",
        "professional_finance",
        "professional_legal",
        "fatalistic_harm",
        "coercion",
    }
    can_continue = not (set(risks) & blocking_risks) and "subject_consent" not in missing and "sensitive_identity" not in privacy

    warnings: list[str] = []
    if "exact_birth_data" in privacy:
        warnings.append("出生日期、时间和地点属于敏感个人资料，输出和日志应最小化保存。")
    if "third_party_subject" in privacy and "subject_consent" in missing:
        warnings.append("第三方命盘需要当事人同意；否则只能做匿名文化解释。")
    if "minor_subject" in privacy:
        warnings.append("未成年人命理只能做支持性、非标签化表述。")
    if "sensitive_identity" in privacy:
        warnings.append("不要收集身份证、手机号、住址或完整真实姓名。")
    if risks:
        warnings.append("请求含高风险或专业替代信号，不能进入确定性命理判断。")

    return {
        "request_text": text,
        "domain": domain,
        "analysis_focus": focus,
        "data_status": status,
        "missing_fields": missing,
        "privacy_flags": privacy,
        "risk_flags": risks,
        "can_continue_mingli": can_continue,
        "reframed_question": reframe(focus, risks, privacy, missing),
        "allowed_scope": [
            "自我理解",
            "阶段复盘",
            "象征性倾向整理",
            "低风险行动提示",
        ],
        "limits": [
            "不做寿命、灾祸、婚育、疾病或财富的确定性断言。",
            "不得替代医疗、法律、财务或心理健康专业建议。",
            "第三方或未成年人资料必须最小化、匿名化，并优先获得同意。",
        ],
        "warnings": warnings,
        "next_steps": next_steps(can_continue, status),
    }


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"request_text": raw}
    if args.text:
        return {"request_text": args.text, "requested_domain": args.domain}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw, "requested_domain": args.domain}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Mingli consultation request text.")
    parser.add_argument("--domain", help="Optional requested domain: bazi, ziwei, or mingli.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to text or JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
