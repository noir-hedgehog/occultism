#!/usr/bin/env python3
"""Record user-provided palmistry and physiognomy observations safely."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

import physiognomy_request_guard


FEATURES = {
    "life_line": ("生命线", "地纹", "life line"),
    "head_line": ("智慧线", "头脑线", "head line"),
    "heart_line": ("感情线", "天纹", "heart line"),
    "fate_line": ("事业线", "命运线", "fate line"),
    "sun_line": ("太阳线", "成功线", "sun line"),
    "mount": ("掌丘", "金星丘", "木星丘", "土星丘", "太阳丘", "水星丘", "月丘"),
    "forehead": ("额头", "天庭"),
    "eyebrows": ("眉", "眉毛"),
    "eyes": ("眼", "眼睛"),
    "nose": ("鼻", "鼻子", "鼻相"),
    "mouth": ("嘴", "嘴巴", "口"),
    "chin": ("下巴", "地阁"),
    "mole": ("痣", "痣相"),
}

MODALITY_KEYWORDS = {
    "palm": ("手相", "掌纹", "生命线", "智慧线", "感情线", "事业线", "掌丘"),
    "face": ("面相", "五官", "额头", "眉", "眼", "鼻", "嘴", "下巴"),
    "mole": ("痣相", "痣"),
}

OBSERVATION_RE = re.compile(r"(.{0,8}(?:线|丘|额头|眉毛?|眼睛?|鼻子?|嘴巴?|下巴|痣).{0,18})")


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_modality(text: str) -> str:
    for modality, keywords in MODALITY_KEYWORDS.items():
        if contains_any(text, keywords):
            return modality
    return "mixed_or_unspecified"


def extract_feature_codes(text: str, explicit_features: list[str]) -> list[str]:
    codes = set()
    for raw in explicit_features:
        normalized = str(raw).strip()
        if normalized in FEATURES:
            codes.add(normalized)
        else:
            for code, aliases in FEATURES.items():
                if normalized in aliases:
                    codes.add(code)
    for code, aliases in FEATURES.items():
        if contains_any(text, aliases):
            codes.add(code)
    return sorted(codes)


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("observation_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("observation_text, request_text, or text is required")
    guard = physiognomy_request_guard.guard(
        {
            "request_text": text,
            "subject_is_self": payload.get("subject_is_self"),
            "consent_obtained": payload.get("consent_obtained"),
            "cultural_learning_only": payload.get("cultural_learning_only"),
        }
    )
    feature_codes = extract_feature_codes(text, list(payload.get("features", []) or []))
    observations = [match.group(1).strip(" ，。；;") for match in OBSERVATION_RE.finditer(text)]
    missing_fields: list[str] = []
    if not feature_codes:
        missing_fields.append("features")
    if guard["consent_state"] == "missing_or_unknown":
        missing_fields.append("subject_consent")
    return {
        "tool": "physiognomy_observation_recorder",
        "system": "palmistry_and_physiognomy_symbolism",
        "is_valid": bool(guard["can_continue_physiognomy"]),
        "can_continue_physiognomy": bool(guard["can_continue_physiognomy"]),
        "observation_text": text,
        "modality": str(payload.get("modality", "")).strip() or detect_modality(text),
        "consent_state": guard["consent_state"],
        "feature_codes": feature_codes,
        "observations": observations[:8],
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_symbols_for_recorded_features",
            "build_symbolic_interpretation_plan",
            "ask_for_missing_observations_without_photo_inference",
        ] if guard["can_continue_physiognomy"] else guard["next_steps"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["observation_text"] = args.text
    if args.subject_is_self:
        payload["subject_is_self"] = True
    if args.consent_obtained:
        payload["consent_obtained"] = True
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"observation_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="User-provided observation text.")
    parser.add_argument("--subject-is-self", action="store_true")
    parser.add_argument("--consent-obtained", action="store_true")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = record(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
