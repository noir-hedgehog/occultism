#!/usr/bin/env python3
"""Build a machine-readable manifest for agent tools and Skill hooks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import knowledge_coverage_audit


INDEX_ROW_RE = re.compile(r"^\|\s*`(?P<skill>[^`]+)`\s*\|\s*(?P<role>.*?)\s*\|\s*(?P<tools>.*?)\s*\|$")
BACKTICK_RE = re.compile(r"`([^`]+)`")

DOMAIN_PREFIXES = [
    ("date_", "date_selection"),
    ("almanac_", "date_selection"),
    ("oracle_lot_", "oracle_lot"),
    ("oracle_card_", "oracle_card"),
    ("cartomancy_", "cartomancy"),
    ("dice_", "dice"),
    ("tasseography_", "tasseography"),
    ("lenormand_", "lenormand"),
    ("crystal_", "crystal"),
    ("candle_", "candle"),
    ("incense_", "incense"),
    ("aroma_", "aroma"),
    ("herbal_", "herbal"),
    ("sigil_", "sigil"),
    ("dowsing_", "dowsing"),
    ("body_omen_", "body_omen"),
    ("scrying_", "scrying"),
    ("casting_lots_", "casting_lots"),
    ("cezi_", "character_divination"),
    ("flower_", "flower"),
    ("animal_omen_", "animal_omen"),
    ("aura_chakra_", "aura_chakra"),
    ("past_life_", "past_life"),
    ("moon_phase_", "moon_phase"),
    ("spirit_message_", "spirit_message"),
    ("psychometry_", "psychometry"),
    ("bibliomancy_", "bibliomancy"),
    ("sky_omen_", "sky_omen"),
    ("manifestation_", "manifestation"),
    ("pet_communication_", "pet_communication"),
    ("synchronicity_", "synchronicity"),
    ("planetary_retrograde_", "planetary_retrograde"),
    ("spiritual_protection_", "spiritual_protection"),
    ("deity_ancestor_", "deity_ancestor"),
    ("sleep_paralysis_", "sleep_paralysis"),
    ("wealth_luck_", "wealth_luck"),
    ("relationship_luck_", "relationship_luck"),
    ("consecration_", "consecration"),
    ("lost_object_", "lost_object"),
    ("sound_cleansing_", "sound_cleansing"),
    ("western_geomancy_", "western_geomancy"),
    ("nine_star_ki_", "nine_star_ki"),
    ("human_design_", "human_design"),
    ("talisman_", "talisman"),
    ("color_", "color"),
    ("zodiac_", "zodiac"),
    ("tarot_", "tarot"),
    ("fengshui_", "fengshui"),
    ("ritual_", "ritual"),
    ("folk_", "folk_custom"),
    ("yijing_", "yijing"),
    ("liuyao_", "liuyao"),
    ("meihua_", "meihua"),
    ("qimen_", "qimen"),
    ("bazi_", "mingli"),
    ("mingli_", "mingli"),
    ("naming_", "naming"),
    ("numerology_", "numerology"),
    ("pendulum_", "pendulum"),
    ("rune_", "rune"),
    ("physiognomy_", "physiognomy"),
    ("palmistry_", "physiognomy"),
    ("astrology_", "astrology"),
    ("dream_", "dream"),
]


def parse_skill_index(root: Path) -> list[dict[str, Any]]:
    index_path = root / "codex-skills" / "index.md"
    if not index_path.exists():
        return []
    skills: list[dict[str, Any]] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = INDEX_ROW_RE.match(line.strip())
        if not match:
            continue
        tools = BACKTICK_RE.findall(match.group("tools"))
        skills.append(
            {
                "skill": match.group("skill"),
                "role": match.group("role").strip(),
                "tools": tools,
                "index_path": "codex-skills/index.md",
            }
        )
    return skills


def script_tools(root: Path) -> set[str]:
    scripts_dir = root / "agent-tools" / "scripts"
    if not scripts_dir.exists():
        return set()
    return {path.stem for path in scripts_dir.glob("*.py") if not path.name.startswith("__")}


def spec_title(root: Path, spec_path: str) -> str:
    path = root / spec_path
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    return ""


def domains_for_tool(tool: str, skill_names: list[str]) -> list[str]:
    domains: set[str] = set()
    for prefix, domain in DOMAIN_PREFIXES:
        if tool.startswith(prefix):
            domains.add(domain)
    for domain, requirements in knowledge_coverage_audit.DOMAIN_REQUIREMENTS.items():
        if tool in requirements.get("tools", []):
            domains.add(domain)
        if tool in requirements.get("verification", []):
            domains.add(domain)
    if tool in knowledge_coverage_audit.COMMON_REQUIREMENTS["shared_tools"]:
        domains.add("shared")
    if not domains and skill_names:
        for skill in skill_names:
            for domain, requirements in knowledge_coverage_audit.DOMAIN_REQUIREMENTS.items():
                if requirements["skill"][0].split("/")[1] == skill:
                    domains.add(domain)
    return sorted(domains or {"shared"})


def build(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    skills = parse_skill_index(root_path)
    tools_from_index = {tool for skill in skills for tool in skill["tools"]}
    tools_from_scripts = script_tools(root_path)
    tool_names = sorted(tools_from_index | tools_from_scripts)
    skill_by_tool: dict[str, list[str]] = {}
    for skill in skills:
        for tool in skill["tools"]:
            skill_by_tool.setdefault(tool, []).append(skill["skill"])

    tools: list[dict[str, Any]] = []
    missing: list[dict[str, str]] = []
    for tool in tool_names:
        files = knowledge_coverage_audit.tool_files(tool)
        absent = [artifact for artifact, path in files.items() if not (root_path / path).exists()]
        for artifact in absent:
            missing.append({"tool": tool, "artifact": artifact, "path": files[artifact]})
        tools.append(
            {
                "name": tool,
                "script": files["script"],
                "schema": files["schema"],
                "spec": files["spec"],
                "summary": spec_title(root_path, files["spec"]),
                "skills": sorted(skill_by_tool.get(tool, [])),
                "domains": domains_for_tool(tool, skill_by_tool.get(tool, [])),
                "status": "ready" if not absent else "incomplete",
                "missing": absent,
            }
        )

    return {
        "tool": "tool_manifest_builder",
        "root": str(root_path),
        "tool_count": len(tools),
        "skill_count": len(skills),
        "is_valid": not missing,
        "tools": tools,
        "skills": skills,
        "missing": missing,
        "limits": [
            "manifest 只证明脚本、schema、spec 和 Skill 索引关系存在，不证明工具语义完全正确。",
            "Skill 蓝图安装状态由 codex_skill_installer 单独判断。",
            "backlog 工具不会进入 manifest，直到脚本、schema 和 spec 三件套齐全。",
        ],
        "next_steps": [
            "use_manifest_for_mcp_or_api_wrappers",
            "run_knowledge_coverage_audit_after_tool_changes",
            "sync_skill_index_when_adding_or_removing_tool_hooks",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    args = parser.parse_args()
    result = build(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
