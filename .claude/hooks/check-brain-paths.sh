#!/bin/bash
# Voice-rule guard: block brain-internal file paths from leaking to outbound content.
# Concepts named in those files are fine; only the path is private.

INPUT=$(cat)
if printf '%s' "$INPUT" | grep -qE '\b(00_foundation|01_strategy|02_leadership|03_ai_native_transformation|04_team_brains|07_operating_rhythms|08_metrics|09_people|10_career|11_compliance_security|12_projects|99_archive|context/knowledge)(\\)?/'; then
  cat >&2 <<'MSG'
Brain-internal file path detected in outgoing content.
Voice rule: no brain-internal path may appear in outbound (chat, email, docs, tickets, PRs). Concepts named in those files are fine. The path itself is private.
Strip the path. Write the substance directly. Retry the tool call.
MSG
  exit 2
fi
exit 0
