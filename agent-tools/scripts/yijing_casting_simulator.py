#!/usr/bin/env python3
"""Simulate Yijing casting methods and record the resulting hexagram."""

from __future__ import annotations

import argparse
import json
import random
import secrets
import sys
from datetime import datetime, timezone
from typing import Any

import yijing_hexagram_record


METHODS = {"three_coins", "yarrow_stalk"}
LINE_LABELS = {
    6: "老阴",
    7: "少阳",
    8: "少阴",
    9: "老阳",
}


def normalize_method(value: object) -> str:
    raw = str(value or "three_coins").strip().lower()
    aliases = {
        "coins": "three_coins",
        "three_coin": "three_coins",
        "coin": "three_coins",
        "三枚铜钱": "three_coins",
        "铜钱": "three_coins",
        "yarrow": "yarrow_stalk",
        "yarrow_stalks": "yarrow_stalk",
        "蓍草": "yarrow_stalk",
    }
    method = aliases.get(raw, raw)
    if method not in METHODS:
        raise ValueError(f"unknown casting method: {value}")
    return method


def cast_three_coin_line(rng: random.Random) -> dict[str, Any]:
    coins = [rng.choice(("heads", "tails")) for _ in range(3)]
    total = sum(3 if coin == "heads" else 2 for coin in coins)
    return {
        "value": total,
        "label": LINE_LABELS[total],
        "trace": {
            "coins": coins,
            "coin_values": [3 if coin == "heads" else 2 for coin in coins],
        },
    }


def cast_yarrow_line(rng: random.Random) -> dict[str, Any]:
    # Traditional yarrow probabilities: 6:1/16, 7:5/16, 8:7/16, 9:3/16.
    value = rng.choices((6, 7, 8, 9), weights=(1, 5, 7, 3), k=1)[0]
    return {
        "value": value,
        "label": LINE_LABELS[value],
        "trace": {
            "probability_model": "traditional_yarrow_distribution",
            "weights": {"6": 1, "7": 5, "8": 7, "9": 3},
        },
    }


def cast_line(method: str, rng: random.Random) -> dict[str, Any]:
    if method == "three_coins":
        return cast_three_coin_line(rng)
    if method == "yarrow_stalk":
        return cast_yarrow_line(rng)
    raise ValueError(f"unknown casting method: {method}")


def simulate(payload: dict[str, Any]) -> dict[str, Any]:
    method = normalize_method(payload.get("casting_method", payload.get("method")))
    seed = payload.get("seed")
    generated_seed = False
    if seed in (None, ""):
        seed = secrets.randbits(64)
        generated_seed = True
    rng = random.Random(str(seed))

    generated_lines = []
    for index in range(1, 7):
        line = cast_line(method, rng)
        generated_lines.append({"index": index, **line})

    cast_time = str(payload.get("cast_time", datetime.now(timezone.utc).isoformat()))
    timezone_name = str(payload.get("timezone", "UTC"))
    record_payload = {
        "question_text": str(payload.get("question_text", payload.get("request_text", ""))).strip(),
        "casting_method": f"simulated_{method}",
        "cast_time": cast_time,
        "timezone": timezone_name,
        "lines": [line["value"] for line in generated_lines],
    }
    recorded = yijing_hexagram_record.record(record_payload)

    return {
        "question_text": record_payload["question_text"],
        "casting_method": method,
        "seed": str(seed),
        "seed_generated": generated_seed,
        "cast_time": cast_time,
        "timezone": timezone_name,
        "line_order": "bottom_to_top",
        "generated_lines": generated_lines,
        "recorded_cast": recorded,
        "limits": [
            "Simulated casting is a randomization aid for symbolic reflection, not proof of fate or prediction.",
            "Use a seed when the cast must be reproducible for audit or tests.",
            "Continue only after yijing_question_guard approves the question framing.",
        ],
        "next_steps": [
            "review_recorded_cast_is_valid",
            "lookup_base_and_changed_hexagrams_with_yijing_hexagram_lookup",
            "interpret_changing_lines_as_change_focus",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload.update(json.load(f))
    if args.method:
        payload["method"] = args.method
    if args.question:
        payload["question_text"] = args.question
    if args.seed:
        payload["seed"] = args.seed
    if args.timezone:
        payload["timezone"] = args.timezone
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"question_text": raw}
    raise ValueError("Provide --json, --file, --method, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON input.")
    parser.add_argument("--file", help="Path to JSON input.")
    parser.add_argument("--method", help="three_coins or yarrow_stalk.")
    parser.add_argument("--question", help="Optional question text.")
    parser.add_argument("--seed", help="Optional deterministic seed.")
    parser.add_argument("--timezone", help="Optional timezone label.")
    args = parser.parse_args()
    try:
        result = simulate(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
