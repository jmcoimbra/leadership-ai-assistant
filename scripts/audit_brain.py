#!/usr/bin/env python3
"""Audit the leadership brain template for first-run readiness."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_DIRS = {
    "00_foundation",
    "01_strategy",
    "02_leadership",
    "03_ai_native_transformation",
    "04_team_brains",
    "07_operating_rhythms",
    "08_metrics",
    "09_people",
    "10_career",
    "11_compliance_security",
    "12_projects",
}
OPTIONAL_LOCAL_REFS = {
    "config/team.yaml",
    ".claude/names.txt",
    ".claude/settings.local.json",
    "01_strategy/strategic_pillars.md",
    "09_people/team_roster.md",
    "10_career/career_trajectory.md",
    "context/knowledge/learnings.jsonl",
}
PLACEHOLDER_ALLOWED = {
    "README.md",
    "FIRST_RUN.md",
    "AGENTS.md",
    "CLAUDE.md",
    "config/team.yaml.example",
    ".claude/names.txt.example",
    ".claude/commands/_preamble.md",
}

PRIVATE_ID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
HEADER_RE = re.compile(r"Owner:\s*.+\|\s*Pillar:\s*.+\|\s*Status:\s*.+\|\s*Last Audit:")
LOCAL_REF_RE = re.compile(r"`([^`]+)`|\]\(([^)]+)\)")
PUBLIC_AWS_IDS = {
    "658327ea-f89d-4fab-a63d-7e88639e58f6",
    "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_files() -> list[Path]:
    ignored = {".git", ".context"}
    return sorted(
        p
        for p in ROOT.rglob("*")
        if p.is_file() and not any(part in ignored for part in p.relative_to(ROOT).parts)
    )


def markdown_files() -> list[Path]:
    return [p for p in iter_files() if p.suffix == ".md"]


def is_core_file(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return bool(parts and parts[0] in CORE_DIRS)


def allows_placeholders(path: Path) -> bool:
    name = rel(path)
    return name in PLACEHOLDER_ALLOWED or "/_template" in name or name.endswith("/_template.md")


def check_governance(errors: list[str], warnings: list[str]) -> None:
    for path in markdown_files():
        if not is_core_file(path) or path.name == "compliance_audit.md":
            continue
        text = path.read_text(errors="ignore")
        name = rel(path)
        header = "\n".join(text.splitlines()[:4])
        if not HEADER_RE.search(header):
            errors.append(f"{name}: missing standard governance header")
        if "## AI Integration" not in text:
            errors.append(f"{name}: missing ## AI Integration")
        if not re.search(r"baseline|target|measurable|metric|outcome|→|->", text, re.I):
            warnings.append(f"{name}: no obvious measurable outcome cue")
        if not re.search(r"escalation|escalate|flagged RED|trigger", text, re.I):
            warnings.append(f"{name}: no obvious escalation cue")


def candidate_ref(raw: str) -> str | None:
    target = raw.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    if target.endswith("/") or any(token in target for token in ("[", "]", "<", ">", "...", "*", "$")):
        return None
    if re.match(r"^[a-z]+:", target):
        return None
    prefixes = (
        "00_", "01_", "02_", "03_", "04_", "07_", "08_", "09_", "10_", "11_", "12_", "99_",
        "context/", ".claude/", "config/", "scripts/", "FIRST_RUN.md", "ADAPTERS.md", "AGENTS.md",
    )
    return target if target.startswith(prefixes) else None


def check_refs(errors: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(errors="ignore")
        for match in LOCAL_REF_RE.finditer(text):
            raw = match.group(1) or match.group(2) or ""
            target = candidate_ref(raw)
            if not target or target in OPTIONAL_LOCAL_REFS:
                continue
            if not (ROOT / target).exists():
                errors.append(f"{rel(path)}: broken local reference `{target}`")


def check_private_data(errors: list[str], warnings: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(errors="ignore")
        name = rel(path)
        private_ids = {match.group(0) for match in PRIVATE_ID_RE.finditer(text)} - PUBLIC_AWS_IDS
        if private_ids:
            errors.append(f"{name}: private-looking UUID detected")
        if re.search(r"BUGS-\d+", text):
            warnings.append(f"{name}: company-specific ticket key detected")
        if "#rnd-" in text:
            warnings.append(f"{name}: company-specific channel name detected")


def check_placeholders(warnings: list[str]) -> None:
    for path in markdown_files():
        if allows_placeholders(path):
            continue
        text = path.read_text(errors="ignore")
        if re.search(r"\[[A-Z][A-Za-z0-9 /_-]+\]", text):
            warnings.append(f"{rel(path)}: placeholder remains outside an approved template file")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    strict_public = "--strict-public" in sys.argv
    strict_placeholders = "--strict-placeholders" in sys.argv
    check_governance(errors, warnings)
    check_refs(errors)
    check_private_data(errors, warnings if strict_public else [])
    if strict_placeholders:
        check_placeholders(warnings)
    if errors:
        print("ERRORS")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("WARNINGS")
        for item in warnings:
            print(f"- {item}")
    if not errors and not warnings:
        print("Audit clean: no errors or warnings.")
    elif not errors:
        print(f"Audit passed with {len(warnings)} warning(s).")
    else:
        print(f"Audit failed with {len(errors)} error(s) and {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
